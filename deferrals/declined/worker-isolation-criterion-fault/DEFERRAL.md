# Worker-isolation scenario grading a design choice

- **Status:** declined (closed by an acceptance-gate triage verdict)
- **Origin:** a skill-test finding on #398, accepted with the finding recorded under the review-round limit
- **Record key:** `worker-isolation-criterion-fault`

## Problem

A worker-isolation scenario's criterion graded how a structure was built rather than isolation or the audit.

## Why it is declined

A test fault: the always-loaded game-design bullet in `.agents/global.md` leaves that build to the agent.

## Reconsider when

Before the scenario next runs.

## Pickup scope

Rewrite the criterion.

## Supporting evidence

| Source | What it shows |
| --- | --- |
| `.agents/global.md`, Task execution and authorization | The game-design bullet |
