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

- `subagent-matrix` — return model capabilities for explicit reviewer dispatch.
- `code-simplify` — the pass every skill pull request gets before it merges; this skill runs after it.
- `session-ledger` — resolve retained private evidence storage and preserve verification inputs and results.

## When It Runs

- **Run before merge for every behavior-changing skill, rule, or agent edit**, whether it came
  through `edit-skill` or was made directly. A rule is reader guidance, so its source type never
  exempts it. An edit that changes what the skill returns the user runs against the concrete example
  `edit-skill` records before the edit; a smoke run validates that format without proposing or
  awaiting approval for it.
- **An edit that changes no instruction a reader follows does not run.** A spelling correction or
  dead link repair asks the reader to do the same work. Its source validation and required reviews
  still apply; there is no changed behavior for a smoke test to exercise.
- Recognise one from the diff rather than from how it is described, and least of all from how small
  it looks: read each changed line against the line it replaces and confirm the instruction is
  identical. A line that gains, loses, sharpens or reorders one is an ordinary edit however few
  words moved, and the whole edit is smoke-tested.
- **A canonical guidance batch is tested in one coordinated round.** Freeze the exact head and
  guidance package for every related guidance pull request, use one edited reader across the
  batch's isolated scenarios, and retain results per head. Run an isolated original control when an
  improvement claim or conflicting instruction needs comparison; a straightforward clarification
  may omit it only with that justification recorded. The original control stays blind to the edited
  diff, criteria, and reports. After its smoke work, the edited reader may independently review the
  complete frozen batch diff, but never supplies its final acceptance. Add readers only for a
  distinct named risk, and rerun only scenarios invalidated by the changed head or guidance.
- A new skill has no original to run against. Its control runs carry no skill text at all, which
  shows what the skill adds over the model alone.
- `skill-gauntlet` asks whether a skill is worth keeping; this skill asks whether one edit does
  what it was made for. Neither replaces the other.

## Workflow

1. **Define the behavior.** Record the observed miss and the outcome the user requires. Default to
   two or three cases covering the triggering case, a different member of that failure class, and
   its likeliest loophole; add a case only for a distinct named risk. Include relevant conflicting
   guidance in the edited reading list and, when a control is required, in its matching reading
   list. Keep expected answers and scoring criteria
   outside everything the testing agents read.
2. **Choose and verify the environment.** Use the smallest environment that exercises the actual
   decision or operation. A review can inspect a relevant live codebase read-only, a frozen diff,
   or an isolated repository with known defects. An action workflow needs a task-owned synthetic
   environment: disposable files, fake credentials, local services or browser surfaces, and action
   recorders as appropriate. Preserve the relevant interfaces, permissions, failures and state
   transitions; a canned success or written promise does not exercise the workflow.
   Never give smoke agents access to the user's browser, profiles, sessions, real credentials, or
   live mutation targets. When a workflow would revoke a credential, send a message, purchase,
   delete or change access, supply a synthetic boundary that records that action and changes only
   disposable state. Verify which implementation and resources each run actually uses before launch.
   Before freezing the reader package, exercise its required fixture interfaces in a disposable
   copy: discovery must expose the identifiers the task needs, operations must be available, and
   state changes and failures must reach the intended records. This checks the fixture contract,
   not the reader's decisions or the comparison's expected result. Reuse that receipt while its
   implementation and interface inputs remain unchanged; repair and recheck a changed contract
   before spending reader runs on it.
3. **Freeze the inputs and criteria.** Save the scenario, environment baseline, reading list,
   edited guidance, any required original guidance, and two to four observable pass criteria in private task evidence
   storage through `session-ledger` before dispatch. Criteria measure actions, resulting state or
   substantiated findings, not recitation of new wording. Use the branch copy and, when required,
   the original from the freshly fetched default branch. Record their revisions or content digests. Give every
   required control an equivalent independent environment so neither run inherits the other's
   mutations or reports.
