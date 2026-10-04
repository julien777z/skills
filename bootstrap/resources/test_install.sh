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

cloud_home="$fixture/cloud"
runtime_home="$fixture/runtime/codex-home"
mkdir -p "$cloud_home"
env -u SKILLS_CLOUD_HOME HOME="$cloud_home" CODEX_HOME="$runtime_home" bash "$repo/bootstrap/install.sh"
assert_link "$cloud_home/.agents/skills/sample" "$repo/.agents/skills/example/sample"
assert_link "$runtime_home/skills/sample" "$repo/.agents/.auto_generated/.codex/skills/sample"
assert_link "$runtime_home/AGENTS.md" "$repo/.agents/global.md"
[ ! -e "$cloud_home/.codex" ]
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
[ ! -e "$neutral_home/.agents/AGENTS.md" ]
[ ! -e "$neutral_home/.agents/rules" ]

claude_home="$fixture/claude"
mkdir -p "$claude_home/.claude"
env -u SKILLS_CLOUD_HOME HOME="$claude_home" CODEX_HOME= bash "$repo/bootstrap/install.sh"
assert_link "$claude_home/.claude/skills/sample" "$repo/.agents/skills/example/sample"
[ ! -e "$claude_home/.agents" ]

conflict_home="$fixture/conflict"
conflict_runtime="$fixture/conflict-runtime"
mkdir -p "$conflict_home/.codex" "$conflict_home/.agents/skills/sample"
printf '%s\n' 'Keep this file' > "$conflict_home/.agents/skills/sample/owned.txt"

if env -u SKILLS_CLOUD_HOME HOME="$conflict_home" CODEX_HOME="$conflict_runtime" bash "$repo/bootstrap/install.sh"; then
  echo 'Expected a conflict to stop installation' >&2
  exit 1
fi

[ "$(cat "$conflict_home/.agents/skills/sample/owned.txt")" = 'Keep this file' ]
[ ! -e "$conflict_home/.codex/skills" ]
[ ! -e "$conflict_runtime" ]

foreign_home="$fixture/foreign"
foreign_runtime="$fixture/foreign-runtime"
mkdir -p "$foreign_home/.codex" "$foreign_runtime/skills" "$fixture/foreign-skill"
ln -s "$fixture/foreign-skill" "$foreign_runtime/skills/sample"

if env -u SKILLS_CLOUD_HOME HOME="$foreign_home" CODEX_HOME="$foreign_runtime" bash "$repo/bootstrap/install.sh"; then
  echo 'Expected a foreign link to stop installation' >&2
  exit 1
fi

assert_link "$foreign_runtime/skills/sample" "$fixture/foreign-skill"
[ ! -e "$foreign_home/.codex/skills" ]
[ ! -e "$foreign_home/.agents" ]

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

  [ ! -e "$blocked_home/.codex/skills" ]
  [ ! -e "$blocked_home/.agents/skills" ]
done

echo 'Installer regression checks passed'
