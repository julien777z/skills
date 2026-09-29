import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Final

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


def read_skills() -> list[tuple[Path, dict[str, str]]]:
    """Read every skill in the source directory, sorted by name."""

    skills: list[tuple[Path, dict[str, str]]] = []

    for skill_file in sorted(SKILLS_DIRECTORY.glob("**/SKILL.md")):
        front_matter = parse_front_matter(skill_file)

        for required in ("name", "description"):
            if not front_matter.get(required):
                raise ValueError(f"{skill_file} front matter has no {required}")

        skills.append((skill_file, front_matter))

    if not skills:
        raise ValueError(f"{SKILLS_DIRECTORY} holds no SKILL.md; refusing to render an empty listing")

    return sorted(skills, key=lambda skill: skill[1]["name"])


def summarize(front_matter: dict[str, str]) -> str:
    """Use the skill's own summary, or its opening sentence if absent."""

    short_description = front_matter.get("short_description")
    summary = short_description or SENTENCE_PATTERN.split(front_matter["description"])[0]

    if short_description and len(summary) > MAX_SUMMARY_LENGTH:
        raise ValueError(f"{front_matter['name']} needs a shorter README description")
    return summary


def render_links(skills: list[tuple[Path, dict[str, str]]]) -> str:
    """Link every skill with a brief description from its own front matter."""

    if not skills:
        return "_None._"

    return "\n".join(
        f"- [`{front_matter['name']}`]({path}) — {summarize(front_matter)}"
        for path, front_matter in skills
    )


def render_section(skills: list[tuple[Path, dict[str, str]]]) -> str:
    """Render both skill groups, split by how each one is invoked."""

    user_invoked = [skill for skill in skills if skill[1].get("disable-model-invocation") == "true"]
    model_invoked = [skill for skill in skills if skill[1].get("disable-model-invocation") != "true"]

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
