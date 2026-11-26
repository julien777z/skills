# Regression Scenarios

Contents: **The Two Kinds**, **Where They Live**, **Format** (with one full example), **When They
Run**, **Changing An Expectation**, **Isolation**, **Criteria**.

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
  updates one as **Changing An Expectation** allows.

## Where They Live

- **Regression scenarios are the YAML files directly in a skill's own top-level `tests/` folder**,
  `<skill>/tests/<slug>.yaml`.
  - A `tests/` folder anywhere else is not one, such as a script's own `scripts/tests/`.
  - A scenario is placed in the skill its `pins` point at first.
- **The folder holds scenario YAML and nothing else.** Each scenario carries the fixture data it
  needs in its own `fixture.spec`. The runner, the builder that turns a spec into files and tools,
  and every transcript and grade stay private and untracked, because the repository keeps no test
  code.
- **A scenario parses with safe YAML loading**, and its contents meet these checks:
  - it carries every top-level key **Format** lists, `definitions` being optional;
  - its `kind` is `happy`, `edge` or `negative`;
  - each `pins` entry names a file that exists under `.agents/`.

  Every date is quoted, so safe loading reads it as a string. Quote any scalar holding a colon
  followed by a space, or a comma inside a flow mapping.

## Format

The top-level keys appear in this order:

- `schema`: the format version, `pinned-scenario/2`.
- `id`: `<skill>/<slug>`, matching the file's place.
- `kind`: `happy`, `edge` or `negative`.
- `title`: one line naming the behavior held.
- `pins`: the guidance this scenario holds in place. Each entry has a `file` under `.agents/`, a
  `section` and `holds`, a sentence saying what that section must keep doing.
- `reading_list`: every file under `.agents/` the reader loads, and nothing else. Conflicting guidance
  the decision meets is included.
- `situation`: prose on what the reader faces, for the writer and the grader.
- `fixture`, which has these fields:
  - `builder`: the fixture kind's name;
  - `options`;
  - `interface`: the contract the fixture keeps, exercised in a disposable copy before readers launch;
  - `records`: what the grader reads;
  - `checksummed`: files whose change a criterion detects;
  - `spec`: the whole fixture as data. `files` maps each path to its exact content, `images` lists
    placeholder images, and `tools` holds a `recording` rule plus each tool's responses. Any session
    builds the fixture from `spec` alone.
- `prompt`: what the reader receives, word for word.
- `actions`: what a reader following the guidance does, in order.
- `subagents`, which has these fields:
  - `fixed_by`: the guidance that sets the count;
  - `expected`: entries with `count`, each optionally with `step`, `role` and `at_once`;
  - `limits`.

  `expected: []` when nothing launches.
- `definitions`: a term each criterion uses, and each exclusion a measure applies.
- `expected`: the criteria. Each entry has an `id`, a `claim`, and a `measure` or a `measure_ref`
  naming another criterion's measure. Each may carry `on_fail: void` when a miss means the run tested
  nothing else.
- `history`: one flow mapping per change, each with these keys:
  - `date`: quoted;
  - `change`;
  - `by`;
  - `reason`, quoted when it holds a colon or a comma;
  - `cause` and `pull_request`, where **Changing An Expectation** asks for them.

This example is the trial's stalled-seat scenario. Its fixture spec, prompt, actions and criteria are
cut for space, and every key is kept:

