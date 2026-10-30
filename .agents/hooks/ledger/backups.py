from collections import defaultdict
from pathlib import Path
from typing import Final

from models import BackupRecord, LedgerFormatError

try:
    import yaml
except ImportError:
    yaml = None

GUIDANCE_CORRECTION: Final = "guidance_correction"
BACKUP_KINDS: Final = frozenset({GUIDANCE_CORRECTION, "plan", "decision", "question"})
SKIPPED_STATUSES: Final = frozenset(
    {"awaiting_action_verification", "withdrawn", "complete", "delivered", "merged"}
)
AWAITING_PULL_REQUEST: Final = "awaiting_pull_request"
YAML_AVAILABLE: Final = yaml is not None


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
