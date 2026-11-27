---
name: subagent-matrix
description: Apply when deciding whether to delegate work to a subagent at all, and before every subagent launch, including a workflow coordinator or nested reviewer, when selecting a live skill-verification model, and when resuming workers stopped by a rate limit or quota. Default reasoning effort to medium unless the user or invoking skill explicitly specifies another effort. Resolve the assignment role and verify the actual model, reasoning and history arguments before dispatch, including a fresh independent or read-only gate, reviewer, validator, or skill-test reader. Resolve cheap, standard, advanced, and specialist capability levels from the host catalog and current official provider sources. Attempt the assigned work with a catalog-hidden candidate before reporting unavailability or proposing a substitution, select the model explicitly, route independent steps through a subagent of the running session, and give the user complete direct-dispatch diagnostics when the launch cannot start.
short_description: 'Select a model capability level for live verification chats or subagent delegation.'
---

# Subagent Matrix

A skill that delegates declares this one in its dependencies; a missing declaration does not
bypass it.

## Dependencies
- `scope-of-change`

- `session-ledger`
- `share-media`

## When To Delegate

Delegate where the work splits into independent parts, needs an independent reader, or would crowd
the coordinator's own context; do small work directly. Start independent tasks concurrently when
their ownership, dependencies and resources permit. Delegation does not extend the user's
authorization or relax safety and sequencing requirements.

**A paused session launches nothing the pause covers; a launch the user asks for during it
runs.** Before any launch, read the task ledger through `session-ledger` for an open `hold` entry,
the user's pause on automated work; a review, gate, worker or check run in a scope it still covers,
one the entry does not list as resumed, waits in that entry's queue until the user resumes it.

## Matrix

These are model families, not pinned versions: each label selects the latest member of its family
on the current host. Cheap through advanced form the ordinary ladder; specialist is a separate tier.

| Capability | Codex family | Claude family | Selection | Fallback |
| ---------- | ------------ | ------------- | --------- | -------- |
| `cheap` | Terra | Sonnet | Lower-cost, bounded tasks and cheaper-model checks, and reviewers and simplification readers during implementation | Caller-authorized ordinary ladder |
| `standard` | Sol | Opus | Balanced reviews, analysis, and substantive tasks, the final review of a whole pull request, and a narrow independent judgment: a small packet whose answer accepts no diff for merge | Caller-authorized ordinary ladder |
| `advanced` | Astra | Fable | Difficult and the most demanding tasks, and an independent judgment that accepts a diff for merge or a plan before it is built | Caller-authorized ordinary ladder |
| `specialist` | — | Mythos | Only a calling skill explicitly selecting specialist | `advanced` by default, or caller-selected tier |

A dash means the provider has no family at that tier: an assignment at that tier on that provider
runs on the nearest tier below it that has one, such as a Codex specialist assignment on Astra at
`advanced`. That is the tier's mapping, not an unsupported-model fallback: the mapped tier counts
as the requested one under the capacity rule, a specialist assignment keeps its own holding rule,
and the dispatch line records the tier it ran at.

A capture worker, mechanically capturing the pages and states a brief lists, takes `cheap`. It
captures without judging; the delegating agent reads every image whole before relying on it or
sending it.

## Workflow

1. **Choose the tier.** The user's explicit model or tier for that role comes first, then the
   calling skill's tier or named family, then **Matrix**'s Selection column, with `standard` as
   the default. Advanced only where that column gives it or a caller requires it; specialist only
   when the calling skill selects it for that assignment, never by difficulty or as a fallback. A
   live skill-verification chat takes the least capable suitable tier. The coordinator's own model
   never decides. Reasoning effort is **medium** unless the user or invoking skill names another
   for that assignment; complexity, role, tier and the parent's own effort never change it.
2. **Resolve the exact model ID** for that family: the latest matching identifier the host's model
   selector offers, or, when it offers none, the current ID in the provider's official model
   catalog or release notes. An exact user override is used as given. **Never hard-code model IDs**
   in guidance, examples or fallback tables, and never guess one. When no ID resolves or the host
   has no model selector, take the launch fallback under **Dispatch**.
