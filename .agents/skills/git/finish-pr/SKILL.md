---
name: finish-pr
description: Review and fix the whole of each task pull request, then merge it at its accepted head. User-invoked only — run when the user asks to finish the task's pull requests, never on the agent's own initiative.
short_description: 'Review and fix the whole pull request, then merge it.'
---

# Finish PR

Review, fix, and merge every open pull request for the active task unless the user names a
specific set.

## Authorization

- Only the user's own request in the current message starts this workflow: its command, or asking
  for it in words. Nothing else is one: not a reference to it in a quoted plan, checklist, summary,
  transcript or future step; not approval of a plan that contains it; not a request to review,
  validate, open a pull request, fix CI, finish implementation, or merge.
- **The invocation authorizes the squash merge of every selected target** at the head its
  `review-pass` accepted, unless the user explicitly withholds merge, in which case each unit ends at
  that head with its pull request left draft. When merge is authorized, nothing reopens it: not the
  diff's size or reach, not that review widened it, and not this run's own unease about how much it
  changes.
- **So never ask the user for permission to merge, and never end a run by offering the merge as the
  remaining step.** The answer was given when the skill was invoked. When the gates are green and the
  head is the accepted one, merge it.
- The same invocation authorizes `review-pass` and `merge-gate` for every selected pull request. It
  does not authorize separately dispatching a release workflow, creating a deployment, or an
  unrelated provider mutation.
- Once started, the run keeps its authorization, targets and merge authority through ordinary user
  interruptions, status requests and separately requested work. Only an explicit pause, stop, handoff, replacement, or terminal result ends it.

## Dependencies
- `list-prs`
- `review-pass`
- `merge-gate`
- `session-ledger`

## Targets

- An explicit pull-request URL or recognized identifier in the user's own message is the sole set:
  verify and resolve it directly. A pull request the message does not name is never added: not one
  mentioned earlier as awaiting merge, not the dependency a held unit waits on, and not one a bare
  "yes" beside the request might answer. Such a dependency stays a gate under **Dependent Pull
  Requests**.
- Otherwise run `list-prs` before starting any individual review, even when the current branch
  already has a pull request or the request uses the singular. Use its full task-wide result,
  including work in other repositories.
- When that list is empty, inspect every repository carrying reviewable task-local changes, commit
  each one's task changes to a branch under the GitHub rules' branch rules, create one draft pull
  request per repository, and record every returned canonical URL with `session-ledger`. An empty
  list ends the run only after that inspection finds no reviewable task work.
- Before starting any individual review, record every selected canonical URL as a pending unit in
  the run's target inventory through `session-ledger`. If discovery is incomplete, also record
  discovery as pending and recover the missing records. Add all recovered targets before marking
  discovery complete; known units can proceed while recovery runs.
- Verify each target's branch, head and state on the host before starting its review.

Each target is an independent unit with its own range, intent, threads, validation, acceptance, and
exact-head merge gate. A compact agent-configuration unit may run right after its related source unit
in another repository only when its complete diff changes one non-executable `.agents` Markdown file
and documents behavior the source unit introduces: merge the source unit first, then complete the
guidance unit's own gates.

## Dependent Pull Requests

A selected pull request whose build or behavior resolves another pull request's branch — through a
manifest, lockfile, submodule or checkout reference — that this session is also changing is a
dependent unit. Its dependency gates its merge, never its review:

- When the dependency is a selected unit, review it first and review the dependent once against
  its accepted head; a dependency that is not a target is only a gate on the dependent's merge. When a later fix to the dependency changes what the dependent consumes, adapting
  the dependent is a fix that `review-pass` reviews as a new delta. A dependency that merged
  before the dependent's review starts is repointed first, as below, and the dependent is then
  reviewed once on that head.
- The dependent completes its review at its accepted head and holds there, draft, while the
  dependency is unmerged, so `merge-gate` later receives that review's coverage. The hold is not a
  withheld merge and does not end the run: other selected units proceed while it waits for the
  dependency's merge through the host's event route, and the run ends only once it lands or reaches
  the gate below. A dependency closed without merging, or whose merge is neither authorized nor
  pending, is a concrete gate: the unit stays at its accepted head, draft, and the **Report** names
  the gate and the saved next action.
- Once the dependency merges, repoint every consuming reference as `merge-gate`'s
  delivery-dependency gate says, regenerating any lockfile with the repository's tooling. The
  repoint's diff holds only those reference edits and the lockfile entries they change.
  `review-pass` reviews it as a new delta, it passes the validation it affects and the pre-push
  checks, and `merge-gate` receives the head `review-pass` accepts.
