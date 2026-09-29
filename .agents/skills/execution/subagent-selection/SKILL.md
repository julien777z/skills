---
name: subagent-selection
description: Apply whenever selecting or launching sub-agents, whether directly for a task or through another skill, and whenever a step calls for a fresh, independent or read-only subagent — a gate, a reviewer, a validator, a smoke reader — including when the host exposes no agent tool to launch one. Resolve cheap, standard, advanced, and frontier model tiers from the current host catalogue, use the chosen tier explicitly for every delegation, and route each independent step through a subagent of the running session.
short_description: 'Apply whenever selecting or launching sub-agents, whether directly for a task or through another skill.'
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

## Dispatch

**Every subagent a skill calls for runs as a subagent of the running session, launched through the
host's agent tool.** It matters most for an independent step, one whose value is a judgement the
author does not make about its own work: an acceptance gate, a simplification or review lens, a
finding validator, a smoke-test reader, an audit's read-only reviewer. A subagent gives it a fresh
context and returns its verdict into the step waiting on it; nothing else does both.

- **Never route one elsewhere**: not through a new remote or cloud session, a scheduled trigger or
  routine, or a message asking any session but the delegating agent to run it. Those run outside
  the step, can fail setup or leave branches behind, and their verdict never returns to the run
  that waits on it.
- **Never answer an independent step in process as a fallback.** The author answering the question
  is exactly what the step exists to prevent, whatever label the report gives it. A skill whose own
  procedure puts a pass in process, such as a small-scope simplification, is not handing it to a
  reviewer, and this leaves that pass alone.
- **A worker whose host gives it no agent tool hands the step up.** It writes the complete
  assignment — the inputs, the question, the reading list, the output shape — to a file, asks the
  agent that delegated to it to run that file as a subagent at the chosen tier, and waits for the
  verdict before going past the step. A worker whose only channel to that agent is its final
  message asks by returning: it ends its turn with the file path and the request, and resumes when
  the verdict comes back. The delegating agent runs it and returns the verdict unedited. With no
  delegating agent to ask, the step is reported as not run, and whatever it gates stays gated.

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
