# Sync-copy search done with the routes the rule bans

- **Status:** declined (closed by an acceptance-gate triage verdict)
- **Origin:** a skill-test finding on #389, accepted with the finding recorded under the review-round limit
- **Record key:** `sync-copy-search-banned-routes`

## Problem

Looking for file-sync copies, a reader used `git status` and a search that skipped the Git directory, and missed copies there and in an ignored folder.

## Why it is declined

The always-loaded sync-copy bullet in `.agents/global.md` names the search over the root, `git rev-parse --git-dir` and `--git-common-dir`, and bans `git status` and `ls`; the reader used the banned routes, and two of the scenario's criteria were ambiguous because its fixture conflicted with the guidance.

## Reconsider when

A valid run in which a reader follows the named routes and still misses an entry.

## Pickup scope

Repair the scenario's fixture first; then trace any remaining miss.

## Supporting evidence

| Source | What it shows |
| --- | --- |
| `.agents/global.md`, Tools and environments, sync-copy bullet | The required search routes |
