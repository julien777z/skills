# Regression Scenarios

Contents: **What A Scenario Holds**, **Where They Live**, **Format** (with one full example),
**When They Run**, **Changing A Scenario**, **Isolation**, **Checks**.

This reference is the skill test's rulebook for pinned regression scenarios. `SKILL.md` sends a
reader to **When They Run** every round, and to the rest when a scenario runs, is written or
changes.

## What A Scenario Holds

`SKILL.md`'s **When It Runs** sets the change check beside the regression scenario. A regression
scenario is committed beside its skill, must always pass, and covers the skill's happy, edge and
negative paths:

- an example execution;
- which subagents launch, and how many;
- what the run should find.

The agent adds a regression scenario when a skill gains a behavior worth holding in place, and
changes one as **Changing A Scenario** allows.

## Where They Live

- **A regression scenario is one folder in a skill's own top-level `tests/` folder**,
  `<skill>/tests/<scenario-name>/`, and its id is that path, such as
  `subagent-matrix/tests/required-provider-stays`.
  - A `tests/` folder anywhere else is not one, such as a script's own `scripts/tests/`.
  - A scenario is placed in the skill its first `covers` entry points at.
- **The folder holds `scenario.yaml` and `fixture/`, and nothing else.**
  - `fixture/` is the working directory the agent starts in, as real files: repository files,
    images, a checklist, the tools' `README.md`.
  - A simulated tool, such as a launcher that accepts or refuses and charges clock time, is
    described as data in `fixture/tools/behavior.yaml`. The run's harness builds each tool it
    lists as `tools/<name>` and leaves `behavior.yaml` out of the agent's working directory.
  - The harness, every transcript and every grade stay private and untracked, because the
    repository keeps no test code.
- **`scenario.yaml` parses with safe YAML loading and holds only the keys Format lists**, in that
  order. Its `kind` is `happy`, `edge` or `negative`, and each `covers` entry names a guidance
  file under `.agents/`, outside every `tests/` folder, and a section that file holds; the first
  entry's file is in the scenario's own skill. Every date is quoted, so safe loading reads
  it as a string. A value holding a colon followed by a space, or a ` #`, goes in a block scalar or
  quotes.
- **The source check enforces these rules.** `skill-pass`'s **Source Check** refuses a
  `scenario.yaml` that breaks them or **Format**'s, the first `history` entry included, which is
  the one that adds the scenario, on the behavior-change route with no `file` or `section`.

## Format

- `title`: one line naming the behavior held.
- `kind`: `happy`, `edge` or `negative`.
- `covers`: the guidance the scenario holds in place, each entry a `file` under `.agents/` and a
  `section`. It decides when the scenario runs, as **When They Run** says.
- `prompt`: the exact message the agent receives.
- `expect`: the checks, each an `id` and a `check`. A check is one or two sentences measurable
  against what the run leaves behind: the tool log, the files written, the final reply. A term it
  needs is defined inside the check that uses it, or in another scenario's check the check names as
  its measure, as **Checks** says, and how many subagents launch is a check like any other.
- `history`: one entry per change, each a quoted `date`, a `route` of `behavior-change` or
  `test-cause`, and a `reason`. A behavior-change entry also carries the `pull_request`, and, unless
  it adds the scenario, the guidance `file` under `.agents/` and the `section` whose hunk in that
  pull request changes what the edited check or fixture measures, in that order between `route`
  and `reason`.

This is one full scenario folder, invented for the example:

```text
deploy-gate/tests/stalled-reviewer-is-replaced/
├── scenario.yaml
└── fixture/
    ├── deploy-notes.md
    ├── service.diff
    └── tools/
        ├── README.md
        └── behavior.yaml
```

`scenario.yaml`:

```yaml
title: A reviewer that never starts is replaced before the deploy step reads its verdict
kind: edge

covers:
  - file: skills/deploy-gate/SKILL.md
    section: Review Before Deploy

prompt: |
  You are working through `deploy-notes.md` in the current directory. Do its open step as the guidance
  you work under requires. `tools/README.md` describes the tools you have. When the step is done, give
  a final reply stating its result.

expect:
  - id: one-replacement
    check: actions.log has exactly two `tools/reviewer start` calls whose trace.log output reads
      `started`, the second after a `tools/reviewer status` call printing `no activity`.
  - id: verdict-from-replacement
    check: The final reply reports the second reviewer's verdict and says the first never started.

history:
  - date: "2026-03-02"
    route: behavior-change
    pull_request: "57"
    reason: added with the review step it holds in place
```

`fixture/deploy-notes.md`:

```markdown
# Deploy notes — billing-api 1.8

1. [done] Build the image.
2. Review `service.diff` with one independent reviewer, then report its verdict.
```

`fixture/service.diff`:
```diff
--- a/app.py
+++ b/app.py
@@ -3,1 +3,1 @@
-TIMEOUT = 5
+TIMEOUT = 50
```

`fixture/tools/README.md`:

```markdown
# Tools

- `tools/reviewer start --brief-file PATH` — starts a reviewer. Prints `started <name>`.
- `tools/reviewer status NAME` — prints the reviewer's state.

Every call is recorded.
```

`fixture/tools/behavior.yaml`:

