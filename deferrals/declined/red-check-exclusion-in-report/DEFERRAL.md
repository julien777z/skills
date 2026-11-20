# A red non-essential check reported to the user

- **Status:** declined (closed by an acceptance-gate triage verdict)
- **Origin:** a skill-test finding on #377, accepted with the finding recorded under the review-round limit
- **Record key:** `red-check-exclusion-in-report`

## Problem

A reader that left a red non-essential check alone, correctly, still named that check and its exclusion in its report to the user.

## Why it is declined

The guidance already says it: `.agents/rules/github.md` records the check and its exclusion evidence in the task's record, and `pre-production` says never to report the red check. The reader had loaded both, and no step that admitted the report was traced.

## Reconsider when

A replay in which a reader that has loaded both still puts the exclusion in its report, with the step that produced it traced.

## Pickup scope

Trace the producing step and repair it at its owner.

## Supporting evidence

| Source | What it shows |
| --- | --- |
| `.agents/rules/github.md`, Merge Authorization | Where the exclusion is recorded |
| `.agents/skills/execution/pre-production/SKILL.md`, essential-checks bullet | That the red check is never reported |
