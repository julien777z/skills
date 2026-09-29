---
name: reconcile-skills
description: Refresh the installed shared skills and rules after their repository merges and Agent Sync finishes, or when the user asks to bring local agent guidance up to date.
short_description: 'Refresh installed shared skills and rules from their source checkout.'
---

# Reconcile Skills

Refresh the user-level agent roots from the shared skills repository. An agent runs this skill
when guidance changes during a session; cloud setup also runs the installer when a session starts.
This skill never copies provider mirrors by hand.

## Refresh

1. Resolve an installed user-level skill link to its Git checkout. Use the main local checkout that
   link targets, not the task worktree. Confirm the checkout is the shared skills repository and its
   README identifies `bootstrap/install.sh`. In a cloud session, use the setup clone under the
   agent's home; its installer selects any attached skills checkout.
2. Record the checkout's current commit and working-tree status. If it is dirty, report the paths
   and stop without discarding or stashing changes. For a local checkout, fetch the remote default
   branch, switch to that branch, and fast-forward only. If the branch diverges, report the commits
   and stop; do not reset it. In cloud, leave the setup clone on its configured branch; the installer
   fetches that branch once and fast-forwards it when invoked.
3. Run `bash bootstrap/install.sh` from the checkout. Resolve each installed skill and
   rule link in every existing user-level agent root and confirm it points into the selected source
   checkout. Check Codex's global `AGENTS.md` link when Codex is installed. Preserve real files and
   foreign links; the installer's conflict preflight reports them before changing links.
4. Read every shared rule changed between the recorded and refreshed commits. When this run follows
   a merge, also read the merged skill and its supporting files from the refreshed commit before
   using them in the current session.

## Report

Report the source checkout, old and new commits, roots refreshed, link verification, and rules
reread. State the exact blocker and untouched paths if the refresh stopped.
