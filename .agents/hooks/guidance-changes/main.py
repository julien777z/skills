#!/usr/bin/env python3
import hashlib
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Final

logger = logging.getLogger(__name__)

STATE_DIRECTORY: Final[Path] = (
    Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local" / "state") / "agent-guidance" / "sessions"
)

PROMPT_PATH: Final[Path] = Path(__file__).resolve().parent / "prompts" / "guidance-changed.md"
GUIDANCE_ROOT: Final[str] = ".agents"
GENERATED_ROOT: Final[str] = ".agents/.auto_generated"
SESSION_START_EVENTS: Final[frozenset[str]] = frozenset({"SessionStart", "sessionStart"})
SILENT_PROMPT_EVENT: Final[str] = "beforeSubmitPrompt"
SESSION_KEYS: Final[tuple[str, ...]] = ("session_id", "conversation_id")
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


def session_state_path(session: str) -> Path:
    """Return the file holding the installed commit a session last saw."""

    return STATE_DIRECTORY / hashlib.sha256(session.encode()).hexdigest()


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

        if len(parts) >= 4 and parts[1] == "skills":
            kinds["skills"].add(parts[3] if len(parts) > 4 else parts[2])
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
        payload: object = json.load(sys.stdin)

        if not isinstance(payload, dict):
            return 0

        session = next((str(payload[key]) for key in SESSION_KEYS if payload.get(key)), None)
        installed = git_output(["rev-parse", "HEAD"])

        if session is None or installed is None:
            return 0

        state = session_state_path(session)
        seen = state.read_text(encoding="utf-8").strip() if state.is_file() else None

        event = payload.get("hook_event_name")

        if seen == installed or (seen is not None and event in SESSION_START_EVENTS | {SILENT_PROMPT_EVENT}):
            return 0

        changes = changed_guidance(seen, installed) if seen is not None else {}

        if changes != {}:
            sys.stdout.write(change_notice(changes))

        STATE_DIRECTORY.mkdir(parents=True, exist_ok=True)
        state.write_text(installed, encoding="utf-8")
    except Exception:
        logger.exception("The guidance-change check could not run")

    return 0


if __name__ == "__main__":
    sys.exit(main())
