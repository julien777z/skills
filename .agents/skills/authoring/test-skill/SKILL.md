---
name: test-skill
description: "Validate behavior-changing skill, rule, and agent edits before merge through realistic tasks with edited guidance and risk-based original controls. Choose isolated environments for actions, retain observed results, and repair guidance or defective tests until the required behavior is verified."
short_description: 'Exercise guidance safely, compare behavior, and repair failing tests.'
---

# Test Skill

Test guidance by having agents do the work it governs, then inspecting the result. Compare edited
and original guidance against the same task when the recorded risk requires a control. Correct
behavior establishes conformance; a difference between the runs establishes improvement. Do not
confuse those conclusions.

## Dependencies
- `subagent-matrix`
- `code-simplify`
- `session-ledger`

## When It Runs

- **Run before merge for every behavior-changing skill, rule, or agent edit**, however it was
  made. A rule is reader guidance, so its source type never
  exempts it. An edit that changes what the skill returns the user runs against the concrete example
  recorded before the edit; a skill-test run validates that format without proposing or
  awaiting approval for it.
- **An edit that changes no instruction a reader follows does not run.** A spelling correction or
  dead link repair asks the reader to do the same work. Its source validation and required reviews
  still apply; there is no changed behavior for a skill test to exercise.
- Recognize one from the diff rather than from how it is described, and least of all from how small
  it looks: read each changed line against the line it replaces and confirm the instruction is
  identical. A line that gains, loses, sharpens or reorders one is an ordinary edit however few
  words moved. Write scenarios for the semantic instruction or behavior delta and any dependencies
  it concretely affects, not for unchanged behavior merely because it shares a skill, file, batch,
  or head; a result already retained follows the carry-forward bullet below. Verify moved unchanged
  text against its source, links, and reachability, and write a scenario for moved text only where
  meaning or reachability changed.
- **An invocation that names several heads is tested in one coordinated round.** Freeze the exact
  head and guidance package for every named pull request, and retain results per head. The round
  runs when, and on the head the caller supplies.
- **Each scenario gets its own reader for each variant it runs**, so its context holds that one
  task: one edited reader per scenario step 1 writes, plus its original control where the next
  bullet requires one. Add readers only for a distinct named risk.
- **An original control runs where an improvement claim or conflicting instruction needs
  comparison**: in a scenario's first round, and in a later round only where the edited run missed
  and the retained control cannot carry forward; a straightforward clarification may omit it only
  with that justification recorded. The original control stays blind to the edited diff, criteria,
  and reports.
- **A retained result carries to a new head only when every file its scenario depends on and its
  execution environment are unchanged there**: each guidance file on its reading list, or, for a
  file every reader loads whole, such as the global rules, the sections its criteria cite, its fixture
  and its criteria, checked against the frozen record by content digest, and the model and
  reasoning-effort identifiers, the harness and the guidance it loaded, and the tools and fixture
  interface the scenario uses: the run's recorded values, each compared with the one a rerun would
  resolve now, never with what the host still offers. Any difference reruns
  that scenario, never a judgment that the change does not touch what it tests; a scenario
  unchanged in both is not rerun.
- A new skill has no original to run against. Its control runs carry no skill text at all, which
  shows what the skill adds over the model alone.

## Workflow

Run after `code-simplify` completes its pass.

1. **Have someone other than the edit's author define the behavior.** Record the observed miss, the
   outcome the user requires and the real case the miss came from. One fresh scenario writer,
   launched through `subagent-matrix` for the round's whole batch of corrections, receives those,
   each failure class and the diff, and writes in one pass the smallest set of scenarios sufficient
   to cover the changed behavior and its affected dependencies: one per failure class, corrections
   that fail the same way sharing it, and a reworded or moved instruction covered by its class's
   scenario rather than one of its own, each mapped to the changed boundary with its observable
   pass criteria. A failure that came from real work is tested on a fixture built from
   that real case; a reproduction scenario the caller supplies is the writer's input, never a
   scenario itself. Include relevant conflicting guidance in the edited reading list and, when a
   control is required, in its matching reading list.
