---
name: execute-task
description: "Always run this. Invoke once, before the first edit, at the start of every task that changes files — including one whose edits sub-agents make, and one that only begins changing files because work turned up a defect — and keep it active until the task's report: it applies the repository's product constraints, fixes the bugs the work encounters rather than reporting them, simplifies as the change grows, gates the branch before it is pushed, checks every outcome it reports, whether its own action or a sub-agent's claim, at the source of truth, and delivers each repository independently. Never invoke it from inside a skill it runs."
short_description: 'Apply repository guidance, fix issues found along the way, validate the diff, and deliver the change.'
---

# Execute Task

Run every change the same way, whether a plan preceded it or the user asked for it in one line.

## Dependencies

- `pre-production` — the target-contract policy for every repository and its data obligations.
- `code-simplify` — simplify each meaningful implementation batch and the complete diff before delivery.
- `acceptance-gate` — judge the complete branch diff before it is pushed.
- `generic-push` — keep each repository's publishing metadata independent during multi-repository changes.
- `merge-conflict` — bring in a conflicting or moved base, found when a push is read back, before other work.

## One Run Per Task

- Invoke this skill once, at the start of a task, before the first edit. A run stays active until
  the task's report, and past it while that report names outstanding work: **Work You Have Already
  Named** keeps the run open until every named item is done or has left that state one of the three
  ways it lists. Nothing in the task re-enters the skill; the run simply has not ended.
- A skill that lists this one as a dependency — `plan-change` does — invokes it once, and the
  skills this one invokes never invoke it back: `pre-production`, `code-simplify`,
  `acceptance-gate`, `generic-push`, and `merge-conflict` are leaves of this run. A second
  invocation while one is active does nothing more than continue the active run.
- This skill never invokes `plan-change`. Where a task needs a plan, `plan-change` runs first and
  invokes this skill once the plan is approved.
- A read-only task — a question answered from the code, a listing, a report with no edit — does
  not run this skill; a task whose edits sub-agents make is not read-only for the agent that
  delegated them. A read-only turn does not close an open run either: a run still holding named
  work stays active through such a turn, and that turn moves its items.

## Task Authorization

- Carry the user's authorization for the task through its ordinary implementation, verification,
  scoped external changes, retries, recovery, and cleanup. A follow-up, interruption, failed attempt,
  or context reset does not require the user to approve those sub-steps again.
- Treat merge, deployment, publication, and release as separate outcomes outside the ordinary
  scoped external changes above. "Implement this plan" is not an explicit instruction for any of
  those outcomes, even when the plan names the action and target. Before acting, identify the
  user's separate explicit instruction for that action and target or applicable guidance or an
  invoked skill that expressly authorizes it; otherwise complete the reviewable work and leave
  that outcome pending.
- Ask only for a decision that materially changes the authorized target, recipient, or outcome, or
  for an action-time confirmation a platform actually requires. Make that question specific to the
  new decision or action; never ask the user to reconfirm the task or say "continue" to resume it.
- An implementation constraint is not a new approval boundary. Exhaust authorized ways to
  complete a sub-step yourself. Do not mistake an action-time confirmation for a mandatory user
  hand-off: after the user confirms the specific pending action, perform it yourself. Hand off only
  when the platform requires the user's own interaction. Never request a secret through chat.
- After a required confirmation, continue the remaining authorized work without another general
  approval request. A refused or unanswered confirmation blocks only the action it governs, as
  **Work You Have Already Named** says of every wait.

## Browser Access

- Use the user's `@Chrome` browser for browser work. Open a new, agent-owned tab in that same browser
  and keep it in the background when the browser supports that; tab isolation does not mean using a
  different browser, profile, or account. Do not inspect, focus, reuse, or close the user's existing
  tabs. If the user explicitly names a different browser or an existing tab for the task, follow
  that direction instead.
- If `@Chrome` tab control is unavailable, use regular Chrome as the fallback and open a new
  agent-owned tab there. It may come to the foreground; keep the user's existing tabs untouched.
  Continue through an appropriate API or CLI when that is more direct. Report a browser-specific
  blocker only if neither Chrome path can complete the required interaction.

## Environment Refusals

- **An environment refusal is a route to find, not a blocker to report.** A repository missing from
  the session is attached or cloned as a writable checkout; a host the environment refuses is reached
  through a path it does serve, and a tool that took the refused path is fixed to take the served
  one; a command a permission boundary denies is put to the user as that exact approval. Report a
  blocker only once every served path has been tried and has failed.

## Product Constraints

