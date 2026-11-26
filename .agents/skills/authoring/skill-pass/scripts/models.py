from enum import StrEnum
from typing import NotRequired, TypedDict


class SourceCommand(StrEnum):
    """An operation the script runs over the canonical agent sources."""

    CHECK = "check"
    MIRROR = "mirror"
    READERS = "readers"
    WORDING = "wording"


class SyncOutcome(StrEnum):
    """What one run of the sync tool concluded."""

    VALID = "valid"
    INVALID = "invalid"
    UNAVAILABLE = "unavailable"


class ScenarioKind(StrEnum):
    """The path a regression scenario holds in place."""

    HAPPY = "happy"
    EDGE = "edge"
    NEGATIVE = "negative"


class ScenarioRoute(StrEnum):
    """The route a change to a regression scenario takes."""

    BEHAVIOR_CHANGE = "behavior-change"
    TEST_CAUSE = "test-cause"


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
