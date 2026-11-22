import argparse
import json
import os
import re
import shlex
import sys
import tempfile
from enum import StrEnum
from pathlib import Path
from typing import Final

NEW_SETTINGS_MODE: Final[int] = 0o600
SOURCE_COMMAND_PATTERN: Final[re.Pattern[str]] = re.compile(
    r'python3 "\$\(git rev-parse --show-toplevel\)/\.agents/hooks/([\w-]+)/main\.py"((?: [\w-]+)*)'
)
HOOK_NAME_PATTERN: Final[re.Pattern[str]] = re.compile(r"[\w-]+")
HOOK_ENTRY_POINT: Final[str] = "main.py"
CONFLICT_EXIT: Final[int] = 1
# Agent Sync's own notes and the hooks, which are reconciled separately, are never merged as settings.
UNMERGED_KEYS: Final[frozenset[str]] = frozenset({"$comment", "hooks"})
RECORD_KEYS: Final[str] = "keys"
RECORD_WRITTEN: Final[str] = "written"
RECORD_PREVIOUS: Final[str] = "previous"
RECORD_EARLIER: Final[str] = "earlier"


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


def installer_command(hooks_dir: Path, name: str, arguments: list[str]) -> str:
    """Return the command that runs one linked hook with its arguments from the hooks directory."""

    return shlex.join(["python3", str(hooks_dir / name / HOOK_ENTRY_POINT), *arguments])


def relocated_handler(handler: dict[str, object], hooks_dir: Path, path: Path) -> dict[str, object]:
    """Point a source handler's command at the hooks linked into the user-level root."""

    command = handler.get("command")
    match = SOURCE_COMMAND_PATTERN.fullmatch(command) if isinstance(command, str) else None

    if match is None:
        raise SettingsConflict(f"{path} has a hook command that is not a generated hook command")

    arguments = match.group(2).split()

    return {**handler, "command": installer_command(hooks_dir, match.group(1), arguments)}


def relocated_entry(entry: dict[str, object], hooks_dir: Path, path: Path) -> dict[str, object]:
    """Point every handler of a source entry at the linked hooks."""

    handlers = entry_handlers(entry)

    if handlers is None:
        return relocated_handler(entry, hooks_dir, path)

    return {**entry, "hooks": [relocated_handler(handler, hooks_dir, path) for handler in handlers]}


def is_installer_handler(handler: dict[str, object], hooks_dir: Path) -> bool:
    """Tell whether a handler's command is one the installer writes for this hooks folder."""

    command = handler.get("command")

    if not isinstance(command, str):
        return False

    try:
        words = shlex.split(command)
    except ValueError:
        return False

    if len(words) < 2:
        return False

    hook = Path(words[1])
    name = hook.parent.name
    arguments = words[2:]

    return (
        hook.name == HOOK_ENTRY_POINT
        and hook.parent.parent == hooks_dir
        and all(HOOK_NAME_PATTERN.fullmatch(word) is not None for word in (name, *arguments))
        and command == installer_command(hooks_dir, name, arguments)
    )


def without_installer_handlers(
    entries: list[dict[str, object]], hooks_dir: Path
) -> list[dict[str, object]]:
    """Drop the installer's handlers from one event's entries, keeping the user's."""

    kept_entries: list[dict[str, object]] = []

    for entry in entries:
        handlers = entry_handlers(entry)

        if handlers is None:
            if not is_installer_handler(entry, hooks_dir):
                kept_entries.append(entry)

            continue

        kept = [handler for handler in handlers if not is_installer_handler(handler, hooks_dir)]

        if kept:
            kept_entries.append({**entry, "hooks": kept})

    return kept_entries


def reconciled(
    target: dict[str, object],
    target_path: Path,
    source: dict[str, object],
    source_path: Path,
    hooks_dir: Path,
) -> dict[str, object]:
    """Return the target settings with exactly the source's hooks registered for the installer."""

    target_hooks = event_entries(target, target_path)
    source_hooks = event_entries(source, source_path)
    hooks: dict[str, list[dict[str, object]]] = {}

    for event, entries in target_hooks.items():
        kept = without_installer_handlers(entries, hooks_dir)

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


