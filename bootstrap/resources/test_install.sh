#!/usr/bin/env bash
set -euo pipefail

cleanup() {
  if [ -n "${lock_holder_pid:-}" ]; then
    kill "$lock_holder_pid" 2>/dev/null || true
    wait "$lock_holder_pid" 2>/dev/null || true
  fi

  rm -rf "${fixture:-}" "${root_fixture:-}" "${rootless_runner:-}"
}

trap cleanup EXIT

readonly SKILLS_REMOTE='https://github.com/julien777z/skills.git'
SOURCE_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

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

if [ "$(id -u)" -eq 0 ]; then
  root_fixture="$(mktemp -d)"
  root_source="$SOURCE_ROOT"
  root_cloud_home="$root_fixture/cloud-home"
  root_clone="$root_cloud_home/.local/share/agent-skills"
  root_home="$root_fixture/root-home"
  root_runtime="$root_fixture/codex-home"
  root_marker="$root_fixture/reexec-marker"

  mkdir -p "$(dirname "$root_clone")" "$root_home/.claude"
  write_foreign_configuration "$root_home/.claude/settings.json" claude
  chown nobody:nogroup "$root_home/.claude/settings.json"
  cp -a "$root_source" "$root_clone"
  rm -rf "$root_clone/.git"
  git -C "$root_clone" init --quiet
  git -C "$root_clone" remote add origin "$SKILLS_REMOTE"
  chown -R nobody:nogroup "$root_cloud_home"
  printf '%s\n' "$root_clone" > "$root_marker"

  (
    cd "$root_clone"
    exec 9<"$root_marker"
    env HOME="$root_home" CODEX_HOME="$root_runtime" SKILLS_CLOUD_HOME="$root_cloud_home" bash "$root_clone/bootstrap/install.sh"
  )

  [ -L "$root_cloud_home/.claude/skills/code-review" ]
  [ "$(realpath "$root_cloud_home/.claude/skills/code-review")" = "$root_clone/.agents/skills/review/code-review" ]
  [ -L "$root_home/.claude/skills/code-review" ]
  [ "$(realpath "$root_home/.claude/skills/code-review")" = "$root_clone/.agents/skills/review/code-review" ]
  [ "$(stat -c %U "$root_home/.claude")" = root ]
  [ "$(stat -c %U "$root_home/.claude/settings.json")" = nobody ]
  assert_hook_configuration "$root_home/.claude/settings.json" claude \
    "$root_home/.claude" "$root_clone" "$root_cloud_home"
  [ -L "$root_runtime/skills/code-review" ]

  root_attached="$root_cloud_home/attached-skills"
  root_overlay="$root_cloud_home/attached-overlay"
  mkdir -p "$root_attached/.agents/skills/example/sample" \
    "$root_attached/.agents/skills/workspace/agent-lock"
  cp -a "$root_source/.agents/hooks" "$root_attached/.agents/"
  cp -a "$root_source/.agents/skills/workspace/agent-lock/resources" \
    "$root_attached/.agents/skills/workspace/agent-lock/"
  printf '%s\n' '# Global guidance' > "$root_attached/.agents/global.md"
  printf '%s\n' '---' 'name: sample' 'description: Sample skill' '---' > "$root_attached/.agents/skills/example/sample/SKILL.md"
  git -C "$root_attached" init --quiet
  git -C "$root_attached" remote add origin "$SKILLS_REMOTE"
  commit_all "$root_attached"
  add_overlay "$root_attached" "$root_overlay" complete
  chown -R nobody:nogroup "$root_attached" "$root_overlay"

  (
    cd "$root_attached"
    env HOME="$root_home" CODEX_HOME="$root_runtime" SKILLS_CLOUD_HOME="$root_cloud_home" \
      bash "$root_clone/.agents/hooks/skills-refresh/install.sh" --resolve-source \
      > "$root_fixture/startup-source"
  )
  [ "$(cat "$root_fixture/startup-source")" = "$root_clone" ]

  (
    cd "$root_attached"
    exec 9<"$root_marker"
    env HOME="$root_home" CODEX_HOME="$root_runtime" SKILLS_CLOUD_HOME="$root_cloud_home" bash "$root_clone/bootstrap/install.sh"
  )

  [ "$(realpath "$root_cloud_home/.claude/skills/sample")" = "$root_overlay/.agents/skills/example/sample" ]
  [ "$(realpath "$root_home/.claude/skills/sample")" = "$root_overlay/.agents/skills/example/sample" ]
  [ "$(stat -c %U "$root_home/.claude/settings.json")" = nobody ]
  assert_hook_configuration "$root_home/.claude/settings.json" claude \
    "$root_home/.claude" "$root_overlay" "$root_cloud_home"

  python3 "$root_overlay/.agents/hooks/skills-refresh/record_overlay.py" "$root_overlay"
  rm "$root_cloud_home/.claude/skills/sample" "$root_home/.claude/skills/sample"
  env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$root_home" CODEX_HOME="$root_runtime" \
    python3 - "$root_home/.claude/settings.json" > "$root_fixture/cloud-hook-output" <<'PY'
from json import dumps, loads
from pathlib import Path
from shlex import split
from subprocess import run
from sys import argv

