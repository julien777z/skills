import itertools
import json
import logging
import os
import shlex
import subprocess
import sys
import threading
import time
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from datetime import timedelta
from functools import cache
from pathlib import Path
from types import MappingProxyType
from typing import Final

from studio_mcp.models import (AgentLockAcquireReport, AgentLockCheckReport, AgentLockReceipt, EditorSlot, RunnerConfig,
                               RunnerLease, RunnerOperation)

# Paths stay on the unresolved install link: installed skills sit side by side there, and a refresh that replaces
# the linked source mid-run leaves them valid.
SCRIPTS: Final[Path] = Path(__file__).absolute().parents[1]
RUNNER_SSH: Final[Path] = SCRIPTS / "runner_ssh.sh"
AGENT_LOCK_ENTRY: Final[Path] = Path("agent-lock") / "resources" / "main.py"
REPOSITORY_SKILLS: Final[tuple[str, ...]] = (".agents", "skills")
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

LOCK_WAIT: Final[timedelta] = timedelta(seconds=50)
# agent-lock expires a lock its holder leaves unrenewed for five minutes and asks for a renewal about every minute.
LOCK_RENEWAL_INTERVAL: Final[timedelta] = timedelta(minutes=1)
# The receipts this process holds, each with the acquisition it belongs to, which a background thread renews until
# each is released or lost.
RENEWED_RECEIPTS: Final[dict[Path, int]] = {}
LOST_RECEIPTS: Final[dict[Path, str | None]] = {}
RENEWED_RECEIPTS_GUARD: Final[threading.Lock] = threading.Lock()
ACQUISITIONS: Final[itertools.count[int]] = itertools.count()
# agent-lock's exit status for a lock that stayed held through the wait.
AGENT_LOCK_BUSY: Final[int] = 2

logger = logging.getLogger(__name__)


@cache
def agent_lock_script() -> Path:
    """Return agent-lock's entry script."""

    sibling = SCRIPTS.parents[1] / AGENT_LOCK_ENTRY
    repository_skills = SCRIPTS.parents[2]

    if sibling.is_file():
        return sibling

    if repository_skills.parts[-2:] != REPOSITORY_SKILLS:
        raise FileNotFoundError(f"agent-lock is not at {sibling}")

    categorized = sorted(repository_skills.glob(f"*/{AGENT_LOCK_ENTRY}"))

    if not categorized:
        raise FileNotFoundError(f"agent-lock is in neither {sibling} nor {repository_skills / '*' / AGENT_LOCK_ENTRY}")

    return categorized[0]


def renewed_lock(lock_receipt: Path) -> AgentLockCheckReport:
    """Renew the lock a receipt owns through agent-lock's check, raising when the receipt no longer owns it."""

    result = subprocess.run([sys.executable, str(agent_lock_script()), "check", "--receipt", str(lock_receipt)],
                            capture_output=True, text=True, check=False,
                            timeout=OPERATION_TIMEOUTS[RunnerOperation.LOCK_CHECK].total_seconds())

    if result.returncode != 0:
        raise RuntimeError(f"Receipt {lock_receipt} does not own a lock:\n{result.stderr}")

    return json.loads(result.stdout)


class LockOwnershipLost(RuntimeError):
    """A lock this process held that a renewal found lost, so nothing may act on its resource any more."""


def lost_lock_key(lock_receipt: Path) -> str | None:
    """Return the key a lost receipt held, or None when its receipt can no longer be read."""

    try:
        receipt: AgentLockReceipt = json.loads(lock_receipt.read_text())
    except (OSError, ValueError):
        return None

    return receipt["key"]


def record_lost_lock(lock_receipt: Path, acquisition: int) -> None:
    """Record a receipt's lock as lost, so operations on its resource stop, while that acquisition is still held."""

    key = lost_lock_key(lock_receipt)

    with RENEWED_RECEIPTS_GUARD:
        if RENEWED_RECEIPTS.get(lock_receipt) != acquisition:
            return

        del RENEWED_RECEIPTS[lock_receipt]
        LOST_RECEIPTS[lock_receipt] = key

    logger.error("Receipt %s lost its %s lock; operations on that resource stop", lock_receipt, key or "unknown")


def assert_receipts_kept(lock_receipts: Sequence[Path]) -> None:
    """Raise when a renewal found the lock of any of the receipts lost."""

    with RENEWED_RECEIPTS_GUARD:
        lost = [(receipt, LOST_RECEIPTS[receipt]) for receipt in lock_receipts if receipt in LOST_RECEIPTS]

    if lost:
        receipt, key = lost[0]

        raise LockOwnershipLost(f"Receipt {receipt} lost its {key or 'unknown'} lock")


