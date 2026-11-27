#!/usr/bin/env python3
import hashlib
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Final

from models import HookInput, SessionState

logger = logging.getLogger(__name__)

STATE_DIRECTORY: Final[Path] = (
    Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local" / "state") / "agent-guidance" / "sessions"
)

PROMPT_PATH: Final[Path] = Path(__file__).resolve().parent / "prompts" / "guidance-changed.md"
GUIDANCE_ROOT: Final[str] = ".agents"
GENERATED_ROOT: Final[str] = ".agents/.auto_generated"
SESSION_START_EVENTS: Final[frozenset[str]] = frozenset({"SessionStart", "sessionStart"})
SESSION_END_EVENTS: Final[frozenset[str]] = frozenset({"SessionEnd", "sessionEnd"})
SILENT_PROMPT_EVENT: Final[str] = "beforeSubmitPrompt"
MAX_NAMES_PER_KIND: Final[int] = 12
GIT_TIMEOUT_SECONDS: Final[int] = 5


def git_output(arguments: list[str]) -> str | None:
    """Return a Git command's trimmed output in the installed source, or None when it fails."""

    source = Path(__file__).resolve().parent

    try:
        completed = subprocess.run(
            ["git", "-C", str(source), *arguments],
            capture_output=True,
            text=True,
            timeout=GIT_TIMEOUT_SECONDS,
            check=True,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    return completed.stdout.strip()


def text_field(payload: dict[object, object], key: str) -> str | None:
    """Return a payload field that holds non-empty text, or None."""

    value = payload.get(key)

    return value if isinstance(value, str) and value else None


def read_hook_input() -> HookInput | None:
    """Read the payload the harness writes to standard input, or None when it is not an object."""

    payload: object = json.load(sys.stdin)

    if not isinstance(payload, dict):
        return None

    return HookInput(
        session=text_field(payload, "session_id") or text_field(payload, "conversation_id"),
        event=text_field(payload, "hook_event_name"),
        transcript_path=text_field(payload, "transcript_path"),
    )


def session_state_path(session: str) -> Path:
    """Return the file holding the installed commit a session last saw."""

    return STATE_DIRECTORY / hashlib.sha256(session.encode()).hexdigest()


def read_state(path: Path) -> SessionState | None:
    """Return a session's saved state, or None when it has none or the record is unreadable."""

    try:
        record: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None

    if not isinstance(record, dict) or not isinstance(record.get("commit"), str):
        return None

    transcript_path = record.get("transcript_path")

    return SessionState(
        commit=record["commit"],
        transcript_path=transcript_path if isinstance(transcript_path, str) else None,
    )


def prune_ended_sessions() -> None:
    """Remove each saved state whose session transcript the harness has since deleted."""

    if not STATE_DIRECTORY.is_dir():
        return

    for path in STATE_DIRECTORY.iterdir():
        state = read_state(path)

        if state is not None and state["transcript_path"] and not Path(state["transcript_path"]).exists():
            path.unlink(missing_ok=True)


def changed_guidance(seen: str, installed: str) -> dict[str, list[str]] | None:
    """Return the skills, rules and other guidance that differ between two installs."""

    listing = git_output(
        [
            "diff",
            "--name-only",
            "--end-of-options",
            seen,
            installed,
            "--",
            f":(top){GUIDANCE_ROOT}",
            f":(top,exclude){GENERATED_ROOT}",
        ]
    )

    if listing is None:
        return None

    kinds: dict[str, set[str]] = {"skills": set(), "rules": set(), "other guidance": set()}

    for path in listing.splitlines():
        parts = Path(path).parts

        if len(parts) >= 5 and parts[1] == "skills":
            kinds["skills"].add(parts[3])
        elif len(parts) >= 3 and parts[1] == "rules":
            kinds["rules"].add(Path(parts[2]).stem)
        elif path == f"{GUIDANCE_ROOT}/global.md":
            kinds["rules"].add("global rules")
        else:
            kinds["other guidance"].add("/".join(parts[1:3]))

    return {kind: sorted(names) for kind, names in kinds.items() if names}


def change_notice(changes: dict[str, list[str]] | None) -> str:
    """Return the note that tells a running session its installed guidance changed."""

    if changes is None:
        listing = "the changed files could not be listed, so re-read each skill and rule you rely on"
    else:
        listing = "; ".join(
            f"{kind}: {', '.join(names[:MAX_NAMES_PER_KIND])}"
            + (f" and {len(names) - MAX_NAMES_PER_KIND} more" if len(names) > MAX_NAMES_PER_KIND else "")
            for kind, names in changes.items()
        )

    return PROMPT_PATH.read_text(encoding="utf-8").format(changes=listing)


def main() -> int:
    """Record the install a session starts on, and note any later install on its next prompt."""

    try:
        hook_input = read_hook_input()

        if hook_input is None or hook_input["session"] is None:
            return 0

        state_path = session_state_path(hook_input["session"])
        saved = read_state(state_path)
        event = hook_input["event"]

        if event in SESSION_END_EVENTS:
            if saved is not None and saved["transcript_path"] is None:
                state_path.unlink(missing_ok=True)

            return 0

        if event in SESSION_START_EVENTS:
            prune_ended_sessions()

        installed = git_output(["rev-parse", "HEAD"])
        seen = saved["commit"] if saved is not None else None

        if installed is None or seen == installed:
            return 0

        if seen is not None and event in SESSION_START_EVENTS | {SILENT_PROMPT_EVENT}:
            return 0

        changes = changed_guidance(seen, installed) if seen is not None else {}

        if changes != {}:
            sys.stdout.write(change_notice(changes))

        written = hook_input["transcript_path"]
        transcript_path = (
            written if written and Path(written).exists() else (saved["transcript_path"] if saved else None)
        )

        STATE_DIRECTORY.mkdir(parents=True, exist_ok=True)
        state_path.write_text(
            json.dumps(SessionState(commit=installed, transcript_path=transcript_path)),
            encoding="utf-8",
        )
    except Exception:
        logger.exception("The guidance-change check could not run")

    return 0


if __name__ == "__main__":
    sys.exit(main())
