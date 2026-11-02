import argparse
import json
import os
import sys
import tempfile
from enum import StrEnum
from pathlib import Path
from typing import Final

NEW_SETTINGS_MODE: Final[int] = 0o600
CANONICAL_HOOKS_PREFIX: Final[str] = "$(git rev-parse --show-toplevel)/.agents/hooks/"
CONFLICT_EXIT: Final[int] = 1


class RegistrationCommand(StrEnum):
    """An operation the script runs on one settings file."""

    CHECK = "check"
    INSTALL = "install"


class SettingsConflict(Exception):
    """A settings file the installer cannot reconcile."""


def read_json_object(path: Path) -> dict[str, object]:
    """Read a settings file as a JSON object, empty when the file is absent."""

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

    return content


def event_entries(content: dict[str, object], path: Path) -> dict[str, list[dict[str, object]]]:
    """Return a settings object's hook entries by event."""

    hooks = content.get("hooks", {})

    if not isinstance(hooks, dict):
        raise SettingsConflict(f"{path} has a hooks value that is not an object")

    for event, entries in hooks.items():
        if not isinstance(entries, list) or not all(isinstance(entry, dict) for entry in entries):
            raise SettingsConflict(f"{path} has a malformed {event} hook list")

    return hooks


def entry_handlers(entry: dict[str, object]) -> list[dict[str, object]] | None:
    """Return a grouped entry's handlers, or None for an entry that is one handler."""

    grouped = entry.get("hooks")

    return grouped if isinstance(grouped, list) else None


def relocated_handler(handler: dict[str, object], hooks_dir: Path, path: Path) -> dict[str, object]:
    """Point a source handler's command at the hooks linked into the user-level root."""

    command = handler.get("command")

    if not isinstance(command, str) or CANONICAL_HOOKS_PREFIX not in command:
        raise SettingsConflict(f"{path} has a hook command outside {CANONICAL_HOOKS_PREFIX}")

    return {**handler, "command": command.replace(CANONICAL_HOOKS_PREFIX, f"{hooks_dir}/")}


def relocated_entry(entry: dict[str, object], hooks_dir: Path, path: Path) -> dict[str, object]:
    """Point every handler of a source entry at the linked hooks."""

    handlers = entry_handlers(entry)

    if handlers is None:
        return relocated_handler(entry, hooks_dir, path)

    return {**entry, "hooks": [relocated_handler(handler, hooks_dir, path) for handler in handlers]}


def is_installer_handler(handler: dict[str, object], hooks_dir: Path, repo_root: Path) -> bool:
    """Tell whether a handler runs a hook the installer links or has since unlinked."""

    command = handler.get("command")
    prefix = f"{hooks_dir}/"

    if not isinstance(command, str) or prefix not in command:
        return False

    hook = hooks_dir / command.split(prefix, 1)[1].split("/", 1)[0]

    if not os.path.lexists(hook):
        return True

    return hook.is_symlink() and hook.resolve().is_relative_to(repo_root)


def without_installer_handlers(
    entries: list[dict[str, object]], hooks_dir: Path, repo_root: Path
) -> list[dict[str, object]]:
    """Drop the installer's handlers from one event's entries, keeping the user's."""

    kept_entries: list[dict[str, object]] = []

    for entry in entries:
        handlers = entry_handlers(entry)

        if handlers is None:
            if not is_installer_handler(entry, hooks_dir, repo_root):
                kept_entries.append(entry)

            continue

        kept = [
            handler
            for handler in handlers
            if not is_installer_handler(handler, hooks_dir, repo_root)
        ]

        if kept:
            kept_entries.append({**entry, "hooks": kept})

    return kept_entries


def reconciled(
    target: dict[str, object],
    target_path: Path,
    source: dict[str, object],
    source_path: Path,
    hooks_dir: Path,
    repo_root: Path,
) -> dict[str, object]:
    """Return the target settings with exactly the source's hooks registered for the installer."""

    target_hooks = event_entries(target, target_path)
    source_hooks = event_entries(source, source_path)
    hooks: dict[str, list[dict[str, object]]] = {}

    for event, entries in target_hooks.items():
        kept = without_installer_handlers(entries, hooks_dir, repo_root)

        if kept or not entries:
            hooks[event] = kept

    for event, entries in source_hooks.items():
        hooks.setdefault(event, []).extend(
            relocated_entry(entry, hooks_dir, source_path) for entry in entries
        )

    result = dict(target)

    if hooks or "hooks" in target:
        result["hooks"] = hooks

    if source_hooks and "version" in source:
        result.setdefault("version", source["version"])

    return result


def write_json_object(path: Path, content: dict[str, object]) -> None:
    """Atomically replace a settings file, keeping its mode and owner."""

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


def parse_arguments() -> argparse.Namespace:
    """Parse the command and the files it reconciles."""

    files = argparse.ArgumentParser(add_help=False)

    files.add_argument("--target", type=Path, required=True, help="User-level settings file.")
    files.add_argument("--source", type=Path, required=True, help="Generated hook registrations.")
    files.add_argument("--hooks-dir", type=Path, required=True, help="User-level hooks directory.")
    files.add_argument(
        "--repo-root", type=Path, required=True, help="Checkout the hooks link into."
    )

    parser = argparse.ArgumentParser(
        description="Register the linked hooks in a user-level settings file."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser(
        RegistrationCommand.CHECK,
        parents=[files],
        help="Report a settings file the installer cannot reconcile.",
    )
    commands.add_parser(
        RegistrationCommand.INSTALL,
        parents=[files],
        help="Register the source's hooks, replacing the installer's earlier registrations.",
    )

    return parser.parse_args()


def main() -> int:
    """Check or install the hook registrations of one user-level root."""

    arguments = parse_arguments()
    command = RegistrationCommand(arguments.command)
    target_path = Path(os.path.realpath(arguments.target))
    source_path: Path = arguments.source

    try:
        target = read_json_object(target_path)
        content = reconciled(
            target,
            target_path,
            read_json_object(source_path),
            source_path,
            arguments.hooks_dir,
            arguments.repo_root.resolve(),
        )
    except SettingsConflict as error:
        print(f"conflict: {error}", file=sys.stderr)

        return CONFLICT_EXIT

    if command is RegistrationCommand.INSTALL and content != target:
        write_json_object(target_path, content)

        print(f"{target_path}: hook registrations updated")

    return 0


if __name__ == "__main__":
    sys.exit(main())
