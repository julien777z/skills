# Shared installation and source-selection helpers. Source from Bash.

is_skills_remote() {
  case "$1" in
    "$SKILLS_REMOTE"|https://github.com/julien777z/skills|git@github.com:julien777z/skills.git|git@github.com:julien777z/skills)
      return 0 ;;
    *) return 1 ;;
  esac
}

source_git() {
  if [ -n "${CLOUD_HOME:-}" ] && [ "$(id -u)" -ne 0 ]; then
    run_as_cloud_user git "$@"
  else
    git -c safe.directory='*' "$@"
  fi
}

# A refresh overlay writes `skills-overlay` into its own Git directory once it is complete.
overlay_marker() {
  local git_dir

  git_dir="$(source_git -C "$1" rev-parse --absolute-git-dir 2>/dev/null)" || return 1

  [ -f "$git_dir/skills-overlay" ] && printf '%s\n' "$git_dir/skills-overlay"
}

# Every linked worktree of a checkout, an overlay included, stands for its main checkout.
main_checkout_of() {
  local common_dir

  common_dir="$(source_git -C "$1" rev-parse --git-common-dir 2>/dev/null)" || {
    printf '%s\n' "$1"

    return
  }

  case "$common_dir" in
    /*) ;;
    *) common_dir="$1/$common_dir" ;;
  esac

  case "$common_dir" in
    */.git) (cd "${common_dir%/.git}" 2>/dev/null && pwd) || printf '%s\n' "$1" ;;
    *) printf '%s\n' "$1" ;;
  esac
}

newest_overlay() {
  local worktree marker newest="" newest_marker=""

  while IFS= read -r worktree; do
    marker="$(overlay_marker "$worktree")" || continue

    if [ -z "$newest_marker" ] || [ "$marker" -nt "$newest_marker" ]; then
      newest="$worktree"
      newest_marker="$marker"
    fi
  done < <(source_git -C "$1" worktree list --porcelain 2>/dev/null | sed -n 's/^worktree //p')

  printf '%s\n' "$newest"
}

check_link() {
  local link="$1" resolved old_root old_remote kind relative artifact

  [ -e "$link" ] || [ -L "$link" ] || return 0

  if [ ! -L "$link" ]; then
    echo "conflict: $link is a real file or directory" >&2
    return 1
  fi

  resolved="$(realpath "$link" 2>/dev/null || true)"
  [ -n "$resolved" ] || resolved="$(readlink "$link")"

  case "$resolved" in
    "$REPO_ROOT"/*) old_root="$REPO_ROOT" ;;
    "$MAIN_CHECKOUT"/*) old_root="$MAIN_CHECKOUT" ;;
    *)
      old_root="$(git -c safe.directory='*' -C "$(dirname "$resolved")" rev-parse --show-toplevel 2>/dev/null || true)"
      old_remote="$(git -c safe.directory='*' -C "$old_root" config --get remote.origin.url 2>/dev/null || true)"

      is_skills_remote "$old_remote" || old_root=""
      ;;
  esac

  kind="$(basename "$(dirname "$link")")"
  [ "${link##*/}" != AGENTS.md ] || kind=global

  if [ -n "$old_root" ]; then
    relative="${resolved#"$old_root"/}"

    case "$kind:$relative" in
      skills:.agents/skills/*|skills:.agents/.auto_generated/.*/skills/*)
        if [ ! -e "$resolved" ] || [ -f "$resolved/SKILL.md" ]; then
          return 0
        fi
        ;;
      agents:.agents/agents/*.md)
        artifact="${relative#.agents/agents/}"
        [[ "$artifact" == */* ]] || return 0
        ;;
      agents:.agents/.auto_generated/.*/agents/*.md)
        artifact="${relative#*/agents/}"
        [[ "$artifact" == */* ]] || return 0
        ;;
      rules:.agents/rules/*.md)
        artifact="${relative#.agents/rules/}"
        [[ "$artifact" == */* ]] || return 0
        ;;
      rules:.agents/.auto_generated/.*/rules/*.md|rules:.agents/.auto_generated/.*/rules/*.mdc)
        artifact="${relative#*/rules/}"
        [[ "$artifact" == */* ]] || return 0
        ;;
      rules:.agents/global.md|global:.agents/global.md|global:.agents/rules/global.md)
        return 0 ;;
      resources:.agents/resources/*)
        artifact="${relative#.agents/resources/}"

        if [[ "$artifact" != */* ]] && { [ ! -e "$resolved" ] || [ -d "$resolved" ]; }; then
          return 0
        fi
        ;;
      hooks:.agents/hooks/skills-refresh)
        return 0 ;;
    esac
  fi

  echo "conflict: $link -> $resolved is not an owned $kind artifact" >&2
  return 1
}

