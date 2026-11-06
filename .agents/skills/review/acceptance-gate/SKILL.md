---
name: acceptance-gate
description: Required checkpoint over an authorized change's complete diff before local completion, draft readiness or merge; run as a workflow dependency without a separate user invocation. Passing tests or an informal self-review never substitute for its verdict; an in-process gate still runs this skill's question and rubric. Judge an issue, finding, proposal or diff against product state, intent and the quality rubric through a read-only subagent, or in process for the primary agent's own plan step; a worker that cannot launch one hands it up to its delegating agent. Run over each finished plan step or worker task before later work builds on it, for triage, before recording a deferral, before and after fixing or resolving one, after base incorporation, and on a fix for a gate or review flag larger than a small repair.
short_description: 'Have an independent reviewer decide whether a proposed change fits the task and the repository.'
---

# Acceptance Gate

Put a decision the author cannot judge about its own work to a subagent that reads the product's
state and the change's intent, applies the repository's rubric, and answers one question. The one
exception, a plan step the primary agent made itself, is gated in process, as **The Gate Subagent**
says.
`references/rubric.md` holds what it judges by; this file holds how it is run.

## Dependencies
- `subagent-matrix`
- `list-prs`
- `code-simplify`
- `security-audit`
- `pre-production`
- `test-fixture`
- `run-site`

## The Intent Statement

Apply `pre-production` to the scope decision, `test-fixture` to test costs and existing reporting
evidence, and `run-site`'s **Scenarios** to changes that add or alter product states.

Apply `security-audit` at `low` effort as a single in-process rubric pass without delegated agents; take its exploitable findings into the verdict.

The caller produces the statement once per change, updates it when accepted requirements or the
user's scope change, and passes it to every gate. The gate judges within the scope the user set,
as the statement records it: work the user cut is reported as out of scope, never flagged as work
the change owes; a defect the change itself introduces is never outside it. A
caller without one supplies the requirements and history so the gate can derive it. A removed shape
is a finding throughout the change, including corrections and base reconciliation. Pure additions
and bug fixes still have requirements for the gate to evaluate. Where no change is in flight, say so
and judge the item on product state and the rubric.

When work changes an owned boundary, the statement quotes the applicable target-contract instruction,
names the one canonical representation, and identifies every retained or candidate representation of
that boundary. The gate cannot accept an abstract summary in place of that receipt; a second consumer
layout, branch, probe, fallback, or compatibility helper is a flag unless the user explicitly approved
retaining it.

The owned-boundary receipt distinguishes the actor or execution owner from its destination and
names the permitted resources and prohibited placements, disclosures or writes. Trace the actual
selectors, configuration and lifecycle to the resolved identities and scopes, with evidence that
they match the accepted contract and one counterexample the implementation must reject. For a
runtime connection, follow each affected process's actual client construction, endpoint and
transport through startup to the observed connection; a credential or another component's listener
establishes capability, not that process's route. A name,
alias, package move, permission grant or test fixture repeating the implementation's assumption
does not prove ownership or isolation. Missing evidence holds a clean verdict; it does not turn
the implementation into the specification.

For every changed or newly resolved dependency, provider, generated contract, shared package, or
other boundary owner, complete the dependency-authority receipt in `references/rubric.md` before a
clean verdict. First reconcile a mismatch between the declared and loaded source: a workflow, cache,
checkout, or resolver that loads another branch is a dependency-routing defect, not evidence that a
consumer must migrate.

An unmerged pull request, proposed branch, or future release is candidate evidence only. It cannot
establish a target contract, satisfy a required repair on another target, or be assumed to merge
unless the user explicitly makes it a dependency.

Once the resolved sources agree, compare consumer migration with changing the owner before accepting
either. Broadening an owner, adapter, generic bound, schema, or validation solely so an owned
consumer's previous input still passes is compatibility even when it adds no branch or fallback.
Flag it unless the evidence establishes that broader input is the owner's independent target
contract or the user explicitly authorized the retained compatibility. Matching runtime behavior
does not establish that a consumer satisfies a type, API, or generated-contract constraint. The
ordinary remedy corrects dependency selection or, when the resolved target contract is current,
updates every owned consumer and removes its obsolete representation.

`references/rubric.md` states what the statement names and how its inputs are reconciled. Read product
state from the target repository's project guidance; never import another repository's assumptions.

## The Gate Subagent

Before dispatch, the caller reconciles the ongoing task through `list-prs` or reuses its still-current
verified result. The affected-repository map includes the current heads and relevant code of
applicable task pull requests, not only default-branch or local checkout comparisons. The gate
checks analogous implementations and the evidence for retained differences; missing applicable
pull-request context is a flag to obtain that context, not permission to assume consistency.

