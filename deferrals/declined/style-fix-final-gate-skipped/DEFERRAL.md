# No final gate over a style fix

- **Status:** declined (closed by an acceptance-gate triage verdict)
- **Origin:** a skill-test finding on #398, accepted with the finding recorded under the review-round limit
- **Record key:** `style-fix-final-gate-skipped`

## Problem

A reader fixed a style flag and ended without the final acceptance that confirms it.

## Why it is declined

The text is right and was loaded: `execute-task` requires one final acceptance at completion, and `acceptance-gate` says final acceptance confirms style fixes; no step that admitted the skip was traced.

## Reconsider when

A traced replay that identifies the step admitting the skip.

## Pickup scope

Repair that step at its owner.

## Supporting evidence

| Source | What it shows |
| --- | --- |
| `.agents/skills/execution/execute-task/SKILL.md`, Completion | The final gate |
| `.agents/skills/review/acceptance-gate/SKILL.md`, Bounds | Style flags |
