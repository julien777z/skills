---
name: reconcile-skills
description: Refresh the installed shared skills and rules to the latest default branch while keeping the session's open skill pull requests and uncommitted skill edits in effect. Use when the GitHub rules' After Agent Sync section calls for it, or when the user asks to bring local agent guidance up to date.
short_description: 'Refresh installed skills to the latest default branch, keeping pending skill changes in effect.'
---

# Reconcile Skills

Refresh the user-level agent roots from the shared skills repository. An agent runs this skill
when the GitHub rules' **After Agent Sync** section calls for it; cloud setup also runs the
installer when a session starts.
This skill never copies provider mirrors by hand.

## Dependencies

- `session-ledger` — the open agent-configuration pull requests this task recorded.
- `merge-conflict` — resolve a conflict between the default branch and a recorded pull request
  inside the overlay.

## What Takes Effect

**The installed guidance is the default branch plus the session's pending skill changes.** Refreshing
never parks pending work where it stops taking effect: the latest default branch, every open
agent-configuration pull request the task's ledger records, and the checkout's uncommitted edits all
take effect together. The merge is local; it never merges, pushes or rebases a pull request.

- **Recorded pull requests** are the `artifact` entries `session-ledger` holds for this task whose
  pull request touches only agent configuration. Verify each is still open on the host; a merged one
  arrives through the default branch, and a closed one is left out. A pull request whose branch is
  checked out counts as recorded.
- **Its content** is the local branch tip when one exists, unpushed commits included, and the fetched
  remote head otherwise.
- **Uncommitted edits** are the source checkout's working tree, untracked files included.

## Refresh

1. Resolve an installed user-level skill link to its Git checkout. Use the main local checkout that
   link targets, not the task worktree. Confirm the checkout is the shared skills repository and its
   README identifies `bootstrap/install.sh`. In a cloud session, use the skills checkout attached to
   the session when there is one, and otherwise the setup clone under the agent's home.
2. Record the checkout's current commit, branch, working-tree status, and installed source. Fetch the
   remote default branch and every recorded pull request's branch.
3. **With no recorded pull request and the checkout on the default branch**, fast-forward it in
   place: create a named `git stash push --include-untracked` when the tree is dirty, fast-forward,
   restore the stash and verify the original paths are present. The checkout is the installed
   source. A cloud setup clone with nothing attached stays on its configured branch; the installer
   fetches that branch and fast-forwards it when invoked.
4. **Otherwise build the overlay**, and leave the source checkout's branch and working tree exactly
   as they were, since the session goes on editing and pushing there:
   1. Create or reuse a linked worktree beside the checkout on a local branch that is never pushed.
      Before resetting it to the fetched default branch, confirm it holds no commit outside its last
      inputs; preserve any it does on a named branch and report it.
   2. Merge each recorded pull request's content into it. Resolve a conflict through
      `merge-conflict`; the resolution stays in the overlay, and the report names the pull request
      that will need it.
   3. Snapshot the source checkout's working tree, untracked files included, through a temporary
      index without touching the checkout, and apply its diff from the checkout's branch head onto
      the overlay, resolving a conflict the same way.
   4. The overlay is the installed source. Rebuild it on every refresh rather than updating it, and
      remove it once no recorded pull request and no uncommitted edit remains. Never edit inside it:
      guidance edits go to the source checkout and reach the overlay at the next refresh.
5. Run `bash bootstrap/install.sh` from the installed source. Resolve each installed skill and
   rule link in every existing user-level agent root and confirm it points into that source. Check
   Codex's global `AGENTS.md` link when Codex is installed. Preserve real files and foreign links; the
   installer's conflict preflight reports them before changing links. Never reset, drop, or
   overwrite preserved work.
6. Read every shared rule and shared skill that differs between the recorded and the new installed
   source, with each changed skill's supporting files, before using them in the current session.

## Report

Report the source checkout and the branch it was left on, the installed source, what took effect —
the default branch's old and new commits, each recorded pull request with the tip merged, and the
uncommitted paths applied — every conflict resolved in the overlay and the pull request it belongs
to, the roots refreshed, link verification, and the skills and rules reread. State the exact blocker
and untouched paths if the refresh stopped.
