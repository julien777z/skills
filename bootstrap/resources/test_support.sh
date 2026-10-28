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

