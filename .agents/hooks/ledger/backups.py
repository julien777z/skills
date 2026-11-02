from collections import defaultdict
from typing import Final

from models import BackedUpKind, BackupRecord, EntryStatus, LedgerFormatError

AWAITING_PULL_REQUEST: Final[str] = "awaiting_pull_request"
COMMENT_URL_PREFIX: Final[str] = "https://"
SETTLED_STATUSES: Final[frozenset[EntryStatus]] = frozenset(
    {EntryStatus.COMPLETE, EntryStatus.WITHDRAWN}
)


def optional_string(data: dict[object, object], name: str, location: str) -> str | None:
    """Read a data field that is a string when present."""

    value = data.get(name)

    if value is not None and not isinstance(value, str):
        raise LedgerFormatError(f"{location} has a {name} that is not a string")

    return value


def comment_urls(value: object, location: str) -> tuple[str, ...]:
    """Read an entry's backup comment URLs from its recovery_comment field."""

    if value is None or value == AWAITING_PULL_REQUEST:
        return ()

    if not isinstance(value, list):
        raise LedgerFormatError(f"{location} has a recovery_comment that is not a list")

    urls = tuple(
        url for url in value if isinstance(url, str) and url.startswith(COMMENT_URL_PREFIX)
    )

    if len(urls) != len(value):
        raise LedgerFormatError(f"{location} has a recovery_comment entry that is not a URL")

    return urls


def entry_record(entry: object, location: str) -> BackupRecord | None:
    """Read the backup facts of one ledger entry, or None for a kind that is not backed up."""

    if not isinstance(entry, dict):
        raise LedgerFormatError(f"{location} is not a mapping")

    entry_id = entry.get("id")
    kind = entry.get("kind")
    data = entry.get("data")

    if not isinstance(entry_id, str) or not entry_id:
        raise LedgerFormatError(f"{location} has no id")

    if not isinstance(kind, str):
        raise LedgerFormatError(f"{location} has no kind")

    if not isinstance(data, dict):
        raise LedgerFormatError(f"{location} has no data mapping")

    if kind not in BackedUpKind:
        return None

    commits = data.get("commits")

    if commits is not None and not isinstance(commits, list):
        raise LedgerFormatError(f"{location} has commits that are not a list")

    return BackupRecord(
        id=entry_id,
        kind=BackedUpKind(kind),
        status=optional_string(data, "status", location),
        has_commit=bool(commits),
        comment_urls=comment_urls(data.get("recovery_comment"), location),
        awaits_pull_request=data.get("recovery_comment") == AWAITING_PULL_REQUEST,
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

    is_guidance = record["kind"] is BackedUpKind.GUIDANCE_CORRECTION

    if is_guidance and not record["has_commit"]:
        return None

    urls = record["comment_urls"]

    if not urls:
        if is_guidance:
            return "has a commit but no recovery_comment URL"

        if record["awaits_pull_request"]:
            return None

        return "no recovery_comment URL"

    if not is_guidance:
        return None

    sharers = sorted({owner for url in urls for owner in url_owners[url] if owner != record["id"]})

    if not sharers:
        return None

    return f"recovery_comment URL is shared with {', '.join(sharers)}"


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