def read_settings_record(path: Path) -> dict[str, dict[str, object]]:
    """Read the settings the installer wrote, with any value each replaced, by key."""

    entries = read_json_object(path).get(RECORD_KEYS, {})

    if not isinstance(entries, dict) or not all(
        isinstance(entry, dict) and RECORD_WRITTEN in entry for entry in entries.values()
    ):
        raise SettingsConflict(f"{path} does not hold the installer's settings record")

    return entries


def is_installer_value(entry: dict[str, object], value: object) -> bool:
    """Tell whether a value is one the installer wrote for a recorded key."""

    return value == entry[RECORD_WRITTEN] or (
        RECORD_EARLIER in entry and value == entry[RECORD_EARLIER]
    )


def merged_settings(
    target: dict[str, object], source: dict[str, object], record: dict[str, dict[str, object]]
) -> tuple[dict[str, object], dict[str, dict[str, object]], dict[str, dict[str, object]]]:
    """Return the target with the source's settings applied, the record of what was written, and
    the record to hold while the target is replaced.

    The held record recognizes the installer's values in both the current target and the new one,
    so a run interrupted between the two writes recovers every replaced value when it is rerun.
    """

    settings = {key: value for key, value in source.items() if key not in UNMERGED_KEYS}
    result = dict(target)
    written: dict[str, dict[str, object]] = {}
    pending: dict[str, dict[str, object]] = {}

    for key, entry in record.items():
        if key in settings or key not in result or not is_installer_value(entry, result[key]):
            continue

        pending[key] = entry

        if RECORD_PREVIOUS in entry:
            result[key] = entry[RECORD_PREVIOUS]
        else:
            del result[key]

    for key, value in settings.items():
        entry = record.get(key)
        current = result.get(key)
        is_installed = entry is not None and key in result and is_installer_value(entry, current)

        if entry is not None and is_installed:
            replaced = {RECORD_PREVIOUS: entry[RECORD_PREVIOUS]} if RECORD_PREVIOUS in entry else {}
        elif key in result:
            replaced = {RECORD_PREVIOUS: current}
        else:
            replaced = {}

        result[key] = value
        written[key] = {RECORD_WRITTEN: value, **replaced}
        earlier = {RECORD_EARLIER: current} if is_installed and current != value else {}
        pending[key] = {**written[key], **earlier}

    return result, written, pending


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
    files.add_argument("--source", type=Path, required=True, help="Generated settings file.")
    files.add_argument("--hooks-dir", type=Path, required=True, help="User-level hooks directory.")
    files.add_argument(
        "--settings-record",
        type=Path,
        help="File recording the settings the installer merged and the values they replaced.",
    )

    parser = argparse.ArgumentParser(
        description="Reconcile the generated hooks and settings into a user-level settings file."
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
        help="Apply the source's hooks and settings, replacing what the installer wrote earlier.",
    )

    return parser.parse_args()


def main() -> int:
    """Check or install the hooks and settings of one user-level root."""

    arguments = parse_arguments()
    command = RegistrationCommand(arguments.command)
    target_path = Path(os.path.realpath(arguments.target))
    source_path: Path = arguments.source
    record_path: Path | None = arguments.settings_record
    record: dict[str, dict[str, object]] = {}
    written: dict[str, dict[str, object]] = {}
    pending: dict[str, dict[str, object]] = {}

    try:
        target = read_json_object(target_path)
        source = read_json_object(source_path)
        content = reconciled(
            target,
            target_path,
            source,
            source_path,
            Path(os.path.abspath(arguments.hooks_dir)),
        )

        if record_path is not None:
            record = read_settings_record(record_path)
            content, written, pending = merged_settings(content, source, record)
    except SettingsConflict as error:
        print(f"conflict: {error}", file=sys.stderr)

        return CONFLICT_EXIT

    if command is not RegistrationCommand.INSTALL:
        return 0

    if record_path is not None and pending != record:
        write_json_object(record_path, {RECORD_KEYS: pending})

    if content != target:
        write_json_object(target_path, content)

        print(f"{target_path}: hooks and settings updated")

    if record_path is not None and written != pending:
        write_json_object(record_path, {RECORD_KEYS: written})

    return 0


if __name__ == "__main__":
    sys.exit(main())