2. **Choose and verify the environment.** Use the smallest environment that exercises the actual
   decision or operation. A review can inspect a relevant live codebase read-only, a frozen diff,
   or an isolated repository with known defects. An action workflow needs a task-owned synthetic
   environment: disposable files, fake credentials, local services or browser surfaces, and action
   recorders as appropriate. Preserve the relevant interfaces, permissions, failures and state
   transitions; a canned success or written promise does not exercise the workflow.
   Never give skill-test agents access to the user's browser, profiles, sessions, real credentials, or
   live mutation targets. When a workflow would revoke a credential, send a message, purchase,
   delete or change access, supply a synthetic boundary that records that action and changes only
   disposable state. Verify which implementation and resources each run actually uses before launch.
   **A reader sees only the variant it tests, and the variant reaches it only as that run's input.**
   Launch the reader as a local headless harness process the running session starts and waits on,
   every user-level skill and rule root it is given set to an empty scratch root, and pass the
   frozen variant through an option that adds a source for that one run, such as a plugin
   directory, an appended system prompt or an input file the run reads. An option that sets where
   the harness reads user-level skills or rules is a user-level root whatever folder it names, so
   the variant never goes in one, in a folder one points at, or in any folder searched by default.
   A subagent of the running session stands in only when its loaded guidance lists no copy of a
   skill or rule under test, with the variant in its brief. Record the route, the command, the
   scratch root's file list with digests, and the harness's record of the guidance it loaded. With
   neither route, the round is a concrete gate under the global rules' **Tools and environments**;
   it never passes with a reader that saw another variant.
   Before freezing the reader package, exercise its required fixture interfaces in a disposable
   copy: discovery must expose the identifiers the task needs, operations must be available, and
   state changes and failures must reach the intended records. This checks the fixture contract,
   not the reader's decisions or the comparison's expected result. Reuse that receipt while its
   implementation and interface inputs remain unchanged; repair and recheck a changed contract
   before spending reader runs on it.
3. **Freeze the inputs and criteria.** Save the scenario, environment baseline, reading list,
   edited guidance, any required original guidance, and the observable pass criteria needed to judge
   each scenario in private task evidence storage through `session-ledger` before dispatch. Criteria measure actions, resulting state or
   substantiated findings, not recitation of new wording, and name each step the workflow under
   test requires: a run that compressed, merged or skipped one misses it however right its end
   result looks. **The frozen scenario and criteria text is the writer's output as it stands**,
   with at most a line naming the file, scenario or digest: the coordinator never shortens,
   restates, completes, reorders, drops or adds a scenario line or criterion, however unworkable
   one looks. Criteria are never amended once a result is seen; a criterion found ambiguous or
   unworkable, by anyone and whenever, is rewritten by one fresh scenario writer launched for every
   criterion awaiting a rewrite at that point, given step 1's inputs and those criteria, never a
   reader's report or a grade. A grader's ambiguity verdict starts that rewrite even when an earlier
   one ran, and a replacement still unworkable goes back the same way with what is wrong, within
   step 7's round limit; until a valid one arrives the criterion stays frozen as written. Every
   scenario a replacement governs reruns fresh, its earlier results kept for the record and never
   rescored. Use the branch copy and, when required,
   the original from the freshly fetched default branch. Record their revisions or content digests. Give every
   required control an equivalent independent environment so neither run inherits the other's
   mutations or reports.
4. **Run the task.** Launch each scenario's edited-guidance reader in isolated resources and, when
   required above, its original-guidance control with identical instructions and independent
   resources. Agents perform the bounded task, including mutations inside their
   synthetic environments when the task calls for them. Read-only review tasks remain read-only.
   Queue readers when capacity is limited; never duplicate an active assignment. The coordinator
   retains responsibility for setup, repair, evidence and completion rather than asking the user to
   arrange the test.
5. **Retain results unaltered and have an independent grader judge them.** Apply
   `subagent-matrix`'s **Dispatch** result-handoff checks to each report and dispatch receipt, and
   retain the report, its action record and the authoritative resulting state as they are. One
   fresh grader per batch of up to eight scenarios, launched through `subagent-matrix` and never the
   edit's author, a writer or a reader, judges every criterion of its batch from copies of the runs
   labeled at random, the frozen criteria and those records, citing an artifact location or an exact
   finding and its supporting source. Nobody rewrites, summarizes or corrects a reader's
   observation before grading or to match an expected answer. Every cell in **Output** is a verdict
   the grader stated for that criterion and run, copied as it is. A criterion the grader calls
   ambiguous, or leaves without a verdict, gets no cell from anyone else: it goes to step 3's rewrite
   once that grade is in, and the table reports it only from the rerun's grade. Every run that
   returned a report goes to the grader, including one the coordinator believes was set up wrongly;
   that diagnosis is recorded beside its grade, and the repaired rerun is graded as well.