The gate is read-only and normally distinct from the author. A plan step the primary agent made
itself is gated in process instead, under the caller's step gates, because the task's final
acceptance reads every line again. If its reader cannot launch, apply `subagent-matrix`'s launch
fallback. Invoke `subagent-matrix` for the
acceptance-gate role, using its configured Codex role selection and the advanced capability level on
other hosts. Dispatch the gate with that exact identifier, and retain catalogue state, identifier, assignment
state and host receipt in the gate record. Its reader freshness follows `subagent-matrix`'s **Dispatch**. It
receives five things and nothing else:

1. the intent statement, quoting the user's request in their words and carrying every decision the
   task has recorded that the item's subject touches, with the user's words, so earlier settled
   behaviour is not judged as new and scope is judged against what the user asked;
2. the originating diff, with its deletions first; for a Proposal before implementation when no
   change is in flight, explicitly declare that no implementation diff exists and name the current
   source snapshot instead; every Diff, Final acceptance and Base incorporation still requires its
   actual immutable diff;
3. the item under judgement — an issue or finding, a proposal, a diff, an incoming base diff, or a
   record; a diff that adds or changes tests carries the cost evidence from its verification run
   under `test-fixture`'s existing-reporting procedure, including any unmeasured attribution;
4. the affected-repository map required by `code-simplify`'s **Trace Changed Flows**;
5. exactly one question from the list below.

**The gate has no shell, so every diff reaches it as content, never as a reference.** The caller
pastes the originating diff and a diff item into the prompt, or writes each to a file the prompt
names, with deletions intact; a commit range, a branch name, or a `git` command leaves the gate
judging a working tree that other edits may have moved, or nothing at all. Its selector receipt is the
model-dispatch record; never replace it with a generic “largest model” label.

**A diff review judges the code as it stands, not only the lines that changed.** Read every module
the diff adds, moves or rewrites whole; moved and renamed code is judged as if it were new. Before
the design comparison, answer the plain question: would an experienced reviewer opening these
modules call any of it slop? Each reason they would give is a flag with its remedy, whether or not a
narrower rule below names it: layers that each add one tweak, wrappers that only forward or fix a
value, one-symbol fragments, a file for a slice of a concern another module owns, one thing
implemented twice, comments narrating code, confusing or near-duplicate names, dead or speculative
code, hand-written configuration or styling where an owner exists. The list illustrates the question
and never bounds it. A rubric exemption that would excuse such a shape is named in the flag. A
remedy that sends the author to an existing piece judges that piece the same way first: a wrapper or
a duplicate is not an owner. An increment fixing an earlier flag is judged on the earlier flags it
answers and on its own lines, read the same way, never only against that flag; the rest of the
modules it touches and of the originating diff, which the earlier gate judged, is context, open to a
new flag only where the increment changes what it depends on or it holds a confirmed defect or
exploitable vulnerability.

**Then make the design comparison.** Inventory the responsibilities and decisions the diff moves,
duplicates, specializes, removes or introduces, reading both sides independently of the caller's
rationale. Follow each prior selected or computed answer to every resulting use, counting independent
selections, copies and repeated work even inside one file; a canonical file is not proof of canonical
decision ownership. Apply the rubric's **Independent Judgment** comparison to those owners and
consumers, including for prose and configuration. Complete the comparisons despite earlier flags,
and name the exact missing input and investigation for any remaining choice. Return the comparisons
and deciding evidence in the existing verdict fields; a checklist or stage inventory alone is
incomplete.

**Make the simpler candidate concrete.** For each suspect shape, apply the rubric's removal test
before accepting it. Return the concrete consolidation or deletion, or the actual current contract
that the simpler complete candidate would break. Missing validation evidence is a separate flag,
never a reason to leave this judgement unfinished.

**Trace changed state-like values during the design comparison.** Apply the rubric's **State
Meaning** criteria to their writers, transformations and consumers, including values whose names did
not change. Include the authority, lifetime and purpose evidence in `Also read`, and semantic
collisions in the flag bullets; missing evidence prevents a clean verdict.

**Then run five greps.** Grep the diff's added lines for five shapes and list every hit as a finding
ahead of all others, with the remedy the rubric names:

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

**Then it lists every product choice the diff makes**, as the global rules define one — a change to
what a feature does or shows, a remedy whose visible effect is large, such as a layout, control or
flow changing across many pages, a change carried past the surface the user named — each with the
user's words in the intent statement that settle it. Small presentation decisions on the surface in
hand are not listed, and neither is local test tooling or the records it seeds, which the global
rules' local-stack bullet leaves to the agent. A product choice with no such words is a flag whose
remedy is putting the choice to the user before the code stands, whatever the step calls itself, a
fix included. An earlier accepted step, a plan record without the user's words, or a brief calling
the choice decided is not those words. A verdict with none says `no product choice added` in those
words.

