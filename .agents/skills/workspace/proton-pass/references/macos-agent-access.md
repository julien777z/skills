# Saved Agent Access On macOS

Use the user's designated macOS Keychain entry for the existing Proton Pass agent token.
The configured agent-access setup uses service `codex.proton-pass.agent` and account
`codex-agent`. These are Keychain lookup identifiers, not token values; the same entry is
usable by Claude, Codex, or another authorized harness running on that Mac. If the user's
setup specifies different identifiers, use those rather than creating another credential.

With the task's `PROTON_PASS_SESSION_DIR` already exported, recover an inactive session in
one shell. Keep tracing off before retrieving the token, and do not enable it for this shell:

```sh
set +x

PROTON_PASS_PERSONAL_ACCESS_TOKEN="$(security find-generic-password \
  -s codex.proton-pass.agent -a codex-agent -w)" || exit

if [ -z "$PROTON_PASS_PERSONAL_ACCESS_TOKEN" ]; then
  printf '%s\n' 'The designated Keychain entry returned no token.' >&2
  exit 1
fi

export PROTON_PASS_PERSONAL_ACCESS_TOKEN

pass-cli logout --force
pass-cli login
login_status=$?

unset PROTON_PASS_PERSONAL_ACCESS_TOKEN

if [ "$login_status" -ne 0 ]; then
  exit "$login_status"
fi

pass-cli info
```

Command substitution captures the token without displaying it. Preserve `security`'s failure
status and diagnostic message; a missing entry, a locked Keychain, and denied access require
different remedies. Do not enumerate or dump unrelated Keychain entries. A Keychain approval
prompt is handled at that boundary; never ask for the token in chat or recreate the agent merely
because a shell did not inherit its token.

Proton [agent access](https://protonpass.github.io/pass-cli/commands/agent/) uses a scoped personal
access token and records reasons for audited operations. The Keychain entry is the host's secure
storage for that token; Proton does not populate the shell environment from it automatically.
