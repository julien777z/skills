from collections.abc import Callable
from enum import StrEnum
from typing import NotRequired, TypedDict


class Tone(StrEnum):
    """Colors a status, pill, column or progress segment."""

    GOOD = "good"
    WARNING = "warning"
    CRITICAL = "critical"
    ACCENT = "accent"
    DONE = "done"


class PullRequestState(StrEnum):
    """States of the pull request a `links` item stands for."""

    OPEN = "open"
    DRAFT = "draft"
    MERGED = "merged"
    CLOSED = "closed"


class QuestionStatus(StrEnum):
    """States of one question in a `questions` section."""

    OPEN = "open"
    ANSWERED = "answered"


class SectionType(StrEnum):
    """Kinds of section a dashboard renders."""

    BOARD = "board"
    QUESTIONS = "questions"
    LINKS = "links"
    TABLE = "table"
    NOTES = "notes"
    DIAGRAM = "diagram"
    OUTLINE = "outline"
    CHANGES = "changes"
    CALLOUT = "callout"


class PageLayout(StrEnum):
    """How a dashboard page arranges its sections."""

    COLUMNS = "columns"
    ROWS = "rows"


class PageIcon(StrEnum):
    """Icons a dashboard page shows beside its name in the sidebar."""

    OVERVIEW = "overview"
    LIST = "list"
    CHART = "chart"
    DIAGRAM = "diagram"
    DOCUMENT = "document"
    SHIELD = "shield"
    PEOPLE = "people"
    DATA = "data"
    SETTINGS = "settings"
    ALERT = "alert"
    CHECK = "check"
    CALENDAR = "calendar"


class Change(StrEnum):
    """What a pull request does to one part of the system."""

    ADDED = "added"
    CHANGED = "changed"
    REMOVED = "removed"


class ObjectShape(TypedDict):
    """Validation rules for one spec object."""

    name: str
    fields: dict[str, Callable[[object, str], object]]
    required: frozenset[str]
    relations: NotRequired[Callable[[dict[str, object], str], None]]
