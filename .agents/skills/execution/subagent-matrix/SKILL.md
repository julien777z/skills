---
name: subagent-matrix
description: Apply before every subagent launch, including a workflow coordinator or nested reviewer, and when selecting a live skill-verification model. Default reasoning effort to medium unless the user or invoking skill explicitly specifies another effort. Resolve the assignment role and verify the actual model, reasoning and history arguments before dispatch, including a fresh independent or read-only gate, reviewer, validator, or smoke reader. Resolve cheap, standard, advanced, and frontier capability levels from the host catalogue and documented dispatch candidates. Attempt the assigned work with a catalogue-hidden candidate before reporting unavailability or proposing a substitution, select the model explicitly, route independent steps through a subagent of the running session, and give the user complete direct-dispatch diagnostics when the launch cannot start.
short_description: 'Select a model capability level for live verification chats or subagent delegation.'
---

# Subagent Matrix

Apply before every sub-agent delegation and when an owning skill requires a model capability level for a live
verification chat. Skills that use it should declare `subagent-matrix` in their dependencies,
but a missing declaration does not bypass selection. Return the selection table to the calling
agent; the calling agent launches the actual assignment with the selected model.

## Workflow

1. Identify the calling skill or direct task, its assigned roles or verification chat, and any
   explicit capability-level or model requirement. Inspect the current host's subagent catalogue and dispatch
   parameters, or its chat model picker, and read
   [model capabilities](references/model-capabilities.md). Keep catalogue discovery, an accepted dispatch,
   and host-exposed runtime identity as separate evidence; a worker-reported label is only a label.
2. Resolve the assignment's role through **Codex role selections** in **model capabilities** first.
   Keep that selected identifier separate from the general capability table: a caller's tier or the
   coordinator's model cannot override a role selection. Resolve all four general capability levels
   to their mapped model families for assignments without a role selection. Use an exact user override only for
   the role, chat, and capability row it expressly governs; one explicitly scoped to every assignment governs
   every row. For every other row, prefer the latest matching identifier from the host's model-selection
   surface. If the family is absent there, read the host's documented candidates in **model capabilities**
   and use that family's candidate for the actual assignment. A family label is not a dispatch identifier,
   and a documented candidate is not a claim of support. Mark a resolved catalogue-hidden candidate `dispatch
   required` and proceed to step 3; never turn catalogue omission into an identifier hold or an override
   question while that candidate exists. Only when neither the host nor the reference nor an exact override
   for that assignment supplies a candidate, or the host has no explicit model-selection mechanism, record
   an identifier-resolution failure and use the in-process fallback for the assignment. Do not invent
   versions or aliases or silently substitute another family.
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
   never relabel it as the requested level. Without that policy, report the unsupported request and host
   receipt; do not substitute another model. If the required worker cannot launch, perform its assigned
   work in process and disclose the loss of independence. Preserve one
   resolved model within comparison pairs.
5. The calling agent chooses a capability level for each role or chat. Honor the user's
   explicit model or capability-level constraint first, then the configured role selection, then the
   calling skill's capability level. For a live
   skill-verification chat, choose the least-capable suitable mapped family, resolve its exact candidate, and
   launch the actual chat assignment; never skip that family because the catalogue omits it. Advance to another
   family only after an explicit unsupported receipt and only as the caller's fallback policy permits. Otherwise
   use the task criteria in the table, with **standard** as the default. Reserve frontier for the most demanding
   assignments unless specifically required. Default reasoning effort to **medium** for every
   assignment, including complex work, independent reviews, coordinators, and higher-capability
   models. Use another effort only when the user or invoking skill explicitly specifies it for
   that assignment; retain the instruction as dispatch evidence. Complexity, role, model capability,
   and the parent agent's own effort do not override the default. An explicit user model
   override is the exact dispatch candidate even when the catalogue omits it; report it as an override rather
   than relabeling it as a different capability level.
