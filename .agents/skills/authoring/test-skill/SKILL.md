---
name: test-skill
description: "Prove a skill edit changes what a reader does: rebuild the miss that prompted it, run reviewers on the edited and the original text, and score both against stated criteria before the pull request merges. Runs on every edit to a skill that changes what a reader does — a step added, removed or reordered, a decision moved, a criterion changed, a new obligation — whether the edit came through edit-skill, arrived while doing other work, or was made directly, and whether or not anyone invoked it. An edit that merges without it is unverified."
short_description: 'Compare edited and original skill guidance against the same scenario.'
---

# Test Skill

A skill edit is a claim that different words produce different behaviour. Test the claim the way
a code change is tested: against the case that motivated it, with the change and without it.

## Dependencies

- `subagent-selection` — return model tiers for explicit reviewer dispatch.
- `code-simplify` — the pass every skill pull request gets before it merges; this skill runs after it.

## When It Runs

- After every skill edit and before its pull request merges, whether the edit came through
  `edit-skill` or was made directly. An edit that skipped this is unverified, and the report
  says so.
- **An edit that changes no instruction a reader follows does not run at all, and its pull request
  merges on the reading**. A term swapped for
  another, a spelling standardised, a typo corrected, a dead link repaired: the text asks a reader
  for exactly what it asked before. There is no behavioural claim to test, and the bar below needs
  a control run to miss, which no such edit can produce. Running it regardless holds the change
  behind a result it can never get, which is how a rename every later session is waiting on sits
  unmerged.
- Recognise one from the diff rather than from how it is described, and least of all from how small
  it looks: read each changed line against the line it replaces and confirm the instruction is
  identical. A line that gains, loses, sharpens or reorders one is an ordinary edit however few
  words moved, and the whole edit is smoke-tested.
- A new skill has no original to run against. Its control runs carry no skill text at all, which
  shows what the skill adds over the model alone.
- `skill-gauntlet` asks whether a skill is worth keeping; this skill asks whether one edit does
  what it was made for. Neither replaces the other.

## Workflow

1. **Name the miss.** State in one sentence what a reader did wrong before the edit, from the
   evidence that prompted it: a review that reported a symptom and not the shape behind it, a
   walkthrough that skipped a check, a plan that stopped a step early. An edit the waiver in **When
   It Runs** covers never reaches this step.
2. **Rebuild the scenario** as something a reviewer can read with none of this conversation: for a
   review skill, a diff plus a checkout at the commit where the miss happened; for a walkthrough
   skill, the page and the change; for a planning skill, the task as it was given. Put it in a
   scratch directory outside every repository and never commit it. The scenario must not name the
   expected answer anywhere a reviewer reads.
   Keep it small: slice the diff to the files the miss lives in, and give every reviewer a reading
   list — those files, their siblings, and the modules the rubric's own searches would reach — so a
   run reads what the scenario needs instead of exploring the tree. Most of a run's time is
   exploration the scenario could have pointed at.
3. **Save both texts beside it:** the edited skill file and the original from the freshly fetched
   default branch. Reviewers read one or the other by path; nothing else about their prompt differs.
4. **Write the pass criteria before launching anything.** Two to four statements, each answerable
   yes or no from a report alone, naming what the report must contain — a count, a named sibling, a
   proposed structure, a check performed — never how well the report reads. A criterion the
   original text would also satisfy measures nothing; drop it. Phrase each as the words the report
   must carry — a symbol's name, a number — so scoring is a search through the report, not a
   reading of it.
5. **Launch the reviewers** using **Reviewer selection** below, in parallel when
   capacity allows. Each selected model gets one run reading the edited text and one reading
   the original. Identical prompts save for the skill path. Read-only, findings only, no edits;
   the parent applies nothing from a smoke run, because the run judges wording, not the code.
   Queue pairs when capacity is limited; never spawn a duplicate while a run is in flight.
6. **Score every report** against every criterion, quoting the line that satisfies or fails it, and
   tabulate as `## Output` shapes it: one row per run, a `Result` column reading `pass` only when
   every criterion passed, and one column per criterion.
7. **Judge the table.** The edit passes when every edited run reads `pass` and at least one control
   reads `miss`. An edited run that misses, and a table where every control passes, both go to
   step 8.
8. **Diagnose, change, rerun, until the table passes.**
   - **An edited run that misses has a cause**; find it in the report and record it before changing
     anything. The wording left the reader room: revise toward what it missed, keeping the language
     broad; a report that named the shape and then reasoned it away — "intentional", "not
     problematic" — is this kind, and the revision states the disposition as fixed. The scenario
     cannot satisfy the criterion, such as a file missing from the reading list, or its prompt never
     made the reader open the skill file: fix the scenario. The report shows the behaviour in words
     the criterion did not search for: rephrase the criterion to that behaviour. A wording change
     reruns every edited run that missed, together; a scenario change reruns every run, controls
     included; a changed criterion rescores every report.
   - **No control misses** means the scenario has not rebuilt the miss. Sharpen it until the
     original text misses — for an edit that broadens a rule, build it on a member of the class the
     original never named — and rerun every run.
   - **A reader no change moves** means the miss in step 1 was misstated or the edit does nothing:
     restate the miss and start again from step 1, or drop or reshape the edit.
9. **Report** the table itself in chat, as `## Output` shapes it; only the quoted evidence behind
   each cell goes to one file in the session's scratch directory, sent with the report. Put one
   sentence in the pull request description naming the miss the edit closes. The table is evidence and does not belong
   in the description.

## Reviewer selection

Invoke `subagent-selection` and select **standard and advanced**. Run one edited/control pair
per available tier: four runs when both tiers are available. Use the same scenario and reading
list across tiers, with the same resolved model and reasoning effort within each pair. Follow the
dependency's explicit dispatch instructions and queue pairs when capacity is limited.

If a tier is unavailable, report its pair as `not run`; available pairs may still provide partial
evidence, but do not claim complete two-tier coverage. If both tiers are unavailable, report the
smoke pass as `not run`. Never treat two runs on one model as a two-tier comparison.

## Output

Return this shape, one table per skill under test, and nothing after the last verdict line:

```markdown
Smoke test: <skill name>

Miss: <one sentence>

| Run | Text | Result | <criterion 1> | <criterion 2> | ... |
|---|---|---|---|---|---|
| <model> | edited | pass | pass | pass | ... |
| <model> | original | miss | miss | pass | ... |

Diagnoses: <one line per step 8 change: round, run, cause, change made> | None

Evidence: <name of the sent evidence file>

Verdict: passes (round <n>) | dropped — <reason> | not run: <reason>
```

Every cell carries `pass` or `miss`; each row shows its latest run. A control row for a new skill
reads `none` in its Text column.

## Guardrails

- Reviewers never see the expected answer, the criteria, or one another's reports.
- Follow the shared tier selection. Never omit a control or claim complete coverage when a tier was not run.
- Never edit the skill under test between launching a pair of runs and scoring them.
- Keep the scenario while the branch is open; every later edit of that skill reuses it.
- Never merge with a failing row or stand with a miss: diagnose it, change what caused it, and
  rerun. The decisions are the tester's and are never put to the user; asking holds every later
  session on the text the edit replaces.