4. **Run the task.** Launch one edited-guidance agent to run the frozen scenarios in isolated
   resources and, when required above, one original-guidance control with identical instructions
   and independent resources. Agents perform the bounded task, including mutations inside their
   synthetic environments when the task calls for them. Read-only review tasks remain read-only.
   Queue readers when capacity is limited; never duplicate an active assignment. The coordinator
   retains responsibility for setup, repair, evidence and completion rather than asking the user to
   arrange the test.
5. **Retain and inspect results immediately.** Apply `subagent-matrix`'s **Dispatch** result-handoff
   checks to each report and dispatch receipt, retain its action record, and inspect the authoritative
   resulting state before accepting an outcome. Score every criterion with an artifact location or
   an exact finding and its supporting source, then construct the tables in **Output**.
6. **Reach a supported conclusion.** Every edited run must meet every criterion, using a valid
   environment and retained evidence. If the edited run passes and the original misses, report
   demonstrated improvement for that case. If both pass, report that both meet the behavior and no
   improvement was demonstrated there; this is a valid conclusion, not a failing test. Never force
   an original-guidance miss, change criteria to reward wording recall, or claim causation from
   matching behavior. A failing edited run requires repair regardless of the original's result.
   When both pass, decide whether the guidance still earns its place: an explicit policy, a
   documented failure outside these samples, a clarified boundary or a useful consistency guarantee
   can justify retaining it without demonstrated improvement in this run. Remove or reshape wording
   that adds no useful instruction. Judge the complete change, not the control result alone, and
   record the evidence for retaining or removing each independently meaningful edit. When independent
   edits deserve different outcomes, separate them through the repository's pull-request workflow
   where authorized; keep coupled instructions and their required repairs together. This assessment
   recommends which changes should merge; the caller still completes acceptance and the authorized
   merge gate. A passing smoke test alone never decides that a pull request should merge.
7. **Repair and rerun until verified.** Diagnose each reported issue at its owner. Fix guidance
   that permits the wrong behavior; fix an invalid fixture, unavailable simulated operation, wrong
   reading list, ambiguous criterion or broken runner before judging guidance. Retain the diagnosis
   and earlier results. Recover missing evidence from the actual run or rerun the affected task;
   never reconstruct a result from a summary. A failed worker is replaced on the same assignment.
   A guidance change reruns every affected edited run; an environment or scenario change reruns
   the edited run and any required control affected by the change; a scoring correction rescores all applicable retained results.
   Inconclusive, improperly tested and missing-evidence states are work to repair, never final
   smoke verdicts or reasons to abandon an authorized change. Keep working through recovery;
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
required reader cannot launch, perform its scenario in process under `subagent-matrix` and disclose
that the result is not independent or blind.

Classify a rejected reader dispatch from the host receipt. Only a receipt establishing that the
requested capability or model is unsupported makes it unavailable for that attempt and permits the
lower-tier fallback. Retry a transient, concurrency, timeout, or unknown rejection once with the
same resolved selection; do not lower the comparison tier. When no required reader launched, retry
the required reader set. When one required reader launched, wait for its terminal report and retry
only the rejected or unattempted required counterpart, never a duplicate of the accepted reader.
When that retry cannot complete the required set, record its receipts and perform the missing
assignment in process. Record every failed attempt separately from reader-run evidence,
including every required reader's receipt; do not score an incomplete required set as a reader
result. When an unsupported request has a permitted fallback, wait for any accepted counterpart's
terminal report, record the incomplete attempt, then launch a fresh required set. When no permitted model fallback remains, record the rejection and perform the missing assignment
in process.

