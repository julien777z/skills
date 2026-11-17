import json
import os
import shlex
import subprocess
import sys
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from datetime import timedelta
from pathlib import Path
from types import MappingProxyType
from typing import Final

from studio_mcp.models import (AgentLockAcquireReport, AgentLockCheckReport, AgentLockReceipt, EditorSlot, RunnerConfig,
                               RunnerLease, RunnerOperation)

# Paths stay on the unresolved install link: installed skills sit side by side there, and a refresh that replaces
# the linked source mid-run leaves them valid.
SCRIPTS: Final[Path] = Path(__file__).absolute().parents[1]
RUNNER_SSH: Final[Path] = SCRIPTS / "runner_ssh.sh"
AGENT_LOCK: Final[Path] = SCRIPTS.parents[1] / "agent-lock" / "resources" / "main.py"
OPERATION_TIMEOUTS: Final[Mapping[RunnerOperation, timedelta]] = MappingProxyType({
    RunnerOperation.INITIALIZE: timedelta(seconds=55),
    RunnerOperation.TOOL_CALL: timedelta(seconds=55),
    RunnerOperation.COPY: timedelta(seconds=120),
    RunnerOperation.LAUNCH: timedelta(seconds=60),
    RunnerOperation.CAPTURE: timedelta(seconds=60),
    RunnerOperation.EDIT_PROBE: timedelta(seconds=15),
    RunnerOperation.PROCESS_LIST: timedelta(seconds=30),
    RunnerOperation.STOP: timedelta(seconds=60),
    RunnerOperation.REMOVAL: timedelta(seconds=30),
    RunnerOperation.LOCK_CHECK: timedelta(seconds=30),
    RunnerOperation.DESCRIBE: timedelta(seconds=30),
    RunnerOperation.SESSION_EXIT: timedelta(seconds=5),
    RunnerOperation.HELPER_CHECK: timedelta(seconds=10),
    # Reading a starved Studio's windows through System Events can take most of a minute.
    RunnerOperation.PLUGIN_ALERT: timedelta(seconds=90),
    RunnerOperation.DIAGNOSIS: timedelta(seconds=15),
})
LEASE_CHECK_BOUND: Final[timedelta] = (OPERATION_TIMEOUTS[RunnerOperation.DESCRIBE]
                                       + OPERATION_TIMEOUTS[RunnerOperation.LOCK_CHECK])
LOCK_WAIT: Final[timedelta] = timedelta(seconds=50)
# agent-lock refuses a lease longer than this.
MAX_LEASE: Final[timedelta] = timedelta(seconds=900)
FOCUS_LEASE: Final[timedelta] = timedelta(seconds=120)
# agent-lock's exit status for a lock that stayed held through the wait.
AGENT_LOCK_BUSY: Final[int] = 2


class RunnerLockBusy(RuntimeError):
    """A runner lock other sessions kept held for the whole wait."""


def runner_config() -> RunnerConfig:
    """Return the game's runner configuration as its settings files name it now."""

    result = subprocess.run([str(RUNNER_SSH), "--describe"], capture_output=True, text=True,
                            timeout=OPERATION_TIMEOUTS[RunnerOperation.DESCRIBE].total_seconds())

    if result.returncode != 0:
        raise RuntimeError(f"No runner VM resolved for this game:\n{result.stderr}")

    values = dict(assignment.split("=", 1) for assignment in shlex.split(result.stdout))
    editors = int(values["ROBLOX_STUDIO_EDITORS"])

    if editors < 1:
        raise RuntimeError(f"ROBLOX_STUDIO_EDITORS must name at least one editor, not {editors}")

    return RunnerConfig(ROBLOX_STUDIO_GAME=values["ROBLOX_STUDIO_GAME"],
                        ROBLOX_STUDIO_TART=values["ROBLOX_STUDIO_TART"],
                        ROBLOX_STUDIO_VM=values["ROBLOX_STUDIO_VM"],
                        ROBLOX_STUDIO_SSH_USER=values["ROBLOX_STUDIO_SSH_USER"],
                        ROBLOX_STUDIO_SSH_KEY=values["ROBLOX_STUDIO_SSH_KEY"],
                        ROBLOX_STUDIO_KNOWN_HOSTS=values["ROBLOX_STUDIO_KNOWN_HOSTS"],
                        ROBLOX_STUDIO_EDITORS=editors)


def runner_environment(config: RunnerConfig) -> dict[str, str]:
    """Return the environment that holds runner_ssh.sh to the game a lease check resolved."""

    return {**os.environ, "ROBLOX_STUDIO_GAME": config["ROBLOX_STUDIO_GAME"]}


def editor_slots(config: RunnerConfig) -> list[EditorSlot]:
    """Return the game's pool of editors."""

    vm = config["ROBLOX_STUDIO_VM"]

    return [EditorSlot(number=number, lock_key=f"{vm}/editor-{number}", project=f"editor-{number}")
            for number in range(1, config["ROBLOX_STUDIO_EDITORS"] + 1)]


