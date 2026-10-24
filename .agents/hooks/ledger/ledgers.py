import json
import os
from pathlib import Path
from typing import Final

from models import HookInput, LedgerStamp

LEDGER_DIRECTORY_NAME: Final = "agent-ledgers"
LEDGER_SUFFIXES: Final = (".yaml", ".yml")
CHECK_SUFFIX: Final = ".ledger-check"


def ledger_directory() -> Path:
    state_home = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")

    return Path(state_home) / LEDGER_DIRECTORY_NAME


def discover_ledgers(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []

    return sorted(
        path
        for path in directory.iterdir()
        if path.suffix in LEDGER_SUFFIXES and not path.name.startswith(".") and path.is_file()
    )


def select_session_ledgers(ledgers: list[Path], hook_input: HookInput) -> list[Path]:
    transcript_path = hook_input.get("transcript_path")

    if not transcript_path:
        return ledgers

    try:
        transcript = Path(transcript_path).read_bytes()
    except OSError:
        return ledgers

    return [
        ledger
        for ledger in ledgers
        if f"{LEDGER_DIRECTORY_NAME}/{ledger.name}".encode() in transcript
    ]


def stamp_path(ledger: Path) -> Path:
    return ledger.with_name(f"{ledger.name}{CHECK_SUFFIX}")


def current_stamp(ledger: Path) -> LedgerStamp:
    status = ledger.stat()

    return LedgerStamp(path=str(ledger), size=status.st_size, mtime_ns=status.st_mtime_ns)


def is_unchanged_since_clean_check(ledger: Path, stamp: LedgerStamp) -> bool:
    try:
        recorded: object = json.loads(stamp_path(ledger).read_text())
    except (OSError, json.JSONDecodeError):
        return False

    return recorded == stamp


def record_clean_check(ledger: Path, stamp: LedgerStamp) -> None:
    try:
        descriptor = os.open(stamp_path(ledger), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)

        with os.fdopen(descriptor, "w") as handle:
            json.dump(stamp, handle)
    except OSError:
        return


def clear_clean_check(ledger: Path) -> None:
    try:
        stamp_path(ledger).unlink(missing_ok=True)
    except OSError:
        return


def remove_orphaned_stamps(directory: Path) -> None:
    for stamp in directory.glob(f"*{CHECK_SUFFIX}"):
        if not stamp.with_name(stamp.name.removesuffix(CHECK_SUFFIX)).exists():
            stamp.unlink(missing_ok=True)
