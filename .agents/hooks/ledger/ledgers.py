import os
from pathlib import Path
from typing import Final

from models import HookInput

LEDGER_DIRECTORY_NAME: Final[str] = "agent-ledgers"
LEDGER_SUFFIXES: Final[frozenset[str]] = frozenset({".yaml", ".yml"})


def ledger_directory() -> Path:
    """Return the private directory that holds task ledgers."""

    state_home = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")

    return Path(state_home) / LEDGER_DIRECTORY_NAME


def session_ledgers(hook_input: HookInput) -> list[Path]:
    """Return the ledgers the session's transcript names."""

    transcript_path = hook_input["transcript_path"]
    directory = ledger_directory()

    if transcript_path is None or not directory.is_dir():
        return []

    try:
        transcript = Path(transcript_path).read_bytes()
    except OSError:
        return []

    return sorted(
        path
        for path in directory.iterdir()
        if path.suffix in LEDGER_SUFFIXES
        and f"{LEDGER_DIRECTORY_NAME}/{path.name}".encode() in transcript
    )
