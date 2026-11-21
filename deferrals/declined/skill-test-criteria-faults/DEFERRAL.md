# Skill-test criteria faults from one coordinated round

- **Status:** declined (closed by an acceptance-gate triage verdict)
- **Origin:** a skill-test finding on #389, accepted with the finding recorded under the review-round limit
- **Record key:** `skill-test-criteria-faults`

## Problem

Several criteria in one coordinated skill-test round were faulty: a `--help` invocation counted as a launch, a fixture that conflicted with the guidance, a stale listing criterion, two close-batch criteria contradicting `modernize-pr`'s directed close, and a criterion requiring a call no guidance names.

## Why it is declined

Test faults with nothing to change in the guidance.

## Reconsider when

Before each affected scenario next runs.

## Pickup scope

Fix each criterion before its scenario runs again.

## Supporting evidence

| Source | What it shows |
| --- | --- |
| `.agents/skills/authoring/test-skill/SKILL.md`, Freeze the inputs | How criteria are rewritten |
