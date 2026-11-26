import re
from pathlib import Path
from typing import Final

SKILLS_DIRNAME: Final[str] = "skills"
SKILL_ENTRY_FILENAME: Final[str] = "SKILL.md"
INSTALLED_PACKAGES_DIRNAME: Final[str] = "node_modules"
SCENARIOS_DIRNAME: Final[str] = "tests"
FENCED_BLOCK_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[ \t]*(?P<fence>```+|~~~+).*?^[ \t]*(?P=fence)[ \t]*$", re.MULTILINE | re.DOTALL
)

HEADING_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^ {0,3}#{1,6}[ \t]+(?P<title>.+?)[ \t]*#*[ \t]*$", re.MULTILINE
)

BOLD_LEAD_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[ \t]*(?:>[ \t]*)?(?:(?:[-*+]|\d+[.)])[ \t]+)?(?:\[[ xX]\][ \t]+)?\*\*(?P<lead>[^*]+)\*\*",
    re.MULTILINE,
)

SECTION_TRAILING_PUNCTUATION: Final[str] = ".:,;!?"


def blank_matches(text: str, pattern: re.Pattern[str]) -> str:
    """Replace every match of a pattern with spaces, keeping each line and offset where it was."""

    return pattern.sub(lambda match: re.sub(r"[^\n]", " ", match.group(0)), text)


def heading_titles(prose: str) -> list[str]:
    """Return a document's headings in order, given its text without code blocks."""

    return [match.group("title") for match in HEADING_PATTERN.finditer(prose)]


def normalized_section_name(name: str) -> str:
    """Return a heading or bold lead in the form two spellings of it are compared in."""

    words = " ".join(name.replace("`", "").replace("’", "'").split())

    return words.rstrip(SECTION_TRAILING_PUNCTUATION).casefold()


def section_names(prose: str) -> tuple[set[str], set[str]]:
    """Return a document's normalized headings and the bold leads of its bullets and paragraphs."""

    headings = {normalized_section_name(title) for title in heading_titles(prose)}
    leads = {
        normalized_section_name(match.group("lead"))
        for match in BOLD_LEAD_PATTERN.finditer(prose)
        if "\n\n" not in match.group("lead")
    }

    return headings, leads


def guidance_prose(path: Path) -> str:
    """Return a guidance file's text with its fenced code blocks blanked out."""

    return blank_matches(path.read_text(encoding="utf-8"), FENCED_BLOCK_PATTERN)


def in_regression_scenarios(path: Path) -> bool:
    """Return whether a path lies in a skill's top-level `tests` folder."""

    return any(
        parent.name == SCENARIOS_DIRNAME and (parent.parent / SKILL_ENTRY_FILENAME).is_file()
        for parent in path.parents
    )


def source_files(directory: Path, pattern: str) -> list[Path]:
    """Return the guidance files under a directory that match a pattern."""

    return sorted(
        path
        for path in directory.rglob(pattern)
        if INSTALLED_PACKAGES_DIRNAME not in path.parts and not in_regression_scenarios(path)
    )


def skill_packages(skills_dir: Path) -> dict[str, Path]:
    """Return each skill's package folder by skill name."""

    entries = source_files(skills_dir, SKILL_ENTRY_FILENAME)

    return {entry.parent.name: entry.parent for entry in entries}
