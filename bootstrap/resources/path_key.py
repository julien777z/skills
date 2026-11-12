from __future__ import annotations

import os
import sys
from pathlib import Path
from unicodedata import normalize


def is_case_insensitive(path: Path) -> bool:
    """Check how the filesystem resolves names beneath this path."""

    if sys.platform == "darwin":
        # Darwin's _PC_CASE_SENSITIVE selector is 11.
        return os.pathconf(path, 11) == 0

    probe = path
    device = path.stat().st_dev

    while probe != probe.parent and probe.parent.stat().st_dev == device:
        alternate = probe.with_name(probe.name.swapcase())

        if alternate != probe and alternate.exists() and os.path.samefile(probe, alternate):
            return True

        probe = probe.parent

    return False


def path_key(requested: Path, entry: bool = False) -> Path:
    """Return the normalized physical path."""

    if entry:
        path = Path(os.path.realpath(requested.parent)) / requested.name
    else:
        path = Path(os.path.realpath(requested))

    current = Path(path.anchor)
    missing = False
    case_insensitive = False

    for part in path.parts[1:]:
        candidate = current / part

        if not missing and os.path.lexists(candidate):
            identity = os.lstat(candidate)

            try:
                with os.scandir(current) as entries:
                    actual = next(
                        (
                            entry.name
                            for entry in entries
                            if entry.stat(follow_symlinks=False).st_ino == identity.st_ino
                            and entry.stat(follow_symlinks=False).st_dev == identity.st_dev
                        ),
                        part,
                    )
            except PermissionError:
                actual = part

            current /= actual
            continue

        if not missing:
            case_insensitive = is_case_insensitive(current)
            missing = True

        current /= part.casefold() if case_insensitive else part

    return current


def path_identity(path: Path) -> tuple[tuple[int, int], tuple[str, ...], set[tuple[int, int]]]:
    """Return the existing ancestor identity and unresolved path suffix."""

    ancestor = Path(os.path.realpath(path))
    suffix = ()

    while not ancestor.exists():
        name = normalize("NFD", ancestor.name) if sys.platform == "darwin" else ancestor.name
        suffix = (name, *suffix)
        ancestor = ancestor.parent

    if suffix and is_case_insensitive(ancestor):
        suffix = tuple(name.casefold() for name in suffix)

    identity = ancestor.stat()
    ancestors = set()

    for current in (ancestor, *ancestor.parents):
        current_identity = current.stat()
        ancestors.add((current_identity.st_dev, current_identity.st_ino))

    return (identity.st_dev, identity.st_ino), suffix, ancestors


def path_relationship(left: Path, right: Path) -> str:
    """Return the physical relationship between two paths."""

    left_identity, left_suffix, left_ancestors = path_identity(left)
    right_identity, right_suffix, right_ancestors = path_identity(right)

    if left_identity == right_identity:
        if left_suffix == right_suffix:
            return "same"

        if right_suffix[:len(left_suffix)] == left_suffix:
            return "contains"

        if left_suffix[:len(right_suffix)] == right_suffix:
            return "inside"
    elif not left_suffix and left_identity in right_ancestors:
        return "contains"
    elif not right_suffix and right_identity in left_ancestors:
        return "inside"

    return "disjoint"


def main() -> None:
    """Print a physical path key or relationship."""

    if sys.argv[1] == "--relationship":
        print(path_relationship(Path(sys.argv[2]), Path(sys.argv[3])))
    else:
        entry = len(sys.argv) > 2 and sys.argv[2] == "--entry"
        print(path_key(Path(sys.argv[1]), entry))


if __name__ == "__main__":
    main()
