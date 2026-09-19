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
# Long enough that a routing opener such as "Always run this." cannot stand as the summary.
MINIMUM_SUMMARY_LENGTH: Final[int] = 40


class Skill(NamedTuple):
    """One skill's listing entry, read from its front matter."""

    slug: str
    name: str
    description: str
    user_invoked_only: bool


def parse_front_matter(path: Path) -> dict[str, str]:
    """Read a skill's flat front matter into a mapping."""

    lines = path.read_text(encoding="utf-8").splitlines()

    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path} does not open with a front-matter fence")

    try:
        closing = lines.index("---", 1)
    except ValueError as error:
        raise ValueError(f"{path} has no closing front-matter fence") from error

    front_matter: dict[str, str] = {}

    for line in lines[1:closing]:
        match = FRONT_MATTER_KEY_PATTERN.match(line)

        if match is None:
            raise ValueError(f"{path} front matter is not one key per line: {line!r}")

        value = match.group(2).strip()

        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]

        front_matter[match.group(1)] = value

    return front_matter


def read_skills() -> list[Skill]:
    """Read every skill in the canonical directory, sorted by name."""

    skills: list[Skill] = []

    for skill_file in sorted(SKILLS_DIRECTORY.glob("*/SKILL.md")):
        front_matter = parse_front_matter(skill_file)
        slug = skill_file.parent.name

        for required in ("name", "description"):
            if not front_matter.get(required):
                raise ValueError(f"{skill_file} front matter has no {required}")

        skills.append(
            Skill(
                slug=slug,
                name=front_matter["name"],
                description=front_matter["description"],
                user_invoked_only=front_matter.get("disable-model-invocation") == "true",
            )
        )

    if not skills:
        raise ValueError(f"{SKILLS_DIRECTORY} holds no SKILL.md; refusing to render an empty listing")

    return sorted(skills, key=lambda skill: skill.name)


def summarize(description: str) -> str:
    """Return the opening sentences of a description, up to the first that says what the skill does."""

    summary = ""

    for sentence in SENTENCE_PATTERN.split(description):
        summary = f"{summary} {sentence}".strip()

        if len(summary) >= MINIMUM_SUMMARY_LENGTH:
            break

    return summary


def render_table(skills: list[Skill]) -> str:
    """Render one group of skills as a Markdown table."""

    if not skills:
        return "_None._"

    rows = "\n".join(
        f"| [`{skill.name}`]({SKILLS_DIRECTORY}/{skill.slug}/SKILL.md) | {summarize(skill.description)} |"
        for skill in skills
    )

    return f"| Skill | What it does |\n|---|---|\n{rows}"


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
            render_table(user_invoked),
            "",
            "### Model-Invoked",
            "",
            "An agent reaches for these on its own whenever the work calls for them.",
            "",
            render_table(model_invoked),
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
