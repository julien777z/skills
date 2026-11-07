import os
import sys
from pathlib import Path

def main() -> None:
    """Print the physical key for a path."""

    entry = len(sys.argv) > 2 and sys.argv[2] == "--entry"
    requested = Path(sys.argv[1])

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

            current /= actual
            continue

        if not missing:
            if sys.platform == "darwin":
                # Darwin's _PC_CASE_SENSITIVE selector is 11.
                case_sensitive_selector = 11
                case_insensitive = os.pathconf(current, case_sensitive_selector) == 0
            else:
                probe = current
                device = current.stat().st_dev

                while probe != probe.parent and probe.parent.stat().st_dev == device:
                    alternate = probe.with_name(probe.name.swapcase())

                    if alternate != probe and alternate.exists() and os.path.samefile(probe, alternate):
                        case_insensitive = True
                        break

                    probe = probe.parent

            missing = True

        current /= part.casefold() if case_insensitive else part

    print(current)


if __name__ == "__main__":
    main()
