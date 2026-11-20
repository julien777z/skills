import argparse
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
import venv
from pathlib import Path
from typing import Final
from urllib.parse import unquote

from models import ActionReference, ExternalResource, SourceCommand, SyncOutcome

logger = logging.getLogger(__name__)

MINIMUM_PYTHON: Final[tuple[int, int]] = (3, 12)
WORKFLOWS_DIRNAME: Final[str] = ".github/workflows"
ACTION_USE_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^\s*(?:-\s*)?uses:\s*(julien777z/agent-sync-action)@(\S+)\s*$", re.MULTILINE
)
CACHE_DIRNAME: Final[str] = "agent-sync-action"
INSTALL_MARKER_FILENAME: Final[str] = "installed"
EXTERNAL_RESOURCES_FILENAME: Final[str] = "external_resources.json"
REPOSITORY_URL_TEMPLATE: Final[str] = "https://github.com/{repository}"
SKILLS_DIRNAME: Final[str] = "skills"
SKILL_ENTRY_FILENAME: Final[str] = "SKILL.md"
DEPENDENCIES_SECTION_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^## Dependencies\n(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL
)
DEPENDENCY_ENTRY_PATTERN: Final[re.Pattern[str]] = re.compile(r"^- `([^`]+)`", re.MULTILINE)
SKILL_NAME_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"(?<![\w/.-])(?P<slash>/)?(?P<tick>`)?(?P<name>[a-z0-9]+(?:-[a-z0-9]+)*)(?P=tick)?(?![\w-])"
)
SKILL_CONTEXT_BEFORE_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"\b(?:skills?|invok(?:e|es|ed|ing)|us(?:e|es|ed|ing)|run(?:s|ning)?|through|via"
    r"|switch(?:es|ing)? to|hand(?:s|ing)? off to)\s+[\"'(]?$",
    re.IGNORECASE,
)
SKILL_CONTEXT_AFTER_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^(?:['’]s\b|[\"')]?\s+skills?\b)", re.IGNORECASE
)
CONTEXT_BEFORE_CHARS: Final[int] = 30
CONTEXT_AFTER_CHARS: Final[int] = 10
SKILL_RESOURCE_KIND: Final[str] = "skill"
INSTALLED_PACKAGES_DIRNAME: Final[str] = "node_modules"
GENERATED_DIRNAME: Final[str] = ".auto_generated"
RULES_DIRNAME: Final[str] = "rules"
REFERENCES_DIRNAME: Final[str] = "references"
GLOBAL_RULES_FILENAME: Final[str] = "global.md"
GLOBAL_RULES_NAME: Final[str] = "global"
FENCED_BLOCK_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[ \t]*(?P<fence>```+|~~~+).*?^[ \t]*(?P=fence)[ \t]*$", re.MULTILINE | re.DOTALL
)
INLINE_CODE_PATTERN: Final[re.Pattern[str]] = re.compile(r"`[^`\n]*`")
HEADING_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^ {0,3}#{1,6}[ \t]+(?P<title>.+?)[ \t]*#*[ \t]*$", re.MULTILINE
)
BOLD_LEAD_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[ \t]*(?:>[ \t]*)?(?:(?:[-*+]|\d+[.)])[ \t]+)?(?:\[[ xX]\][ \t]+)?\*\*(?P<lead>[^*]+)\*\*",
    re.MULTILINE,
)
HTML_ANCHOR_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"<a\s[^>]*?\b(?:id|name)=[\"'](?P<anchor>[^\"']+)[\"']", re.IGNORECASE
)
MARKDOWN_LINK_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"\[(?P<text>[^\]\n]*(?:\n[^\]\n]+)?)\]\((?P<target>[^()\s]+)(?:\s+\"[^\"\n]*\")?\)"
)
LINK_TEXT_PATTERN: Final[re.Pattern[str]] = re.compile(r"\[([^\]]*)\]\([^)]*\)")
URL_SCHEME_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
LINK_PLACEHOLDER_CHARS: Final[frozenset[str]] = frozenset("<>{}$*")
SLUG_DROPPED_PATTERN: Final[re.Pattern[str]] = re.compile(r"[^\w\- ]")
SKILL_SECTION_CITATION_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"`(?P<name>[a-z0-9]+(?:-[a-z0-9]+)*)`['’]s\s+\*\*(?P<section>[^*]+)\*\*"
)
RULE_SECTION_CITATION_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"(?:\b[Tt]he\s+(?P<word>[A-Za-z][A-Za-z0-9-]*)|`(?P<tick>[A-Za-z0-9_-]+)(?:\.md)?`)"
    r"\s+rules?(?:['’]s|s?['’])\s+\*\*(?P<section>[^*]+)\*\*"
)
RULE_PATH_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"(?<![\w/.-])(?P<prefix>(?:[\w.-]+/)*)rules/(?P<name>[A-Za-z0-9_-]+)\.md(?![\w-])"
)
RULE_FILE_MENTION_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"`(?P<name>[A-Za-z0-9_-]+)\.md`\s+rule\b"
)
SECTION_TRAILING_PUNCTUATION: Final[str] = ".:,;!?"
SECTION_START_PATTERN: Final[re.Pattern[str]] = re.compile(r"$|\W")


