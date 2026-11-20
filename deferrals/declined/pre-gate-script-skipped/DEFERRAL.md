# Python rule script skipped before a gate

- **Status:** declined (closed by an acceptance-gate triage verdict)
- **Origin:** a skill-test finding on #398, accepted with the finding recorded under the review-round limit
- **Record key:** `pre-gate-script-skipped`

## Problem

Readers dispatched a gate without first running the Python rule findings script.

## Why it is declined

The text is right and was loaded: `execute-task` runs the script before any gate over Python files, and `acceptance-gate` makes its output a required gate input, so a gate dispatched without it holds on missing evidence.

## Reconsider when

A gate that accepts without that output.

## Pickup scope

Repair the gate's evidence check on such evidence.

## Supporting evidence

| Source | What it shows |
| --- | --- |
| `.agents/skills/execution/execute-task/SKILL.md` | The pre-gate run |
| `.agents/skills/review/acceptance-gate/SKILL.md`, The Gate Subagent | The required input |
