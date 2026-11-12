#!/bin/sh
# Runs a command in the game's Tart runner over its pinned SSH key, finding the guest's address on every call.
# The game is ROBLOX_STUDIO_GAME, or else the repository the command runs in, named by its main checkout's folder.
# games/<game>.env names the game's VM, conventionally <game>-vm; its configured name is the lock key.
# ROBLOX_STUDIO_EXPECTED_VM, when set, refuses the call unless the game's file still names that VM.
# The runner's Studio MCP over stdio: runner_ssh.sh /Applications/RobloxStudio.app/Contents/MacOS/StudioMCP
# `runner_ssh.sh --describe` prints the game's resolved runner configuration as shell assignments instead.
set -eu

config_dir="$HOME/.config/roblox-studio"
runner_env="$config_dir/runner.env"

if [ ! -f "$runner_env" ]; then
  echo "Studio runner configuration not found: $runner_env" >&2
  exit 1
fi

if [ -z "${ROBLOX_STUDIO_GAME:-}" ]; then
  if ! common_dir="$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null)"; then
    echo "Run inside the game's repository or set ROBLOX_STUDIO_GAME" >&2
    exit 1
  fi

  if [ "$(basename "$common_dir")" != ".git" ]; then
    echo "Cannot name the game from $common_dir; set ROBLOX_STUDIO_GAME" >&2
    exit 1
  fi

  ROBLOX_STUDIO_GAME="$(basename "$(dirname "$common_dir")")"
fi

case "$ROBLOX_STUDIO_GAME" in
  '' | [._-]* | *[!A-Za-z0-9._-]*)
    echo "Game names use letters, digits, '.', '_' and '-', starting with a letter or digit: $ROBLOX_STUDIO_GAME" >&2
    exit 1
    ;;
esac

game_env="$config_dir/games/$ROBLOX_STUDIO_GAME.env"

if [ ! -f "$game_env" ]; then
  echo "No runner VM is configured for $ROBLOX_STUDIO_GAME: $game_env" >&2
  exit 1
fi

expected_vm="${ROBLOX_STUDIO_EXPECTED_VM:-}"

. "$runner_env"

# The game's file names its own VM and host keys; the shared file's values for them never apply.
unset ROBLOX_STUDIO_VM ROBLOX_STUDIO_KNOWN_HOSTS
. "$game_env"

: "${ROBLOX_STUDIO_TART:?$runner_env sets no ROBLOX_STUDIO_TART}"
: "${ROBLOX_STUDIO_SSH_USER:?$runner_env sets no ROBLOX_STUDIO_SSH_USER}"
: "${ROBLOX_STUDIO_SSH_KEY:?$runner_env sets no ROBLOX_STUDIO_SSH_KEY}"
: "${ROBLOX_STUDIO_VM:?$game_env sets no ROBLOX_STUDIO_VM}"
: "${ROBLOX_STUDIO_KNOWN_HOSTS:?$game_env sets no ROBLOX_STUDIO_KNOWN_HOSTS}"

if [ -n "$expected_vm" ] && [ "$expected_vm" != "$ROBLOX_STUDIO_VM" ]; then
  echo "$game_env now names $ROBLOX_STUDIO_VM, not the locked $expected_vm" >&2
  exit 1
fi

if [ "${1:-}" = "--describe" ]; then
  for name in ROBLOX_STUDIO_GAME ROBLOX_STUDIO_TART ROBLOX_STUDIO_VM ROBLOX_STUDIO_SSH_USER ROBLOX_STUDIO_SSH_KEY \
    ROBLOX_STUDIO_KNOWN_HOSTS; do
    eval "value=\$$name"
    printf "%s='%s'\n" "$name" "$(printf '%s' "$value" | sed "s/'/'\\\\''/g")"
  done

  exit 0
fi

address="$("$ROBLOX_STUDIO_TART" ip "$ROBLOX_STUDIO_VM")"

exec ssh -T -i "$ROBLOX_STUDIO_SSH_KEY" -o IdentitiesOnly=yes \
  -o UserKnownHostsFile="$ROBLOX_STUDIO_KNOWN_HOSTS" -o StrictHostKeyChecking=yes -o BatchMode=yes \
  "$ROBLOX_STUDIO_SSH_USER@$address" "$@"
