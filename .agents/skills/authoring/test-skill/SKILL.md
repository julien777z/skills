---
name: test-skill
description: "Prove every behavior-changing skill, rule, or agent edit changes what a reader does: rebuild the miss, run one reader on edited guidance and one on the original per scenario, and score both before the pull request merges."
short_description: 'Compare edited and original skill guidance against the same scenario.'
---

# Test Skill

A skill edit is a claim that different words produce different behaviour. Test the claim the way
a code change is tested: against the case that motivated it, with the change and without it.

## Dependencies

- `subagent-selection` — return model tiers for explicit reviewer dispatch.
- `code-simplify` — the pass every skill pull request gets before it merges; this skill runs after it.
- `session-ledger` — resolve retained private evidence storage and preserve verification inputs and results.

## When It Runs

- **Run before merge for every behavior-changing skill, rule, or agent edit**, whether it came
  through `edit-skill` or was made directly. A rule is reader guidance, so its source type never
  exempts it. An edit that changes what the skill returns the user runs only after the user
  approved a fictional example of that output, as `edit-skill` requires; a smoke run never
  proposes a format.
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
   private task evidence directory resolved with `session-ledger`, outside every repository, and
   never commit it. Use that directory for this run's frozen packages, dispatch inputs, reader
   reports and score tables too. The scenario must not name the
   expected answer anywhere a reviewer reads.
   Keep it small: slice the diff to the files the miss lives in, and give every reviewer a reading
   list — those files, their siblings, and the modules the rubric's own searches would reach — so a
   run reads what the scenario needs instead of exploring the tree. Most of a run's time is
   exploration the scenario could have pointed at. Beside the triggering case, build a second
   scenario on a different member of the same class, so the result shows the edit's breadth and
   not only its one instance.
   **Then build a third on the likeliest loophole**: a route by which a reader follows the edited
   text and still commits the miss. Look for it in three places. One is an escape the wording leaves
   open — asking instead of acting, offering the work as a choice, deferring it, calling it out of
   scope, reporting it rather than doing it, deciding the case falls outside the rule, or doing the
   step in name only. Another is guidance the same session also loads that points the other way — a
   global rule, an output-style skill, a caller or callee of the edited skill, an example that still
   shows the old behaviour; search those files for the miss's own words and for their opposite, and
   put the file that opens the route in both runs' reading lists. The third is the edit itself: one
   that gives the reader something new to do or look at opens a route of its own, so test what the
   reader does when that thing turns up something wrong — a capture the edit says to open showing a
   defect, a check it adds failing, a step it adds that cannot complete.
3. **Beside the scenario, save both texts** of every file the change edits that a run reads — the edited
   skill, and any adjacent file a loophole brought into the change under step 8: the branch copy
   and the original from the freshly fetched default branch. Edited runs read the branch copies,
   controls the originals; nothing else about their prompt differs.
4. **Write the pass criteria before launching anything.** Two to four statements, each answerable
   yes or no from a report alone, naming what the report must contain — a count, a named sibling, a
   proposed structure, a check performed — never how well the report reads. A criterion the
   original text would also satisfy measures nothing; drop it. Phrase each as the words the report
   must carry — a symbol's name, a number — so scoring is a search through the report, not a
   reading of it.
5. **Launch the reviewers** using **Reviewer selection** below, in parallel when
   capacity allows: one run reading the edited text and one reading the original, per
   scenario. Identical prompts save for those paths. Read-only, findings only, no edits;
   the parent applies nothing from a smoke run, because the run judges wording, not the code.
   Queue pairs when capacity is limited; never spawn a duplicate while a run is in flight.
6. **Score every report** against every criterion, quoting the line that satisfies or fails it, and
   tabulate as `## Output` shapes it.
7. **Judge each scenario's table.** The edit passes when, in every scenario, every edited run reads
   `pass` and at least one control reads `miss`. An edited run that misses, and a table where every
   control passes, both go to step 8.
8. **Diagnose, change, rerun, until every table passes.**
   - **An edited run that misses has a cause**; find it in the report and record it before changing
     anything. The wording left the reader room: revise toward what it missed, keeping the language
     broad; a report that named the shape and then reasoned it away — "intentional", "not
     problematic" — is this kind, and the revision states the disposition as fixed and names those
     reasons as not reasons. The scenario cannot satisfy the criterion, such as a file missing from
     the reading list, or its prompt never made the reader open the skill file: fix the scenario.
     The run took a loophole another loaded file opens: fix it in that file, which joins the change.
     The report shows the behaviour in words the criterion did not search for: rephrase the
     criterion to that behaviour. A wording change in any file under test reruns every edited run
     that reads that file, together; a scenario change reruns every run, controls included; a changed
     criterion rescores every report.
   - **No control misses** means the scenario has not rebuilt the miss. Sharpen it until the
     original text misses — for an edit that broadens a rule, build it on a member of the class the
     original never named — and rerun every run.
   - **A reader no change moves** means the miss in step 1 was misstated or the edit does nothing:
     restate the miss and start again from step 1, or drop or reshape the edit.
9. **Report** the tables in chat, and send one markdown file from the task's evidence directory
   for the whole smoke test, both as `## Output` shapes them. Put one sentence in the pull request
   description naming the miss the edit closes. The tables are evidence and do not belong in the
   description.

## Reviewer selection

Invoke `subagent-selection` and select the **standard** tier. Run one edited/control pair per
scenario — two runs — with the same resolved model, reasoning effort, scenario and reading list in
both. Follow the dependency's explicit dispatch instructions, including its equivalent-model
fallback when the requested tier is unavailable. Report `not run` only when no available model
can perform the comparison.

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

Diagnoses: <one line per step 8 change: scenario, round, run label, cause, change made> | None

Evidence: <name of the sent file>

Verdict: passes (round <n>) | dropped — <reason> | not run: <reason>
```

- **One titled table per scenario**, the bold `Scenario <n>: <short name>` line above it and its
  legend line under it, repeated for each scenario the smoke test ran; Diagnoses and Verdict follow
  the last one.
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

- **<criterion>, <pass | miss>:** <quoted line>
- **Round <n>, for the record:** <what the run missed before its rerun>
```

The heading reads `## Evidence: <skill name>` when the file covers several skills; the round in a
run heading and the round bullet appear only on a run that was rerun.

## Guardrails

- Reviewers never see the expected answer, the criteria, or one another's reports.
- Follow the shared tier selection. Never omit a control.
- Never edit any file under test between launching a pair of runs and scoring them.
- Keep the scenario while the branch is open; every later edit of that skill reuses it.
- Never merge with a failing run or stand with a miss: diagnose it, change what caused it, and
  rerun. The decisions are the tester's and are never put to the user; asking holds every later
  session on the text the edit replaces.
