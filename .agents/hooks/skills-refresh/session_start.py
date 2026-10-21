"""Adapt the shared installation checker to a provider's SessionStart event."""

from json import dumps, load
from os import environ, getpid
from pathlib import Path
from subprocess import run
from sys import argv, executable, stdin
from tempfile import TemporaryDirectory

from models import StartupContext, StartupResult
from state import overlay_changed


def repair(source: Path, outcome: Path) -> None:
    run([
        executable, str(source / ".agents/skills/workspace/agent-lock/resources/main.py"),
        "check", "--receipt", environ["AGENT_LOCK_RECEIPT"],
    ], check=True, text=True)

    if overlay_changed(source):
        outcome.write_text("reconcile")

        return

    command = ["bash", str(source / "bootstrap/install.sh"), "--local-only"]
    check = run([*command, "--check"], capture_output=True, text=True, timeout=20)

    if check.returncode == 0:
        outcome.write_text("current")

        return

    if check.returncode != 3:
        raise RuntimeError(f"Shared skills check failed:\n{check.stdout}{check.stderr}")

    installed = run(command, capture_output=True, text=True, timeout=30)

    if installed.returncode != 0:
        raise RuntimeError(f"Shared skills repair failed:\n{installed.stdout}{installed.stderr}")

    verified = run([*command, "--check"], capture_output=True, text=True, timeout=20)

    if verified.returncode != 0:
        raise RuntimeError(f"Installed skills verification failed:\n{verified.stdout}{verified.stderr}")

    outcome.write_text("repaired")


def refresh(source: Path) -> str:
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

        return outcome.read_text()


def session_start(provider: str) -> None:
    event = load(stdin)

    if event.get("hook_event_name") != "SessionStart" or event.get("source") not in ("startup", "resume"):
        return

    source = Path(__file__).resolve().parents[3]
    outcome = refresh(source)

    if outcome == "current":
        return

    if outcome == "reconcile":
        print(dumps(StartupResult(hookSpecificOutput=StartupContext(
            hookEventName="SessionStart",
            additionalContext="Shared skills overlay inputs changed or the installed source is an unmarked worktree. Run reconcile-skills before ordinary work; preserve pending changes.",
        ))))

        return

    if outcome != "repaired":
        raise ValueError(f"Unexpected skills refresh outcome: {outcome}")

    output = StartupContext(
        hookEventName="SessionStart",
        additionalContext="Installed shared skill and rule links were repaired and verified. Read changed guidance before using it.",
    )

    if provider == "claude":
        output["reloadSkills"] = True
    else:
        output["additionalContext"] += " Codex discovers skills before SessionStart; newly installed skills appear in the next session. Do not claim the current catalogue was reloaded."

    print(dumps(StartupResult(hookSpecificOutput=output)))


if __name__ == "__main__":
    if argv[1:2] == ["--repair"]:
        repair(Path(argv[2]), Path(argv[3]))
    elif argv[1:] in (["codex"], ["claude"]):
        session_start(argv[1])
    else:
        raise ValueError("Expected the codex or claude adapter, or --repair source outcome")
