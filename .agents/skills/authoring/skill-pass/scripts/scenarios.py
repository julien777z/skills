import argparse
import json
import subprocess
from pathlib import Path
from typing import Final

import yaml

from models import ScenarioKind, ScenarioRoute
from validate_sources import (
    SCENARIOS_DIRNAME,
    SKILLS_DIRNAME,
    guidance_prose,
    normalized_section_name,
    section_names,
    skill_packages,
    source_files,
)

SCENARIO_FILENAME: Final[str] = "scenario.yaml"
FIXTURE_DIRNAME: Final[str] = "fixture"
SCENARIO_KEYS: Final[tuple[str, ...]] = ("title", "kind", "covers", "prompt", "expect", "history")
EXPECT_KEYS: Final[tuple[str, ...]] = ("id", "check")
ADDING_ENTRY_KEYS: Final[tuple[str, ...]] = ("date", "route", "pull_request", "reason")
BEHAVIOR_CHANGE_ENTRY_KEYS: Final[tuple[str, ...]] = (
    "date",
    "route",
    "pull_request",
    "file",
    "section",
    "reason",
)

TEST_CAUSE_ENTRY_KEYS: Final[tuple[str, ...]] = ("date", "route", "reason")


def listed_files(agents_dir: Path) -> set[Path]:
    """Return the files Git tracks or would track under a directory, leaving out ignored ones."""

    listing = subprocess.run(
        ["git", "-C", str(agents_dir), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )

    paths = (agents_dir / name for name in listing.stdout.split("\0") if name)

    return {path for path in paths if path.is_file()}


def folder_entries(directory: Path, files: set[Path]) -> dict[str, bool]:
    """Return each listed entry directly inside a directory, mapped to whether it is a folder."""

    entries: dict[str, bool] = {}

    for path in files:
        if path != directory and path.is_relative_to(directory):
            parts = path.relative_to(directory).parts
            entries[parts[0]] = entries.get(parts[0], False) or len(parts) > 1

    return entries


def scenario_folders(skills_dir: Path, files: set[Path]) -> list[tuple[Path, Path]]:
    """Return each listed entry of a skill's top-level tests folder with the skill it sits in."""

    return sorted(
        (package / SCENARIOS_DIRNAME / name, package)
        for package in skill_packages(skills_dir).values()
        for name in folder_entries(package / SCENARIOS_DIRNAME, files)
    )


def folder_problems(folder: Path, files: set[Path]) -> list[str]:
    """Report a scenario folder that does not hold exactly its scenario file and fixture folder."""

    entries = folder_entries(folder, files)

    if not entries:
        return ["is not a scenario folder"]

    expected = {SCENARIO_FILENAME, FIXTURE_DIRNAME}

    if set(entries) == expected and entries[FIXTURE_DIRNAME] and not entries[SCENARIO_FILENAME]:
        return []

    held = ", ".join(sorted(entries)) or "nothing"

    return [f"holds {held}; a scenario folder holds {', '.join(sorted(expected))}"]


def mapping_entries(value: object, field: str) -> list[dict[object, object]] | str:
    """Return a field's entries when it is a list of mappings, or the problem with it."""

    if not isinstance(value, list) or not value:
        return f"`{field}` is not a nonempty list"

    if not all(isinstance(entry, dict) for entry in value):
        return f"a `{field}` entry is not a mapping"

    return value


def covers_problems(covers: object, agents_dir: Path, package: Path) -> list[str]:
    """Report covers entries whose guidance file or section heading does not exist."""

    entries = mapping_entries(covers, "covers")

    if isinstance(entries, str):
        return [entries]

    guidance = {path.resolve() for path in source_files(agents_dir, "*.md")}
    problems: list[str] = []

    for number, entry in enumerate(entries, start=1):
        file = entry.get("file")
        section = entry.get("section")

        if not isinstance(file, str) or not isinstance(section, str):
            problems.append(f"covers entry {number} does not hold a `file` and a `section`")

            continue

        target = (agents_dir / file).resolve()

        if target not in guidance:
            problems.append(
                f"covers entry {number}: `{file}` is not a guidance file under {agents_dir.name}/"
            )

            continue

        if number == 1 and not target.is_relative_to(package.resolve()):
            problems.append(f"covers entry 1: `{file}` is not in the skill the scenario sits in")

        try:
            headings, _ = section_names(guidance_prose(target))
        except UnicodeDecodeError:
            problems.append(f"covers entry {number}: `{file}` is not UTF-8 text")

            continue

        if normalized_section_name(section) not in headings:
            problems.append(f"covers entry {number}: `{file}` has no heading **{section}**")

    return problems


def expect_problems(expect: object) -> list[str]:
    """Report expect entries that do not hold an id and a check."""

    entries = mapping_entries(expect, "expect")

    if isinstance(entries, str):
        return [entries]

    return [
        f"expect entry {number} does not hold a nonempty `id` and `check`"
        for number, entry in enumerate(entries, start=1)
        if not all(isinstance(entry.get(key), str) and entry.get(key) for key in EXPECT_KEYS)
    ]


def history_entry_keys(entry: dict[object, object], is_first: bool) -> tuple[str, ...] | None:
    """Return the keys a history entry must hold, in order, or None for an unknown route."""

    match entry.get("route"):
        case ScenarioRoute.BEHAVIOR_CHANGE if is_first:
            return ADDING_ENTRY_KEYS
        case ScenarioRoute.BEHAVIOR_CHANGE:
            return BEHAVIOR_CHANGE_ENTRY_KEYS
        case ScenarioRoute.TEST_CAUSE:
            return TEST_CAUSE_ENTRY_KEYS
        case _:
            return None


def history_problems(history: object) -> list[str]:
    """Report history entries whose date, route or keys break the scenario route rules."""

    entries = mapping_entries(history, "history")

    if isinstance(entries, str):
        return [entries]

    problems: list[str] = []

    if entries[0].get("route") != ScenarioRoute.BEHAVIOR_CHANGE:
        problems.append(
            "history entry 1, which adds the scenario, is not on the"
            f" {ScenarioRoute.BEHAVIOR_CHANGE} route"
        )

    for number, entry in enumerate(entries, start=1):
        if not isinstance(entry.get("date"), str):
            problems.append(f"history entry {number}: `date` is not a quoted string")

        expected = history_entry_keys(entry, is_first=number == 1)

        if expected is None:
            routes = ", ".join(route.value for route in ScenarioRoute)

            problems.append(f"history entry {number}: `route` is not one of {routes}")

            continue

        if tuple(entry) != expected:
            problems.append(
                f"history entry {number}: keys are {', '.join(map(str, entry))};"
                f" a {entry['route']} entry holds {', '.join(expected)}, in that order"
            )

    return problems


def scenario_problems(folder: Path, package: Path, agents_dir: Path, files: set[Path]) -> list[str]:
    """Report every way one scenario folder breaks the regression-scenario format."""

    label = folder.relative_to(agents_dir.parent).as_posix()
    layout = folder_problems(folder, files)

    if layout:
        return [f"{label}: {problem}" for problem in layout]

    try:
        scenario = yaml.safe_load((folder / SCENARIO_FILENAME).read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        return [f"{label}: {SCENARIO_FILENAME} is not UTF-8 text"]
    except yaml.YAMLError as exc:
        return [f"{label}: does not parse with safe YAML loading: {' '.join(str(exc).split())}"]

    if not isinstance(scenario, dict):
        return [f"{label}: is not a mapping"]

    if tuple(scenario) != SCENARIO_KEYS:
        return [
            f"{label}: keys are {', '.join(map(str, scenario))}; a scenario holds"
            f" {', '.join(SCENARIO_KEYS)}, in that order"
        ]

    kinds = ", ".join(kind.value for kind in ScenarioKind)
    problems = [] if scenario["kind"] in ScenarioKind else [f"`kind` is not one of {kinds}"]

    problems += covers_problems(scenario["covers"], agents_dir, package)
    problems += expect_problems(scenario["expect"])
    problems += history_problems(scenario["history"])

    return [f"{label}: {problem}" for problem in problems]


def main() -> None:
    """Print the problems every regression scenario has, as a JSON list of strings."""

    parser = argparse.ArgumentParser(
        description="Check every pinned regression scenario file against the scenario format."
    )

    parser.add_argument("agents_dir", type=Path, help="Canonical source directory to check.")

    agents_dir: Path = parser.parse_args().agents_dir.resolve()
    files = listed_files(agents_dir)
    problems = [
        problem
        for folder, package in scenario_folders(agents_dir / SKILLS_DIRNAME, files)
        for problem in scenario_problems(folder, package, agents_dir, files)
    ]

    print(json.dumps(problems))


if __name__ == "__main__":
    main()
