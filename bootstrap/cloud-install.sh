#!/usr/bin/env bash
# Run from Claude cloud setup after cloning this repository to the cache path.
set -euo pipefail

USER_HOME="${SKILLS_CLOUD_HOME:-/home/user}"
CACHE="$USER_HOME/.local/share/agent-skills"
SKILLS_REMOTE='https://github.com/julien777z/skills.git'

run_as_user() {
  if [ "$(id -u)" -eq 0 ]; then
    runuser -u user -- env HOME="$USER_HOME" "$@"
  else
    env HOME="$USER_HOME" "$@"
  fi
}

is_skills_checkout() {
  local remote
  remote="$(run_as_user git -C "$1" remote get-url origin 2>/dev/null || true)"
  case "$remote" in
    "$SKILLS_REMOTE"|https://github.com/julien777z/skills|git@github.com:julien777z/skills.git|git@github.com:julien777z/skills)
      return 0 ;;
    *) return 1 ;;
  esac
}

[ -d "$USER_HOME" ] || { echo "Missing Claude user home: $USER_HOME" >&2; exit 1; }
[ -d "$CACHE/.git" ] || { echo "Missing skills setup clone: $CACHE" >&2; exit 1; }
is_skills_checkout "$CACHE" || { echo "Setup clone is not the skills repository: $CACHE" >&2; exit 1; }

# This checkout is disposable installation state, so update it only when clean and fast-forwardable.
if [ -n "$(run_as_user git -C "$CACHE" status --porcelain)" ]; then
  echo "Skills setup clone has local edits; refusing to overwrite them: $CACHE" >&2
  exit 1
fi
run_as_user git -C "$CACHE" pull --ff-only

source="$CACHE"
while IFS= read -r git_marker; do
  candidate="$(dirname "$git_marker")"
  [ "$candidate" = "$CACHE" ] && continue
  if is_skills_checkout "$candidate"; then
    if [ "$source" != "$CACHE" ]; then
      echo "Multiple attached skills checkouts found; choose one before installing." >&2
      exit 1
    fi
    source="$candidate"
  fi
done < <(find "$USER_HOME" -mindepth 2 -maxdepth 4 -name .git \( -type d -o -type f \) -print)

run_as_user mkdir -p "$USER_HOME/.claude"
run_as_user bash "$source/bootstrap/install.sh"
printf 'Installed skills from %s\n' "$source"
