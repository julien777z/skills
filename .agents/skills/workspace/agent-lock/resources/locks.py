from datetime import UTC, datetime, timedelta
from hashlib import sha256
from json import dumps
from os import getpid
from pathlib import Path
from time import monotonic, sleep
from typing import Final
from uuid import uuid4

from models.ownership import (
    Acquisition,
    LockResult,
    Outcome,
    Ownership,
    QueueRecord,
    Receipt,
    Ticket,
    Waiter,
)
from utils import (
    JsonValue,
    assert_supported_version,
    atomic_write,
    exclusive_file,
    process_alive,
    read_json_record,
    read_text_field,
)

# A holder renews about every minute; a lock left unrenewed for five minutes has a holder that is gone.
RENEWAL_INTERVAL: Final = timedelta(minutes=1)
LEASE: Final = timedelta(minutes=5)
POLL_SECONDS: Final = 0.25
TICKET_RENEWAL: Final = timedelta(seconds=5)
TICKET_GRACE: Final = timedelta(seconds=30)


def resource_path(directory: Path, key: str) -> Path:
    """Locate one exact resource key within the shared coordinator directory."""

    if not key.strip():
        raise ValueError("The resource key must not be empty")

    return directory.expanduser().resolve() / (sha256(key.encode("utf-8")).hexdigest() + ".lock")


def state_path(path: Path) -> Path:
    """Locate ownership data beside its persistent mutex."""

    return path.with_name(path.name + ".json")


def queue_path(path: Path) -> Path:
    """Locate the arrival-order queue beside its persistent mutex."""

    return path.with_name(path.name + ".queue.json")


def read_timestamp(record: dict[str, JsonValue], key: str) -> datetime:
    """Read a timezone-aware ISO-8601 timestamp from a decoded JSON record."""

    value = datetime.fromisoformat(read_text_field(record, key))

    if value.tzinfo is None:
        raise ValueError(f"{key} must include a timezone")

    return value


def read_queue(path: Path) -> list[Ticket]:
    """Validate the persisted queue of waiters, oldest first."""

    try:
        record = read_json_record(queue_path(path))
    except FileNotFoundError:
        return []

    if record is None:
        return []

    assert_supported_version(record, "queue")

    entries = record.get("tickets")

    if not isinstance(entries, list):
        raise ValueError("Unsupported queue record")

    tickets: list[Ticket] = []

    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Queue tickets must be JSON objects")

        pid = entry.get("pid")

        if pid is not None and (not isinstance(pid, int) or isinstance(pid, bool) or pid <= 0):
            raise ValueError("A queue ticket's pid must be a positive integer or null")

        priority = entry.get("priority")

        if not isinstance(priority, bool):
            raise ValueError("A queue ticket's priority field must be present and a boolean")

        tickets.append(
            Ticket(
                receipt=read_text_field(entry, "receipt"),
                owner=read_text_field(entry, "owner"),
                activity=read_text_field(entry, "activity"),
                pid=pid,
                priority=priority,
                enqueued_at=read_timestamp(entry, "enqueued_at"),
                renewed_at=read_timestamp(entry, "renewed_at"),
            )
        )

    return tickets


def write_queue(path: Path, tickets: list[Ticket]) -> None:
    """Persist the queue of waiters, oldest first."""

    atomic_write(queue_path(path), dumps(QueueRecord(version=1, tickets=tickets), default=datetime.isoformat))


def is_live(ticket: Ticket, now: datetime) -> bool:
    """Keep a ticket while its waiter is polling or recently returned between bounded calls."""

    if now - ticket["renewed_at"] > TICKET_GRACE:
        return False

    return ticket["pid"] is None or process_alive(ticket["pid"])


def queued_waiters(tickets: list[Ticket], now: datetime) -> list[Waiter]:
    """Report live waiters with their one-based queue positions."""

    live = [ticket for ticket in tickets if is_live(ticket, now)]

    return [
        Waiter(
            position=position,
            owner=ticket["owner"],
            activity=ticket["activity"],
            enqueued_at=ticket["enqueued_at"],
        )
        for position, ticket in enumerate(live, start=1)
    ]


def take_ticket(tickets: list[Ticket], request: Acquisition, now: datetime) -> Ticket:
    """Return this receipt's place in the queue, joining behind the tickets of its own priority when it has none."""

    receipt = str(request["receipt_path"])
    ticket = next((ticket for ticket in tickets if ticket["receipt"] == receipt), None)

    if ticket is None:
        ticket = Ticket(
            receipt=receipt,
            owner=request["owner"],
            activity=request["activity"],
            pid=getpid(),
            priority=request["priority"],
            enqueued_at=now,
            renewed_at=now,
        )

        if ticket["priority"]:
            tickets.insert(sum(1 for queued in tickets if queued["priority"]), ticket)
        else:
            tickets.append(ticket)
    elif ticket["pid"] != getpid() or now - ticket["renewed_at"] >= TICKET_RENEWAL:
        ticket["pid"] = getpid()
        ticket["renewed_at"] = now

    return ticket


def read_ownership(path: Path) -> Ownership | None:
    """Validate persisted ownership before making an access decision."""

    try:
        record = read_json_record(state_path(path))
    except FileNotFoundError:
        return None

    if record is None:
        return None

    assert_supported_version(record, "ownership")

    acquired_at = read_timestamp(record, "acquired_at")
    expires_at = read_timestamp(record, "expires_at")

    if expires_at <= acquired_at:
        raise ValueError("Ownership must expire after it was acquired")

    return Ownership(
        version=1,
        key=read_text_field(record, "key"),
        token=read_text_field(record, "token"),
        owner=read_text_field(record, "owner"),
        activity=read_text_field(record, "activity"),
        acquired_at=acquired_at,
        expires_at=expires_at,
    )


