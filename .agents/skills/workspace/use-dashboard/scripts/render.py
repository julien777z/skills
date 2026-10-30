import fcntl
import logging
import os
import shutil
import subprocess
from argparse import ArgumentParser
from collections.abc import Callable
from datetime import datetime
from enum import StrEnum
from functools import partial
from hashlib import sha256
from html import escape
from html.parser import HTMLParser
from json import JSONDecodeError, dumps, loads
from pathlib import Path
from typing import Final, cast

from models import (
    Change,
    ObjectShape,
    PageIcon,
    PageLayout,
    PullRequestState,
    QuestionStatus,
    SectionType,
    Tone,
)

logger = logging.getLogger(__name__)

APP_ROOT: Final[Path] = Path(__file__).resolve().parent.parent / "app"
APP_BUILD_OUTPUTS: Final[frozenset[str]] = frozenset({"node_modules", "dist"})
APP_LOCKFILE: Final[str] = "package-lock.json"
CACHE_ROOT: Final[Path] = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / "use-dashboard"
DATA_PLACEHOLDER: Final[str] = "__DASHBOARD_DATA__"
TITLE_PLACEHOLDER: Final[str] = "__DASHBOARD_TITLE__"
PAGE_TITLE_TEMPLATE: Final[str] = "Dashboard - {title}"
DOCUMENT_PREAMBLE: Final[str] = (
    '<!doctype html>\n<html lang="en">\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
)


class DashboardSpecError(ValueError):
    """Raised when a dashboard spec does not match the documented shape."""


class DashboardBuildError(RuntimeError):
    """Raised when the dashboard app cannot be built."""


class DocumentParts(HTMLParser):
    """Offsets of a built page's head and body contents."""

    def __init__(self, source: str) -> None:
        super().__init__(convert_charrefs=False)

        self.line_starts = [0]
        self.offsets: dict[str, int] = {}

        for line in source.splitlines(keepends=True):
            self.line_starts.append(self.line_starts[-1] + len(line))

        self.feed(source)
        self.close()

    def position(self, after_tag: bool) -> int:
        """Return the parser's offset, after the tag just read when asked."""

        line, column = self.getpos()
        offset = self.line_starts[line - 1] + column

        return offset + len(self.get_starttag_text() or "") if after_tag else offset

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Record where the head and body contents start."""

        if tag in {"head", "body"} and f"{tag}_start" not in self.offsets:
            self.offsets[f"{tag}_start"] = self.position(after_tag=True)

    def handle_endtag(self, tag: str) -> None:
        """Record where the head and body contents end."""

        if tag in {"head", "body"}:
            self.offsets[f"{tag}_end"] = self.position(after_tag=False)


def check_text(value: object, path: str) -> None:
    """Require a non-empty string."""

    if not isinstance(value, str) or not value.strip():
        raise DashboardSpecError(f"{path} must be a non-empty string")


def check_list(value: object, path: str, allow_empty: bool = False) -> list[object]:
    """Return a JSON array."""

    if not isinstance(value, list):
        raise DashboardSpecError(f"{path} must be a list")

    if not value and not allow_empty:
        raise DashboardSpecError(f"{path} must hold at least one entry")

    return value


def check_texts(value: object, path: str) -> None:
    """Require a list of non-empty strings."""

    for index, entry in enumerate(check_list(value, path)):
        check_text(entry, f"{path}[{index}]")


def check_rows(value: object, path: str) -> None:
    """Require a list of rows, each a list of non-empty strings."""

    for index, row in enumerate(check_list(value, path)):
        check_texts(row, f"{path}[{index}]")


def check_choice[E: StrEnum](value: object, path: str, choices: type[E]) -> E:
    """Require one member of a string enum and return it."""

    if not isinstance(value, str) or value not in {choice.value for choice in choices}:
        raise DashboardSpecError(f"{path} must be one of: {', '.join(choice.value for choice in choices)}")

    return choices(value)


def check_fraction(value: object, path: str) -> None:
    """Require a number from 0 to 1."""

    if isinstance(value, bool) or not isinstance(value, int | float) or not 0 <= value <= 1:
        raise DashboardSpecError(f"{path} must be a number from 0 to 1")


def check_whole_number(value: object, path: str) -> None:
    """Require a positive whole number."""

    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise DashboardSpecError(f"{path} must be a whole number from 1")


def check_timestamp(value: object, path: str) -> None:
    """Require an ISO 8601 timestamp."""

    try:
        datetime.fromisoformat(str(value))
    except ValueError as error:
        raise DashboardSpecError(f"{path} must be an ISO 8601 timestamp") from error


def check_object(value: object, path: str, shape: ObjectShape) -> dict[str, object]:
    """Return a JSON object after validating it."""

    if not isinstance(value, dict):
        raise DashboardSpecError(f"{path} must be an object")

    unknown = sorted(set(value) - set(shape["fields"]))

    if unknown:
        raise DashboardSpecError(f"{path} has unknown fields: {', '.join(unknown)}")

    missing = sorted(shape["required"] - set(value))

    if missing:
        raise DashboardSpecError(f"{path} is missing: {', '.join(missing)}")

    for key, field_value in value.items():
        shape["fields"][key](field_value, f"{path}.{key}")

    if "relations" in shape:
        shape["relations"](value, path)

    return value


def check_objects(value: object, path: str, shape: ObjectShape, allow_empty: bool = False, unique: str | None = None) -> None:
    """Require a list of objects of one shape."""

    entries = [check_object(entry, f"{path}[{index}]", shape) for index, entry in enumerate(check_list(value, path, allow_empty))]

    if unique:
        keys = [entry[unique] for entry in entries]

        if len(set(keys)) != len(keys):
            raise DashboardSpecError(f"{path} must not repeat the same {unique}")


def check_table_rows(table: dict[str, object], path: str) -> None:
    """Require every table row to hold one cell per column."""

    width = len(cast(list[str], table["columns"]))

    for index, row in enumerate(cast(list[list[str]], table["rows"])):
        if len(row) != width:
            raise DashboardSpecError(f"{path}.rows[{index}] must hold {width} cells")


def check_diagram(diagram: dict[str, object], path: str) -> None:
    """Require a diagram's boxes, arrows and pull requests to refer to one another."""

    pull_requests = [entry["ref"] for entry in cast(list[dict[str, object]], diagram.get("prs", []))]
    nodes = cast(list[dict[str, object]], diagram["nodes"])
    edges = cast(list[dict[str, object]], diagram["edges"])
    node_ids = [node["id"] for node in nodes]
    step_count = len(cast(list[str], diagram.get("steps", [])))

    for index, node in enumerate(nodes):
        if "pr" in node and node["pr"] not in pull_requests:
            raise DashboardSpecError(f"{path}.nodes[{index}].pr must name a ref listed in {path}.prs")

    for index, edge in enumerate(edges):
        step = cast(int | None, edge.get("step"))

        for end in ("from", "to"):
            if edge[end] not in node_ids:
                raise DashboardSpecError(f"{path}.edges[{index}].{end} must name a node id")

        if step is not None and step > step_count:
            raise DashboardSpecError(f"{path}.edges[{index}].step must number an entry in {path}.steps")