EXIT_CODES: Final[dict[SyncOutcome, int]] = {
    SyncOutcome.VALID: 0,
    SyncOutcome.INVALID: 1,
    SyncOutcome.UNAVAILABLE: 2,
}
TOOL_EXIT_OUTCOMES: Final[dict[int, SyncOutcome]] = {
    0: SyncOutcome.VALID,
    2: SyncOutcome.INVALID,
}


def find_action_reference(root: Path) -> ActionReference:
    """Read which sync action revision the repository's workflows pin."""

    workflows_dir = root / WORKFLOWS_DIRNAME
    workflow_paths = sorted(workflows_dir.glob("*.yml")) + sorted(workflows_dir.glob("*.yaml"))
    matches = (
        ACTION_USE_PATTERN.search(path.read_text(encoding="utf-8")) for path in workflow_paths
    )
    match = next(filter(None, matches), None)

    if match is None:
        raise RuntimeError(
            f"No workflow under {workflows_dir} pins the sync action, so there is no revision to match"
        )

    return ActionReference(repository=match.group(1), reference=match.group(2))


def resolve_commit(action: ActionReference) -> str:
    """Resolve the pinned reference to the commit the workflow runs today."""

    url = REPOSITORY_URL_TEMPLATE.format(repository=action["repository"])
    listing = subprocess.run(
        ["git", "ls-remote", url, action["reference"], f"{action['reference']}^{{}}"],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    rows = [line.split("\t", 1) for line in listing.stdout.splitlines() if line.strip()]

    if not rows:
        raise RuntimeError(f"{url} has no reference named {action['reference']}")

    peeled = next((commit for commit, name in rows if name.endswith("^{}")), None)

    return peeled or rows[0][0]


def tool_python(install_dir: Path) -> Path:
    """Return the interpreter of an installed sync tool."""

    return install_dir / ("Scripts" if os.name == "nt" else "bin") / "python"


def install_tool(action: ActionReference, commit: str) -> Path:
    """Install the sync tool at one commit and return its interpreter."""

    install_dir = (
        Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / CACHE_DIRNAME / commit
    )
    marker = install_dir / INSTALL_MARKER_FILENAME

    if marker.exists():
        logger.info(
            "Sync tool %s@%s is installed at %s",
            action["repository"],
            commit[:12],
            install_dir,
        )

        return tool_python(install_dir)

    if install_dir.exists():
        shutil.rmtree(install_dir)

    logger.info(
        "Installing sync tool %s@%s into %s",
        action["repository"],
        commit[:12],
        install_dir,
    )

    # A copied interpreter from a standalone Python build cannot find its standard library, so the
    # environment links to the interpreter, as `python -m venv` does outside Windows.
    venv.EnvBuilder(with_pip=True, symlinks=os.name != "nt").create(install_dir)

    url = REPOSITORY_URL_TEMPLATE.format(repository=action["repository"])
    subprocess.run(
        [
            str(tool_python(install_dir)),
            "-m",
            "pip",
            "install",
            "--quiet",
            f"git+{url}@{commit}",
        ],
        check=True,
    )

    marker.touch()

    return tool_python(install_dir)


def run_sync_tool(python: Path, root: Path, agents_dirname: str, command: list[str]) -> SyncOutcome:
    """Run one sync tool command over a canonical tree and report its outcome."""

    arguments = [
        str(python),
        "-m",
        "agent_sync",
        *command,
        "--root",
        str(root),
        "--agents-dir",
        agents_dirname,
    ]
    run = subprocess.run(arguments, check=False, capture_output=True, text=True)
    outcome = TOOL_EXIT_OUTCOMES.get(run.returncode, SyncOutcome.UNAVAILABLE)

    if outcome is not SyncOutcome.VALID:
        logger.error("The sync tool reported:\n%s", (run.stdout + run.stderr).strip())

    return outcome


def mirror_in_scratch(python: Path, root: Path, agents_dirname: str) -> SyncOutcome:
    """Validate external resources and mirror canonical sources in a scratch copy."""

    with tempfile.TemporaryDirectory(prefix="agent-sync-") as scratch:
        scratch_agents = Path(scratch) / agents_dirname

        shutil.copytree(root / agents_dirname, scratch_agents, symlinks=True)

        commands: list[list[str]] = [["mirror-harnesses"]]

        if (scratch_agents / EXTERNAL_RESOURCES_FILENAME).exists():
            commands.insert(0, ["refresh-external-resources", "--dry-run"])

        for command in commands:
            outcome = run_sync_tool(python, Path(scratch), agents_dirname, command)

            if outcome is not SyncOutcome.VALID:
                return outcome

    return SyncOutcome.VALID


def declared_dependencies(entry_point: str) -> set[str]:
    """Return the skill names an entry point's Dependencies section lists."""

    section = DEPENDENCIES_SECTION_PATTERN.search(entry_point)

    if section is None:
        return set()

    return set(DEPENDENCY_ENTRY_PATTERN.findall(section.group(1)))


def named_skills(text: str, skill_names: set[str]) -> set[str]:
    """Return the skills a text names, code blocks included.

    A hyphenated name in backticks counts anywhere. Any other backticked or hyphenated mention
    counts only in skill context, since a name also spells ordinary words, fields and keywords:
    followed by `'s` or the word skill, or after the word skill, a verb that runs one, such
    as invoke, use, run, switch to or hand off to, or through or via. A `/name` command is one the
    user is told to run, never a reference, and an unquoted one-word name never counts.
    """

    named: set[str] = set()

    for match in SKILL_NAME_PATTERN.finditer(text):
        name = match.group("name")

        if name not in skill_names:
            continue

        quoted = match.group("tick") is not None
        command = match.group("slash") is not None
        hyphenated = "-" in name

        if command or not (quoted or hyphenated):
            continue

        if (quoted and hyphenated) or is_in_skill_context(text, match):
            named.add(name)

    return named


def is_in_skill_context(text: str, match: re.Match[str]) -> bool:
    """Report whether the words around a matched name show it names a skill."""

    before = text[max(0, match.start() - CONTEXT_BEFORE_CHARS) : match.start()]
    after = text[match.end() : match.end() + CONTEXT_AFTER_CHARS]

    return bool(
        SKILL_CONTEXT_BEFORE_PATTERN.search(before) or SKILL_CONTEXT_AFTER_PATTERN.search(after)
    )


def third_party_skill_names(skills_dir: Path) -> set[str]:
    """Return the skills the external resources file refreshes from their upstream."""

    registry = skills_dir.parent / EXTERNAL_RESOURCES_FILENAME

    if not registry.exists():
        return set()

    resources: list[ExternalResource] = json.loads(registry.read_text())["resources"]

    return {
        resource.get("skill_name_override", resource["name"])
        for resource in resources
        if resource["kind"] == SKILL_RESOURCE_KIND and resource["update_on_sync"]
    }


def source_files(directory: Path, pattern: str) -> list[Path]:
    """Return the files under a directory that match a pattern, leaving out installed packages."""

    return sorted(
        path for path in directory.rglob(pattern) if INSTALLED_PACKAGES_DIRNAME not in path.parts
    )


def find_dependency_problems(skills_dir: Path) -> list[str]:
    """Report skills named without being declared, and cycles among declared dependencies.

    Packages refreshed from upstream are not read for names, since their upstream owns their text.
    """

    entries = source_files(skills_dir, SKILL_ENTRY_FILENAME)
    packages = {entry.parent.name: entry.parent for entry in entries}
    third_party = third_party_skill_names(skills_dir)
    skill_names = set(packages)
    graph: dict[str, set[str]] = {}
    problems: list[str] = []

    for name, package in sorted(packages.items()):
        declared = declared_dependencies((package / SKILL_ENTRY_FILENAME).read_text())

        graph[name] = declared & skill_names

        if name in third_party:
            continue

        texts = [path.read_text() for path in source_files(package, "*.md")]
        named = set().union(*(named_skills(text, skill_names) for text in texts)) - {name}

        for missing in sorted(named - declared):
            problems.append(f"{name} names `{missing}` without declaring it in its Dependencies")

    finished: set[str] = set()

    def visit(name: str, path: list[str]) -> None:
        for dependency in sorted(graph.get(name, ())):
            if dependency in path:
                cycle = path[path.index(dependency) :] + [dependency]

                problems.append("dependency cycle: " + " -> ".join(cycle))
            elif dependency not in finished:
                visit(dependency, path + [dependency])

        finished.add(name)

    for name in sorted(graph):
        if name not in finished:
            visit(name, [name])

    return problems


def blank_matches(text: str, pattern: re.Pattern[str]) -> str:
    """Replace every match of a pattern with spaces, keeping each line and offset where it was."""

    return pattern.sub(lambda match: re.sub(r"[^\n]", " ", match.group(0)), text)


def line_number(text: str, offset: int) -> int:
    """Return the one-based line an offset of a text falls on."""

    return text.count("\n", 0, offset) + 1


def normalized_section_name(name: str) -> str:
    """Return a heading or bold lead in the form two spellings of it are compared in."""

    words = " ".join(name.replace("`", "").replace("’", "'").split())

    return words.rstrip(SECTION_TRAILING_PUNCTUATION).casefold()


def heading_titles(prose: str) -> list[str]:
    """Return a document's headings in order, given its text without code blocks."""

    return [match.group("title") for match in HEADING_PATTERN.finditer(prose)]


def heading_anchors(prose: str) -> set[str]:
    """Return the anchors a document's headings and explicit anchor tags answer to."""

    anchors = {match.group("anchor").casefold() for match in HTML_ANCHOR_PATTERN.finditer(prose)}
    seen: dict[str, int] = {}

    for title in heading_titles(prose):
        plain = LINK_TEXT_PATTERN.sub(r"\1", title).replace("`", "").replace("*", "")
        slug = SLUG_DROPPED_PATTERN.sub("", plain.strip().lower()).replace(" ", "-")
        count = seen.get(slug, 0)

        seen[slug] = count + 1

        anchors.add(slug if count == 0 else f"{slug}-{count}")

    return anchors


def section_names(prose: str) -> tuple[set[str], set[str]]:
    """Return a document's normalized headings and the bold leads of its bullets and paragraphs."""

    headings = {normalized_section_name(title) for title in heading_titles(prose)}
    leads = {
        normalized_section_name(match.group("lead"))
        for match in BOLD_LEAD_PATTERN.finditer(prose)
        if "\n\n" not in match.group("lead")
    }

    return headings, leads


def find_citation_problems(agents_dir: Path) -> list[str]:
    """Report citations in canonical guidance that point at nothing.

    A relative markdown link must reach a file, and its anchor a heading there. A section cited as
    `skill-name`'s **Section**, the global rules' **Section** or the <Name> rule's **Section** must
    be a heading or the bold lead of a bullet or paragraph, or the words one starts with, in that
    skill's entry point and references or in that rule. A rule file named as `rules/<name>.md` or as the `<name>.md` rule
    must exist. Generated mirrors and packages refreshed from upstream are not read, and a mention
    whose target is ambiguous is passed over.
    """

    root = agents_dir.parent
    skills_dir = agents_dir / SKILLS_DIRNAME
    rules_dir = agents_dir / RULES_DIRNAME
    packages = {
        entry.parent.name: entry.parent for entry in source_files(skills_dir, SKILL_ENTRY_FILENAME)
    }
    third_party_dirs = {
        package
        for name, package in packages.items()
        if name in third_party_skill_names(skills_dir)
    }
    package_dirs = set(packages.values())
    rule_paths = {path.stem.casefold(): path for path in sorted(rules_dir.glob("*.md"))}
    global_rules = agents_dir / GLOBAL_RULES_FILENAME

    if global_rules.exists():
        rule_paths[GLOBAL_RULES_NAME] = global_rules

    prose_by_path: dict[Path, str] = {}

    def prose_of(path: Path) -> str:
        if path not in prose_by_path:
            prose_by_path[path] = blank_matches(
                path.read_text(encoding="utf-8"), FENCED_BLOCK_PATTERN
            )

        return prose_by_path[path]

    def has_section(targets: list[Path], section: str) -> bool:
        cited = normalized_section_name(section)

        for target in targets:
            headings, leads = section_names(prose_of(target))

            if any(
                SECTION_START_PATTERN.match(name[len(cited) :])
                for name in headings | leads
                if name.startswith(cited)
            ):
                return True

        return False

    problems: list[str] = []

    for path in source_files(agents_dir, "*.md"):
        if GENERATED_DIRNAME in path.parts or not third_party_dirs.isdisjoint(path.parents):
            continue

        prose = prose_of(path)
        label = path.relative_to(root).as_posix()
        package = next((parent for parent in path.parents if parent in package_dirs), None)
        local_dirs = [path.parent] if package is None else [path.parent, package]

        for match in MARKDOWN_LINK_PATTERN.finditer(blank_matches(prose, INLINE_CODE_PATTERN)):
            target = match.group("target")

            if (
                URL_SCHEME_PATTERN.match(target)
                or target.startswith(("/", "//"))
                or not LINK_PLACEHOLDER_CHARS.isdisjoint(target)
            ):
                continue

            file_part, _, anchor = target.partition("#")
            linked = (path.parent / unquote(file_part)).resolve() if file_part else path
            where = f"{label}:{line_number(prose, match.start())}"

            if not linked.exists():
                problems.append(f"{where}: link target `{target}` does not exist")

                continue

            if not anchor or linked.suffix != ".md":
                continue

            if unquote(anchor).casefold() not in heading_anchors(prose_of(linked)):
                problems.append(f"{where}: link `{target}` names an anchor no heading there has")

        for match in SKILL_SECTION_CITATION_PATTERN.finditer(prose):
            name = match.group("name")
            section = " ".join(match.group("section").split())

            if name not in packages or "\n\n" in match.group("section"):
                continue

            cited_package = packages[name]
            targets = [cited_package / SKILL_ENTRY_FILENAME] + source_files(
                cited_package / REFERENCES_DIRNAME, "*.md"
            )

            if not has_section(targets, section):
                problems.append(
                    f"{label}:{line_number(prose, match.start())}: `{name}` has no section"
                    f" **{section}** in its {SKILL_ENTRY_FILENAME} or references"
                )

        for match in RULE_SECTION_CITATION_PATTERN.finditer(prose):
            name = match.group("word") or match.group("tick")
            section = " ".join(match.group("section").split())
            rule_path = rule_paths.get(name.casefold())

            if rule_path is None or "\n\n" in match.group("section"):
                continue

            if not has_section([rule_path], section):
                problems.append(
                    f"{label}:{line_number(prose, match.start())}:"
                    f" {rule_path.relative_to(root).as_posix()} has no section **{section}**"
                )

        mentions = [
            (match, match.group("prefix") in ("", f"{agents_dir.name}/"))
            for match in RULE_PATH_PATTERN.finditer(prose)
        ] + [(match, True) for match in RULE_FILE_MENTION_PATTERN.finditer(prose)]

        for match, is_rule_reference in sorted(mentions, key=lambda mention: mention[0].start()):
            filename = f"{match.group('name')}.md"
            is_local = any(
                (directory / candidate).exists()
                for directory in local_dirs
                for candidate in (filename, f"{RULES_DIRNAME}/{filename}")
            )

            if not is_rule_reference or is_local or (rules_dir / filename).exists():
                continue

            problems.append(
                f"{label}:{line_number(prose, match.start())}: rule file"
                f" {rules_dir.relative_to(root).as_posix()}/{filename} does not exist"
            )

    return problems


def parse_arguments() -> argparse.Namespace:
    """Parse the command and the tree it runs on."""

    tree = argparse.ArgumentParser(add_help=False)

    tree.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root (default: the working directory).",
    )

    tree.add_argument(
        "--agents-dir",
        default=".agents",
        help="Canonical source directory name (default: .agents).",
    )

    parser = argparse.ArgumentParser(
        description="Run the sync tool the repository's workflow pins over its canonical agent sources."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser(
        SourceCommand.CHECK,
        parents=[tree],
        help="Validate skill dependencies, citations and the canonical sources in a scratch copy.",
    )

    mirror = commands.add_parser(
        SourceCommand.MIRROR,
        parents=[tree],
        help="Regenerate the provider mirrors of the canonical sources in place.",
    )

    mirror.add_argument(
        "--output-dir",
        required=True,
        help="Directory, relative to the root, that receives the provider mirrors.",
    )

    return parser.parse_args()


def main() -> SyncOutcome:
    """Run the requested command from the command line."""

    arguments = parse_arguments()
    command = SourceCommand(arguments.command)
    root: Path = arguments.root.resolve()
    agents_dirname: str = arguments.agents_dir

    if sys.version_info < MINIMUM_PYTHON:
        minimum = ".".join(str(part) for part in MINIMUM_PYTHON)

        raise RuntimeError(
            f"The sync tool needs Python {minimum} or newer; run this with the repository's interpreter"
        )

    if not (root / agents_dirname).is_dir():
        raise RuntimeError(f"{root / agents_dirname} is not a directory")

    action = find_action_reference(root)
    commit = resolve_commit(action)
    python = install_tool(action, commit)

    if command is SourceCommand.MIRROR:
        logger.info(
            "Mirroring %s into %s with %s@%s",
            agents_dirname,
            arguments.output_dir,
            action["repository"],
            action["reference"],
        )

        return run_sync_tool(
            python,
            root,
            agents_dirname,
            ["mirror-harnesses", "--output-dir", arguments.output_dir],
        )

    problems = find_dependency_problems(root / agents_dirname / SKILLS_DIRNAME)

    for problem in problems:
        logger.error("Skill dependencies: %s", problem)

    citation_problems = find_citation_problems(root / agents_dirname)

    for problem in citation_problems:
        logger.error("Citations: %s", problem)

    problems += citation_problems

    logger.info(
        "Validating %s in a scratch copy with %s@%s",
        agents_dirname,
        action["repository"],
        action["reference"],
    )

    outcome = mirror_in_scratch(python, root, agents_dirname)

    if problems and outcome is SyncOutcome.VALID:
        return SyncOutcome.INVALID

    return outcome


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    try:
        outcome = main()
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        logger.error("%s", exc)

        outcome = SyncOutcome.UNAVAILABLE

    match outcome:
        case SyncOutcome.VALID:
            logger.info("Valid: the sync tool accepted every canonical source.")
        case SyncOutcome.INVALID:
            logger.error(
                "Invalid: the canonical tree was refused; fix what is reported above."
            )
        case SyncOutcome.UNAVAILABLE:
            logger.error("Unavailable: the sync tool did not run to completion.")

    raise SystemExit(EXIT_CODES[outcome])