groups = loads(Path(argv[1]).read_text())["hooks"]["SessionStart"]
command = groups[-1]["hooks"][0]["command"]
run(
    split(command),
    input=dumps({"hook_event_name": "SessionStart", "source": "resume"}),
    text=True,
    check=True,
)
PY
  assert_session_output "$root_fixture/cloud-hook-output" claude \
    'Installed shared skill and rule links were repaired and verified'
  assert_link "$root_cloud_home/.claude/skills/sample" "$root_overlay/.agents/skills/example/sample"
  assert_link "$root_home/.claude/skills/sample" "$root_overlay/.agents/skills/example/sample"

  rootless_runner="$(mktemp -d)"

  mkdir -p "$rootless_runner/bootstrap/resources" \
    "$rootless_runner/.agents/skills/workspace/agent-lock"
  cp "$0" "$rootless_runner/bootstrap/resources/test_install.sh"
  cp "$(dirname "$0")/../install.sh" "$rootless_runner/bootstrap/install.sh"
  cp -a "$root_source/.agents/hooks" "$rootless_runner/.agents/"
  cp -a "$root_source/.agents/skills/workspace/agent-lock/resources" \
    "$rootless_runner/.agents/skills/workspace/agent-lock/"
  chown -R nobody:nogroup "$rootless_runner"

  runuser -u nobody -- env PATH="$PATH" bash "$rootless_runner/bootstrap/resources/test_install.sh"
  exit
fi

installer="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/install.sh"
fixture="$(mktemp -d)"

repo="$fixture/repo"
mkdir -p "$repo/bootstrap" "$repo/.agents/skills/example/sample" "$repo/.agents/rules" \
  "$repo/.agents/.auto_generated/.codex/skills/sample" \
  "$repo/.agents/skills/workspace/agent-lock"
cp "$installer" "$repo/bootstrap/install.sh"
cp -a "$SOURCE_ROOT/.agents/hooks" "$repo/.agents/"
cp -a "$SOURCE_ROOT/.agents/skills/workspace/agent-lock/resources" \
  "$repo/.agents/skills/workspace/agent-lock/"
printf '%s\n' '# Global guidance' > "$repo/.agents/global.md"
printf '%s\n' '# Rule' > "$repo/.agents/rules/example.md"
printf '%s\n' '---' 'name: sample' 'description: Sample skill' '---' > "$repo/.agents/skills/example/sample/SKILL.md"
cp "$repo/.agents/skills/example/sample/SKILL.md" "$repo/.agents/.auto_generated/.codex/skills/sample/SKILL.md"
printf '%s\n' '__pycache__/' > "$repo/.gitignore"
git -C "$repo" init --quiet
git -C "$repo" remote add origin "$SKILLS_REMOTE"
commit_all "$repo"

no_fetch_home="$fixture/no-fetch-home"
no_fetch_clone="$no_fetch_home/.local/share/agent-skills"
no_fetch_bin="$fixture/no-fetch-bin"
no_fetch_marker="$fixture/unexpected-fetch"
system_git="$(command -v git)"
mkdir -p "$(dirname "$no_fetch_clone")" "$no_fetch_home/.codex" "$no_fetch_bin"
cp -a "$repo" "$no_fetch_clone"
printf '%s\n' '#!/usr/bin/env bash' \
  'if [[ " $* " == *" fetch "* ]]; then' \
  '  : > "$GIT_FETCH_MARKER"' \
  '  exit 92' \
  'fi' \
  "exec $system_git \"\$@\"" > "$no_fetch_bin/git"
chmod +x "$no_fetch_bin/git"

(
  cd "$no_fetch_home"
  env HOME="$no_fetch_home" CODEX_HOME="$no_fetch_home/.codex" \
    SKILLS_CLOUD_HOME="$no_fetch_home" GIT_FETCH_MARKER="$no_fetch_marker" \
    PATH="$no_fetch_bin:$PATH" bash "$no_fetch_clone/bootstrap/install.sh" --local-only
  env HOME="$no_fetch_home" CODEX_HOME="$no_fetch_home/.codex" \
    SKILLS_CLOUD_HOME="$no_fetch_home" GIT_FETCH_MARKER="$no_fetch_marker" \
    PATH="$no_fetch_bin:$PATH" bash "$no_fetch_clone/bootstrap/install.sh" --check --local-only
)
assert_absent "$no_fetch_marker"

remote_home="$fixture/remote-home"
remote_repository="$fixture/remote-origin.git"
mkdir -p "$remote_home/.local/bin"
cat > "$remote_home/.local/bin/codex" <<'PYNATIVE'
#!/usr/bin/env python3
from json import dumps, loads
from os import environ
from pathlib import Path
from sys import argv, stdin

assert argv[1:] == ["app-server", "--stdio"]
root = Path(environ["CODEX_HOME"])
state = root / "native-trust.json"

for line in stdin:
    request = loads(line)
    method = request["method"]

    if method == "initialize":
        result = {}
    elif method == "hooks/list":
        command = loads((root / "hooks.json").read_text())["hooks"]["SessionStart"][-1]["hooks"][0]["command"]
        trusted = loads(state.read_text()) if state.exists() else {}
        result = {"data": [{"hooks": [
            {"command": command, "eventName": "sessionStart", "sourcePath": str(root / "hooks.json"),
             "key": "owned-startup", "currentHash": "owned-hash", "trustStatus": "trusted" if "owned-startup" in trusted else "untrusted"},
            {"command": "echo foreign", "eventName": "sessionStart", "sourcePath": str(root / "hooks.json"),
             "key": "foreign-startup", "currentHash": "foreign-hash", "trustStatus": "untrusted"},
        ]}]}
    elif method == "config/batchWrite":
        edit, = request["params"]["edits"]
        assert edit["keyPath"] == "hooks.state"
        assert edit["mergeStrategy"] == "upsert"
        assert set(edit["value"]) == {"owned-startup"}
        state.write_text(dumps(edit["value"]))
        result = {}
    else:
        raise AssertionError(method)

    print(dumps({"id": request["id"], "result": result}), flush=True)