check_directory() {
  local directory="$1"

  while [ "$directory" != / ] && [ "$directory" != . ]; do
    if [ -L "$directory" ]; then
      echo "conflict: $directory is a symlink" >&2
      return 1
    fi

    if [ -e "$directory" ] && [ ! -d "$directory" ]; then
      echo "conflict: $directory is not a directory" >&2
      return 1
    fi

    directory="$(dirname "$directory")"
  done
}

preflight_provider() {
  local provider="$1" root="$2" skill agent rule resource name failed=0

  check_directory "$root/skills" || return 1

  [ -d "$root" ] || return 0

  while IFS= read -r skill; do
    name="${skill##*/}"

    [ "$root/skills/$name" -ef "$skill" ] || check_link "$root/skills/$name" || failed=1
  done < <(find "$CANONICAL_SKILLS" -type d -exec test -e '{}/SKILL.md' \; -print -prune | sort)

  if [ "$provider" = agents ]; then
    return "$failed"
  fi

  if [ "$provider" = codex ] || [ "$provider" = claude ]; then
    check_directory "$root/hooks" || failed=1
    check_link "$root/hooks/skills-refresh" || failed=1
  fi

  check_directory "$root/resources" || failed=1

  if [ -d "$CANONICAL_RESOURCES" ]; then
    for resource in "$CANONICAL_RESOURCES"/*; do
      [ -d "$resource" ] || continue

      name="${resource##*/}"

      check_link "$root/resources/$name" || failed=1
    done
  fi

  if { [ "$provider" = "claude" ] || [ "$provider" = "cursor" ]; } && [ -d "$CANONICAL_AGENTS" ]; then
    check_directory "$root/agents" || failed=1

    for agent in "$CANONICAL_AGENTS"/*.md; do
      [ -f "$agent" ] || continue

      name="${agent##*/}"

      check_link "$root/agents/$name" || failed=1
    done
  fi

  if [ -d "$CANONICAL_RULES" ]; then
    check_directory "$root/rules" || failed=1

    for rule in "$CANONICAL_RULES"/*.md; do
      [ -f "$rule" ] || continue

      name="${rule##*/}"

      if [ "$provider" = "cursor" ]; then
        name="${name%.md}.mdc"
      fi

      check_link "$root/rules/$name" || failed=1
    done
  fi

  if { [ "$provider" = "claude" ] || [ "$provider" = "cursor" ]; } && [ "$CANONICAL_GLOBAL" != "$CANONICAL_RULES/global.md" ]; then
    check_directory "$root/rules" || failed=1

    name="global.md"
    if [ "$provider" = "cursor" ]; then
      name="global.mdc"
    fi

    check_link "$root/rules/$name" || failed=1
  fi

  if [ "$provider" = "codex" ] && { [ -e "$root/AGENTS.md" ] || [ -L "$root/AGENTS.md" ]; }; then
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
  local dir="$1" link

  for link in "$dir"/*; do
    [ -L "$link" ] || continue

    case "$expected_links" in
      *"|$link|"*) continue ;;
    esac

    if check_link "$link" >/dev/null 2>&1; then
      remove_link "$link"
    fi
  done
}

install_provider() {
  local provider="$1" root="$2" skill agent rule resource name skills=0 agents=0 rules=0 resources=0

  if [ ! -d "$root" ]; then
    install_changed=1

    if [ "$INSTALL_MODE" = check ]; then
      return
    fi
  fi

  found_root=1
  expected_links=""

  [ "$INSTALL_MODE" = check ] || mkdir -p "$root/skills"

  while IFS= read -r skill; do
    name="${skill##*/}"

    install_link "$(link_source "$provider" skills "$name" "$skill")" "$root/skills/$name"
    skills=$((skills + 1))
  done < <(find "$CANONICAL_SKILLS" -type d -exec test -e '{}/SKILL.md' \; -print -prune | sort)

  prune_links "$root/skills"

  if [ "$provider" = agents ]; then
    [ "$INSTALL_MODE" = check ] || echo "$root: $skills skills linked"

    return
  fi

  if [ -d "$CANONICAL_RESOURCES" ]; then
    [ "$INSTALL_MODE" = check ] || mkdir -p "$root/resources"

    for resource in "$CANONICAL_RESOURCES"/*; do
      [ -d "$resource" ] || continue

      name="${resource##*/}"

      install_link "$resource" "$root/resources/$name"
      resources=$((resources + 1))
    done

  fi

  prune_links "$root/resources"

  if { [ "$provider" = "claude" ] || [ "$provider" = "cursor" ]; } && [ -d "$CANONICAL_AGENTS" ]; then
    [ "$INSTALL_MODE" = check ] || mkdir -p "$root/agents"

    for agent in "$CANONICAL_AGENTS"/*.md; do
      [ -f "$agent" ] || continue

      name="${agent##*/}"

      install_link "$(link_source "$provider" agents "$name" "$agent")" "$root/agents/$name"
      agents=$((agents + 1))
    done

    prune_links "$root/agents"
  fi

  if [ -d "$CANONICAL_RULES" ]; then
    [ "$INSTALL_MODE" = check ] || mkdir -p "$root/rules"

    for rule in "$CANONICAL_RULES"/*.md; do
      [ -f "$rule" ] || continue

      name="${rule##*/}"

      if [ "$provider" = "cursor" ]; then name="${name%.md}.mdc"; fi

      install_link "$(link_source "$provider" rules "$name" "$rule")" "$root/rules/$name"
      rules=$((rules + 1))
    done

  fi

  if { [ "$provider" = "claude" ] || [ "$provider" = "cursor" ]; } && [ "$CANONICAL_GLOBAL" != "$CANONICAL_RULES/global.md" ]; then
    name="global.md"
    if [ "$provider" = "cursor" ]; then name="global.mdc"; fi

    install_link "$CANONICAL_GLOBAL" "$root/rules/$name"
    rules=$((rules + 1))
  fi

  prune_links "$root/rules"

  if [ "$provider" = "codex" ]; then
    install_link "$CANONICAL_GLOBAL" "$root/AGENTS.md"
  fi

  [ "$INSTALL_MODE" = check ] || echo "$root: $skills skills, $agents agents, $rules rules, $resources resources linked"

  if [ "$provider" = codex ] || [ "$provider" = claude ]; then
    [ "$INSTALL_MODE" = check ] || mkdir -p "$root/hooks"
    install_link "$REPO_ROOT/.agents/hooks/skills-refresh" "$root/hooks/skills-refresh"

    python3 "$REPO_ROOT/.agents/hooks/skills-refresh/configuration.py" "$INSTALL_MODE" "$provider" "$root" "$REPO_ROOT" "${CLOUD_HOME:-}" "$AUTO_UPDATE" || {
      [ "$?" -eq 3 ] || return 1
      install_changed=1
    }
  fi
}


install_link() {
  local source="$1" destination="$2"
  expected_links="$expected_links|$destination|"

  if [ -L "$destination" ] && [ "$destination" -ef "$source" ]; then
    return 0
  fi

  install_changed=1

  if [ "$INSTALL_MODE" = apply ]; then
    ln -sfn "$source" "$destination"
  fi
}

remove_link() {
  install_changed=1

  if [ "$INSTALL_MODE" = apply ]; then
    rm -f "$1"
  fi
}
