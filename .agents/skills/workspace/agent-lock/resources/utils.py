from collections.abc import Generator, Mapping
from contextlib import contextmanager
from fcntl import LOCK_EX, LOCK_UN, flock
from json import loads
from math import isfinite
from os import fdopen, fsync, kill, replace
from pathlib import Path
from tempfile import mkstemp
from typing import cast

type JsonValue = str | int | float | bool | None | list[JsonValue] | dict[str, JsonValue]


@contextmanager
def exclusive_file(path: Path) -> Generator[None]:
    """Serialize local processes using a persistent mutex file."""

    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)

    with path.open("a+b") as handle:
        flock(handle.fileno(), LOCK_EX)

        try:
            yield
        finally:
            flock(handle.fileno(), LOCK_UN)


def atomic_write(path: Path, content: str) -> None:
    """Replace a file without exposing a partial write."""

    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    descriptor, temporary = mkstemp(prefix=".agent-lock-", dir=path.parent)

    try:
        with fdopen(descriptor, "w") as handle:
            handle.write(content + "\n")
            handle.flush()
            fsync(handle.fileno())

        replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def read_json_record(path: Path) -> dict[str, JsonValue] | None:
    """Decode a JSON object or null at the file boundary."""

    value = cast(JsonValue, loads(path.read_text()))

    if value is not None and not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object or null: {path}")

    return value


def read_text_field(record: Mapping[str, JsonValue], key: str) -> str:
    """Read a nonempty string from a decoded JSON record."""

    value = record.get(key)

    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Expected a nonempty string for {key}")

    return value


def assert_supported_version(record: Mapping[str, JsonValue], record_kind: str) -> None:
    """Assert that a decoded record carries the one supported format version."""

    version = record.get("version")

    if not isinstance(version, int) or isinstance(version, bool) or version != 1:
        raise ValueError(f"Unsupported {record_kind} record")


def process_alive(pid: int) -> bool:
    """Report whether a local process still exists."""

    try:
        kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        pass

    return True


def positive_seconds(value: str) -> float:
    """Parse a positive finite duration supplied by a CLI."""

    seconds = float(value)

    if not isfinite(seconds) or seconds <= 0:
        raise ValueError("Duration must be positive and finite")

    return seconds

