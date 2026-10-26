---
name: test-skill
description: "Validate behavior-changing skill, rule, and agent edits before merge through realistic tasks with edited and original guidance. Choose isolated environments for actions, retain observed results, and repair guidance or defective tests until the required behavior is verified."
short_description: 'Exercise guidance safely, compare behavior, and repair failing tests.'
---

# Test Skill

Test guidance by having agents do the work it governs, then inspecting the result. Compare edited
and original guidance against the same task. Correct behavior establishes conformance; a difference
between the runs establishes improvement. Do not confuse those conclusions.

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
- **A batch of edits on one pull request is tested in one round.** The round carries every edit's
  scenarios, and each run reads the whole batch's edited or original package. Its reading list
  records every file in that package.
- A new skill has no original to run against. Its control runs carry no skill text at all, which
  shows what the skill adds over the model alone.
- `skill-gauntlet` asks whether a skill is worth keeping; this skill asks whether one edit does
  what it was made for. Neither replaces the other.

## Workflow

1. **Define the behavior.** Record the observed miss and the outcome the user requires. Build the
   triggering case, a different member of that failure class, and its likeliest loophole. Include
   relevant conflicting guidance in both reading lists. Keep expected answers and scoring criteria
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
3. **Freeze the inputs and criteria.** Save the scenario, environment baseline, reading list,
   edited and original guidance, and two to four observable pass criteria in private task evidence
   storage through `session-ledger` before dispatch. Criteria measure actions, resulting state or
   substantiated findings, not recitation of new wording. Use the branch copy and the original from
   the freshly fetched default branch. Record their revisions or content digests. Give paired runs
   equivalent independent environments so neither inherits the other's mutations or reports.
4. **Run the task.** Launch one edited and one original-guidance agent per scenario through
   **Reviewer selection**, with identical instructions except guidance and isolated resource paths.
   Agents perform the bounded task, including mutations inside their synthetic environments when
   the task calls for them. Read-only review tasks remain read-only. Queue pairs when capacity is
   limited; never duplicate an active assignment. The coordinator retains responsibility for setup,
   repair, evidence and completion rather than asking the user to arrange the test.
5. **Retain and inspect results immediately.** Save each raw agent report, dispatch receipt and
   action record as it arrives, read it back, and inspect the authoritative resulting state before
   accepting an outcome. A summary, a worker's claim that it passed, or a locator to an absent file
   is not evidence. Score every criterion with an artifact location or an exact finding and its
   supporting source, then construct the tables in **Output**.
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
   both members of its affected pair; a scoring correction rescores all applicable retained results.
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
`dispatch required` result with an exact identifier launches the actual reader pair. Only `identifier required`
and every rejection not explicitly unsupported retain the concrete hold.

Classify a rejected reader dispatch from the host receipt. Only a receipt establishing that the
requested capability or model is unsupported makes it unavailable for that attempt and permits the
lower-tier fallback. Retry a transient, concurrency, timeout, or unknown rejection once with the
same resolved selection; do not lower the comparison tier. When neither reader launched, retry the
full pair. When one reader launched, wait for its terminal report and retry only the rejected or
unattempted counterpart, never a duplicate of the accepted reader. When that retry cannot complete
the pair, record the terminal hold with both receipts and the unchanged requested selection. Record
every failed attempt separately from reader-run evidence, including both pair-member receipts; do
not score an incomplete pair as a reader result. When an unsupported request has a permitted
fallback, wait for any accepted counterpart's terminal report, record the incomplete attempt, then
launch a fresh full pair. When no permitted fallback remains, record the terminal hold
with the unsupported request and rejection evidence.

Run one edited/control pair per scenario — two runs — with the same resolved model, reasoning
effort, scenario and reading list in both. Record the catalogue state, requested capability and family,
exact dispatch identifier, resolved reasoning effort, selector resolution, and accepted actual-assignment
dispatch receipt with those explicit parameters in each run's evidence entry. Record catalogue state separately
from assignment state: a catalogue-hidden family is `dispatch required` until its exact identifier is resolved
and the assigned worker accepts it, then it is `accepted`; a missing identifier is a hold, not an unavailable
model. Selector resolution retains an explicit unsupported request,
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
| <Model> B | miss | miss | pass | miss |

A reads the edited text, B the original.

Comparison: improvement demonstrated | both meet the behavior; no improvement demonstrated

Disposition: retain | reshape | remove | separate independent changes — <value judgment and evidence>

Diagnoses: <one line per step 7 change: scenario, round, run label, cause, change made> | None

Evidence: <name of the sent file>

Verdict: passes (round <n>) | not run: <nonbehavioral change under When It Runs>
```

- **One titled table per scenario**, with its legend, supported Comparison and evidence-backed
  Disposition underneath; Diagnoses and Verdict follow the last one. Both rows may pass. Use the
  actual results rather than copying the illustrative control miss above.
- **One row per run**, labelled with the model and a letter: A reads the edited text, B the
  original, or no skill text for a new skill, which its legend line says. Each row shows its latest
  run.
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

#### Dispatch attempt <n> (incomplete pair)

- **Catalogue state:** <capability> / <family> — <catalogue-confirmed | catalogue-hidden>
- **Requested selection:** <capability> / <family>
- **Dispatch identifier:** <exact identifier | identifier required>
- **Assignment state:** <not requested | dispatch required | identifier required | accepted | unavailable: reason>
- **Reasoning effort:** <requested and resolved effort>
- **Selector resolution:** <rejection classification; retained exact identifier or exact selected fallback identifier>
- **Reader A dispatch, <accepted | rejected | not attempted>:** <receipt or reason>
- **Reader B dispatch, <accepted | rejected | not attempted>:** <receipt or reason>
- **Outcome:** <same-selection pair retried | missing member retried | fresh fallback pair launched | terminal hold>
```

The heading reads `## Evidence: <skill name>` when the file covers several skills; the round in a
reader-run heading and the round bullet appear only on a run that was rerun. An incomplete-pair
dispatch attempt omits criterion scoring because it produced no comparable reader pair.

## Guardrails

- Reviewers never see the expected answer, the criteria, or one another's reports.
- Follow the shared capability selection. Never omit a control.
- Never edit any file under test between launching a pair of runs and scoring them.
- Keep the scenario and raw evidence while the branch is open; reuse valid inputs in later rounds.
- Never merge with a failing run or stand with a miss: diagnose it, change what caused it, and
  rerun. The decisions are the tester's and are never put to the user; asking holds every later
  session on the text the edit replaces.
