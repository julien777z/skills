---
name: update-skills
description: Refresh the installed shared skills and rules to the latest default branch while keeping pending skill pull requests, the checked-out skills branch and uncommitted skill edits in effect. Use when the GitHub rules' After Agent Sync section calls for it, or when the user asks to bring local agent guidance up to date.
short_description: 'Refresh installed skills to the latest default branch, keeping pending skill changes in effect.'
---

# Update Skills

Refresh the user-level agent roots from the shared skills repository. An agent runs this skill
when the GitHub rules' **After Agent Sync** section calls for it; cloud setup also runs the
installer when a session starts.
This skill never copies provider mirrors by hand.

## Dependencies

- `session-ledger` — the open pull requests this task created or worked on.
- `merge-conflict` — its comparison and resolution of a conflict inside the overlay.
- `agent-lock` — one refresh at a time on the machine's shared install.

## What Takes Effect

**The installed guidance is the default branch plus pending skill changes.** Refreshing never
parks pending work where it stops taking effect: the latest default branch, the agent configuration
of every pull request in effect and of the checked-out branch, and the checkout's uncommitted edits
all take effect together. The merge is local; it never merges, pushes or rebases a pull request. In
a cloud session the source checkout is the attached skills checkout; with nothing attached, the
setup clone stays on its configured branch.

**Only `.agents` changes take effect, and only from trusted inputs.** Each input contributes its
changes under `.agents` and nothing else; the report lists the other paths it carried. An input is
trusted when it lives in the shared skills repository itself, never a fork or another repository;
an untrusted one is left out and reported.

- **Recorded pull requests** are the `artifact` entries `session-ledger` holds for this task with a
  `created` or `touched` receipt, open on the host and trusted. A `reference` entry never takes
  effect. A merged pull request arrives through the default branch.
- **Pull requests in effect** are the recorded ones plus each pull request the current overlay —
  the newest complete one, read at step 2 — names in its stored inputs that is still open on the
  host and trusted, whichever session recorded it, so one session's refresh never drops another's
  pending changes from the shared install.
- **A pull request's content** is its fetched remote head followed by its local branch tip when one
  exists, so pushed commits from other workers and unpushed local commits both arrive.
- **The checked-out branch**, when it is not the default branch, takes effect at its local tip only
  when it is the head branch of a pull request in effect or its upstream is a branch on the shared
  repository's own remote. A branch with no upstream, or one tracking a fork, is left out; its
  uncommitted edits still take effect.
- **Uncommitted edits** are the source checkout's working tree, untracked files included.

## Refresh

Hold `agent-lock` on the key `skills-install`, acquired with `--ttl-seconds 1800`, from step 2 until
step 6 finishes, so two sessions never build or remove overlays at once. Run its `check` before
every write to shared state: step 3's stash, fast-forward and marker deletion, step 4.4's marker,
step 5, and each removal in step 6. On a failed check, stop writes immediately, reacquire the lock, restore any stash this run pushed
and verify its paths, then restart at step 2. Keep step 2's first record whole and the head each
abandoned build reached; the restarted step 2 adds only overlays that record lacks. Repeat recovery
after each lost lease until verification succeeds. After safe cleanup, release the lock with
`--resource-idle` once step 6 finishes or an authority conflict holds further writes. A release the tool refuses means a successor took the lock after its deadline:
release nothing, and report that the lock expired and which overlays were removed after its
deadline.

A local fault is recovery work, not completion. If a checkout, Git object, ref, overlay or managed
link cannot be read, preserve the original state and reconstruct a healthy source from the latest
default branch, the last verified complete snapshot and retained trusted input records. Recover every
readable pending change and preserve unreadable originals for later recovery; do not assert their
contents or silently discard them. Repair the native installer or its owned source as needed, and
resume the refresh through link verification. Link verification proves which source was installed,
not the contents of unreadable inputs: report that uncertainty and continue investigating retained
originals without holding installation. Use retained ownership records and installer preflight to
distinguish managed links from foreign links. Reading merged guidance does not install it. Preserve
foreign files and links, trust checks and lock ownership throughout; a genuine authority conflict
remains a decision while independent recovery continues.

