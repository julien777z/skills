# Pinned-lease criterion asking for report text

- **Status:** declined (closed by an acceptance-gate triage verdict)
- **Origin:** a skill-test finding on #392, accepted with the finding recorded under the review-round limit
- **Record key:** `modernize-lease-criterion-fault`

## Problem

A criterion required the modernize report to record the push command with its pinned lease.

## Why it is declined

A test fault: the reader did pin the lease, and `modernize-pr`'s Output asks only for the range-diff result and push; its guardrail governs the push itself.

## Reconsider when

A run that pushes without a pinned lease.

## Pickup scope

Rewrite the criterion before its scenario next runs.

## Supporting evidence

| Source | What it shows |
| --- | --- |
| `.agents/skills/git/modernize-pr/SKILL.md`, Output and Guardrails | What the report and the push require |
