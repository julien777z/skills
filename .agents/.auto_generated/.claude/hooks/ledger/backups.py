from collections import defaultdict
from typing import Final

from models import BackedUpKind, BackupRecord, EntryStatus, LedgerFormatError

AWAITING_PULL_REQUEST: Final[str] = "awaiting_pull_request"
COMMENT_URL_PREFIX: Final[str] = "https://"
BACKED_UP_KINDS: Final[frozenset[str]] = frozenset(BackedUpKind)
SETTLED_STATUSES: Final[frozenset[EntryStatus]] = frozenset(
    {EntryStatus.COMPLETE, EntryStatus.WITHDRAWN}
)


def optional_string(data: dict[object, object], name: str, location: str) -> str | None:
    """Read a data field that is a string when present."""

    value = data.get(name)

    if value is not None and not isinstance(value, str):
        raise LedgerFormatError(f"{location} has a {name} that is not a string")

    return value


def recovery_comment_items(value: object, location: str) -> list[str]:
    """Read an entry's recovery_comment list of backup comment URLs and awaiting markers."""

    if value is None:
        return []

    if not isinstance(value, list):
        raise LedgerFormatError(f"{location} has a data.recovery_comment that is not a list")

    items = [
        item
        for item in value
        if isinstance(item, str)
        and (item.startswith(COMMENT_URL_PREFIX) or item == AWAITING_PULL_REQUEST)
    ]

    if len(items) != len(value):
        raise LedgerFormatError(
            f"{location} has a data.recovery_comment item that is neither a URL "
            f"nor {AWAITING_PULL_REQUEST}"
        )

    return items


def entry_record(entry: object, location: str) -> BackupRecord | None:
    """Read the backup facts of one ledger entry, or None for a kind that is not backed up."""

    if not isinstance(entry, dict):
        raise LedgerFormatError(f"{location} is not a mapping")

    kind = entry.get("kind")

    if not isinstance(kind, str):
        raise LedgerFormatError(f"{location} has no kind")

    if kind not in BACKED_UP_KINDS:
        return None

    entry_id = entry.get("id")
    data = entry.get("data")

    if not isinstance(entry_id, str) or not entry_id:
        raise LedgerFormatError(f"{location} has no id")

    if not isinstance(data, dict):
        raise LedgerFormatError(f"{location} has no data mapping")

    commits = data.get("commits")

    if commits is not None and not isinstance(commits, list):
        raise LedgerFormatError(f"{location} has commits that are not a list")

    items = recovery_comment_items(data.get("recovery_comment"), location)

    return BackupRecord(
        id=entry_id,
        kind=BackedUpKind(kind),
        status=optional_string(data, "status", location),
        has_commit=bool(commits),
        comment_urls=tuple(item for item in items if item != AWAITING_PULL_REQUEST),
        has_recovery_comment=bool(items),
    )


def ledger_records(document: object) -> list[BackupRecord]:
    """Read the backup facts of every backed-up entry in a ledger document."""

    if not isinstance(document, dict) or not isinstance(document.get("session_ledger"), dict):
        raise LedgerFormatError("it has no session_ledger mapping")

    entries = document["session_ledger"].get("entries")

    if not isinstance(entries, list):
        raise LedgerFormatError("session_ledger has no entries list")

    records = (
        entry_record(entry, f"session_ledger.entries[{index}]")
        for index, entry in enumerate(entries)
    )

    return [record for record in records if record is not None]


def missing_backup(record: BackupRecord, url_owners: dict[str, list[str]]) -> str | None:
    """Describe what an entry's backup lacks, or None when it owes nothing."""

    if record["status"] in SETTLED_STATUSES:
        return None

    if record["kind"] is BackedUpKind.QUESTION and record["status"] != EntryStatus.ANSWERED:
        return None

    if record["kind"] is not BackedUpKind.GUIDANCE_CORRECTION:
        return None if record["has_recovery_comment"] else "data.recovery_comment is empty"

    if not record["has_commit"]:
        return None

    urls = record["comment_urls"]

    if not urls:
        return "has a commit but no comment URL in data.recovery_comment"

    sharers = sorted({owner for url in urls for owner in url_owners[url] if owner != record["id"]})

    if not sharers:
        return None

    return f"data.recovery_comment URL is shared with {', '.join(sharers)}"


def ledger_findings(document: object) -> list[str]:
    """List every entry in a ledger document that owes a backup comment."""

    records = ledger_records(document)
    url_owners: dict[str, list[str]] = defaultdict(list)

    for record in records:
        for url in record["comment_urls"]:
            url_owners[url].append(record["id"])

    findings: list[str] = []

    for record in records:
        problem = missing_backup(record, url_owners)

        if problem is not None:
            findings.append(f"- {record['id']} ({record['kind']}): {problem}")

    return findings
