# Merged pull requests named by number alone on the modernize dashboard

- **Status:** declined (closed by an acceptance-gate triage verdict)
- **Origin:** a skill-test finding on #392, accepted with the finding recorded under the review-round limit
- **Record key:** `modernize-dashboard-pr-naming`

## Problem

A reader named merged pull requests by number alone on the modernize dashboard.

## Why it is declined

The text is right and was loaded: `modernize-pr` names each pull request `repository#number` wherever the page names it, and the always-loaded link rule in `.agents/global.md` requires the repository in the link text when the text spans repositories.

## Reconsider when

A reader that applies both lines and still cannot tell whether a base change is covered.

## Pickup scope

Clarify `modernize-pr`'s naming line only on such evidence.

## Supporting evidence

| Source | What it shows |
| --- | --- |
| `.agents/skills/git/modernize-pr/SKILL.md`, dashboard | The naming requirement |
| `.agents/global.md`, User-Facing Output | Repository inside link text |
