from datetime import datetime, timedelta
from enum import StrEnum
from pathlib import Path
from typing import Literal, NotRequired, TypedDict


class Outcome(StrEnum):
    """Result of a resource ownership operation."""

    AVAILABLE = "available"
    HELD = "held"
    EXPIRED = "expired"
    ACQUIRED = "acquired"
    BUSY = "busy"
    OWNED = "owned"
    RELEASED = "released"
    COMPLETED = "completed"
    INTERRUPTED = "interrupted"
    ERROR = "error"


class Ownership(TypedDict):
    """One exclusive claim with a fixed expiration time."""

    version: Literal[1]
    key: str
    token: str
    owner: str
    activity: str
    acquired_at: datetime
    expires_at: datetime


class Receipt(TypedDict):
    """Capability identifying one acquisition of a resource."""

    lock_file: str
    key: str
    token: str


class Acquisition(TypedDict):
    """Validated settings for waiting on and acquiring a resource."""

    key: str
    state_directory: Path
    owner: str
    activity: str
    receipt_path: Path
    wait: timedelta
    ttl: timedelta


class LockResult(TypedDict):
    """CLI ownership result and its supporting evidence."""

    status: Outcome
    ownership: NotRequired[Ownership | None]
    remaining_seconds: NotRequired[float]
    receipt: NotRequired[str]
    expired_owner: NotRequired[str | None]
    message: NotRequired[str]


class CommandResult(TypedDict):
    """A foreground command's completion or cancellation result."""

    status: Outcome
    command_exit_code: int
    interrupted_by: int | None
