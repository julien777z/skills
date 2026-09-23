---
name: execute-task
description: "Always run this. Invoke once, before the first edit, at the start of every task that changes files — including one that only begins changing files because work turned up a defect — and keep it active until the task's report: it shapes every response, applies the repository's product constraints, fixes the bugs the work encounters rather than reporting them, simplifies as the change grows, gates the branch before it is pushed, and delivers each repository independently. Never invoke it from inside a skill it runs."
---

# Execute Task

Run every change the same way, whether a plan preceded it or the user asked for it in one line.

## Dependencies

- `i-have-adhd` — shape every user-facing response for the rest of the session, from the first one
  of the task until the reader's stop phrase. Invoke it at the start of the run when it is not
  already active in the session; a second invocation in an active session changes nothing.
- `pre-production` — the repository's target-contract and staging-data policy, when the repository
  declares one.
- `code-simplify` — simplify each meaningful implementation batch and the complete diff before delivery.
- `acceptance-gate` — judge the complete branch diff before it is pushed.
- `generic-push` — keep each repository's publishing metadata independent during multi-repository changes.

## One Run Per Task

- Invoke this skill once, at the start of a task, before the first edit. A run stays active until
  the task's report, and past it while that report names outstanding work: **Work You Have Already
  Named** keeps the run open until every named item is done or has left that state one of the three
  ways it lists. Nothing in the task re-enters the skill; the run simply has not ended.
- A skill that lists this one as a dependency — `plan-change` does — invokes it once, and the
  skills this one invokes never invoke it back: `i-have-adhd`, `pre-production`, `code-simplify`,
  `acceptance-gate`, and `generic-push` are leaves of this run. A second invocation while one is
  active does nothing more than continue the active run.
- This skill never invokes `plan-change`. Where a task needs a plan, `plan-change` runs first and
  invokes this skill once the plan is approved.
- A read-only task — a question answered from the code, a listing, a report with no edit — does
  not run this skill. It does not close an open run either: a run still holding named work stays
  active through such a turn, and that turn moves its items.

## Product Constraints

`pre-production` is active as soon as the run opens in a repository that declares it. Read it
completely, explicitly invoke it, and announce the invocation before the first edit. Listing it as
a dependency is not an invocation. Where the repository declares none, read its product state from
its project guidance and treat every compatibility question below as one that guidance answers.

## Encountered Issues

Apply `pre-production`'s encountered-issues policy while making the change. The rules below govern
how those issues are handled.

- **A bug the work turns up is fixed in the change in flight, and offering it to the user is not a
  disposition.** "Want this handled, or shall I leave it?" reads as diligence and is the failure this
  section exists to prevent: it spends a turn to obtain permission for something already required,
  and a no leaves a known defect in the tree with the agent's name on the decision. The question that
  is genuinely the user's is about a **product change** — what a feature does, what a record keeps,
  who a surface serves, a contract somebody outside the repository speaks — never whether an
  encountered bug gets fixed.
- Being found rather than assigned changes nothing about whether a bug is fixed; it changes only
  where the fix lands, which is the branch in flight. Say in the report what was fixed and why it
  was in the path of the work, so the reviewer sees a decision rather than a surprise.
- What puts a **new** issue in that path is an act the work performed: a file it opened, a command
  it ran, a check it read, a review it received. How far the fix then reaches is a different
  question, and `pre-production`'s **Scope Follows The Defect, Not The Request** answers it.
- Never reject a fix solely because it is described as high risk. Assess its expected net effect,
  concrete failure modes, and available validation instead of treating the label as a stop rule.
- Fix and verify a non-defect improvement when the correction can be completed in one focused pass
  and produces an overall net gain: removing a code smell, simplifying the implementation, or
  applying the target-contract policy from `pre-production`. A defect is governed above and carries
  no such condition.
- Delete every piece of confirmed dead code encountered during implementation, even when it sits
  outside the files or packages already being changed. Confirm that no live application or
  library consumer, public export, or external contract still depends on it; remove tests that
  exist only to exercise the dead code; and validate the affected behavior. This requirement does
  not turn implementation into a proactive dead-code audit of the whole repository.
