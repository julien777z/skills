#!/usr/bin/env python3
import json
import logging
import os
import re
import sys
from pathlib import Path
from types import ModuleType
from typing import Final

from documents import is_untouched_session_ledger, ledger_findings, ledger_sessions
from ledgers import create_session_ledger, session_ledger_path, session_ledgers
from models import HookInput, HookOutcome, LedgerFormatError

try:
    import yaml
except ImportError:
    yaml: ModuleType | None = None

logger = logging.getLogger(__name__)

FOLLOWUP_EVENT_NAME: Final[str] = "stop"
SESSION_END_EVENT_NAMES: Final[frozenset[str]] = frozenset({"SessionEnd", "sessionEnd"})
SESSION_ID_FIELDS: Final[tuple[str, ...]] = ("session_id", "conversation_id")
SESSION_ID_PATTERN: Final[re.Pattern[str]] = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")
PROMPTS_DIRECTORY: Final[Path] = Path(os.path.abspath(__file__)).parent / "prompts"
CREATED_LEDGER_PROMPT_FILENAME: Final[str] = "created-ledger.md"
MISSING_BACKUPS_PROMPT_FILENAME: Final[str] = "missing-backups.md"
UNREADABLE_LEDGERS_PROMPT_FILENAME: Final[str] = "unreadable-ledgers.md"
REPLY_PROMPT_FILENAME: Final[str] = "reply.md"


def prompt(filename: str) -> str:
    """Read one of the hook's prompts to the agent."""

    return (PROMPTS_DIRECTORY / filename).read_text(encoding="utf-8").strip()


def session_identity(payload: dict[object, object]) -> str | None:
    """Read the session's file-name-safe ID from the harness payload."""

    value = next(
        (payload[field] for field in SESSION_ID_FIELDS if isinstance(payload.get(field), str)),
        None,
    )

    return value if isinstance(value, str) and SESSION_ID_PATTERN.fullmatch(value) else None


def read_hook_input() -> HookInput:
    """Read the turn-end or session-end payload the harness writes to standard input."""

    payload: object = json.load(sys.stdin)

    if not isinstance(payload, dict):
        raise TypeError("The hook input is not a JSON object")

    transcript_path = payload.get("transcript_path")
    loop_count = payload.get("loop_count")

    return HookInput(
        is_session_end=payload.get("hook_event_name") in SESSION_END_EVENT_NAMES,
        is_continuation=payload.get("stop_hook_active") is True
        or (isinstance(loop_count, int) and loop_count > 0),
        expects_followup_message=payload.get("hook_event_name") == FOLLOWUP_EVENT_NAME,
        transcript_path=transcript_path if isinstance(transcript_path, str) else None,
        session_id=session_identity(payload),
    )


def deliver(hook_input: HookInput, message: str) -> HookOutcome:
    """Hand the agent the work this message names and the instruction to end with its reply."""

    message = f"{message}\n\n{prompt(REPLY_PROMPT_FILENAME)}"

    if hook_input["expects_followup_message"]:
        print(json.dumps({"followup_message": message}))

        return HookOutcome.END_TURN

    print(message, file=sys.stderr)

    return HookOutcome.HOLD_TURN


def create_ledger(hook_input: HookInput) -> HookOutcome:
    """Create the session's ledger and name it to the agent."""

    if hook_input["session_id"] is None:
        return HookOutcome.END_TURN

    try:
        created = create_session_ledger(hook_input["session_id"])
    except OSError as error:
        logger.error("The session's ledger could not be created: %s", error)

        return HookOutcome.FAILED

    if created is None:
        return HookOutcome.END_TURN

    return deliver(hook_input, prompt(CREATED_LEDGER_PROMPT_FILENAME).format(path=created))


def end_session(hook_input: HookInput) -> HookOutcome:
    """Remove the session's ledger when nothing was recorded in it."""

    session_id = hook_input["session_id"]

    if session_id is None:
        return HookOutcome.END_TURN

    path = session_ledger_path(session_id)

    try:
        text = path.read_text()
    except FileNotFoundError:
        return HookOutcome.END_TURN
    except (OSError, UnicodeDecodeError) as error:
        logger.error("The session's ledger could not be read: %s", error)

        return HookOutcome.FAILED

    if yaml is None:
        logger.error("The session's ledger was not checked: PyYAML is not installed")

        return HookOutcome.FAILED

    try:
        if is_untouched_session_ledger(yaml.safe_load(text), session_id):
            path.unlink()
    except (OSError, yaml.YAMLError, LedgerFormatError) as error:
        logger.error("The session's ledger was kept: %s", error)

        return HookOutcome.FAILED

    return HookOutcome.END_TURN


def main() -> HookOutcome:
    """Run the ledger hook for the event the harness reports."""

    hook_input = read_hook_input()

    if hook_input["is_session_end"]:
        return end_session(hook_input)

    if hook_input["is_continuation"]:
        return HookOutcome.END_TURN

    named, mentioning = session_ledgers(hook_input)

    if not named and not mentioning:
        return create_ledger(hook_input)

    if yaml is None:
        logger.error("Ledger backups were not checked: PyYAML is not installed")

        return HookOutcome.FAILED

    checked = False
    unreadable: list[str] = []
    missing: list[str] = []

    for ledger in sorted(named | mentioning):
        try:
            document = yaml.safe_load(ledger.read_text())

            if ledger in mentioning and hook_input["session_id"] not in ledger_sessions(document):
                continue

            findings = ledger_findings(document)
        except (OSError, UnicodeDecodeError, yaml.YAMLError, LedgerFormatError) as error:
            checked = True
            unreadable.append(f"{ledger} could not be read: {error}")

            continue

        checked = True

        if findings:
            missing.append(
                f"{ledger} has entries missing their backup comment:\n" + "\n".join(findings)
            )

    if not checked:
        return create_ledger(hook_input)

    reports = unreadable + missing

    if not reports:
        return HookOutcome.END_TURN

    if unreadable:
        reports.append(prompt(UNREADABLE_LEDGERS_PROMPT_FILENAME))

    if missing:
        reports.append(prompt(MISSING_BACKUPS_PROMPT_FILENAME))

    return deliver(hook_input, "\n\n".join(reports))


if __name__ == "__main__":
    sys.exit(main().value)
