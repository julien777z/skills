---
name: subagent-selection
description: Apply whenever selecting or launching sub-agents, whether directly for a task or through another skill. Resolve cheap, standard, advanced, and frontier model tiers from the current host catalogue and use the chosen tier explicitly for every delegation.
---

# Subagent Selection

Apply before every sub-agent delegation. Skills that delegate should declare `subagent-selection`
in their dependencies, but a missing declaration does not bypass selection. Return the selection
table to the delegating agent; this skill does not launch agents or change settings itself.

## Workflow

1. Identify the calling skill or direct task, its assigned roles, and any explicit tier or model
   requirement. Inspect the current host's subagent catalogue and dispatch parameters, and read
   [model tiers](references/model-tiers.md).
2. Resolve all four tiers to the latest available model in each mapped family using the host's
   catalogue. Use only identifiers the host actually exposes; never store versioned IDs in skill
   guidance or invent an identifier. When catalogue ordering is ambiguous, use a documented current
   family alias; otherwise mark the row unavailable with the ambiguity as its reason.
3. Return all four rows even when some are unavailable. An unsupported host, absent family, or lack
   of explicit model selection makes that row unavailable; never silently substitute another family
   or inherit the orchestrator. Disclose missing coverage or a blocker when a required tier cannot
   run. Availability is not permission to change repository or global settings.
4. The delegating agent chooses a tier for each role. Honor the user's explicit model or tier first,
   then the calling skill's tier; otherwise use the task criteria in the table, with **standard**
   as the default. Reserve frontier for the most demanding assignments unless specifically required.
   An explicit user model override still must resolve to a supported host identifier; report it as
   an override rather than relabeling it as a different tier.
5. Pass the chosen identifier explicitly at dispatch. For Codex `spawn_agent`, use
   `fork_turns: "none"` with a self-contained assignment, scope, constraints, and reading list so
   model inheritance cannot override selection. Reuse the resolved table while the host catalogue
   is unchanged; resolve again when it changes. Preserve one resolved model and reasoning effort
   within each comparison pair.

## Output

Return this table to the delegating agent, using actual resolved identifiers rather than
placeholders. For an unavailable row, use `unavailable` for the model and state the reason in Status.
The delegating agent then records the selected tier per role, or the explicit user override.

```markdown
Caller: <skill name or direct task>
Host: <current host>

| Tier     | Resolved model              | Status                |
| -------- | --------------------------- | --------------------- |
| cheap    | <identifier or unavailable> | available or <reason> |
| standard | <identifier or unavailable> | available or <reason> |
| advanced | <identifier or unavailable> | available or <reason> |
| frontier | <identifier or unavailable> | available or <reason> |
```
