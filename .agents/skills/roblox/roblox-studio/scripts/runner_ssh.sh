#!/bin/sh
# Runs a command in the retained Tart runner over its pinned SSH key, finding the guest's address on every call.
# The runner's Studio MCP over stdio: runner_ssh.sh /Applications/RobloxStudio.app/Contents/MacOS/StudioMCP
set -eu

runner_env="$HOME/.config/roblox-studio/runner.env"

if [ ! -f "$runner_env" ]; then
  echo "Studio runner configuration not found: $runner_env" >&2
  exit 1
fi

. "$runner_env"

address="$("$ROBLOX_STUDIO_TART" ip "$ROBLOX_STUDIO_VM")"

exec ssh -T -i "$ROBLOX_STUDIO_SSH_KEY" -o IdentitiesOnly=yes \
  -o UserKnownHostsFile="$ROBLOX_STUDIO_KNOWN_HOSTS" -o StrictHostKeyChecking=yes -o BatchMode=yes \
  "$ROBLOX_STUDIO_SSH_USER@$address" "$@"
