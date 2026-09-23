from datetime import UTC, datetime, timedelta
from hashlib import sha256
from json import dumps
from pathlib import Path
from time import monotonic, sleep
from typing import Final
from uuid import uuid4

from models.ownership import (
    Acquisition,
    LockResult,
    Outcome,
    Ownership,
    Receipt,
)
from utils import (
    atomic_write,
    exclusive_file,
    read_json_record,
    read_text_field,
)

DEFAULT_TTL: Final = timedelta(minutes=10)
MAX_TTL: Final = timedelta(minutes=30)


def resource_path(directory: Path, key: str) -> Path:
    """Locate one exact resource key within the shared coordinator directory."""

    if not key.strip():
        raise ValueError("The resource key must not be empty")

    return directory.expanduser().resolve() / (sha256(key.encode("utf-8")).hexdigest() + ".lock")


def state_path(path: Path) -> Path:
    """Locate ownership data beside its persistent mutex."""

    return path.with_name(path.name + ".json")


def read_ownership(path: Path) -> Ownership | None:
    """Validate persisted ownership before making an access decision."""

    try:
        record = read_json_record(state_path(path))
    except FileNotFoundError:
        return None

    if record is None:
        return None

    version = record.get("version")
    if not isinstance(version, int) or isinstance(version, bool) or version != 1:
        raise ValueError("Unsupported ownership record")

    acquired_at = datetime.fromisoformat(read_text_field(record, "acquired_at"))
    expires_at = datetime.fromisoformat(read_text_field(record, "expires_at"))

    if acquired_at.tzinfo is None or expires_at.tzinfo is None:
        raise ValueError("Ownership timestamps must include a timezone")

    if not timedelta() < expires_at - acquired_at <= MAX_TTL:
        raise ValueError("Ownership duration must be positive and at most thirty minutes")

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


def ownership_status(ownership: Ownership | None) -> LockResult:
    """Describe current ownership without extending its deadline."""

    if ownership is None:
        return LockResult(status=Outcome.AVAILABLE, ownership=None)

    remaining = (ownership["expires_at"] - datetime.now(UTC)).total_seconds()

    return LockResult(
        status=Outcome.HELD if remaining > 0 else Outcome.EXPIRED,
        ownership=ownership,
        remaining_seconds=max(0, remaining),
    )


def acquire_resource(request: Acquisition) -> LockResult:
    """Acquire one bounded ownership claim or return contention evidence."""

    path = resource_path(request["state_directory"], request["key"])
    receipt_path = request["receipt_path"]

    if receipt_path in (path, state_path(path)):
        raise ValueError("Receipt must be separate from lock state")

    if not request["owner"].strip() or not request["activity"].strip():
        raise ValueError("Owner and activity must identify this assignment")

    if not timedelta() < request["ttl"] <= MAX_TTL:
        raise ValueError("Lock duration must be positive and at most thirty minutes")

    deadline = monotonic() + request["wait"].total_seconds()

    while True:
        with exclusive_file(path):
            current = read_ownership(path)
            now = datetime.now(UTC)

            if current is None or now >= current["expires_at"]:
                ownership = Ownership(
                    version=1,
                    key=request["key"],
                    token=str(uuid4()),
                    owner=request["owner"],
                    activity=request["activity"],
                    acquired_at=now,
                    expires_at=now + request["ttl"],
                )
                receipt = Receipt(lock_file=str(path), key=request["key"], token=ownership["token"])

                atomic_write(state_path(path), dumps(ownership, default=datetime.isoformat))
                atomic_write(receipt_path, dumps(receipt))

                return LockResult(
                    status=Outcome.ACQUIRED,
                    ownership=ownership,
                    receipt=str(receipt_path),
                    expired_owner=current["owner"] if current else None,
                )

        remaining = deadline - monotonic()

        if remaining <= 0:
            result = ownership_status(current)
            result["status"] = Outcome.BUSY

            return result

        sleep(min(0.25, remaining))


def check_ownership(receipt: Receipt) -> LockResult:
    """Assert that a receipt still owns an unexpired lock."""

    with exclusive_file(Path(receipt["lock_file"])):
        current = read_ownership(Path(receipt["lock_file"]))

        if (
            current is None
            or current["token"] != receipt["token"]
            or current["key"] != receipt["key"]
            or datetime.now(UTC) >= current["expires_at"]
        ):
            raise ValueError("This receipt no longer owns the resource. Stop acting on it.")

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
