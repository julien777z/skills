import mmap
import os
import re
import stat
from datetime import UTC, datetime
from pathlib import Path
from typing import Final

from models import HookInput

LEDGER_DIRECTORY_NAME: Final[str] = "agent-ledgers"
LEDGER_NAME_PATTERN: Final[re.Pattern[bytes]] = re.compile(rb"agent-ledgers/([^\s\"'\\/]+\.ya?ml)")
TIMESTAMP_PATTERN: Final[re.Pattern[bytes]] = re.compile(rb'"timestamp"\s*:\s*"([^"]+)"')


def ledger_directory() -> Path:
    """Return the private directory that holds task ledgers."""

    state_home = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")

    return Path(state_home) / LEDGER_DIRECTORY_NAME


def session_start(transcript: mmap.mmap) -> datetime | None:
    """Read the session's start from the first timestamp its transcript records."""

    match = TIMESTAMP_PATTERN.search(transcript)

    if match is None:
        return None

    try:
        started = datetime.fromisoformat(match.group(1).decode())
    except (UnicodeDecodeError, ValueError):
        return None

    return started if started.tzinfo is not None else started.replace(tzinfo=UTC)


def is_written_since(path: Path, started: datetime | None) -> bool:
    """Tell whether a ledger file exists and was modified at or after the session's start."""

    try:
        status = path.stat()
    except OSError:
        return False

    is_recent = started is None or datetime.fromtimestamp(status.st_mtime, UTC) >= started

    return stat.S_ISREG(status.st_mode) and is_recent


def session_ledgers(hook_input: HookInput) -> list[Path]:
    """Return the ledgers the session writes: named in its transcript and modified since it began."""

    transcript_path = hook_input["transcript_path"]
    directory = ledger_directory()

    if transcript_path is None or not directory.is_dir():
        return []

    try:
        with (
            open(transcript_path, "rb") as handle,
            mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ) as transcript,
        ):
            names = {match.group(1) for match in LEDGER_NAME_PATTERN.finditer(transcript)}
            started = session_start(transcript)
    except (OSError, ValueError):
        return []

    candidates = (directory / os.fsdecode(name) for name in names)

    return sorted(path for path in candidates if is_written_since(path, started))