`pre-production` is active in every change task. Read it completely, explicitly invoke it, and
announce the invocation before the first edit. Listing it as a dependency is not an invocation.
Read the repository's product state from its project guidance before choosing how to change a
contract or stored value.

Before editing a language or package, read its applicable shared and repository rules and nearby
analogous files. Match their code grouping and spacing in every new or substantially edited file;
inspect the complete result beside those siblings before delivery. A formatter passing is not a
substitute for that comparison.

## Encountered Issues

Apply `pre-production`'s encountered-issues policy while making the change. The rules below govern
how those issues are handled.

- **A bug the work turns up, or a finding a gate, review, or simplification pass returns, is fixed in
  the change in flight, and offering it to the user is not a disposition.** "Want this handled, or
  shall I leave it?" reads as diligence and is the failure this section exists to prevent: it spends
  a turn to obtain permission for something already required, and a no leaves a known defect in the
  tree with the agent's name on the decision. The question that
  is genuinely the user's is about a **product change** — what a feature does, what a record keeps,
  who a surface serves, a contract a consumer outside the user's control speaks — never whether an
  encountered issue gets fixed.
- Being found rather than assigned, or predating the change — older code in a file the work
  touches, a gap a gate labels pre-existing — changes nothing about whether it is fixed; it changes
  only where the fix lands, which is the branch in flight. Say in the report what was fixed and why it
  was in the path of the work, so the reviewer sees a decision rather than a surprise.
- What puts a **new** issue in that path is an act the work performed: a file it opened, a command
  it ran, a check it read, a review it received. How far the fix then reaches is a different
  question, and `pre-production`'s **Scope Follows The Defect, Not The Request** answers it.
- Never reject a fix solely because it is described as high risk. Assess its expected net effect,
  concrete failure modes, and available validation instead of treating the label as a stop rule.
- Fix and verify a non-defect improvement when the correction can be completed in one focused pass
  and produces an overall net gain: removing a code smell, simplifying the implementation, or
  applying the target-contract policy from `pre-production`. A defect, or a finding a gate, review,
  or simplification pass returns, is governed above and carries no such condition.
- Delete every piece of confirmed dead code encountered during implementation, even when it sits
  outside the files or packages already being changed. Confirm that no live application or
  library consumer, public export, or external contract still depends on it; remove tests that
  exist only to exercise the dead code; and validate the affected behavior. This requirement does
  not turn implementation into a proactive dead-code audit of the whole repository.
- Use the repository's relevant tests as the regression guardrail; do not preserve a defect solely
  because an existing test asserts the old behavior. When coverage is absent or insufficient, use
  the strongest available validation and account explicitly for the uncovered behavior.
- One focused pass means the correction needs no separate research or design phase and is not
  expected to require multiple implementation iterations.
- Apply an owned API, protobuf, schema, payload, or stored-shape change selected by
  `pre-production` without a second approval; update every consumer the user controls, in
  whichever repository it lives, plus every generated artifact and required migration for the
  target contract.
- Apply **Task Authorization** to encountered corrections. Ask only when the correction is a product
  change as the first bullet defines it, changes security or disclosure posture, reaches a
  repository, environment, or external recipient the task did not authorize, or a platform requires
  action-time confirmation. Another file, component, or package in the same repository is never a
  new target, and neither is a repository the user owns that consumes a contract the change breaks:
  it is delivered under **Multi-Repository Delivery**. For a bug or a returned finding the fix
  proceeds and is not held for an answer; what goes to the user is scope, sequencing, and where the
  work lands, never whether it is fixed.
- When asking, state the trigger, impact, expected work, recommendation, and concrete choices.

## CI Gates And Deliberate Breaks

Some required checks exist to detect deliberate changes: contract compatibility, schema
compatibility, generated-output drift.

- Such a gate going red is an accepted, reported outcome of an intentional break, never a reason
  to reshape the change.
- Never weaken the gate to recover green: no ignore lists, no exception entries, no reserved
  placeholders faking compatibility.
- Report it instead. State in the pull request that the break is deliberate and list exactly what
  the gate reported, so a reviewer can confirm nothing unintended is in the diff.
- Do not let a green run drive design. Choosing a wider or additive shape so that a gate stays
  green is the same defect as suppressing the gate.

## Ongoing Simplification

Read and invoke `code-simplify` as the change is made — after each meaningful implementation batch
— and once across the complete diff before delivery. It is not a single pass held back for the end.