PYNATIVE
chmod +x "$remote_home/.local/bin/codex"
remote_checkout="$remote_home/.local/share/agent-skills"
mkdir -p "$remote_home/.codex" "$remote_home/.claude" "$remote_home/.claude-2" "$(dirname "$remote_checkout")"
git clone --quiet --bare "$repo" "$remote_repository"
git --git-dir="$remote_repository" branch -M main
git --git-dir="$remote_repository" symbolic-ref HEAD refs/heads/main
git config --file "$remote_home/.gitconfig" "url.file://$remote_repository.insteadOf" "$SKILLS_REMOTE"
env HOME="$remote_home" git clone --quiet "$SKILLS_REMOTE" "$remote_checkout"
write_foreign_configuration "$remote_home/.codex/hooks.json" codex

env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$remote_home" PATH="$remote_home/.local/bin:$PATH" CODEX_HOME= \
  CLAUDE_CONFIG_DIR="$remote_home/.claude-2" bash "$remote_checkout/bootstrap/install.sh" --local-only --auto-update
env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$remote_home" PATH="$remote_home/.local/bin:$PATH" CODEX_HOME= \
  CLAUDE_CONFIG_DIR="$remote_home/.claude-2" bash "$remote_checkout/bootstrap/install.sh" --local-only
python3 - "$remote_home" <<'PYHOOK'
from json import loads
from pathlib import Path
from shlex import split
from sys import argv

home = Path(argv[1])

for root, filename in ((".codex", "hooks.json"), (".claude", "settings.json"), (".claude-2", "settings.json")):
    groups = loads((home / root / filename).read_text())["hooks"]["SessionStart"]
    owned = [handler["command"] for group in groups for handler in group["hooks"] if str(home / root / "hooks/skills-refresh/session_start.py") in handler["command"]]
    assert len(owned) == 1, owned
    assert split(owned[0])[-1] == "--fetch", owned

assert loads((home / ".codex/hooks.json").read_text())["foreignSetting"] == "preserved"
PYHOOK

for remote_origin in "$SKILLS_REMOTE" "${SKILLS_REMOTE%.git}" \
  git@github.com:julien777z/skills.git git@github.com:julien777z/skills; do
  git config --file "$remote_home/.gitconfig" --add \
    "url.file://$remote_repository.insteadOf" "$remote_origin"
  git -C "$remote_checkout" remote set-url origin "$remote_origin"
  env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$remote_home" \
    PATH="$remote_home/.local/bin:$PATH" CODEX_HOME= CLAUDE_CONFIG_DIR="$remote_home/.claude-2" \
    bash "$remote_checkout/bootstrap/install.sh" --local-only --check
  env HOME="$remote_home" PATH="$remote_home/.local/bin:$PATH" \
    SKILLS_CLOUD_HOME="$remote_home" CLAUDE_CONFIG_DIR="$remote_home/.claude-2" \
    python3 "$remote_home/.codex/hooks/skills-refresh/session_start.py" --update \
    > "$fixture/origin-update-output"
  [ "$(cat "$fixture/origin-update-output")" = current ]
done

git -C "$remote_checkout" remote set-url origin "file://$remote_repository"
assert_status 1 env HOME="$remote_home" PATH="$remote_home/.local/bin:$PATH" \
  SKILLS_CLOUD_HOME="$remote_home" CLAUDE_CONFIG_DIR="$remote_home/.claude-2" \
  bash "$remote_checkout/bootstrap/install.sh" --local-only --check
assert_status 1 env HOME="$remote_home" PATH="$remote_home/.local/bin:$PATH" \
  SKILLS_CLOUD_HOME="$remote_home" CLAUDE_CONFIG_DIR="$remote_home/.claude-2" \
  python3 "$remote_home/.codex/hooks/skills-refresh/session_start.py" --update
git -C "$remote_checkout" remote set-url origin "$SKILLS_REMOTE"

remote_writer="$fixture/remote-writer"
git clone --quiet "$remote_repository" "$remote_writer"
printf '%s\n' '# Latest shared guidance' >> "$remote_writer/.agents/global.md"
commit_all "$remote_writer"
git -C "$remote_writer" push --quiet origin main
remote_latest="$(git -C "$remote_writer" rev-parse HEAD)"
printf '%s\n' '{"hook_event_name":"SessionStart","source":"startup"}' | \
  env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$remote_home" PATH="$remote_home/.local/bin:$PATH" CODEX_HOME= SKILLS_CLOUD_HOME="$remote_home" \
    python3 "$remote_home/.claude/hooks/skills-refresh/session_start.py" claude --fetch \
    > "$fixture/remote-session-output"
[ "$(git -C "$remote_checkout" rev-parse HEAD)" = "$remote_latest" ]
assert_session_output "$fixture/remote-session-output" claude 'Installed shared skill and rule links were repaired and verified'

remote_overlay="$fixture/remote-overlay"
add_overlay "$remote_checkout" "$remote_overlay" complete
python3 "$remote_overlay/.agents/hooks/skills-refresh/record_overlay.py" "$remote_overlay"
env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$remote_home" PATH="$remote_home/.local/bin:$PATH" CODEX_HOME= \
  bash "$remote_checkout/bootstrap/install.sh" --local-only --source "$remote_overlay"
