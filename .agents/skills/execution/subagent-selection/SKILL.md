---
name: subagent-selection
description: Apply when selecting a model for a live skill-verification chat or selecting and launching a subagent, including a fresh independent or read-only gate, reviewer, validator, or smoke reader. Resolve cheap, standard, advanced, and frontier capability levels from the host catalogue and documented dispatch candidates. Attempt the assigned work with a catalogue-hidden candidate before reporting unavailability or proposing a substitution, select the model explicitly, and route independent steps through a subagent of the running session.
short_description: 'Select a model capability level for live verification chats or subagent delegation.'
---

# Subagent Selection

Apply before every sub-agent delegation and when an owning skill requires a model capability level for a live
verification chat. Skills that use it should declare `subagent-selection` in their dependencies,
but a missing declaration does not bypass selection. Return the selection table to the calling
agent; the calling agent launches the actual assignment with the selected model.

## Workflow

1. Identify the calling skill or direct task, its assigned roles or verification chat, and any
   explicit capability-level or model requirement. Inspect the current host's subagent catalogue and dispatch
   parameters, or its chat model picker, and read
   [model capabilities](references/model-capabilities.md). Keep catalogue discovery, an accepted dispatch,
   and host-exposed runtime identity as separate evidence; a worker-reported label is only a label.
2. Resolve all four capability levels to their mapped model families. Use the user's exact model override
   when present; otherwise prefer the latest matching identifier from the host's model-selection surface.
   If the family is absent there, read the host's documented candidates in **model capabilities** and use
   that family's candidate for the actual assignment. A family label is not a dispatch identifier, and a
   documented candidate is not a claim of support. Mark a resolved catalogue-hidden candidate `dispatch
   required` and proceed to step 3; never turn catalogue omission into an identifier hold or an override
   question while that candidate exists. Only when neither the host nor the reference nor an exact user
   override supplies a candidate, or the host has no explicit model-selection mechanism, record an
   identifier-resolution hold. Do not invent versions or aliases or silently substitute another family.
3. Before a caller marks a requested capability level or explicit model unavailable, follows an
   unavailable-model fallback, or takes an in-process route, launch the actual assigned work once with its exact
   candidate identifier and explicit reasoning effort. A successful dispatch establishes that the host accepted
   the requested identifier for that launch; it does not establish catalogue availability or runtime identity.
   An explicit host receipt that the candidate is unsupported establishes unavailability. The accepted worker
   performs the assignment; never launch a throwaway availability probe. Record the runtime identifier only
   when the host exposes its exact value. Generic provider or product
   branding, a worker-reported label, or no runtime identifier is neither confirmation nor a contradiction of
   the accepted selection. Availability is not permission to change repository or global settings.
4. When a requested capability level or model is explicitly unsupported, apply a fallback only when the
   calling skill declares its direction and limits and it respects the user's explicit model or capability
   constraint. Report the original request as unavailable and name the actual fallback capability and model;
   never relabel it as the requested level. Without that policy, stop the dependent step and report the
   unsupported request, host receipt, and waiting work to the caller; do not substitute another model or
   replace an independent step in process. Preserve one resolved model within comparison pairs.
5. The calling agent chooses a capability level and reasoning effort for each role or chat. Honor the user's
   explicit model or capability-level constraint first, then the calling skill's capability level. For a live
   skill-verification chat, choose the least-capable suitable mapped family, resolve its exact candidate, and
   launch the actual chat assignment; never skip that family because the catalogue omits it. Advance to another
   family only after an explicit unsupported receipt and only as the caller's fallback policy permits. Otherwise
   use the task criteria in the table, with **standard** as the default. Reserve frontier for the most demanding
   assignments unless specifically required. Use **medium** reasoning for bounded checks and **high** for
   complex, cross-cutting work; never dispatch a subagent at any other reasoning effort. An explicit user model
   override is the exact dispatch candidate even when the catalogue omits it; report it as an override rather
   than relabeling it as a different capability level.
6. Select the chosen identifier and reasoning effort explicitly when starting a verification chat or
   dispatching a sub-agent. For Codex `spawn_agent`, use `fork_turns: "none"` with a self-contained
   assignment, scope, constraints, and reading list so model inheritance cannot override selection. Reuse a
   catalogue-confirmed selection while the host catalogue is unchanged. Reuse accepted-dispatch evidence only
   for the same active assignment; a later independent assignment launches its own worker. Preserve one
   resolved model and reasoning effort within each comparison pair.

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
placeholders. Record catalogue evidence and assignment evidence separately. A catalogue-hidden mapped family
with a resolved candidate is `dispatch required` until the actual assignment establishes acceptance or the host
explicitly rejects it as unsupported; after acceptance, record `accepted` while retaining `catalogue-hidden`.
Use `identifier required` only for an identifier-resolution hold established by Workflow step 2; report that
step's resolved candidate and state rather than independently selecting candidate sources here. This is a
hold, never an unavailable-model result. Use `unavailable` only
when a host receipt explicitly rejects the exact candidate as unsupported. The calling agent then records the
selected capability level per role or chat, or the explicit user override.

```markdown
Caller: <skill name or direct task>
Host: <current host>

| Capability | Catalogue state | Dispatch identifier | Assignment state |
| ---------- | --------------- | ------------------- | ---------------- |
| cheap | catalogue-confirmed or catalogue-hidden | <identifier or identifier required> | not requested, dispatch required, identifier required, accepted, or unavailable: <reason> |
| standard | catalogue-confirmed or catalogue-hidden | <identifier or identifier required> | not requested, dispatch required, identifier required, accepted, or unavailable: <reason> |
| advanced | catalogue-confirmed or catalogue-hidden | <identifier or identifier required> | not requested, dispatch required, identifier required, accepted, or unavailable: <reason> |
| frontier | catalogue-confirmed or catalogue-hidden | <identifier or identifier required> | not requested, dispatch required, identifier required, accepted, or unavailable: <reason> |
```

A calling skill that launches selected work retains the catalogue state, exact identifier, assignment state, and
host receipt in its own evidence. Runtime identity is additional evidence only when the host exposes it.
