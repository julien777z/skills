---
name: finish-pr
description: Review and fix the whole of each selected pull request, then merge it at its accepted head. Use when the user asks to finish pull requests. Run only when the user asks for it.
short_description: 'Review and fix the whole pull request, then merge it.'
---

# Finish PR

Review, fix, and merge the pull requests selected under **Targets**.

## Authorization

- Only the user's own request in the current message starts this workflow: its command, or asking
  for it in words. Nothing else is one: not a reference to it in a quoted plan, checklist, summary,
  transcript or future step; not approval of a plan that contains it; not a request to review,
  validate, open a pull request, fix CI, finish implementation, or merge.
- **The invocation authorizes the squash merge of every selected target** at the head its
  `review-pass` accepted, unless the user explicitly withholds merge, in which case each unit ends at
  that head with its pull request left draft. When merge is authorized, nothing reopens it: not the
  diff's size, and not this run's own unease about how much it
  changes.
- **So never ask the user for permission to merge, and never end a run by offering the merge as the
  remaining step.** The answer was given when the skill was invoked. When the gates are green and the
  head is the accepted one, merge it.
- The same invocation authorizes `review-pass` and `merge-gate` for every selected pull request.
  It does not authorize separately dispatching a release workflow, creating a deployment, or an
  unrelated provider mutation: `merge-gate`'s **Authorization** says what authorizes those, its
  **No Verification Or Deploy Work** what follows each merge, and its **Pull Request Activity** when a pull request
  is polled.
- Once started, the run keeps its authorization, targets and merge authority through ordinary user
  interruptions, status requests and separately requested work. Only an explicit pause, stop, handoff, replacement, or terminal result ends it.

## Dependencies
- `list-prs`
- `pre-production`
- `review-pass`
- `merge-gate`
- `session-ledger`
- `execute-task`
- `stop-gates`

## Targets

- An explicit pull-request URL or recognized identifier in the user's own message is the sole set,
  verified and resolved directly, apart from the task's open pull requests confined to deferral
  records, which join every run's set since the GitHub rule's **Merge Authorization** already grants
  their merge. Any other pull request the message does not name is never added: not one
  mentioned earlier as awaiting merge, not the dependency a held unit waits on, and not one a bare
  "yes" beside the request might answer. Such a dependency stays a gate under **Dependent Pull
  Requests**.
- With no explicit target, ask `list-prs` for all open pull requests created in the current
  session before starting any individual review. Reconcile creation receipts across the whole
  session through `session-ledger`, including earlier tasks and other repositories. A current
  checkout, recently discussed pull request, or singular wording does not narrow the set.
  A pre-existing pull request the session only touched needs an explicit target unless it
  qualifies under the deferral exception above.
- When that list is empty, inspect every repository carrying reviewable task-local changes, commit
  each one's task changes to a branch under the GitHub rules' branch rules, create one draft pull
  request per repository, and record every returned canonical URL with `session-ledger`. An empty
  list ends the run only after that inspection finds no reviewable task work.
- Before starting any individual review, record every selected canonical URL as a pending unit in
  the run's target inventory through `session-ledger`. If discovery is incomplete, also record
  discovery as pending and recover the missing records. Add all recovered targets before marking
  discovery complete; known units can proceed while recovery runs.
- Verify each target's branch, head and state on the host. A target stays draft through its work
  and review: `merge-gate` marks it ready, as the last step before the merge, once `review-pass`
  has accepted its head.
- Apply the GitHub rule's **Branches and Pull Requests** to source follow-ups, review fixes and
  check fixes. When an addition changes a selected target, refresh that pull request's intent
  before reviewing its resulting head. The **Targets** above still determine which pull requests
  this invocation may merge.
- **Open recorded work `review-pass` returns is built on the target before its review starts**;
  review, merge and a dependency-held repoint keep their own order under **Workflow** and
  **Dependent Pull Requests**.

Each target is an independent unit with its own range, intent, threads, validation, acceptance, and
exact-head merge gate; **Workflow**'s combined review reads together, before the first of them
merges, the units whose changes meet. A compact agent-configuration unit may run right after its related
source unit in another repository only when its complete diff changes one non-executable `.agents`
Markdown file and documents behavior the source unit introduces: review it before the combined
review as any unit, merge the source unit first, then complete the guidance unit's merge gate.

## Dependent Pull Requests

A selected pull request whose build or behavior resolves another pull request's branch — through a
manifest, lockfile, submodule or checkout reference — that this session is also changing is a
dependent unit. Its dependency gates its merge, never its review:

