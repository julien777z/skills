import argparse
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
import venv
from enum import StrEnum
from pathlib import Path
from typing import Final, TypedDict

logger = logging.getLogger(__name__)

MINIMUM_PYTHON: Final[tuple[int, int]] = (3, 12)
WORKFLOWS_DIRNAME: Final[str] = ".github/workflows"
ACTION_USE_PATTERN: Final[re.Pattern[str]] = re.compile(r"uses:\s*([\w.-]+/agent-sync-action)@(\S+)")
COMMIT_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{40}$")
CACHE_DIRNAME: Final[str] = "agent-sync-action"
INSTALL_MARKER_FILENAME: Final[str] = "installed"
REPOSITORY_URL_TEMPLATE: Final[str] = "https://github.com/{repository}"


class SourceCheckOutcome(StrEnum):
    """What one run of the source check concluded."""

    VALID = "valid"
    INVALID = "invalid"
    UNAVAILABLE = "unavailable"


class ActionReference(TypedDict):
    """The sync action a workflow pins."""

    repository: str
    reference: str


EXIT_CODES: Final[dict[SourceCheckOutcome, int]] = {
    SourceCheckOutcome.VALID: 0,
    SourceCheckOutcome.INVALID: 1,
    SourceCheckOutcome.UNAVAILABLE: 2,
}
TOOL_EXIT_OUTCOMES: Final[dict[int, SourceCheckOutcome]] = {
    0: SourceCheckOutcome.VALID,
    2: SourceCheckOutcome.INVALID,
}


def find_action_reference(root: Path) -> ActionReference:
    """Read which sync action revision the repository's workflows pin."""

    workflows_dir = root / WORKFLOWS_DIRNAME
    workflow_paths = sorted(workflows_dir.glob("*.yml")) + sorted(workflows_dir.glob("*.yaml"))
    matches = (ACTION_USE_PATTERN.search(path.read_text(encoding="utf-8")) for path in workflow_paths)
    match = next(filter(None, matches), None)

    if match is None:
        raise RuntimeError(
            f"No workflow under {workflows_dir} pins the sync action, so there is no revision to match"
        )

    return ActionReference(repository=match.group(1), reference=match.group(2))


def resolve_commit(action: ActionReference) -> str:
    """Resolve the pinned reference to the commit the workflow runs today."""

    if COMMIT_PATTERN.match(action["reference"]):
        return action["reference"]

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

    install_dir = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / CACHE_DIRNAME / commit
    marker = install_dir / INSTALL_MARKER_FILENAME

    if marker.exists():
        logger.info("Sync tool %s@%s is installed at %s", action["repository"], commit[:12], install_dir)

        return tool_python(install_dir)

    if install_dir.exists():
        shutil.rmtree(install_dir)

    logger.info("Installing sync tool %s@%s into %s", action["repository"], commit[:12], install_dir)

    venv.EnvBuilder(with_pip=True).create(install_dir)

    url = REPOSITORY_URL_TEMPLATE.format(repository=action["repository"])
    subprocess.run(
        [str(tool_python(install_dir)), "-m", "pip", "install", "--quiet", f"git+{url}@{commit}"],
        check=True,
    )
    marker.touch()

    return tool_python(install_dir)


def mirror_in_scratch(python: Path, root: Path, agents_dirname: str) -> SourceCheckOutcome:
    """Mirror the canonical tree into a scratch copy of the repository with the sync tool."""

    with tempfile.TemporaryDirectory(prefix="agent-sync-") as scratch:
        shutil.copytree(root / agents_dirname, Path(scratch) / agents_dirname, symlinks=True)

        run = subprocess.run(
            [
                str(python),
                "-m",
                "agent_sync",
                "mirror-providers",
                "--root",
                scratch,
                "--agents-dir",
                agents_dirname,
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    outcome = TOOL_EXIT_OUTCOMES.get(run.returncode, SourceCheckOutcome.UNAVAILABLE)

    if outcome is not SourceCheckOutcome.VALID:
        logger.error("The sync tool reported:\n%s", (run.stdout + run.stderr).strip())

    return outcome


def main() -> SourceCheckOutcome:
    """Run the source check from the command line."""

    parser = argparse.ArgumentParser(
        description="Mirror the canonical agent sources with the sync tool the workflow pins."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root (default: the working directory).",
    )
    parser.add_argument(
        "--agents-dir",
        default=".agents",
        help="Canonical source directory name (default: .agents).",
    )

    arguments = parser.parse_args()
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

    logger.info(
        "Mirroring %s in a scratch copy with %s@%s", agents_dirname, action["repository"], action["reference"]
    )

    return mirror_in_scratch(python, root, agents_dirname)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    try:
        outcome = main()
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        logger.error("%s", exc)

        outcome = SourceCheckOutcome.UNAVAILABLE

    match outcome:
        case SourceCheckOutcome.VALID:
            logger.info("Valid: the sync tool mirrored every canonical file.")
        case SourceCheckOutcome.INVALID:
            logger.error("Invalid: the sync tool refused the canonical tree; fix what it reported above.")
        case SourceCheckOutcome.UNAVAILABLE:
            logger.error("Unavailable: the check did not reach a verdict.")

    raise SystemExit(EXIT_CODES[outcome])
