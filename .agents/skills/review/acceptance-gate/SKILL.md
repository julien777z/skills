---
name: acceptance-gate
description: Independent read-only verdict on a pull request's complete diff before merge, run once per pull request; also for a triage or deferral decision, a list of borderline incidental items, and base incorporation; per plan step only for a finished step that later steps build on. Never run per fix — the repairs of a verdict's defect flags go to one fresh gate, apart from a proposal's, which its calling workflow judges.
short_description: 'Have an independent reviewer decide whether a proposed change fits the task and the repository.'
---

# Acceptance Gate

Put a decision the author cannot judge about its own work to a subagent that reads the product's
state and the change's intent, applies the repository's rubric, and answers one question. It runs
once over a pull request's complete diff, before its merge, and otherwise only for the questions
below that a caller cannot settle alone. A plan step or worker task is gated only when later steps
build on it; every other step, and every fix to a review finding, gets its author's own checks,
while a gate's flag is closed only by a fresh gate under **Bounds**, apart from a proposal whose
calling workflow states how its repairs are judged.
`references/rubric.md` holds what it judges by; this file holds how it is run.

## Dependencies
- `subagent-matrix`
- `list-prs`
- `code-simplify`
- `security-audit`
- `pre-production`
- `test-fixture`
- `run-site`
- `council`
- `skill-pass`

## The Intent Statement

The caller produces the statement once per change, updates it when accepted requirements or the
user's scope change, and passes it to every gate. The gate judges within the scope the user set,
as the statement records it: work the user cut is reported as out of scope, never flagged as work
the change owes; a defect the change itself introduces is never outside it. A
caller without one supplies the requirements and history so the gate can derive it. A removed shape
is a finding throughout the change, including corrections and base reconciliation. Pure additions
and bug fixes still have requirements for the gate to evaluate. Where no change is in flight, say so
and judge the item on product state and the rubric.

The statement carries the receipts `references/rubric.md`'s **What The Intent Statement Names**
lists, and that section says how its inputs are reconciled; a missing receipt holds a clean verdict.
Read product state from the target repository's project guidance; never import another repository's
assumptions.

## The Gate Subagent

Before dispatch, the caller reconciles the ongoing task through `list-prs` or reuses its still-current
verified result. The affected-repository map includes the current heads and relevant code of
applicable task pull requests, not only default-branch or local checkout comparisons. The gate
checks analogous implementations and the evidence for retained differences; missing applicable
pull-request context is a flag to obtain that context, not permission to assume consistency.

**Before dispatch, the caller runs the pre-gate check.** When the Python rules apply, the caller
runs `scripts/python_rule_findings.py` with the project's Python interpreter on the in-scope Python
files, fixes each finding, and each paragraph candidate `pre-production`'s **Code Layout** makes a
boundary, in the lines the change writes or edits, then runs it again. The reader verifies each
reported shape against the source and rule.

The gate is read-only and distinct from the author. If its reader cannot launch, apply
`subagent-matrix`'s launch fallback. Invoke `subagent-matrix` at the capability level
**Questions** gives the gate's question. Dispatch the gate with that exact identifier, and retain catalog state, identifier, assignment
state and host receipt in the gate record. Its reader freshness follows `subagent-matrix`'s **Dispatch**. Its
prompt carries five things and nothing else; what it reads from the tree itself, the paragraphs
after them say:

1. the intent statement, quoting the user's request in their words and carrying every decision the
   task has recorded that the item's subject touches, with the user's words, so earlier settled
   behavior is not judged as new and scope is judged against what the user asked. Include
   explicit requirements and later corrections for any skill or rule the diff touches;
2. the originating diff, with its deletions first; for a Proposal before implementation when no
   change is in flight, explicitly declare that no implementation diff exists and name the current
   source snapshot instead; every Diff, Final acceptance and Base incorporation still requires its
   actual immutable diff;
