#!/usr/bin/env python3
import json
import re
import sys
from types import ModuleType
from typing import Final

from backups import ledger_findings
from ledgers import create_session_ledger, session_ledgers
from models import HookInput, LedgerFormatError

try:
    import yaml
except ImportError:
    yaml: ModuleType | None = None

BLOCK_EXIT: Final[int] = 2
UNCHECKED_EXIT: Final[int] = 1
FOLLOWUP_EVENT_NAME: Final[str] = "stop"
SESSION_ID_FIELDS: Final[tuple[str, ...]] = ("session_id", "conversation_id")
SESSION_ID_PATTERN: Final[re.Pattern[str]] = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")
CREATED_LEDGER_STEP: Final[str] = (
    "No ledger recorded this session, so {path} was created as its ledger, as "
    "session-ledger's Storage says. Record in it whatever session-ledger's Workflow keeps from "
    "this session's work so far, if anything. When this session continues a task whose ledger "
    "already exists, add the session ID this file lists under sessions to that ledger instead, "
    "move anything recorded here into it and delete this file. Then end the turn."
)

MISSING_BACKUPS_STEP: Final[str] = (
    "Post or edit each backup comment as session-ledger's Backup section says, "
    "record its URL in the entry, and then end the turn."
)

UNREADABLE_LEDGERS_STEP: Final[str] = (
    "Repair each unreadable ledger so it follows session-ledger's Output format, "
    "and then end the turn."
)


def session_identity(payload: dict[object, object]) -> str | None:
    """Read the session's ID from the harness's field for it, when it is safe in a file name."""

    for field in SESSION_ID_FIELDS:
        value = payload.get(field)

        if isinstance(value, str):
            return value if SESSION_ID_PATTERN.fullmatch(value) else None

    return None


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
        session_id=session_identity(payload),
    )


def deliver(hook_input: HookInput, message: str) -> int:
    """Hand the agent a message it must act on before the turn ends."""

    if hook_input["expects_followup_message"]:
        print(json.dumps({"followup_message": message}))

        return 0

    print(message, file=sys.stderr)

    return BLOCK_EXIT


def main() -> int:
    """Create the session's ledger when none records it, then hold the turn for missing backups."""

    hook_input = read_hook_input()

    if hook_input["is_continuation"]:
        return 0

    ledgers = session_ledgers(hook_input)

    if not ledgers:
        if hook_input["session_id"] is None:
            return 0

        try:
            created = create_session_ledger(hook_input["session_id"])
        except OSError as error:
            print(f"The session's ledger could not be created: {error}", file=sys.stderr)

            return UNCHECKED_EXIT

        if created is None:
            return 0

        return deliver(hook_input, CREATED_LEDGER_STEP.format(path=created))

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

    return deliver(hook_input, "\n\n".join(reports))


if __name__ == "__main__":
    sys.exit(main())