```yaml
recording:
  actions_log: actions.log    # "<seq>\t<tool> <subcommand>\t<arguments>", before each call
  trace_log: trace.log        # "<seq>\t<output>", after it
tools:
  reviewer:
    kind: launcher
    start: {requires: [--brief-file], prints: "started {name}"}
    # the first reviewer started never shows activity; every later one completes
    status: {first: "{name}: no activity", later: "{name}: complete; verdict: TIMEOUT tenfold, should"}
```

## When They Run

- **A round runs every regression scenario its diff touches.** A scenario is selected when any of
  these holds:
  - a `covers` entry names a changed file;
  - it belongs to a skill that reads a changed skill: one that declares the changed skill or cites
    it, as `skill-pass`'s **Source Check** lists readers;
  - a changed file is guidance every session loads, `.agents/global.md` or a rule with `alwaysApply:
    true`, or a skill `global.md` **Skills that always run** starts, which selects every scenario.
- **Each selected scenario gets one reader and runs with no control**, since it asks only whether
  the skill still does what its scenario says, and joins the round's grader batches.
- **Each scenario passes or fails as a whole**, and passes only when every check passes.
- **A miss blocks like a failing edited run.** It is diagnosed at its owner, repaired and rerun
  within **Repair and rerun until verified** in `SKILL.md`. A miss caused by the guidance is
  repaired in the guidance. A miss caused by the scenario is repaired as **Changing A Scenario**
  says.

## Changing A Scenario

- **Adding a scenario needs nothing more** than its `history` entry, on the behavior-change route
  of the pull request that adds it.
- **Every change to a scenario takes one of two routes, and no other**: any key but `history`,
  `kind` and `expect` as much as `covers` and `prompt`, and any file under `fixture/`, its
  `behavior.yaml` included. Each change adds a `history` entry on its route, so a later reader can
  tell an intended change of behavior from a drifted test.
  - **Behavior change.** The change is made in the pull request whose guidance diff changes that
    behavior. Its entry names that pull request in `pull_request`, and in `file` and `section` the
    guidance whose hunk there changes what the edited check or fixture measures, and gives the
    reason. Deleting a scenario folder takes this route, in the pull request that removes the
    behavior it holds.
  - **Test cause.** A fresh writer's rewrite, whose entry claims no change of behavior, carries
    no `pull_request`, `file` or `section`, and names in its `reason` which opener below opened
    the route.
- **The test-cause route opens on three things, and never on a run's miss**:
  - a grader's "ambiguous" return, as **Checks** says; a "pass (note)" verdict, a pass carrying a
    reservation about the check, counts as one;
  - a review's or gate's flag on the check's or fixture's text;
  - the user's direction about the scenario format.
- **Every change to a check or fixture, on either route, goes to an independent Diff gate before any
  rerun**, through `acceptance-gate`. For a behavior-change entry the gate confirms that the named
  `file` and `section` have a hunk in that pull request changing what the edited check measures; an
  entry it cannot confirm is undone; a test-cause rewrite of that check follows only when one of the
  three openers above holds, by a fresh writer as below.
- **A test-cause writer**, launched as `subagent-matrix` says, one for every check awaiting a
  rewrite at that point, gets the check, the guidance it tests and what opened the route — the
  grader's two readings, the flag, or the user's direction — and no transcript text, so the new text
  measures the guidance rather than one run's answer.
- **Every scenario a change governs then reruns fresh**, every scenario whose check names a
  rewritten check as its measure included, and its earlier results are kept for the record.
- **A check is never loosened so that a run passes.** A miss the guidance caused is repaired in the
  guidance. A rewrite answers what opened its route in what the check says, never the verdict a run
  got.

## Isolation

- **A reader gets a real install of the branch under test, never a reading list.** Run the
  repository's installer from a fresh copy of that branch into a fresh scratch home, the way a
  session gets its skills, and point the reader's harness at that home as its only user-level root.
  The reader then finds and loads skills itself, from the skill listing and descriptions. The
  installer leaves each skill's top-level `tests/` folder out, so no scenario reaches the install.
- **The reader's working directory is a copy of `fixture/`** with each tool built from
  `behavior.yaml` and that file left out. The prompt is the only message it receives, launched as
  `SKILL.md`'s **Workflow** launches a reader. It never receives `scenario.yaml`.
- **Every reader transcript is audited for a read of any `tests/` path**, whether by a file tool, a
  search or a shell command. A hit voids the run, and the run is rerun once the route that exposed
  the path is closed.
- **Only the grader sees `scenario.yaml`**, as the run's frozen checks, with the fixture and the
  run's records.
- **The writer of a scenario or a check is never the author of the guidance change under test**,
  so the expectation is not shaped by the change's own reasoning.

## Checks

- **A check reads recorded artifacts**: the tool log, the tool outputs, the resulting files against
  the fixture's copies, a sent message, the transcript's launches, the final reply. It never asks for
  the grader's impression of what the reader meant.
- **Every term and exclusion a check applies is settled inside that check**, or in the check it
  names as its measure, such as text that also occurs in the fixture, or fixed template labels, so
  two graders apply it the same way.
- **A check may name another scenario's check as its measure**, by the scenario's id and the check's
  `id`, and state only how its own text differs, so one measure is never kept as two copies that
  drift. The grader of the naming scenario receives the named `scenario.yaml` too, and a rewrite of
  the named check reruns every scenario that names it.
- **A grader that finds a check admitting two readings returns "ambiguous" with both readings and
  the verdict each gives**, and never chooses one. The check then takes the test-cause route in
  **Changing A Scenario**.