printf '%s\n' '{"hook_event_name":"SessionStart","source":"startup"}' | \
  env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$remote_home" PATH="$remote_home/.local/bin:$PATH" CODEX_HOME= SKILLS_CLOUD_HOME="$remote_home" \
    python3 "$remote_home/.codex/hooks/skills-refresh/session_start.py" codex --fetch \
    > "$fixture/current-remote-overlay-output"
[ ! -s "$fixture/current-remote-overlay-output" ]
printf '%s\n' '# Updated overlay base' >> "$remote_writer/.agents/global.md"
commit_all "$remote_writer"
git -C "$remote_writer" push --quiet origin main
printf '%s\n' '{"hook_event_name":"SessionStart","source":"resume"}' | \
  env HOME="$remote_home" PATH="$remote_home/.local/bin:$PATH" CODEX_HOME= SKILLS_CLOUD_HOME="$remote_home" \
    python3 "$remote_home/.codex/hooks/skills-refresh/session_start.py" codex --fetch \
    > "$fixture/pending-remote-overlay-output"
assert_session_output "$fixture/pending-remote-overlay-output" pending 'Run update-skills before ordinary work'
[ "$(git -C "$remote_overlay" rev-parse HEAD)" = "$remote_latest" ]
env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$remote_home" PATH="$remote_home/.local/bin:$PATH" CODEX_HOME= \
  bash "$remote_checkout/bootstrap/install.sh" --local-only --source "$remote_checkout"
git -C "$remote_checkout" worktree remove "$remote_overlay"


printf '%s\n' '# Keep local guidance' >> "$remote_checkout/.agents/global.md"
printf '%s\n' '# New remote guidance' >> "$remote_writer/.agents/global.md"
commit_all "$remote_writer"
git -C "$remote_writer" push --quiet origin main
cp "$remote_checkout/.agents/global.md" "$fixture/dirty-guidance"
printf '%s\n' '{"hook_event_name":"SessionStart","source":"resume"}' | \
  env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$remote_home" PATH="$remote_home/.local/bin:$PATH" CODEX_HOME= SKILLS_CLOUD_HOME="$remote_home" \
    python3 "$remote_home/.codex/hooks/skills-refresh/session_start.py" codex --fetch \
    > "$fixture/dirty-session-output"
[ "$(git -C "$remote_checkout" rev-parse HEAD)" = "$remote_latest" ]
cmp "$remote_checkout/.agents/global.md" "$fixture/dirty-guidance"
assert_session_output "$fixture/dirty-session-output" pending 'Run update-skills before ordinary work'

mv "$remote_repository" "$fixture/offline-origin.git"
printf '%s\n' '{"hook_event_name":"SessionStart","source":"startup"}' | \
  env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$remote_home" PATH="$remote_home/.local/bin:$PATH" CODEX_HOME= SKILLS_CLOUD_HOME="$remote_home" \
    python3 "$remote_home/.codex/hooks/skills-refresh/session_start.py" codex --fetch \
    > "$fixture/offline-session-output" 2> "$fixture/offline-session-error"
assert_session_output "$fixture/offline-session-output" pending 'Remote skills refresh failed'
grep -q 'CalledProcessError' "$fixture/offline-session-error"
cmp "$remote_checkout/.agents/global.md" "$fixture/dirty-guidance"
assert_status 1 env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$remote_home" PATH="$remote_home/.local/bin:$PATH" CODEX_HOME= SKILLS_CLOUD_HOME="$remote_home" \
  python3 "$remote_home/.codex/hooks/skills-refresh/session_start.py" --update
mv "$fixture/offline-origin.git" "$remote_repository"

cloud_home="$fixture/cloud"
runtime_home="$fixture/runtime/codex-home"
mkdir -p "$cloud_home" "$runtime_home"
write_foreign_configuration "$runtime_home/hooks.json" codex
env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$cloud_home" CODEX_HOME="$runtime_home" bash "$repo/bootstrap/install.sh"
assert_link "$cloud_home/.agents/skills/sample" "$repo/.agents/skills/example/sample"
assert_link "$runtime_home/skills/sample" "$repo/.agents/.auto_generated/.codex/skills/sample"
assert_link "$runtime_home/AGENTS.md" "$repo/.agents/global.md"
assert_absent "$cloud_home/.codex"
assert_hook_configuration "$runtime_home/hooks.json" codex "$runtime_home" "$repo"
cp "$runtime_home/hooks.json" "$fixture/codex-hooks-first.json"
env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$cloud_home" CODEX_HOME="$runtime_home" bash "$repo/bootstrap/install.sh"
cmp "$fixture/codex-hooks-first.json" "$runtime_home/hooks.json"
assert_hook_configuration "$runtime_home/hooks.json" codex "$runtime_home" "$repo"

local_home="$fixture/local"
mkdir -p "$local_home/.codex"
env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$local_home" CODEX_HOME= bash "$repo/bootstrap/install.sh"
assert_link "$local_home/.codex/skills/sample" "$repo/.agents/.auto_generated/.codex/skills/sample"
assert_link "$local_home/.agents/skills/sample" "$repo/.agents/skills/example/sample"

neutral_home="$fixture/neutral"
mkdir -p "$neutral_home/.agents"
env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$neutral_home" CODEX_HOME= bash "$repo/bootstrap/install.sh"
assert_link "$neutral_home/.agents/skills/sample" "$repo/.agents/skills/example/sample"
assert_absent "$neutral_home/.agents/AGENTS.md"
assert_absent "$neutral_home/.agents/rules"