def check_sections(value: object, path: str) -> None:
    """Require a list of sections."""

    for index, section in enumerate(check_list(value, path)):
        section_path = f"{path}[{index}]"
        raw_type = section.get("type") if isinstance(section, dict) else None
        section_type = check_choice(raw_type, f"{section_path}.type", SectionType)

        check_object(section, section_path, SECTION_SHAPES[section_type])


def section_shape(
    fields: dict[str, Callable[[object, str], object]],
    required: frozenset[str],
    relations: Callable[[dict[str, object], str], None] | None = None,
) -> ObjectShape:
    """Return the shape of a section type."""

    shape = ObjectShape(
        fields={"type": check_text, "title": check_text} | fields,
        required=frozenset({"type", "title"}) | required,
    )

    if relations:
        shape["relations"] = relations

    return shape


def paged_items_section(shape: ObjectShape) -> ObjectShape:
    """Return the shape of a section listing items of one shape, optionally a page at a time."""

    return section_shape({"items": partial(check_objects, shape=shape), "page_size": check_whole_number}, frozenset({"items"}))


CHECK_TONE: Final[Callable[[object, str], object]] = partial(check_choice, choices=Tone)
CHECK_CHANGE: Final[Callable[[object, str], object]] = partial(check_choice, choices=Change)
CHECK_LAYOUT: Final[Callable[[object, str], object]] = partial(check_choice, choices=PageLayout)

