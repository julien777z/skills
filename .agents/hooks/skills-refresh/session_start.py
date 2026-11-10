from json import JSONDecodeError, dumps, load, loads
from logging import Logger, getLogger
from os import environ, getpid
from pathlib import Path
from subprocess import CalledProcessError, TimeoutExpired, run
from sys import argv, executable, stderr, stdin
from tempfile import TemporaryDirectory

from models import (
    CursorStartupResult, HookEventName, Provider, RefreshOutcome,
    StartupContext, StartupEvent, StartupResult, StartupSource,
)
from state import fetch_updates, overlay_changed, repair_commit_graph


logger: Logger = getLogger(__name__)


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

    remote_outcome = RefreshOutcome.CURRENT

    try:
        graph_repaired = repair_commit_graph(selected_source)

        if fetch:
            try:
                remote_outcome = fetch_updates(selected_source)
            except (CalledProcessError, TimeoutExpired, OSError, ValueError):
                logger.exception("Remote skills refresh failed")
                remote_outcome = RefreshOutcome.FAILED

        needs_reconciliation = remote_outcome == RefreshOutcome.RECONCILE or overlay_changed(selected_source)
    except (CalledProcessError, TimeoutExpired, OSError, ValueError):
        logger.exception("Skills checkout refresh failed; retaining installed guidance")
        outcome.write_text(RefreshOutcome.FAILED)

        return

    if needs_reconciliation:
        outcome.write_text(
            RefreshOutcome.FAILED if remote_outcome == RefreshOutcome.FAILED else RefreshOutcome.RECONCILE
        )

        return

    command = [*installer, "--source", str(selected_source)]
    check = run([*command, "--check"], capture_output=True, text=True, timeout=20)

    if check.returncode == 0:
        updated = graph_repaired or remote_outcome == RefreshOutcome.REPAIRED
        outcome.write_text(
            RefreshOutcome.FAILED if remote_outcome == RefreshOutcome.FAILED
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

    outcome.write_text(RefreshOutcome.FAILED if remote_outcome == RefreshOutcome.FAILED else RefreshOutcome.REPAIRED)


def refresh(source: Path, fetch: bool = False) -> RefreshOutcome:
    """Run the installation check under shared ownership."""

    lock = source / ".agents/skills/workspace/agent-lock/resources/main.py"

    with TemporaryDirectory(prefix="skills-startup-") as temporary:
        outcome = Path(temporary) / "outcome"

        try:
            result = run([
                executable, str(lock), "consume", "skills-install",
                "--owner", f"skills-startup/{getpid()}",
                "--activity", "Check and repair installed shared skills",
                "--receipt", str(Path(temporary) / "lock.json"),
                "--wait-seconds", "5", "--ttl-seconds", "150", "--",
                executable, str(Path(__file__).resolve()), "--repair", str(source), str(outcome),
                *(["--fetch"] if fetch else []),
            ], capture_output=True, text=True, timeout=160)
        except TimeoutExpired:
            logger.exception("Shared skills startup lock supervisor timed out")

            return RefreshOutcome.FAILED

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
            print(f"Shared skills startup did not finish:\n{result.stdout}", file=stderr)

            return RefreshOutcome.FAILED

        return RefreshOutcome(outcome.read_text())


def read_prompts() -> dict[str, str]:
    """Read the named sections of the shared prompt file."""

    document = Path(__file__).with_name("prompts.md").read_text()
    prompts: dict[str, str] = {}

    for section in document.split("\n## ")[1:]:
        name, _, body = section.partition("\n")
        prompts[name] = body.strip()

    return prompts


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
    outcome = refresh(source, fetch)

    if outcome == RefreshOutcome.CURRENT:
        return

    prompts = read_prompts()
    context = prompts[outcome.value]

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
        discovery = prompts["codex-discovery"]
        output["additionalContext"] += f" {discovery}"

    print(dumps(StartupResult(hookSpecificOutput=output)))


if __name__ == "__main__":
    if argv[1:2] == ["--repair"]:
        repair(Path(argv[2]), Path(argv[3]), argv[4:] == ["--fetch"])
    elif argv[1:] == ["--update"]:
        result = refresh(Path(__file__).resolve().parents[3], fetch=True)

        print(result.value)

        if result in (RefreshOutcome.RECONCILE, RefreshOutcome.BUSY, RefreshOutcome.FAILED):
            print(read_prompts()[result.value])

        raise SystemExit(0 if result in (RefreshOutcome.CURRENT, RefreshOutcome.REPAIRED) else 1)
    elif argv[1:2] in ([Provider.CODEX], [Provider.CLAUDE], [Provider.CURSOR]) and argv[2:] in ([], ["--fetch"]):
        session_start(Provider(argv[1]), argv[2:] == ["--fetch"])
    else:
        raise ValueError("Expected codex|claude|cursor [--fetch], --update, or --repair source outcome [--fetch]")
