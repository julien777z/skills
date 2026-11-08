from enum import StrEnum
from typing import NotRequired, TypedDict


class SourceCommand(StrEnum):
    """An operation the script runs with the pinned sync tool."""

    CHECK = "check"
    MIRROR = "mirror"


class SyncOutcome(StrEnum):
    """What one run of the sync tool concluded."""

    VALID = "valid"
    INVALID = "invalid"
    UNAVAILABLE = "unavailable"


class ActionReference(TypedDict):
    """The sync action a workflow pins."""

    repository: str
    reference: str


class ExternalResource(TypedDict):
    """One entry of the external resources file the sync tool refreshes."""

    kind: str
    name: str
    skill_name_override: NotRequired[str]
    update_on_sync: bool
