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


class IconName(StrEnum):
    """Icons the navbar shows for a dashboard and for each of its pages."""

    OVERVIEW = "overview"
    PROGRESS = "progress"
    BOARD = "board"
    CHECKLIST = "checklist"
    LIST = "list"
    CHART = "chart"
    ACTIVITY = "activity"
    DIAGRAM = "diagram"
    DOCUMENT = "document"
    GUIDE = "guide"
    LEGAL = "legal"
    SHIELD = "shield"
    PEOPLE = "people"
    DATA = "data"
    PACKAGE = "package"
    RELEASE = "release"
    PULL_REQUEST = "pull-request"
    SETTINGS = "settings"
    ALERT = "alert"
    CHECK = "check"
    CALENDAR = "calendar"


class SourceKind(StrEnum):
    """What a source link opens, shown at the start of its pill."""

    DOC = "doc"
    CODE = "code"
    DIFF = "diff"
    SPEC = "spec"
    PULL_REQUEST = "pull-request"
    CONFIG = "config"
    TEST = "test"
    PAGE = "page"
    DATA = "data"


class Change(StrEnum):
    """What a pull request does to one part of the system."""

    ADDED = "added"
    CHANGED = "changed"
    REMOVED = "removed"


class Field(TypedDict):
    """One spec field: how it is checked and the TypeScript type it declares."""

    check: Callable[[object, str], object]
    typescript: str
    shape: NotRequired["ObjectShape"]
    choices: NotRequired[type[StrEnum]]


class ObjectShape(TypedDict):
    """Validation rules for one spec object."""

    name: str
    fields: dict[str, Field]
    required: frozenset[str]
    relations: NotRequired[Callable[[dict[str, object], str], None]]