LABEL_SHAPE: Final[ObjectShape] = ObjectShape(fields={"label": check_text, "tone": CHECK_TONE}, required=frozenset({"label"}))
SEGMENT_SHAPE: Final[ObjectShape] = ObjectShape(
    fields={"label": check_text, "tone": CHECK_TONE, "weight": check_whole_number},
    required=frozenset({"label"}),
)
CARD_SHAPE: Final[ObjectShape] = ObjectShape(
    fields={"title": check_text, "detail": check_text, "meta": check_text, "tag": check_text, "url": check_text},
    required=frozenset({"title"}),
)
QUESTION_SHAPE: Final[ObjectShape] = ObjectShape(
    fields={
        "question": check_text,
        "status": partial(check_choice, choices=QuestionStatus),
        "context": check_text,
        "options": check_texts,
        "recommendation": check_text,
        "answer": check_text,
        "meta": check_text,
    },
    required=frozenset({"question", "status"}),
)
LINK_SHAPE: Final[ObjectShape] = ObjectShape(
    fields={
        "label": check_text,
        "url": check_text,
        "detail": check_text,
        "status": check_text,
        "tone": CHECK_TONE,
        "state": partial(check_choice, choices=PullRequestState),
    },
    required=frozenset({"label", "url"}),
)
CHANGE_ITEM_SHAPE: Final[ObjectShape] = ObjectShape(
    fields={"name": check_text, "change": CHECK_CHANGE, "detail": check_text},
    required=frozenset({"name", "change"}),
)
PULL_REQUEST_SHAPE: Final[ObjectShape] = ObjectShape(
    fields={"ref": check_text, "url": check_text},
    required=frozenset({"ref", "url"}),
)
NODE_SHAPE: Final[ObjectShape] = ObjectShape(
    fields={"id": check_text, "label": check_text, "detail": check_text, "pr": check_text, "change": CHECK_CHANGE},
    required=frozenset({"id", "label"}),
)
EDGE_SHAPE: Final[ObjectShape] = ObjectShape(
    fields={"from": check_text, "to": check_text, "label": check_text, "step": check_whole_number, "change": CHECK_CHANGE},
    required=frozenset({"from", "to"}),
)
OUTLINE_ITEM_SHAPE: Final[ObjectShape] = ObjectShape(
    fields={"title": check_text, "detail": check_text, "tone": CHECK_TONE, "tag": check_text, "meta": check_text},
    required=frozenset({"title", "detail"}),
)
OUTLINE_GROUP_SHAPE: Final[ObjectShape] = ObjectShape(
    fields={"title": check_text, "items": partial(check_objects, shape=OUTLINE_ITEM_SHAPE)},
    required=frozenset({"title", "items"}),
)
REFERENCE_SHAPE: Final[ObjectShape] = ObjectShape(fields={"text": check_text, "url": check_text}, required=frozenset({"text", "url"}))
COLUMN_SHAPE: Final[ObjectShape] = ObjectShape(
    fields={
        "title": check_text,
        "tone": CHECK_TONE,
        "page_size": check_whole_number,
        "items": partial(check_objects, shape=CARD_SHAPE, allow_empty=True),
    },
    required=frozenset({"title", "items"}),
)
SECTION_SHAPES: Final[dict[SectionType, ObjectShape]] = {
    SectionType.BOARD: section_shape({"columns": partial(check_objects, shape=COLUMN_SHAPE)}, frozenset({"columns"})),
    SectionType.QUESTIONS: paged_items_section(QUESTION_SHAPE),
    SectionType.LINKS: paged_items_section(LINK_SHAPE),
    SectionType.NOTES: section_shape({"items": check_texts}, frozenset({"items"})),
    SectionType.CHANGES: paged_items_section(CHANGE_ITEM_SHAPE),
    SectionType.OUTLINE: section_shape(
        {"groups": partial(check_objects, shape=OUTLINE_GROUP_SHAPE)},
        frozenset({"groups"}),
    ),
    SectionType.CALLOUT: section_shape({"body": check_text, "tone": CHECK_TONE}, frozenset({"body"})),
    SectionType.TABLE: section_shape(
        {"columns": check_texts, "rows": check_rows},
        frozenset({"columns", "rows"}),
        check_table_rows,
    ),
    SectionType.DIAGRAM: section_shape(
        {
            "prs": partial(check_objects, shape=PULL_REQUEST_SHAPE, unique="ref"),
            "nodes": partial(check_objects, shape=NODE_SHAPE, unique="id"),
            "edges": partial(check_objects, shape=EDGE_SHAPE),
            "steps": check_texts,
        },
        frozenset({"nodes", "edges"}),
        check_diagram,
    ),
}
PAGE_SHAPE: Final[ObjectShape] = ObjectShape(
    fields={
        "title": check_text,
        "icon": partial(check_choice, choices=PageIcon),
        "layout": CHECK_LAYOUT,
        "sections": check_sections,
    },
    required=frozenset({"title", "sections"}),
)
DASHBOARD_SHAPE: Final[ObjectShape] = ObjectShape(
    fields={
        "title": check_text,
        "subtitle": check_text,
        "updated_at": check_timestamp,
        "status": partial(
            check_object,
            shape=LABEL_SHAPE,
        ),
        "progress": partial(
            check_object,
            shape=ObjectShape(
                fields={
                    "value": check_fraction,
                    "label": check_text,
                    "detail": check_text,
                    "segments": partial(check_objects, shape=SEGMENT_SHAPE),
                },
                required=frozenset({"value", "label"}),
            ),
        ),
        "metrics": partial(
            check_objects,
            shape=ObjectShape(
                fields={"label": check_text, "value": check_text, "detail": check_text},
                required=frozenset({"label", "value"}),
            ),
        ),
        "pages": partial(check_objects, shape=PAGE_SHAPE),
        "references": partial(check_objects, shape=REFERENCE_SHAPE, unique="text"),
    },
    required=frozenset({"title", "updated_at", "pages"}),
)


