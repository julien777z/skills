#!/usr/bin/env bash
set -euo pipefail

readonly INSTALL_DIR=/usr/local/bin
readonly INSTALLER_URL='https://proton.me/download/pass-cli/install.sh'

if [ -x "$INSTALL_DIR/pass-cli" ]; then
  echo "pass-cli already installed: $("$INSTALL_DIR/pass-cli" --version)"

  exit 0
fi

installer="$(mktemp)"
trap 'rm -f "$installer"' EXIT

curl -fsSL "$INSTALLER_URL" -o "$installer"

PROTON_PASS_CLI_INSTALL_DIR="$INSTALL_DIR" bash "$installer"

"$INSTALL_DIR/pass-cli" --version