claude_home="$fixture/claude"
mkdir -p "$claude_home/.claude"
write_foreign_configuration "$claude_home/.claude/settings.json" claude
env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$claude_home" CODEX_HOME= bash "$repo/bootstrap/install.sh"
assert_link "$claude_home/.claude/skills/sample" "$repo/.agents/skills/example/sample"
assert_hook_configuration "$claude_home/.claude/settings.json" claude "$claude_home/.claude" "$repo"
assert_absent "$claude_home/.agents"
env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$claude_home" CODEX_HOME= \
  bash "$repo/bootstrap/install.sh" --check --local-only

drift_repo="$fixture/drift-repo"
drift_home="$fixture/drift-home"
cp -a "$repo" "$drift_repo"
mkdir -p "$drift_repo/.agents/skills/example/renamed-old" \
  "$drift_repo/.agents/skills/example/removed" \
  "$drift_repo/.agents/.auto_generated/.codex/skills/renamed-old" \
  "$drift_repo/.agents/.auto_generated/.codex/skills/removed" \
  "$drift_home/.codex"
printf '%s\n' '---' 'name: renamed-old' 'description: Renamed skill' '---' \
  > "$drift_repo/.agents/skills/example/renamed-old/SKILL.md"
printf '%s\n' '---' 'name: removed' 'description: Removed skill' '---' \
  > "$drift_repo/.agents/skills/example/removed/SKILL.md"
cp "$drift_repo/.agents/skills/example/renamed-old/SKILL.md" \
  "$drift_repo/.agents/.auto_generated/.codex/skills/renamed-old/SKILL.md"
cp "$drift_repo/.agents/skills/example/removed/SKILL.md" \
  "$drift_repo/.agents/.auto_generated/.codex/skills/removed/SKILL.md"
commit_all "$drift_repo"

env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$drift_home" \
  CODEX_HOME="$drift_home/.codex" bash "$drift_repo/bootstrap/install.sh" --local-only
ln -s "$drift_repo/.agents/skills/example/sample" \
  "$drift_home/.agents/skills/stale-alias"
ln -s "$drift_repo/.agents/.auto_generated/.codex/skills/sample" \
  "$drift_home/.codex/skills/stale-alias"
ln -s "$drift_repo/.agents/rules/example.md" \
  "$drift_home/.codex/rules/stale-alias.md"
mv "$drift_repo/.agents/skills/example/renamed-old" \
  "$drift_repo/.agents/skills/example/renamed-new"
mv "$drift_repo/.agents/.auto_generated/.codex/skills/renamed-old" \
  "$drift_repo/.agents/.auto_generated/.codex/skills/renamed-new"
rm -rf "$drift_repo/.agents/skills/example/removed" \
  "$drift_repo/.agents/.auto_generated/.codex/skills/removed"
rm "$drift_home/.codex/skills/sample"
ln -sfn "$drift_repo/.agents/skills/example/renamed-new" \
  "$drift_home/.agents/skills/sample"
snapshot_tree "$drift_home" > "$fixture/drift-before-check"

assert_status 3 env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$drift_home" \
  CODEX_HOME="$drift_home/.codex" bash "$drift_repo/bootstrap/install.sh" \
  --check --local-only
snapshot_tree "$drift_home" > "$fixture/drift-after-check"
cmp "$fixture/drift-before-check" "$fixture/drift-after-check"
assert_absent "$drift_home/.codex/skills/sample"
assert_link "$drift_home/.agents/skills/sample" \
  "$drift_repo/.agents/skills/example/renamed-new"

env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$drift_home" \
  CODEX_HOME="$drift_home/.codex" bash "$drift_repo/bootstrap/install.sh" --local-only
assert_link "$drift_home/.codex/skills/sample" \
  "$drift_repo/.agents/.auto_generated/.codex/skills/sample"
assert_link "$drift_home/.agents/skills/sample" \
  "$drift_repo/.agents/skills/example/sample"
assert_link "$drift_home/.codex/skills/renamed-new" \
  "$drift_repo/.agents/.auto_generated/.codex/skills/renamed-new"
assert_link "$drift_home/.agents/skills/renamed-new" \
  "$drift_repo/.agents/skills/example/renamed-new"
assert_absent "$drift_home/.codex/skills/renamed-old"
assert_absent "$drift_home/.agents/skills/renamed-old"
assert_absent "$drift_home/.codex/skills/removed"
assert_absent "$drift_home/.agents/skills/removed"
assert_absent "$drift_home/.codex/skills/stale-alias"
assert_absent "$drift_home/.agents/skills/stale-alias"
assert_absent "$drift_home/.codex/rules/stale-alias.md"
env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$drift_home" \
  CODEX_HOME="$drift_home/.codex" bash "$drift_repo/bootstrap/install.sh" \
  --check --local-only

write_foreign_configuration "$drift_home/.codex/hooks.json" codex
cp "$drift_home/.codex/hooks.json" "$fixture/configuration-before-check.json"
assert_status 3 env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$drift_home" \
  CODEX_HOME="$drift_home/.codex" bash "$drift_repo/bootstrap/install.sh" \
  --check --local-only
cmp "$fixture/configuration-before-check.json" "$drift_home/.codex/hooks.json"
env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$drift_home" \
  CODEX_HOME="$drift_home/.codex" bash "$drift_repo/bootstrap/install.sh" --local-only
assert_hook_configuration "$drift_home/.codex/hooks.json" codex \
  "$drift_home/.codex" "$drift_repo"

session_repo="$fixture/session-repo"
session_home="$fixture/session-home"
session_runtime="$session_home/.codex"
cp -a "$repo" "$session_repo"
mkdir -p "$session_runtime"
env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$session_home" CODEX_HOME="$session_runtime" \
  bash "$session_repo/bootstrap/install.sh" --local-only
