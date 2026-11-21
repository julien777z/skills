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
    """One exclusive claim, which expires once its holder stops renewing it."""

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


class Ticket(TypedDict):
    """One waiter's place in a resource's queue.

    `pid` names the process polling for the waiter, or is `None` while the waiter is between
    bounded calls. A `priority` ticket waits ahead of every ordinary one.
    """

    receipt: str
    owner: str
    activity: str
    pid: int | None
    priority: bool
    enqueued_at: datetime
    renewed_at: datetime


class QueueRecord(TypedDict):
    """A resource's persisted queue of waiters, oldest first."""

    version: Literal[1]
    tickets: list[Ticket]


class Waiter(TypedDict):
    """A queued waiter as `status` reports it."""

    position: int
    owner: str
    activity: str
    enqueued_at: datetime


class Acquisition(TypedDict):
    """Validated settings for waiting on and acquiring one of a set of resources."""

    keys: list[str]
    state_directory: Path
    owner: str
    activity: str
    receipt_path: Path
    wait: timedelta
    priority: bool


class LockResult(TypedDict):
    """CLI ownership result and its supporting evidence."""

    status: Outcome
    ownership: NotRequired[Ownership | None]
    remaining_seconds: NotRequired[float]
    receipt: NotRequired[str]
    expired_owner: NotRequired[str | None]
    queue_position: NotRequired[int]
    waiters: NotRequired[list[Waiter]]
    last_activity_at: NotRequired[datetime | None]
    message: NotRequired[str]


class CommandResult(TypedDict):
    """A foreground command's completion or cancellation result."""

    status: Outcome
    command_exit_code: int
    interrupted_by: int | None
