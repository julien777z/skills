from json import JSONDecodeError, dumps, load, loads
from logging import getLogger
from os import environ, getpid
from pathlib import Path
from subprocess import CalledProcessError, TimeoutExpired, run
from sys import argv, executable, stderr, stdin
from tempfile import TemporaryDirectory

from models import (
    CursorStartupResult, HookEventName, Provider, RefreshOutcome,
    StartupContext, StartupEvent, StartupResult, StartupSource,
)
from state import fetch_updates, overlay_changed


logger = getLogger(__name__)


def repair(source: Path, outcome: Path, fetch: bool = False) -> None:
    """Check and repair the locked installation."""

    run([
        executable, str(source / ".agents/skills/workspace/agent-lock/resources/main.py"),
        "check", "--receipt", environ["AGENT_LOCK_RECEIPT"],
    ], check=True, text=True)

    installer = ["bash", str(source / ".agents/hooks/skills-refresh/install.sh"), "--local-only"]
    selection = run([
        *installer, "--resolve-source",
    ], capture_output=True, text=True, timeout=20)

    if selection.returncode != 0:
        raise RuntimeError(f"Shared skills source selection failed:\n{selection.stdout}{selection.stderr}")

    selected_source = Path(selection.stdout.strip())

    fetch_failed = False
    updated = False

    if fetch:
        try:
            remote_outcome = fetch_updates(selected_source)
        except (CalledProcessError, TimeoutExpired, OSError, ValueError):
            logger.exception("Remote skills refresh failed; retaining installed guidance")
            fetch_failed = True
        else:
            if remote_outcome == RefreshOutcome.RECONCILE:
                outcome.write_text(RefreshOutcome.RECONCILE)

                return

            updated = remote_outcome == RefreshOutcome.REPAIRED

    if overlay_changed(selected_source):
        outcome.write_text(RefreshOutcome.FAILED if fetch_failed else RefreshOutcome.RECONCILE)

        return

    command = [*installer, "--source", str(selected_source)]
    check = run([*command, "--check"], capture_output=True, text=True, timeout=20)

    if check.returncode == 0:
        outcome.write_text(
            RefreshOutcome.FAILED if fetch_failed
            else RefreshOutcome.REPAIRED if updated
            else RefreshOutcome.CURRENT
        )

        return

    if check.returncode != 3:
        raise RuntimeError(f"Shared skills check failed:\n{check.stdout}{check.stderr}")

    installed = run(command, capture_output=True, text=True, timeout=30)

    if installed.returncode != 0:
        raise RuntimeError(f"Shared skills repair failed:\n{installed.stdout}{installed.stderr}")

    verified = run([*command, "--check"], capture_output=True, text=True, timeout=20)

    if verified.returncode != 0:
        raise RuntimeError(f"Installed skills verification failed:\n{verified.stdout}{verified.stderr}")

    outcome.write_text(RefreshOutcome.FAILED if fetch_failed else RefreshOutcome.REPAIRED)


def refresh(source: Path, fetch: bool = False) -> RefreshOutcome:
    """Run the installation check under shared ownership."""

    lock = source / ".agents/skills/workspace/agent-lock/resources/main.py"

    with TemporaryDirectory(prefix="skills-startup-") as temporary:
        outcome = Path(temporary) / "outcome"
        result = run([
            executable, str(lock), "consume", "skills-install",
            "--owner", f"skills-startup/{getpid()}",
            "--activity", "Check and repair installed shared skills",
            "--receipt", str(Path(temporary) / "lock.json"),
            "--wait-seconds", "5", "--ttl-seconds", "150", "--",
            executable, str(Path(__file__).resolve()), "--repair", str(source), str(outcome),
            *(["--fetch"] if fetch else []),
        ], capture_output=True, text=True, timeout=160)

        if result.stderr:
            print(result.stderr, file=stderr, end="")

        if result.returncode == 2:
            try:
                lock_result = loads(result.stdout)
            except JSONDecodeError:
                lock_result = None

            if isinstance(lock_result, dict) and lock_result.get("status") == RefreshOutcome.BUSY:
                return RefreshOutcome.BUSY

        if result.returncode != 0:
            raise RuntimeError(f"Shared skills startup did not finish:\n{result.stdout}{result.stderr}")

        return RefreshOutcome(outcome.read_text())


def session_start(provider: Provider, fetch: bool = False) -> None:
    """Handle a supported provider startup event."""

    event: StartupEvent = load(stdin)
    cursor = provider == Provider.CURSOR and event.get("hook_event_name") == HookEventName.SESSION_START_CAMEL

    if not cursor and (
        event.get("hook_event_name") != HookEventName.SESSION_START
        or event.get("source") not in (StartupSource.STARTUP, StartupSource.RESUME)
    ):
        return

    source = Path(__file__).resolve().parents[3]
    prompts = Path(__file__).resolve().parent / "prompts"
    outcome = refresh(source, fetch)

    if outcome == RefreshOutcome.CURRENT:
        return

    if outcome in (RefreshOutcome.RECONCILE, RefreshOutcome.BUSY, RefreshOutcome.FAILED):
        prompt = f"{outcome.value}.md"
        context = (prompts / prompt).read_text().strip()
    else:
        context = (prompts / "repaired.md").read_text().strip()

    if cursor:
        print(dumps(CursorStartupResult(additional_context=context)))

        return

    output = StartupContext(
        hookEventName=HookEventName.SESSION_START,
        additionalContext=context,
    )

    if outcome == RefreshOutcome.REPAIRED and provider == Provider.CLAUDE:
        output["reloadSkills"] = True
    elif outcome == RefreshOutcome.REPAIRED and provider == Provider.CODEX:
        discovery = (prompts / "codex-discovery.md").read_text().strip()
        output["additionalContext"] += f" {discovery}"

    print(dumps(StartupResult(hookSpecificOutput=output)))


if __name__ == "__main__":
    if argv[1:2] == ["--repair"]:
        repair(Path(argv[2]), Path(argv[3]), argv[4:] == ["--fetch"])
    elif argv[1:] == ["--update"]:
        result = refresh(Path(__file__).resolve().parents[3], fetch=True)

        print(result.value)

        if result in (RefreshOutcome.RECONCILE, RefreshOutcome.BUSY, RefreshOutcome.FAILED):
            print((Path(__file__).resolve().parent / "prompts" / f"{result.value}.md").read_text().strip())

        raise SystemExit(0 if result in (RefreshOutcome.CURRENT, RefreshOutcome.REPAIRED) else 1)
    elif argv[1:2] in ([Provider.CODEX], [Provider.CLAUDE], [Provider.CURSOR]) and argv[2:] in ([], ["--fetch"]):
        session_start(Provider(argv[1]), argv[2:] == ["--fetch"])
    else:
        raise ValueError("Expected codex|claude|cursor [--fetch], --update, or --repair source outcome [--fetch]")
