# Little headroom in the generated AGENTS.md under its size cap

- **Status:** declined (closed by an acceptance-gate admission verdict)
- **Origin:** a skill-doctor leftover on #423, head `5ffbcd23`
- **Record key:** `generated-agents-md-cap-headroom`

## Problem

The root `AGENTS.md` that Agent Sync generates from `.agents/global.md`, the always-apply rules and `.agents/project.md` is 32,759 bytes at #423's head, 9 bytes under the 32,768 bytes Codex reads by default (35,190 bytes before #423). The next growth of any of those sources fails the source check until room is made.

## Why it is declined

A check already enforces it on demand: #423's `find_instructions_cap_problems`, run from `mirror_in_scratch` in `skill-pass/scripts/validate_sources.py`, refuses a generated instructions file past the cap, and the authoring budget rule makes the change that grows the file make its room in the same change. Nothing is over budget today: the file is within the cap and `.agents/global.md` is 169 lines, under its 200-line budget. A record would be a second copy of the check that goes stale.

## Reconsider when

The cap check is removed or stops running on the generated file, or a host with a smaller cap starts loading it.

## Pickup scope

None while the check runs; a change that grows an always-loaded source makes room in that change.

## Supporting evidence

| Source | What it shows |
| --- | --- |
| `.agents/skills/authoring/skill-pass/scripts/validate_sources.py`, `find_instructions_cap_problems` and `CODEX_INSTRUCTIONS_CAP_BYTES` | The check that refuses a generated file past 32,768 bytes |
| `.agents/skills/authoring/skill-pass/SKILL.md`, Source Check | States the refusal on any branch |
| `.agents/skills/authoring/skill-pass/references/authoring.md`, size budgets | A change that grows a file past its budget makes room in the same change; the generated file is measured against its host's cap |
| Regression rerun mirror at `5ffbcd23` | Generated `AGENTS.md` measured at 32,759 bytes |
