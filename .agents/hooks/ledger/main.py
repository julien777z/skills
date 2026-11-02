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


def read_hook_input() -> HookInput:
    """Read the turn-end payload the harness writes to standard input."""

    payload: object = json.load(sys.stdin)

    if not isinstance(payload, dict):
        raise TypeError("The hook input is not a JSON object")

    transcript_path = payload.get("transcript_path")

    return HookInput(
        stop_hook_active=payload.get("stop_hook_active") is True,
        transcript_path=transcript_path if isinstance(transcript_path, str) else None,
    )


def main() -> int:
    """Block the turn's end while a ledger the session names owes a backup comment."""

    hook_input = read_hook_input()

    if hook_input["stop_hook_active"]:
        return 0

    ledgers = session_ledgers(hook_input)

    if not ledgers:
        return 0

    if yaml is None:
        print("Ledger backups were not checked: PyYAML is not installed", file=sys.stderr)

        return UNCHECKED_EXIT

    reports: list[str] = []

    for ledger in ledgers:
        try:
            findings = ledger_findings(yaml.safe_load(ledger.read_text()))
        except (OSError, UnicodeDecodeError, yaml.YAMLError, LedgerFormatError) as error:
            reports.append(f"{ledger} could not be read: {error}")

            continue

        if findings:
            reports.append(
                f"{ledger} has entries missing their backup comment:\n" + "\n".join(findings)
            )

    if not reports:
        return 0

    reports.append(
        "Post or edit each backup comment as session-ledger's Backup section says, "
        "record its URL in the entry, and then end the turn."
    )

    print("\n\n".join(reports), file=sys.stderr)

    return BLOCK_EXIT


if __name__ == "__main__":
    sys.exit(main())
