---
name: smoke-test
description: "Prove a skill edit changes what a reader does: rebuild the miss that prompted it, run reviewers on the edited and the original text, and score both against stated criteria before the pull request merges. Runs on every edit to a skill that changes what a reader does — a step added, removed or reordered, a decision moved, a criterion changed, a new obligation — whether the edit came through edit-skill, arrived while doing other work, or was made directly, and whether or not anyone invoked it. An edit that merges without it is unverified."
---

# Smoke Test Skill

A skill edit is a claim that different words produce different behaviour. Test the claim the way
a code change is tested: against the case that motivated it, with the change and without it.

## Dependencies

- `code-simplify` — the pass every skill pull request gets before it merges; this skill runs after it.

## When It Runs

- After every skill edit and before its pull request merges, whether the edit came through
  `edit-skill` or was made directly. An edit that skipped this is unverified, and the report
  says so.
- A new skill has no original to run against. Its control runs carry no skill text at all, which
  shows what the skill adds over the model alone.
- `skill-gauntlet` asks whether a skill is worth keeping; this skill asks whether one edit does
  what it was made for. Neither replaces the other.

## Workflow

1. **Name the miss.** State in one sentence what a reader did wrong before the edit, from the
   evidence that prompted it: a review that reported a symptom and not the shape behind it, a
   walkthrough that skipped a check, a plan that stopped a step early. A pure rewording has no
   miss; say so and still run the scenario, because the rewording may have lost what worked.
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
5. **Launch the reviewers** in parallel and in the background: for at least two models weaker than
   the one running the session — a mid-sized and a small model — one run reading the edited text
   and one reading the original. Identical prompts save for the skill path. Read-only, findings
   only, no edits; the parent applies nothing from a smoke run, because the run judges wording, not
   the code. Never spawn a duplicate while a run is in flight.
6. **Score every report** against every criterion, quoting the line that satisfies or fails it, and
   tabulate: one row per run, one column per criterion.
7. **Judge the table.** The edit passes when every run reading the edited text meets every criterion
   and at least one control run misses at least one. Both halves matter. A control that also passes
   means one of two things and the tester says which: the words changed nothing a reader does, or
   the scenario is too easy to separate them. Sharpen the scenario inside the same bound, and when
   that bound is spent apply the same decision a spent bound gets below. An edited run that misses
   names the sentence to revise: revise toward what it missed, keep the language broad, and rerun
   that model once. Controls run in the first round only, since the original text does not change;
   a revision reruns only the models that missed, all of them together, never one after another.
   A run that named the shape and then reasoned it away —
   "correctly delegates", "intentional", "not problematic" — is a wording miss of one kind: the check
   left its disposition to judgement, so the revision states the disposition as fixed and names the
   reasons a reader gives for keeping the shape as not reasons. Before a third round, re-read the
   scenario and the criteria as well as the wording: a criterion the scenario cannot satisfy — a
   file the reviewer was never given — is fixed in the scenario, and the controls need no rerun for
   that.
8. **Run the bounded loop.** The loop ends when every edited run meets every criterion, and the pull
   request merges then and not before; a failing row is never merged while a round remains. **The
   rounds are bounded, and the bound is a judgement made before the first revision**: state how
   many rounds the miss is worth — three is usual, fewer for a one-line edit, more where each round
   is cheap and the criterion is central —
   and when the last one still fails, stop revising and decide: let the edit stand with the miss
   when the failing report follows the edit in substance and misses only the words the criterion
   looked for, make a different change to the skill when the rounds tried one shape of wording and
   another is still untried, or drop the edit when the controls show the words changed nothing —
   unless the edit is strictly broader than the text it replaces, a class named where only an
   instance was, in which case let it stand. The three are the whole set, so the pull request is
   never left open on this, and the decision is the tester's and is never put to the user; asking
   holds every later session on the text the edit replaces. Report the table, the sentence last
   revised, and the decision with its reason; whether the pull request then merges is the
   delivery's call, not this skill's. A loop
   that will not close within the bound usually means the miss in step 1 was misstated; say so when
   it is.
9. **Report** the table with its quoted evidence in chat, as `## Output` shapes it, and put one
   sentence in the pull request description naming the miss the edit closes. The table is evidence
   and does not belong in the description.

## Output

Return this shape, one table per skill under test, and nothing after the last verdict line:

```markdown
Smoke test: <skill name>

Miss: <one sentence>

| Run | Text | <criterion 1> | <criterion 2> | ... |
|---|---|---|---|---|
| <model> | edited | pass: "<quoted line>" | miss | ... |
| <model> | original | miss | pass: "<quoted line>" | ... |

Verdict: passes | revised and rerun (round <n>) | bound spent: <stands with the miss | edited again | dropped> — <reason> | not run: <reason>
```

Every cell carries `pass` with the line that satisfies the criterion or `miss`. A control row for a
new skill reads `none` in its Text column.

## Guardrails

- Reviewers never see the expected answer, the criteria, or one another's reports.
- Never conclude from one model. Wording only the largest model follows has not been tested.
- Never edit the skill under test between launching a pair of runs and scoring them.
- Keep the scenario while the branch is open; every later edit of that skill reuses it.
- Never let a failing row stand before the bounded rounds are spent; after them, decide and state
  the decision. The decision is never put to the user, before the bound or after it.
