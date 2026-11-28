from enum import Enum, StrEnum
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


class HookOutcome(Enum):
    """How the hook leaves the turn, valued as its process exit code."""

    END_TURN = 0
    UNCHECKED = 1
    HOLD_TURN = 2


class HookInput(TypedDict):
    """The turn-end payload fields the hook reads."""

    is_continuation: bool
    expects_followup_message: bool
    transcript_path: str | None
    session_id: str | None


class BackupRecord(TypedDict):
    """The backup facts of one backed-up ledger entry."""

    id: str
    kind: BackedUpKind
    status: str | None
    has_commit: bool
    comment_urls: tuple[str, ...]
    has_recovery_comment: bool


class LedgerFormatError(Exception):
    """A ledger that does not follow the session-ledger schema."""
