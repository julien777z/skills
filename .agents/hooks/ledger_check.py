#!/usr/bin/env python3
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Final, TypedDict

try:
    import yaml
except ImportError:
    yaml = None

LEDGER_DIRECTORY_NAME: Final = "agent-ledgers"
LEDGER_SUFFIXES: Final = (".yaml", ".yml")
CHECK_SUFFIX: Final = ".ledger-check"

GUIDANCE_CORRECTION: Final = "guidance_correction"
BACKUP_KINDS: Final = frozenset({GUIDANCE_CORRECTION, "plan", "decision", "question"})
SKIPPED_STATUSES: Final = frozenset(
    {"awaiting_action_verification", "withdrawn", "complete", "delivered", "merged"}
)
AWAITING_PULL_REQUEST: Final = "awaiting_pull_request"

BLOCK_EXIT: Final = 2
UNCHECKED_EXIT: Final = 1


class HookInput(TypedDict, total=False):
    stop_hook_active: bool
    transcript_path: str


class BackupRecord(TypedDict):
    id: str
    kind: str
    statuses: frozenset[str]
    has_commit: bool
    urls: frozenset[str]
    awaits_pull_request: bool


class LedgerStamp(TypedDict):
    path: str
    size: int
    mtime_ns: int


class LedgerFormatError(Exception):
    pass


def read_hook_input() -> HookInput:
    if sys.stdin is None or sys.stdin.isatty():
        return HookInput()

    try:
        payload: object = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return HookInput()

    if not isinstance(payload, dict):
        return HookInput()

    hook_input = HookInput()

    if payload.get("stop_hook_active") is True:
        hook_input["stop_hook_active"] = True

    transcript_path = payload.get("transcript_path")

    if isinstance(transcript_path, str):
        hook_input["transcript_path"] = transcript_path

    return hook_input


def ledger_directory() -> Path:
    state_home = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")

    return Path(state_home) / LEDGER_DIRECTORY_NAME


