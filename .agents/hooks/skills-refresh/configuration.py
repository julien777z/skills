from asyncio import StreamReader, StreamWriter, create_subprocess_exec, run, timeout
from asyncio.subprocess import PIPE
from json import dumps, loads
from os import chmod, chown, environ, geteuid, replace
from pathlib import Path
from shlex import quote, split
from sys import argv
from tempfile import NamedTemporaryFile
from typing import cast

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
    """Merge the owned startup registration."""

    path = root / ("hooks.json" if provider == Provider.CODEX else "settings.json")

    if path.is_symlink():
        raise ValueError(f"Hook configuration must be a regular file: {path}")

    document = loads(path.read_text()) if path.exists() else {}

    if not isinstance(document, dict):
        raise ValueError(f"Expected a JSON object in {path}")

    hooks = document.setdefault("hooks", {})

    if not isinstance(hooks, dict):
        raise ValueError(f"Expected a hooks object in {path}")

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

    root.mkdir(parents=True, exist_ok=True)

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
