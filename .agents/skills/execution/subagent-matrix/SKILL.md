---
name: subagent-matrix
description: Apply before every subagent launch, including a workflow coordinator or nested reviewer, and when selecting a live skill-verification model. Default reasoning effort to medium unless the user or invoking skill explicitly specifies another effort. Resolve the assignment role and verify the actual model, reasoning and history arguments before dispatch, including a fresh independent or read-only gate, reviewer, validator, or skill-test reader. Resolve cheap, standard, advanced, and frontier capability levels from the host catalog and documented dispatch candidates. Attempt the assigned work with a catalog-hidden candidate before reporting unavailability or proposing a substitution, select the model explicitly, route independent steps through a subagent of the running session, and give the user complete direct-dispatch diagnostics when the launch cannot start.
short_description: 'Select a model capability level for live verification chats or subagent delegation.'
---

# Subagent Matrix

Apply before every sub-agent delegation and when an owning skill requires a model capability level for a live
verification chat. Skills that use it should declare `subagent-matrix` in their dependencies,
but a missing declaration does not bypass selection. Return the selection table to the calling
agent; the calling agent launches the actual assignment with the selected model.

## Dependencies

- `share-captures`

## Workflow

1. Identify the calling skill or direct task, its assigned roles or verification chat, and any
   explicit capability-level or model requirement. Inspect the current host's subagent catalog and dispatch
   parameters, or its chat model picker, and read
   [model capabilities](references/model-capabilities.md). Keep catalog discovery, an accepted dispatch,
   and host-exposed runtime identity as separate evidence; a worker-reported label is only a label.
2. Resolve the capability level or model family the caller names to its family in **model
   capabilities**; the coordinator's model never overrides it. Use an exact user override only for
   the role, chat, and capability row it expressly governs; one explicitly scoped to every assignment governs
   every row. For every other row, prefer the latest matching identifier from the host's model-selection
   surface. If the family is absent there, read the host's documented candidates in **model capabilities**
   and use that family's candidate for the actual assignment. A family label is not a dispatch identifier,
   and a documented candidate is not a claim of support. Mark a resolved catalog-hidden candidate `dispatch
   required` and proceed to step 3; never turn catalog omission into an identifier hold or an override
   question while that candidate exists. Only when neither the host nor the reference nor an exact override
   for that assignment supplies a candidate, or the host has no explicit model-selection mechanism, record
   an identifier-resolution failure and use the launch fallback for the assignment. Do not invent
   versions or aliases or silently substitute another family.
3. Before a caller marks a requested capability level or explicit model unavailable, follows an
   unavailable-model fallback, or takes the launch fallback, launch the actual assigned work once with its exact
   candidate identifier and explicit reasoning effort when the native tool is available. A successful dispatch establishes that the host accepted
   the requested identifier for that launch; it does not establish catalog availability or runtime identity.
   An explicit host receipt that the candidate is unsupported establishes unavailability only as this step defines
   below. **A refusal that names its own cause or fix is a repair, never unavailability**: a client or runtime
   version too old, a sign-in, a disabled provider, a stale process. A rate limit or quota refusal is not this
   kind; it follows the capacity rule below. The repair is the first step and every
   fallback comes after it: update the client, sign in, enable the provider or restart the process, or confirm the
   condition no longer holds, then launch the same assignment again with the same identifier. Updating or
   repairing the agent's own client or runtime is that repair, never a repository or global settings change,
   which this step forbids below. Repair the component that actually holds the refused value, read from the
   running request path rather than from the refusal's own advice, such as a proxy between the agent and the
   provider. Only when that component is out of reach, as the global rules' bullet on a step only the user can
   take settles it, does its repair go to the user as such a step, with the exact command, while the fallback
   below proceeds for the assignment in hand. Unavailability, and every fallback or substitution it permits,
   starts only when that relaunch is refused again or the named repair cannot be made, recorded with both
   receipts and the repair attempted; only that is an explicit unsupported receipt wherever this skill or its
   callers name one. **A rate limit or quota refusal is temporary capacity, never unavailability**, even when it
   names a long reset time: it permits no fallback, no other provider and no absorbing the work into the
   coordinator's own process. Resume or relaunch the same worker on the same model once the limit no longer
   holds, read from the request path itself: the coordinator answering on that model, or the relaunch being
   accepted, shows it has cleared. The accepted worker
   performs the assignment; never launch a throwaway availability probe. Record the runtime identifier only
   when the host exposes its exact value. Generic provider or product
   branding, a worker-reported label, or no runtime identifier is neither confirmation nor a contradiction of
   the accepted selection. Availability is not permission to change repository or global settings, such as a
   model policy or a provider's configuration.