3. the item under judgment — an issue or finding, a proposal, a diff, an incoming base diff, or a
   record; a diff that adds or changes tests carries the cost evidence from its verification run
   under `test-fixture`'s existing-reporting procedure, including any unmeasured attribution, and
   every diff carries the warnings and deprecation messages its verification runs printed, or an
   explicit empty result. A diff that adds code carries the reuse receipts `code-simplify`'s
   **Before Choosing A Design** check left and the results of a search made with a shell at the
   judged head: for each addition, the terms searched and the candidates found, with a source
   excerpt for each candidate and callee the gate needs to verify its effect. A gate carries
   the reuse search of the review that preceded it when its caller ran one; any other carries the
   caller's own. A
   citation without its source content, or an addition with no search result, is missing
   evidence. For a skill or rule change, include the frozen base and resulting
   package contents and the real case it governs, when supplied;
4. the affected-repository map required by `code-simplify`'s **Trace Changed Flows**. For each
   changed file group, resolve its project guidance, scoped repository rules and installed shared
   rules by path. Supply the complete text and scope of each source inline or in a named file. In a
   repository the owner does not own, as `pre-production`'s **Whose Standards Apply** defines it, the
   brief says so: the gate judges the change against the request, its defects and that repository's
   own guidance and conventions, and a shared rule's standard is no flag there. Supply the
   pre-gate check's file list and every finding it printed, including an explicit empty result;
5. exactly one question from the list below.

**The gate judges with its dependencies' criteria.** Apply `pre-production` to the scope decision,
`test-fixture` to test costs and existing reporting evidence, and `run-site`'s **Scenarios** to
changes that add or alter product states. Apply `security-audit`'s review in process, as an
invocation that cannot launch agents, with no delegated agents; take its exploitable findings into
the verdict. Where the item carries that skill's result for the same range, read the result
against the diff in place of that pass.

**The gate has no shell, so every diff reaches it as content, never as a reference.** The caller
pastes the originating diff and a diff item into the prompt, or writes each to a file the prompt
names, with deletions intact; a commit range, a branch name, or a `git` command leaves the gate
judging a working tree that other edits may have moved, or nothing at all. Its selector receipt is the
model-dispatch record; never replace it with a generic “largest model” label.

**A diff review judges the code as it stands, not only the lines that changed.**

- Read every module the diff adds, moves or rewrites whole; moved and renamed code is judged as if
  it were new.
- A diff that changes a skill or rule is judged as the package it results in: every file of each
  skill and rule it touches is read whole at the head, for the checks `skill-pass`'s **Reviewer
  Brief** assigns the acceptance gate and no other reader's.
- Where the item carries a real case the guidance governs, the gate walks the resulting text through
  it and flags the step a reader would take wrongly.
- Apply the rubric's **Guidance Intent** check. Record the evidence for a clean result under
  `Also read`.
- Before the design comparison, answer the plain question: would an experienced reviewer reading the
  change — its code, configuration and prose, and the verification output supplied — call any of it
  slop, or say it does not make sense? Each reason they would give is a flag with its remedy,
  whether or not a narrower rule below names it: layers that each add one tweak, wrappers that only
  forward or fix a value, one-symbol fragments, a file for a slice of a concern another module
  owns, one thing implemented twice, comments narrating code, confusing or near-duplicate names,
  dead or speculative code, hand-written configuration or styling where an owner exists, a setting
  left in the form its library warns against, a shortcut a comment or report admits, a result its
  reader would question. The list illustrates the question and never bounds it.
- A rubric exemption that would excuse such a shape is named in the flag. A remedy that sends the
  author to an existing piece judges that piece the same way first: a wrapper or a duplicate is not
  an owner.
- An increment fixing an earlier flag is judged on the earlier flags it answers and on its own
  lines, read the same way, never only against that flag; the rest of the modules it touches and of
  the originating diff, which the earlier gate judged, is context, open to a new flag only where the
  increment changes what it depends on or it holds a confirmed defect or exploitable vulnerability.