Run one edited reader across the frozen scenarios and one original control only when the recorded
comparison requires it, with the same resolved model and reasoning effort where both run. Record
the catalogue state, requested capability and family, exact dispatch identifier, resolved reasoning
effort, selector resolution, and accepted actual-assignment dispatch receipt with those explicit
parameters in each run's evidence entry. Record catalogue state separately
from assignment state: a catalogue-hidden family is `dispatch required` until its exact identifier is resolved
and the assigned worker accepts it, then it is `accepted`; a missing identifier triggers the in-process
fallback and is not an unsupported-model receipt. Selector resolution retains an explicit unsupported request,
the exact fallback capability and dispatch identifier when one is permitted, why that fallback was selected,
and any explicit user override. Record the runtime-identity and runtime-label evidence as
`subagent-matrix`'s Workflow step 3 defines. Follow the selector's dispatch instructions.

## Output

Return this shape, one block per skill under test, and in chat nothing after the last verdict line:

```markdown
Smoke test: <skill name>

Miss: <one sentence>

**Scenario <n>: <short name>**

| Run | Result | <criterion 1> | <criterion 2> | <criterion 3> |
|---|---|---|---|---|
| <Model> A | pass | pass | pass | pass |
| <Model> B, when required | miss | miss | pass | miss |

A reads the edited text. B reads the original only when the recorded comparison requires a control.

Comparison: improvement demonstrated | both meet the behavior; no improvement demonstrated | conformance only; control omitted: <recorded clarification justification>

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
- **One row per run**, labelled with the model and a letter: A reads the edited text; B reads the
  original only when required, or no skill text for a new skill. Each row shows its latest run.
- **`Result` follows `Run`** and reads `pass` only when every criterion in that row passed; each
  further column is one criterion, headed with a short name for the behaviour it checks, never
  `Run`, `Result`, a run label, or a phrase built on them. Every cell carries `pass` or `miss`.
- **At most five columns**, so at most three criteria per table. More criteria continue in a
  further table under the same scenario title, with the same rows and legend line.

The sent file holds the block of every skill the smoke test covered, then a `---` line and the
evidence behind every cell, one section per skill:

```markdown
## Evidence

### Scenario <n>: <short name>

<one line on what the scenario contains and what else it carries>

#### <run label> (<edited | original> text[, round <n>])

- **Catalogue state:** <capability> / <family> — <catalogue-confirmed | catalogue-hidden>
- **Requested selection:** <capability> / <family>
- **Dispatch identifier:** <exact identifier | identifier required>
- **Assignment state:** <not requested | dispatch required | identifier required | accepted | unavailable: reason>
- **Reasoning effort:** <requested and resolved effort>
- **Selector resolution:** <accepted identifier | explicit unsupported receipt | same-selection retry | fallback or override>
- **Actual-assignment dispatch, accepted:** <source>
- **Runtime identity, <model | not exposed>:** <host evidence>
- **Runtime label:** <verbatim generic label | not exposed>
- **Environment:** <baseline identity, isolated resources, and verified execution boundary>
- **Retained results:** <raw report, dispatch receipt, action record and resulting-state locators>
- **<criterion>, <pass | miss>:** <artifact location or exact finding with supporting source>
- **Edit disposition:** <each independent edit, retain/reshape/remove/separate decision, and value evidence>
- **Round <n>, for the record:** <what the run missed before its rerun>

#### Dispatch attempt <n> (incomplete required reader set)

- **Catalogue state:** <capability> / <family> — <catalogue-confirmed | catalogue-hidden>
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
reader-run heading and the round bullet appear only on a run that was rerun. An incomplete required
reader set omits criterion scoring because it produced no valid result.
Retain the whole-PR recommendation with its per-edit rationale and supporting artifact locators
in the same evidence file; per-scenario conclusions do not replace that decision.

## Guardrails

- Reviewers never see the expected answer, the criteria, or one another's reports.
- Follow the shared capability selection. Omit a control only under the recorded clarification
  justification above.
- Never edit any file under test between launching its required readers and scoring them.
- Keep the scenario and raw evidence while the branch is open; reuse valid inputs in later rounds.
- Never merge with a failing run or stand with a miss: diagnose it, change what caused it, and
  rerun. The decisions are the tester's and are never put to the user; asking holds every later
  session on the text the edit replaces.
