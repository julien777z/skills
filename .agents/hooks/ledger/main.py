#!/usr/bin/env python3
import json
import sys
from typing import Final

from backups import YAML_AVAILABLE, check_ledger
from ledgers import (
    clear_clean_check,
    current_stamp,
    discover_ledgers,
    is_unchanged_since_clean_check,
    ledger_directory,
    record_clean_check,
    remove_orphaned_stamps,
    select_session_ledgers,
)
from models import HookInput, LedgerFormatError

BLOCK_EXIT: Final = 2
UNCHECKED_EXIT: Final = 1


def read_hook_input() -> HookInput:
    if sys.stdin is None or sys.stdin.isatty():
        return HookInput()

    try:
        payload: object = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return HookInput()

    if not isinstance(payload, dict):
        return HookInput()

    hook_input = HookInput()

    if payload.get("stop_hook_active") is True:
        hook_input["stop_hook_active"] = True

    transcript_path = payload.get("transcript_path")

    if isinstance(transcript_path, str):
        hook_input["transcript_path"] = transcript_path

    return hook_input


def main() -> int:
    hook_input = read_hook_input()

    if hook_input.get("stop_hook_active"):
        return 0

    directory = ledger_directory()
    ledgers = select_session_ledgers(discover_ledgers(directory), hook_input)

    if directory.is_dir():
        remove_orphaned_stamps(directory)

    reports: list[str] = []
    unchecked: list[str] = []

    for ledger in ledgers:
        try:
            stamp = current_stamp(ledger)
        except OSError:
            continue

        if is_unchanged_since_clean_check(ledger, stamp):
            continue

        try:
            findings = check_ledger(ledger)
        except LedgerFormatError as error:
            clear_clean_check(ledger)

            if not YAML_AVAILABLE:
                unchecked.append(f"{ledger}: {error}")
            else:
                reports.append(f"{ledger} could not be read: {error}")

            continue

        if not findings:
            record_clean_check(ledger, stamp)

            continue

        clear_clean_check(ledger)
        reports.append(
            f"{ledger} has entries missing their backup comment:\n" + "\n".join(findings)
        )

    if reports:
        reports.append(
            "Post or edit each backup comment as session-ledger's Backup section says, "
            "record its URL in the entry, and then end the turn."
        )
        print("\n\n".join(reports), file=sys.stderr)

        return BLOCK_EXIT

    if unchecked:
        print("Ledger backups were not checked:\n" + "\n".join(unchecked), file=sys.stderr)

        return UNCHECKED_EXIT

    return 0


if __name__ == "__main__":
    sys.exit(main())
