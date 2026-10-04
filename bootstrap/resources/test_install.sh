#!/usr/bin/env bash
set -euo pipefail

installer="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/install.sh"
fixture="$(mktemp -d)"
trap 'rm -rf "$fixture"' EXIT

repo="$fixture/repo"
mkdir -p "$repo/bootstrap" "$repo/.agents/skills/example/sample" "$repo/.agents/rules" \
  "$repo/.agents/.auto_generated/.codex/skills/sample"
cp "$installer" "$repo/bootstrap/install.sh"
printf '%s\n' '# Global guidance' > "$repo/.agents/global.md"
printf '%s\n' '# Rule' > "$repo/.agents/rules/example.md"
printf '%s\n' '---' 'name: sample' 'description: Sample skill' '---' > "$repo/.agents/skills/example/sample/SKILL.md"
cp "$repo/.agents/skills/example/sample/SKILL.md" "$repo/.agents/.auto_generated/.codex/skills/sample/SKILL.md"

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

cloud_home="$fixture/cloud"
runtime_home="$fixture/runtime/codex-home"
mkdir -p "$cloud_home"
env -u SKILLS_CLOUD_HOME HOME="$cloud_home" CODEX_HOME="$runtime_home" bash "$repo/bootstrap/install.sh"
assert_link "$cloud_home/.agents/skills/sample" "$repo/.agents/skills/example/sample"
assert_link "$runtime_home/skills/sample" "$repo/.agents/.auto_generated/.codex/skills/sample"
assert_link "$runtime_home/AGENTS.md" "$repo/.agents/global.md"
assert_absent "$cloud_home/.codex"
env -u SKILLS_CLOUD_HOME HOME="$cloud_home" CODEX_HOME="$runtime_home" bash "$repo/bootstrap/install.sh"

local_home="$fixture/local"
mkdir -p "$local_home/.codex"
env -u SKILLS_CLOUD_HOME HOME="$local_home" CODEX_HOME= bash "$repo/bootstrap/install.sh"
assert_link "$local_home/.codex/skills/sample" "$repo/.agents/.auto_generated/.codex/skills/sample"
assert_link "$local_home/.agents/skills/sample" "$repo/.agents/skills/example/sample"

neutral_home="$fixture/neutral"
mkdir -p "$neutral_home/.agents"
env -u SKILLS_CLOUD_HOME HOME="$neutral_home" CODEX_HOME= bash "$repo/bootstrap/install.sh"
assert_link "$neutral_home/.agents/skills/sample" "$repo/.agents/skills/example/sample"
assert_absent "$neutral_home/.agents/AGENTS.md"
assert_absent "$neutral_home/.agents/rules"

claude_home="$fixture/claude"
mkdir -p "$claude_home/.claude"
env -u SKILLS_CLOUD_HOME HOME="$claude_home" CODEX_HOME= bash "$repo/bootstrap/install.sh"
assert_link "$claude_home/.claude/skills/sample" "$repo/.agents/skills/example/sample"
assert_absent "$claude_home/.agents"

cloud_clone_home="$fixture/cloud-clone-home"
cloud_clone="$cloud_clone_home/.local/share/agent-skills"
cloud_runtime="$fixture/cloud-clone-runtime"
cloud_marker="$fixture/cloud-clone-marker"
mkdir -p "$(dirname "$cloud_clone")"
cp -a "$repo" "$cloud_clone"
git -C "$cloud_clone" init --quiet
git -C "$cloud_clone" remote add origin https://github.com/julien777z/skills.git
printf '%s\n' "$cloud_clone" > "$cloud_marker"
(
  exec 9<"$cloud_marker"
  env HOME="$fixture/runtime-user" CODEX_HOME="$cloud_runtime" SKILLS_CLOUD_HOME="$cloud_clone_home" bash "$cloud_clone/bootstrap/install.sh"
)
assert_link "$cloud_clone_home/.agents/skills/sample" "$cloud_clone/.agents/skills/example/sample"
assert_link "$cloud_runtime/skills/sample" "$cloud_clone/.agents/.auto_generated/.codex/skills/sample"

conflict_home="$fixture/conflict"
conflict_runtime="$fixture/conflict-runtime"
mkdir -p "$conflict_home/.codex" "$conflict_home/.agents/skills/sample"
printf '%s\n' 'Keep this file' > "$conflict_home/.agents/skills/sample/owned.txt"

if env -u SKILLS_CLOUD_HOME HOME="$conflict_home" CODEX_HOME="$conflict_runtime" bash "$repo/bootstrap/install.sh"; then
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

if env -u SKILLS_CLOUD_HOME HOME="$foreign_home" CODEX_HOME="$foreign_runtime" bash "$repo/bootstrap/install.sh"; then
  echo 'Expected a foreign link to stop installation' >&2
  exit 1
fi

assert_link "$foreign_runtime/skills/sample" "$fixture/foreign-skill"
assert_absent "$foreign_home/.codex/skills"
assert_absent "$foreign_home/.agents"

for obstruction in shared-file runtime-file dangling-root blocked-parent skills-file; do
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
  esac

  if env -u SKILLS_CLOUD_HOME HOME="$blocked_home" CODEX_HOME="$blocked_runtime" bash "$repo/bootstrap/install.sh"; then
    echo "Expected $obstruction to stop installation" >&2
    exit 1
  fi

  assert_absent "$blocked_home/.codex/skills"
  assert_absent "$blocked_home/.agents/skills"
done

echo 'Installer regression checks passed'
