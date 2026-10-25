import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Final

NEW_SETTINGS_MODE: Final = 0o600

CANONICAL_HOOKS_PREFIX: Final = "$(git rev-parse --show-toplevel)/.agents/hooks/"


class SettingsConflict(Exception):
    pass


def read_json_object(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}

    if not path.is_file():
        raise SettingsConflict(f"{path} is not a regular file")

    try:
        content: object = json.loads(path.read_text())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SettingsConflict(f"{path} is not valid JSON: {error}") from error

    if not isinstance(content, dict):
        raise SettingsConflict(f"{path} does not hold a JSON object")

    event_entries(content, path)

    return content


def event_entries(content: dict[str, object], path: Path) -> dict[str, list[dict[str, object]]]:
    hooks = content.get("hooks", {})

    if not isinstance(hooks, dict):
        raise SettingsConflict(f"{path} has a hooks value that is not an object")

    for event, entries in hooks.items():
        if not isinstance(entries, list) or not all(isinstance(entry, dict) for entry in entries):
            raise SettingsConflict(f"{path} has a malformed {event} hook list")

    return hooks


def handlers(entry: dict[str, object]) -> list[dict[str, object]]:
    grouped = entry.get("hooks")

    return grouped if isinstance(grouped, list) else [entry]


def user_level(entry: dict[str, object], hooks_dir: Path) -> dict[str, object]:
    def _relocated(handler: dict[str, object]) -> dict[str, object]:
        command = handler.get("command")

        if not isinstance(command, str):
            return handler

        return {**handler, "command": command.replace(CANONICAL_HOOKS_PREFIX, f"{hooks_dir}/")}

    if isinstance(entry.get("hooks"), list):
        return {**entry, "hooks": [_relocated(handler) for handler in handlers(entry)]}

    return _relocated(entry)


def references_missing_hook(handler: dict[str, object], hooks_dir: Path) -> bool:
    command = handler.get("command")
    prefix = f"{hooks_dir}/"

    if not isinstance(command, str) or prefix not in command:
        return False

    hook_name = command.split(prefix, 1)[1].split("/", 1)[0].strip("\"'")

    return not os.path.lexists(hooks_dir / hook_name)


def prune_missing_hooks(content: dict[str, object], hooks_dir: Path, path: Path) -> int:
    hooks = event_entries(content, path)
    removed = 0

    for event in list(hooks):
        kept_entries = []

        for entry in hooks[event]:
            kept = [handler for handler in handlers(entry) if not references_missing_hook(handler, hooks_dir)]
            removed += len(handlers(entry)) - len(kept)

            if kept and isinstance(entry.get("hooks"), list):
                kept_entries.append({**entry, "hooks": kept})
            elif kept:
                kept_entries.append(entry)

        hooks[event] = kept_entries

    return removed


def add_source_hooks(content: dict[str, object], source: dict[str, object], hooks_dir: Path, path: Path) -> int:
    if "version" in source:
        content.setdefault("version", source["version"])

    hooks = content.setdefault("hooks", {})
    added = 0

    for event, source_entries in event_entries(source, path).items():
        entries = hooks.setdefault(event, [])

        for source_entry in source_entries:
            relocated = user_level(source_entry, hooks_dir)
            registered = {handler.get("command") for entry in entries for handler in handlers(entry)}

            if all(handler.get("command") in registered for handler in handlers(relocated)):
                continue

            entries.append(relocated)
            added += 1

    return added


def write_json_object(path: Path, content: dict[str, object]) -> None:
    if path.exists():
        status = path.stat()
        mode, owner, group = status.st_mode & 0o7777, status.st_uid, status.st_gid
    else:
        status = path.parent.stat()
        mode, owner, group = NEW_SETTINGS_MODE, status.st_uid, status.st_gid

    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")

    try:
        with os.fdopen(descriptor, "w") as handle:
            json.dump(content, handle, indent=2)
            handle.write("\n")

        os.chmod(temporary, mode)

        if os.geteuid() == 0:
            os.chown(temporary, owner, group)

        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def main(arguments: list[str]) -> int:
    if len(arguments) != 4 or arguments[0] not in ("check", "install"):
        print("usage: register_hooks.py check|install TARGET SOURCE HOOKS_DIR", file=sys.stderr)

        return 2

    action = arguments[0]
    target_path = Path(os.path.realpath(arguments[1]))
    source_path = Path(arguments[2])
    hooks_dir = Path(arguments[3])

    try:
        source = read_json_object(source_path)
        target = read_json_object(target_path)
    except SettingsConflict as error:
        print(f"conflict: {error}", file=sys.stderr)

        return 1

    if action == "check":
        return 0

    removed = prune_missing_hooks(target, hooks_dir, target_path)
    added = add_source_hooks(target, source, hooks_dir, source_path)

    if added or removed:
        write_json_object(target_path, target)
        print(f"{target_path}: {added} hook registrations added, {removed} removed")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
