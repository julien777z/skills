---
name: reconcile-skills
description: Refresh the installed shared skills and rules to the latest default branch while keeping pending skill pull requests, the checked-out skills branch and uncommitted skill edits in effect. Use when the GitHub rules' After Agent Sync section calls for it, or when the user asks to bring local agent guidance up to date.
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

**The installed guidance is the default branch plus pending skill changes.** Refreshing never
parks pending work where it stops taking effect: the latest default branch, every pull request in
effect, the checked-out branch, and the checkout's uncommitted edits all take effect together. The
merge is local; it never merges, pushes or rebases a pull request. In a cloud session the source
checkout is the attached skills checkout; with nothing attached, the setup clone stays on its
configured branch.

Every input passes the **source checks**: it lives in the shared skills repository itself, never a
fork or another repository, and every file it changes from its merge base with the default branch is
agent configuration. An input that fails them is left out and reported.

- **Recorded pull requests** are the `artifact` entries `session-ledger` holds for this task with a
  `created` or `touched` receipt, open on the host and passing the source checks. A `reference`
  entry never takes effect. A merged pull request arrives through the default branch.
- **Pull requests in effect** are the recorded ones plus each pull request the current overlay's
  stored inputs name that is still open on the host and passes the source checks, whichever session
  recorded it, so one session's refresh never drops another's pending changes from the shared
  install.
- **A pull request's content** is its fetched remote head followed by its local branch tip when one
  exists, so pushed commits from other workers and unpushed local commits both arrive.
- **The checked-out branch**, when it is not the default branch, is an input in its own right at its
  local tip, with or without a pull request, once it passes the source checks: no upstream, or one
  on the shared repository's own remote.
- **Uncommitted edits** are the source checkout's working tree, untracked files included.

## Refresh

1. Resolve an installed user-level skill link to its Git checkout. When the link resolves into an
   overlay worktree, use the main checkout it is a linked worktree of. Confirm the checkout is the
   shared skills repository and its README identifies `bootstrap/install.sh`.
2. Record the checkout's current commit, branch, working-tree status, and installed source.
3. Fetch the remote default branch and the branch of every pull request in effect. **With no pull
   request in effect, the checkout on the default branch and every pending input empty**,
   fast-forward the checkout in place: create a named `git stash push --include-untracked` when the
   tree is dirty, fast-forward, restore the stash and verify the original paths are present. The
   checkout is the installed source; continue at step 5.
4. **Otherwise build a new overlay**, and leave the source checkout's branch and working tree exactly
   as they were, since the session goes on editing and pushing there. The installed links keep
   pointing at the previous source until the new overlay is complete:
   1. Create a new linked worktree beside the checkout, on a fresh local branch that is never
      pushed, at the fetched default branch.
   2. Merge each pull request in effect, then the checked-out branch. A conflict, between the default
      branch and a pull request or between two of them, is resolved through `merge-conflict` steps 3
      to 8, with the overlay as built so far as the base and the incoming branch as the head; leave
      out step 7's regeneration and pre-push checks, and its gate and push steps, since the overlay
      is local. The report names each pull request that will need the same resolution.
   3. Snapshot the source checkout's working tree, untracked files included, through a temporary
      index without touching the checkout, apply its diff from the checkout's branch head onto the
      overlay, resolving a conflict the same way, and commit it in the overlay.
   4. Write the overlay's inputs last, to a `skills-overlay` file in its own Git directory: each
      pull request in effect, the checked-out branch, and the overlay's built head commit. That file
      marks the overlay complete, and the installer then installs from the newest complete overlay
      of the source checkout. Never edit inside it: guidance edits go to the source checkout and
      reach the next overlay at the next refresh.
5. Run the installer: `bash bootstrap/install.sh` from the source checkout on a local machine, or
   the setup clone's installer in a cloud session, which selects the attached checkout and relinks
   every cloud home. The installer fetches a cloud setup clone's configured branch and
   fast-forwards it, and installs from the newest complete overlay when one exists. Resolve each installed skill and
   rule link in every existing user-level agent root and confirm it points into that source. Check
   Codex's global `AGENTS.md` link when Codex is installed. Preserve real files and foreign links; the
   installer's conflict preflight reports them before changing links. Never reset, drop, or
   overwrite preserved work.
6. Once the links point into the new source, remove the previous overlay, if any. First compare it
   with its stored built head: preserve a commit after that head, or a working tree that differs from
   it, on a named branch, and report it.
7. Read every shared rule and shared skill that differs between the recorded and the new installed
   source, with each changed skill's supporting files, before using them in the current session.

## Report

Report the source checkout and the branch it was left on, the installed source, what took effect —
the default branch's old and new commits, each pull request in effect with the tips merged, the
checked-out branch, and the uncommitted paths applied — every input left out by the source checks,
every conflict resolved in the overlay and the pull request it belongs to, anything preserved from
the previous overlay, the roots refreshed, link verification, and the skills and rules reread. State
the exact blocker and untouched paths if the refresh stopped; the links still point at the previous
source then.
