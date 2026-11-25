#!/usr/bin/env python3
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Final

logger = logging.getLogger(__name__)

# The harness truncates session-start hook context past this many characters.
MAX_CONTEXT_CHARACTERS: Final[int] = 10_000
SKILLS_DIRECTORY_NAME: Final[str] = "skills"
SKILL_ENTRY_FILENAME: Final[str] = "SKILL.md"
SKILL_NAME_PATTERN: Final[re.Pattern[str]] = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
FRONTMATTER_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"\A---[^\S\r\n]*\r?\n.*?\r?\n---[^\S\r\n]*(?:\r?\n|\Z)", re.DOTALL
)
CONTEXT_JSON_EVENT_NAME: Final[str] = "sessionStart"
PROMPTS_DIRECTORY_NAME: Final[str] = "prompts"
LOADED_SKILL_PROMPT_FILENAME: Final[str] = "skill-loaded.md"
SKILL_TO_READ_PROMPT_FILENAME: Final[str] = "skill-to-read.md"


def hook_directory() -> Path:
    """Return this hook's folder as it is linked, without following the link."""

    return Path(os.path.abspath(__file__)).parent


def installed_skill_path(name: str) -> Path:
    """Return a skill's entry file in this hook's user-level root, flat or in a category folder."""

    skills = hook_directory().parent.parent / SKILLS_DIRECTORY_NAME
    flat = skills / name / SKILL_ENTRY_FILENAME

    if flat.is_file():
        return flat

    return min(skills.glob(f"*/{name}/{SKILL_ENTRY_FILENAME}"), default=flat)


def session_context(name: str) -> str | None:
    """Return the text that loads an installed skill, or None when the skill is not installed."""

    path = installed_skill_path(name)
    prompts = hook_directory() / PROMPTS_DIRECTORY_NAME
    loaded_prompt = prompts / LOADED_SKILL_PROMPT_FILENAME
    skill_to_read_prompt = prompts / SKILL_TO_READ_PROMPT_FILENAME

    if not path.is_file():
        return None

    body = FRONTMATTER_PATTERN.sub("", path.read_text(encoding="utf-8"), count=1).strip()
    context = loaded_prompt.read_text(encoding="utf-8").format(name=name, body=body)

    if len(context) > MAX_CONTEXT_CHARACTERS:
        return skill_to_read_prompt.read_text(encoding="utf-8").format(name=name, path=path)

    return context


def expects_context_json() -> bool:
    """Tell whether the harness reads the session context from a JSON object."""

    if sys.stdin.isatty():
        return False

    try:
        payload: object = json.load(sys.stdin)
    except (OSError, ValueError):
        return False

    return isinstance(payload, dict) and payload.get("hook_event_name") == CONTEXT_JSON_EVENT_NAME


def main() -> int:
    """Start the session with the named skill loaded, never holding the session up."""

    try:
        names = sys.argv[1:]

        if len(names) != 1 or SKILL_NAME_PATTERN.fullmatch(names[0]) is None:
            logger.error("Expected one skill name, got %s", names)

            return 0

        context = session_context(names[0])

        if context is None:
            return 0

        if expects_context_json():
            context = json.dumps({"additional_context": context})

        sys.stdout.write(context)
    except Exception:
        logger.exception("The session-start skill could not be loaded")

    return 0


if __name__ == "__main__":
    sys.exit(main())
