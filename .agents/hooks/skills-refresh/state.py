from hashlib import sha256
from json import dumps, loads
from os import chown, geteuid, replace
from pathlib import Path
from subprocess import PIPE, run
from tempfile import NamedTemporaryFile

from models import RefreshOutcome


def git(source: Path, *arguments: str) -> str:
    """Read trusted checkout metadata."""

    return run(
        ["git", "-c", f"safe.directory={source}", "-C", str(source), *arguments],
        check=True, stdout=PIPE, text=True, timeout=30,
    ).stdout.strip()


def checkout_root(source: Path) -> Path:
    """Locate the checkout shared by installation worktrees."""

    common = Path(git(source, "rev-parse", "--git-common-dir"))

    if not common.is_absolute():
        common = source / common

    return common.resolve().parent


def fetch_updates(source: Path) -> RefreshOutcome:
    """Fetch the default branch, preserving pending work for reconciliation."""

    checkout = checkout_root(source)
    remote = git(checkout, "remote", "get-url", "origin")

    if remote not in (
        "https://github.com/julien777z/skills.git",
        "https://github.com/julien777z/skills",
        "git@github.com:julien777z/skills.git",
        "git@github.com:julien777z/skills",
    ):
        raise ValueError("Automatic refresh requires the shared skills origin")

    run(
        ["git", "-C", str(checkout), "-c", "credential.interactive=false", "fetch", "origin"],
        check=True, timeout=30,
    )

    default = git(checkout, "symbolic-ref", "refs/remotes/origin/HEAD")
    head = git(checkout, "rev-parse", "HEAD")
    latest = git(checkout, "rev-parse", default)

    if source.resolve() != checkout:
        included = run(
            ["git", "-C", str(source), "merge-base", "--is-ancestor", latest, "HEAD"],
            timeout=30,
        ).returncode == 0

        return RefreshOutcome.CURRENT if included else RefreshOutcome.RECONCILE

    if head == latest:
        return RefreshOutcome.CURRENT

    branch = git(checkout, "symbolic-ref", "--quiet", "HEAD")

    if (
        branch != default.replace("refs/remotes/origin/", "refs/heads/", 1)
        or git(checkout, "status", "--porcelain")
        or run(["git", "-C", str(checkout), "merge-base", "--is-ancestor", "HEAD", latest], timeout=30).returncode != 0
    ):
        return RefreshOutcome.RECONCILE

    git(checkout, "merge", "--ff-only", latest)

    return RefreshOutcome.REPAIRED


def overlay_state(source: Path) -> str | None:
    """Fingerprint the overlay composition inputs."""

    git_directory = Path(git(source, "rev-parse", "--absolute-git-dir"))
    marker = git_directory / "skills-overlay"

    if not marker.is_file():
        return None

    checkout = checkout_root(source)
    digest = sha256(marker.read_bytes())
    digest.update(git(checkout, "rev-parse", "HEAD").encode())
    digest.update(git(checkout, "diff", "HEAD", "--", ".agents").encode())

    for name in git(checkout, "ls-files", "--others", "--exclude-standard", "--", ".agents").splitlines():
        path = checkout / name
        digest.update(name.encode())

        if path.is_symlink():
            digest.update(str(path.readlink()).encode())
        elif path.is_file():
            digest.update(path.read_bytes())

    return digest.hexdigest()


def receipt_path(source: Path) -> Path:
    """Locate the shared overlay receipt."""

    return Path(git(source, "rev-parse", "--absolute-git-dir")) / "skills-refresh-inputs.json"


def overlay_changed(source: Path) -> bool:
    """Check whether the installed source needs reconciliation."""

    current = overlay_state(source)

    if current is None:
        common = Path(git(source, "rev-parse", "--git-common-dir"))

        if not common.is_absolute():
            common = source / common

        return source.resolve() != common.resolve().parent

    receipt = receipt_path(source)

    return not receipt.is_file() or loads(receipt.read_text()).get("inputs") != current


def record_overlay(source: Path) -> None:
    """Record a freshly composed overlay."""

    inputs = overlay_state(source)

    if inputs is None:
        return

    receipt = receipt_path(source)
    receipt.parent.mkdir(parents=True, exist_ok=True, mode=0o700)

    with NamedTemporaryFile(mode="w", dir=receipt.parent, delete=False) as temporary:
        temporary.write(dumps({"inputs": inputs}) + "\n")
        temporary_path = Path(temporary.name)

    if geteuid() == 0:
        owner = source.stat()
        chown(temporary_path, owner.st_uid, owner.st_gid)

    replace(temporary_path, receipt)
