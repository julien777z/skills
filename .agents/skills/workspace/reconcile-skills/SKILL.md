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

- `session-ledger` — the open agent-configuration pull requests this task created or worked on.
- `merge-conflict` — its comparison and resolution of a conflict inside the overlay.

## What Takes Effect

**The installed guidance is the default branch plus pending skill changes.** Refreshing never parks
pending work where it stops taking effect: the latest default branch, every open agent-configuration
pull request in effect, the checked-out branch, and the checkout's uncommitted edits all take effect
together. The merge is local; it never merges, pushes or rebases a pull request.

- **Recorded pull requests** are the `artifact` entries `session-ledger` holds for this task with a
  `created` or `touched` receipt, for a pull request in the shared skills repository whose head
  branch lives in that repository rather than a fork, and whose files are all agent configuration. A
  `reference` entry, another repository's pull request and a fork's never take effect. Verify each
  is still open on the host; a merged one arrives through the default branch, and a closed one is
  left out.
- **Pull requests in effect** are the recorded ones plus those the overlay's stored inputs name that
  pass the same checks, so one session's refresh never drops another session's pending changes from
  the shared install.
- **A pull request's content** is its fetched remote head followed by its local branch tip when one
  exists, so pushed commits from other workers and unpushed local commits both arrive.
- **The checked-out branch**, when it is not the default branch, is an input in its own right at its
  local tip, with or without a pull request.
- **Uncommitted edits** are the source checkout's working tree, untracked files included.

## Refresh

1. Resolve an installed user-level skill link to its Git checkout. When the link resolves into the
   overlay worktree, use the main checkout it is a linked worktree of. Confirm the checkout is the
   shared skills repository and its README identifies `bootstrap/install.sh`. **In a cloud
   session**, run the setup clone's installer, which selects any attached skills checkout and
   relinks every cloud home, and build no overlay: the attached checkout's branch and edits are what
   it installs. Leave the setup clone on its configured branch; the installer fetches that branch
   and fast-forwards it. Then continue at step 6.
2. Record the checkout's current commit, branch, working-tree status, and installed source. Fetch
   the remote default branch and the branch of every pull request in effect.
3. **With no pull request in effect and the checkout on the default branch**, fast-forward it in
   place: create a named `git stash push --include-untracked` when the tree is dirty, fast-forward,
   restore the stash and verify the original paths are present. The checkout is the installed
   source. After step 5 relinks into it, remove any previous overlay under step 4.1's preservation.
4. **Otherwise build the overlay**, and leave the source checkout's branch and working tree exactly
   as they were, since the session goes on editing and pushing there:
   1. Create or reuse a linked worktree beside the checkout on a local branch that is never pushed.
      Before resetting it to the fetched default branch, read its working-tree status and compare
      its commits with its stored inputs; preserve an uncommitted change or a commit outside them on
      a named branch, and report it.
   2. Merge each pull request in effect, then the checked-out branch. A conflict, between the
      default branch and a pull request or between two pull requests, is resolved with
      `merge-conflict`'s comparison and resolution steps 3–6; its gate and push steps do not apply,
      since the overlay is local and rebuilt. The report names each pull request that will need the
      same resolution.
   3. Snapshot the source checkout's working tree, untracked files included, through a temporary
      index without touching the checkout, and apply its diff from the checkout's branch head onto
      the overlay, resolving a conflict the same way.
   4. Store the overlay's inputs — each pull request in effect and the checked-out branch — in the
      overlay worktree's own Git directory. The overlay is the installed source. Rebuild it on every
      refresh rather than updating it. Never edit inside it: guidance edits go to the source
      checkout and reach the overlay at the next refresh.
5. Run `bash bootstrap/install.sh` from the installed source. Resolve each installed skill and rule
   link in every existing user-level agent root and confirm it points into that source. Check
   Codex's global `AGENTS.md` link when Codex is installed. Preserve real files and foreign links;
   the installer's conflict preflight reports them before changing links. Never reset, drop, or
   overwrite preserved work.
6. Read every shared rule and shared skill that differs between the recorded and the new installed
   source, with each changed skill's supporting files, before using them in the current session.

## Report

Report the source checkout and the branch it was left on, the installed source, what took effect —
the default branch's old and new commits, each pull request in effect with the tips merged, the
checked-out branch, and the uncommitted paths applied — every conflict resolved in the overlay and
the pull request it belongs to, anything preserved from an earlier overlay, the roots refreshed,
link verification, and the skills and rules reread. State the exact blocker and untouched paths if
the refresh stopped.
