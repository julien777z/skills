import mmap
import os
import re
import stat
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from typing import Final

from models import HookInput

try:
    import yaml
except ImportError:
    yaml: ModuleType | None = None

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


def lists_session(path: Path, session_id: str) -> bool:
    """Tell whether a ledger's sessions list holds the session's ID."""

    try:
        text = path.read_bytes()
    except OSError:
        return False

    if session_id.encode() not in text:
        return False

    # A ledger naming the session that cannot be parsed is its own, reported rather than replaced.
    if yaml is None:
        return True

    try:
        document = yaml.safe_load(text)
    except yaml.YAMLError:
        return True

    ledger = document.get("session_ledger") if isinstance(document, dict) else None
    sessions = ledger.get("sessions") if isinstance(ledger, dict) else None

    return isinstance(sessions, list) and session_id in sessions


def session_ledgers(hook_input: HookInput) -> list[Path]:
    """Return the ledgers changed since the session began that its transcript names or list it."""

    directory = ledger_directory()

    if not directory.is_dir():
        return []

    names, started = transcript_ledgers(hook_input["transcript_path"])
    session_id = hook_input["session_id"]
    named = {directory / os.fsdecode(name) for name in names}
    listed = set(directory.iterdir()) if session_id is not None else set()
    written = (path for path in named | listed if is_written_since(path, started))

    return sorted(
        path
        for path in written
        if path in named
        or (
            session_id is not None
            and path.suffix in LEDGER_SUFFIXES
            and lists_session(path, session_id)
        )
    )


def create_session_ledger(session_id: str) -> Path | None:
    """Create the session's empty ledger file unless it exists."""

    directory = ledger_directory()

    directory.mkdir(mode=0o700, parents=True, exist_ok=True)

    path = directory / f"session-{session_id}.yaml"
    descriptor, temporary = tempfile.mkstemp(dir=directory, prefix=".session-", suffix=".tmp")

    try:
        with os.fdopen(descriptor, "w") as handle:
            handle.write(SESSION_LEDGER_TEMPLATE.format(session_id=session_id))

        os.link(temporary, path)
    except FileExistsError:
        return None
    finally:
        os.unlink(temporary)

    return path