Before the design comparison, verify that the supplied rule sources are complete and cover the
file groups in the diff. Check preambles, imports, declarations and executable bodies in the
scope above. For Python, check the opening statement and each data-holding declaration's bases
and decorators against the language rules before judging its placement. Flag each violation by
line and rule even when a narrower check passes. Formatting, type and CI checks prove only the
rules they enforce. Flag missing evidence and say what to supply.

**Then make the design comparison.** Inventory the responsibilities and decisions the diff moves,
duplicates, specializes, removes or introduces, reading both sides independently of the caller's
rationale. Follow each prior selected or computed answer to every resulting use, counting independent
selections, copies and repeated work even inside one file; a canonical file is not proof of canonical
decision ownership. Apply the rubric's **Independent Judgment** comparison to those owners and
consumers, including for prose and configuration. Complete the comparisons despite earlier flags,
and name the exact missing input and investigation for any remaining choice. Return the comparisons
and deciding evidence in the existing verdict fields; a checklist or stage inventory alone is
incomplete.

**Make the simpler candidate concrete.** For each thing the diff adds, check its reuse receipt
against the supplied search results and candidate sources, and read the tree with the gate's own
tools for an analogous implementation those results miss; the results say where to start, never
where to stop. Flag a duplicate of an existing owner, new code where an owner needed one more
condition or parameter, and a parameter, option or branch for a condition nothing uses, each at
the severity `code-simplify`'s rubric gives it. Where the change wrote that check's three fields,
verify each against the sources. Name the searches and candidates read in `Also read`. For other
suspect shapes, apply the rubric's removal test. Missing validation evidence
is a separate flag, never a reason to leave the design judgment unfinished.

**Trace changed state-like values during the design comparison**, as the rubric's **The Design
Comparison** sets out; missing evidence prevents a clean verdict.

**Then run the five greps** the `code-simplify` rubric's **Five Greps** defines, as the rubric's
**The Design Comparison** sets out; a verdict with none says `no hit for any of the five greps` in
those words.

**Then list every guard, refusal, validation, or branch the diff adds**, as the rubric's **The
Design Comparison** sets out; a verdict with none says `no guard added` in those words.

**Then list every product choice the diff makes**, as the rubric's **The Design Comparison** sets
out; a verdict with none says `no product choice added` in those words.

**Then list every workaround the diff makes**, as the rubric's **The Design Comparison** sets out; a
verdict with none says `no workaround added` in those words.

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

An invocation that names several frozen diffs, each with its exact head and intent, may get one
fresh gate that inspects them together and returns a distinct verdict for each head. Its prompt
names every head and intent, and its evidence retains the per-head disposition. Retain an earlier
per-head acceptance only while that head, its inputs, and its affected-repository map remain exact;
rerun the changed head and its dependent gates without invalidating unrelated heads. A shared
question never lets an author judge their own work or collapse distinct verdicts.

## Questions

Exactly one per gate, each decided by the tests in `references/rubric.md`, with nothing appended.
Whether an item is the change's doing or predates it is never asked to soften a defect; it bears
only on scope, as **The Intent Statement** says. The question sets the gate's capability level, at `subagent-matrix`'s default effort: Proposal,
Diff and Final acceptance run at advanced, and Triage, Admission and Base incorporation, whose
packets are small and whose answers accept no diff for merge, run at standard. A caller names the
question and never a level of its own:

- **Triage — what should happen to this?** An issue, a finding or a proposed record, or a list of
  them in one call; the answer is one of fix, close, defer
  or do for each.
- **Admission — may this work be deferred?** The triage question asked of a proposed record.
- **Proposal — should this be written?**
- **Diff — should this stand?** A finished plan step or worker task that later steps build on, a
  correction after base incorporation, or the repairs of and answers to a verdict's flags, read with the
  whole branch diff as its originating diff.
- **Base incorporation — what did the base bring in that the change must refactor?** The procedure
  below.
