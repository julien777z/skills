import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Final, NamedTuple

SKILLS_DIRECTORY: Final[Path] = Path(".agents/skills")
README_PATH: Final[Path] = Path("README.md")
COMMIT_MESSAGE: Final[str] = "docs: render the skill listing"
BOT_NAME: Final[str] = "github-actions[bot]"
BOT_EMAIL: Final[str] = "github-actions[bot]@users.noreply.github.com"
START_MARKER: Final[str] = "<!-- skills:start -->"
END_MARKER: Final[str] = "<!-- skills:end -->"
FRONT_MATTER_KEY_PATTERN: Final[re.Pattern[str]] = re.compile(r"^([A-Za-z][\w-]*):\s*(.*)$")
SENTENCE_PATTERN: Final[re.Pattern[str]] = re.compile(r"(?<=[.!?])\s+")
MAX_SUMMARY_LENGTH: Final[int] = 140
SHORT_DESCRIPTIONS: Final[dict[str, str]] = {
    "acceptance-gate": "Have an independent reviewer decide whether a proposed change fits the task and the repository.",
    "assume-library-update": "Write consuming code for a change in one of your libraries before the library update is available.",
    "ci-watch": "Watch a pull request, resolve review findings, and check that CI passes.",
    "config-doctor": "Find configuration names that disagree across code and deployments, or are no longer used.",
    "coordinate-repositories": "Carry one task across selected repositories and user-level installations.",
    "cr": "Resolve a pull request's review threads and checks, then merge and verify it.",
    "current-changes": "Summarize the branch's changes against the default branch with links to the code.",
    "defer-execution": "Schedule separate work on its own branch, either now or after the current pull request merges.",
    "defer-scope": "Record unfinished work in the repository it affects, or read its active records.",
    "doctor-protocol": "Set the audit, fix, review, and reporting process used by every doctor skill.",
    "edit-skill": "Edit a skill, rule, or agent file and fix the guidance gap that prompted the change.",
    "execute-defer-scope": "Review and resolve recorded deferred work for a chosen issue, path, or pull request.",
    "execute-task": "Apply repository guidance, fix issues found along the way, validate the diff, and deliver the change.",
    "guidance-doctor": "Review agent guidance for instructions to cut, clarify, or add.",
    "i-have-adhd": "Make responses easier to scan, with the next action first and tangents removed.",
    "incident": "Restore a broken deployed service, test the fix, and merge the scoped repair.",
    "legacy-doctor": "Remove fallbacks, aliases, and duplicate paths left over from an old contract.",
    "luau": "Apply Roblox Luau conventions when reading or changing game code and tooling.",
    "manage-mcps": "Audit and repair managed MCP connectors across Claude Desktop and Codex.",
    "merge-conflict": "Bring the base branch into a work branch, resolve conflicts, and validate the result.",
    "pre-production": "Apply a pre-release repository's product constraints to contracts, schemas, and stored data.",
    "rebuild-git-history": "Rework your branch into focused commits while preserving and checking its content.",
    "refactor": "Plan and carry out a repository refactor with independent structural review.",
    "roblox-building": "Build and improve Roblox worlds, terrain, structures, props, and assets.",
    "roblox-react": "Design and change React-rendered Roblox interfaces, including HUDs and menus.",
    "roblox-studio": "Create, polish, and playtest Roblox games in Studio.",
    "run-site": "Start a local app, repair startup failures, and test its core flow in a browser.",
    "schema-doctor": "Check models and schemas for unnecessary nulls, complexity, keys, and indexes.",
    "skill-gauntlet": "Audit installed agent skills and test which ones to improve, retire, or install.",
    "storyline": "Create or improve a coherent game story with playable beats and a satisfying ending.",
    "test-fixture": "Check test data and fixtures before changing tests or running tests after a fixture change.",
    "test-skill": "Compare edited and original skill guidance against the same scenario.",
    "text-highlight": "Show code changes in small diff-shaped excerpts that are easy to locate.",
    "vercel-react-view-transitions": "Build smooth React animations with the View Transition API.",
}


class Skill(NamedTuple):
    """One skill's listing entry, read from its front matter."""

    path: Path
    name: str
    description: str
    user_invoked_only: bool


def parse_front_matter(path: Path) -> dict[str, str]:
    """Read a skill's top-level front-matter keys into a mapping."""

    lines = path.read_text(encoding="utf-8").splitlines()

    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path} does not open with a front-matter fence")

    try:
        closing = lines.index("---", 1)
    except ValueError as error:
        raise ValueError(f"{path} has no closing front-matter fence") from error

    front_matter: dict[str, str] = {}
    current_key: str | None = None

    for line in lines[1:closing]:
        if not line.strip():
            continue

        # Fold a multiline description while ignoring nested metadata.
        if line[:1].isspace():
            if current_key == "description":
                front_matter[current_key] += f" {line.strip()}"
            continue

        match = FRONT_MATTER_KEY_PATTERN.match(line)

        if match is None:
            raise ValueError(f"{path} has an invalid top-level front-matter line: {line!r}")

        current_key = match.group(1)
        front_matter[current_key] = match.group(2).strip()

    for key, value in front_matter.items():
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            quote = value[0]
            value = value[1:-1]
            if quote == "'":
                value = value.replace("''", "'")

        front_matter[key] = value

    return front_matter


