from json import dumps, load
from os import environ, getpid
from pathlib import Path
from subprocess import run
from sys import argv, executable, stdin
from tempfile import TemporaryDirectory

from models import RefreshOutcome, StartupContext, StartupResult
from state import overlay_changed


def repair(source: Path, outcome: Path) -> None:
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

    if overlay_changed(selected_source):
        outcome.write_text(RefreshOutcome.RECONCILE)

        return

    command = [*installer, "--source", str(selected_source)]
    check = run([*command, "--check"], capture_output=True, text=True, timeout=20)

    if check.returncode == 0:
        outcome.write_text(RefreshOutcome.CURRENT)

        return

    if check.returncode != 3:
        raise RuntimeError(f"Shared skills check failed:\n{check.stdout}{check.stderr}")

    installed = run(command, capture_output=True, text=True, timeout=30)

    if installed.returncode != 0:
        raise RuntimeError(f"Shared skills repair failed:\n{installed.stdout}{installed.stderr}")

    verified = run([*command, "--check"], capture_output=True, text=True, timeout=20)

    if verified.returncode != 0:
        raise RuntimeError(f"Installed skills verification failed:\n{verified.stdout}{verified.stderr}")

    outcome.write_text(RefreshOutcome.REPAIRED)


def refresh(source: Path) -> RefreshOutcome:
    """Run the installation check under shared ownership."""

    lock = source / ".agents/skills/workspace/agent-lock/resources/main.py"

    with TemporaryDirectory(prefix="skills-startup-") as temporary:
        outcome = Path(temporary) / "outcome"
        result = run([
            executable, str(lock), "consume", "skills-install",
            "--owner", f"skills-startup/{getpid()}",
            "--activity", "Check and repair installed shared skills",
            "--receipt", str(Path(temporary) / "lock.json"),
            "--wait-seconds", "5", "--ttl-seconds", "90", "--",
            executable, str(Path(__file__).resolve()), "--repair", str(source), str(outcome),
        ], capture_output=True, text=True, timeout=100)

        if result.returncode != 0:
            raise RuntimeError(f"Shared skills startup did not finish:\n{result.stdout}{result.stderr}")

        return RefreshOutcome(outcome.read_text())


def session_start(provider: str) -> None:
    """Handle a supported provider startup event."""

    event = load(stdin)

    if event.get("hook_event_name") != "SessionStart" or event.get("source") not in ("startup", "resume"):
        return

    source = Path(__file__).resolve().parents[3]
    prompts = Path(__file__).resolve().parent / "prompts"
    outcome = refresh(source)

    if outcome == RefreshOutcome.CURRENT:
        return

    if outcome == RefreshOutcome.RECONCILE:
        print(dumps(StartupResult(hookSpecificOutput=StartupContext(
            hookEventName="SessionStart",
            additionalContext=(prompts / "reconcile.md").read_text().strip(),
        ))))

        return

    output = StartupContext(
        hookEventName="SessionStart",
        additionalContext=(prompts / "repaired.md").read_text().strip(),
    )

    if provider == "claude":
        output["reloadSkills"] = True
    else:
        discovery = (prompts / "codex-discovery.md").read_text().strip()
        output["additionalContext"] += f" {discovery}"

    print(dumps(StartupResult(hookSpecificOutput=output)))


if __name__ == "__main__":
    if argv[1:2] == ["--repair"]:
        repair(Path(argv[2]), Path(argv[3]))
    elif argv[1:] in (["codex"], ["claude"]):
        session_start(argv[1])
    else:
        raise ValueError("Expected the codex or claude adapter, or --repair source outcome")
