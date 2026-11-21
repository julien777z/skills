# A report offering to revert a design change

- **Status:** declined (closed by an acceptance-gate triage verdict)
- **Origin:** a skill-test finding on #398, accepted with the finding recorded under the review-round limit
- **Record key:** `report-offers-revert`

## Problem

A reader's report ended with an offer to revert a design change it made on its own authority.

## Why it is declined

The text is right and was loaded: `.agents/global.md` User-Facing Output says such work is reported as made, with no offer to revert it; the skill whose closing-line rule could produce such an offer was not loaded.

## Reconsider when

A traced replay naming the step that produces the offer.

## Pickup scope

Repair that step.

## Supporting evidence

| Source | What it shows |
| --- | --- |
| `.agents/global.md`, User-Facing Output | Reported as made, no offer to revert |
