# Refresh the Primary Checkout

- Locate the primary checkout in Git's worktree inventory and verify the remote identifies the
  merged repository. Fetch the pull request's target branch from that remote and confirm the
  fetched tip contains the verified merge and any CI commits identified by the merge gate. For a guidance merge, keep the Agent Sync and installed
  guidance results from `merge-gate`. Verify the generated guidance in the refreshed checkout.
- Before changing an index, working tree, or branch, check for an in-progress Git operation in
  each affected checkout. Resume the refresh after that operation finishes or is safely recovered.
- Inspect the current branch, index, working tree, and untracked files. Remove a local edit only
  when the fetched tree already has it or the exact change landed in the target branch's history
  and was not subsequently reverted. Compare staged and unstaged changes, including file mode and binary
  changes, before restoring anything. For a file with mixed or uncertain changes, preserve the
  entire file unless the landed and local-only changes can be verified independently.
- Apply the task execution guidance's **Copies A Sync Service Left Behind** procedure to verified
  duplicates made by a file sync service or the operating system. Exclude them from the preservation
  stash.
- Stage the remaining local-only edits by path, including untracked files that belong to the work.
  When a path has different staged and working-tree edits, keep its index entry intact. Save the
  index, working tree, and untracked files in a named local stash and verify the saved versions
  before switching. Record its commit and original branch so it can be restored there. Leave the stash
  in place and keep the original branch and its commits. Give a detached starting commit a local
  preservation branch if no retained branch contains it. Preserve ignored or nested files
  separately if they would block the switch, verifying the saved contents before moving them.
- Run `git switch --no-overwrite-ignore <target-branch>` in the primary checkout and fast-forward
  with `git merge --ff-only --no-autostash --no-overwrite-ignore <verified-remote-tip>`. If the target branch is already
  checked out elsewhere, switch that worktree to a local preservation branch at its existing
  commit, keeping any in-progress work there. Keep both worktrees on named branches.
  If the local target branch has commits outside the fetched tip's history, preserve its tip under a separate local branch before
  moving the target branch to the verified remote tip. Resolve these local conditions and retry
  the switch or fast-forward. A branch mismatch, local edits, or divergence does not end the refresh.
- Verify the primary checkout is on the target branch at the fetched tip, contains the verified
  merge, and is clean in `git status --porcelain --untracked-files=all`. Preserve any remaining
  local work and recheck. When the user is viewing another worktree in a Git client, select the primary checkout
  there and verify the displayed branch. Record the resulting head and every preservation branch
  or stash created. If an active Git
  operation or unavailable checkout prevents safe recovery, follow the applicable Git recovery
  route and resume the refresh when it is safe. Record any remaining external blocker and the
  saved next action. Continue independent units without reopening a verified merge.
- For the shared skills repository, keep the installed overlay produced by `merge-gate`. Any
  local guidance parked by this checkout refresh remains recoverable from its branch or stash.
  Record that a later installation refresh reads pending guidance from its ordinary inputs,
  including eligible open pull requests and the current checkout.
