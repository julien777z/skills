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
from collections.abc import Iterator
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
SCENARIOS_DIRNAME: Final[str] = "tests"
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
RULE_PATH_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"(?<![\w/.-])(?P<prefix>(?:[\w.-]+/)*)rules/(?P<name>[A-Za-z0-9_-]+)\.md(?![\w-])"
)
RULE_FILE_MENTION_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"`(?P<name>[A-Za-z0-9_-]+)\.md`\s+rule\b"
)
RULE_MENTION_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"(?:\b[Tt]he\s+(?P<word>[A-Za-z][A-Za-z0-9-]*)|`(?P<tick>[A-Za-z0-9_-]+)(?:\.md)?`)"
    r"\s+rules?(?:(?:['’]s|['’])\s+\*\*(?P<section>[^*]+)\*\*|\b)"
)
ALWAYS_LOADED_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"\A---\n.*?^alwaysApply:\s*true\s*$.*?^---$", re.MULTILINE | re.DOTALL
)
SECTION_TRAILING_PUNCTUATION: Final[str] = ".:,;!?"
SECTION_START_PATTERN: Final[re.Pattern[str]] = re.compile(r"$|\W")
FRONTMATTER_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"\A---\n.*?^---[ \t]*$", re.MULTILINE | re.DOTALL
)
FRONTMATTER_FIELD_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^(?P<name>description|when_to_use):[ \t]*(?P<value>.*(?:\n[ \t]+.*)*)", re.MULTILINE
)
BLOCK_SCALAR_PATTERN: Final[re.Pattern[str]] = re.compile(r"\A[>|][+-]?[ \t]*\n")
UNIT_BREAK_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"\n[ \t]*\n|\n(?=[ \t]*(?:(?:[-*+]|\d+[.)])[ \t]|\|))"
)
TABLE_RULE_PATTERN: Final[re.Pattern[str]] = re.compile(r"[ \t|:-]+")
WORDING_PATTERNS: Final[dict[str, re.Pattern[str]]] = {
    "never": re.compile(r"\bnever\b", re.IGNORECASE),
    "do_not": re.compile(r"\b(?:do not|don['’]t)\b", re.IGNORECASE),
    "must_not": re.compile(r"\b(?:must not|mustn['’]t|may not)\b", re.IGNORECASE),
    "always": re.compile(r"\balways\b", re.IGNORECASE),
}
PROHIBITION_PATTERN: Final[re.Pattern[str]] = re.compile(
    "|".join(WORDING_PATTERNS[name].pattern for name in ("never", "do_not", "must_not")),
    re.IGNORECASE,
)
REASON_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"\b(?:because|since|so that|so the|otherwise|which is why)\b", re.IGNORECASE
)
NEGATION_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"\b(?:never|not|no|cannot|don['’]t)\b", re.IGNORECASE
)
CAPITAL_EMPHASIS_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"\b(?:NEVER|ALWAYS|MUST|NOT|CRITICAL|IMPORTANT|ONLY|STOP|REQUIRED|MANDATORY|WARNING)\b"
)
WORDING_COLUMNS: Final[tuple[str, ...]] = (
    "lines",
    "words",
    "units",
    *WORDING_PATTERNS,
    "bold_prohibitions",
    "capital_emphasis",
    "prohibiting_units",
    "reasoned_units",
)
DESCRIPTION_FIELD: Final[str] = "description"
DESCRIPTION_SPECIFICATION_CHARS: Final[int] = 1024
DESCRIPTION_LISTING_CHARS: Final[int] = 1536
OUTPUT_DIR_PATTERN: Final[re.Pattern[str]] = re.compile(r"^\s*output-dir:\s*(\S+)\s*$", re.MULTILINE)
INSTRUCTIONS_FILENAME: Final[str] = "AGENTS.md"
GENERATED_ROOT_FILES: Final[frozenset[str]] = frozenset({INSTRUCTIONS_FILENAME})
PROVIDER_ROOT_DIRNAMES: Final[frozenset[str]] = frozenset({".claude", ".codex", ".cursor"})
CODEX_INSTRUCTIONS_CAP_BYTES: Final[int] = 32768
REMOTE_HEAD_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^ref: refs/heads/(\S+)\tHEAD$", re.MULTILINE
)

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


def generated_output_dir(root: Path, agents_dirname: str) -> str:
    """Read the directory the sync workflow writes generated output into."""

    workflows_dir = root / WORKFLOWS_DIRNAME
    workflow_paths = sorted(workflows_dir.glob("*.yml")) + sorted(workflows_dir.glob("*.yaml"))

    for path in workflow_paths:
        match = OUTPUT_DIR_PATTERN.search(path.read_text(encoding="utf-8"))

        if match is not None:
            return match.group(1).strip("\"'").rstrip("/")

    return f"{agents_dirname}/{GENERATED_DIRNAME}"


