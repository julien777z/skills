# Skills Refresh Prompts

## busy

Another process holds the skills-install lock. The startup check has not run. Wait for that process to finish, then run update-skills before ordinary work; preserve pending changes.

## codex-discovery

Codex discovers skills before SessionStart; newly installed skills appear in the next session. Do not claim the current catalogue was reloaded.

## failed

Remote skills refresh failed. The installed guidance remains available. Inspect the hook error output and retry update-skills when GitHub is reachable; preserve pending changes.

## reconcile

Shared skills need reconciliation with pending source changes, an unmarked worktree, or the fetched default branch. Run update-skills before ordinary work; preserve pending changes.

## repaired

Installed shared skill and rule links were repaired and verified. Read changed guidance before using it.