def assert_runner_locks_kept(config: RunnerConfig) -> None:
    """Raise when a renewal found lost a lock this process held on the runner's VM, its editors or its focus."""

    vm = config["ROBLOX_STUDIO_VM"]

    with RENEWED_RECEIPTS_GUARD:
        lost = [receipt for receipt, key in LOST_RECEIPTS.items()
                if key is None or key == vm or key.startswith(f"{vm}/")]

    assert_receipts_kept(lost)


def renew_held_locks() -> None:
    """Renew every receipt this process holds once per interval."""

    while True:
        time.sleep(LOCK_RENEWAL_INTERVAL.total_seconds())

        with RENEWED_RECEIPTS_GUARD:
            receipts = sorted(RENEWED_RECEIPTS.items())

        for receipt, acquisition in receipts:
            try:
                renewed_lock(receipt)
            except RuntimeError:
                record_lost_lock(receipt, acquisition)
            except (OSError, ValueError, subprocess.TimeoutExpired):
                logger.warning("Renewing the lock of receipt %s failed; retrying at the next interval", receipt,
                               exc_info=True)


@cache
def lock_renewal_thread() -> threading.Thread:
    """Start, once per process, the daemon thread that keeps this process's locks renewed while it runs."""

    thread = threading.Thread(target=renew_held_locks, name="agent-lock renewal", daemon=True)

    thread.start()

    return thread


def keep_acquired_lock_renewed(lock_receipt: Path) -> None:
    """Renew a newly acquired receipt's lock in the background until it is released."""

    with RENEWED_RECEIPTS_GUARD:
        RENEWED_RECEIPTS[lock_receipt] = next(ACQUISITIONS)
        LOST_RECEIPTS.pop(lock_receipt, None)

    lock_renewal_thread()


def keep_held_lock_renewed(lock_receipt: Path) -> None:
    """Renew a receipt's lock in the background under its current acquisition, never reviving one found lost."""

    with RENEWED_RECEIPTS_GUARD:
        if lock_receipt not in LOST_RECEIPTS and lock_receipt not in RENEWED_RECEIPTS:
            RENEWED_RECEIPTS[lock_receipt] = next(ACQUISITIONS)

    lock_renewal_thread()


def stop_renewing_lock(lock_receipt: Path) -> None:
    """Stop the background renewal of a receipt's lock, and forget any loss recorded for it."""

    with RENEWED_RECEIPTS_GUARD:
        RENEWED_RECEIPTS.pop(lock_receipt, None)
        LOST_RECEIPTS.pop(lock_receipt, None)


class RunnerLockBusy(RuntimeError):
    """A runner lock other sessions kept held for the whole wait."""