For a diff question, also apply the `code-simplify` rubric’s **Trace Changed Flows** to the supplied
implementations, consumers, and affected-repository map. A diff alone that cannot establish that
receipt needs those contents from the caller before a clean verdict; a prose-only change names no
executable flow but still receives a map of affected guidance owners. Flag a missing, unsupported,
or incomplete map rather than treating the reviewed checkout as the complete system. Report its
findings in the verdict and summarize clean flow evidence under `Also read`.

It returns the verdict its question defines, shaped as `references/rubric.md` — What A Verdict Names
requires.

Route the gate through `subagent-matrix`'s **Dispatch**, including its launch fallback when the
required reader cannot launch.

For a canonical guidance batch, one fresh gate may inspect the complete frozen diffs together and
return a distinct verdict for each exact head. Its prompt names every head and intent, and its
evidence retains the per-head disposition. Retain an earlier per-head acceptance only while that
head, its inputs, and its affected-repository map remain exact; rerun the changed head and its
dependent gates without invalidating unrelated batch heads. A shared question never lets an author
judge their own work or collapse distinct verdicts.

## Questions

Exactly one per gate, each decided by the tests in `references/rubric.md`, with nothing appended.
Whether an item is the change's doing or predates it is never asked, since no disposition turns on
it:

- **Triage — what should happen to this?** An issue, a finding or a proposed record; the answer is
  one of fix, close, defer or do.
- **Admission — may this work be deferred?** The triage question asked of a proposed record.
- **Proposal — should this be written?**
- **Diff — should this stand?** A finished step's or task's diff, or the increment fixing a flag,
  read with the whole branch diff as its originating diff.
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
Before admitting a flag, check it against the task's recorded decisions and the commit that
introduced the behaviour it names. A flag that reopens a behaviour choice the user's recorded words
or an earlier accepted step settled, or that asks for work outside the scope the user set, is
answered as settled or out of scope with that evidence; it is never repaired and never put to the
user as a question. Only the user's words settle a product choice: one an accepted step or an
agent-written record holds without them is still open, and goes to the user. A confirmed defect or a
security vulnerability is never settled this way, whatever an
earlier step accepted: it is repaired as below.
Read every other objection and remedy against the intent and standing guidance, make the smallest
coherent repair using the existing owner or mechanism, and send the changed increment with the
whole originating diff to a fresh independent gate, following `subagent-matrix`'s **Dispatch**.

**A small repair is checked in process instead.** A repair is small when it changes about 30 lines or
fewer and carries out the remedy the flag names without settling a design, product or security
choice of its own. The agent that made it re-reads the changed lines against the flag's objection and
remedy, runs the checks covering that code, and records the result with the flag; no fresh gate or
worker is started for it. It still counts as one of the flag's repair rounds, and the next gate over
the step or the complete diff is the independent acceptance covering its resolution. A larger repair,
one that settles such a choice, or one the in-process check cannot settle goes to a fresh gate as
above.

**Repair rounds are counted per objection and per change.** A change gets at most 3 rounds across
every kind of check, the first and 2 after repairs, as the global rules' review-round limit counts
them: once 3 have failed it, whatever each raised, the decision that bullet calls for replaces
another repair, and an acceptance with recorded findings that decision makes is the one exception to
the rules below on flagged diffs; an in-process check of a small repair is not one of those 3
rounds. While the change is under that limit, a flag gets at most two repair rounds of its own, and
one a fresh gate raises for the first time starts at zero. A flag the gate still raises after its
own second repair, with the change still under the limit, goes to the user as a report, never as a
choice about whether to fix it or leave it in place: the open flag, each remedy tried and its
evidence, the gate's proposed remedy and the recommended next step. Every other flag keeps its own
repair and gate meanwhile, and the user's reply directs only the flag the report names.

Never rerun an unchanged item hoping for acceptance, argue it through the same gate, rename it to
reset its history, or keep flagged code because the caller can authorize its merge. Carry unresolved
objections and previous remedies into the next review; a remedy that reverses one given earlier
names it and the evidence it was wrong. If evidence refutes an objection, send that
evidence to a fresh gate for an explicit disposition; the caller cannot dismiss it unilaterally.

When the intent statement already schedules a flag's remedy as named work with its owner, such as
a consumer's migration on its own pull request, the gate reports it as a hold on the merge that
work must precede, not a flag on the step, and it counts no repair round. The hold stays until that
work is accepted.

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

Product choices: <each product choice the diff makes with the user's words settling it, or `no product choice added`>

Also read: <the Independent Judgment comparison receipt, plus additions of other kinds>
```
