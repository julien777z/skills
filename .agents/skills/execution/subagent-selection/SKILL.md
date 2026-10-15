---
name: subagent-selection
description: Apply when selecting a model for a live skill-verification chat or selecting and launching a subagent, including a fresh independent or read-only gate, reviewer, validator, or smoke reader. Resolve cheap, standard, advanced, and frontier capability levels from the current host catalogue, select the model explicitly, and route independent steps through a subagent of the running session.
short_description: 'Select a model capability level for live verification chats or subagent delegation.'
---

# Subagent Selection

Apply before every sub-agent delegation and when an owning skill requires a model capability level for a live
verification chat. Skills that use it should declare `subagent-selection` in their dependencies,
but a missing declaration does not bypass selection. Return the selection table to the calling
agent; this skill does not launch agents or change settings itself.

## Workflow

1. Identify the calling skill or direct task, its assigned roles or verification chat, and any
   explicit capability-level or model requirement. Inspect the current host's subagent catalogue and dispatch
   parameters, or its chat model picker, and read
   [model capabilities](references/model-capabilities.md). Keep catalogue discovery, an accepted dispatch,
   and a worker's self-reported runtime identity as separate evidence.
2. Resolve all four capability levels to the latest available model in each mapped family using the host's
   catalogue. Use only identifiers the host exposes through its catalogue, picker, or a successful explicit
   dispatch in the current host session; never store versioned IDs in skill guidance or invent an identifier.
   When catalogue ordering is ambiguous, use a documented current family alias; otherwise mark the row
   unavailable with the ambiguity as its reason.
3. Return all four rows even when some are unavailable. An unsupported host, absent family, or lack
   of explicit model selection makes that row unavailable; never silently substitute another family
   or inherit the orchestrator. A successful explicit dispatch establishes that its requested identifier
   was accepted for that launch. It does not establish the worker's runtime identifier: record that only
   when the host exposes the exact value. Generic provider or product branding, or no runtime identifier,
   is neither confirmation nor a contradiction of the accepted selection. Availability is not permission
   to change repository or global settings.
4. When a requested capability level or model is unavailable, apply a fallback only when the
   calling skill explicitly declares its direction and limits and it respects the user's explicit
   model or capability constraint. Report the original request as unavailable and name the actual
   fallback capability and model; never relabel it as the requested level. Without that policy,
   stop the dependent step and report the unavailable request, host capability and waiting work to
   the caller; do not substitute another model. The caller either follows its own in-process route
   or retains the concrete hold for the user. Preserve one resolved model within comparison pairs.
5. The calling agent chooses a capability level and reasoning effort for each role or chat. Honor the user's explicit model or capability-level constraint first,
   then the calling skill's capability level. For a live skill-verification chat, choose the least-capable available
   model; otherwise use the task criteria in the table, with **standard** as the default. Reserve
   frontier for the most demanding assignments unless specifically required. Use **medium** reasoning
   for bounded checks and **high** for complex, cross-cutting work; never dispatch a subagent at any
   other reasoning effort. An explicit user model override still must resolve to a supported host
   identifier; report it as an override rather than relabeling it as a different capability level.
6. Select the chosen identifier and reasoning effort explicitly when starting a verification chat or
   dispatching a sub-agent. For Codex `spawn_agent`, use `fork_turns: "none"` with a self-contained
   assignment, scope, constraints, and reading list so model inheritance cannot override selection.
   Reuse the resolved table while the host catalogue is unchanged; resolve again when it changes.
   Preserve one resolved model and reasoning effort within each comparison pair.

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
- **An independent step gets a newly launched subagent for every question it answers.** A gate,
  finding validator or smoke reader that has answered about an item is never resumed, messaged or
  reused for a later round on it — not to judge the repair of its own flag or a revised item — since
  its answer would then rest on its own earlier verdict. A skill whose procedure reuses a reviewer
  on purpose, such as a simplification rescan, says so where it does.
- **A worker whose host gives it no agent tool hands the step up.** It writes the complete
  assignment — the inputs, the question, the reading list, the output shape — to a file, asks the
  agent that delegated to it to run that file as a subagent at the chosen capability level, and waits for the
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
- **Assign one implementation owner per coherent scope, and a fresh worker for each delegated
  task.** The primary agent retains integration, dependencies and product decisions. Delegate
  independently owned scopes with explicit files, inputs, expected result and handoff; do not split
  a coupled feature among workers merely to increase parallelism. Workers may build in parallel
  only when their edits and resources do not overlap and neither needs an unsettled output from the
  other. A worker ends with its task; the next gets a fresh context. Read-only gates and reviews may
  run alongside building at the cadence their owning skill sets.

## Output

Return this table to the calling agent, using actual resolved identifiers rather than
placeholders. For an unavailable row, use `unavailable` for the model and state the reason in Status.
The calling agent then records the selected capability level per role or chat, or the explicit user override.

```markdown
Caller: <skill name or direct task>
Host: <current host>

| Capability | Resolved model              | Status                |
| ---------- | --------------------------- | --------------------- |
| cheap    | <identifier or unavailable> | available or <reason> |
| standard | <identifier or unavailable> | available or <reason> |
| advanced | <identifier or unavailable> | available or <reason> |
| frontier | <identifier or unavailable> | available or <reason> |
```