- When the dependency is a selected unit, review it first and review the dependent once against
  its accepted head; a dependency that is not a target is only a gate on the dependent's merge. When a later fix to the dependency changes what the dependent consumes, adapting
  the dependent is a fix that `review-pass` reviews as a new delta. A dependency that merged
  before the dependent's review starts is repointed first, as below, and the dependent is then
  reviewed once on that head.
- The dependent completes its review at its accepted head and holds there, still draft, while the
  dependency is unmerged, so `merge-gate` later receives that review's coverage. The hold is not a
  withheld merge and does not end the run: other selected units proceed while it waits for the
  dependency's merge through the host's event route, and the run ends only once it lands or reaches
  the gate below. A dependency closed without merging, or whose merge is neither authorized nor
  pending, is a concrete gate: the unit stays at its accepted head, and the **Report** names
  the gate and the saved next action.
- Once the dependency merges, repoint every consuming reference as `merge-gate`'s
  delivery-dependency gate says, regenerating any lockfile with the repository's tooling. The
  repoint's diff holds only those reference edits and the lockfile entries they change.
  `review-pass` reviews it as a new delta, it passes the validation it affects and the GitHub
  rule's **Pre-Push Gate**, and `merge-gate` receives the head `review-pass` accepts.
- Then land the dependent under the same invocation's merge authorization. A user's explicit
  withholding of merge still ends the unit at its accepted head.

## Workflow

Process each eligible unit through these steps, preserving their order within that unit. A held unit
does not delay starting another independent unit whose current work and dependencies permit it;
hold only the unit that needs the unresolved result, recording its gate and saved next action;
**Review the combined set** alone waits, and only for the whole-pull-request review of the units
in its set.
Follow the active task's recorded priorities when choosing the next eligible unit.

Before the first step, follow `stop-gates`' **Asking While Paused** once for the whole selection.

1. **Review the whole pull request.** Invoke `review-pass` on the pull request, or once on a bulk
   set as its **Targets** names one, with its intent statement, asking for the whole pull request: its complete merge-base diff, the full contents of every touched file, related code and
   sibling modules. Its **Range** decides what an earlier pass already covers: a pull request whose
   recorded `whole` head has not moved keeps that verdict and is reviewed again by no one, and one
   that moved since gets only its delta from that head. It returns the accepted head.
2. **Review the combined set.** When the selected units hold more than one member of the set
   `review-pass`'s **Set and timing** defines, invoke its **Combined Review** over those members
   once **Review the whole pull request** has returned for each. A member goes on only at a head
   that round accepted; a unit outside the set goes on from its own review.
3. **Gate and merge.** When merge is withheld, the unit ends at that head, its pull request left draft. A dependent unit
   holds at that head until its dependency merges and then repoints, as **Dependent Pull Requests**
   says. Otherwise invoke `merge-gate` with:
   - the pull request and the head `review-pass` accepted, or a dependent unit's repointed head;
   - its **Checks** results, with their commands and head, as the behaviors local tests already cover;
   - that this caller owns the primary checkout refresh after applicable CI writes and Agent Sync;
   - every exclusion it returned, with its evidence;
   - the fix rule for every fix `merge-gate` makes — a check fix, a conflict resolution, a commit
     someone else pushed: refresh the target's intent if its scope changed, then `review-pass`
     runs again over the fix's delta. The fix is pushed through
     the GitHub rule's **Pre-Push Gate**, whose verdict is its gate. A fix counts only once both have
     passed.
4. **Refresh the checkout.** After a verified merge, run **Local Checkout**. Record the merge and checkout outcome, or the
   gate that holds the merge, with `session-ledger`, and continue to the next unit.

Before concluding, require discovery to be complete and reconcile the recorded target inventory
with its verified dispositions. Resume any unit without a disposition even if a different
repository's pull request already merged. Work through every merge gate the run can resolve
within its scope and continue through the authorized merge when the gate clears. Every entry must
be verified merged with `merge-gate`
returned, ended at its accepted head with merge withheld, or held by a gate that is reported,
draft where the gate held it before `merge-gate` marked it ready. A failed readiness transition is
itself a host gate with its evidence. GitHub
head lag and a retryable rate limit are nonterminal.

## Local Checkout

Refresh the primary checkout after every verified merge. Use `merge-gate`'s **CI Commits To The
Target Branch** result to include CI-generated commits. For agent configuration, carry over its
**After Agent Sync** result as well.

Use its **Refresh The Primary Checkout** procedure and record the resulting local commit.

## Report

Every terminal report includes a clickable Markdown link for every pull request created, updated,
reviewed, or merged during the run; never replace links with repository names, numbers, counts, or
bare URLs. For each unit, report `review-pass`'s **Output** in full, its combined review line
included, and the merge commit or the gate that holds it. For a merged unit, include the local checkout outcome and resulting commit,
or the reason it could not be refreshed.
