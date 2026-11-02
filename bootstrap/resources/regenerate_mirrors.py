import os
import re
import shutil
import subprocess
import sys
import venv
from pathlib import Path
from typing import Final

WORKFLOWS_DIRNAME: Final = ".github/workflows"
ACTION_USE_PATTERN: Final = re.compile(r"uses:\s*([\w.-]+/agent-sync-action)@(\S+)")
COMMIT_PATTERN: Final = re.compile(r"^[0-9a-f]{40}$")
CACHE_DIRNAME: Final = "agent-sync-action"
INSTALL_MARKER_FILENAME: Final = "installed"
REPOSITORY_URL_TEMPLATE: Final = "https://github.com/{repository}"


def find_action_reference(root: Path) -> tuple[str, str] | None:
    workflows_dir = root / WORKFLOWS_DIRNAME
    workflow_paths = sorted(workflows_dir.glob("*.yml")) + sorted(workflows_dir.glob("*.yaml"))
    matches = (ACTION_USE_PATTERN.search(path.read_text(encoding="utf-8")) for path in workflow_paths)
    match = next(filter(None, matches), None)

    return (match.group(1), match.group(2)) if match else None


def resolve_commit(url: str, reference: str) -> str:
    if COMMIT_PATTERN.match(reference):
        return reference

    listing = subprocess.run(
        ["git", "ls-remote", url, reference, f"{reference}^{{}}"],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    rows = [line.split("\t", 1) for line in listing.stdout.splitlines() if line.strip()]

    if not rows:
        raise RuntimeError(f"{url} has no reference named {reference}")

    peeled = next((commit for commit, name in rows if name.endswith("^{}")), None)

    return peeled or rows[0][0]


def install_tool(url: str, commit: str) -> Path:
    install_dir = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / CACHE_DIRNAME / commit
    python = install_dir / "bin" / "python"
    marker = install_dir / INSTALL_MARKER_FILENAME

    if marker.exists():
        return python

    if install_dir.exists():
        shutil.rmtree(install_dir)

    venv.EnvBuilder(with_pip=True).create(install_dir)
    subprocess.run([str(python), "-m", "pip", "install", "--quiet", f"git+{url}@{commit}"], check=True)
    marker.touch()

    return python


def main(root: Path, output_dir: str) -> None:
    action = find_action_reference(root)

    if action is None:
        print(f"No workflow under {root / WORKFLOWS_DIRNAME} pins the sync action; no mirrors to regenerate")

        return

    repository, reference = action
    url = REPOSITORY_URL_TEMPLATE.format(repository=repository)
    python = install_tool(url, resolve_commit(url, reference))

    subprocess.run(
        [str(python), "-m", "agent_sync", "mirror-harnesses", "--root", str(root), "--output-dir", output_dir],
        check=True,
    )


if __name__ == "__main__":
    root_argument, output_dir_argument = sys.argv[1:]

    main(Path(root_argument), output_dir_argument)