rm "$session_runtime/skills/sample"

for event in '{"hook_event_name":"Other","source":"startup"}' \
  '{"hook_event_name":"SessionStart","source":"clear"}'; do
  printf '%s\n' "$event" | env -u SKILLS_CLOUD_HOME -u CLOUD_HOME \
    HOME="$session_home" CODEX_HOME="$session_runtime" \
    python3 "$session_runtime/hooks/skills-refresh/session_start.py" codex \
    > "$fixture/irrelevant-session-output"
  [ ! -s "$fixture/irrelevant-session-output" ]
  assert_absent "$session_runtime/skills/sample"
done

lock_script="$session_repo/.agents/skills/workspace/agent-lock/resources/main.py"
lock_ready="$fixture/lock-ready"
lock_release="$fixture/lock-release"
env HOME="$session_home" python3 "$lock_script" consume skills-install \
  --owner fixture/holder --activity 'Hold installer for concurrency test' \
  --receipt "$fixture/holder-receipt.json" --wait-seconds 1 --ttl-seconds 30 -- \
  bash -c 'touch "$1"; while [ ! -f "$2" ]; do sleep 0.02; done' \
  fixture-holder "$lock_ready" "$lock_release" > "$fixture/holder-output" 2>&1 &
lock_holder_pid=$!

for _ in $(seq 1 100); do
  [ -e "$lock_ready" ] && break
  sleep 0.02
done
[ -e "$lock_ready" ]

printf '%s\n' '{"hook_event_name":"SessionStart","source":"startup"}' | \
  env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$session_home" \
    CODEX_HOME="$session_runtime" \
    python3 "$session_runtime/hooks/skills-refresh/session_start.py" codex --fetch \
    > "$fixture/busy-session-output"
kill -0 "$lock_holder_pid"
assert_absent "$session_runtime/skills/sample"
assert_session_output "$fixture/busy-session-output" codex \
  'startup check has not run'

assert_status 1 env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$session_home" \
  CODEX_HOME="$session_runtime" \
  python3 "$session_runtime/hooks/skills-refresh/session_start.py" --update
kill -0 "$lock_holder_pid"
assert_absent "$session_runtime/skills/sample"

printf '%s\n' '{"hook_event_name":"SessionStart","source":"startup"}' | \
  env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$session_home" \
    CODEX_HOME="$session_runtime" \
    python3 "$session_runtime/hooks/skills-refresh/session_start.py" codex \
    > "$fixture/codex-session-output" &
session_hook_pid=$!
sleep 0.25
kill -0 "$session_hook_pid"
assert_absent "$session_runtime/skills/sample"
touch "$lock_release"
wait "$lock_holder_pid"
lock_holder_pid=
wait "$session_hook_pid"

assert_link "$session_runtime/skills/sample" \
  "$session_repo/.agents/.auto_generated/.codex/skills/sample"
assert_session_output "$fixture/codex-session-output" codex \
  'newly installed skills appear in the next session'

printf '%s\n' '{"hook_event_name":"SessionStart","source":"resume"}' | \
  env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$session_home" \
    CODEX_HOME="$session_runtime" \
    python3 "$session_runtime/hooks/skills-refresh/session_start.py" codex \
    > "$fixture/current-session-output"
[ ! -s "$fixture/current-session-output" ]

session_claude_home="$fixture/session-claude-home"
mkdir -p "$session_claude_home/.claude"
env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$session_claude_home" CODEX_HOME= \
  bash "$session_repo/bootstrap/install.sh" --local-only
rm "$session_claude_home/.claude/skills/sample"
printf '%s\n' '{"hook_event_name":"SessionStart","source":"resume"}' | \
  env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$session_claude_home" CODEX_HOME= \
    python3 "$session_claude_home/.claude/hooks/skills-refresh/session_start.py" claude \
    > "$fixture/claude-session-output"
assert_link "$session_claude_home/.claude/skills/sample" \
  "$session_repo/.agents/skills/example/sample"
assert_session_output "$fixture/claude-session-output" claude \
  'Installed shared skill and rule links were repaired and verified'

cloud_clone_home="$fixture/cloud-clone-home"
cloud_clone="$cloud_clone_home/.local/share/agent-skills"
attached_checkout="$cloud_clone_home/attached-skills"
cloud_runtime="$fixture/cloud-clone-runtime"
cloud_marker="$fixture/cloud-clone-marker"
mkdir -p "$(dirname "$cloud_clone")"
cp -a "$repo" "$cloud_clone"
cp -a "$repo" "$attached_checkout"
printf '%s\n' "$cloud_clone" > "$cloud_marker"
(
  cd "$attached_checkout/.agents"
  exec 9<"$cloud_marker"
  env HOME="$fixture/runtime-user" CODEX_HOME="$cloud_runtime" SKILLS_CLOUD_HOME="$cloud_clone_home" bash "$cloud_clone/bootstrap/install.sh"
)
assert_link "$cloud_clone_home/.agents/skills/sample" "$attached_checkout/.agents/skills/example/sample"
assert_link "$cloud_runtime/skills/sample" "$attached_checkout/.agents/.auto_generated/.codex/skills/sample"

mkdir -p "$cloud_clone_home/.codex"
(
  cd "$attached_checkout/.agents"
  exec 9<"$cloud_marker"
  env HOME="$fixture/runtime-user" CODEX_HOME="$cloud_clone_home/.codex" SKILLS_CLOUD_HOME="$cloud_clone_home" bash "$cloud_clone/bootstrap/install.sh" > "$fixture/cloud-codex-output"
)
assert_link "$cloud_clone_home/.codex/skills/sample" "$attached_checkout/.agents/.auto_generated/.codex/skills/sample"
[ "$(grep -Fc "$cloud_clone_home/.codex:" "$fixture/cloud-codex-output")" -eq 1 ]

