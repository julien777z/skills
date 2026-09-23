from argparse import ArgumentParser, ArgumentTypeError, Namespace
from datetime import datetime, timedelta
from json import dumps
from os import environ
from pathlib import Path
from sys import argv, stderr

from locks import (
    DEFAULT_TTL,
    MAX_TTL,
    acquire_resource,
    check_ownership,
    ownership_status,
    read_ownership,
    read_receipt,
    release_ownership,
    resource_path,
)
from models.ownership import Acquisition, CommandResult, LockResult, Outcome
from utils import exclusive_file, positive_seconds, run_command


def parse_ttl(value: str) -> float:
    """Validate the CLI duration without allocating an excessive timedelta."""

    seconds = positive_seconds(value)

    if seconds > MAX_TTL.total_seconds():
        raise ArgumentTypeError("must not exceed 1800 seconds (30 minutes)")

    return seconds


def create_parser() -> ArgumentParser:
    """Describe resource ownership commands."""

    parser = ArgumentParser(
        description="Exclusive resource ownership with automatic expiry and no heartbeats"
    )
    commands = parser.add_subparsers(dest="command", required=True)

    for command in ("acquire", "consume"):
        acquire_parser = commands.add_parser(command)
        acquire_parser.add_argument("key")
        acquire_parser.add_argument("--state-dir", type=Path, default=Path.home() / ".local/state/agent-lock")
        acquire_parser.add_argument("--owner", required=True)
        acquire_parser.add_argument("--activity", required=True)
        acquire_parser.add_argument("--receipt", type=Path, required=True)
        acquire_parser.add_argument("--wait-seconds", type=positive_seconds, default=50)
        acquire_parser.add_argument("--ttl-seconds", type=parse_ttl, default=DEFAULT_TTL.total_seconds())

    status_parser = commands.add_parser("status")
    status_parser.add_argument("key")
    status_parser.add_argument("--state-dir", type=Path, default=Path.home() / ".local/state/agent-lock")

    for command in ("check", "release"):
        receipt_parser = commands.add_parser(command)
        receipt_parser.add_argument("--receipt", type=Path, required=True)

        if command == "release":
            receipt_parser.add_argument("--resource-idle", action="store_true", required=True)

    return parser


def consume(
    request: Acquisition, acquired: LockResult, child_command: list[str]
) -> tuple[CommandResult, int]:
    """Run a protected command and release ownership."""

    ownership = acquired.get("ownership")

    if ownership is None:
        raise ValueError("An acquired lock must identify its owner")

    receipt = read_receipt(request["receipt_path"])

    try:
        result = run_command(
            child_command,
            {**environ, "AGENT_LOCK_RECEIPT": str(request["receipt_path"])},
            ownership["expires_at"],
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
                key=options.key,
                state_directory=options.state_dir,
                owner=options.owner,
                activity=options.activity,
                receipt_path=options.receipt.expanduser().resolve(),
                wait=timedelta(seconds=options.wait_seconds),
                ttl=timedelta(seconds=options.ttl_seconds),
            )
            result = acquire_resource(request)

            if result["status"] == Outcome.BUSY:
                exit_code = 2
            elif options.command == "consume":
                result, exit_code = consume(request, result, child_command)

        case "check" | "release":
            receipt = read_receipt(options.receipt)

            if options.command == "check":
                result = check_ownership(receipt)
            else:
                if not release_ownership(receipt):
                    raise ValueError("This receipt no longer owns the resource. Stop acting on it.")

                result = LockResult(status=Outcome.RELEASED)

        case "status":
            path = resource_path(options.state_dir, options.key)

            with exclusive_file(path):
                result = ownership_status(read_ownership(path))

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

    try:
        result, exit_code = execute(options, child_command)
        print(dumps(result, default=datetime.isoformat))
        return exit_code
    except (OSError, ValueError, OverflowError) as error:
        print(dumps(LockResult(status=Outcome.ERROR, message=str(error))), file=stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(argv[1:]))
