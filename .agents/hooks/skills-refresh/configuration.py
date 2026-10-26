from json import dumps, loads
from os import chmod, chown, geteuid, replace
from pathlib import Path
from shlex import quote, split
from sys import argv
from tempfile import NamedTemporaryFile

from models import InstallationMode


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

    return True


if __name__ == "__main__":
    mode = InstallationMode(argv[1])
    changed = configure(mode, argv[2], Path(argv[3]), Path(argv[4]), argv[5], argv[6:7] == ["1"])

    raise SystemExit(3 if changed and mode == InstallationMode.CHECK else 0)
