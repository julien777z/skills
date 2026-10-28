"""Store explicitly registered user profile roots."""

import fcntl
import json
import os
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile

from models import Provider


def validate(value: str) -> tuple[Provider, str]:
    provider, separator, root = value.partition("=")

    if not separator or provider not in {Provider.CLAUDE, Provider.CODEX} or not root.startswith("/") or any(c in root for c in "\n\r\t"):
        raise ValueError(f"Invalid profile registration: {value!r}")

    return Provider(provider), os.path.normpath(root)


def main() -> None:
    home = Path(sys.argv[1])
    mode = sys.argv[2]
    additions = [validate(value) for value in sys.argv[3:]]
    directory = home / ".config" / "agent-skills"
    path = directory / "profiles.json"

    if mode == "list" and not path.exists():
        profiles = []
    else:
        directory.mkdir(mode=0o700, parents=True, exist_ok=True)

        with (directory / "profiles.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            raw = json.loads(path.read_text()) if path.exists() else []

            if not isinstance(raw, list) or not all(isinstance(value, str) for value in raw):
                raise ValueError(f"Invalid profile registry: {path}")

            profiles = [validate(value) for value in raw]

            if mode == "register":
                profiles = list(dict.fromkeys([*profiles, *additions]))

                with NamedTemporaryFile(mode="w", dir=directory, delete=False) as temporary:
                    json.dump([f"{provider}={root}" for provider, root in profiles], temporary, indent=2)
                    temporary.write("\n")
                    temporary_path = temporary.name

                os.chmod(temporary_path, 0o600)
                os.replace(temporary_path, path)

    for provider, root in [*profiles, *additions]:
        print(f"{provider}\t{root}")


if __name__ == "__main__":
    main()
