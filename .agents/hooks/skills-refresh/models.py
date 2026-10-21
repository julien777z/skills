"""The SessionStart output shared by the provider adapters."""

from typing import NotRequired, TypedDict


class StartupContext(TypedDict):
    hookEventName: str
    additionalContext: str
    reloadSkills: NotRequired[bool]


class StartupResult(TypedDict):
    hookSpecificOutput: StartupContext