- Every pass covers three things, never the diff hunks alone: the **changes** themselves, the
  **similar code** they resemble, and the **sibling modules** around them.
  - **Changes**: the full contents of every file the task has touched so far, not only the lines
    edited in the current batch.
  - **Similar code**: every other place in the repository already expressing the same concept,
    shape, or operation as the changed code — a near-duplicate helper, a parallel implementation,
    a second representation of one value. Search by concept and by key operation, not by filename;
    a sibling-only read cannot find the canonical implementation another package owns. Where the
    change and the code it resembles should be one thing, make them one thing.
  - **Sibling modules**: the other modules in each changed file's package, which is where a
    misplaced piece of logic and its rightful home become visible together.
- When simplification or dead-code deletion changes another file, add that file's full contents,
  its similar code, and its sibling modules to the scope recursively before continuing.
- Resolve the final pass the same way, from the complete diff.
- Apply every simplification that produces an overall net improvement, using `pre-production` for
  contract decisions; ask only about one that meets **Encountered Issues**' condition for asking.

## Pre-Push Gate

Before the branch is pushed, and again before each later push that carries new work, run over the
whole branch diff against its base — committed and uncommitted work alike, with no pull request
required — first the final `code-simplify` pass above, applying its simplifications directly, then
`acceptance-gate`'s diff question with the change's intent statement, then the repository's fast
checks: lint, type checks, the unit tests of the changed packages, and any check a skill in use
requires before a push. Fix what they flag, re-run the acceptance gate once, and re-run the checks
until they pass. Commit the edits before pushing. A branch whose diff holds only dot-files and
dot-directories, `.github` aside, skips the simplification pass and the acceptance gate; the checks
still run.

- **Push each coherent unit of work as soon as its gate is clean.** A push is what lets the user
  review and test the work, so a gated commit held locally withholds that review.
- **The order is change, gate, push, then the slow verification**: a browser walkthrough, a full or
  end-to-end suite, a run against a service without the change, root-causing a failure the change
  did not cause — anything slow or needing a running stack. What it finds goes out as fix pushes,
  each through its own gate.
- **Pushed is not done**: the change is reported done only once that verification has passed.
- **Never hold a gated commit** to batch it with pending work, to wait for another approval, or to
  save a gate run. A second gate over a small later push is cheap; hours of unpushed work are not.

## Reported Outcomes

An outcome is what its source of truth shows, never what an action or a worker said about it.

- **After any action that changes shared state, read the resulting state before reporting it or
  starting the next item.** A push, merge, deployment, migration, or refresh reports that it ran,
  not the state it left, so read that state where it lives. After a push, that is the pull request
  on the pushed head: its mergeable state and its checks starting, since the base can move while
  the push runs.
- **Whatever that read shows wrong is the next thing done**, ahead of every queued item, and is
  never carried to "the next push" or bundled behind other work. A conflict or a moved base is
  brought in through `merge-conflict`, gated under the **Pre-Push Gate**, pushed, and read back.
- **A delegated worker's report of an outcome is a claim, never evidence.** Before relaying it or
  building on it, check it at its source: "tests pass" against the run or the CI result on that
  commit, "pushed" or "exists" against the branch, "merged" or "refreshed" against the default
  branch or the installed copy, "deployed" or "healthy" against the host, "fixed" by reproducing it
  or reading the evidence, "the screenshot shows it" by looking at the image, "no references
  remain" by searching. A claim the check contradicts is the next thing done, ahead of queued
  work: sent back to the worker with what the read showed, or fixed here.
- **A deferral inside a report — "I'll do X next" — is named work of this run** under **Work You
  Have Already Named**, tracked until done; the report does not close it.
- **A status sent to the user states what was just read and where**, never what was reported or
  expected: conflicted, failing, running, or passing, on the head or target named. "Done" or
  "ready" is written only when that read says so.

## Pull Requests

The GitHub rule's **Branches and Pull Requests** decides where each piece of work lands: per
repository and session, one pull request for source and one for agent configuration, every later
request joining the open one of its kind, never one per task. A guidance change never rides the
source branch in flight, however closely it follows that work. Check the session's open pull
requests in a repository before creating any branch there, and say in chat what was consolidated
when a stray one is folded in.

## Multi-Repository Delivery

When one change spans multiple repositories, treat each repository as an independent delivery
context, with **Pull Requests** applying inside each of them.

- Invoke `generic-push` separately for each repository before committing or publishing.
- Write every branch name, commit message, pull-request title, pull-request description, review
  comment, code comment, and repository-local report solely from that repository's perspective.
- Do not name, link, describe, or explain another involved repository, its branch, pull request,
  implementation, or coordination context in those artifacts.
- Keep cross-repository coordination and combined status reporting in user chat.

