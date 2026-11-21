# A selection menu rebuilt instead of asked through interactive-skill

- **Status:** declined (closed by an acceptance-gate triage verdict)
- **Origin:** a skill-test finding on #399, accepted with the finding recorded under the review-round limit
- **Record key:** `skill-gauntlet-selection-menu-bypass`

## Problem

A `skill-gauntlet` reader built its own selection menu and never invoked `interactive-skill`.

## Why it is declined

The guidance already requires the behavior and is reachable: `skill-gauntlet` says to invoke `interactive-skill` to ask its selection and lists it among its dependencies, and `interactive-skill`'s description says a declared menu is asked only through it. Another run on the same text did invoke it, so one miss in two runs shows no gap in the text.

## Reconsider when

A later skill test on this text has the reader skip `interactive-skill` again; a repeated miss is diagnosed as an instruction not prominent enough.

## Pickup scope

Diagnose the decision step that skipped the invocation and repair it at its owner.

## Supporting evidence

| Source | What it shows |
| --- | --- |
| `.agents/skills/authoring/skill-gauntlet/SKILL.md`, step 3 | The invocation at the selection step |
| `.agents/skills/workspace/interactive-skill/SKILL.md`, description | A declared menu is asked only through it |