def read_skills() -> list[Skill]:
    """Read every skill in the source directory, sorted by name."""

    skills: list[Skill] = []

    for skill_file in sorted(SKILLS_DIRECTORY.glob("**/SKILL.md")):
        front_matter = parse_front_matter(skill_file)
        for required in ("name", "description"):
            if not front_matter.get(required):
                raise ValueError(f"{skill_file} front matter has no {required}")

        skills.append(
            Skill(
                path=skill_file,
                name=front_matter["name"],
                description=front_matter["description"],
                user_invoked_only=front_matter.get("disable-model-invocation") == "true",
            )
        )

    if not skills:
        raise ValueError(f"{SKILLS_DIRECTORY} holds no SKILL.md; refusing to render an empty listing")

    return sorted(skills, key=lambda skill: skill.name)


def summarize(skill: Skill) -> str:
    """Use an authored short summary when the skill's opening sentence runs long."""

    summary = SHORT_DESCRIPTIONS.get(skill.name, SENTENCE_PATTERN.split(skill.description)[0])
    if len(summary) > MAX_SUMMARY_LENGTH:
        raise ValueError(f"{skill.name} needs a shorter README description")
    return summary


def render_links(skills: list[Skill]) -> str:
    """Link every skill with a brief description from its own front matter."""

    if not skills:
        return "_None._"

    return "\n".join(
        f"- [`{skill.name}`]({skill.path}) — {summarize(skill)}"
        for skill in skills
    )


def render_section(skills: list[Skill]) -> str:
    """Render both skill groups, split by how each one is invoked."""

    user_invoked = [skill for skill in skills if skill.user_invoked_only]
    model_invoked = [skill for skill in skills if not skill.user_invoked_only]

    return "\n".join(
        [
            START_MARKER,
            "",
            "### User-Invoked",
            "",
            "These run only when you ask for them by name, such as `/refactor`.",
            "",
            render_links(user_invoked),
            "",
            "### Model-Invoked",
            "",
            "An agent reaches for these on its own whenever the work calls for them.",
            "",
            render_links(model_invoked),
            "",
            END_MARKER,
        ]
    )


def render_readme(current: str, section: str) -> str:
    """Replace the managed skills section in the README text."""

    start = current.find(START_MARKER)
    end = current.find(END_MARKER)

    if start == -1 or end == -1:
        raise ValueError(f"{README_PATH} has no {START_MARKER} / {END_MARKER} pair")

    return current[:start] + section + current[end + len(END_MARKER) :]


def commit_listing(branch: str) -> None:
    """Commit and push the rendered listing as the workflow bot."""

    subprocess.run(["git", "config", "user.name", BOT_NAME], check=True)
    subprocess.run(["git", "config", "user.email", BOT_EMAIL], check=True)
    subprocess.run(["git", "add", "--", str(README_PATH)], check=True)
    subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE], check=True)

    if subprocess.run(["git", "push", "origin", f"HEAD:{branch}"]).returncode == 0:
        return

    # Another workflow committed to the branch first; rebase onto it and push once more.
    subprocess.run(["git", "fetch", "origin", branch], check=True)
    subprocess.run(["git", "rebase", f"origin/{branch}"], check=True)
    subprocess.run(["git", "push", "origin", f"HEAD:{branch}"], check=True)


def main() -> None:
    """Render the README's skill listing, or report that it is stale."""

    parser = argparse.ArgumentParser(description="Render the README's skill listing.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero when the README does not already match the skills.",
    )
    parser.add_argument(
        "--commit-to",
        metavar="BRANCH",
        help="Commit and push the rendered listing to this branch when it changed.",
    )

    parsed = parser.parse_args()

    current = README_PATH.read_text(encoding="utf-8")
    rendered = render_readme(current, render_section(read_skills()))

    if parsed.check:
        if rendered != current:
            print(f"{README_PATH} is stale; run this script without --check.", file=sys.stderr)

            raise SystemExit(1)

        print(f"{README_PATH} matches the skills.")

        return

    if rendered == current:
        print(f"{README_PATH} already matches the skills.")

        return

    README_PATH.write_text(rendered, encoding="utf-8")

    print(f"{README_PATH} updated.")

    if parsed.commit_to:
        commit_listing(parsed.commit_to)


if __name__ == "__main__":
    main()