```yaml
schema: pinned-scenario/2
id: subagent-matrix/stalled-default-seat-moves-to-own-provider
kind: happy
title: A default council seat on the other provider stalls and moves to the session's own provider

pins:
  - file: skills/execution/subagent-matrix/references/fallbacks.md
    section: A Launch On Another Provider's Model
    holds: the stalled other-provider launch is read at the first sibling's return and relaunched on
      the session's own provider at the same level, replacement first, cancel after

reading_list:
  - global.md
  - skills/review/council/SKILL.md
  - skills/execution/subagent-matrix/SKILL.md
  - skills/execution/subagent-matrix/references/fallbacks.md

situation: >
  A release checklist's open step asks for a council review in Ask mode with no provider requirement.
  The session runs on Claude. The Sol (Codex) seat is accepted and never shows activity; the Claude
  seats complete the moment they are read.

fixture:
  builder: launcher
  options: {steps: council}
  interface:
    - "agent launch refuses a missing or empty --brief-file and an unknown model"
    - "codex-provider agents are accepted and never show activity"
  records: [actions.log, trace.log, state/launches.tsv, state/briefs-at-launch/, final_reply]
  checksummed: []
  spec:
    files:
      release-checklist.md: |
        # Release checklist — rates-service 2.4

        1. [done] Run unit checks. Result: passed.
        2. Independent review of the retry change in `change.diff`: run `council` in Ask mode on it.
    tools:
      recording:
        - "every call appends `<seq>\t<tool> <subcommand>\t<arguments>` to actions.log, and its
          output and the clock to trace.log"
      agent:
        - "`status <name>` adds 20 to state/clock; a codex-provider launch prints `<name>: running;
          accepted but no activity: events=0`"

prompt: |
  You are working through `release-checklist.md` in the current directory. Do step 2 as the guidance
  you work under requires. `tools/README.md` describes the tools you have.

actions:
  - launches the three default seats in parallel
  - at the first sibling's return, makes its very next call a read of the Sol seat's activity
  - relaunches the Sol seat's assignment on Opus with the same brief, then cancels the Sol launch

subagents:
  fixed_by: council Members (three seats) and the fallbacks section (one replacement)
  expected:
    - {step: 2, role: council seat, count: 3, at_once: true}
    - {step: 2, role: replacement seat, count: 1}
  limits:
    codex_launches_for_step: 1

definitions:
  wait: a `tools/agent wait` call, whatever its --minutes

expected:
  - id: replace-then-cancel
    claim: The stalled launch is cancelled only once the replacement is accepted.
    measure: A `cancel` on the Sol seat comes after the replacement launch whose trace.log output
      reads accepted, and no cancel on the Sol seat precedes that acceptance.

history:
  - {date: "2026-11-25", change: added, by: pinned-scenario trial, reason: first pinned set}
```

## When They Run

- **A round runs every regression scenario its diff touches, beside the change check and never
  instead of it.** A scenario is selected when any of these holds:
  - it pins a changed file;
  - its `reading_list` lists a changed file;
  - it belongs to a skill that reads a changed skill: one that declares the changed skill or cites it,
    as `skill-pass`'s **Source Check** lists readers.
- **Each selected scenario gets one reader and runs with no control**, since it asks only whether
  the skill still does what its scenario says. The scenarios join the round's grader batches of up
  to eight. So a round adds one reader per selected scenario and no writer, and its count grows only
  with the scenarios the diff selects.
- **Each scenario passes or fails as a whole**, and passes only when every criterion passes.
- **A miss blocks like a failing edited run.** It is diagnosed at its owner, repaired and rerun
  within **Repair and rerun until verified** in `SKILL.md`. A miss caused by the guidance is
  repaired in the guidance. A miss caused by the scenario is repaired as **Changing An Expectation**
  says.

## Changing An Expectation

- **Adding a scenario needs nothing more** than its `history` line.
- **An `expected` entry or a `kind` changes or goes only in the pull request whose guidance diff
  changes that behavior.** Its `history` line names that pull request in `pull_request` and gives the
  reason, so a later reader can tell an intended change of behavior from a drifted test.
- **A criterion found ambiguous or unworkable is rewritten by a fresh writer**, launched as
  `subagent-matrix` says, one for every criterion awaiting a rewrite at that point.
  - The writer reads the criterion and the guidance it tests, and never a reader's report or a grade,
    so the new text measures the guidance rather than one run's answer.
  - The `history` line carries `cause: test cause`.
  - Every scenario the rewrite governs reruns fresh, and its earlier results are kept for the record.
- **A measure is never loosened so that a run passes.** A miss the guidance caused is repaired in the
  guidance. A rewrite answers an ambiguity in what the measure says, never the verdict it gave.

## Isolation

- **A reader receives only the compiled prompt, the files on its reading list and the fixture built
  from `fixture.spec`**, launched as the [reader dispatch reference](reader-dispatch.md) says. It
  never receives the scenario file, its `actions`, `subagents`, `definitions`, `expected` or
  `history`.
- **Every reader transcript is audited for a read of any `tests/` path**, whether by a file tool, a
  search or a shell command. A hit voids the run, and the run is rerun once the route that exposed
  the path is closed.
- **Only the grader sees the scenario YAML**, as the run's frozen criteria.
- **The writer of a scenario or a criterion is never the author of the guidance change under test**,
  so the expectation is not shaped by the change's own reasoning.

## Criteria

- **A measure reads recorded artifacts**: the action log, the tool outputs, the resulting files, a
  checksum, a sent message, the final reply. It never asks for the grader's impression of what the
  reader meant.
- **Every exclusion a measure applies goes in `definitions`** with the edge cases settled, such as
  text that also occurs in the fixture, or fixed template labels, so two graders apply it the same
  way.
- **A grader that finds a measure admitting two readings returns "ambiguous" with both readings and
  the verdict each gives**, and never chooses one. The criterion then goes to the fresh-writer
  rewrite above.