def read_receipt(path: Path) -> Receipt:
    """Validate an acquisition capability at the file boundary."""

    record = read_json_record(path)

    if record is None:
        raise ValueError("Receipt must contain an ownership capability")

    return Receipt(
        lock_file=read_text_field(record, "lock_file"),
        key=read_text_field(record, "key"),
        token=read_text_field(record, "token"),
    )


def last_activity(path: Path) -> datetime | None:
    """Return when the key's lock was last acquired, renewed or released, each of which rewrites its ownership file."""

    try:
        modified = state_path(path).stat().st_mtime
    except FileNotFoundError:
        return None

    return datetime.fromtimestamp(modified, UTC)


def ownership_status(ownership: Ownership | None) -> LockResult:
    """Describe current ownership without renewing it."""

    if ownership is None:
        return LockResult(status=Outcome.AVAILABLE, ownership=None)

    remaining = (ownership["expires_at"] - datetime.now(UTC)).total_seconds()

    return LockResult(
        status=Outcome.HELD if remaining > 0 else Outcome.EXPIRED,
        ownership=ownership,
        remaining_seconds=max(0, remaining),
    )


def leave_queue(path: Path, receipt: str) -> None:
    """Remove a receipt's ticket from one key's queue."""

    with exclusive_file(path):
        stored = read_queue(path)
        tickets = [ticket for ticket in stored if ticket["receipt"] != receipt]

        if tickets != stored:
            write_queue(path, tickets)


def claim_or_queue(
    key: str, path: Path, request: Acquisition, expired: bool
) -> LockResult | tuple[int, LockResult] | None:
    """Claim one key for the request when its ticket leads a free lock; otherwise keep its place in the queue.

    Returns the acquisition, the queue position with its contention evidence once the wait has expired, or `None`
    while waiting goes on.
    """

    with exclusive_file(path):
        current = read_ownership(path)
        now = datetime.now(UTC)
        stored = read_queue(path)
        tickets = [ticket.copy() for ticket in stored if is_live(ticket, now)]

        ticket = take_ticket(tickets, request, now)

        if tickets[0] is ticket and (current is None or now >= current["expires_at"]):
            ownership = Ownership(
                version=1,
                key=key,
                token=str(uuid4()),
                owner=request["owner"],
                activity=request["activity"],
                acquired_at=now,
                expires_at=now + LEASE,
            )
            receipt = Receipt(lock_file=str(path), key=key, token=ownership["token"])

            write_queue(path, tickets[1:])
            atomic_write(state_path(path), dumps(ownership, default=datetime.isoformat))
            atomic_write(request["receipt_path"], dumps(receipt))

            return LockResult(
                status=Outcome.ACQUIRED,
                ownership=ownership,
                receipt=str(request["receipt_path"]),
                expired_owner=current["owner"] if current else None,
            )

        if not expired:
            if tickets != stored:
                write_queue(path, tickets)

            return None

        ticket["pid"] = None
        ticket["renewed_at"] = now

        write_queue(path, tickets)

        position = next(position for position, queued in enumerate(tickets, start=1) if queued is ticket)
        result = ownership_status(current)
        result["status"] = Outcome.BUSY
        result["queue_position"] = position

        return position, result


def acquire_resource(request: Acquisition) -> LockResult:
    """Acquire the first of the request's keys to come free, or return contention evidence."""

    paths = [(key, resource_path(request["state_directory"], key)) for key in request["keys"]]
    receipt_path = request["receipt_path"]

    if any(receipt_path in (path, state_path(path), queue_path(path)) for _, path in paths):
        raise ValueError("Receipt must be separate from lock state")

    if not request["owner"].strip() or not request["activity"].strip():
        raise ValueError("Owner and activity must identify this assignment")

    deadline = monotonic() + request["wait"].total_seconds()

    while True:
        expired = monotonic() >= deadline
        contention: list[tuple[int, LockResult]] = []

        for key, path in paths:
            claim = claim_or_queue(key, path, request, expired)

            if isinstance(claim, tuple):
                contention.append(claim)
            elif claim is not None:
                for other_key, other_path in paths:
                    if other_key != key:
                        leave_queue(other_path, str(receipt_path))

                return claim

        if expired:
            _, busy = min(contention, key=lambda queued: queued[0])

            return busy

        sleep(min(POLL_SECONDS, max(0, deadline - monotonic())))


def renew_ownership(receipt: Receipt) -> LockResult:
    """Assert that a receipt still owns an unexpired lock, and renew it for another lease."""

    path = Path(receipt["lock_file"])

    with exclusive_file(path):
        current = read_ownership(path)
        now = datetime.now(UTC)

        if (
            current is None
            or current["token"] != receipt["token"]
            or current["key"] != receipt["key"]
            or now >= current["expires_at"]
        ):
            raise ValueError("This receipt no longer owns the resource. Stop acting on it.")

        current["expires_at"] = now + LEASE

        atomic_write(state_path(path), dumps(current, default=datetime.isoformat))

        result = ownership_status(current)
        result["status"] = Outcome.OWNED

        return result


def release_ownership(receipt: Receipt) -> bool:
    """Release only the ownership identified by this receipt."""

    path = Path(receipt["lock_file"])

    with exclusive_file(path):
        current = read_ownership(path)

        if current is None or current["token"] != receipt["token"] or current["key"] != receipt["key"]:
            return False

        atomic_write(state_path(path), "null")

        return True
