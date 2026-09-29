#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_REMOTE='https://github.com/julien777z/skills.git'

if [[ "$REPO_ROOT" == */.local/share/agent-skills ]]; then
  CLOUD_HOME="${REPO_ROOT%/.local/share/agent-skills}"
  if [ -n "${SKILLS_CLOUD_HOME:-}" ] && [ "$SKILLS_CLOUD_HOME" != "$CLOUD_HOME" ]; then
    echo "Cloud setup clone is outside SKILLS_CLOUD_HOME: $REPO_ROOT" >&2
    exit 1
  fi
  [ -d "$REPO_ROOT/.git" ] || { echo "Missing skills setup clone: $REPO_ROOT" >&2; exit 1; }

  run_as_cloud_user() {
    if [ "$(id -u)" -eq 0 ]; then
      local owner

      owner="$(stat -c %U "$CLOUD_HOME")"

      if [ "$owner" != root ]; then
        runuser -u "$owner" -- env HOME="$CLOUD_HOME" "$@"

        return
      fi
    fi
    env HOME="$CLOUD_HOME" "$@"
  }

  is_skills_checkout() {
    local remote

    if [ "$(id -u)" -eq 0 ]; then
      # Attached Claude checkouts belong to the session user, not the setup-clone owner.
      remote="$(git -c "safe.directory=$1" -C "$1" remote get-url origin 2>/dev/null || true)"
    else
      remote="$(run_as_cloud_user git -C "$1" remote get-url origin 2>/dev/null || true)"
    fi

    case "$remote" in
      "$SKILLS_REMOTE"|https://github.com/julien777z/skills|git@github.com:julien777z/skills.git|git@github.com:julien777z/skills)
        return 0 ;;
      *) return 1 ;;
    esac
  }

  is_skills_checkout "$REPO_ROOT" || { echo "Setup clone is not the skills repository: $REPO_ROOT" >&2; exit 1; }
  if [ "${SKILLS_INSTALL_UPDATED:-0}" != 1 ]; then
    if [ -n "$(run_as_cloud_user git -C "$REPO_ROOT" status --porcelain)" ]; then
      echo "Skills setup clone has local edits; refusing to overwrite them: $REPO_ROOT" >&2
      exit 1
    fi

    cloud_branch="$(run_as_cloud_user git -C "$REPO_ROOT" symbolic-ref --quiet --short HEAD)" || {
      echo "Skills setup clone must be on a branch: $REPO_ROOT" >&2
      exit 1
    }
    installer_blob="$(run_as_cloud_user git -C "$REPO_ROOT" rev-parse HEAD:bootstrap/install.sh)"

    # Claude's proxy may configure a CA bundle under /root that the clone owner cannot read.
    fetch_env=()
    ca_bundle="${GIT_SSL_CAINFO:-$(git config --get-urlmatch http.sslCAInfo "$SKILLS_REMOTE" || true)}"
    ca_bundle="${ca_bundle:-${SSL_CERT_FILE:-}}"
    if [ "$(id -u)" -eq 0 ] && [ -n "$ca_bundle" ] && [ -r "$ca_bundle" ]; then
      if ! run_as_cloud_user test -r "$ca_bundle"; then
        staged_ca="$(mktemp)"
        trap 'rm -f "$staged_ca"' EXIT
        install -m 0644 "$ca_bundle" "$staged_ca"
        ca_bundle="$staged_ca"
      fi
      fetch_env=(GIT_SSL_CAINFO="$ca_bundle" SSL_CERT_FILE="$ca_bundle")
    fi

    run_as_cloud_user env ${fetch_env[@]+"${fetch_env[@]}"} git -C "$REPO_ROOT" fetch origin "$cloud_branch"
    run_as_cloud_user git -C "$REPO_ROOT" merge --ff-only "origin/$cloud_branch"

    if [ "$installer_blob" != "$(run_as_cloud_user git -C "$REPO_ROOT" rev-parse HEAD:bootstrap/install.sh)" ]; then
      if [ -n "${staged_ca:-}" ]; then
        rm -f "$staged_ca"
        trap - EXIT
      fi
      SKILLS_INSTALL_UPDATED=1 exec bash "$REPO_ROOT/bootstrap/install.sh"
    fi
  fi

  source_checkout="$REPO_ROOT"
  search_roots=("$CLOUD_HOME")
  if [ "$CLOUD_HOME" = /home/claude ] && [ -d /home/user ]; then
    search_roots+=(/home/user)
  fi
  for search_root in "${search_roots[@]}"; do
    while IFS= read -r git_marker; do
      candidate="$(dirname "$git_marker")"
      [ "$candidate" = "$REPO_ROOT" ] && continue
      if is_skills_checkout "$candidate"; then
        if [ "$source_checkout" != "$REPO_ROOT" ]; then
          echo "Multiple attached skills checkouts found; choose one before installing." >&2
          exit 1
        fi
        source_checkout="$candidate"
      fi
    done < <(find "$search_root" -mindepth 2 -maxdepth 4 -name .git \( -type d -o -type f \) -print)
  done

  REPO_ROOT="$source_checkout"
