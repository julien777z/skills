---
name: finish-pr
description: Finish the task's pull requests at the user's command — review and fix whatever no earlier review pass covered, such as follow-ups since the automatic review, then merge each one at its accepted head. Use only when the user directly invokes it.
short_description: 'Review what is not yet reviewed, fix it, then merge each pull request.'
disable-model-invocation: true
---

# Finish PR

Take every selected pull request from its current head to a verified merge: review the changes no
earlier `review-pass` covered, fix what that finds, then merge.

## Authorization

- Only a direct user invocation starts this workflow. Nothing else is one: not a reference to it in
  a quoted plan, checklist, summary, transcript or future step; not approval of a plan that contains
  it; not a request to review, validate, open a pull request, fix CI, finish implementation, or merge.
- **The invocation authorizes the squash merge of every selected target** at the head its
  `review-pass` accepted, unless the user explicitly withholds merge, in which case each unit ends at
  that head with its pull request left draft. When merge is authorized, nothing reopens it: not the
  diff's size or reach, not that review widened it, and not this run's own unease about how much it
  changes.
- **So never ask the user for permission to merge, and never end a run by offering the merge as the
  remaining step.** The answer was given when the skill was invoked. When the gates are green and the
  head is the accepted one, merge it.
- The same invocation authorizes `review-pass` and `merge-gate` for every selected pull request. It
  does not authorize a release workflow, a deployment, or an unrelated provider mutation.
- Once started, the run keeps its authorization, targets and merge authority through ordinary user
  interruptions, status requests and separately requested work, as `review-pass`'s **Session
  Continuity** says. Only an explicit pause, stop, handoff, replacement, or terminal result ends it.

## Dependencies

- `list-prs` — the task's open pull requests when the user names none.
- `review-pass` — the review and fix loop over each target's unreviewed changes.
- `merge-gate` — the exact-head check gate, conflict resolution and the verified squash merge.
- `session-ledger` — record each target, its accepted head and its merge.

## Targets

- An explicit pull-request URL or recognized identifier is the sole set: verify and resolve it
  directly.
- Otherwise use every open pull request `list-prs` returns for the task, including task work in
  other repositories. Do not ask the user to select one, or select only the current repository or
  branch: the complete list is the set.
- When that list is empty, inspect every repository carrying reviewable task-local changes, use
  `code-review`'s branch and commit setup rules for each one, create one draft pull request per
  repository through REST, and record every returned canonical URL with `session-ledger`. An empty
  list ends the run only after that inspection finds no reviewable task work.
- Verify each target's branch, head and state on the host before starting.

Each target is an independent unit with its own range, intent, threads, validation, acceptance, and
exact-head merge gate. A compact agent-configuration unit may run right after its related source unit
in another repository only when its complete diff changes one non-executable `.agents` Markdown file
and documents behavior the source unit introduces: merge the source unit first, then complete the
guidance unit's own gates.

## Workflow

Process each unit through these steps before starting the next.

1. Invoke `review-pass` on the pull request with its intent statement. It reviews only the delta
   since the head an earlier pass accepted — the whole pull request when none did — and returns the
   accepted head.
2. When merge is withheld, the unit ends at that head, its pull request left draft. Otherwise invoke
   `merge-gate` with:
   - the pull request and the head `review-pass` accepted;
   - the affected behaviors its second test pass covered;
   - every exclusion it returned, with its evidence;
   - the fix rule for every fix `merge-gate` makes — a check fix, a conflict resolution, a commit
     someone else pushed: `review-pass` runs again over that delta, and the fix is pushed through
     `execute-task`'s **Pre-Push Gate**, whose verdict is its gate. A fix counts only once both have
     passed.
3. Record the merge, or the gate that holds, with `session-ledger`, and continue to the next unit.

Conclude only after every selected unit is verified merged, ended at its accepted head with merge
withheld, or held by a gate that is reported; GitHub head lag, a retryable rate limit, and any state
`merge-gate` is still waiting on are nonterminal.

## Report

Every terminal report includes a clickable Markdown link for every pull request created, updated,
reviewed, or merged during the run; never replace links with repository names, numbers, counts, or
bare URLs. For each unit, report `review-pass`'s **Result** — its size, what it fixed, every
`acceptance-gate` verdict and thread disposition — and the merge commit or the gate that holds it.