4. When a requested capability level or model is explicitly unsupported, apply a fallback only when the
   calling skill declares its direction and limits and it respects the user's explicit model or capability
   constraint. **A permitted fallback steps down as little as it can**, in this order, launching the actual
   assignment at each step and moving on only on an explicit unsupported receipt:
   1. earlier versions of the same family, newest first, found in the host's model-selection surface
      including entries it omits from its short list;
   2. the other provider's family at the requested level;
   3. the family one capability level below, on the same provider first, then the other provider's family at
      that level;
   4. each lower level in turn, never skipping one. A family another seat or worker already uses is still the
      next step: a fallback chooses by capability, never to keep the families distinct.
   Report the original request as unavailable and name the actual fallback capability and model;
   never relabel it as the requested level. Without that policy, report the unsupported request and host
   receipt; do not substitute another model. If the required worker cannot launch, apply the launch
   fallback below. Preserve one
   resolved model within comparison pairs.
5. The calling agent chooses a capability level for each role or chat. Honor the user's
   explicit model or capability-level constraint first, then the calling skill's capability level or
   named family. For a live
   skill-verification chat, choose the least-capable suitable mapped family, resolve its exact candidate, and
   launch the actual chat assignment; never skip that family because the catalog omits it. Advance to another
   family only after an explicit unsupported receipt and only as the caller's fallback policy permits. Otherwise
   use the task criteria in the table, with **standard** as the default. Reserve frontier for the most demanding
   assignments unless specifically required. Default reasoning effort to **medium** for every
   assignment, including complex work, independent reviews, coordinators, and higher-capability
   models. Use another effort only when the user or invoking skill explicitly specifies it for
   that assignment; retain the instruction as dispatch evidence. Complexity, role, model capability,
   and the parent agent's own effort do not override the default. An explicit user model
   override is the exact dispatch candidate even when the catalog omits it; report it as an override rather
   than relabeling it as a different capability level.
6. Select the chosen identifier and reasoning effort explicitly when starting a verification chat or
   dispatching a sub-agent. For Codex `spawn_agent`, use `fork_turns: "none"` with a self-contained
   assignment, scope, constraints, and reading list so model inheritance cannot override selection. Reuse a
   catalog-confirmed selection while the host catalog is unchanged. Reuse accepted-dispatch evidence only
   for the same active assignment; a later independent assignment launches its own worker. Preserve one
   resolved model and reasoning effort within each comparison pair.
7. Before sending a dispatch, compare its actual `model`, reasoning effort and history mode with
   the selection receipt. A missing model argument is not an explicit selection, even when
   the parent happens to use the selected model. Correct the call before launching: on Codex,
   send the selected `model` and effort with `fork_turns: "none"`. Delegating through a coordinator
   does not change the child's role or permit a history fork to inherit the coordinator's model.
   Check that effort is medium or has the explicit instruction required above. Record the
   arguments the host accepted; a missing or mismatched field is an invalid dispatch,
   not review evidence. Replace that reader with an explicitly selected reader before counting
   the required review or gate as complete.

## Dispatch

**Launch every available subagent a skill calls for through the running session's agent tool.** It matters most for an independent step, one whose value is a judgment the
author does not make about its own work. A subagent gives it a fresh
context and returns its verdict into the step waiting on it; nothing else does both.

- **Never route one elsewhere**: not through a new remote or cloud session, a scheduled trigger or
  routine, or a message asking any session but the delegating agent to run it. Those run outside
  the step, can fail setup or leave branches behind, and their verdict never returns to the run
  that waits on it.
- **Launch fallback: a worker that cannot launch a subagent its step needs hands the step up; never
  absorb it.** Attempt the native dispatch when available. This covers a host that gives the worker
  no agent tool and a native dispatch that fails other than by a capacity refusal, which step 3 waits out and relaunches, for reviewers, lenses, validators, gates and
  further implementation workers alike. The worker writes the complete assignment — the inputs, the
  question, the reading list, the output shape — to a file, asks the agent that delegated to it to
  run that file as a subagent at the chosen capability level, and waits for the verdict before going
  past the step; that agent launches the workers the step calls for, so each runs with its own
  context. Work the step splits among several workers is never carried by one of them alone, which
  cannot do it thoroughly. A worker whose only channel to that agent is its final message
  asks by returning: it ends its turn with the file path and the request, and resumes when the
  verdict comes back. The delegating agent runs it and returns the verdict unedited; when the
  finished worker cannot be resumed, the delegating agent carries out what the verdict calls for,
  such as the fix steps a flag names, under the follow-up bullet below. Only the top-level agent,
  with no delegating agent to ask, performs an assignment in process after its own launch fails,
  records the launch outcome, and reports that the result lacked independent review; never describe
  an in-process result as an independent verdict. A brief never tells a worker to fall back to
  in-process review or gating.
