from enum import StrEnum
from typing import TypedDict


class BackedUpKind(StrEnum):
    """A ledger entry kind backed up in a pull-request comment."""

    GUIDANCE_CORRECTION = "guidance_correction"
    PLAN = "plan"
    DECISION = "decision"
    QUESTION = "question"


class EntryStatus(StrEnum):
    """A ledger entry status the backup check acts on."""

    ANSWERED = "answered"
    COMPLETE = "complete"
    WITHDRAWN = "withdrawn"


class HookInput(TypedDict):
    """The turn-end payload fields the backup check reads."""

    stop_hook_active: bool
    transcript_path: str | None


class BackupRecord(TypedDict):
    """The backup facts of one backed-up ledger entry."""

    id: str
    kind: BackedUpKind
    status: str | None
    has_commit: bool
    comment_urls: tuple[str, ...]
    awaits_pull_request: bool


class LedgerFormatError(Exception):
    """A ledger that does not follow the session-ledger schema."""