def focus_lock_key(config: RunnerConfig) -> str:
    """Return the lock key for input and captures that reach only the guest's frontmost window."""

    return f"{config['ROBLOX_STUDIO_VM']}/focus"


def member_receipt(lock_receipt: Path, slot: EditorSlot) -> Path:
    """Return where a whole-VM lease keeps its receipt for one editor's lock."""

    return lock_receipt.with_name(f"{lock_receipt.stem}.{slot['project']}.json")


def agent_lock_status(output: str) -> str | None:
    """Return the status agent-lock printed, or None when it printed no report, as when Python cannot start it."""

    try:
        report = json.loads(output)
    except json.JSONDecodeError:
        return None

    return report.get("status") if isinstance(report, dict) else None


def acquire_lock(keys: Sequence[str], lock_receipt: Path, owner: str, activity: str, lease: timedelta,
                 wait: timedelta, priority: bool = False) -> AgentLockAcquireReport:
    """Take one of the keys through agent-lock, writing its receipt to lock_receipt, or raise when they stay busy."""

    lock_receipt.parent.mkdir(parents=True, exist_ok=True)

    choice = ["--any"] if len(keys) > 1 else []
    ordering = ["--priority"] if priority else []

    result = subprocess.run([sys.executable, str(AGENT_LOCK), "acquire", *keys, *choice, *ordering, "--owner", owner,
                             "--activity", activity, "--receipt", str(lock_receipt), "--wait-seconds",
                             str(wait.total_seconds()), "--ttl-seconds", str(lease.total_seconds())],
                            capture_output=True, text=True,
                            timeout=(wait + OPERATION_TIMEOUTS[RunnerOperation.LOCK_CHECK]).total_seconds())

    if result.returncode == AGENT_LOCK_BUSY and agent_lock_status(result.stdout) == "busy":
        raise RunnerLockBusy(f"The {' or '.join(keys)} lock stayed held:\n{result.stdout}")

    if result.returncode != 0:
        raise RuntimeError(f"The {' or '.join(keys)} lock was not acquired ({result.returncode}):\n"
                           f"{result.stdout}{result.stderr}")

    return json.loads(result.stdout)


def release_lock(lock_receipt: Path) -> None:
    """Release the lock a receipt owns, stating to agent-lock that its resource is idle."""

    result = subprocess.run([sys.executable, str(AGENT_LOCK), "release", "--receipt", str(lock_receipt),
                             "--resource-idle"], capture_output=True, text=True,
                            timeout=OPERATION_TIMEOUTS[RunnerOperation.LOCK_CHECK].total_seconds())

    if result.returncode != 0:
        raise RuntimeError(f"Receipt {lock_receipt} did not release its lock:\n{result.stderr}")


def acquire_editor_lock(lock_receipt: Path, owner: str, activity: str, lease: timedelta = MAX_LEASE,
                        wait: timedelta = LOCK_WAIT) -> AgentLockAcquireReport:
    """Take whichever of the game's editors comes free first for one segment of a check."""

    keys = [slot["lock_key"] for slot in editor_slots(runner_config())]

    return acquire_lock(keys, lock_receipt, owner, activity, lease, wait)


def acquire_runner_lock(lock_receipt: Path, owner: str, activity: str, lease: timedelta = MAX_LEASE,
                        wait: timedelta = LOCK_WAIT, priority: bool = False) -> AgentLockAcquireReport:
    """Take the whole runner VM: its own lock, then every editor's lock once that editor is free."""

    config = runner_config()
    vm = config["ROBLOX_STUDIO_VM"]
    receipts = {vm: lock_receipt, **{slot["lock_key"]: member_receipt(lock_receipt, slot)
                                     for slot in editor_slots(config)}}
    reports: dict[str, AgentLockAcquireReport] = {}
    taken: list[Path] = []
    acquired = False

    try:
        for key in sorted(receipts):
            reports[key] = acquire_lock([key], receipts[key], owner, activity, lease, wait, priority)
            taken.append(receipts[key])

        acquired = True
    finally:
        if not acquired:
            for receipt in reversed(taken):
                release_lock(receipt)
                receipt.unlink(missing_ok=True)

    return reports[vm]


def release_runner_lock(lock_receipt: Path) -> None:
    """Release the editor or the whole VM a receipt holds, stating to agent-lock that it is idle."""

    for slot in reversed(editor_slots(runner_config())):
        receipt = member_receipt(lock_receipt, slot)

        if receipt.is_file():
            release_lock(receipt)
            receipt.unlink()

    release_lock(lock_receipt)