- **An independent step gets a newly launched subagent for every question it answers when available.** A gate,
  finding validator or skill-test reader that has answered about an item is never resumed, messaged or
  reused for a later round on it — not to judge the repair of its own flag or a revised item — since
  its answer would then rest on its own earlier verdict. A reviewer that a review loop keeps across
  its rounds, carrying the ledger, is a reviewer and not one of these.
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
  mid-run channel the host gives it to the delegating agent, it sends the file path and the
  caption `share-captures` requires, or, for a capture worker that captures without judging as
  [model capabilities](references/model-capabilities.md) says, what each capture shows, leaving its
  reading and caption to the delegating agent; a worker whose only channel is its final message
  returns with the captures made since and is resumed. Work that will make such captures goes to a worker the
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
- **A delegated task is one plan step or one fix round, never a phase**, so each worker's context
  stays the size of its step. A follow-up after a worker's task ended — a gate's fix steps, a
  review's findings, a reviewer's question — is a new task: assign nontrivial execution to a fresh
  worker with the findings, the files they name, the branch and its head. File count alone does not
  make a task trivial. A finished worker is never resumed for a follow-up, since
  resuming reloads its whole earlier context to make a small change.

## Launch Failure Reporting

When a required direct subagent dispatch cannot start, preserve its exact attempted dispatch,
record it, and apply the launch fallback in **Dispatch**; a capacity refusal is recorded and relaunched as Workflow step 3 says, never sent to that fallback. Do not turn a tool inventory from a nested bridge or an unrelated agent tool
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
- Name the fallback taken, with its loss of independence when it ran in process; do not substitute an unrelated agent or claim it performed the assignment.

Use this user-facing shape whenever a launch failure is material to the task:

```markdown
## Subagent launch fallback

- **Assignment:** <required independent step>
- **Native tool:** `<exact direct tool name>` — <attempted or not exposed>
- **Selected dispatch:** `<model>` / `<reasoning effort>` / `<history mode>`
- **Arguments:** `<complete argument names and safe values>`
- **Host receipt:** <verbatim receipt, or `none — <why no invocation was possible>`>
- **Classification:** <one permitted classification and its evidence>
- **Fallback:** <handed up to the delegating agent, or top-level in-process work and its loss of independence>
```

## Output

Return this table to the calling agent, using actual resolved identifiers rather than
placeholders. Record catalog evidence and assignment evidence separately. A catalog-hidden mapped family
with a resolved candidate is `dispatch required` until the actual assignment establishes acceptance or the host
explicitly rejects it as unsupported; after acceptance, record `accepted` while retaining `catalog-hidden`.
Use `identifier required` only for an identifier-resolution failure established by Workflow step 2; report that
step's resolved candidate and state rather than independently selecting candidate sources here. Apply the
launch fallback; do not describe the missing identifier as an unsupported-model receipt. Use `unavailable` only
when a host receipt explicitly rejects the exact candidate as unsupported after step 3's repair and relaunch. The calling agent then records the
selected capability level per role or chat, or the explicit user override.

```markdown
Caller: <skill name or direct task>
Host: <current host>
Role: <assignment role>
Selected dispatch: <exact identifier> / <reasoning effort> / <history mode>

| Capability | Catalog state | Dispatch identifier | Assignment state |
| ---------- | --------------- | ------------------- | ---------------- |
| cheap | catalog-confirmed or catalog-hidden | <identifier or identifier required> | not requested, dispatch required, identifier required, accepted, or unavailable: <reason> |
| standard | catalog-confirmed or catalog-hidden | <identifier or identifier required> | not requested, dispatch required, identifier required, accepted, or unavailable: <reason> |
| advanced | catalog-confirmed or catalog-hidden | <identifier or identifier required> | not requested, dispatch required, identifier required, accepted, or unavailable: <reason> |
| frontier | catalog-confirmed or catalog-hidden | <identifier or identifier required> | not requested, dispatch required, identifier required, accepted, or unavailable: <reason> |
```

A calling skill that launches selected work retains the catalog state, exact identifier, assignment state, and
host receipt in its own evidence. Runtime identity is additional evidence only when the host exposes it.
