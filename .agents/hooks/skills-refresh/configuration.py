from asyncio import StreamReader, StreamWriter, create_subprocess_exec, run, timeout
from asyncio.subprocess import PIPE
from contextlib import ExitStack
from fcntl import LOCK_EX, flock
from json import dumps, loads
from os import chmod, chown, environ, geteuid, replace
from pathlib import Path
from re import Pattern, compile
from shlex import quote, split
from sys import argv
from tempfile import NamedTemporaryFile
from typing import Final, cast

from models import (
    CodexClientInfo,
    CodexHooksQuery,
    CodexHookTrust,
    CodexInitialize,
    CodexRequest,
    CodexTrustEdit,
    CodexTrustStatus,
    CodexTrustWrite,
    HookCommand,
    HookGroup,
    HookEventName,
    Provider,
    InstallationMode,
)


SOURCE_COMMAND: Final[Pattern[str]] = compile(
    r'python3 "\$\(git rev-parse --show-toplevel\)/\.agents/hooks/([\w-]+)/main\.py"'
)


def is_managed_handler(handler: dict[str, object], hooks_dir: Path) -> bool:
    """Identify an exact linked-hook command owned by the installer."""

    command = handler.get("command")

    if not isinstance(command, str):
        return False

    try:
        words = split(command)
    except ValueError:
        return False

    if len(words) != 2:
        return False

    hook = Path(words[1])

    return (
        hook.name == "main.py"
        and hook.parent.parent == hooks_dir
        and SOURCE_COMMAND.fullmatch(
            f'python3 "$(git rev-parse --show-toplevel)/.agents/hooks/{hook.parent.name}/main.py"'
        ) is not None
        and command == f"python3 {quote(str(hook))}"
    )


def reconcile_generated_hooks(document: dict[str, object], provider: Provider, root: Path, source: Path) -> dict[str, object]:
    """Reconcile generated events alongside the native startup registration."""

    filename = "settings.json" if provider == Provider.CLAUDE else "hooks.json"
    source_path = source / ".agents/.auto_generated" / f".{provider}" / filename
    generated = loads(source_path.read_text())
    hooks = document.setdefault("hooks", {})

    if not isinstance(hooks, dict):
        raise ValueError(f"Expected a hooks object in {root / filename}")

    for event, entries in list(hooks.items()):
        if event in (HookEventName.SESSION_START, HookEventName.SESSION_START_CAMEL):
            continue

        if not isinstance(entries, list) or not all(isinstance(entry, dict) for entry in entries):
            raise ValueError(f"Invalid {event} hook list in {root / filename}")

        kept = []

        for entry in entries:
            handlers = entry.get("hooks")

            if isinstance(handlers, list):
                remaining = [handler for handler in handlers if not is_managed_handler(handler, root / "hooks")]

                if remaining:
                    kept.append({**entry, "hooks": remaining})
            elif not is_managed_handler(entry, root / "hooks"):
                kept.append(entry)

        if kept or not entries:
            hooks[event] = kept
        else:
            del hooks[event]

    for event, entries in generated.get("hooks", {}).items():
        if event in (HookEventName.SESSION_START, HookEventName.SESSION_START_CAMEL):
            continue

        for entry in entries:
            handlers = entry.get("hooks")
            relocated = []

            for handler in handlers if isinstance(handlers, list) else [entry]:
                match = SOURCE_COMMAND.fullmatch(handler["command"])

                if match is None:
                    raise ValueError(f"Invalid generated hook command in {source_path}: {handler['command']}")

                command = f"python3 {quote(str(root / 'hooks' / match.group(1) / 'main.py'))}"
                relocated.append({**handler, "command": command})

            hooks.setdefault(event, []).append(
                {**entry, "hooks": relocated} if isinstance(handlers, list) else relocated[0]
            )

    if "version" in generated:
        document.setdefault("version", generated["version"])

    return hooks