def runner_lease(lock_receipt: Path) -> RunnerLease:
    """Return the game's runner, the editor the receipt holds, and how long its lease has left."""

    config = runner_config()
    vm = config["ROBLOX_STUDIO_VM"]

    result = subprocess.run([sys.executable, str(AGENT_LOCK), "check", "--receipt", str(lock_receipt)],
                            capture_output=True, text=True,
                            timeout=OPERATION_TIMEOUTS[RunnerOperation.LOCK_CHECK].total_seconds())

    if result.returncode != 0:
        raise RuntimeError(f"Receipt {lock_receipt} does not own a lock:\n{result.stderr}")

    report: AgentLockCheckReport = json.loads(result.stdout)
    key = report["ownership"]["key"]
    editor = next((slot for slot in editor_slots(config) if slot["lock_key"] == key), None)

    if editor is None and key != vm:
        raise RuntimeError(f"Receipt {lock_receipt} owns {key}, not {vm} or one of its editors")

    return RunnerLease(config=config, editor=editor, remaining=timedelta(seconds=report["remaining_seconds"]))


def assert_runner_lease_covers(lock_receipt: Path, needed: timedelta) -> RunnerConfig:
    """Assert that the receipt owns the game's runner or one of its editors for at least the needed time."""

    lease = runner_lease(lock_receipt)

    if lease["remaining"] < needed:
        raise RuntimeError(f"The {lease['config']['ROBLOX_STUDIO_VM']} lease has "
                           f"{lease['remaining'].total_seconds():.0f} s left; this call can take up to "
                           f"{needed.total_seconds():.0f} s")

    return lease["config"]


@contextmanager
def focused_input(lock_receipt: Path, activity: str, hold: timedelta = FOCUS_LEASE,
                  wait: timedelta = LOCK_WAIT) -> Iterator[None]:
    """Hold the guest's focus for an editor launch, or input or a capture that reaches only its frontmost window."""

    config = assert_runner_lease_covers(lock_receipt, wait + hold)
    focus_receipt = lock_receipt.with_name(f"{lock_receipt.stem}.focus.json")

    acquire_lock([focus_lock_key(config)], focus_receipt, f"focus for {lock_receipt.stem}", activity, hold, wait)

    try:
        yield
    finally:
        release_lock(focus_receipt)
        focus_receipt.unlink(missing_ok=True)


def run_in_runner(command: str, lock_receipt: Path, timeout: timedelta, data: bytes | None = None) -> bytes:
    """Run a shell command in the runner guest."""

    return run_guest_command(command, assert_runner_lease_covers(lock_receipt, timeout), timeout, data)


def run_guest_command(command: str, config: RunnerConfig, timeout: timedelta, data: bytes | None = None) -> bytes:
    """Run a shell command in the guest of a runner whose lease the caller has already checked."""

    # The guest's login shell may be zsh, which splits words differently, so commands always run under sh.
    result = subprocess.run([str(RUNNER_SSH), f"/bin/sh -c {shlex.quote(command)}"], input=data,
                            capture_output=True, timeout=timeout.total_seconds(), env=runner_environment(config))

    if result.returncode != 0:
        raise RuntimeError(f"Runner command failed ({result.returncode}): {command}\n{result.stderr.decode()}")

    return result.stdout


def held_editor_slots(lock_receipt: Path, config: RunnerConfig) -> tuple[list[EditorSlot], bool]:
    """Return the editors of the pool a receipt holds, read from the receipt its caller has checked, and whether it
    holds the whole VM with every editor."""

    receipt: AgentLockReceipt = json.loads(lock_receipt.read_text())
    slots = editor_slots(config)
    editor = next((slot for slot in slots if slot["lock_key"] == receipt["key"]), None)

    if editor is not None:
        return [editor], False

    held = [slot for slot in slots if member_receipt(lock_receipt, slot).is_file()]

    return held, len(held) == len(slots)


def editor_launch_refusal(project: str | None, held: Sequence[EditorSlot], whole_vm: bool, pool_size: int,
                          running: int) -> str | None:
    """Return why a lease may not launch another editor, or None when it may.

    An editor launches under one editor's lock, in that editor's project folder, or under the whole VM, and never past
    the pool's size. A project of None is a published place, which has no project folder.
    """

    if not whole_vm and len(held) != 1:
        return (f"The lease holds only the VM's own lock, not one of its {pool_size} editors; an editor launches only "
                "under one editor's lock or the whole VM's. Tooling that takes the VM's lock alone to open an editor "
                "predates the pool of editors; update it.")

    if not whole_vm and project is not None and project != held[0]["project"]:
        return (f"The {held[0]['lock_key']} lock launches editors only in its project {held[0]['project']}, "
                f"not {project}")

    if running >= pool_size:
        return f"The VM already runs {running} editors, its pool's size; close one before launching another"

    return None


def assert_editor_launch_allowed(lock_receipt: Path, config: RunnerConfig, project: str | None,
                                 running: set[int]) -> None:
    """Raise unless the receipt's lease may launch an editor in the project beside the running editors."""

    held, whole_vm = held_editor_slots(lock_receipt, config)
    refusal = editor_launch_refusal(project, held, whole_vm, config["ROBLOX_STUDIO_EDITORS"], len(running))

    if refusal:
        raise RuntimeError(f"{refusal}: running editors {sorted(running)}")