def runner_config() -> RunnerConfig:
    """Return the game's runner configuration as its settings files name it now."""

    result = subprocess.run([str(RUNNER_SSH), "--describe"], capture_output=True, text=True, check=False,
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
        report: object = json.loads(output)
    except json.JSONDecodeError:
        return None

    match report:
        case {"status": str() as status}:
            return status
        case _:
            return None


def acquire_lock(keys: Sequence[str], lock_receipt: Path, owner: str, activity: str, wait: timedelta,
                 priority: bool = False) -> AgentLockAcquireReport:
    """Acquire one of the keys through agent-lock and keep it renewed."""

    lock_receipt.parent.mkdir(parents=True, exist_ok=True)

    choice = ["--any"] if len(keys) > 1 else []
    ordering = ["--priority"] if priority else []

    result = subprocess.run([sys.executable, str(agent_lock_script()), "acquire", *keys, *choice, *ordering,
                             "--owner", owner, "--activity", activity, "--receipt", str(lock_receipt),
                             "--wait-seconds", str(wait.total_seconds())],
                            capture_output=True, text=True, check=False,
                            timeout=(wait + OPERATION_TIMEOUTS[RunnerOperation.LOCK_CHECK]).total_seconds())

    if result.returncode == AGENT_LOCK_BUSY and agent_lock_status(result.stdout) == "busy":
        raise RunnerLockBusy(f"The {' or '.join(keys)} lock stayed held:\n{result.stdout}")

    if result.returncode != 0:
        raise RuntimeError(f"The {' or '.join(keys)} lock was not acquired ({result.returncode}):\n"
                           f"{result.stdout}{result.stderr}")

    keep_acquired_lock_renewed(lock_receipt)

    return json.loads(result.stdout)


def release_lock(lock_receipt: Path) -> None:
    """Release the lock a receipt owns, stating to agent-lock that its resource is idle."""

    stop_renewing_lock(lock_receipt)

    result = subprocess.run([sys.executable, str(agent_lock_script()), "release", "--receipt", str(lock_receipt),
                             "--resource-idle"], capture_output=True, text=True, check=False,
                            timeout=OPERATION_TIMEOUTS[RunnerOperation.LOCK_CHECK].total_seconds())

    if result.returncode != 0:
        raise RuntimeError(f"Receipt {lock_receipt} did not release its lock:\n{result.stderr}")


def acquire_editor_lock(lock_receipt: Path, owner: str, activity: str,
                        wait: timedelta = LOCK_WAIT) -> AgentLockAcquireReport:
    """Take whichever of the game's editors comes free first for a check."""

    keys = [slot["lock_key"] for slot in editor_slots(runner_config())]

    return acquire_lock(keys, lock_receipt, owner, activity, wait)


def acquire_runner_lock(lock_receipt: Path, owner: str, activity: str, wait: timedelta = LOCK_WAIT,
                        priority: bool = False) -> AgentLockAcquireReport:
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
            reports[key] = acquire_lock([key], receipts[key], owner, activity, wait, priority)
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
    """Renew a receipt's locks and return the runner and the editor it holds."""

    config = runner_config()
    vm = config["ROBLOX_STUDIO_VM"]

    assert_receipts_kept([lock_receipt, *(member_receipt(lock_receipt, slot) for slot in editor_slots(config))])

    report = renewed_lock(lock_receipt)
    key = report["ownership"]["key"]
    slots = editor_slots(config)
    editor = next((slot for slot in slots if slot["lock_key"] == key), None)

    if editor is None and key != vm:
        raise RuntimeError(f"Receipt {lock_receipt} owns {key}, not {vm} or one of its editors")

    keep_held_lock_renewed(lock_receipt)

    if editor is None:
        for slot in slots:
            receipt = member_receipt(lock_receipt, slot)

            if receipt.is_file():
                renewed_lock(receipt)

                keep_held_lock_renewed(receipt)

    return RunnerLease(config=config, editor=editor)


def assert_runner_lock_held(lock_receipt: Path) -> RunnerConfig:
    """Assert that the receipt owns the game's runner or one of its editors, renewing it, and return the runner."""

    return runner_lease(lock_receipt)["config"]


@contextmanager
def focused_input(lock_receipt: Path, activity: str, wait: timedelta = LOCK_WAIT) -> Iterator[None]:
    """Hold the guest's focus for an editor launch, or input or a capture that reaches only its frontmost window."""

    config = assert_runner_lock_held(lock_receipt)
    focus_receipt = lock_receipt.with_name(f"{lock_receipt.stem}.focus.json")

    acquire_lock([focus_lock_key(config)], focus_receipt, f"focus for {lock_receipt.stem}", activity, wait)

    try:
        yield
    finally:
        release_lock(focus_receipt)

        focus_receipt.unlink(missing_ok=True)


def run_in_runner(command: str, lock_receipt: Path, timeout: timedelta, data: bytes | None = None) -> bytes:
    """Run a shell command in the runner guest."""

    return run_guest_command(command, assert_runner_lock_held(lock_receipt), timeout, data)


def run_guest_command(command: str, config: RunnerConfig, timeout: timedelta, data: bytes | None = None) -> bytes:
    """Run a shell command in the guest of a runner whose lease the caller has already checked."""

    assert_runner_locks_kept(config)

    # The guest's login shell may be zsh, which splits words differently, so commands always run under sh.
    result = subprocess.run([str(RUNNER_SSH), f"/bin/sh -c {shlex.quote(command)}"], input=data,
                            capture_output=True, check=False, timeout=timeout.total_seconds(),
                            env=runner_environment(config))

    if result.returncode != 0:
        raise RuntimeError(f"Runner command failed ({result.returncode}): {command}\n{result.stderr.decode()}")

    return result.stdout


def held_editor_slots(lock_receipt: Path, config: RunnerConfig) -> tuple[list[EditorSlot], bool]:
    """Return the editors a checked receipt holds and whether it holds the whole VM."""

    receipt: AgentLockReceipt = json.loads(lock_receipt.read_text())
    slots = editor_slots(config)
    editor = next((slot for slot in slots if slot["lock_key"] == receipt["key"]), None)

    if editor is not None:
        return [editor], False

    held = [slot for slot in slots if member_receipt(lock_receipt, slot).is_file()]

    return held, len(held) == len(slots)


def editor_launch_refusal(project: str | None, held: Sequence[EditorSlot], whole_vm: bool, pool_size: int,
                          running: int) -> str | None:
    """Return why a lease may not launch another editor, or None when it may."""

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
