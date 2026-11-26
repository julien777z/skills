import logging
import os
import re
import shutil
import subprocess
import tempfile
import venv
from pathlib import Path
from typing import Final

from models import ActionReference, SyncOutcome

logger = logging.getLogger(__name__)

WORKFLOWS_DIRNAME: Final[str] = ".github/workflows"
ACTION_USE_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^\s*(?:-\s*)?uses:\s*(julien777z/agent-sync-action)@(\S+)\s*$", re.MULTILINE
)

CACHE_DIRNAME: Final[str] = "agent-sync-action"
INSTALL_MARKER_FILENAME: Final[str] = "installed"
EXTERNAL_RESOURCES_FILENAME: Final[str] = "external_resources.json"
REPOSITORY_URL_TEMPLATE: Final[str] = "https://github.com/{repository}"
INSTRUCTIONS_FILENAME: Final[str] = "AGENTS.md"
CODEX_INSTRUCTIONS_CAP_BYTES: Final[int] = 32768
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


def cache_dir() -> Path:
    """Return the user's cache directory, where the script's environments are installed."""

    return Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache")


def install_environment(install_dir: Path, requirement: str) -> Path:
    """Install one pinned requirement into its own environment and return its interpreter."""

    marker = install_dir / INSTALL_MARKER_FILENAME

    if marker.exists():
        logger.info("%s is installed at %s", requirement, install_dir)

        return tool_python(install_dir)

    if install_dir.exists():
        shutil.rmtree(install_dir)

    logger.info("Installing %s into %s", requirement, install_dir)

    # A copied interpreter from a standalone Python build cannot find its standard library, so the
    # environment links to the interpreter, as `python -m venv` does outside Windows.
    venv.EnvBuilder(with_pip=True, symlinks=os.name != "nt").create(install_dir)

    subprocess.run(
        [str(tool_python(install_dir)), "-m", "pip", "install", "--quiet", requirement],
        check=True,
    )

    marker.touch()

    return tool_python(install_dir)


def install_tool(action: ActionReference, commit: str) -> Path:
    """Install the sync tool at one commit and return its interpreter."""

    url = REPOSITORY_URL_TEMPLATE.format(repository=action["repository"])

    return install_environment(cache_dir() / CACHE_DIRNAME / commit, f"git+{url}@{commit}")


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