3. **Launch the actual assignment with that ID.** A catalog that omits a family is no evidence it
   is unavailable; only the host's explicit unsupported receipt for the launch is. Never launch a
   throwaway availability probe, and never change repository or global settings, such as a model
   policy or provider configuration, to make a launch work.
   - **A refusal that names its own fix is repaired, then the same launch is retried**: a client
     too old, a sign-in, a disabled provider, a stale process. Repair the component that holds the
     refused value, found from the running request path, such as a proxy, rather than from the
     refusal's advice. Only a repair that needs the user's own identity, device or password goes to
     the user, as a question with the exact command.
   - **A capacity refusal of a launch moves the assignment to the same tier on the other provider**,
     with the same brief and effort, unless the user or calling skill requires a provider or exact
     model, in which case it reruns there when capacity returns. When that also refuses, relaunch on
     whichever permitted model clears first: an accepted launch, or the coordinator answering on that
     model, shows it has cleared. Capacity is never unavailability: it allows no lower tier, no
     in-process work and no hold.
   - **A running worker a capacity refusal stopped is resumed, not relaunched**: at once, in its own
     thread so it keeps its context, within the count **Dispatch** allows, whatever model the
     coordinator answers on. The coordinator answering at all is reason enough, and an accepted
     resume shows capacity has cleared; the resume is the assigned work, never a probe. It is never
     scheduled for the reset time the refusal names, and a refused resume is retried at the
     delegating agent's next check of it rather than moved, since moving would lose that context.
   - **An explicit unsupported receipt** allows a fallback only when the calling skill declares one
     and the candidate meets every provider, model or tier requirement; otherwise report the receipt
     and substitute nothing. A permitted fallback steps down as little as it can, launching the
     assignment at each step and moving on only on another unsupported receipt: earlier versions of
     the same family, newest first; the other provider's family at that tier; then each lower tier
     in turn, same provider first, never skipping one, even to a family another seat already uses. A
     specialist assignment, on an unsupported or a denied receipt, instead falls back as its
     **Matrix** row says, holding when that would break the user's constraint or is itself
     unsupported. Report the original request as unavailable and name the tier and model actually
     used.
   - A comparison pair keeps one model and effort on both sides through every relaunch.
4. **Send the dispatch explicitly**: the selected model and effort as arguments, and no inherited
   history, with a self-contained brief (on Codex `spawn_agent`, `fork_turns: "none"`). Check the
   call's actual arguments before sending; a missing model argument is no selection even when the
   parent runs the same model. A dispatch with a missing or mismatched field is invalid: replace
   that reader before counting its review or gate. Each later independent assignment launches its
   own worker.

## Dispatch

**Launch every available subagent a skill calls for through the running session's agent tool.** It
matters most for an independent step, one whose value is a judgment the author does not make about
its own work: a subagent gives it a fresh context and returns its verdict into the step waiting on it.

- **Never route one elsewhere**: not through a new remote or cloud session, a scheduled trigger or
  routine, or a message asking any session but the delegating agent to run it; their verdicts never
  return to the waiting step. The one exception is a reader whose test requires that it load no
  installed copy of the guidance under test: it runs as a local headless harness process the
  running session starts and waits on, with its user-level skill and rule roots pointed at a
  scratch root, and hands back its complete original output.
- **Launch fallback: a worker that cannot launch a subagent its step needs hands the step up; never
  absorb it.** After the native dispatch fails for a reason Workflow step 3 does not repair, hand
  the delegating agent the complete assignment: inputs, question, reading list, output shape, tier,
  provider or model requirements, fallback policy and launch receipts. A worker whose only channel
  is its final message ends its turn with the file path and the request and resumes when the
  verdict returns; when it cannot be resumed, the delegating agent carries out what the verdict
  calls for under the follow-up bullet below. Work split among several workers is never carried by
  one of them alone. Only the top-level agent, with no one to hand it to, runs an assignment in
  process, and reports that the result lacked independent review: such a result never admits the
  change it judges, so that step stays a gate until a launched subagent answers it. A brief never
  tells a worker to fall back to in-process review.
- **An independent step gets a newly launched subagent for every question it answers.** A gate,
  finding validator, skill-test reader or grader that has answered about an item is never resumed
  or reused for a later round on it, including judging the repair of its own flag. A verdict
  waiting only on evidence it names is not yet an answer: the same run receives that evidence. A
  review loop's reviewer kept across rounds is a reviewer, not one of these.
