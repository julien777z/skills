# Delivery Routes

What the short route runs and how a batch moves between routes; read from **Guidance Delivery** in `SKILL.md` once a batch qualifies for the short route.

## Short route

The editing agent runs the source check, `skill-pass`'s pass
and the `code-simplify` pass itself, in process; one independent `acceptance-gate` reads the
batch's delta, briefed as **Brief `review-pass`'s final acceptance** says with the Scope
Statements as intent; and `test-skill` runs its single-scenario form for each entry, entries that
fail the same way sharing a scenario, with no control run, since the observed miss already
shows the original text failing. No `review-pass` runs. It starts the gate and the skill test's
writer, grader and one reader per scenario: four agents for one correction. The pull request
then merges as **Check the diff file list against the default branch, then merge** says. A
repair goes back to a fresh gate over its delta and reruns its scenario. A batch that stops
qualifying, when an entry joins it or a repair grows it, moves to the full route and keeps
every verdict on what did not change.