cloud_overlay="$cloud_clone_home/attached-overlay"
cloud_partial="$cloud_clone_home/attached-partial"
commit_all "$attached_checkout"
add_overlay "$attached_checkout" "$cloud_overlay" complete
add_overlay "$attached_checkout" "$cloud_partial" partial

(
  cd "$attached_checkout/.agents"
  exec 9<"$cloud_marker"
  env HOME="$fixture/runtime-user" CODEX_HOME="$cloud_clone_home/.codex" SKILLS_CLOUD_HOME="$cloud_clone_home" bash "$cloud_clone/bootstrap/install.sh"
)

assert_link "$cloud_clone_home/.agents/skills/sample" "$cloud_overlay/.agents/skills/example/sample"
assert_link "$cloud_clone_home/.codex/skills/sample" "$cloud_overlay/.agents/.auto_generated/.codex/skills/sample"

mkdir -p "$fixture/partial-home/.codex"
printf '%s\n' '{"hook_event_name":"SessionStart","source":"startup"}' | \
  env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$fixture/partial-home" CODEX_HOME= \
    python3 "$cloud_partial/.agents/hooks/skills-refresh/session_start.py" codex \
    > "$fixture/partial-overlay-output"
assert_session_output "$fixture/partial-overlay-output" codex 'unmarked worktree'

conflict_home="$fixture/conflict"
conflict_runtime="$fixture/conflict-runtime"
mkdir -p "$conflict_home/.codex" "$conflict_home/.agents/skills/sample"
printf '%s\n' 'Keep this file' > "$conflict_home/.agents/skills/sample/owned.txt"

if env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$conflict_home" CODEX_HOME="$conflict_runtime" bash "$repo/bootstrap/install.sh"; then
  echo 'Expected a conflict to stop installation' >&2
  exit 1
fi

[ "$(cat "$conflict_home/.agents/skills/sample/owned.txt")" = 'Keep this file' ]
assert_absent "$conflict_home/.codex/skills"
assert_absent "$conflict_runtime"

foreign_home="$fixture/foreign"
foreign_runtime="$fixture/foreign-runtime"
mkdir -p "$foreign_home/.codex" "$foreign_runtime/skills" "$fixture/foreign-skill"
ln -s "$fixture/foreign-skill" "$foreign_runtime/skills/sample"

if env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$foreign_home" CODEX_HOME="$foreign_runtime" bash "$repo/bootstrap/install.sh"; then
  echo 'Expected a foreign link to stop installation' >&2
  exit 1
fi

assert_link "$foreign_runtime/skills/sample" "$fixture/foreign-skill"
assert_absent "$foreign_home/.codex/skills"
assert_absent "$foreign_home/.agents"

mkdir -p "$repo/.agents/references"
printf '%s\n' 'Foreign content' > "$repo/README.md"
printf '%s\n' 'Foreign content' > "$repo/.agents/references/foreign.md"

for foreign_target in README.md .agents/references/foreign.md; do
  internal_foreign_home="$fixture/internal-foreign-$(basename "$foreign_target")"
  mkdir -p "$internal_foreign_home/.codex/skills"
  ln -s "$repo/$foreign_target" "$internal_foreign_home/.codex/skills/sample"

  assert_status 1 env -u SKILLS_CLOUD_HOME -u CLOUD_HOME \
    HOME="$internal_foreign_home" CODEX_HOME= \
    bash "$repo/bootstrap/install.sh" --local-only
  assert_link "$internal_foreign_home/.codex/skills/sample" "$repo/$foreign_target"
  assert_absent "$internal_foreign_home/.agents"
done

for obstruction in shared-file runtime-file dangling-root blocked-parent skills-file linked-skills; do
  blocked_home="$fixture/$obstruction"
  blocked_runtime="$fixture/$obstruction-runtime"
  mkdir -p "$blocked_home/.codex"

  case "$obstruction" in
    shared-file) touch "$blocked_home/.agents" ;;
    runtime-file) touch "$blocked_runtime" ;;
    dangling-root) ln -s "$fixture/missing" "$blocked_runtime" ;;
    blocked-parent)
      touch "$blocked_runtime"
      blocked_runtime="$blocked_runtime/nested"
      ;;
    skills-file)
      mkdir -p "$blocked_runtime"
      touch "$blocked_runtime/skills"
      ;;
    linked-skills)
      mkdir -p "$blocked_home/.agents" "$fixture/linked-skills"
      ln -s "$fixture/linked-skills" "$blocked_home/.agents/skills"
      ;;
  esac

  if env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$blocked_home" CODEX_HOME="$blocked_runtime" bash "$repo/bootstrap/install.sh"; then
    echo "Expected $obstruction to stop installation" >&2
    exit 1
  fi

  assert_absent "$blocked_home/.codex/skills"
  if [ "$obstruction" = linked-skills ]; then
    assert_link "$blocked_home/.agents/skills" "$fixture/linked-skills"
  else
    assert_absent "$blocked_home/.agents/skills"
  fi
done

resources_home="$fixture/resources"
resources_runtime="$fixture/resources-runtime"
resources_target="$fixture/linked-resources"
mkdir -p "$resources_home/.codex" "$resources_target"
ln -s "$resources_target" "$resources_home/.codex/resources"
ln -s "$repo/missing-resource" "$resources_target/stale"

