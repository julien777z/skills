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
  the task's report; nothing in the task re-enters it.
- A skill that lists this one as a dependency — `plan-change` does — invokes it once, and the
  skills this one invokes never invoke it back: `i-have-adhd`, `pre-production`, `code-simplify`,
  `acceptance-gate`, and `generic-push` are leaves of this run. A second invocation while one is
  active does nothing more than continue the active run.
- This skill never invokes `plan-change`. Where a task needs a plan, `plan-change` runs first and
  invokes this skill once the plan is approved.
- A read-only task — a question answered from the code, a listing, a report with no edit — does
  not run this skill.

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
- Ask the user before fixing an issue that requires architectural work, a broad refactor,
  migration, new dependency, substantial investigation, product intent, destructive action,
  or expanded authority. For a bug the fix proceeds and is not held for an answer; what goes to the
  user is scope, sequencing, and where the work lands, never whether it is fixed.
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

## Multi-Repository Delivery

When one change spans multiple repositories, treat each repository as an independent delivery
context.

- Invoke `generic-push` separately for each repository before committing or publishing.
- Write every branch name, commit message, pull-request title, pull-request description, review
  comment, code comment, and repository-local report solely from that repository's perspective.
- Do not name, link, describe, or explain another involved repository, its branch, pull request,
  implementation, or coordination context in those artifacts.
- Keep cross-repository coordination and combined status reporting in user chat.

## Completion

Before declaring the task done:

1. Verify every requested outcome and every automatic incidental fix.
2. Confirm tests and relevant validation cover every incidental fix and simplification, and that
   intentional contract changes are reflected in the expected behavior.
3. Confirm multi-repository delivery artifacts describe only their owning repository.
4. Report the implementation, encountered fixes, simplification passes, validation, and any
   unresolved decision awaiting the user.
