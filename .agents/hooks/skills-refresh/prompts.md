# Skills Refresh Prompts

## busy

Another process holds the skills-install lock. The startup check has not run. Wait for that process to finish, then run update-skills before ordinary work; preserve pending changes.

## codex-discovery

Codex discovers skills before SessionStart; newly installed skills appear in the next session. Do not claim the current catalogue was reloaded.

## failed

The shared skills startup check failed. Before ordinary work, inspect the hook diagnostics and run update-skills against the selected local checkout. Repair Git errors you can verify and resolve, preserving pending changes and unreadable originals. Use the installed guidance until the repair and refreshed links are verified. Ask the user only for a step that requires their access or a decision only they can make.

## reconcile

Shared skills need reconciliation with pending source changes, an unmarked worktree, or the fetched default branch. Run update-skills before ordinary work; preserve pending changes.

## repaired

The shared skills startup check repaired the checkout or installation and verified the links. Read changed guidance before using it.