if env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$resources_home" CODEX_HOME="$resources_runtime" bash "$repo/bootstrap/install.sh"; then
  echo 'Expected linked resources to stop installation' >&2
  exit 1
fi

assert_link "$resources_home/.codex/resources" "$resources_target"
assert_link "$resources_target/stale" "$repo/missing-resource"

prunable_home="$fixture/prunable-resources"
prunable_runtime="$fixture/prunable-resources-runtime"
mkdir -p "$prunable_home/.codex/resources"
ln -s "$repo/.agents/resources/missing-resource" "$prunable_home/.codex/resources/stale"

env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$prunable_home" CODEX_HOME="$prunable_runtime" bash "$repo/bootstrap/install.sh"
assert_absent "$prunable_home/.codex/resources/stale"

overlay_repo="$fixture/overlay-repo"
overlay_home="$fixture/overlay-home"
cp -a "$repo" "$overlay_repo"
mkdir -p "$overlay_home/.agents" "$overlay_home/.codex"
add_overlay "$overlay_repo" "$fixture/overlay-old" complete
add_overlay "$overlay_repo" "$fixture/overlay-new" complete
touch -d @1 "$(git -C "$fixture/overlay-old" rev-parse --absolute-git-dir)/skills-overlay"

env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$overlay_home" CODEX_HOME= bash "$overlay_repo/bootstrap/install.sh"

assert_link "$overlay_home/.agents/skills/sample" "$fixture/overlay-new/.agents/skills/example/sample"
assert_link "$overlay_home/.codex/skills/sample" \
  "$fixture/overlay-new/.agents/.auto_generated/.codex/skills/sample"
printf '%s\n' '{"hook_event_name":"SessionStart","source":"startup"}' | \
  env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$overlay_home" CODEX_HOME= \
    python3 "$overlay_home/.codex/hooks/skills-refresh/session_start.py" codex \
    > "$fixture/missing-overlay-receipt-output"
assert_session_output "$fixture/missing-overlay-receipt-output" codex \
  'Shared skills need reconciliation'

env HOME="$overlay_home" python3 \
  "$fixture/overlay-new/.agents/hooks/skills-refresh/record_overlay.py" \
  "$fixture/overlay-new"
overlay_git_dir="$(git -C "$fixture/overlay-new" rev-parse --absolute-git-dir)"
overlay_receipt="$overlay_git_dir/skills-refresh-inputs.json"
[ -f "$overlay_receipt" ]

printf '%s\n' '{"hook_event_name":"SessionStart","source":"resume"}' | \
  env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$overlay_home" CODEX_HOME= \
    python3 "$overlay_home/.codex/hooks/skills-refresh/session_start.py" codex \
    > "$fixture/current-overlay-output"
[ ! -s "$fixture/current-overlay-output" ]

add_overlay "$overlay_repo" "$fixture/overlay-unrecorded" complete
touch -d @2147483000 "$(git -C "$fixture/overlay-unrecorded" rev-parse --absolute-git-dir)/skills-overlay"
snapshot_tree "$overlay_home/.codex" "$overlay_home/.agents" > "$fixture/before-newer-overlay"
printf '%s\n' '{"hook_event_name":"SessionStart","source":"resume"}' | \
  env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$overlay_home" CODEX_HOME= \
    python3 "$overlay_home/.codex/hooks/skills-refresh/session_start.py" codex \
    > "$fixture/newer-overlay-output"
assert_session_output "$fixture/newer-overlay-output" codex \
  'Shared skills need reconciliation'
snapshot_tree "$overlay_home/.codex" "$overlay_home/.agents" > "$fixture/after-newer-overlay"
cmp "$fixture/before-newer-overlay" "$fixture/after-newer-overlay"
git -C "$overlay_repo" worktree remove "$fixture/overlay-unrecorded"

overlay_other_home="$fixture/overlay-other-home"
mkdir -p "$overlay_other_home/.codex"
cp "$overlay_receipt" "$fixture/overlay-receipt-before-other-home.json"
env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$overlay_other_home" CODEX_HOME= \
  bash "$overlay_repo/bootstrap/install.sh" --local-only
cmp "$fixture/overlay-receipt-before-other-home.json" "$overlay_receipt"
printf '%s\n' '{"hook_event_name":"SessionStart","source":"startup"}' | \
  env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$overlay_other_home" CODEX_HOME= \
    python3 "$overlay_other_home/.codex/hooks/skills-refresh/session_start.py" codex \
    > "$fixture/cross-home-overlay-output"
[ ! -s "$fixture/cross-home-overlay-output" ]

printf '%s\n' '# Pending overlay input' > "$overlay_repo/.agents/rules/pending.md"
cp "$overlay_receipt" "$fixture/overlay-receipt-before-install.json"
env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$overlay_home" CODEX_HOME= \
  bash "$overlay_repo/bootstrap/install.sh" --local-only
cmp "$fixture/overlay-receipt-before-install.json" "$overlay_receipt"
rm "$overlay_home/.codex/skills/sample"
printf '%s\n' '{"hook_event_name":"SessionStart","source":"resume"}' | \
  env -u SKILLS_CLOUD_HOME -u CLOUD_HOME HOME="$overlay_home" CODEX_HOME= \
    python3 "$overlay_home/.codex/hooks/skills-refresh/session_start.py" codex \
    > "$fixture/overlay-session-output"
assert_absent "$overlay_home/.codex/skills/sample"
assert_session_output "$fixture/overlay-session-output" codex \
  'Shared skills need reconciliation'

echo 'Installer regression checks passed'
