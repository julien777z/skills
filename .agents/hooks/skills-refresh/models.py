from enum import StrEnum
from typing import NotRequired, TypedDict


class InstallationMode(StrEnum):
    """Name the configuration command modes."""

    APPLY = "apply"
    CHECK = "check"
    PREFLIGHT = "preflight"


class StartupContext(TypedDict):
    """Provider startup context."""

    hookEventName: str
    additionalContext: str
    reloadSkills: NotRequired[bool]


class StartupResult(TypedDict):
    """Provider startup response."""

    hookSpecificOutput: StartupContext


class RefreshOutcome(StrEnum):
    """Local installation check outcome."""

    CURRENT = "current"
    RECONCILE = "reconcile"
    REPAIRED = "repaired"
