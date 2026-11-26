import argparse
import json
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
)

SCENARIO_FILENAME: Final[str] = "scenario.yaml"
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


def scenario_paths(skills_dir: Path) -> list[Path]:
    """Return every scenario file in a skill's top-level folder of regression scenarios."""

    return sorted(
        path
        for package in skill_packages(skills_dir).values()
        for path in (package / SCENARIOS_DIRNAME).glob(f"*/{SCENARIO_FILENAME}")
    )


def mapping_entries(value: object, field: str) -> list[dict[object, object]] | str:
    """Return a field's entries when it is a list of mappings, or the problem with it."""

    if not isinstance(value, list) or not value:
        return f"`{field}` is not a nonempty list"

    if not all(isinstance(entry, dict) for entry in value):
        return f"a `{field}` entry is not a mapping"

    return value


def covers_problems(covers: object, agents_dir: Path) -> list[str]:
    """Report covers entries whose file or section heading does not exist."""

    entries = mapping_entries(covers, "covers")

    if isinstance(entries, str):
        return [entries]

    problems: list[str] = []

    for number, entry in enumerate(entries, start=1):
        file = entry.get("file")
        section = entry.get("section")

        if not isinstance(file, str) or not isinstance(section, str):
            problems.append(f"covers entry {number} does not hold a `file` and a `section`")

            continue

        target = (agents_dir / file).resolve()

        if not target.is_relative_to(agents_dir.resolve()) or not target.is_file():
            problems.append(f"covers entry {number}: `{file}` is not a file under {agents_dir.name}/")

            continue

        headings, _ = section_names(guidance_prose(target))

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
            f"history entry 1, which adds the scenario, is not on the {ScenarioRoute.BEHAVIOR_CHANGE} route"
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


def scenario_problems(path: Path, agents_dir: Path) -> list[str]:
    """Report every way one scenario file breaks the regression-scenario format."""

    label = path.relative_to(agents_dir.parent).as_posix()

    try:
        scenario = yaml.safe_load(path.read_text(encoding="utf-8"))
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

    problems += covers_problems(scenario["covers"], agents_dir)
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
    problems = [
        problem
        for path in scenario_paths(agents_dir / SKILLS_DIRNAME)
        for problem in scenario_problems(path, agents_dir)
    ]

    print(json.dumps(problems))


if __name__ == "__main__":
    main()
