import json
import os
import re
import sys
import tempfile
from pathlib import Path

NEW_SETTINGS_MODE = 0o600


class SettingsConflict(Exception):
    pass


def read_settings(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}

    if not path.is_file():
        raise SettingsConflict(f"{path} is not a regular file")

    try:
        settings: object = json.loads(path.read_text())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SettingsConflict(f"{path} is not valid JSON: {error}") from error

    if not isinstance(settings, dict):
        raise SettingsConflict(f"{path} does not hold a JSON object")

    hook_groups(settings, path)

    return settings


def hook_groups(settings: dict[str, object], path: Path) -> dict[str, list[dict[str, object]]]:
    hooks = settings.get("hooks", {})

    if not isinstance(hooks, dict):
        raise SettingsConflict(f"{path} has a hooks value that is not an object")

    for event, groups in hooks.items():
        if not isinstance(groups, list) or not all(
            isinstance(group, dict)
            and isinstance(group.get("hooks"), list)
            and all(isinstance(handler, dict) for handler in group["hooks"])
            for group in groups
        ):
            raise SettingsConflict(f"{path} has a malformed {event} hook list")

    return hooks


def handler_command(handler: object) -> object:
    return handler.get("command") if isinstance(handler, dict) else None


def prune_missing_hooks(settings: dict[str, object], hooks_dir: Path) -> int:
    reference = re.compile(re.escape(f"$HOME/{hooks_dir.parent.name}/hooks/") + r"([^\"'\s]+)")
    removed = 0

    def _references_missing_hook(handler: dict[str, object]) -> bool:
        command = handler_command(handler)
        match = reference.search(command) if isinstance(command, str) else None

        return match is not None and not os.path.lexists(hooks_dir / match.group(1))

    hooks = hook_groups(settings, hooks_dir)

    for event in list(hooks):
        for group in hooks[event]:
            kept = [handler for handler in group["hooks"] if not _references_missing_hook(handler)]
            removed += len(group["hooks"]) - len(kept)
            group["hooks"] = kept

        hooks[event] = [group for group in hooks[event] if group["hooks"]]

        if not hooks[event]:
            del hooks[event]

    return removed


def add_source_hooks(settings: dict[str, object], source: dict[str, object], path: Path) -> int:
    source_hooks = hook_groups(source, path)

    if not source_hooks:
        return 0

    hooks = settings.setdefault("hooks", {})
    added = 0

    for event, source_groups in source_hooks.items():
        groups = hooks.setdefault(event, [])

        for source_group in source_groups:
            registered = {
                handler_command(handler) for group in groups for handler in group["hooks"]
            }
            missing = [
                handler
                for handler in source_group["hooks"]
                if handler_command(handler) not in registered
            ]

            if not missing:
                continue

            matcher = source_group.get("matcher")
            target = next((group for group in groups if group.get("matcher") == matcher), None)

            if target is None:
                target = {**source_group, "hooks": []}
                groups.append(target)

            target["hooks"].extend(missing)
            added += len(missing)

    return added


def write_settings(path: Path, settings: dict[str, object]) -> None:
    if path.exists():
        status = path.stat()
        mode, owner, group = status.st_mode & 0o7777, status.st_uid, status.st_gid
    else:
        status = path.parent.stat()
        mode, owner, group = NEW_SETTINGS_MODE, status.st_uid, status.st_gid

    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")

    try:
        with os.fdopen(descriptor, "w") as handle:
            json.dump(settings, handle, indent=2)
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
        print(
            "usage: register_hooks.py check|install SETTINGS SOURCE HOOKS_DIR",
            file=sys.stderr,
        )

        return 2

    action = arguments[0]
    settings_path = Path(os.path.realpath(arguments[1]))
    source_path = Path(arguments[2])
    hooks_dir = Path(arguments[3])

    try:
        source = read_settings(source_path)
        settings = read_settings(settings_path)
    except SettingsConflict as error:
        print(f"conflict: {error}", file=sys.stderr)

        return 1

    if action == "check":
        return 0

    removed = prune_missing_hooks(settings, hooks_dir)
    added = add_source_hooks(settings, source, source_path)

    if added or removed:
        write_settings(settings_path, settings)
        print(f"{settings_path}: {added} hook registrations added, {removed} removed")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
