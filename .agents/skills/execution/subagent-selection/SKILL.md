---
name: subagent-selection
description: Apply when selecting a model for a live skill-verification chat or selecting and launching a subagent, including a fresh independent or read-only gate, reviewer, validator, or smoke reader. Resolve cheap, standard, advanced, and frontier tiers from the current host catalogue, select the model explicitly, and route independent steps through a subagent of the running session.
short_description: 'Select a model tier for live verification chats or subagent delegation.'
---

# Subagent Selection

Apply before every sub-agent delegation and when an owning skill requires a model tier for a live
verification chat. Skills that use it should declare `subagent-selection` in their dependencies,
but a missing declaration does not bypass selection. Return the selection table to the calling
agent; this skill does not launch agents or change settings itself.

## Workflow

1. Identify the calling skill or direct task, its assigned roles or verification chat, and any
   explicit tier or model requirement. Inspect the current host's subagent catalogue and dispatch
   parameters, or its chat model picker, and read
   [model tiers](references/model-tiers.md).
2. Resolve all four tiers to the latest available model in each mapped family using the host's
   catalogue. Use only identifiers the host actually exposes; never store versioned IDs in skill
   guidance or invent an identifier. When catalogue ordering is ambiguous, use a documented current
   family alias; otherwise mark the row unavailable with the ambiguity as its reason.
3. Return all four rows even when some are unavailable. An unsupported host, absent family, or lack
   of explicit model selection makes that row unavailable; never silently substitute another family
   or inherit the orchestrator. Disclose missing coverage or a blocker when a required tier cannot
   run. Availability is not permission to change repository or global settings.
4. The calling agent chooses a tier for each role or chat. Honor the user's explicit model or tier first,
   then the calling skill's tier. For a live skill-verification chat, choose the lowest available
   tier; otherwise use the task criteria in the table, with **standard** as the default. Reserve
   frontier for the most demanding assignments unless specifically required. An explicit user model
   override still must resolve to a supported host identifier; report it as an override rather than
   relabeling it as a different tier.
5. Select the chosen identifier explicitly when starting a verification chat or dispatching a
   sub-agent. For Codex `spawn_agent`, use
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
  verdict before going past the step. The gate over a finished task's diff is not such a step: the
  delegating agent runs it from the branch and head the worker reports, under the delegated-edits bullet
  of `execute-task`'s **Pre-Push Gate**. A worker whose only channel to
  that agent is its final message asks by returning: it ends its turn with the file path and the
  request, and resumes when the verdict comes back. The delegating agent runs it and returns the verdict unedited; when the
  finished worker cannot be resumed, the delegating agent carries out what the verdict calls for,
  such as the fix steps a flag names, itself. With no
  delegating agent to ask, the step is reported as not run, and whatever it gates stays gated.
- **A worker that ends before its work is done is replaced, never reported as a question.** A
  crash, a lost session or a harness stop, including the stop a user's interruption of the
  delegating agent's turn sends to every running worker, leaves the work as authorized as it was.
  Start a new worker on the same assignment at once, briefed from what the stopped one left: its
  branch, its commits, its uncommitted files and its last hand-up. A notice that a worker will not
  be resumed says only that its context is gone; the user's own words withdrawing that work are
  what stop it.
- **A worker hands each capture the user should see up the same way, as it is made.** Through any
  mid-run channel the host gives it to the delegating agent, it sends the file path and a line on
  what the capture shows; a worker whose only channel is its final message returns with the
  captures made since and is resumed. Work that will make such captures goes to a worker the
  delegating agent can resume or hear from mid-run; where the host offers neither, the delegating
  agent splits the work so each delegation ends at one such capture, and forwards each as it
  arrives.
- **Build work goes to one implementation worker at a time, and a fresh one for each task.** A
  worker that edits files is started for one task and ends with it; the next task gets a new worker,
  never one still carrying an earlier task's history, and a session never runs two building at
  once. A short history keeps each of its steps cheap. Its brief names the exact files to change,
  and the files to read beside them, so its steps go on the change rather than on searching.
  Read-only steps — a gate, a reviewer, a validator — may still run beside it, at the cadence their
  owning skill sets.

## Output

Return this table to the calling agent, using actual resolved identifiers rather than
placeholders. For an unavailable row, use `unavailable` for the model and state the reason in Status.
The calling agent then records the selected tier per role or chat, or the explicit user override.

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