- **Final acceptance — may this merge?** The complete pull-request diff, read once after review is
  clean and before any check gate. A calling workflow that states the size past which it reads a
  diff in slices puts that diff slice by slice instead, one gate per slice, and then puts the
  seams between slices to one more gate. At most five slices, grouped by package the
  way `code-simplify` slices a scope. The diff is accepted when every slice and the seams
  are; each line is still read once, and a repair round reruns only the slices a repair touched and
  their seams.

### Base incorporation

Run after an incorporation of the base this session performed in which Git reported a conflict,
or whose incoming diff touches a file, a shared contract or agent guidance the change also touches
or depends on. A clean incorporation disjoint from the change takes no gate of its own: the caller
records both file lists and the comparison that showed them disjoint, and final acceptance reads
the resulting head. The base advancing remotely without being incorporated does not trigger the check, and
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

A verdict binds its caller as the rubric's **What A Verdict Binds** says.

A flag blocks the flagged proposal or diff, not an ordinary repair the task already authorizes.
Before admitting a flag, check it against the task's recorded decisions and the commit that
introduced the behavior it names. A flag that reopens a behavior choice the user's recorded words
or an earlier acceptance settled, or that asks for work outside the scope the user set, is
answered as settled or out of scope with that evidence; it is never repaired and never put to the
user as a question. Only the user's words settle a product choice: one an earlier acceptance or an
agent-written record holds without them is still open, and goes to the user. A confirmed defect or a
security vulnerability is never settled this way, whatever an
earlier acceptance said: it is repaired as below.
Read every other objection and remedy against the intent and standing guidance and make the
smallest coherent repair using the existing owner or mechanism.

**No flag is closed by the run that raised it or the agent that answered it.** The agent that made
a repair re-reads the changed lines against the flag's objection and remedy and runs the checks
covering that code. Then the repairs of every flag one verdict raised, and each settled,
out-of-scope or council-dropped answer with its evidence, go together to one fresh gate under the
Diff question, following `subagent-matrix`'s **Dispatch**; it answers each flag separately, and
only its acceptance closes a flag. Its brief carries each flag in the verdict's own words, the
repair and the output of the checks the repair reran, so it reads them without an evidence round.
A change gets at most 3 review rounds in total: the first
review and 2 re-reviews after repairs; that gate is one of them, and one of the repair rounds below
for each flag it reads a repair of. The exceptions are a style flag and a flag naming only missing
evidence, each closed as its paragraph below says, and the decision `council` makes once 3 review
rounds have failed the change, which settles its flags as it rules, and a proposal whose calling
workflow states how its repairs are judged.

**Each flag carries its severity, `defect` or `style`.** A style flag concerns only the form of
lines whose behavior, structure and contract stand: a docstring's or comment's length, a missing
blank line, a name's length, wording that misstates nothing. Everything else is a defect, however
small its fix. The author fixes a style flag and runs the checks covering it, and final acceptance,
which every change gets before it merges, confirms it; a style flag final acceptance raised is
confirmed by a fresh re-check of those lines alone. A style flag costs no round, under the
3-round limit or the repair rounds below, and never goes to `council`.

**A gap in the evidence a gate was given is not a failed round.** A gate whose verdict waits only
on evidence it names, such as a source excerpt or a run's output, receives that evidence in the same
run and finishes its verdict, and that verdict is the round's. Only evidence travels this way: a
change to the diff, or to any text the gate judges, goes to a fresh gate, and no gate judges wording
it proposed itself.

**Repair rounds are counted per objection and per change, in every review loop.**

- **Per change:** a change is one plan step, worker task or finding fix, and it gets at most 3
  rounds across every kind of check, such as a review, a gate, a smoke test or CI: the first and 2
  after repairs. A round fails a change only when it raised a finding or flag on that change's
  lines. A round a broken runner, fixture or provider cut short before judging the change is not
  counted, and neither are a style flag and an evidence gap, as the paragraphs above say.