fi

CANONICAL_SKILLS="$REPO_ROOT/.agents/skills"
CANONICAL_AGENTS="$REPO_ROOT/.agents/agents"
CANONICAL_RULES="$REPO_ROOT/.agents/rules"
CANONICAL_GLOBAL="$REPO_ROOT/.agents/global.md"
if [ ! -f "$CANONICAL_GLOBAL" ]; then
  CANONICAL_GLOBAL="$CANONICAL_RULES/global.md"
fi
CANONICAL_RESOURCES="$REPO_ROOT/.agents/resources"
GENERATED_ROOT="$REPO_ROOT/.agents/.auto_generated"
PROVIDERS=(claude codex cursor)
found_root=0
TARGET_HOMES=("$HOME")
if [ -n "${CLOUD_HOME:-}" ]; then
  TARGET_HOMES=("$CLOUD_HOME")
  if [ "$(id -u)" -eq 0 ] && [ "$CLOUD_HOME" != /root ] && [ -d "$CLOUD_HOME/.claude" ]; then
    # Claude starts as root, though its setup checkout belongs to the claude user.
    mkdir -p /root/.claude
    TARGET_HOMES+=(/root)
  fi
fi

check_link() {
  local link="$1" resolved old_root old_remote

  [ -e "$link" ] || [ -L "$link" ] || return 0

  if [ ! -L "$link" ]; then
    echo "conflict: $link is a real file or directory" >&2
    return 1
  fi

  resolved="$(realpath "$link" 2>/dev/null || true)"
  [ -n "$resolved" ] || resolved="$(readlink "$link")"

  case "$resolved" in
    "$REPO_ROOT"/*) return 0 ;;
  esac

  old_root="$(git -c safe.directory='*' -C "$(dirname "$resolved")" rev-parse --show-toplevel 2>/dev/null || true)"
  old_remote="$(git -c safe.directory='*' -C "$old_root" remote get-url origin 2>/dev/null || true)"

  case "$old_remote:$resolved" in
    https://github.com/julien777z/skills.git:"$old_root"/.agents/*|\
    https://github.com/julien777z/skills.git:"$old_root"/bootstrap/*|\
    https://github.com/julien777z/skills:"$old_root"/.agents/*|\
    https://github.com/julien777z/skills:"$old_root"/bootstrap/*|\
    git@github.com:julien777z/skills.git:"$old_root"/.agents/*|\
    git@github.com:julien777z/skills.git:"$old_root"/bootstrap/*)
      return 0 ;;
  esac

  echo "conflict: $link points outside $REPO_ROOT" >&2
  return 1
}

preflight_provider() {
  local provider="$1" root="$2/.$provider" skill agent rule resource name failed=0

  [ -d "$root" ] || return 0

  while IFS= read -r skill; do
    name="$(basename "$skill")"
    check_link "$root/skills/$name" || failed=1
  done < <(find "$CANONICAL_SKILLS" -type d -exec test -e '{}/SKILL.md' \; -print -prune | sort)

  if [ -d "$CANONICAL_RESOURCES" ]; then
    for resource in "$CANONICAL_RESOURCES"/*; do
      [ -d "$resource" ] || continue
      name="$(basename "$resource")"
      check_link "$root/resources/$name" || failed=1
    done
  fi

  if { [ "$provider" = "claude" ] || [ "$provider" = "cursor" ]; } && [ -d "$CANONICAL_AGENTS" ]; then
    for agent in "$CANONICAL_AGENTS"/*.md; do
      [ -f "$agent" ] || continue
      name="$(basename "$agent")"
      check_link "$root/agents/$name" || failed=1
    done
  fi

  if [ -d "$CANONICAL_RULES" ]; then
    for rule in "$CANONICAL_RULES"/*.md; do
      [ -f "$rule" ] || continue
      name="$(basename "$rule")"
      if [ "$provider" = "cursor" ]; then name="${name%.md}.mdc"; fi
      check_link "$root/rules/$name" || failed=1
    done
  fi

  if { [ "$provider" = "claude" ] || [ "$provider" = "cursor" ]; } && [ "$CANONICAL_GLOBAL" != "$CANONICAL_RULES/global.md" ]; then
    name="global.md"
    if [ "$provider" = "cursor" ]; then name="global.mdc"; fi
    check_link "$root/rules/$name" || failed=1
  fi

  if [ "$provider" = "codex" ] && { [ -L "$root/AGENTS.md" ] || [ -s "$root/AGENTS.md" ]; }; then
    check_link "$root/AGENTS.md" || failed=1
  fi

  [ "$failed" -eq 0 ]
}

link_source() {
  local provider="$1" kind="$2" name="$3" canonical="$4"
  local mirror="$GENERATED_ROOT/.$provider/$kind/$name"

  if [ -e "$mirror" ]; then
    printf '%s\n' "$mirror"
  else
    printf '%s\n' "$canonical"
  fi
}

prune_links() {
  local dir="$1" link target old_root relative

  for link in "$dir"/*; do
    [ -L "$link" ] || continue

    target="$(readlink "$link")"

    case "$target" in
      "$REPO_ROOT"/*) [ -e "$link" ] || rm -f "$link" ;;
      *)
        check_link "$link" >/dev/null 2>&1 || continue

        old_root="$(git -c safe.directory='*' -C "$(dirname "$target")" rev-parse --show-toplevel 2>/dev/null || true)"
        [ -n "$old_root" ] || continue

        relative="${target#"$old_root"/}"
        [ -e "$REPO_ROOT/$relative" ] || rm -f "$link"
        ;;
    esac
  done
}

install_provider() {
  local provider="$1" root="$2/.$provider" skill agent rule resource name skills=0 agents=0 rules=0 resources=0

  [ -d "$root" ] || return 0

  found_root=1

  mkdir -p "$root/skills"
  while IFS= read -r skill; do
    name="$(basename "$skill")"
    ln -sfn "$(link_source "$provider" skills "$name" "$skill")" "$root/skills/$name"
    skills=$((skills + 1))
  done < <(find "$CANONICAL_SKILLS" -type d -exec test -e '{}/SKILL.md' \; -print -prune | sort)
  prune_links "$root/skills"

  if [ -d "$CANONICAL_RESOURCES" ]; then
    mkdir -p "$root/resources"
    for resource in "$CANONICAL_RESOURCES"/*; do
      [ -d "$resource" ] || continue
      name="$(basename "$resource")"
      ln -sfn "$resource" "$root/resources/$name"
      resources=$((resources + 1))
    done
  fi
  prune_links "$root/resources"

  if { [ "$provider" = "claude" ] || [ "$provider" = "cursor" ]; } && [ -d "$CANONICAL_AGENTS" ]; then
    mkdir -p "$root/agents"
    for agent in "$CANONICAL_AGENTS"/*.md; do
      [ -f "$agent" ] || continue
      name="$(basename "$agent")"
      ln -sfn "$(link_source "$provider" agents "$name" "$agent")" "$root/agents/$name"
      agents=$((agents + 1))
    done
    prune_links "$root/agents"
  fi

  if [ -d "$CANONICAL_RULES" ]; then
    mkdir -p "$root/rules"
    for rule in "$CANONICAL_RULES"/*.md; do
      [ -f "$rule" ] || continue
      name="$(basename "$rule")"
      if [ "$provider" = "cursor" ]; then name="${name%.md}.mdc"; fi
      ln -sfn "$(link_source "$provider" rules "$name" "$rule")" "$root/rules/$name"
      rules=$((rules + 1))
    done
    prune_links "$root/rules"
  fi
  if { [ "$provider" = "claude" ] || [ "$provider" = "cursor" ]; } && [ "$CANONICAL_GLOBAL" != "$CANONICAL_RULES/global.md" ]; then
    name="global.md"
    if [ "$provider" = "cursor" ]; then name="global.mdc"; fi
    ln -sfn "$CANONICAL_GLOBAL" "$root/rules/$name"
    rules=$((rules + 1))
  fi
  if [ "$provider" = "codex" ]; then
    ln -sfn "$CANONICAL_GLOBAL" "$root/AGENTS.md"
  fi

  echo "$root: $skills skills, $agents agents, $rules rules, $resources resources linked"
}

preflight_ok=1
for target_home in "${TARGET_HOMES[@]}"; do
  for provider in "${PROVIDERS[@]}"; do
    preflight_provider "$provider" "$target_home" || preflight_ok=0
  done
done
if [ "$preflight_ok" -eq 0 ]; then
  echo "Resolve the listed skill conflicts before installing; no links were changed." >&2
  exit 1
fi

for target_home in "${TARGET_HOMES[@]}"; do
  for provider in "${PROVIDERS[@]}"; do
    install_provider "$provider" "$target_home"
  done
done

if [ "$found_root" -eq 0 ]; then
  echo "No user-level agent root found (looked for .claude, .codex, .cursor); nothing linked."
else
  echo "Installed skills from $REPO_ROOT"
fi
