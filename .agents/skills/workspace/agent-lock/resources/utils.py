from collections.abc import Generator, Mapping, Sequence
from contextlib import contextmanager
from datetime import UTC, datetime
from fcntl import LOCK_EX, LOCK_UN, flock
from json import loads
from math import isfinite
from os import fdopen, fsync, killpg, replace
from pathlib import Path
from signal import SIGINT, SIGKILL, SIGTERM, signal
from subprocess import Popen, TimeoutExpired
from sys import stderr
from tempfile import mkstemp
from types import FrameType
from typing import cast

from models.ownership import CommandResult, Outcome

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


def positive_seconds(value: str) -> float:
    """Parse a positive finite duration supplied by a CLI."""

    seconds = float(value)

    if not isfinite(seconds) or seconds <= 0:
        raise ValueError("Duration must be positive and finite")

    return seconds


def run_command(
    command: Sequence[str], environment: Mapping[str, str], expires_at: datetime
) -> CommandResult:
    """Run a foreground process group until completion or the deadline."""

    def _interrupt(signum: int, _frame: FrameType | None) -> None:
        """Interrupt the supervisor's blocking wait."""

        raise InterruptedError(signum)

    previous_handlers = {signum: signal(signum, _interrupt) for signum in (SIGINT, SIGTERM)}
    try:
        remaining = (expires_at - datetime.now(UTC)).total_seconds()
        if remaining <= 0:
            return CommandResult(status=Outcome.EXPIRED, command_exit_code=124, interrupted_by=None)

        outcome = Outcome.COMPLETED
        interrupted_by: int | None = None
        with Popen(command, env=environment, stdout=stderr, start_new_session=True) as child:
            try:
                child.wait(timeout=max(0, (expires_at - datetime.now(UTC)).total_seconds()))
            except TimeoutExpired:
                outcome = Outcome.EXPIRED
            except InterruptedError as error:
                outcome = Outcome.INTERRUPTED
                interrupted_by = int(error.args[0])
            finally:
                try:
                    killpg(child.pid, SIGKILL)
                except ProcessLookupError:
                    pass
                child.wait()
            return CommandResult(
                status=outcome,
                command_exit_code=child.returncode,
                interrupted_by=interrupted_by,
            )
    finally:
        for signum, handler in previous_handlers.items():
            signal(signum, handler)
