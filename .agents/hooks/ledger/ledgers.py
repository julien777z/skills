import mmap
import os
import re
import stat
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Final

from models import HookInput

LEDGER_DIRECTORY_NAME: Final[str] = "agent-ledgers"
LEDGER_SUFFIXES: Final[frozenset[str]] = frozenset({".yaml", ".yml"})
LEDGER_NAME_PATTERN: Final[re.Pattern[bytes]] = re.compile(rb"agent-ledgers/([^\s\"'\\/]+\.ya?ml)")
TIMESTAMP_PATTERN: Final[re.Pattern[bytes]] = re.compile(rb'"timestamp"\s*:\s*"([^"]+)"')
SESSION_LEDGER_TEMPLATE: Final[str] = (
    'session_ledger:\n  sessions:\n    - "{session_id}"\n  entries: []\n'
)


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


def transcript_ledgers(transcript_path: str | None) -> tuple[set[bytes], datetime | None]:
    """Read the ledger names a transcript mentions and the session start it records."""

    if transcript_path is None:
        return set(), None

    try:
        with (
            open(transcript_path, "rb") as handle,
            mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ) as transcript,
        ):
            names = {match.group(1) for match in LEDGER_NAME_PATTERN.finditer(transcript)}
            started = session_start(transcript)
    except (OSError, ValueError):
        return set(), None

    return names, started


def is_written_since(path: Path, started: datetime | None) -> bool:
    """Tell whether a ledger file exists and was modified at or after the session's start."""

    try:
        status = path.stat()
    except OSError:
        return False

    is_recent = started is None or datetime.fromtimestamp(status.st_mtime, UTC) >= started

    return stat.S_ISREG(status.st_mode) and is_recent


def names_session(path: Path, session_id: str) -> bool:
    """Tell whether a ledger file's text holds the session's ID."""

    try:
        return session_id.encode() in path.read_bytes()
    except OSError:
        return False


def session_ledgers(hook_input: HookInput) -> tuple[set[Path], set[Path]]:
    """Return the ledgers changed since the session began: named by its transcript, then by ID."""

    directory = ledger_directory()

    if not directory.is_dir():
        return set(), set()

    names, started = transcript_ledgers(hook_input["transcript_path"])
    session_id = hook_input["session_id"]
    candidates = (directory / os.fsdecode(name) for name in names)
    named = {path for path in candidates if is_written_since(path, started)}

    if session_id is None:
        return named, set()

    mentioning = {
        path
        for path in directory.iterdir()
        if path.suffix in LEDGER_SUFFIXES
        and path not in named
        and is_written_since(path, started)
        and names_session(path, session_id)
    }

    return named, mentioning


def session_ledger_path(session_id: str) -> Path:
    """Return where the hook keeps the ledger it creates for a session."""

    return ledger_directory() / f"session-{session_id}.yaml"


def create_session_ledger(session_id: str) -> Path | None:
    """Create the session's empty ledger file unless it exists."""

    path = session_ledger_path(session_id)
    directory = path.parent

    directory.mkdir(mode=0o700, parents=True, exist_ok=True)

    descriptor, temporary = tempfile.mkstemp(dir=directory, prefix=".session-", suffix=".tmp")

    try:
        with os.fdopen(descriptor, "w") as handle:
            handle.write(SESSION_LEDGER_TEMPLATE.format(session_id=session_id))
            handle.flush()
            os.fsync(handle.fileno())

        os.link(temporary, path)
    except FileExistsError:
        return None
    finally:
        os.unlink(temporary)

    return path


def remove_untouched_session_ledger(session_id: str) -> None:
    """Delete the ledger the hook created for a session while it still holds only the session."""

    path = session_ledger_path(session_id)

    try:
        if path.read_text() == SESSION_LEDGER_TEMPLATE.format(session_id=session_id):
            path.unlink()
    except FileNotFoundError:
        return
