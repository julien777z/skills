assert_link() {
  [ -L "$1" ] && [ "$(readlink "$1")" = "$2" ] || {
    echo "Unexpected link: $1 (expected $2)" >&2
    exit 1
  }
}

assert_absent() {
  [ ! -e "$1" ] && [ ! -L "$1" ] || {
    echo "Unexpected path: $1" >&2
    exit 1
  }
}

assert_status() {
  local expected="$1"
  shift

  set +e
  "$@"
  local actual=$?
  set -e

  [ "$actual" -eq "$expected" ] || {
    echo "Unexpected exit status: $actual (expected $expected)" >&2
    exit 1
  }
}

assert_hook_configuration() {
  python3 - "$1" "$2" "$3" "$4" "${5:-}" <<'PY'
from json import loads
from pathlib import Path
from shlex import quote
from sys import argv

path = Path(argv[1])
provider = argv[2]
root = Path(argv[3])
source = Path(argv[4])
document = loads(path.read_text())

assert document["foreignSetting"] == "preserved"
assert "BeforeTool" in document["hooks"]

groups = document["hooks"]["SessionStart"]
commands = [handler.get("command") for group in groups for handler in group["hooks"]]
invocation = ["python3", str(root / "hooks/skills-refresh/session_start.py"), provider]

if argv[5]:
    invocation = ["env", f"SKILLS_CLOUD_HOME={argv[5]}", *invocation]

owned = " ".join(quote(argument) for argument in invocation)

assert commands.count(owned) == 1, commands
assert groups[-1]["matcher"] == "startup|resume"
assert len(commands) == 7, commands
assert "foreign-start" in commands
assert "foreign-session" in commands
assert "echo /tmp/hooks/skills-refresh/session_start.py" in commands
assert f"python3 /tmp/hooks/skills-refresh/session_start.py.backup {provider}" in commands
assert f"python3 /previous/.agents/hooks/skills-refresh/session_start.py {provider}" in commands
assert f"python3 /opt/other/hooks/skills-refresh/session_start.py {provider}" in commands
assert (root / "hooks/skills-refresh").resolve() == (
    source / ".agents/hooks/skills-refresh"
).resolve()
PY
}

assert_session_output() {
  python3 - "$1" "$2" "$3" <<'PY'
from json import loads
from pathlib import Path
from sys import argv

output = loads(Path(argv[1]).read_text())["hookSpecificOutput"]
provider = argv[2]
message = argv[3]

assert output["hookEventName"] == "SessionStart"
assert message in output["additionalContext"]

if provider == "claude":
    assert output["reloadSkills"] is True
else:
    assert "reloadSkills" not in output
PY
}

snapshot_tree() {
  for root in "$@"; do
    find "$root" -printf '%y %p %l\n'
    find "$root" -type f -exec sha256sum {} +
  done | sort
}

write_foreign_configuration() {
  python3 - "$1" "$2" <<'PY'
from json import dumps
from pathlib import Path
from sys import argv

path = Path(argv[1])
provider = argv[2]
document = {
    "foreignSetting": "preserved",
    "hooks": {
        "BeforeTool": [{
            "matcher": "*",
            "hooks": [{"type": "command", "command": "foreign-before"}],
        }],
        "SessionStart": [
            {
                "matcher": "startup",
                "hooks": [{"type": "command", "command": "foreign-start"}],
            },
            {
                "matcher": "startup|resume",
                "hooks": [
                    {
                        "type": "command",
                        "command": f"python3 {path.parent / 'hooks/skills-refresh/session_start.py'} {provider}",
                        "statusMessage": "Previous startup status",
                    },
                    {"type": "command", "command": "foreign-session"},
                    {
                        "type": "command",
                        "command": "echo /tmp/hooks/skills-refresh/session_start.py",
                    },
                    {
                        "type": "command",
                        "command": f"python3 /tmp/hooks/skills-refresh/session_start.py.backup {provider}",
                    },
                    {
                        "type": "command",
                        "command": f"python3 /previous/.agents/hooks/skills-refresh/session_start.py {provider}",
                    },
                    {
                        "type": "command",
                        "command": f"python3 /opt/other/hooks/skills-refresh/session_start.py {provider}",
                    },
                ],
            },
        ],
    },
}

path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(dumps(document, indent=2) + "\n")
PY
}

commit_all() {
  git -C "$1" add -A

  if git -C "$1" diff --cached --quiet; then
    return
  fi

  git -C "$1" -c user.name=test -c user.email=test@example.invalid commit --quiet -m fixture
}

add_overlay() {
  git -C "$1" worktree add --quiet -b "skills-overlay/$(basename "$2")" "$2"

  if [ "$3" = complete ]; then
    touch "$(git -C "$2" rev-parse --absolute-git-dir)/skills-overlay"
  fi
}

assert_concurrent_hook_updates() {
  python3 - "$1" "$2" "$3" <<'PY'
from json import loads
from multiprocessing import get_context
from os import environ
from pathlib import Path
from sys import argv, path
from unittest.mock import patch

source, home, executable = map(Path, argv[1:])
context = get_context("fork")
path.insert(0, str(source / ".agents/hooks/skills-refresh"))

from configuration import configure
from models import InstallationMode, Provider

for provider in (Provider.CLAUDE, Provider.CODEX):
    root = home / provider
    root.mkdir(parents=True)
    filename = "hooks.json" if provider == Provider.CODEX else "settings.json"
    entered, release, fetched = context.Event(), context.Event(), context.Event()
    template = source / ".agents/hooks/hooks.json"
    read_text = Path.read_text

    def reconcile(fetch: bool) -> None:
        """Exercise competing native configuration transactions."""

        def read(self: Path, encoding: str | None = None, errors: str | None = None) -> str:
            """Pause the first transaction after its configuration read."""

            content = read_text(self, encoding=encoding, errors=errors)

            if self == template and not fetch:
                entered.set()
                assert release.wait(10)

            return content

        with patch.object(Path, "read_text", read), patch.dict("os.environ", {"PATH": f"{executable}:{environ['PATH']}"}):
            configure(InstallationMode.APPLY, provider, root, source, "", fetch)

        if fetch:
            fetched.set()

    startup = context.Process(target=reconcile, args=(False,))
    update = context.Process(target=reconcile, args=(True,))

    try:
        startup.start()
        assert entered.wait(10)
        update.start()
        fetched.wait(1)
        release.set()
        startup.join(10)
        update.join(10)

        assert startup.exitcode == 0
        assert update.exitcode == 0
        groups = loads((root / filename).read_text())["hooks"]["SessionStart"]
        command = groups[-1]["hooks"][0]["command"]
        assert command.endswith("--fetch"), command
    finally:
        release.set()

        for process in (startup, update):
            if process.pid is not None:
                if process.is_alive():
                    process.terminate()

                process.join()
PY
}
