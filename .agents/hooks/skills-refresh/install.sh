#!/usr/bin/env bash
set -euo pipefail

SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
REPO_ROOT="$SOURCE_ROOT"
INSTALLER_DIR="$SOURCE_ROOT/bootstrap"
origin_lines="$(python3 "$SOURCE_ROOT/.agents/hooks/skills-refresh/session_start.py" --origins)"
SKILLS_REMOTES=()

while IFS= read -r origin; do
  SKILLS_REMOTES+=("$origin")
done <<< "$origin_lines"

readonly SKILLS_REMOTE="${SKILLS_REMOTES[0]:?Missing shared skills origins}"
INSTALL_MODE=apply
LOCAL_ONLY=0
RESOLVE_SOURCE=0
SELECTED_SOURCE=""
AUTO_UPDATE=0
INSTALL_ARGUMENTS=("$@")

while [ "$#" -gt 0 ]; do
  case "$1" in
    --check) INSTALL_MODE=check ;;
    --local-only) LOCAL_ONLY=1 ;;
    --auto-update) AUTO_UPDATE=1 ;;
    --resolve-source) RESOLVE_SOURCE=1; LOCAL_ONLY=1 ;;
    --source)
      shift
      SELECTED_SOURCE="${1:?--source requires a selected checkout}"
      ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done

reexecuted=0

if IFS= read -r -u 9 reexec_root 2>/dev/null && [ "$reexec_root" = "$REPO_ROOT" ]; then
  reexecuted=1
fi

source "$SOURCE_ROOT/.agents/hooks/skills-refresh/installation.sh"

if [ -n "${SKILLS_CLOUD_HOME:-}" ]; then
  REPO_ROOT="$SKILLS_CLOUD_HOME/.local/share/agent-skills"
fi

if [[ "$REPO_ROOT" == */.local/share/agent-skills ]]; then
  CLOUD_HOME="${REPO_ROOT%/.local/share/agent-skills}"
  CLOUD_CLAUDE_HOME=""

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
      remote="$(git -c "safe.directory=$1" -C "$1" config --get remote.origin.url 2>/dev/null || true)"
    else
      remote="$(run_as_cloud_user git -C "$1" config --get remote.origin.url 2>/dev/null || true)"
    fi

    is_skills_remote "$remote"
  }

  is_skills_checkout "$REPO_ROOT" || { echo "Setup clone is not the skills repository: $REPO_ROOT" >&2; exit 1; }

  if [ "$reexecuted" -eq 0 ] && [ "$LOCAL_ONLY" -eq 0 ]; then
    if [ -n "$(run_as_cloud_user git -C "$REPO_ROOT" status --porcelain)" ]; then
      echo "Skills setup clone has local edits; refusing to overwrite them: $REPO_ROOT" >&2
      exit 1
    fi

    cloud_branch="$(run_as_cloud_user git -C "$REPO_ROOT" symbolic-ref --quiet --short HEAD)" || {
      echo "Skills setup clone must be on a branch: $REPO_ROOT" >&2
      exit 1
    }

    installer_blob="$(run_as_cloud_user git -C "$REPO_ROOT" rev-parse HEAD:bootstrap/install.sh HEAD:.agents/hooks/skills-refresh)"

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

    if [ "$installer_blob" != "$(run_as_cloud_user git -C "$REPO_ROOT" rev-parse HEAD:bootstrap/install.sh HEAD:.agents/hooks/skills-refresh)" ]; then
      if [ -n "${staged_ca:-}" ]; then
        rm -f "$staged_ca"
        trap - EXIT
      fi

      reexec_marker="$(mktemp)"
      printf '%s\n' "$REPO_ROOT" > "$reexec_marker"

      exec 9<"$reexec_marker"
      rm -f "$reexec_marker"

      exec bash "$REPO_ROOT/bootstrap/install.sh" "${INSTALL_ARGUMENTS[@]}"
    fi
  fi

  if [ -z "$SELECTED_SOURCE" ] && [ "$RESOLVE_SOURCE" -eq 0 ]; then
    source_checkout="$REPO_ROOT"
    search_roots=("$CLOUD_HOME")
    declare -A seen_checkouts=()

    current_checkout="$(git -c safe.directory='*' -C "$PWD" rev-parse --show-toplevel 2>/dev/null || true)"

    if [ -n "$current_checkout" ]; then
      current_checkout="$(main_checkout_of "$current_checkout")"
    fi

    if [ -n "$current_checkout" ] && [ "$current_checkout" != "$REPO_ROOT" ] && is_skills_checkout "$current_checkout"; then
      seen_checkouts["$current_checkout"]=1
      source_checkout="$current_checkout"
    fi

    if [ "$PWD" != "$CLOUD_HOME" ]; then
      search_roots+=("$PWD")
    fi

    if [ "$CLOUD_HOME" = /home/claude ] && [ -d /home/user ]; then
      search_roots+=(/home/user)
    fi

    for search_root in "${search_roots[@]}"; do
      while IFS= read -r git_marker; do
        candidate="$(main_checkout_of "$(dirname "$git_marker")")"

        [ "$candidate" = "$REPO_ROOT" ] && continue
        [ -z "${seen_checkouts[$candidate]:-}" ] || continue
        seen_checkouts["$candidate"]=1

        if is_skills_checkout "$candidate"; then
          if [ "$source_checkout" != "$REPO_ROOT" ]; then
            echo "Multiple attached skills checkouts found; choose one before installing." >&2
            exit 1
          fi

          source_checkout="$candidate"
        fi
      done < <(find "$search_root" -mindepth 1 -maxdepth 4 -name .git \( -type d -o -type f \) -print)
    done

    REPO_ROOT="$source_checkout"
  fi
