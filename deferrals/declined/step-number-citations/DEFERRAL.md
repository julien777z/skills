# Guidance that cites a step by its number

- **Status:** declined (closed by an acceptance-gate admission verdict)
- **Origin:** cleanup a review of #402 left alone because the sweep reached past the files that pull request changed
- **Record key:** `step-number-citations`

## Problem

About 19 owned guidance files cite a step by its number, such as "step 4" or "**Workflow** steps 1
to 4", where `skill-pass`'s authoring reference asks that a section be cited by its name, so a
citation survives a list being renumbered.

## Why it is declined

Every such citation checked resolves to the step it names today, so no reader is misled. The
`skill-doctor` **Stale** lens finds each one on demand, and `skill-pass`'s **Writing** rule
converts a skill's citations whenever that skill is next edited, so a record would only repeat
both.

## Reconsider when

A step-number citation is found that no longer lands on the step it names. That citation is a
defect and is fixed on sight, never recorded.

## Pickup scope

Every citation in owned guidance, excluding skills the external-resources registry refreshes,
names the passage it points to by its section heading or bold lead, so the reader lands on one
passage however the list is later renumbered.

## Supporting evidence

| Source | What it shows |
| --- | --- |
| `.agents/skills/authoring/skill-pass/references/authoring.md`, Writing | Cite a section by its name, never by a step number |
| `.agents/skills/doctors/skill-doctor/SKILL.md`, Stale lens | Finds a section cited by a step number |
