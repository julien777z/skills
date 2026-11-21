# A red-lint scenario whose finding the reader removes before lint runs

- **Status:** declined (closed by an acceptance-gate triage verdict)
- **Origin:** a skill-test finding on #399, accepted with the finding recorded under the review-round limit
- **Record key:** `pre-production-scenario-lacks-red-check`

## Problem

A skill-test scenario for routing a red non-essential check to `pre-production` used a finding the reader had an editing reason to remove before lint first ran, so no red check ever appeared for the routing to act on.

## Why it is declined

Scenarios are private and written fresh for each round, so nothing in the repository holds the fault, and `test-skill` already requires the smallest environment that exercises the decision and repairs an invalid fixture before judging guidance.

## Reconsider when

The red-lint routing is tested again and its scenario still has no red finding the reader has no editing reason to touch, which would show the writer guidance permits the fault.

## Pickup scope

Repair the scenario-writing guidance in `test-skill` on that evidence.

## Supporting evidence

| Source | What it shows |
| --- | --- |
| `.agents/skills/authoring/test-skill/SKILL.md`, steps 2 and 7 | Environment that exercises the decision; fixture repair first |
| `.agents/rules/github.md`, Pre-Push Gate | The routing under test |