6. Select the chosen identifier and reasoning effort explicitly when starting a verification chat or
   dispatching a sub-agent. For Codex `spawn_agent`, use `fork_turns: "none"` with a self-contained
   assignment, scope, constraints, and reading list so model inheritance cannot override selection. Reuse a
   catalogue-confirmed selection while the host catalogue is unchanged. Reuse accepted-dispatch evidence only
   for the same active assignment; a later independent assignment launches its own worker. Preserve one
   resolved model and reasoning effort within each comparison pair.
7. Before sending a dispatch, compare its actual `model`, reasoning effort and history mode with
   the selected role receipt. A missing model argument is not an explicit selection, even when
   the parent happens to use the selected model. Correct the call before launching: on Codex,
   send the selected `model` and effort with `fork_turns: "none"`. Delegating through a coordinator
   does not change the child's role or permit a history fork to inherit the coordinator's model.
   Check that effort is medium or has the explicit instruction required above. Record the
   arguments the host accepted; a missing or mismatched field is an invalid dispatch,
   not review evidence. Replace that reader with an explicitly selected reader before counting
   the required review or gate as complete.

## Dispatch

**Launch every available subagent a skill calls for through the running session's agent tool.** It matters most for an independent step, one whose value is a judgement the
author does not make about its own work: an acceptance gate, a simplification or review lens, a
finding validator, a smoke-test reader, an audit's read-only reviewer. A subagent gives it a fresh
context and returns its verdict into the step waiting on it; nothing else does both.

- **Never route one elsewhere**: not through a new remote or cloud session, a scheduled trigger or
  routine, or a message asking any session but the delegating agent to run it. Those run outside
  the step, can fail setup or leave branches behind, and their verdict never returns to the run
  that waits on it.
- **When a required subagent cannot launch, perform its assignment in process.** Attempt the native
  dispatch when available, then apply the same scope and rubric in process if it cannot start or
  complete. Record the launch outcome and report that the result lacked independent review; never
  describe the in-process result as an independent verdict.
- **An independent step gets a newly launched subagent for every question it answers when available.** A gate,
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
  delegating agent to ask, perform the assigned step in process and report the loss of independence.
- **An early final does not finish the assignment.** Reconcile its retained results and live child
  jobs before replacing anything. The parent takes over unfinished coordination and keeps waiting
  for existing producers; it does not launch another coordinator to relay the same work. Replace
  only an unfinished execution that actually stopped, using a fresh worker with its branch,
  commits, uncommitted files and last hand-up. A crash, lost session or harness stop does not
  withdraw the user's authority, and neither a completed job nor a running one is repeated merely
  because its coordinator ended.
- **The producer retains its complete result before handing it up.** Give it a durable private
  destination and the owning workflow's required result contract in the brief. The parent reads
  that original and checks its target and required coverage before counting completion; a short
  original can be complete, while a rewritten summary cannot replace missing evidence. Recover
  an original from retained host output when available; otherwise repeat only the unproven step,
  not the surrounding cohort.
- **A worker hands each capture the user should see up the same way, as it is made.** Through any
  mid-run channel the host gives it to the delegating agent, it sends the file path and a line on
  what the capture shows; a worker whose only channel is its final message returns with the
  captures made since and is resumed. Work that will make such captures goes to a worker the
  delegating agent can resume or hear from mid-run; where the host offers neither, the delegating
  agent splits the work so each delegation ends at one such capture, and forwards each as it
  arrives.
- **Assign one implementation owner per coherent scope, and a fresh worker for each delegated
  task.** The primary agent retains integration, dependencies, product decisions and orchestration.
  Delegate work that produces an independent result, not a wrapper that only invokes another
  coordinator. Before launching, settle its checked prerequisites, immutable inputs, actual
  role-resolved launch arguments and required handoff; unresolved setup stays with the current
  owner rather than becoming a worker's discovery task. Delegate
  independently owned scopes with explicit files, inputs, expected result and handoff; do not split
  a coupled feature among workers merely to increase parallelism. Workers may build in parallel
  only when their edits and resources do not overlap and neither needs an unsettled output from the
  other. A worker ends with its task; the next gets a fresh context. Read-only gates and reviews may
  run alongside building at the cadence their owning skill sets.