def git_output(root: Path, *arguments: str) -> str | None:
    """Return one git command's output, or None when it fails."""

    run = subprocess.run(
        ["git", "-C", str(root), *arguments], check=False, capture_output=True, text=True
    )

    return run.stdout.strip() if run.returncode == 0 else None


def default_branch_ref(root: Path) -> str | None:
    """Resolve the remote-tracking ref of origin's default branch."""

    symbolic = git_output(root, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")

    if symbolic is not None:
        return symbolic

    listing = git_output(root, "ls-remote", "--symref", "origin", "HEAD") or ""
    remote_head = REMOTE_HEAD_PATTERN.search(listing)

    if remote_head is None:
        return None

    candidate = f"origin/{remote_head.group(1)}"

    if git_output(root, "rev-parse", "--verify", "--quiet", f"refs/remotes/{candidate}") is None:
        return None

    return candidate


def find_generated_edits(root: Path, agents_dirname: str) -> list[str]:
    """List generated paths a branch other than the default branch changes."""

    default_ref = default_branch_ref(root)
    branch = git_output(root, "rev-parse", "--abbrev-ref", "HEAD")

    if default_ref is None or branch is None:
        logger.warning("Generated: skipped, since no default branch or current branch resolved")

        return []

    if default_ref == f"origin/{branch}":
        return []

    base = git_output(root, "merge-base", default_ref, "HEAD")
    changed = git_output(root, "diff", "--name-only", base) if base else None

    if changed is None:
        logger.warning("Generated: skipped, since no change against %s could be read", default_ref)

        return []

    output_dir = generated_output_dir(root, agents_dirname)

    return [
        f"{path} is written by Agent Sync only"
        for path in changed.splitlines()
        if path.startswith(f"{output_dir}/")
        or path in GENERATED_ROOT_FILES
        or path.split("/", 1)[0] in PROVIDER_ROOT_DIRNAMES
    ]


def find_instructions_cap_problems(scratch: Path) -> list[str]:
    """Report a generated instructions file past Codex's default size cap."""

    instructions = scratch / INSTRUCTIONS_FILENAME

    if not instructions.is_file():
        return []

    size = instructions.stat().st_size

    if size <= CODEX_INSTRUCTIONS_CAP_BYTES:
        return []

    return [
        f"the generated instructions file {INSTRUCTIONS_FILENAME} is {size} bytes, past the "
        f"{CODEX_INSTRUCTIONS_CAP_BYTES}-byte default Codex reads"
    ]


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

        cap_problems = find_instructions_cap_problems(Path(scratch))

        for problem in cap_problems:
            logger.error("Instructions size: %s", problem)

        if cap_problems:
            return SyncOutcome.INVALID

    return SyncOutcome.VALID


def declared_dependencies(entry_point: str) -> set[str]:
    """Return the skill names an entry point's Dependencies section lists."""

    section = DEPENDENCIES_SECTION_PATTERN.search(entry_point)

    if section is None:
        return set()

    return set(DEPENDENCY_ENTRY_PATTERN.findall(section.group(1)))


def skill_mentions(text: str, skill_names: set[str]) -> Iterator[re.Match[str]]:
    """Yield each place a text names a skill, code blocks included."""

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
            yield match


def named_skills(text: str, skill_names: set[str]) -> set[str]:
    """Return the skills a text names, as `skill_mentions` finds them."""

    return {match.group("name") for match in skill_mentions(text, skill_names)}


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


def in_regression_scenarios(path: Path) -> bool:
    """Return whether a path lies in a skill's top-level folder of regression scenarios."""

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


def rule_files(agents_dir: Path) -> dict[str, Path]:
    """Return each rule file by its casefolded name, the global rules under `global`."""

    rules = {
        path.stem.casefold(): path for path in sorted((agents_dir / RULES_DIRNAME).glob("*.md"))
    }
    global_rules = agents_dir / GLOBAL_RULES_FILENAME

    if global_rules.exists():
        rules[GLOBAL_RULES_NAME] = global_rules

    return rules


def find_dependency_problems(skills_dir: Path) -> list[str]:
    """Report skills named without being declared, and cycles among declared dependencies."""

    packages = skill_packages(skills_dir)
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


def owned_guidance_files(agents_dir: Path) -> list[Path]:
    """Return the canonical Markdown the repository owns, without mirrors or upstream packages."""

    skills_dir = agents_dir / SKILLS_DIRNAME
    third_party = third_party_skill_names(skills_dir)
    third_party_dirs = {
        package for name, package in skill_packages(skills_dir).items() if name in third_party
    }

    return [
        path
        for path in source_files(agents_dir, "*.md")
        if GENERATED_DIRNAME not in path.parts and third_party_dirs.isdisjoint(path.parents)
    ]


def find_citation_problems(agents_dir: Path) -> list[str]:
    """Report links, section citations and rule file names in guidance that point at nothing."""

    root = agents_dir.parent
    rules_dir = agents_dir / RULES_DIRNAME
    packages = skill_packages(agents_dir / SKILLS_DIRNAME)
    package_dirs = set(packages.values())
    rule_paths = rule_files(agents_dir)
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

    for path in owned_guidance_files(agents_dir):
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

        for match in RULE_MENTION_PATTERN.finditer(prose):
            name = match.group("word") or match.group("tick")
            cited_section = match.group("section")
            rule_path = rule_paths.get(name.casefold())

            if rule_path is None or cited_section is None or "\n\n" in cited_section:
                continue

            section = " ".join(cited_section.split())

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


def find_readers(agents_dir: Path, name: str, section: str | None) -> list[str]:
    """Return one line per place in guidance that declares, names or cites a skill or rule."""

    root = agents_dir.parent
    packages = skill_packages(agents_dir / SKILLS_DIRNAME)
    rule_paths = rule_files(agents_dir)
    rule_path = None if name in packages else rule_paths.get(name.casefold())

    if name not in packages and rule_path is None:
        raise RuntimeError(f"{name} is neither a skill nor a rule under {agents_dir}")

    wanted = None if section is None else normalized_section_name(section)
    own_dir = packages.get(name)
    readers: list[str] = []

    if rule_path is not None and (
        rule_path == rule_paths.get(GLOBAL_RULES_NAME)
        or ALWAYS_LOADED_PATTERN.search(rule_path.read_text())
    ):
        readers.append(
            f"{rule_path.relative_to(root).as_posix()}: loads in every session, so every skill reads it"
        )

    if own_dir is not None and wanted is None:
        for _, package in sorted(packages.items()):
            entry = package / SKILL_ENTRY_FILENAME

            if name in declared_dependencies(entry.read_text()):
                readers.append(f"{entry.relative_to(root).as_posix()}: declares `{name}`")

    for path in source_files(agents_dir, "*.md"):
        if GENERATED_DIRNAME in path.parts or path == rule_path:
            continue

        if own_dir is not None and own_dir in path.parents:
            continue

        text = path.read_text(encoding="utf-8")
        mentions: dict[int, str | None] = {}

        if rule_path is None:
            for match in skill_mentions(text, {name}):
                mentions[match.start("name")] = None

            for match in SKILL_SECTION_CITATION_PATTERN.finditer(text):
                if match.group("name") == name:
                    mentions[match.start("name")] = match.group("section")
        else:
            for pattern in (RULE_PATH_PATTERN, RULE_FILE_MENTION_PATTERN):
                for match in pattern.finditer(text):
                    if match.group("name").casefold() == rule_path.stem.casefold():
                        mentions[match.start()] = None

            for match in RULE_MENTION_PATTERN.finditer(text):
                cited_name = match.group("word") or match.group("tick")

                if rule_paths.get(cited_name.casefold()) == rule_path:
                    mentions[match.start()] = match.group("section")

        for offset, cited_section in sorted(mentions.items()):
            where = f"{path.relative_to(root).as_posix()}:{line_number(text, offset)}"

            if cited_section is None and wanted is None:
                readers.append(f"{where}: names it")
            elif cited_section is not None and wanted in (
                None,
                normalized_section_name(cited_section),
            ):
                readers.append(f"{where}: cites **{' '.join(cited_section.split())}**")

    return readers


def prose_units(prose: str) -> list[str]:
    """Return a document's paragraphs, list items and table rows, given its text without code."""

    pieces = UNIT_BREAK_PATTERN.split(blank_matches(prose, HEADING_PATTERN))

    return [
        " ".join(piece.split())
        for piece in pieces
        if piece.strip() and not TABLE_RULE_PATTERN.fullmatch(piece)
    ]


def frontmatter_field_lengths(frontmatter: str) -> dict[str, int]:
    """Return the character length of the description and when-to-use text in a frontmatter."""

    lengths: dict[str, int] = {}

    for match in FRONTMATTER_FIELD_PATTERN.finditer(frontmatter):
        folded = BLOCK_SCALAR_PATTERN.sub("", match.group("value"))
        value = " ".join(line.strip() for line in folded.splitlines())

        if len(value) > 1 and value[0] == value[-1] == "'":
            value = value[1:-1].replace("''", "'")
        elif len(value) > 1 and value[0] == value[-1] == '"':
            value = value[1:-1].replace('\\"', '"')

        lengths[match.group("name")] = len(value)

    return lengths


def wording_report(agents_dir: Path) -> list[str]:
    """Return the owned guidance's prohibition and emphasis counts as printable table rows."""

    root = agents_dir.parent
    counts: dict[str, dict[str, int]] = {}
    long_descriptions: list[str] = []

    for path in owned_guidance_files(agents_dir):
        text = path.read_text(encoding="utf-8")
        label = path.relative_to(root).as_posix()
        frontmatter = FRONTMATTER_PATTERN.match(text)
        body = text if frontmatter is None else text[frontmatter.end() :]
        prose = blank_matches(blank_matches(body, FENCED_BLOCK_PATTERN), INLINE_CODE_PATTERN)
        units = prose_units(prose)
        prohibiting = [unit for unit in units if PROHIBITION_PATTERN.search(unit)]
        bold_leads = (match.group("lead") for match in BOLD_LEAD_PATTERN.finditer(prose))
        values = [
            len(text.splitlines()),
            len(text.split()),
            len(units),
            *(len(pattern.findall(prose)) for pattern in WORDING_PATTERNS.values()),
            sum(1 for lead in bold_leads if NEGATION_PATTERN.search(lead)),
            len(CAPITAL_EMPHASIS_PATTERN.findall(prose)),
            len(prohibiting),
            sum(1 for unit in prohibiting if REASON_PATTERN.search(unit)),
        ]

        counts[label] = dict(zip(WORDING_COLUMNS, values, strict=True))

        if frontmatter is None or path.name != SKILL_ENTRY_FILENAME:
            continue

        lengths = frontmatter_field_lengths(frontmatter.group(0))

        for chars, limit, measured in (
            (lengths.get(DESCRIPTION_FIELD, 0), DESCRIPTION_SPECIFICATION_CHARS, "description"),
            (sum(lengths.values()), DESCRIPTION_LISTING_CHARS, "description and when-to-use text"),
        ):
            if chars > limit:
                long_descriptions.append(f"{label}: {measured}: {chars} characters, past {limit}")

    def row(label: str, count: dict[str, int]) -> str:
        rate = 100 * count["prohibiting_units"] / max(count["units"], 1)

        cells = [label, *(str(count[column]) for column in WORDING_COLUMNS), f"{rate:.1f}"]

        return "\t".join(cells)

    total = {column: sum(count[column] for count in counts.values()) for column in WORDING_COLUMNS}

    return [
        "\t".join(["path", *WORDING_COLUMNS, "prohibiting_per_100_units"]),
        *(row(label, count) for label, count in counts.items()),
        row(f"total of {len(counts)} files", total),
        *long_descriptions,
    ]


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
        description="Check the repository's canonical agent sources with the sync tool its workflow pins, list what reads one of them, or count their prohibition and emphasis wording."
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

    readers = commands.add_parser(
        SourceCommand.READERS,
        parents=[tree],
        help="List the canonical guidance that declares, names or cites a skill or a rule.",
    )

    readers.add_argument(
        "name",
        help="Skill name, or rule file name without its extension; global is the global rules.",
    )

    readers.add_argument(
        "--section",
        help="Section of that skill or rule; only the lines citing it are listed.",
    )

    commands.add_parser(
        SourceCommand.WORDING,
        parents=[tree],
        help="Count prohibition and emphasis wording and over-long descriptions in owned guidance.",
    )

    return parser.parse_args()


def run_command(arguments: argparse.Namespace) -> SyncOutcome:
    """Run one command over the canonical sources."""

    command = SourceCommand(arguments.command)
    root: Path = arguments.root.resolve()
    agents_dirname: str = arguments.agents_dir

    if command in (SourceCommand.READERS, SourceCommand.WORDING):
        listed = (
            find_readers(root / agents_dirname, arguments.name, arguments.section)
            if command is SourceCommand.READERS
            else wording_report(root / agents_dirname)
        )

        for line in listed:
            print(line)

        return SyncOutcome.VALID

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

    generated_problems = find_generated_edits(root, agents_dirname)

    for problem in generated_problems:
        logger.error("Generated: %s", problem)

    problems += generated_problems

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


def main() -> None:
    """Parse the command line, run its command and exit with the outcome's code."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    arguments = parse_arguments()

    try:
        outcome = run_command(arguments)
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        logger.error("%s", exc)

        outcome = SyncOutcome.UNAVAILABLE

    if SourceCommand(arguments.command) in (SourceCommand.READERS, SourceCommand.WORDING):
        raise SystemExit(EXIT_CODES[outcome])

    match outcome:
        case SyncOutcome.VALID:
            logger.info("Valid: the sync tool accepted every canonical source.")
        case SyncOutcome.INVALID:
            logger.error("Invalid: the canonical tree was refused; fix what is reported above.")
        case SyncOutcome.UNAVAILABLE:
            logger.error("Unavailable: the sync tool did not run to completion.")

    raise SystemExit(EXIT_CODES[outcome])


if __name__ == "__main__":
    main()