6. **Reach a supported conclusion.** Every edited run must meet every criterion, using a valid
   environment and retained evidence. If the edited run passes and the original misses, report
   demonstrated improvement for that case. If both pass, report that both meet the behavior and no
   improvement was demonstrated there; this is a valid conclusion, not a failing test. Never force
   an original-guidance miss or claim causation from matching behavior. A failing edited run
   requires repair regardless of the original's result.
   When both pass, decide whether the guidance still earns its place: an explicit policy, a
   documented failure outside these samples, a clarified boundary or a useful consistency guarantee
   can justify retaining it without demonstrated improvement in this run. Remove or reshape wording
   that adds no useful instruction. Judge the complete change, not the control result alone, and
   record the evidence for retaining or removing each independently meaningful edit. When independent
   edits deserve different outcomes, separate them through the repository's pull-request workflow
   where authorized; keep coupled instructions and their required repairs together. This assessment
   recommends which changes should merge and decides no merge itself. A passing skill test alone
   never decides that a pull request should merge.
7. **Repair and rerun until verified**, within the global rules' review-round limit of 3 rounds per
   change: after the third failing round over the same edit, that bullet's decision replaces another
   repair. Diagnose each reported issue at its owner. Fix guidance that permits the wrong behavior;
   fix an invalid fixture, unavailable simulated operation, wrong reading list, ambiguous criterion
   or broken runner before judging guidance. Retain the diagnosis and earlier results. Recover
   missing evidence from the actual run or rerun the affected task; never reconstruct a result from
   a summary. A worker that ended without a complete result is replaced on the same assignment.
   Every completed run is graded and kept: a rerun follows a recorded repair of its cause, never an
   unchanged scenario rerun for a better result, and covers what the carry-forward bullet in **When
   It Runs** does not carry.
   Inconclusive, improperly tested and missing-evidence states are work to repair, never final
   skill-test verdicts or reasons to abandon an authorized change. Keep working through recovery;
   genuine external authorization or host boundaries follow the global rules and **Reviewer
   selection**, holding only the dependent action while repair or resolution remains active.
8. **Report the verified result.** Send the tables and one evidence file in the **Output** shape.
   Describe the behavior verified in the pull request; claim improved behavior only where the
   comparison demonstrates it. Scenario packages and raw evidence remain private, never committed.

## Reviewer selection

Invoke `subagent-matrix` and request **standard** by default. Only after a host receipt explicitly
rejects the standard tier's exact identifier as unsupported, select the next permitted lower mapped capability,
resolve its exact identifier, and launch the actual reader assignment. Advance again only after that candidate
receives its own explicit unsupported receipt; never move upward or inherit the orchestrator's model. This
fallback applies to this skill's default, never against the user's explicit model or capability constraint. A
`dispatch required` result with an exact identifier launches the actual required reader set. When a
required reader, scenario writer or grader cannot launch, apply `subagent-matrix`'s launch
fallback for its assignment.

Classify a rejected reader dispatch from the host receipt. Only a receipt establishing that the
requested capability or model is unsupported makes it unavailable for that attempt and permits the
lower-tier fallback. Retry a transient, concurrency, timeout, or unknown rejection once with the
same resolved selection; do not lower the comparison tier. When no required reader launched, retry
the required reader set. When one required reader launched, wait for its terminal report and retry
only the rejected or unattempted required counterpart, never a duplicate of the accepted reader.
When that retry cannot complete the required set, record its receipts and apply `subagent-matrix`'s
launch fallback for the missing assignment. Record every failed attempt separately from reader-run evidence,
including every required reader's receipt; grade and retain each run that completed, and withhold
the comparison and the passing verdict until the required set completes. When an unsupported request has a permitted fallback, wait for any accepted counterpart's
terminal report, record the incomplete attempt, then launch a fresh required set. When no permitted model fallback remains, record the rejection and apply `subagent-matrix`'s launch
fallback for the missing assignment.

Run each scenario's edited reader, and its original control only where **When It Runs** requires
one, with the same resolved model and reasoning effort where both run. Record
the catalog state, requested capability and family, exact dispatch identifier, resolved reasoning
effort, selector resolution, and accepted actual-assignment dispatch receipt with those explicit
parameters in each run's evidence entry. Record catalog state separately
from assignment state: a catalog-hidden family is `dispatch required` until its exact identifier is resolved
and the assigned worker accepts it, then it is `accepted`; a missing identifier triggers the launch
fallback and is not an unsupported-model receipt. Selector resolution retains an explicit unsupported request,
the exact fallback capability and dispatch identifier when one is permitted, why that fallback was selected,
and any explicit user override. Record the runtime-identity and runtime-label evidence as
`subagent-matrix`'s Workflow step 3 defines. Follow the selector's dispatch instructions.

## Output

A scenario written, run or graded in process is recorded with the same actions and evidence and
labeled in process.

Return this shape, one block per skill under test, and in chat nothing after the last verdict line:

