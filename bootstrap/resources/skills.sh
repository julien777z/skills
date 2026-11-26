# Hidden provider packages are outside the user catalog. Claude also owns the skills it syncs from
# an account and the one a cloud session supplies.
CLAUDE_OWNED_SKILLS='synced session-start-hook'

protected_skill() {
  local provider="$1" name="$2" root="$3" path_helper="$4"
  local entry_key lowered owned owned_key

  case "$name" in
    .*) return 0 ;;
  esac

  [ "$provider" = claude ] || return 1

  lowered="$(printf '%s' "$name" | tr '[:upper:]' '[:lower:]')"

  for owned in $CLAUDE_OWNED_SKILLS; do
    [ "$lowered" = "$owned" ] || continue

    entry_key="$(python3 "$path_helper" "$root/skills/$name" --entry)" || return 0
    owned_key="$(python3 "$path_helper" "$root/skills/$owned" --entry)" || return 0

    [ "$entry_key" = "$owned_key" ] && return 0
  done

  return 1
}

preflight_skill_reconciliation() {
  local skills_root="$1" destination_parent source

  shift

  destination_parent="$skills_root"

  while [ ! -d "$destination_parent" ]; do
    destination_parent="$(dirname -- "$destination_parent")"
  done

  if [ ! -x "$destination_parent" ] || [ ! -w "$destination_parent" ]; then
    printf 'Cannot write skills directory: %s\n' "$skills_root" >&2
    return 1
  fi

  if [ -d "$skills_root" ] && { [ ! -x "$skills_root" ] || ! ls -A -- "$skills_root" >/dev/null; }; then
    printf 'Cannot list skills directory: %s\n' "$skills_root" >&2
    return 1
  fi

  for source in "$@"; do
    if [ ! -f "$source/SKILL.md" ] || [ ! -r "$source/SKILL.md" ]; then
      printf 'Unreadable skill source: %s\n' "$source/SKILL.md" >&2
      return 1
    fi
  done
}

reconcile_skill_links() {
  local provider="$1" root="$2" path_helper="$3"
  local entry expected found name source
  local desired_links=()

  shift 3

  if [ "$(( $# % 2 ))" -ne 0 ]; then
    printf '%s\n' 'Expected skill name and source pairs' >&2
    return 1
  fi

  while [ "$#" -gt 0 ]; do
    name="$1"
    source="$2"

    case "$name" in
      ""|.|..|*/*)
        printf 'Invalid skill name: %s\n' "$name" >&2
        return 1
        ;;
    esac

    if protected_skill "$provider" "$name" "$root" "$path_helper"; then
      printf 'Cannot replace protected skill: %s\n' "$name" >&2
      return 1
    fi

    desired_links+=("$name" "$source")
    shift 2
  done

  mkdir -p "$root/skills" || return 1

  # Prune first so a differently cased alias can be replaced with its canonical spelling.
  for entry in "$root/skills"/*; do
    [ -e "$entry" ] || [ -L "$entry" ] || continue
    protected_skill "$provider" "${entry##*/}" "$root" "$path_helper" && continue
    found=0
    set -- ${desired_links[@]+"${desired_links[@]}"}

    while [ "$#" -gt 0 ]; do
      expected="$root/skills/$1"

      if [ "$entry" = "$expected" ]; then
        found=1
        break
      fi

      shift 2
    done

    [ "$found" -eq 0 ] || continue
    rm -rf -- "$entry" || return 1
  done

  set -- ${desired_links[@]+"${desired_links[@]}"}

  while [ "$#" -gt 0 ]; do
    entry="$root/skills/$1"
    source="$2"
    shift 2

    if [ -e "$source/tests" ] || [ -L "$source/tests" ]; then
      link_skill_without_scenarios "$source" "$entry" || return 1
      continue
    fi

    if [ -L "$entry" ] && [ "$(readlink "$entry")" = "$source" ]; then
      continue
    fi

    if [ -L "$entry" ] || [ -e "$entry" ]; then
      rm -rf -- "$entry" || return 1
    fi

    ln -s "$source" "$entry" || return 1
  done
}

# A skill's top-level `tests/` holds regression scenarios with their expected answers, so the
# installed skill is a directory linking every other top-level entry.
link_skill_without_scenarios() {
  local source="$1" entry="$2" item name
  local expected=()

  for item in "$source"/* "$source"/.[!.]* "$source"/..?*; do
    [ -e "$item" ] || [ -L "$item" ] || continue
    name="${item##*/}"
    [ "$name" = tests ] && continue
    expected+=("$name")
  done

  if skill_links_match "$source" "$entry" ${expected[@]+"${expected[@]}"}; then
    return 0
  fi

  if [ -L "$entry" ] || [ -e "$entry" ]; then
    rm -rf -- "$entry" || return 1
  fi

  mkdir "$entry" || return 1

  for name in ${expected[@]+"${expected[@]}"}; do
    ln -s "$source/$name" "$entry/$name" || return 1
  done
}

skill_links_match() {
  local source="$1" entry="$2" item name count=0

  shift 2

  [ -d "$entry" ] && [ ! -L "$entry" ] || return 1

  for name in "$@"; do
    [ -L "$entry/$name" ] && [ "$(readlink "$entry/$name")" = "$source/$name" ] || return 1
  done

  for item in "$entry"/* "$entry"/.[!.]* "$entry"/..?*; do
    [ -e "$item" ] || [ -L "$item" ] || continue
    count=$((count + 1))
  done

  [ "$count" -eq "$#" ]
}