fi

if [ "$RESOLVE_SOURCE" -eq 1 ]; then
  REPO_ROOT="$SOURCE_ROOT"
fi

if [ -n "$SELECTED_SOURCE" ]; then
  REPO_ROOT="$SELECTED_SOURCE"
else
  overlay_root="$(newest_overlay "$REPO_ROOT")"

  if [ -n "$overlay_root" ]; then
    if [ "$INSTALL_MODE" != check ] && [ "$RESOLVE_SOURCE" -eq 0 ]; then
      echo "Using the refresh overlay $overlay_root; update-skills rebuilds it from the latest default branch."
    fi
    REPO_ROOT="$overlay_root"
  fi
fi

if [ "$RESOLVE_SOURCE" -eq 1 ]; then
  printf '%s\n' "$REPO_ROOT"
  exit 0
fi

MAIN_CHECKOUT="$(main_checkout_of "$REPO_ROOT")"
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

  if [ ! -d "$CLOUD_HOME/.codex" ]; then
    CLOUD_CLAUDE_HOME="$CLOUD_HOME"
  fi

  if [ -n "$CLOUD_CLAUDE_HOME" ] && [ "$(id -u)" -eq 0 ] && [ "$CLOUD_HOME" != "$HOME" ]; then
    # Claude starts as root, though its setup checkout belongs to the claude user.
    TARGET_HOMES+=("$HOME")
  fi
fi

INSTALL_PROVIDERS=()
INSTALL_ROOTS=()

add_install_root() {
  local provider="$1" root="$2" index

  for index in "${!INSTALL_ROOTS[@]}"; do
    if [ "${INSTALL_PROVIDERS[$index]}" = "$provider" ] && [ "${INSTALL_ROOTS[$index]}" = "$root" ]; then
      return
    fi
  done

  INSTALL_PROVIDERS+=("$provider")
  INSTALL_ROOTS+=("$root")
}

for target_home in "${TARGET_HOMES[@]}"; do
  for provider in "${PROVIDERS[@]}"; do
    root="$target_home/.$provider"

    [ -d "$root" ] || continue

    add_install_root "$provider" "$root"
  done

  if [ -n "${CLOUD_CLAUDE_HOME:-}" ] && { [ "$target_home" = "$CLOUD_CLAUDE_HOME" ] || [ "$target_home" = "$HOME" ]; }; then
    add_install_root claude "$target_home/.claude"
  fi

  # Codex discovers user skills here even when its runtime home is ephemeral.
  if [ -d "$target_home/.agents" ] || [ -d "$target_home/.codex" ] || { [ -n "${CODEX_HOME:-}" ] && { [ "$target_home" = "$HOME" ] || [ "$target_home" = "${CLOUD_HOME:-}" ]; }; }; then
    add_install_root agents "$target_home/.agents"
  fi
done

if [ -n "${CODEX_HOME:-}" ]; then
  add_install_root codex "$CODEX_HOME"
fi

if [ -n "${CLAUDE_CONFIG_DIR:-}" ]; then
  add_install_root claude "$CLAUDE_CONFIG_DIR"
fi

preflight_ok=1

for index in "${!INSTALL_ROOTS[@]}"; do
  preflight_provider "${INSTALL_PROVIDERS[$index]}" "${INSTALL_ROOTS[$index]}" || preflight_ok=0

  if [ "${INSTALL_PROVIDERS[$index]}" = codex ] || [ "${INSTALL_PROVIDERS[$index]}" = claude ]; then
    python3 "$REPO_ROOT/.agents/hooks/skills-refresh/configuration.py" preflight "${INSTALL_PROVIDERS[$index]}" "${INSTALL_ROOTS[$index]}" "$REPO_ROOT" "${CLOUD_HOME:-}" "$AUTO_UPDATE" || preflight_ok=0
  fi
done

if [ "$preflight_ok" -eq 0 ]; then
  echo "Resolve the listed skill conflicts before installing; no links were changed." >&2
  exit 1
fi

install_changed=0

for index in "${!INSTALL_ROOTS[@]}"; do
  [ "$INSTALL_MODE" = check ] || mkdir -p "${INSTALL_ROOTS[$index]}"
  install_provider "${INSTALL_PROVIDERS[$index]}" "${INSTALL_ROOTS[$index]}"
done

if [ "$INSTALL_MODE" = check ]; then
  [ "$install_changed" -eq 0 ] || exit 3
  exit 0
fi

if [ "$found_root" -eq 0 ]; then
  echo "No user-level agent root found (looked for .claude, .codex, .cursor); nothing linked."
else
  echo "Installed skills from $REPO_ROOT"
fi

if [ "$LOCAL_ONLY" -eq 0 ] && [ "${CLOUD_HOME:-}" = /home/claude ]; then
  bash "$INSTALLER_DIR/resources/install_pass_cli.sh"
fi
