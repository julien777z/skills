from hashlib import sha256
from json import dumps, loads
from os import chown, geteuid, replace
from pathlib import Path
from subprocess import PIPE, run
from tempfile import NamedTemporaryFile


def git(source: Path, *arguments: str) -> str:
    """Read trusted checkout metadata."""

    return run(
        ["git", "-c", f"safe.directory={source}", "-C", str(source), *arguments],
        check=True, stdout=PIPE, text=True,
    ).stdout.strip()


def overlay_state(source: Path) -> str | None:
    """Fingerprint the overlay composition inputs."""

    git_directory = Path(git(source, "rev-parse", "--absolute-git-dir"))
    marker = git_directory / "skills-overlay"

    if not marker.is_file():
        return None

    common = Path(git(source, "rev-parse", "--git-common-dir"))

    if not common.is_absolute():
        common = source / common

    checkout = common.resolve().parent
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
