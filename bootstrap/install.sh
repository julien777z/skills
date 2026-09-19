#!/usr/bin/env bash
# Link this repository's skills and agent definitions into every user-level agent root that
# already exists (~/.claude, ~/.codex, ~/.cursor). Re-running is safe: links are replaced, links
# left behind by a removed skill are pruned, and a root that does not exist is left alone.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CANONICAL_SKILLS="$REPO_ROOT/.agents/skills"
CANONICAL_AGENTS="$REPO_ROOT/.agents/agents"
GENERATED_ROOT="$REPO_ROOT/.agents/.auto_generated"
PROVIDERS=(claude codex cursor)
found_root=0

# The provider mirror carries native metadata the sync workflow generates (a Codex policy file,
# an agent's model); it is preferred when the workflow has produced it.
link_source() {
  local provider="$1" kind="$2" name="$3"
  local mirror="$GENERATED_ROOT/.$provider/$kind/$name"
  if [ -e "$mirror" ]; then
    printf '%s\n' "$mirror"
  else
    printf '%s\n' "$REPO_ROOT/.agents/$kind/$name"
  fi
}

install_link() {
  local target="$1" link="$2"
  if [ -e "$link" ] && [ ! -L "$link" ]; then
    echo "skipping $link: a real file or directory is already there" >&2
    return 0
  fi
  ln -sfn "$target" "$link"
}

# Remove links into this repository whose target no longer exists.
prune_links() {
  local dir="$1" link target
  for link in "$dir"/*; do
    [ -L "$link" ] || continue
    target="$(readlink "$link")"
    case "$target" in
      "$REPO_ROOT"/*) [ -e "$link" ] || rm -f "$link" ;;
    esac
  done
}

install_provider() {
  local provider="$1" root="$HOME/.$provider" skill agent name skills=0 agents=0
  [ -d "$root" ] || return 0
  found_root=1

  mkdir -p "$root/skills"
  for skill in "$CANONICAL_SKILLS"/*/; do
    [ -f "$skill/SKILL.md" ] || continue
    name="$(basename "$skill")"
    install_link "$(link_source "$provider" skills "$name")" "$root/skills/$name"
    skills=$((skills + 1))
  done
  prune_links "$root/skills"

  # Only Claude and Cursor hold agent definitions beside their skills.
  if { [ "$provider" = "claude" ] || [ "$provider" = "cursor" ]; } && [ -d "$CANONICAL_AGENTS" ]; then
    mkdir -p "$root/agents"
    for agent in "$CANONICAL_AGENTS"/*.md; do
      [ -f "$agent" ] || continue
      name="$(basename "$agent")"
      install_link "$(link_source "$provider" agents "$name")" "$root/agents/$name"
      agents=$((agents + 1))
    done
    prune_links "$root/agents"
  fi

  echo "$root: $skills skills, $agents agents linked"
}

for provider in "${PROVIDERS[@]}"; do
  install_provider "$provider"
done

if [ "$found_root" -eq 0 ]; then
  echo "No user-level agent root found under $HOME (looked for .claude, .codex, .cursor); nothing linked."
fi