def embed_dashboard_spec(spec: dict[str, object]) -> str:
    """Serialize the spec for embedding in a script element."""

    serialized = dumps(spec, ensure_ascii=False, indent=2)

    return serialized.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")


def app_source_files() -> list[Path]:
    """Return the dashboard app's source files, without its build outputs."""

    return sorted(
        path for path in APP_ROOT.rglob("*") if path.is_file() and not APP_BUILD_OUTPUTS.intersection(path.relative_to(APP_ROOT).parts)
    )


def digest_files(paths: list[Path]) -> str:
    """Return one digest over the relative paths and contents of files in the app."""

    digest = sha256()

    for path in paths:
        digest.update(str(path.relative_to(APP_ROOT)).encode("utf-8"))
        digest.update(path.read_bytes())

    return digest.hexdigest()[:16]


def run_npm(arguments: list[str], workspace: Path) -> None:
    """Run one npm command in the build workspace."""

    npm = shutil.which("npm")

    if npm is None:
        raise DashboardBuildError("building the dashboard needs Node.js 20 or newer and npm on PATH")

    result = subprocess.run([npm, *arguments], cwd=workspace, capture_output=True, text=True, check=False)

    if result.returncode != 0:
        raise DashboardBuildError(f"npm {' '.join(arguments)} failed:\n{result.stdout}{result.stderr}")


def document_contents(page: str) -> str:
    """Return a built page's head and body contents, without the document around them."""

    offsets = DocumentParts(page).offsets
    head = page[offsets["head_start"] : offsets["head_end"]].strip()
    body = page[offsets["body_start"] : offsets["body_end"]].strip()

    return f"{head}\n{body}\n"


def build_template() -> str:
    """Return the built dashboard page, building the app the first time its source changes."""

    sources = app_source_files()
    template_path = CACHE_ROOT / f"template-{digest_files(sources)}.html"
    workspace = CACHE_ROOT / f"workspace-{digest_files([APP_ROOT / APP_LOCKFILE])}"

    CACHE_ROOT.mkdir(parents=True, exist_ok=True)

    with (CACHE_ROOT / ".lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)

        if template_path.exists():
            return template_path.read_text(encoding="utf-8")

        logger.info("use-dashboard: building the dashboard app, which takes a minute the first time")

        workspace.mkdir(exist_ok=True)

        for source in sources:
            target = workspace / source.relative_to(APP_ROOT)

            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

        if not (workspace / "node_modules").is_dir():
            run_npm(["ci", "--no-audit", "--no-fund", "--loglevel=error"], workspace)

        run_npm(["run", "build"], workspace)

        template = document_contents((workspace / "dist" / "index.html").read_text(encoding="utf-8"))
        partial_path = template_path.with_suffix(".partial")

        partial_path.write_text(template, encoding="utf-8")
        partial_path.replace(template_path)

        for stale in CACHE_ROOT.glob("template-*.html"):
            if stale != template_path:
                stale.unlink()

        for stale in CACHE_ROOT.glob("workspace-*"):
            if stale != workspace:
                shutil.rmtree(stale)

        return template


def render_dashboard(spec: object, fragment: bool) -> str:
    """Return the dashboard page for a spec."""

    dashboard = check_object(spec, "dashboard", DASHBOARD_SHAPE)
    template = build_template()

    page = template.replace(DATA_PLACEHOLDER, embed_dashboard_spec(dashboard), 1)
    page = page.replace(TITLE_PLACEHOLDER, escape(PAGE_TITLE_TEMPLATE.format(title=dashboard["title"])), 1)

    return page if fragment else DOCUMENT_PREAMBLE + page + "</html>\n"


def main() -> int:
    """Render a dashboard spec into an HTML page."""

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    parser = ArgumentParser(description="Render a dashboard spec into an HTML page")

    parser.add_argument("--input", required=True, type=Path, help="dashboard spec JSON file")
    parser.add_argument("--output", required=True, type=Path, help="HTML file to write")
    parser.add_argument(
        "--fragment",
        action="store_true",
        help="omit the document preamble, for hosts that wrap the page in their own document",
    )

    arguments = parser.parse_args()

    try:
        page = render_dashboard(loads(arguments.input.read_text(encoding="utf-8")), arguments.fragment)
        encoded_page = page.encode("utf-8")
    except (OSError, JSONDecodeError, UnicodeError, DashboardSpecError, DashboardBuildError) as error:
        logger.error("use-dashboard: %s", error)

        return 1

    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_bytes(encoded_page)

    logger.info("%s", arguments.output.resolve())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
