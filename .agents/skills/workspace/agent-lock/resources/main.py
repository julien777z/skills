from argparse import ArgumentParser, Namespace
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime, timedelta
from json import dumps
from os import environ, killpg
from pathlib import Path
from signal import SIGINT, SIGKILL, SIGTERM, signal
from subprocess import Popen, TimeoutExpired
from sys import argv, stderr
from types import FrameType

from locks import (
    RENEWAL_INTERVAL,
    acquire_resource,
    last_activity,
    ownership_status,
    queued_waiters,
    read_ownership,
    read_queue,
    read_receipt,
    release_ownership,
    renew_ownership,
    resource_path,
)
from models.ownership import Acquisition, CommandResult, LockResult, Outcome, Receipt
from utils import exclusive_file, positive_seconds


def create_parser() -> ArgumentParser:
    """Describe resource ownership commands."""

    parser = ArgumentParser(
        description="Exclusive resource ownership that lasts while its holder keeps renewing it"
    )

    commands = parser.add_subparsers(dest="command", required=True)

    for command in ("acquire", "consume"):
        acquire_parser = commands.add_parser(command)
        acquire_parser.add_argument("key", nargs="+")
        acquire_parser.add_argument("--any", action="store_true")
        acquire_parser.add_argument("--state-dir", type=Path, default=Path.home() / ".local/state/agent-lock")
        acquire_parser.add_argument("--owner", required=True)
        acquire_parser.add_argument("--activity", required=True)
        acquire_parser.add_argument("--receipt", type=Path, required=True)
        acquire_parser.add_argument("--wait-seconds", type=positive_seconds, default=50)
        acquire_parser.add_argument("--priority", action="store_true")

    status_parser = commands.add_parser("status")
    status_parser.add_argument("key")
    status_parser.add_argument("--state-dir", type=Path, default=Path.home() / ".local/state/agent-lock")

    for command in ("check", "release"):
        receipt_parser = commands.add_parser(command)
        receipt_parser.add_argument("--receipt", type=Path, required=True)

        if command == "release":
            receipt_parser.add_argument("--resource-idle", action="store_true", required=True)

    return parser


def run_command(
    command: Sequence[str],
    environment: Mapping[str, str],
    receipt: Receipt,
) -> CommandResult:
    """Run a foreground process group to completion while renewing the receipt's lock."""

    def _interrupt(signum: int, _frame: FrameType | None) -> None:
        """Interrupt the supervisor's blocking wait."""

        raise InterruptedError(signum)

    previous_handlers = {signum: signal(signum, _interrupt) for signum in (SIGINT, SIGTERM)}

    try:
        try:
            renew_ownership(receipt)
        except ValueError:
            return CommandResult(status=Outcome.EXPIRED, command_exit_code=124, interrupted_by=None)

        outcome = Outcome.COMPLETED
        interrupted_by: int | None = None

        with Popen(command, env=environment, stdout=stderr, start_new_session=True) as child:
            try:
                while True:
                    try:
                        child.wait(timeout=RENEWAL_INTERVAL.total_seconds())
                    except TimeoutExpired:
                        renew_ownership(receipt)
                        continue

                    break
            except ValueError:
                outcome = Outcome.EXPIRED
            except InterruptedError as error:
                outcome = Outcome.INTERRUPTED
                interrupted_by = int(error.args[0])
            finally:
                try:
                    killpg(child.pid, SIGKILL)
                except ProcessLookupError:
                    pass

                child.wait()

            return CommandResult(
                status=outcome,
                command_exit_code=child.returncode,
                interrupted_by=interrupted_by,
            )
    finally:
        for signum, handler in previous_handlers.items():
            signal(signum, handler)


def consume(
    request: Acquisition, acquired: LockResult, child_command: list[str]
) -> tuple[CommandResult, int]:
    """Run a protected command, renewing ownership while it runs, and release ownership."""

    ownership = acquired.get("ownership")

    if ownership is None:
        raise ValueError("An acquired lock must identify its owner")

    receipt = read_receipt(request["receipt_path"])

    try:
        result = run_command(
            child_command,
            {**environ, "AGENT_LOCK_RECEIPT": str(request["receipt_path"])},
            receipt,
        )
    finally:
        release_ownership(receipt)

    match result["status"]:
        case Outcome.EXPIRED:
            exit_code = 124
        case Outcome.INTERRUPTED:
            exit_code = 128 + (result["interrupted_by"] or 0)
        case _:
            code = result["command_exit_code"]
            exit_code = 128 - code if code < 0 else code

    return result, exit_code


def execute(options: Namespace, child_command: list[str]) -> tuple[LockResult | CommandResult, int]:
    """Apply one ownership command."""

    result: LockResult | CommandResult
    exit_code = 0
    match options.command:
        case "acquire" | "consume":
            request = Acquisition(
                keys=options.key,
                state_directory=options.state_dir,
                owner=options.owner,
                activity=options.activity,
                receipt_path=options.receipt.expanduser().resolve(),
                wait=timedelta(seconds=options.wait_seconds),
                priority=options.priority,
            )

            result = acquire_resource(request)

            if result["status"] == Outcome.BUSY:
                exit_code = 2
            elif options.command == "consume":
                result, exit_code = consume(request, result, child_command)

        case "check" | "release":
            receipt = read_receipt(options.receipt)

            if options.command == "check":
                result = renew_ownership(receipt)
            else:
                if not release_ownership(receipt):
                    raise ValueError("This receipt no longer owns the resource. Stop acting on it.")

                result = LockResult(status=Outcome.RELEASED)

        case "status":
            path = resource_path(options.state_dir, options.key)

            with exclusive_file(path):
                result = ownership_status(read_ownership(path))
                result["waiters"] = queued_waiters(read_queue(path), datetime.now(UTC))
                result["last_activity_at"] = last_activity(path)

        case _:
            raise ValueError("Unknown lock command")

    return result, exit_code


def main(arguments: list[str]) -> int:
    """Report a resource ownership command result."""

    parser = create_parser()
    child_command: list[str] = []

    if arguments[:1] == ["consume"] and "--" in arguments:
        separator = arguments.index("--")
        child_command = arguments[separator + 1 :]
        arguments = arguments[:separator]

    options = parser.parse_args(arguments)

    if options.command == "consume" and not child_command:
        parser.error("consume requires -- followed by a foreground command")

    if options.command in ("acquire", "consume") and len(options.key) > 1 and not options.any:
        parser.error("several keys take --any, which acquires whichever is free first")

    if options.command in ("acquire", "consume") and len(set(options.key)) != len(options.key):
        parser.error("each key is named once")

    try:
        result, exit_code = execute(options, child_command)
        print(dumps(result, default=datetime.isoformat))
        return exit_code
    except (OSError, ValueError, OverflowError) as error:
        print(dumps(LockResult(status=Outcome.ERROR, message=str(error))), file=stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(argv[1:]))
