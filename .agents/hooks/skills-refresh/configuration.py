"""Merge the owned startup hook into provider configuration without replacing other hooks."""

from json import dumps, loads
from os import chmod, chown, geteuid, replace
from pathlib import Path
from shlex import quote
from sys import argv
from tempfile import NamedTemporaryFile


def configure(mode: str, provider: str, root: Path, source: Path) -> bool:
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
    handler["command"] = " ".join([
        "python3", quote(str(root / "hooks/skills-refresh/session_start.py")), provider,
    ])
    retained = []

    for group in groups:
        if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
            raise ValueError(f"Invalid SessionStart group in {path}")

        handlers = [item for item in group["hooks"] if not (
            isinstance(item, dict) and item.get("statusMessage") == handler["statusMessage"]
            and isinstance(item.get("command"), str)
            and "/hooks/skills-refresh/session_start.py" in item["command"]
        )]

        if handlers:
            retained.append({**group, "hooks": handlers})

    hooks["SessionStart"] = [*retained, owned]
    original = loads(path.read_text()) if path.exists() else {}
    changed = document != original

    if not changed or mode != "apply":
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
    changed = configure(argv[1], argv[2], Path(argv[3]), Path(argv[4]))
    raise SystemExit(3 if changed and argv[1] == "check" else 0)
