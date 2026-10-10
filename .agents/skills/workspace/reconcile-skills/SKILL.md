---
name: reconcile-skills
description: Refresh the installed shared skills and rules when the GitHub rules' After Agent Sync section calls for it, or when the user asks to bring local agent guidance up to date.
short_description: 'Refresh installed shared skills and rules from their source checkout.'
---

# Reconcile Skills

Refresh the user-level agent roots from the shared skills repository. An agent runs this skill
when the GitHub rules' **After Agent Sync** section calls for it; cloud setup also runs the
installer when a session starts.
This skill never copies provider mirrors by hand.

## Refresh

1. Resolve an installed user-level skill link to its Git checkout. Use the main local checkout that
   link targets, not the task worktree. Confirm the checkout is the shared skills repository and its
   README identifies `bootstrap/install.sh`. In a cloud session, use the setup clone under the
   agent's home; its installer selects any attached skills checkout.
2. Record the checkout's current commit, branch, and working-tree status. A dirty working tree is
   not a refresh blocker: preserve it before changing refs, including untracked paths. When the
   checkout is already on the default branch, create a named `git stash push --include-untracked`
   and restore it after the refresh, verifying the original paths are present. When another branch
   owns the work, preserve it in a separate linked worktree: stash it, switch the source checkout
   to the default branch, create the preservation worktree at the original branch, and restore the
   stash there. After either preservation path, fetch the remote default branch and fast-forward
   the source checkout before installation. Keep installed links on that refreshed default-branch
   checkout and report any preservation worktree path. Never reset, drop, or overwrite preserved
   work. In cloud, leave the setup clone on its configured branch; the
   installer fetches that branch once and fast-forwards it when invoked.
3. Run `bash bootstrap/install.sh` from the checkout. Resolve each installed skill and
   rule link in every existing user-level agent root and confirm it points into the selected source
   checkout. Check Codex's global `AGENTS.md` link when Codex is installed. Preserve real files and
   foreign links; the installer's conflict preflight reports them before changing links.
4. Read every shared rule and shared skill changed between the recorded and refreshed commits, with
   each changed skill's supporting files, before using them in the current session.

## Report

Report the source checkout, old and new commits, roots refreshed, link verification, and skills and
rules reread. State the exact blocker and untouched paths if the refresh stopped.
