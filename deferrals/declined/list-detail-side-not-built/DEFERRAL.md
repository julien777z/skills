# A list declared with a detail side that was never built

- **Status:** declined (closed by an acceptance-gate triage verdict)
- **Origin:** a skill-test finding on #389, accepted with the finding recorded under the review-round limit
- **Record key:** `list-detail-side-not-built`

## Problem

A reader declared a list's details as shown on a side panel without adding that panel.

## Why it is declined

Not a guidance defect: `roblox-ui` says a list with a detail side shows the selected entry there; the miss is unfinished work, not something the text permits.

## Reconsider when

A reader that builds the side panel and still cannot tell which of the list rules applies.

## Pickup scope

Clarify the list rules only on such evidence.

## Supporting evidence

| Source | What it shows |
| --- | --- |
| `.agents/skills/roblox/roblox-ui/SKILL.md` | The detail-side rule |
