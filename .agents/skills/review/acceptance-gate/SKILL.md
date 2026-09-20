---
name: acceptance-gate
description: Judge an issue, a finding, a proposal, or a diff against the product's state, a change's stated intent, and the repository's quality rubric through a read-only subagent that answers one question with a specific verdict. Use to triage whether work is fixed now, done, deferred, or closed as not worth doing; before recording a deferral; before and after fixing a would-be deferral or resolving a recorded one; after merging or rebasing the base branch into a change; and once over the complete diff before a pull request merges.
---

# Acceptance Gate

Put a decision the author cannot judge about its own work to a subagent that reads the product's
state and the change's intent, applies the repository's rubric, and answers one question.
`references/rubric.md` holds what it judges by; this file holds how it is run.

## Dependencies

- `code-simplify` — its `references/rubric.md` defines slop and prices a mechanism. The gate borrows
  that file and never the applying-fixes workflow.
- `security-audit` — run at its `low` effort, which is defined as a single in-process pass against
  its `references/rubric.md` and names no delegated agents, because a read-only gate cannot spawn
  one. The rubric defines what counts as an exploitable finding, what it is worth, and in what order
  to look for the smallest remedy; the gate takes the verdict into its own and never that skill's
  approval gate, tracking, or fixes.

## The Intent Statement

The caller produces the statement once per change, updates it when accepted requirements change,
and passes it to every gate. A caller without one supplies the requirements and history so the gate
can derive it. A removed shape is a finding throughout the change, including corrections and base
reconciliation. Pure additions and bug fixes still have requirements for the gate to evaluate.
Where no change is in flight, say so and judge the item on product state and the rubric.

`references/rubric.md` states what the statement names and how its inputs are reconciled. Read product
state from the target repository's project guidance; never import another repository's assumptions.

## The Gate Subagent

The gate is read-only and distinct: not the author of the item, and not the subagent that answered an
earlier question about the same item. It receives four things and nothing else:

1. the intent statement;
2. the originating diff, with its deletions first;
3. the item under judgement — an issue or finding, a proposal, a diff, an incoming base diff, or a
   record;
4. exactly one question from the list below.

**Its first act on any diff is two greps.** Before reading the diff for anything else, grep its added lines for two shapes and list every
hit as a finding ahead of all others, with the remedy the rubric names:

1. **A reader reaching through a table keyed by a model, class or type for a fact about the key**
   — the pattern `[A-Z_]+\[` followed by a model, record, class, `type(` or `cls` expression, as in
   `FORM_TYPES[model].label` or `KINDS[type(record)]`. Each hit is a finding whether or not the diff
   added the table: the value belongs on the key as a class attribute or property, every reader
   moves onto it, and the table goes.
2. **A repository-wide fact held as a loose string** — an email address, a street address, a legal
   entity or product name in a string literal outside one typed model in the package every consumer reads. Each hit
   moves onto that model, which every consumer reads.

A report that lists no hit for either grep says so in those words.

It returns the verdict its question defines, shaped as `references/rubric.md` — What A Verdict Names
requires.

Where the host has no subagent dispatch, answer the question in process against the same four inputs
and say in the report that the gate ran degraded.

## Questions

Exactly one per gate, each decided by the tests in `references/rubric.md`:

- **Triage — what should happen to this?** An issue, a finding or a proposed record; the answer is
  one of fix, close, defer or do.
- **Admission — may this work be deferred?** The triage question asked of a proposed record.
- **Proposal — should this be written?**
- **Diff — should this stand?**
- **Base incorporation — what did the base bring in that the change must refactor?** The procedure
  below.
- **Final acceptance — may this merge?** The complete pull-request diff, read once after review is
  clean and before any check gate.

### Base incorporation

Run after every
incorporation of the base this session performed, whether or not `cr` is active or Git reports
conflicts. The base advancing remotely without being incorporated does not trigger the check, and
neither does an incorporation another session performed and pushed: that branch has changed hands
under the GitHub rules on branch ownership, and its resolved result is theirs to gate.

1. Record the previous merge-base commit before incorporation and the incorporated base commit.
   Supply both, the originating change with its intent history, and the resolved result. If the
   previous base was not recorded, reconstruct it from commit parents or reflog; do not substitute
   the current merge base and silently review an empty range.
2. Give an independent read-only gate, on the host's largest model tier, the intent statement, originating diff, and an item containing
   the previous-to-incorporated-base diff plus the resolved tree and correction diff. Inspect cleanly
   merged code and relevant surrounding implementations as well as conflict resolutions. Exclude
   landed immutable migration revisions; their repository-owned migration procedure still applies.
3. The verdict takes the shape the rubric's base-incorporation test requires.
4. Refactor flagged incoming code through the proposal and diff questions within **Bounds**. Obtain a
   completed independent verdict covering the resolved result and any corrections before pushing or
   declaring reconciliation complete. Record the compared commits and reviewed result with that
   verdict. A missing review or unresolved flag is not acceptance; mergeability and tests are separate
   evidence, and acceptance grants no pull-request merge authorization.

## Bounds

The gate is never advisory; the rubric says what each disposition binds the caller to.

Each item gets one rewrite against the objection, and the rewritten item goes to a fresh gate. Never
argue one item through the same gate twice, and never re-run a gate until one passes. The second flag
ends the item, and its disposition is the caller's, from these:

- **revert and record** — undo the item and record the work through the repository's deferral
  mechanism with both flags as its reason;
- **re-scope** — solve the part that can be solved cleanly and re-state the record or task for the
  rest;
- **escalate** — put the conflict to the user with the flag quoted, as a blocker. Escalation is for
  a change whose merge needs an authorization only the user holds; it is never how a caller avoids
  a decision.
- **let it stand** — keep the item with the flag's reason answered in the caller's own report. This
  is available only where the change's merge needs no authorization — a pull request confined to
  agent configuration — and there escalate is not: nothing is put to the user.

Work that is the change's own purpose is never reverted and recorded; a second flag on it escalates
where escalate is available, and is otherwise the caller's to fix, let stand, or drop.

## Reporting

Report every verdict with what it named, whether or not the item went on to land. A deferral's
admission verdict is written on its record, and a close's reason and reconsideration criterion on
the cancelled record.

## Output

The gate returns this shape and nothing else; the caller repeats it in its own report:

```markdown
Gate: <question> — <item in one line>

Verdict: accept | flag | fix | close | defer | do

- <for a flag: the quoted line, the shape it takes, the intent or rubric item it violates, and the
  remedy the change itself would take; one bullet per flag>
- <for an acceptance: each addition whose kind matches a removed shape, the shape it takes, and why
  it is neither the removed shape nor a finding; one bullet per addition>
- <for a triage disposition: the test that decided it and the fact it rests on>

Also read: <additions of other kinds, summarised in one line, or `none`>
```