- Use the repository's relevant tests as the primary regression guardrail. Add or update tests for
  the intended contract and run them; do not preserve a defect solely because an existing test
  asserts the old behavior. When coverage is absent or insufficient, use the strongest available
  validation and account explicitly for the uncovered behavior.
- One focused pass means the correction needs no separate research or design phase and is not
  expected to require multiple implementation iterations.
- Apply an owned API, protobuf, schema, payload, or stored-shape change selected by
  `pre-production` without a second approval; update every in-repository consumer, generated
  artifact, and required migration for the target contract.
- Ask only when a correction needs user-owned product intent, a security or disclosure decision,
  destructive action, expanded external authority, or an architectural decision that
  `pre-production` does not settle. For a bug the fix proceeds and is not held for an answer; what
  goes to the user is scope, sequencing, and where the work lands, never whether it is fixed.
- When asking, state the trigger, impact, expected work, recommendation, and concrete choices.
- Continue independent approved work when the unresolved issue does not block it.

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
- Apply simplifications that produce an overall net improvement and can be completed and verified
  in one focused pass, using `pre-production` for contract decisions.
- Ask the user about larger or decision-dependent simplifications before applying them.

## Pre-Push Gate

Before the branch is pushed, and again before any later push that carries new work, run over the
whole branch diff against its base — committed and uncommitted work alike, with no pull request
required — first the final `code-simplify` pass above, applying its simplifications directly, then
`acceptance-gate`'s diff question with the change's intent statement. Fix what the gate flags and
re-gate once. Commit the edits before pushing. A branch whose diff holds only dot-files and
dot-directories, `.github` aside, skips both.

## One Pull Request Per Repository

**A session opens one branch and one pull request in each repository it touches, and every later
request joins it.** The unit is the repository and the session, never the task: a new thing the user
asks for mid-session is more work for the branch already in flight there, whatever it is — a feature
beside a fix, a documentation change beside both, a second option in the same file.

Before creating any branch, check whether this session already has one in that repository. Creating a
second is the failure this section exists to prevent, and the reviewer pays for it: two pull requests
in one repository that must be read together, merged in order, and kept from conflicting.

Three things earn a separate branch, and nothing else does:

- the user asks for that work to be held apart;
- the session's pull request in that repository has already merged, so the work starts from the
  freshly fetched default branch;
- the change is agent configuration, which goes to the default branch on its own under the GitHub
  rules, because the next session reads it rather than shipping it.

**"It could be reviewed on its own" is never a reason, and neither is a feeling that the new work is
a different kind of thing.** Both are always available — every added option, every fix, every
rewritten paragraph could be read alone — so a rule that yields to them yields always, and the
session ends with a pull request per request. When a reason to split arrives, check it against the
three above by name; anything else is this rule being argued with rather than applied.

**Having already opened the second one is not a reason to keep it.** Move its commits onto the branch
already in flight, close it saying where the work went, and say in chat what was consolidated.

## Multi-Repository Delivery

When one change spans multiple repositories, treat each repository as an independent delivery
context. The rule above applies inside each of them: one branch and one pull request per repository,
not one per repository per task.

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
them; where their specifics matter to a reviewer, they belong in the pull request description, which
is read once, rather than in code and documentation that outlive the conversation.

Where this run touched more than one repository, sweep for it before delivering: search each
repository for the distinctive nouns of the others it was worked on beside, and read what comes
back. A borrowed name is invisible to the author precisely because it was familiar.

## Work You Have Already Named

**Naming work as next is a commitment, and it stays this run's obligation across every later turn**
— including a turn whose own request changes no files, which would otherwise not run this skill at
all. The run that named the work owns it until it is done, and naming it is what keeps the run open
under **One Run Per Task**.

A new request does not cancel it. The two queue together, and the turn that serves the new one also
moves the old one — the user asking about something else is not the user withdrawing what they asked
for before.

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

## Completion

Before declaring the task done:

1. Verify every requested outcome and every automatic incidental fix.
2. Confirm tests and relevant validation cover every incidental fix and simplification, and that
   intentional contract changes are reflected in the expected behavior.
3. Confirm multi-repository delivery artifacts describe only their owning repository.
4. Report the implementation, encountered fixes, simplification passes, validation, and any
   unresolved decision awaiting the user.
