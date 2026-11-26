# Regression Scenarios

Contents: **The Two Kinds**, **Where They Live**, **Format** (with one full example), **When They
Run**, **Changing A Scenario**, **Isolation**, **Checks**.

This reference is the skill test's rulebook for pinned regression scenarios. `SKILL.md` sends a
reader here when a round selects them, and when one is written or changed.

## The Two Kinds

- **A change check** asks whether a new guidance change holds up. Its scenarios are written fresh for
  the change's failure classes, as **Workflow** in `SKILL.md` sets out, and stay in private task
  evidence.
- **A regression scenario** asks whether a skill still does what it did. It is committed beside the
  skill, it must always pass, and it covers the skill's happy, edge and negative paths:
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
- **`scenario.yaml` parses with safe YAML loading and holds only the keys **Format** lists**, in
  that order. Its `kind` is `happy`, `edge` or `negative`, and each `covers` entry names a file that
  exists under `.agents/` and a section that file holds. Every date is quoted, so safe loading reads
  it as a string. A value holding a colon followed by a space, or a ` #`, goes in a block scalar or
  quotes.

## Format

- `title`: one line naming the behavior held.
- `kind`: `happy`, `edge` or `negative`.
- `covers`: the guidance the scenario holds in place, each entry a `file` under `.agents/` and a
  `section`. It decides when the scenario runs, as **When They Run** says.
- `prompt`: the exact message the agent receives.
- `expect`: the checks, each an `id` and a `check`. A check is one or two sentences measurable
  against what the run leaves behind: the tool log, the files written, the final reply. A term it
  needs is defined inside the check that uses it, and how many subagents launch is a check like any
  other.
- `history`: one entry per change, each a quoted `date`, a `route` of `behavior-change` or
  `test-cause`, the `pull_request` for a behavior change only, and a `reason`.

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

- **A round runs every regression scenario its diff touches, beside the change check and never
  instead of it.** A scenario is selected when either holds:
  - a `covers` entry names a changed file;
  - it belongs to a skill that reads a changed skill: one that declares the changed skill or cites
    it, as `skill-pass`'s **Source Check** lists readers.
- **Each selected scenario gets one reader and runs with no control**, since it asks only whether
  the skill still does what its scenario says. The scenarios join the round's grader batches of up
  to eight. So a round adds one reader per selected scenario and no writer, and its count grows only
  with the scenarios the diff selects.
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
    behavior, and its entry names that pull request in `pull_request` and gives the reason.
    Deleting a scenario folder takes this route, in the pull request that removes the behavior it
    holds.
  - **Test cause.** A fresh writer's rewrite, whose entry claims no change of behavior and carries
    no `pull_request`.
- **The test-cause route opens only on a grader's "ambiguous" return**, as **Checks** says; a
  "pass (note)" verdict, a pass carrying a reservation about the check, counts as one.
  - The writer, launched as `subagent-matrix` says, one for every check awaiting a rewrite at that
    point, gets the check, the guidance it tests and the grader's two readings, and no transcript
    text, so the new text measures the guidance rather than one run's answer.
  - The rewritten check goes to an independent Diff gate, through `acceptance-gate`, before any
    rerun.
  - Every scenario the rewrite governs then reruns fresh, and its earlier results are kept for the
    record.
- **A check is never loosened so that a run passes.** A miss the guidance caused is repaired in the
  guidance. A rewrite answers an ambiguity in what the check says, never the verdict it gave.

## Isolation

- **A reader gets a real install of the branch under test, never a reading list.** Run the
  repository's installer from a fresh copy of that branch into a fresh scratch home, the way a
  session gets its skills, and point the reader's harness at that home as its only user-level root.
  The reader then finds and loads skills itself, from the skill listing and descriptions. The
  installer leaves each skill's top-level `tests/` folder out, so no scenario reaches the install.
- **The reader's working directory is a copy of `fixture/`** with each tool built from
  `behavior.yaml` and that file left out. The prompt is the only message it receives, launched as
  the [reader dispatch reference](reader-dispatch.md) says. It never receives `scenario.yaml`.
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
- **Every term and exclusion a check applies is settled inside that check**, such as text that also
  occurs in the fixture, or fixed template labels, so two graders apply it the same way.
- **A grader that finds a check admitting two readings returns "ambiguous" with both readings and
  the verdict each gives**, and never chooses one. The check then takes the test-cause route in
  **Changing A Scenario**.