def discover_ledgers(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []

    return sorted(
        path
        for path in directory.iterdir()
        if path.suffix in LEDGER_SUFFIXES and not path.name.startswith(".") and path.is_file()
    )


def remove_orphaned_stamps(directory: Path) -> None:
    for stamp in directory.glob(f"*{CHECK_SUFFIX}"):
        if not stamp.with_name(stamp.name.removesuffix(CHECK_SUFFIX)).exists():
            stamp.unlink(missing_ok=True)


def select_session_ledgers(ledgers: list[Path], hook_input: HookInput) -> list[Path]:
    transcript_path = hook_input.get("transcript_path")

    if not transcript_path:
        return ledgers

    try:
        transcript = Path(transcript_path).read_bytes()
    except OSError:
        return ledgers

    return [
        ledger
        for ledger in ledgers
        if f"{LEDGER_DIRECTORY_NAME}/{ledger.name}".encode() in transcript
    ]


def stamp_path(ledger: Path) -> Path:
    return ledger.with_name(f"{ledger.name}{CHECK_SUFFIX}")


def current_stamp(ledger: Path) -> LedgerStamp:
    status = ledger.stat()

    return LedgerStamp(path=str(ledger), size=status.st_size, mtime_ns=status.st_mtime_ns)


def is_unchanged_since_clean_check(ledger: Path, stamp: LedgerStamp) -> bool:
    try:
        recorded: object = json.loads(stamp_path(ledger).read_text())
    except (OSError, json.JSONDecodeError):
        return False

    return recorded == stamp


def record_clean_check(ledger: Path, stamp: LedgerStamp) -> None:
    try:
        descriptor = os.open(stamp_path(ledger), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)

        with os.fdopen(descriptor, "w") as handle:
            json.dump(stamp, handle)
    except OSError:
        return


def clear_clean_check(ledger: Path) -> None:
    try:
        stamp_path(ledger).unlink(missing_ok=True)
    except OSError:
        return


def entry_field(entry: dict[object, object], name: str) -> object:
    data = entry.get("data")

    if isinstance(data, dict) and name in data:
        return data[name]

    return entry.get(name)


def comment_urls(value: object) -> frozenset[str]:
    values = value if isinstance(value, list) else [value]

    return frozenset(
        url.strip() for url in values if isinstance(url, str) and url.strip().startswith("https://")
    )


def entry_statuses(entry: dict[object, object]) -> frozenset[str]:
    return frozenset(
        value.strip().lower()
        for value in (entry_field(entry, "status"), entry_field(entry, "delivery"))
        if isinstance(value, str)
    )


def entry_record(entry: object, kind: str, fallback_id: str) -> BackupRecord | None:
    if not isinstance(entry, dict):
        return None

    entry_id = entry.get("id")
    recovery_comment = entry_field(entry, "recovery_comment")

    return BackupRecord(
        id=str(entry_id) if entry_id else fallback_id,
        kind=kind,
        statuses=entry_statuses(entry),
        has_commit=bool(entry_field(entry, "commits") or entry_field(entry, "commit")),
        urls=comment_urls(recovery_comment),
        awaits_pull_request=recovery_comment == AWAITING_PULL_REQUEST,
    )


def ledger_records(document: object) -> list[BackupRecord]:
    if not isinstance(document, dict) or not isinstance(document.get("session_ledger"), dict):
        raise LedgerFormatError("it has no session_ledger mapping")

    session_ledger = document["session_ledger"]

    if not isinstance(session_ledger.get("entries"), list):
        raise LedgerFormatError("session_ledger has no entries list")

    records: list[BackupRecord] = []

    for scope, container in (("session_ledger.", session_ledger), ("", document)):
        entries = container.get("entries")
        decisions = container.get("decisions")

        for index, entry in enumerate(entries if isinstance(entries, list) else []):
            kind = str(entry.get("kind")) if isinstance(entry, dict) else ""
            record = entry_record(entry, kind, f"{scope}entries[{index}]")

            if record is not None:
                records.append(record)

        for index, decision in enumerate(decisions if isinstance(decisions, list) else []):
            record = entry_record(decision, "decision", f"{scope}decisions[{index}]")

            if record is not None:
                records.append(record)

    return records


def missing_backup(record: BackupRecord, url_owners: dict[str, list[BackupRecord]]) -> str | None:
    if record["kind"] not in BACKUP_KINDS or record["statuses"] & SKIPPED_STATUSES:
        return None

    if record["kind"] == "question" and "answered" not in record["statuses"]:
        return None

    is_guidance = record["kind"] == GUIDANCE_CORRECTION

    if is_guidance and not record["has_commit"]:
        return None

    if not record["urls"]:
        if is_guidance:
            return "has a commit but no recovery_comment URL"

        if record["awaits_pull_request"]:
            return None

        return "no recovery_comment URL"

    if not is_guidance:
        return None

    sharers = sorted(
        {
            owner["id"]
            for url in record["urls"]
            for owner in url_owners[url]
            if owner["id"] != record["id"]
        }
    )

    if not sharers:
        return None

    return f"recovery_comment URL is shared with {', '.join(sharers)}"


def ledger_findings(records: list[BackupRecord]) -> list[str]:
    url_owners: dict[str, list[BackupRecord]] = defaultdict(list)

    for record in records:
        for url in record["urls"]:
            url_owners[url].append(record)

    findings: list[str] = []

    for record in records:
        problem = missing_backup(record, url_owners)

        if problem is not None:
            findings.append(f"- {record['id']} ({record['kind']}): {problem}")

    return findings


def check_ledger(ledger: Path) -> list[str]:
    if yaml is None:
        raise LedgerFormatError("PyYAML is not installed")

    loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)

    try:
        document: object = yaml.load(ledger.read_text(), Loader=loader)
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as error:
        raise LedgerFormatError(str(error)) from error

    return ledger_findings(ledger_records(document))


def main() -> int:
    hook_input = read_hook_input()

    if hook_input.get("stop_hook_active"):
        return 0

    directory = ledger_directory()
    ledgers = select_session_ledgers(discover_ledgers(directory), hook_input)

    if directory.is_dir():
        remove_orphaned_stamps(directory)

    reports: list[str] = []
    unchecked: list[str] = []

    for ledger in ledgers:
        try:
            stamp = current_stamp(ledger)
        except OSError:
            continue

        if is_unchanged_since_clean_check(ledger, stamp):
            continue

        try:
            findings = check_ledger(ledger)
        except LedgerFormatError as error:
            clear_clean_check(ledger)

            if yaml is None:
                unchecked.append(f"{ledger}: {error}")
            else:
                reports.append(f"{ledger} could not be read: {error}")

            continue

        if not findings:
            record_clean_check(ledger, stamp)

            continue

        clear_clean_check(ledger)
        reports.append(
            f"{ledger} has entries missing their backup comment:\n" + "\n".join(findings)
        )

    if reports:
        reports.append(
            "Post or edit each backup comment as session-ledger's Backup section says, record its URL "
            "in the entry, and then end the turn."
        )
        print("\n\n".join(reports), file=sys.stderr)

        return BLOCK_EXIT

    if unchecked:
        print("Ledger backups were not checked:\n" + "\n".join(unchecked), file=sys.stderr)

        return UNCHECKED_EXIT

    return 0


if __name__ == "__main__":
    sys.exit(main())