- **An early final does not finish the assignment.** Reconcile its retained results and live child
  jobs before replacing anything; the parent takes over unfinished coordination rather than
  launching another coordinator. Replace only an execution that actually stopped, with a fresh
  worker given its branch, commits, uncommitted files and last hand-up. A crash or harness stop
  does not withdraw the user's authority or make finished work repeat.
- **The producer retains its complete result before handing it up**, at a durable private
  destination the brief names, in the owning workflow's result contract. The parent reads that
  original and checks its target and coverage before counting completion; a rewritten summary
  never replaces missing evidence. Recover an original from host output when possible; otherwise
  repeat only the unproven step.
- **A worker hands each capture the user should see up as it is made**, through any mid-run channel
  the host gives it, with the file path and the caption `share-media` requires; a capture worker
  sends what each capture shows and leaves the caption to the delegating agent. Work that makes
  such captures goes to a worker the delegating agent can resume or hear from mid-run; where the
  host offers neither, split the work so each delegation ends at one capture.
- **At most five execution workers run at once in a session**: subagents that implement,
  investigate or test a scope. A reviewer, gate, validator or reader a step requires is not one and
  starts when its step reaches it. Count the running workers before launching one; a host or
  provider limit that stops workers lowers the count until they run cleanly.
- **Work that shares an area with a running worker's scope goes to that worker**, such as the same
  feature, window, files or verification setup, not to a new one.
- **Work that needs a new worker while five run waits for a slot**, recorded with its brief, except
  work that removes what running workers are blocked on, such as a shared runner they queue for. A
  worker it unblocks pushes its work and pauses, the unblocking work takes that slot, with priority
  on the shared resource's lock where it has one, and the paused worker resumes once it lands.
- **One implementation owner per coherent scope.** A scope is a plan step that stands alone, the
  coupled steps of one feature built in order by one worker, or one fix round; steps are coupled
  when one reads another's schema, calls its interface or extends its code. Never split a coupled
  feature to gain parallelism; parallel workers need non-overlapping edits and resources. Settle
  prerequisites, inputs and launch arguments before launching; the primary agent keeps
  integration, product decisions and orchestration. A follow-up after a worker's task ended, such as
  a gate's fix steps or a review's findings, goes to a fresh worker with the brief's fix form, never
  to the finished one. Read-only gates and reviews may run beside building as their skill sets.
- **Bulk pull requests are one scope.** Pull requests opened together to make one similar change
  across repositories get one worker that implements all of them, never one per pull request, and
  are reviewed and gated once as a set.
- **Every implementation and fix worker gets the [worker brief](references/worker-brief.md) with
  every field filled.** A skill that delegates edits fills that form rather than writing its own.
- **A running worker is told when guidance it works under changes**: which file, each section that
  changed, and what it says.
- **An editing worker's own worktree** is the host's worktree isolation where it offers one,
  otherwise a worktree the brief names under the task's working-files folder, made from the branch
  the worker pushes to.

## Launch Failure Reporting

When a required launch cannot start and the failure matters to the task, report it in this shape.
Attempt the native dispatch once whenever its tool is exposed, and never claim an attempt when it
was not. Keep every argument name and value, omitting only secret values.

```markdown
## Subagent launch fallback

- **Assignment:** <required independent step>
- **Native tool:** `<exact direct tool name>` — <attempted or not exposed>
- **Selected dispatch:** `<model>` / `<reasoning effort>` / `<history mode>`
- **Arguments:** `<complete argument names and safe values>`
- **Host receipt:** <verbatim receipt, or `none — <why no invocation was possible>`>
- **Classification:** <native tool not exposed | no resolved model ID | unsupported-model receipt | denied receipt | rejected dispatch | capacity refusal | accepted worker later failed>
- **Fallback:** <assignment held, handed up to the delegating agent, or top-level in-process work and its loss of independence>
```

## Output

Each launch keeps one record, which a calling skill retains in its own evidence:

```markdown
Dispatch: <role> — <tier> / <exact model ID> / <reasoning effort> / <history mode> — <host receipt> [— fallback from <requested tier and model>: <receipt>]
```

A worker's reported model name is a label, not evidence; record the runtime model only when the
host itself exposes it.