## Launch Failure Reporting

When a required direct subagent dispatch cannot start, preserve its exact attempted dispatch and
record it and perform the assigned work in process. Do not turn a tool inventory from a nested bridge or an unrelated agent tool
into evidence about the native launcher's availability.

- Attempt the selected native dispatch once whenever its direct tool is exposed. Never claim an
  attempted invocation when the tool was not exposed.
- State the native tool's exact name, the assignment role and gated work, selected model, reasoning
  effort, history mode, and every argument sent to the host. Preserve argument names and values;
  omit only typed credentials or other secret values, retaining their field names and shapes.
- State the complete host receipt exactly when one exists. When no invocation was possible, say
  which direct tool surface was inspected and that there is no host receipt.
- Classify the outcome as one of: native tool not exposed, no resolved dispatch identifier, explicit
  unsupported-model receipt, rejected dispatch, capacity refusal, or accepted dispatch whose worker
  later failed. Do not collapse these into a generic unavailable-agent claim.
- Name the in-process fallback and its loss of independence; do not substitute an unrelated agent
  or claim it performed the assignment.

Use this user-facing shape whenever a launch failure is material to the task:

```markdown
## Subagent launch fallback

- **Assignment:** <required independent step>
- **Native tool:** `<exact direct tool name>` — <attempted or not exposed>
- **Selected dispatch:** `<model>` / `<reasoning effort>` / `<history mode>`
- **Arguments:** `<complete argument names and safe values>`
- **Host receipt:** <verbatim receipt, or `none — <why no invocation was possible>`>
- **Classification:** <one permitted classification and its evidence>
- **Fallback:** <in-process work and its loss of independence>
```

## Output

Return this table to the calling agent, using actual resolved identifiers rather than
placeholders. Record catalogue evidence and assignment evidence separately. A catalogue-hidden mapped family
with a resolved candidate is `dispatch required` until the actual assignment establishes acceptance or the host
explicitly rejects it as unsupported; after acceptance, record `accepted` while retaining `catalogue-hidden`.
Use `identifier required` only for an identifier-resolution hold established by Workflow step 2; report that
step's resolved candidate and state rather than independently selecting candidate sources here. Apply the
in-process fallback; do not describe the missing identifier as an unsupported-model receipt. Use `unavailable` only
when a host receipt explicitly rejects the exact candidate as unsupported. The calling agent then records the
selected capability level per role or chat, or the explicit user override.

```markdown
Caller: <skill name or direct task>
Host: <current host>
Role: <assignment role>
Selected dispatch: <exact identifier> / <reasoning effort> / <history mode>

| Capability | Catalogue state | Dispatch identifier | Assignment state |
| ---------- | --------------- | ------------------- | ---------------- |
| cheap | catalogue-confirmed or catalogue-hidden | <identifier or identifier required> | not requested, dispatch required, identifier required, accepted, or unavailable: <reason> |
| standard | catalogue-confirmed or catalogue-hidden | <identifier or identifier required> | not requested, dispatch required, identifier required, accepted, or unavailable: <reason> |
| advanced | catalogue-confirmed or catalogue-hidden | <identifier or identifier required> | not requested, dispatch required, identifier required, accepted, or unavailable: <reason> |
| frontier | catalogue-confirmed or catalogue-hidden | <identifier or identifier required> | not requested, dispatch required, identifier required, accepted, or unavailable: <reason> |
```

A calling skill that launches selected work retains the catalogue state, exact identifier, assignment state, and
host receipt in its own evidence. Runtime identity is additional evidence only when the host exposes it.
