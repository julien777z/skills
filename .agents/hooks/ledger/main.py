#!/usr/bin/env python3
import json
import sys
from types import ModuleType
from typing import Final

from backups import ledger_findings
from ledgers import session_ledgers
from models import HookInput, LedgerFormatError

try:
    import yaml
except ImportError:
    yaml: ModuleType | None = None

BLOCK_EXIT: Final[int] = 2
UNCHECKED_EXIT: Final[int] = 1
FOLLOWUP_EVENT_NAME: Final[str] = "stop"
MISSING_BACKUPS_STEP: Final[str] = (
    "Post or edit each backup comment as session-ledger's Backup section says, "
    "record its URL in the entry, and then end the turn."
)
UNREADABLE_LEDGERS_STEP: Final[str] = (
    "Repair each unreadable ledger so it follows session-ledger's Output format, "
    "and then end the turn."
)


def read_hook_input() -> HookInput:
    """Read the turn-end payload the harness writes to standard input."""

    payload: object = json.load(sys.stdin)

    if not isinstance(payload, dict):
        raise TypeError("The hook input is not a JSON object")

    transcript_path = payload.get("transcript_path")
    loop_count = payload.get("loop_count")

    return HookInput(
        is_continuation=payload.get("stop_hook_active") is True
        or (isinstance(loop_count, int) and loop_count > 0),
        expects_followup_message=payload.get("hook_event_name") == FOLLOWUP_EVENT_NAME,
        transcript_path=transcript_path if isinstance(transcript_path, str) else None,
    )


def main() -> int:
    """Keep the turn going while a ledger the session writes owes a backup comment."""

    hook_input = read_hook_input()

    if hook_input["is_continuation"]:
        return 0

    ledgers = session_ledgers(hook_input)

    if not ledgers:
        return 0

    if yaml is None:
        print("Ledger backups were not checked: PyYAML is not installed", file=sys.stderr)

        return UNCHECKED_EXIT

    unreadable: list[str] = []
    missing: list[str] = []

    for ledger in ledgers:
        try:
            findings = ledger_findings(yaml.safe_load(ledger.read_text()))
        except (OSError, UnicodeDecodeError, yaml.YAMLError, LedgerFormatError) as error:
            unreadable.append(f"{ledger} could not be read: {error}")

            continue

        if findings:
            missing.append(
                f"{ledger} has entries missing their backup comment:\n" + "\n".join(findings)
            )

    reports = unreadable + missing

    if not reports:
        return 0

    if unreadable:
        reports.append(UNREADABLE_LEDGERS_STEP)

    if missing:
        reports.append(MISSING_BACKUPS_STEP)

    message = "\n\n".join(reports)

    if hook_input["expects_followup_message"]:
        print(json.dumps({"followup_message": message}))

        return 0

    print(message, file=sys.stderr)

    return BLOCK_EXIT


if __name__ == "__main__":
    sys.exit(main())