async def trust_codex_hook(root: Path, command: str) -> None:
    """Approve only the installed shared hook through native configuration writes."""

    process = await create_subprocess_exec(
        "codex", "app-server", "--stdio",
        env={**environ, "CODEX_HOME": str(root)},
        stdin=PIPE, stdout=PIPE,
    )

    # PIPE guarantees both streams; Process typing does not encode the pipe modes.
    input_stream = cast(StreamWriter, process.stdin)
    output_stream = cast(StreamReader, process.stdout)

    async def _request(request: CodexRequest) -> object:
        input_stream.write((dumps(request) + "\n").encode())

        await input_stream.drain()

        while line := await output_stream.readline():
            response = loads(line)

            if response.get("id") != request["id"]:
                continue

            if "error" in response:
                raise RuntimeError(f"Codex {request['method']} failed: {dumps(response['error'])}")

            return response["result"]

        raise RuntimeError(f"Codex transport closed during {request['method']}")

    try:
        async with timeout(30):
            await _request(CodexRequest(
                id=1, method="initialize",
                params=CodexInitialize(clientInfo=CodexClientInfo(name="skills-installer", version="1")),
            ))

            listing = await _request(CodexRequest(
                id=2, method="hooks/list", params=CodexHooksQuery(cwds=[str(root.parent)]),
            ))

            if not isinstance(listing, dict) or not isinstance(listing.get("data"), list):
                raise ValueError(f"Invalid Codex hook listing: {listing!r}")

            owned = [
                hook
                for entry in listing["data"]
                for hook in entry["hooks"]
                if hook.get("command") == command
                and hook.get("eventName") == HookEventName.SESSION_START_CAMEL
                and hook.get("sourcePath") == str(root / "hooks.json")
            ]

            if len(owned) != 1:
                raise ValueError("Codex must identify exactly one installed shared startup hook")

            hook = owned[0]

            if hook["trustStatus"] == CodexTrustStatus.TRUSTED:
                return

            await _request(CodexRequest(
                id=3, method="config/batchWrite",
                params=CodexTrustWrite(
                    edits=[CodexTrustEdit(
                        keyPath="hooks.state",
                        value={hook["key"]: CodexHookTrust(trusted_hash=hook["currentHash"])},
                        mergeStrategy="upsert",
                    )],
                    reloadUserConfig=True,
                ),
            ))

            verified = await _request(CodexRequest(
                id=4, method="hooks/list", params=CodexHooksQuery(cwds=[str(root.parent)]),
            ))

            if not isinstance(verified, dict) or not any(
                candidate.get("key") == hook["key"]
                and candidate.get("trustStatus") == CodexTrustStatus.TRUSTED
                for entry in verified["data"] for candidate in entry["hooks"]
            ):
                raise RuntimeError("Codex did not retain the shared startup hook trust")
    finally:
        if process.returncode is None:
            process.terminate()

        await process.wait()


def owned_arguments(command: object, provider: Provider, script: Path) -> list[str] | None:
    """Return parsed arguments only for the complete installed refresh invocation."""

    if not isinstance(command, str):
        return None

    try:
        parsed = split(command)
    except ValueError:
        return None

    arguments = parsed[:-1] if parsed[-1:] == ["--fetch"] else parsed

    if len(arguments) == 5 and arguments[0] == "env" and arguments[1].startswith("SKILLS_CLOUD_HOME="):
        arguments = arguments[2:]

    if (
        len(arguments) == 3
        and arguments[0] == "python3"
        and arguments[1] == str(script)
        and arguments[2] == provider
    ):
        return parsed

    return None


