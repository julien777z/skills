---
name: acceptance-gate
description: Judge an issue, a finding, a proposal, or a diff against the product's state, a change's stated intent, and the repository's quality rubric through a read-only subagent that answers one question with a specific verdict. Use to triage whether work is fixed now, done, deferred, or closed as not worth doing; before recording a deferral; before and after fixing a would-be deferral or resolving a recorded one; after merging or rebasing the base branch into a change; once over a finished task's complete diff before reporting local completion or its pull request leaves draft or merges; and on the fix for a flag a gate or review raised.
short_description: 'Have an independent reviewer decide whether a proposed change fits the task and the repository.'
---

# Acceptance Gate

Put a decision the author cannot judge about its own work to a subagent that reads the product's
state and the change's intent, applies the repository's rubric, and answers one question.
`references/rubric.md` holds what it judges by; this file holds how it is run.

## Dependencies

- `subagent-selection` — route the gate through a subagent of the running session.
- `list-prs` — the caller supplies verified task-work pull requests for cross-repository context.
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

When work changes an owned boundary, the statement quotes the applicable target-contract instruction,
names the one canonical representation, and identifies every retained or candidate representation of
that boundary. The gate cannot accept an abstract summary in place of that receipt; a second consumer
layout, branch, probe, fallback, or compatibility helper is a flag unless the user explicitly approved
retaining it.

`references/rubric.md` states what the statement names and how its inputs are reconciled. Read product
state from the target repository's project guidance; never import another repository's assumptions.

## The Gate Subagent

Before dispatch, the caller reconciles the ongoing task through `list-prs` or reuses its still-current
verified result. The affected-repository map includes the current heads and relevant code of
applicable task pull requests, not only default-branch or local checkout comparisons. The gate
checks analogous implementations and the evidence for retained differences; missing applicable
pull-request context is a flag to obtain that context, not permission to assume consistency.

The gate is read-only and distinct: not the author of the item, and not the subagent that answered an
earlier question about the same item. It receives five things and nothing else:

1. the intent statement;
2. the originating diff, with its deletions first;
3. the item under judgement — an issue or finding, a proposal, a diff, an incoming base diff, or a
   record;
4. the affected-repository map required by `code-simplify`'s **Trace Changed Flows**;
5. exactly one question from the list below.

**The gate has no shell, so every diff reaches it as content, never as a reference.** The caller
pastes the originating diff and a diff item into the prompt, or writes each to a file the prompt
names, with deletions intact; a commit range, a branch name, or a `git` command leaves the gate
judging a working tree that other edits may have moved, or nothing at all. Dispatch it on the
host's largest model, named explicitly.

**Its first act on any diff is five greps.** Before reading the diff for anything else, grep its added lines for five shapes and list
every hit as a finding ahead of all others, with the remedy the rubric names:

1. **A reader reaching through a table keyed by a model, class or type for a fact about the key**
   — the pattern `[A-Z_]+\[` followed by a model, record, class, `type(` or `cls` expression, as in
   `FORM_TYPES[model].label` or `KINDS[type(record)]`. Each hit is a finding whether or not the diff
   added the table: the value belongs on the key as a class attribute or property, every reader
   moves onto it, and the table goes.
2. **A repository-wide fact held as a loose string** — an email address, a street address, a legal
   entity or product name in a string literal outside one typed model in the package every consumer reads. Each hit
   moves onto that model, which every consumer reads.
