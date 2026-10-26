from asyncio import create_subprocess_exec, run, timeout
from asyncio.subprocess import PIPE
from json import dumps, loads
from os import chmod, chown, environ, geteuid, replace
from pathlib import Path
from shlex import quote, split
from sys import argv
from tempfile import NamedTemporaryFile

from models import (
    CodexClientInfo,
    CodexHooksQuery,
    CodexHookTrust,
    CodexInitialize,
    CodexRequest,
    CodexTrustEdit,
    CodexTrustStatus,
    CodexTrustWrite,
    InstallationMode,
)


async def trust_codex_hook(root: Path, command: str) -> None:
    """Approve only the installed shared hook through native configuration writes."""

    process = await create_subprocess_exec(
        "codex", "app-server", "--stdio",
        env={**environ, "CODEX_HOME": str(root)},
        stdin=PIPE, stdout=PIPE,
    )

    async def _request(request: CodexRequest) -> object:
        if process.stdin is None or process.stdout is None:
            raise RuntimeError("Codex app-server did not open its native transport")

        process.stdin.write((dumps(request) + "\n").encode())

        await process.stdin.drain()

        while line := await process.stdout.readline():
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
                and hook.get("eventName") == "sessionStart"
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


def owns_command(command: object, provider: str, script: Path) -> bool:
    """Recognize the complete installed refresh invocation."""

    if not isinstance(command, str):
        return False

    try:
        arguments = split(command)
    except ValueError:
        return False

    if arguments[-1:] == ["--fetch"]:
        arguments = arguments[:-1]

    if len(arguments) == 5 and arguments[0] == "env" and arguments[1].startswith("SKILLS_CLOUD_HOME="):
        arguments = arguments[2:]

    return (
        len(arguments) == 3
        and arguments[0] == "python3"
        and arguments[1] == str(script)
        and arguments[2] == provider
    )


def configure(mode: InstallationMode, provider: str, root: Path, source: Path, cloud_home: str, auto_update: bool = False) -> bool:
    """Merge the owned startup registration."""

    path = root / ("hooks.json" if provider == "codex" else "settings.json")

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

    template = loads((source / ".agents/hooks/skills-refresh/hooks.json").read_text())
    owned = template["hooks"]["SessionStart"][0]
    handler = owned["hooks"][0]
    script = root / "hooks/skills-refresh/session_start.py"
    command = ["python3", str(script), provider]

    for group in groups:
        if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
            raise ValueError(f"Invalid SessionStart group in {path}")

        for item in group["hooks"]:
            if isinstance(item, dict) and owns_command(item.get("command"), provider, script):
                auto_update = auto_update or split(item["command"])[-1:] == ["--fetch"]

    if auto_update:
        command.append("--fetch")

    if cloud_home:
        command = ["env", f"SKILLS_CLOUD_HOME={cloud_home}", *command]

    handler["command"] = " ".join(quote(argument) for argument in command)
    retained = []

    for group in groups:
        if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
            raise ValueError(f"Invalid SessionStart group in {path}")

        handlers = [item for item in group["hooks"] if not (
            isinstance(item, dict) and owns_command(item.get("command"), provider, script)
        )]

        if handlers:
            retained.append({**group, "hooks": handlers})

    hooks["SessionStart"] = [*retained, owned]
    original = loads(path.read_text()) if path.exists() else {}
    changed = document != original

    if not changed or mode != InstallationMode.APPLY:
        if mode == InstallationMode.APPLY and auto_update and provider == "codex":
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

    if auto_update and provider == "codex":
        run(trust_codex_hook(root, handler["command"]))

    return True


if __name__ == "__main__":
    mode = InstallationMode(argv[1])
    changed = configure(mode, argv[2], Path(argv[3]), Path(argv[4]), argv[5], argv[6:7] == ["1"])

    raise SystemExit(3 if changed and mode == InstallationMode.CHECK else 0)
