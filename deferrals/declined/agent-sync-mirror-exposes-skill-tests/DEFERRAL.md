# Agent Sync mirror exposes skills' regression scenarios

- **Status:** declined (closed by an acceptance-gate admission verdict)
- **Origin:** a skill-doctor leftover on #423, head `5ffbcd23`
- **Record key:** `agent-sync-mirror-exposes-skill-tests`

## Problem

Agent Sync (`julien777z/agent-sync-action`, run by `.github/workflows/agent-sync.yml`) writes each skill mirror under `.agents/.auto_generated/<harness>/skills/<skill>` as one symlink to the whole skill folder, so a skill's top-level `tests/` regression scenarios, expected answers included, show through the mirror. #423's installer leaves `tests/` out of installed copies; the mirror itself does not.

## Why it is declined

Not an external blocker: `julien777z/agent-sync-action` is the user's own repository, and work owed by a tool the user owns is never one. Today the exposure reaches no reader who does not already see the files: `bootstrap/install.sh` `link_source` installs from the mirror, and #423's `reconcile_skill_links` / `link_skill_without_scenarios` in `bootstrap/resources/skills.sh` check `$source/tests` on that path and build the installed copy without it. The final regression rerun at `5ffbcd23` found 0 `tests/` paths in the installed home and no read of `tests/` by any reader. An agent that sees the mirror's `tests/` is working inside this repository, where the canonical `.agents/skills/**/tests/` folders sit in the same checkout, so excluding them from the mirror would hide nothing.

## Reconsider when

Any reader loads skills from the Agent Sync mirror without going through the installer — a scenario harness, another repository's checkout of the mirror, or a harness reading `.agents/.auto_generated/<harness>/skills` directly.

## Pickup scope

Then the fix is in `julien777z/agent-sync-action`: a skill with a top-level `tests/` is mirrored as a directory with a regular-file `SKILL.md` and links to its other top-level entries, and this repository consumes it through its workflow.

## Supporting evidence

| Source | What it shows |
| --- | --- |
| `bootstrap/resources/skills.sh`, `link_skill_without_scenarios` | The installer's exclusion of `tests/` |
| `bootstrap/install.sh`, `link_source` | Installs read the mirror through that exclusion |
| `.github/workflows/agent-sync.yml` | Agent Sync writes the mirror on pushes to `main` |
| Regression rerun at `5ffbcd23`, `home-listing.txt` and isolation audit | 0 installed `tests/` paths; no reader read `tests/` |