## Each Repository Speaks Only Its Own Vocabulary

The delivery rule above governs the artifacts around a change. This one governs what goes **inside**
it, and it binds in every repository the run touches whether or not that repository's own rules say
so — a repository with no independence rule of its own is the one most likely to be given another's
words.

**Never write another repository's nouns into this one.** Its product name, its services, its
skills, its tables and columns, its record types, its routes, its identifiers, the words its
business speaks: all of them stay where they are. That holds in source, tests, fixtures, sample
data, error messages, comments, and documentation alike, and it holds hardest in a library or a
tool, where every reader is a different consumer who has never heard of the repository the author
happened to come from.

**An example is where this fails, because an example needs a name and the author has one to hand.**
Documenting a folder layout, a config key, a path shape, or a call, the concrete thing the author
just saw is the nearest name and the worst one: it reads as this tool's own vocabulary to everyone
after them, and it goes stale the moment that other repository renames it. Invent the name instead.
An example naming a real artifact of another repository is the defect, however accurate it is.

Name things for the shape being demonstrated, never for whichever caller prompted the work. A
consumer's needs are a legitimate reason to build something and never a reason to name it after
them. Describe the target repository's own contract and behavior to reviewers; keep
consumer-specific coordination in user chat, following the Multi-Repository Delivery rule above.

Where this run touched more than one repository, sweep for it before delivering: search each
repository for the distinctive nouns of the others it was worked on beside, and read what comes
back. A borrowed name is invisible to the author precisely because it was familiar.

## Work You Have Already Named

**Naming work as next is a commitment, and it stays this run's obligation across every later turn**
— including a turn whose own request changes no files, which would otherwise not run this skill at
all. The run that named the work owns it until it is done, and naming it is what keeps the run open
under **One Run Per Task**.

**A new request, an interruption, or a context summary cancels none of it**, and the work each one
displaces is named work whether or not a report named it: an approved plan short of its last entry,
commits a remote lacks, a checkout left mid-edit. The turn that serves the new request also moves
it — the user asking about something else is not the user withdrawing what they asked for before.

- **Write it down before anything else starts.** The displaced work goes into the session's task
  list, with its next step, before the first step of whatever displaced it.
- **An interruption pauses the step in flight; it never ends the run.** "Continue", or anything
  meaning it, resumes exactly that step, and is never answered with nothing.
- **A context summary's pending list is this run's named work**, not background. The first turn
  after it moves the oldest item as well as whatever the summary's next step names.
- **Commits a remote lacks are undelivered work**; their next step is the pre-push gate and the push,
  whatever the gate's size. A hook or status line counting unpushed commits that have passed their
  gate reports a push owed now, not something to explain.

**The failure is a report, not a refusal.** It reads as diligence: the item appears under "still to
do", the turn ends, the next message arrives, and the item appears again, unchanged, in the next
report. Nothing was declined and nothing was done, and each repetition makes the next one easier,
because the item now looks like a standing note rather than work somebody is waiting for.

So the test is the item's own line. Before a report goes out, compare each outstanding item against
the line the last report carried for it. **A line that has not changed means the item is finished in
this turn, before the report is sent** — not moved a little, and not dropped from the list, which
is the same failure with the evidence removed.

An item may leave that state three ways, and each is stated in its own line:

- it is done;
- a blocker holds it, named — and a question put to the user and not yet answered is a blocker, as
  is an authorization this session does not hold;
- it is no longer work, because the user withdrew it or a later request superseded it, said with
  that reason.

**A wait blocks only the work that depends on what is awaited.** While one item waits on something
outside the run's hands — a background agent, CI, a review, a build, the user's answer to one
question or confirmation — start the authorized, already-named work that neither needs the awaited
result nor touches the files or resources the awaited work is changing. Each item held for the wait
names what it uses that only the awaited result will supply, and one with nothing to name starts
now: coming later in the plan, belonging to the same feature, or consuming a shape already agreed
with the awaited work, such as a planned contract, is not such a thing, so build against that shape.
A turn that ends on "still waiting on X" while such work exists is the failure above, and a status
report is not a stopping point. Only when every remaining item depends on the awaited result does
the turn end on the wait.

## Completion

Before declaring the task done:

1. Verify every requested outcome and every automatic incidental fix.
2. Confirm tests and relevant validation cover every incidental fix and simplification, and that
   intentional contract changes are reflected in the expected behavior.
3. Confirm multi-repository delivery artifacts describe only their owning repository.
4. Report the implementation, encountered fixes, simplification passes, validation, and any
   unresolved decision awaiting the user.