- Then land the dependent under the same invocation's merge authorization. A user's explicit
  withholding of merge still ends the unit at its accepted head.

## Workflow

Process each eligible unit through these steps, preserving their order within that unit. A held unit
does not delay starting another independent unit whose current work and dependencies permit it;
hold only the unit that needs the unresolved result, recording its gate and saved next action.
Follow the active task's recorded priorities when choosing the next eligible unit.

1. Invoke `review-pass` on the pull request with its intent statement, asking for the whole pull
   request: its complete merge-base diff, the full contents of every touched file, related code and
   sibling modules. Its **Range** decides what an earlier whole pass already covers, so a pull
   request already reviewed whole — one an earlier run held for a dependency, say — gets only its
   delta since that accepted head. It returns the accepted head.
2. When merge is withheld, the unit ends at that head, its pull request left draft. A dependent unit
   holds at that head until its dependency merges and then repoints, as **Dependent Pull Requests**
   says. Otherwise invoke `merge-gate` with:
   - the pull request and the head `review-pass` accepted, or a dependent unit's repointed head;
   - its **Checks** results, with their commands and head, as the behaviors local tests already cover;
   - that this caller owns the primary checkout refresh after Agent Sync;
   - every exclusion it returned, with its evidence;
   - the fix rule for every fix `merge-gate` makes — a check fix, a conflict resolution, a commit
     someone else pushed: `review-pass` runs again over that fix's delta, and the fix is pushed through
     the GitHub rule’s **Pre-Push Gate**, whose verdict is its gate. A fix counts only once both have
     passed.
3. After a verified merge, run **Local Checkout**. Record the merge and checkout outcome, or the
   gate that holds the merge, with `session-ledger`, and continue to the next unit.

Before concluding, require discovery to be complete and reconcile the recorded target inventory
with its verified dispositions. Resume any unit without a disposition even if a different
repository's pull request already merged. Every entry must be verified merged with `merge-gate`
returned, ended at its accepted head with merge withheld, or held by a gate that is reported. GitHub
head lag and a retryable rate limit are nonterminal.

## Local Checkout

- Locate the primary checkout in Git's worktree inventory and verify the remote identifies the
  merged repository. Fetch the pull request's target branch from that remote and confirm the
  fetched tip contains the verified merge. For a guidance merge, keep the Agent Sync and installed
  guidance results from `merge-gate`. Verify the generated guidance in the refreshed checkout.
- Before changing an index, working tree, or branch, check for an in-progress Git operation in
  each affected checkout. Resume the refresh after that operation finishes or is safely recovered.
- Inspect the current branch, index, working tree, and untracked files. Remove a local edit only
  when the fetched tree already has it or the exact change landed in the target branch's history
  and was not subsequently reverted. Compare staged and unstaged changes, including file mode and binary
  changes, before restoring anything. For a file with mixed or uncertain changes, preserve the
  entire file unless the landed and local-only changes can be verified independently.
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
  If the local target branch has diverged, preserve its tip under a separate local branch before
  moving the target branch to the verified remote tip. Resolve these local conditions and retry
  the switch or fast-forward. A branch mismatch, local edits, or divergence does not end the refresh.
- Verify the primary checkout is on the target branch at the fetched tip and contains the verified
  merge. When the user is viewing another worktree in a Git client, select the primary checkout
  there and verify the displayed branch. Record the resulting head and every preservation branch
  or stash created. If an active Git
  operation or unavailable checkout prevents safe recovery, follow the applicable Git recovery
  route and resume the refresh when it is safe. Record any remaining external blocker and the
  saved next action. Continue independent units without reopening a verified merge.
- For the shared skills repository, keep the installed overlay produced by `merge-gate`. Any
  local guidance parked by this checkout refresh remains recoverable from its branch or stash.
  Record that a later installation refresh reads pending guidance from its ordinary inputs,
  including eligible open pull requests and the current checkout.

## Report

Every terminal report includes a clickable Markdown link for every pull request created, updated,
reviewed, or merged during the run; never replace links with repository names, numbers, counts, or
bare URLs. For each unit, report `review-pass`'s **Output** in full and the merge commit or the
gate that holds it. For a merged unit, include the local checkout outcome and resulting commit,
or the reason it could not be refreshed.