1. Resolve an installed user-level skill link to its Git checkout. When the link resolves into an
   overlay worktree, use the main checkout it is a linked worktree of. Confirm the checkout is the
   shared skills repository and its README identifies `bootstrap/install.sh`.
2. Record the checkout's current commit, branch, working-tree status, installed source, and each
   `skills-overlay/` worktree with the built head its marker stores. Fetch the remote default branch
   and the branch of every pull request in effect.
3. **With no pull request in effect and the checkout on the default branch**, fast-forward it in
   place: create a named `git stash push --include-untracked` when the tree is dirty, fast-forward,
   restore the stash and verify the original paths are present. Its uncommitted edits stay live
   through the links into it. Then delete every overlay's `skills-overlay` marker, so the installer
   returns to the checkout, and continue at step 5.
4. **Otherwise build a new overlay**, and leave the source checkout's branch and working tree exactly
   as they were, since the session goes on editing and pushing there. The installed links keep
   pointing at the previous source until the new overlay is complete:
   1. Create a new linked worktree beside the checkout, on a fresh local branch named
      `skills-overlay/<UTC timestamp>` that is never pushed, at the fetched default branch.
   2. Bring in each pull request in effect, then the checked-out branch: apply the input's
      `.agents` diff from its merge base with the default branch three-way, and commit it. A
      conflict, between the default branch and an input or between two inputs, is resolved through
      `merge-conflict` steps 3 to 8, with the overlay as built so far as the base and the input as
      the head; leave out step 7's regeneration and pre-push checks, and its gate and push steps,
      since the overlay is local. The report names each pull request that will need the same
      resolution.
   3. Snapshot the source checkout's working tree, untracked files included, through a temporary
      index without touching the checkout, apply its `.agents` diff from the checkout's branch head
      onto the overlay, resolving a conflict the same way, and commit it in the overlay.
   4. Write the overlay's inputs last, to a `skills-overlay` file in its own Git directory: each
      pull request in effect, the checked-out branch, and the overlay's built head commit. That file
      marks the overlay complete, and the installer then installs from the newest complete overlay
      of the source checkout. Never edit inside it: guidance edits go to the source checkout and
      reach the next overlay at the next refresh.
5. Run the installer: `bash bootstrap/install.sh` from the source checkout on a local machine, or
   the setup clone's installer in a cloud session, which selects the attached checkout and relinks
   every cloud home. The installer fetches a cloud setup clone's configured branch and
   fast-forwards it, and installs from the newest complete overlay when one exists. Resolve each
   installed skill and rule link in every existing user-level agent root and confirm it points into
   the installed source. Check Codex's global `AGENTS.md` link when Codex is installed. Preserve
   real files and foreign links; the installer's conflict preflight reports them before changing
   links. Never reset, drop, or overwrite preserved work.
6. Once the links point into the installed source, remove every other `skills-overlay/` worktree of
   the checkout, complete or not; this step alone removes overlays. First compare each with the
   built head step 2 recorded for it, or for each of this run's abandoned builds the head it
   reached, or, for a markerless overlay this run never recorded, its starting commit: preserve a
   commit after it, or a working tree that differs from it, on a named branch, and report it. Then
   remove the worktree and delete its `skills-overlay/` branch, along with every `skills-overlay/`
   branch left without a worktree.
7. Read every shared rule and shared skill that differs between the recorded and the new installed
   source, with each changed skill's supporting files, before using them in the current session.

## Report

Report the source checkout and the branch it was left on, the installed source and the commit its
links resolve to, what took effect — the default branch's old and new commits, each pull request in
effect with the tips brought in, the checked-out branch, and the uncommitted paths applied — every
input or path left out and why, every conflict resolved in the overlay and the pull request it
belongs to, anything preserved from a removed overlay, the roots refreshed, link verification, and
the skills and rules reread. Name any preserved unreadable originals and the evidence used to reconstruct the installed source; retain any unresolved authority conflict and its next action.
