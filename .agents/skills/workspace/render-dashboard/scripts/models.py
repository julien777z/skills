from collections.abc import Callable
from enum import StrEnum
from typing import NotRequired, TypedDict


class Tone(StrEnum):
    """Colors a status, pill, column or progress segment."""

    GOOD = "good"
    WARNING = "warning"
    CRITICAL = "critical"
    ACCENT = "accent"


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


class PageLayout(StrEnum):
    """How a dashboard page arranges its sections."""

    COLUMNS = "columns"
    ROWS = "rows"


class Change(StrEnum):
    """What a pull request does to one part of the system."""

    ADDED = "added"
    CHANGED = "changed"
    REMOVED = "removed"


class ObjectShape(TypedDict):
    """Validation rules for one spec object."""

    fields: dict[str, Callable[[object, str], object]]
    required: frozenset[str]
    relations: NotRequired[Callable[[dict[str, object], str], None]]
