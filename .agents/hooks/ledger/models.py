from typing import TypedDict


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