3. **A container declared for one member** — `APIRouter(` (or the framework's router constructor)
   in an added line, followed by a count of the handlers registered on that router in the resulting
   tree. One handler is a finding whether or not the diff added the router: the handler moves onto
   the router that already owns its resource, at a path under that resource, and the router and its
   module go. A prefix ending in a verb or an operation is the same finding read from the URL.
4. **A data-holding class declared outside model ownership** — every added `BaseModel`, dataclass,
   named tuple, or equivalent record declared outside a `models.py` file or `models/` package. Move
   it to a concept-specific model module. Only a Pydantic `BaseSettings` class is configuration and
   belongs in `config.py` or `config/`; registries, manifests, policies, provider payloads, and
   response schemas remain models. Never move a model into operational code merely to eliminate a
   one-symbol declarative module.
5. **A typed parameter built as a dict** — an annotation on a dict literal, `name: SomeTypedDict = {`
   or `params: sdk.params.X = {`, and a bare dict passed where an SDK or repository signature names a
   `TypedDict`, at any nesting level. Each hit is rewritten as the constructor call
   (`sdk.params.X(...)`, `sdk.RequestOptions(...)`), with tests asserting the same way.

A report that lists no hit for any of the five greps says so in those words.

**Then it lists every guard, refusal, validation, or branch the diff adds with the writers of the
value it tests and of what its path reads next**, by path and function, and flags each one the
rubric's diff test flags. For an owned boundary, it also names every representation each path reads
or writes and flags a second representation, including one hidden behind a helper. A verdict with no
added guard says `no guard added` in those words.

For a diff question, also apply the `code-simplify` rubric’s **Trace Changed Flows** to the supplied
implementations, consumers, and affected-repository map. A diff alone that cannot establish that
receipt needs those contents from the caller before a clean verdict; a prose-only change names no
executable flow but still receives a map of affected guidance owners. Flag a missing, unsupported,
or incomplete map rather than treating the reviewed checkout as the complete system. Report its
findings in the verdict and summarize clean flow evidence under `Also read`.

It returns the verdict its question defines, shaped as `references/rubric.md` — What A Verdict Names
requires.

The gate always runs as a subagent of the running session, routed as `subagent-selection`'s
**Dispatch** section directs.

## Questions

Exactly one per gate, each decided by the tests in `references/rubric.md`, with nothing appended.
Whether an item is the change's doing or predates it is never asked, since no disposition turns on
it:

- **Triage — what should happen to this?** An issue, a finding or a proposed record; the answer is
  one of fix, close, defer or do.
- **Admission — may this work be deferred?** The triage question asked of a proposed record.
- **Proposal — should this be written?**
- **Diff — should this stand?** A finished task's diff, or the increment fixing a flag, read with
  the whole branch diff as its originating diff.
- **Base incorporation — what did the base bring in that the change must refactor?** The procedure
  below.
- **Final acceptance — may this merge?** The complete pull-request diff, read once after review is
  clean and before any check gate.

### Base incorporation

Run after every
incorporation of the base this session performed, whether or not Git reports
conflicts. The base advancing remotely without being incorporated does not trigger the check, and
neither does an incorporation another session performed and pushed: that branch has changed hands
under the GitHub rules on branch ownership, and its resolved result is theirs to gate.

1. Record the previous merge-base commit before incorporation and the incorporated base commit.
   Supply both, the originating change with its intent history, and the resolved result. If the
   previous base was not recorded, reconstruct it from commit parents or reflog; do not substitute
   the current merge base and silently review an empty range.
2. Give an independent read-only gate the intent statement, originating diff, and an item containing
   the previous-to-incorporated-base diff plus the resolved tree and correction diff. Inspect cleanly
   merged code and relevant surrounding implementations as well as conflict resolutions. Exclude
   landed immutable migration revisions; their repository-owned migration procedure still applies.
3. The verdict takes the shape the rubric's base-incorporation test requires.
4. Refactor flagged code, whether incoming or an older gap the verdict found in surrounding code,
   through the proposal and diff questions within **Bounds**. Obtain a completed independent verdict covering the resolved result and any corrections before
   declaring reconciliation complete. Record the compared commits and reviewed result with that
   verdict. A missing review or unresolved flag is not acceptance; mergeability and tests are separate
   evidence, and acceptance grants no pull-request merge authorization.

## Bounds

The gate is never advisory; the rubric says what each disposition binds the caller to.

A flag blocks the flagged proposal or diff, not an ordinary repair the task already authorizes.
Read its concrete objection and remedy against the intent and standing guidance, make the smallest
coherent repair using the existing owner or mechanism, and send the changed increment with the
whole originating diff to a fresh independent gate. Continue that repair-and-review path while an
in-scope remedy remains; a second or later flag is not a stop rule or a new approval boundary.

Never rerun an unchanged item hoping for acceptance, argue it through the same gate, rename it to
reset its history, or keep flagged code because the caller can authorize its merge. Carry unresolved
objections and previous remedies into the next review. If evidence refutes an objection, send that
evidence to a fresh gate for an explicit disposition; the caller cannot dismiss it unilaterally.

When no compliant repair is available, name the conflict and the smallest native repair examined.
Apply the rubric's triage and admission tests before reverting, recording, or re-scoping any work;
flag count alone satisfies none of them. A non-defect may be deferred only on those tests' evidence,
including when its simplest compliant repair still requires substantial irreducible complexity or
mechanisms its gain cannot carry. A confirmed defect remains owed under the fix test. A hypothetical
safeguard or compatibility concern is judged against the target repository's product state and
contract, not promoted to a defect merely because a reviewer flagged it.

Escalate only a genuine unresolved product, scope, or authorization choice, stating the concrete
fork and why authorized remedies cannot settle it. Repair authority and merge authority are separate:
a source pull request awaiting merge permission continues through authorized repairs and reviews.
Keep unrelated authorized work moving while a real decision waits. No flagged diff stands or merges
without an independent acceptance covering its resolution.

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

Writers read: <each guard the diff adds with the writers it read, or `no guard added`>

Also read: <additions of other kinds, summarised in one line, or `none`>
```