```markdown
Skill test: <skill name>

Miss: <one sentence>

**Scenario <n>: <short name>**

| Run | Result | <criterion 1> | <criterion 2> | <criterion 3> |
|---|---|---|---|---|
| <Model> A | pass | pass | pass | pass |
| <Model> B, when required | miss | miss | pass | miss |

A reads the edited text. B reads the original only when the recorded comparison requires a control.

Comparison: improvement demonstrated | both meet the behavior; no improvement demonstrated | conformance only; control not run: <reason under When It Runs>

Disposition: retain | reshape | remove | separate independent changes — <value judgment and evidence>

Recommendation: merge | reshape before merge | remove | separate independent changes — <whole-PR value judgment and evidence>

Diagnoses: <one line per step 7 change: scenario, round, run label, cause, change made> | None

Evidence: <name of the sent file>

Verdict: passes (round <n>) | not run: <nonbehavioral change under When It Runs>
```

- **One titled table per scenario**, with its legend, supported Comparison and evidence-backed
  Disposition underneath. One whole-PR Recommendation reconciles those dispositions after the last
  scenario, before Diagnoses and Verdict; a merge recommendation remains subject to the caller's
  gates. Both rows may pass. Use the actual results rather than copying the illustrative control
  miss above.
- **One row per run**, labeled with the model and a letter: A reads the edited text; B reads the
  original only when required, or no skill text for a new skill. Each row shows its latest run.
- **`Result` follows `Run`** and reads `pass` only when every criterion in that row passed; each
  further column is one criterion, headed with a short name for the behavior it checks, never
  `Run`, `Result`, a run label, or a phrase built on them. Every cell carries the grader's `pass`
  or `miss`, as step 5 says.
- **At most five columns**, so at most three criteria per table. More criteria continue in a
  further table under the same scenario title, with the same rows and legend line.

The sent file holds the block of every skill the skill test covered, then a `---` line and the
evidence behind every cell, one section per skill:

```markdown
## Evidence

### Scenario <n>: <short name>

<one line on what the scenario contains, what else it carries, and the scenario writer's dispatch receipt>

#### <run label> (<edited | original> text[, round <n>])

- **Catalog state:** <capability> / <family> — <catalog-confirmed | catalog-hidden>
- **Requested selection:** <capability> / <family>
- **Dispatch identifier:** <exact identifier | identifier required>
- **Assignment state:** <not requested | dispatch required | identifier required | accepted | unavailable: reason>
- **Reasoning effort:** <requested and resolved effort>
- **Selector resolution:** <accepted identifier | explicit unsupported receipt | same-selection retry | fallback or override>
- **Actual-assignment dispatch, accepted:** <source>
- **Runtime identity, <model | not exposed>:** <host evidence>
- **Runtime label:** <verbatim generic label | not exposed>
- **Environment:** <baseline identity, isolated resources, and verified execution boundary>
- **Retained results:** <raw report, dispatch receipt, action record, resulting-state and grader-receipt locators>
- **<criterion>, <pass | miss>:** <artifact location or exact finding with supporting source>
- **Edit disposition:** <each independent edit, retain/reshape/remove/separate decision, and value evidence>
- **Round <n>, for the record:** <what the run missed before its rerun>

#### Dispatch attempt <n> (incomplete required reader set)

- **Catalog state:** <capability> / <family> — <catalog-confirmed | catalog-hidden>
- **Requested selection:** <capability> / <family>
- **Dispatch identifier:** <exact identifier | identifier required>
- **Assignment state:** <not requested | dispatch required | identifier required | accepted | unavailable: reason>
- **Reasoning effort:** <requested and resolved effort>
- **Selector resolution:** <rejection classification; retained exact identifier or exact selected fallback identifier>
- **Edited reader dispatch, <accepted | rejected | not attempted>:** <receipt or reason>
- **Required control dispatch, <accepted | rejected | not applicable>:** <receipt or reason>
- **Outcome:** <same-selection set retried | missing reader retried | fresh fallback set launched | terminal hold>
```

The heading reads `## Evidence: <skill name>` when the file covers several skills; the round in a
reader-run heading and the round bullet appear only on a run that was rerun. A run that completed
in an incomplete required set is graded under its own run heading; the attempt section records
only the dispatch.
Retain the whole-PR recommendation with its per-edit rationale and supporting artifact locators
in the same evidence file; per-scenario conclusions do not replace that decision.

## Guardrails

- Readers never see the expected answer, the criteria, or one another's reports.
- Follow the shared capability selection. Run or omit a control only as **When It Runs** says.
- Never edit any file under test between launching its required readers and grading them.
- Keep the scenario and raw evidence while the branch is open; reuse valid inputs in later rounds.
- Never merge with a failing run or stand with a miss: diagnose it, change what caused it, and
  rerun. The decisions are the tester's and are never put to the user; asking holds every later
  session on the text the edit replaces.