def configure(mode: InstallationMode, provider: Provider, root: Path, source: Path, cloud_home: str, auto_update: bool = False, approve_owned_hooks: bool = False) -> bool:
    """Reconcile generated hooks and the native startup registration."""

    path = root / ("settings.json" if provider == Provider.CLAUDE else "hooks.json")

    with ExitStack() as resources:
        if mode == InstallationMode.APPLY:
            root.mkdir(parents=True, exist_ok=True)
            lock_path = root / "skills-refresh.lock"
            lock = resources.enter_context(lock_path.open("a"))
            chmod(lock_path, 0o600)

            if geteuid() == 0:
                owner = path.stat() if path.exists() else root.stat()
                chown(lock_path, owner.st_uid, owner.st_gid)

            flock(lock, LOCK_EX)

        if path.is_symlink():
            raise ValueError(f"Hook configuration must be a regular file: {path}")

        document = loads(path.read_text()) if path.exists() else {}

        if not isinstance(document, dict):
            raise ValueError(f"Expected a JSON object in {path}")

        hooks = reconcile_generated_hooks(document, provider, root, source)

        if provider != Provider.CURSOR:
            groups = hooks.setdefault("SessionStart", [])

            if not isinstance(groups, list):
                raise ValueError(f"Expected a SessionStart array in {path}")

            template = loads((source / ".agents/hooks/hooks.json").read_text())
            canonical_script = "$(git rev-parse --show-toplevel)/.agents/hooks/skills-refresh/session_start.py"
            registrations = [
                (group, handler)
                for group in template["hooks"]["SessionStart"]
                for handler in group["hooks"]
                if split(handler["command"]) == ["python3", canonical_script, "{{harness}}"]
            ]

            if len(registrations) != 1:
                raise ValueError("Shared startup hook requires exactly one canonical registration")

            group_template, handler_template = registrations[0]
            script = root / "hooks/skills-refresh/session_start.py"
            command = ["python3", str(script), provider]

            retained = []

            for group in groups:
                if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
                    raise ValueError(f"Invalid SessionStart group in {path}")

                handlers = []

                for item in group["hooks"]:
                    arguments = owned_arguments(item.get("command"), provider, script) if isinstance(item, dict) else None

                    if arguments is None:
                        handlers.append(item)
                    else:
                        auto_update = auto_update or arguments[-1:] == ["--fetch"]

                if handlers:
                    retained.append({**group, "hooks": handlers})

            if auto_update:
                command.append("--fetch")

            if cloud_home:
                command = ["env", f"SKILLS_CLOUD_HOME={cloud_home}", *command]

            handler = HookCommand(
                type="command",
                command=" ".join(quote(argument) for argument in command),
                timeout=handler_template["timeout"],
                statusMessage="Checking installed shared skills",
            )
            owned = HookGroup(matcher=group_template["matcher"], hooks=[handler])
            hooks["SessionStart"] = [*retained, owned]

        original = loads(path.read_text()) if path.exists() else {}
        changed = document != original

        if not changed or mode != InstallationMode.APPLY:
            if mode == InstallationMode.APPLY and (auto_update or approve_owned_hooks) and provider == Provider.CODEX:
                run(trust_codex_hook(root, handler["command"]))

            return changed

        with NamedTemporaryFile(mode="w", dir=root, delete=False) as temporary:
            temporary.write(dumps(document, indent=2) + "\n")
            temporary_path = Path(temporary.name)

        chmod(temporary_path, path.stat().st_mode & 0o777 if path.exists() else 0o600)

        if geteuid() == 0:
            owner = path.stat() if path.exists() else root.stat()
            chown(temporary_path, owner.st_uid, owner.st_gid)

        replace(temporary_path, path)

        if (auto_update or approve_owned_hooks) and provider == Provider.CODEX:
            run(trust_codex_hook(root, handler["command"]))

        return True


if __name__ == "__main__":
    mode = InstallationMode(argv[1])
    changed = configure(mode, Provider(argv[2]), Path(argv[3]), Path(argv[4]), argv[5], argv[6:7] == ["1"], argv[7:8] == ["1"])

    raise SystemExit(3 if changed and mode == InstallationMode.CHECK else 0)