- **At the limit:** once 3 rounds have failed a change, whatever each raised, `council` in **Ask**
  mode decides between a simpler approach, reverting the change and accepting it with the remaining
  findings recorded, within the limit `council`'s **Ask** sets on what a ruling accepts. That
  decision replaces another repair, and an acceptance with recorded findings it makes is the one
  exception to the rules below on flagged diffs.
- **Per flag:** while the change is under that limit, a flag gets at most two repair rounds of its
  own, and one a fresh gate raises for the first time starts at zero. A flag the gate still raises
  after its own second repair, with the change still under the limit, goes to `council` in **Ask**
  mode with the open flag, each remedy tried and its evidence, and the gate's proposed remedy. Its
  ruling decides the remedy, which is applied and checked as any repair is, and the caller's result
  names the flag and the ruling. The verdict's other flags go on to their fresh gate meanwhile.
- A flag the council returns as the user's choice goes to the user, as a report of those facts with
  a recommended next step, never as a choice about whether to fix it or leave it in place.

A verdict changes only when the item does: rerunning an unchanged item, arguing it through the same
gate or renaming it to reset its history changes nothing, and flagged code stays flagged whoever can
authorize the merge. Carry unresolved
objections and previous remedies into the next review; a remedy that reverses one given earlier
names it and the evidence it was wrong. If evidence refutes an objection, put the
objection, that evidence and the code it concerns to `council` in **Ask** mode for a ruling: a
unanimous `drop` is the evidence a fresh gate closes the flag on, and anything else keeps it open
for repair. The caller cannot dismiss it unilaterally.

When the intent statement already schedules a flag's remedy as named work with its owner, such as
a consumer's migration on its own pull request, the gate reports it as a hold on the merge that
work must precede, not a flag on the change, and it counts no repair round. The hold stays until that
work is accepted.

When no compliant repair is available, name the conflict and the smallest native repair examined.
Apply the rubric's triage and admission tests before reverting, recording, or re-scoping any work;
flag count alone satisfies none of them. A non-defect may be deferred only on those tests' evidence,
including when its simplest compliant repair still requires substantial irreducible complexity or
mechanisms its gain cannot carry. A confirmed defect remains owed under the fix test. A hypothetical
safeguard or compatibility concern is judged against the target repository's product state and
contract, not promoted to a defect merely because a reviewer flagged it. Deprecated usage and a
warning a run prints are never hypothetical: they are defects under `pre-production`, and the gate
flags each one it meets in the diff or in the verification output the caller supplies.

Escalate only a genuine unresolved product, scope, security, disclosure or authorization choice, stating the concrete
fork and why authorized remedies cannot settle it. Repair authority and merge authority are separate:
a source pull request awaiting merge permission continues through authorized repairs and reviews.
Keep unrelated authorized work moving while a real decision waits. No diff merges with a flag
still open, apart from the acceptance with recorded findings `council` makes at the 3-round limit.

## Reporting

Report every verdict with what it named, whether or not the item went on to land. A deferral's
admission verdict is written on its record, and a close's reason and reconsideration criterion on
the canceled record.

## Output

The gate returns this shape and nothing else; the caller repeats it in its own report:

```markdown
Gate: <question> — <item in one line>

Verdict: accept | flag | fix | close | defer | do

- <for a flag: `[defect]` or `[style]`, the quoted line or missing evidence, the shape it takes, the
  intent, rule or rubric item it violates, and the remedy the change itself would take; one bullet
  per flag>
- <for an acceptance: each addition whose kind matches a removed shape, the shape it takes, and why
  it is neither the removed shape nor a finding; one bullet per addition>
- <for a triage disposition: the test that decided it and the fact it rests on>

Greps: <the grep each hit flagged above came from, or `no hit for any of the five greps`>

Writers read: <each guard the diff adds with the writers it read, or `no guard added`; owned-boundary input evidence>

Product choices: <each product choice the diff makes with the user's words settling it, or `no product choice added`>

Workarounds: <each workaround the diff makes with the user's words asking for it, or `no workaround added`>

Also read: <the Independent Judgment comparison receipt, file groups and rules checked, plus additions of other kinds>
```
