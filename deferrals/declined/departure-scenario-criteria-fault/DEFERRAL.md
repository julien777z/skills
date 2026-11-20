# Departure scenario with contradictory criteria

- **Status:** declined (closed by an acceptance-gate triage verdict)
- **Origin:** a skill-test finding on #389, accepted with the finding recorded under the review-round limit
- **Record key:** `departure-scenario-criteria-fault`

## Problem

A skill-test scenario for hiding a departed character missed, but its criteria needed a quest identifier the prompt never gave and contradicted each other.

## Why it is declined

A test fault: the `roblox-gameplay` departure rule needs no change.

## Reconsider when

A valid scenario in which the departure is told after the character's last interaction and the reader still keeps the character.

## Pickup scope

Rewrite the scenario's criteria before it next runs.

## Supporting evidence

| Source | What it shows |
| --- | --- |
| `.agents/skills/roblox/roblox-gameplay/SKILL.md` | The departure rule |
