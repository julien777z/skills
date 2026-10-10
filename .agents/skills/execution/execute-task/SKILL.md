---
name: execute-task
description: "Always run this. Invoke once at the start of every task authorized to change files, before recommending an implementation, delegating edits, or editing — including one whose edits sub-agents make, and one that only begins changing files because work turned up a defect — and keep it active until verified completion or explicit user stop or handoff. It plans first: it puts a plan to the user and waits for approval before editing, except for a trivial change, and plans each follow-up the same way. It then applies the repository's product constraints, fixes the bugs the work encounters rather than reporting them, commits each small step and pushes it promptly once its checks pass, keeps session-created source work to one pull request per repository, finishes each pull request with a simplification pass, a test sweep, an acceptance gate and a history rewrite before sending it for review, checks every outcome it reports at the source of truth, and delivers each repository independently. Never invoke it from inside a skill it runs."
short_description: 'Plan the change for approval, then apply repository guidance, fix issues found along the way, and deliver a reviewable pull request.'
---

# Execute Task

Plan the change, get it approved, then run it the same way every time. **Plan** decides what will be
built; **Execution** builds it and hands the user a pull request to review.

## Dependencies

- `pre-production` — the target-contract policy for every repository and its data obligations.
- `code-simplify` — simplify the finished task's complete diff before delivery.
- `acceptance-gate` — judge the finished task's complete diff before local completion or the pull request leaves draft or merges, and each fix for a flag it raises.
- `generic-push` — keep each repository's publishing metadata independent during multi-repository changes.
- `merge-conflict` — bring in a conflicting base as soon as a push read-back shows it, and a moved one once at **Completion**.
- `subagent-selection` — the hand-up a worker without an agent tool uses for an independent step.
- `land-pr` — mark the finished pull request ready and drive its checks to green at **Completion**.
- `test-fixture` — the sweep over the task's tests at **Completion**.
- `security-audit` — **Building It Safely** while writing code that crosses a trust boundary, and
  its **Diff Review** of such a change at **Completion**.
- `rewrite-git-history` — one commit per material change before the pull request is sent for review.
- `edit-skill` — process the task's recorded guidance corrections at **Completion**.
- `list-prs` — the task's pull requests for the ready-for-review message.

## One Run Per Task

- Invoke this skill once when a task is authorized to change files, before its implementation
  recommendation, delegated edits, or first edit. A run stays active until
  the task's outcome is verified complete or the user explicitly stops or hands it off. **Work You
  Have Already Named** retains outstanding items and their next actions through reports, gates and
  interruptions. Nothing in the task re-enters the skill; the run simply has not ended.
- A skill that lists this one as a dependency invokes it once, and the skills this one invokes
  never invoke it back: every skill under **Dependencies** is a leaf of this run. A second
  invocation while one is active does nothing more than continue the active run.
- A skill that presents its own plan, such as a doctor's remediation plan, presents it through
  **Plan** below.
- A read-only task — a question answered from the code, a listing, a report with no edit — does
  not run this skill; a task whose edits sub-agents make is not read-only for the agent that
  delegated them. A read-only turn does not close an open run either: a run still holding named
  work stays active through such a turn, and that turn moves its items.

## Plan

Every task that changes files starts here, and so does every follow-up that arrives while one runs.

### When A Plan Is Needed

- **Every change gets a plan put to the user before its first edit, except a trivial one.** A
  trivial change has no design choice in it: a typo, a one-line fix, a rename the user named. It
  goes straight to **Execution**.
- Work the approved plan already covers takes no new plan: an encountered issue, a gate's or a
  review's flag, a failing check. Neither does a guidance correction, which `edit-skill` records
  during the run and processes at **Completion**. A guidance edit the user asks for directly is a
  change like any other, planned unless trivial.

### What The Plan Holds

- At most five numbered steps, each one bounded action with its wall-clock estimate, then the
  total and what the user does afterwards, then every decision the plan needs. Keep it under 200
  words while `i-have-adhd` is active, and send any detail a caller requires — a gated plan, a
  ledger — as a file, as the global rules' **User-Facing Output** says, instead of restating it.
- **An estimate is the executing agent's own wall-clock, never the effort the same work would
  take a person.** Reading, searching and editing take an agent minutes whatever the file count;
  the time comes from what the run waits on — test and build durations, CI, gate and review
  passes, background agents — so a step's figure is those durations, observed for comparable runs
  where they exist, plus its edits. List what the plan needs from the user — an approval, a merge,
  a manual action — separately, with its time.
- Schedule steps by `subagent-selection`'s **Dispatch**: coupled work stays sequential, and
  independent scopes with separate owners, files and resources overlap once their inputs are
  settled. Estimate the elapsed time with that overlap.
- **Settle ownership before the plan is final.** For a plan that introduces a subsystem, runtime
  boundary, or independent consumer, apply `code-simplify`'s ownership analysis to the proposed
  shape and the analogous implementations already in the repository, with one read-only subagent
  inventorying them when the comparison spans subsystems. The plan states where common behavior
  will live and which policy or wiring stays consumer-specific; it never starts from a parallel
  structure and leaves ownership for implementation.
- Send this shape, leaving out the decision block when there is none:

```markdown
**Approve this plan?** Reply "go", or tell me what to change.

1. <step> (~<n> min)
2. <step> (~<n> min)

**Total: ~<n> min.** Then <what the user does next, with its time>.

**Decision needed:**
1. **<subject>** — <question>? I recommend <option>, because <reason>. Step <n> depends on this answer.
```

### Approval

- Only an explicit user response approves a plan. A timeout, inactivity, a missing response, a tool
  result, a mode change or a system notice never does. When control returns without one, send the
  unchanged plan again in ordinary chat and begin nothing.
- An interruption continues the same plan. Never replace or silently revise an unapproved plan;
  fold the user's amendments in and present the complete revised plan again.
- Approval authorizes ordinary implementation and verification, never a merge, deployment,
  publication or release the plan happens to list; **Task Authorization** says what does.
- **Offering the next step as a choice is a stop wearing a question mark.** "Say the word and I will
  start the next group" hands back an instruction the user gave once. Ask only for a decision that
  is genuinely the user's, and put it in the question rather than in the plan's continuation.

### Follow-Ups

A follow-up is planned on its own, and only the work it changes waits for it.

- **One that touches nothing in flight** — other files, another outcome — leaves the running work
  going. It gets its own plan, or none when trivial, and runs beside that work once approved, under
  `subagent-selection`'s **Dispatch**. Send:

```markdown
**Running work keeps going:** <step in flight> doesn't touch <what the follow-up changes>.

**Plan for the follow-up. Approve?**
1. <step> (~<n> min)

<No decisions needed. | **Decision needed:** …>
```

- **One that changes what is being built** pauses only the work it affects. Write that work and its
  next step down under **Work You Have Already Named**, put the amended plan in the full shape
  above, and resume it on approval. Unaffected work keeps running while the user decides.
- A follow-up on a pull request already sent for review converts it back to draft before its first
  push, as the GitHub rule says, and its **Completion** folds each change into the history under
  `rewrite-git-history` rather than rebuilding it.

## Execution

Execution starts once the plan is approved, or straight away for a trivial change.

### Task Authorization

- Carry the user's authorization for the task through its ordinary implementation, verification,
  scoped external changes, retries, recovery, and cleanup. A follow-up, interruption, failed attempt,
  or context reset does not require the user to approve those sub-steps again.
- Treat merge, deployment, publication, and release as separate outcomes outside the ordinary
  scoped external changes above. "Implement this plan" is not an explicit instruction for any of
  those outcomes, even when the plan names the action and target. Before acting, identify the
  user's separate explicit instruction for that action and target or applicable guidance or an
  invoked skill that expressly authorizes it; otherwise complete the reviewable work and leave
  that outcome pending.
- Ask only for a decision that materially changes the authorized target, recipient, or outcome, or
  for an action-time confirmation a platform actually requires. Make that question specific to the
  new decision or action; never ask the user to reconfirm the task or say "continue" to resume it.
- **A question the guidance already answers is not the user's to answer.** Before a question goes
  out, and again each time one carried from an earlier turn, a note or a summary would be put
  again, read the rules and the repository's project guidance governing its subject; where they
  decide it, act and report what was done. The class: whether to delete, reset or recreate a local
  resource, such as a cache volume filling the disk or a database stuck on a migration the branch
  has since regenerated, and whether to reset or reopen local records to reach a state, such as a
  test account back at its first sign-in, both of which the global rules give the agent; what a
  data change owes records already stored, which project guidance says; which of two
  implementation details to use where a rule picks one; and what configuration exists or how it is
  scoped, which is read where it lives. A permission denial leaves the decision where it was, as
  **Environment Refusals** says.
- Apply the global rules' **Task execution and authorization** decision boundary before choosing
  an encountered issue's remedy, including one proposed by a worker or reviewer. An ambiguous
  instruction has no approved interpretation: name both concrete outcomes and build on the
  user's answer, quoting their words in a delegated brief. This decision wait holds only the
  dependent remedy, never the remaining authorized work.
- An implementation constraint is not a new approval boundary. Exhaust authorized ways to
  complete a sub-step yourself. Do not mistake an action-time confirmation for a mandatory user
  hand-off: after the user confirms the specific pending action, perform it yourself. Hand off only
  when the platform requires the user's own interaction. Never request a secret through chat.
- After a required confirmation, continue the remaining authorized work without another general
  approval request. A refused or unanswered confirmation blocks only the action it governs, as
  **Work You Have Already Named** says of every wait.

### Browser Access

- Use the user's `@Chrome` browser for browser work unless the user names another browser. When
  the user explicitly selects an existing tab or window, use only that authorized surface;
  otherwise create a new task-owned tab before any page read or action. Retain its handle or stable
  ID and keep actions bound to it under the global rules' tab-ownership procedure. Keep a new tab
  in the background when supported; tab isolation does not require another profile or account.
- When attaching a browser CLI to an existing browser, create and select the task tab first, or
  select the existing surface the user explicitly authorized, before commands that navigate or
  inspect the current page. A named CLI session alone does not establish tab ownership.
- For the default Chrome route, if connected tab control is unavailable, use regular Chrome with
  the same surface-selection requirement above. It may come to the foreground. Continue through an
  appropriate API or CLI when that is more direct. Report a browser-specific blocker only when the
  authorized browser's normal recovery paths cannot complete the required interaction.

### Environment Refusals

- **An environment refusal is a route to find, not a blocker to report.** A repository missing from
  the session is attached or cloned as a writable checkout; a host the environment refuses is reached
  through a path it does serve, and a tool that took the refused path is fixed to take the served
  one. Report a blocker only once every served path has been tried and has failed. A command a
  permission check refuses falls under the next bullet instead, even when it targets a host.
- **A permission check is not a route to find: what it refuses is not attempted again, and the
  decision never becomes the user's.** Use the owner's own routine tool from the start — a package
  manager's cache-clean rather than a raw delete of its cache directory — because that is the
  ordinary way to do the job, not a workaround. Once a permission boundary refuses an action,
  whether a rule the user set or an automated safety check, that outcome is not attempted again by
  any other command, tool or wording, and every other piece of work carries on. Report the refusal
  once, plainly, as a permission the user can grant: what was refused, and that it runs once
  allowed — "The permission check blocked `<command>`; it runs once you allow it, and everything
  else is done." Whether the action is wanted was settled by the guidance before the check ran, so
  the report never asks it or offers options: "Delete X? Yes or no" is the defect.

### Product Constraints

`pre-production` is active in every change task. Read it completely, explicitly invoke it, and
announce the invocation before the first edit. Listing it as a dependency is not an invocation.
Read the repository's product state from its project guidance before choosing how to change a
contract or stored value.

Before recommending an implementation or delegating its edits, trace the requested behavior from
the caller to its owner and inspect that owner's existing capabilities. Apply the guidance and
analogous implementations below to that choice, not only to the later edit.

Before an edit that crosses a trust boundary `security-audit` names, invoke it and apply its
**While Writing Code**.

Before each edit, read the shared and repository rules governing every surface it reaches — its
language, framework and package, and the kind of thing it changes, such as a form, a query, a test
or interface copy — and nearby analogous files. Where those files disagree, the one departing from
the rest, or from the mechanism that owns the concern, is an encountered issue to fix, never the
pattern to copy. That holds at every point new instructions arrive, not only at the task's start:
a correction, a fix step or a resumed brief that sends the work to a surface whose rules the run has
not read has them read before it is acted on, and having worked in the same language or package
earlier in the run is not having read them. Match the analogous files' code grouping and spacing in
every new or substantially edited file; inspect the complete result beside those siblings before
delivery. A formatter passing is not a substitute for that comparison.

### Encountered Issues

Apply `pre-production`'s encountered-issues policy while making the change. The rules below govern
how those issues are handled.

- **Classify validation failures before expanding the task.** When existing run evidence or a
  reproduction through the native check on the default branch establishes the same failure under
  comparable inputs, and the change neither introduces nor worsens it, report the check and that
  evidence as a baseline failure. Continue the requested work and its relevant validation; do not
  repair, rerun, investigate further, ask a product question, or record a deferral for that failure
  merely because validation encountered it. Keep the failed result visible and never report the
  whole check as passing. This exclusion does not cover a defect the user assigned, a failure of
  the behavior the task must establish, or a confirmed finding independently established by a
  review or source inspection apart from diagnosis of the excluded check. Do not reopen an
  exclusion by relabeling that same failure as a review or source finding. Assigned defects and
  independent findings remain fix responsibilities even when older code caused them.
  Missing comparison evidence is not a baseline exclusion; inspect the failure at its native owner
  before choosing its disposition. Pass established exclusions and their evidence to every later
  validation or merge gate.

- **A confirmed defect the work turns up, or a finding against the task's changed design, is fixed
  in the change in flight, in a shape the standing guidance allows as the next bullet says, and
  offering it to the user is not a disposition.** "Want this handled, or shall I leave it?" reads as
  diligence and is the failure this section exists to prevent: it spends a turn to obtain permission
  for something already required, and a no leaves a known defect in the tree with the agent's name
  on the decision. The question that is genuinely the user's is about a **product change** — what a
  feature does or presents, what a record keeps, who a surface serves, a contract a consumer outside the user's
  control speaks — never whether an encountered issue gets fixed.
- **An instruction one agent passes another — a brief, a correction, a review finding, a gate's fix
  step, a note or summary an earlier turn left for a later one — is checked against the standing
  guidance before it is sent and again before it is acted on**, because it never outranks that
  guidance, as the global rules' **Task execution and authorization** says. Each side reads every
  item against the rules and skills governing the surface it changes — the language, framework,
  copy and testing rules, and the skills the worker runs — opening them at that moment where it has
  not read them yet. The class is any item asking for what a rule rules out: a review finding
  asking for the catch-all exception handler the language rule bans, a brief telling a worker to
  skip a check a skill requires before a push, a correction asking for copy the copy rules forbid,
  one asking for a boat-rental waiver to arrive filled in from the renter's last booking when the
  forms rule says a form someone attests to starts empty.
  - **The agent writing it** rewrites an item a rule forbids into a shape the rule allows, or drops
    it where none exists. One the user asked for in their own words goes out with those words quoted
    and the rule they set aside named; a rule the agent thinks is wrong is put to the user, never
    overridden by an instruction.
  - **The agent receiving it** carries out every other item. For the forbidden one, it fixes the
    defect the item names in a shape the rule allows, where one exists, and leaves only the
    forbidden shape undone. It names that item and the rule it breaks to the sender, through the
    next hand-up or report, and neither implements nor drops it silently. Only the user's own
    words, quoted, with the rule they set aside named, override it.
- When local validation fails before exercising the changed behavior, trace the failing setup
  operation under `code-simplify`'s **Trace Changed Flows** before choosing a remedy or reporting
  a limitation. Include that inherited operation in the affected-repository map, compare its
  prerequisites with applicable parallel implementations, and repair its repository-owned inputs
  at their owner. A caller-supplied workaround is not verification of the repaired native route;
  rerun that route before completion. Preserve a required prerequisite whose concrete contract
  differs, and apply **Environment Refusals** and **Task Authorization** to an actual external or
  permission boundary.
- **An encountered defect that remains in the task is fixed where the work is in flight.** Its
  origin changes neither that responsibility nor its priority. Read history when it helps write
  the fix, rather than asking the user whether it predates the change. Say what was fixed and why
  it was in the path of the work.
- What puts a **new** issue in that path is an act the work performed: a file it opened, a command
  it ran, a check it read, a review it received, and anything it looked at — a screenshot or
  recording, its own or a worker's, a walk through the product, a log, a report. A defect seen there
  is found exactly as a failing test is. How far the fix then reaches is a different question, and
  `pre-production`'s **Scope Follows The Defect, Not The Request** answers it.
- Never reject a fix solely because it is described as high risk. Assess its expected net effect,
  concrete failure modes, and available validation instead of treating the label as a stop rule.
- Apply `pre-production`'s scope decision before treating a review observation as mandatory work.
  Fix confirmed defects and findings against the changed design. A non-defect improvement earns
  inclusion only as a bounded local refactor whose complete consumer updates fit one focused pass
  and produce an overall net gain. A review naming it does not turn independent cleanup into a
  defect or authorize recursive expansion.
- Delete every piece of confirmed dead code encountered during implementation, even when it sits
  outside the files or packages already being changed, within `pre-production`'s size budget.
  Confirm that no live application or library consumer, public export, or external contract still
  depends on it, judged where the change will land as `code-simplify`'s rubric says; remove tests
  that exist only to exercise the dead code; and validate the affected behavior. This requirement
  does not turn implementation into a proactive dead-code audit of the whole repository.
- Use the repository's relevant tests as the regression guardrail; do not preserve a defect solely
  because an existing test asserts the old behavior. When coverage is absent or insufficient, use
  the strongest available validation and account explicitly for the uncovered behavior.
- One focused pass means the correction needs no separate research or design phase and is not
  expected to require multiple implementation iterations.
- Apply an owned API, protobuf, schema, payload, or stored-shape change selected by
  `pre-production` without a second approval; update every consumer the user controls, in
  whichever repository it lives, plus every generated artifact and required migration for the
  target contract.
- Apply **Task Authorization** to encountered corrections. Ask only when the correction is a product
  change as the first bullet defines it, changes security or disclosure posture, reaches a
  repository, environment, or external recipient the task did not authorize, or a platform requires
  action-time confirmation. Another file, component, or package in the same repository is never a
  new target, and neither is a repository the user owns that consumes a contract the change breaks:
  it is delivered under **Multi-Repository Delivery**. The obligation to fix a bug or returned
  finding remains; apply **Task Authorization** to its remedy rather than treating the finding
  as permission for an unsettled product choice. Continue independent authorized work while that
  choice waits, and never ask whether the defect should be ignored.
- When asking, state the trigger, impact, expected work, recommendation, and concrete choices.

### CI Gates And Deliberate Breaks

Some required checks exist to detect deliberate changes: contract compatibility, schema
compatibility, generated-output drift.

- Such a gate going red is an accepted, reported outcome of an intentional break, never a reason
  to reshape the change.
- Never weaken the gate to recover green: no ignore lists, no exception entries, no reserved
  placeholders faking compatibility.
- Report it instead. State in the pull request that the break is deliberate and list exactly what
  the gate reported, so a reviewer can confirm nothing unintended is in the diff.
- Do not let a green run drive design. Choosing a wider or additive shape so that a gate stays
  green is the same defect as suppressing the gate.

### Ongoing Simplification

Read and invoke `code-simplify` once across the finished task's complete diff, under
**Completion**, never per push.

Own each coherent feature through integration: the primary agent settles dependencies, product
decisions and the combined result. Simplify a feature as it is built; the final `code-simplify` pass
still covers the complete diff. Assign a worker an independently owned scope with a concrete
boundary and return condition, not an arbitrary slice of the primary agent's feature. Keep admitted
cleanup with its feature; an independently selected cleanup follows its own stated scope and
ownership. When cleanup crosses an interface or repository, bring its producer and consumers to a
coordinated checkpoint, verify compatibility at both ends, and keep the cleanup named until
that check passes. Neither a slower dependency nor unrelated work drops an encountered issue from
the task.

- Every pass covers three things, never the diff hunks alone: the **changes** themselves, the
  **similar code** they resemble, and the **sibling modules** around them.
  - **Changes**: the full contents of every file the task has touched so far, not only the lines
    edited in the current batch.
  - **Similar code**: every other place in the repository already expressing the same concept,
    shape, or operation as the changed code — a near-duplicate helper, a parallel implementation,
    a second representation of one value. Search by concept and by key operation, not by filename;
    a sibling-only read cannot find the canonical implementation another package owns. Where the
    change and the code it resembles should be one thing, make them one thing, within
    `pre-production`'s size budget.
  - **Sibling modules**: the other modules in each changed file's package, which is where a
    misplaced piece of logic and its rightful home become visible together.
- When a repair changes another file, inspect its complete contents and relevant owners to verify
  that repair and its necessary consumer updates. This expands validation, not permission for a
  new cleanup frontier; use `pre-production`'s scope decision before adding another correction.
- Resolve the final pass the same way, from the complete diff. Check the combined scope against
  the requested outcome, including all incidental changes; individually useful edits can add up
  to a disproportionate change.
- Apply complete defect repairs and bounded local simplifications under `pre-production`; ask
  only about a genuine decision **Encountered Issues** reserves for the user.

### Pre-Push Gate

Every push goes out once the pre-push checks below pass, on a draft and on a pull request ready for
review alike; nothing holds committed work on one machine. `code-simplify` and `acceptance-gate`'s
diff question do not run per push: they run once over the finished task's complete diff, under
**Completion**. A fix pushed for a flag a gate or review raised gets one fresh `acceptance-gate`
run over that fix's increment, read with the whole branch diff as its originating diff, as
`acceptance-gate`'s **Bounds** require; that fresh verdict is what other skills mean by an
increment's **Pre-Push Gate** verdict.

Read the shared testing rule before planning test runs or briefing an implementation worker.
Its **Verification Cadence** governs tests, builds, browser walkthroughs and reviews, including
pre-push checks. Deferred feature verification does not hold an intermediate push and remains
required afterward. Run the relevant batch after the feature is complete, then the required final
checks before delivery; retain evidence that the change has not invalidated.

- **Required checks use CI’s commands and scope, at the verification checkpoints above.** Read
  the workflow files that trigger on a pull request and run every checking job that can run
  locally — lint, format, type checks, build, tests, generated-output drift, docs or coverage
  checks — with the job's own command and scope, plus any check a skill in use requires. Do not
  restart the batch for each push; retain results whose code and inputs remain unchanged. Project
  guidance that lists those commands is a shortcut to the workflows, never a
  substitute; where the two disagree, the workflow is right. A job that needs a hosted service or a
  running stack, or is too slow to run before every push, joins the slow verification below and is
  named in the report.
- **A local variant of a CI check is not that check**, and each of these passes locally and fails
  in CI: lint or type checks scoped to the changed files, where CI's whole-tree run finds an import
  another change left unused in a file the branch never touched; a formatter or linter in write
  mode, which rewrites what CI's check mode reports; a tool at a version or with a config other than
  the one CI resolves; a job left out because the diff looks unrelated to it, such as a
  generated-output drift check or a whole-tree check that every shared component has a docs page.

Before each push, list the exact adjacent line pairs where setup, a guard, transformation, side effect,
or return meets the next phase without the blank line required by the global code-layout rule.
Fix every listed boundary in the lines the change writes or edits, and elsewhere in the changed files
within `pre-production`'s incidental size budget, as the global code-layout rule says; an unrelated
bug or a passing formatter does not satisfy this spacing check.

- **Commit each small coherent step and push it as soon as its checks pass**, and at least every
  five minutes of work — a function and its callers updated, a test brought to pass, one finding
  fixed — never at the end of a unit or task. A push is what lets the user review and test the work, and the only copy that
  outlives the machine: a recycled container or an ended session takes every commit and edit no
  remote holds.
- **Nothing outside the change holds a push or becomes a question about pushing.** A dependency
  still in review in another repository, an unreleased package version, a sibling pull request not
  yet merged, CI expected to stay red until one of those lands: the branch consumes the
  dependency's pull-request branch, or its default branch once merged — in the manifest, the
  lockfile and any workflow checkout, as the global rules' version-reference bullet allows while
  developing — or builds on a same-repository sibling's branch as the GitHub rule's branch bullets
  set out, and pushes. Which branch it consumes, and a red check that dependency explains, are
  reported in user chat rather than waited on, never in the pull-request description; switching
  back to the released version is named work for when the dependency merges.
- **No edit sits uncommitted through a long wait outside the checks.** Before the slow verification
  below, a background worker, CI on the pushed head, or a question to the user, bring the work to a
  coherent step, commit it, and push it; the checks' own runs are part of the push, not such a wait.
- **Delegated edits run at this cadence.** A brief handing a worker edits states it, names the
  branch the worker pushes to — the branch of the pull request the work continues, under **Pull
  Requests** — and names the exact files to change, under `subagent-selection`'s **Dispatch**. The
  worker pushes each step once its checks pass and reports the branch and head. The delegating
  agent, which holds the intent statement, reads that head under **Reported Outcomes** and, once
  the worker's task is finished, runs one `code-simplify` pass and one `acceptance-gate` diff
  question over that task's diff, returning what they flag as fix steps for the next worker. The worker ends with nothing uncommitted and
  nothing unpushed, never amends or rebases a pushed commit, and its report names the branch and
  head.
- **Pull requests stay draft while the work runs**, so these pushes start no test jobs, as the
  GitHub rule's **Workflows** section sets up; the tests run once, when **Completion** takes the
  pull request out of draft. A ready pull request the task resumes changing goes back to draft
  first, as the GitHub rule's **Branches and Pull Requests** says.
- **The order is change, checks, push, then the slow verification**: a browser walkthrough, a full
  or end-to-end suite, a run against a service without the change, root-causing a failure seen
  along the way — anything slow or needing a running stack. What it finds goes out as fix pushes, each once its checks pass.
- **Pushed is not done**: the change is reported done only once that verification has passed.

### Reported Outcomes

An outcome is what its source of truth shows, never what an action or a worker said about it.

- **After any action that changes shared state, read the resulting state before reporting it or
  starting the next item.** A push, merge, deployment, migration, or refresh reports that it ran,
  not the state it left, so read that state where it lives. After a push, that is the pull request
  on the pushed head, or, before one exists, the remote branch head: its mergeable state and the
  checks that run for its state starting — a draft starts no test jobs — since the base can move
  while the push runs.
- **Whatever that read shows wrong is the next thing done**, ahead of every queued item, and is
  never carried to "the next push" or bundled behind other work. A conflict is brought in
  through `merge-conflict`, delivered under the **Pre-Push Gate**, and read back. A base that only
  moved, with no conflict, is brought in once, at **Completion**, before the final acceptance.
- **A delegated worker's report of an outcome is a claim, never evidence.** Before relaying it or
  building on it, check it at its source: "tests pass" against the run or the CI result on that
  commit, "pushed" or "exists" against the branch, "merged" or "refreshed" against the default
  branch or the installed copy, "deployed" or "healthy" against the host, "fixed" by reproducing it
  or reading the evidence, "the screenshot shows it" by looking at the image, "no references
  remain" by searching. A claim the check contradicts is the next thing done, ahead of queued
  work: sent back to the worker with what the read showed, or fixed here.
- **A deferral inside a report — "I'll do X next" — is named work of this run** under **Work You
  Have Already Named**, tracked until done; the report does not close it.
- **A status sent to the user states what was just read and where**, never what was reported or
  expected: conflicted, failing, running, or passing, on the head or target named. "Done" or
  "ready" is written only when that read says so, and a file sent with it is checked first as the
  global rules' **User-Facing Output** requires.

### Pull Requests

The GitHub rule's **Branches and Pull Requests** owns pull-request selection: source work defaults
to this session's pull request, while agent configuration follows its shared batching route.
Apply that ownership decision before preserving a checked-out branch or updating an existing pull
request. A guidance change never rides the source branch in flight. Verify selected pull requests
remotely, and leave another session's branch and pull request untouched unless the selected route
explicitly directs continuing it.

### Multi-Repository Delivery

When one change spans multiple repositories, treat each repository as an independent delivery
context, with **Pull Requests** applying inside each of them.

- Invoke `generic-push` separately for each repository before committing or publishing.
- Write every branch name, commit message, pull-request title, pull-request description, review
  comment, code comment, and repository-local report solely from that repository's perspective.
- Do not name, link, describe, or explain another involved repository, its branch, pull request,
  implementation, or coordination context in those artifacts.
- Keep cross-repository coordination and combined status reporting in user chat.

### Each Repository Speaks Only Its Own Vocabulary

The delivery rule above governs the artifacts around a change. This one governs what goes **inside**
it, and it binds in every repository the run touches whether or not that repository's own rules say
so — a repository with no independence rule of its own is the one most likely to be given another's
words.

**Never write another repository's nouns into this one.** Its product name, its services, its
skills, its tables and columns, its record types, its routes, its identifiers, the words its
business speaks: all of them stay where they are. That holds in source, tests, fixtures, sample
data, error messages, comments, and documentation alike, and it holds hardest in a library or a
tool, where every reader is a different consumer who has never heard of the repository the author
happened to come from.

**An example is where this fails, because an example needs a name and the author has one to hand.**
Documenting a folder layout, a config key, a path shape, or a call, the concrete thing the author
just saw is the nearest name and the worst one: it reads as this tool's own vocabulary to everyone
after them, and it goes stale the moment that other repository renames it. Invent the name instead.
An example naming a real artifact of another repository is the defect, however accurate it is.

Name things for the shape being demonstrated, never for whichever caller prompted the work. A
consumer's needs are a legitimate reason to build something and never a reason to name it after
them. Describe the target repository's own contract and behavior to reviewers; keep
consumer-specific coordination in user chat, following the Multi-Repository Delivery rule above.

Where this run touched more than one repository, sweep for it before delivering: search each
repository for the distinctive nouns of the others it was worked on beside, and read what comes
back. A borrowed name is invisible to the author precisely because it was familiar.

### Work You Have Already Named

**Naming work as next is a commitment, and it stays this run's obligation across every later turn**
— including a turn whose own request changes no files, which would otherwise not run this skill at
all. The run that named the work owns it until it is done, and naming it is what keeps the run open
under **One Run Per Task**.

**A new request, an interruption, or a context summary cancels none of it**, and the work each one
displaces is named work whether or not a report named it: an approved plan short of its last entry,
commits a remote lacks, a checkout left mid-edit. The turn that serves the new request also moves
it — the user asking about something else is not the user withdrawing what they asked for before.

- **Write it down before anything else starts.** The displaced work goes into the session's task
  list, with its next step, before the first step of whatever displaced it.
- **An interruption pauses the step in flight; it never ends the run.** After a follow-up
  finishes, restore the displaced task as the in-progress item in the session's task list and
  execute its saved next step without waiting for "continue". A promise to resume is not that
  step. Completing
  its own delivery — including a guidance merge and refresh, a diagnostic answer, or a local
  environment repair — does not complete the surrounding task. Report that intermediate result
  while continuing. A held item keeps its saved next action; repair, resolution and waiting follow
  the global rules' **Tools and environments** boundary. End only when the task is verified
  complete or the user explicitly stops or hands it off.
  "Continue", or anything meaning it, resumes exactly the paused step and is never answered with
  nothing.
- **A context summary's pending list is this run's named work**, not background. The first turn
  after it moves the oldest item as well as whatever the summary's next step names. A constraint it
  carries, such as "ask before X", is an earlier turn's instruction, checked under **Encountered
  Issues** before it is obeyed.
- **Commits a remote lacks are undelivered work**; their next step is the pre-push checks and the
  push. A hook or status line counting unpushed commits whose checks pass reports a push owed now,
  not something to explain.

**The failure is a report, not a refusal.** It reads as diligence: the item appears under "still to
do", the turn ends, the next message arrives, and the item appears again, unchanged, in the next
report. Nothing was declined and nothing was done, and each repetition makes the next one easier,
because the item now looks like a standing note rather than work somebody is waiting for.

So the test is the item's own line. Before a report goes out, compare each outstanding item against
the line the last report carried for it. **A line that has not changed means the item is finished in
this turn, before the report is sent** — not moved a little, and not dropped from the list, which
is the same failure with the evidence removed.

Each item's line records its current disposition:

- it is done;
- a named gate holds its dependent action — including an unanswered question or missing
  authorization — with its evidence, saved next action and live repair, resolution or wait route;
- it is no longer work, because the user withdrew it or a later request superseded it, said with
  that reason.

A held item remains outstanding; naming its gate or reporting it does not end the run. Withdrawal
or supersession removes only the work the user's instruction actually cancels.

**A wait blocks only the work that depends on what is awaited.** While one item waits on something
outside the run's hands — a background agent, CI, a review, a build, the user's answer to one
question or confirmation — start the authorized, already-named work that neither needs the awaited
result nor touches the files or resources the awaited work is changing. Each item held for the wait
names what it uses that only the awaited result will supply, and one with nothing to name starts
now: coming later in the plan, belonging to the same feature, or consuming a shape already agreed
with the awaited work, such as a planned contract, is not such a thing, so build against that shape.
When the awaited work is a building worker, another edit starts only in an independently owned
scope with separate files and resources, under `subagent-selection`'s **Dispatch**; otherwise do
read-only verification, review or question preparation while it runs.
A status report is not a stopping point. When every remaining item depends on an awaited result,
apply the global rules' **Tools and environments** pending-result boundary: keep the available
wait or event route active and resume the saved next action when it resolves. An unresolved user
choice holds its dependent remedy; it does not close the run or cancel independent work. A guidance
correction is recorded and the run carries on; it is processed at **Completion**, never a reason to
end or pause the surrounding task. Report a blocker only on that boundary's concrete evidence.

### Completion

Run this checkpoint before reporting a change complete, including a local-only result with no
pull request. In that case, source-stream steps 1–3 and step 5's verification review the complete
task diff and its validation prerequisites, and the history, the message and `land-pr` apply only
when a pull request exists. A failed local setup
operation remains encountered work under **Encountered Issues**, not an unverified-completion caveat. The independent gate
receives its affected-repository map and comparison evidence along with the diff.

Before the final delivery steps below, select the applicable verification route under the shared
testing rule's **Environments** section, then verify the requested behavior on the change's branch
within the authorized scope, including reachable dependency branches. When a requested flow failed,
repair and push the fix, exercise that branch through the applicable route, and repeat the complete
failed flow until its requested outcome is verified. A narrower health check or passing component
test cannot replace that flow.
Missing merge approval holds merging, never this branch verification; check the available branch
route before declaring a gate. Merge is delivery after verification, never its prerequisite.

Then finish each pull request the task changed, once, with its work finished. Two streams run
side by side from here: the guidance stream and the source stream.

- **Guidance stream.** Hand the task's recorded `guidance_correction` entries to `edit-skill`'s
  **Ledger Processing**, on its own agent-configuration branch, delegated so it never waits on the
  source stream. A task with none has no guidance stream.
- **Source stream**, in this order for each source pull request; an agent-configuration pull
  request belongs to the guidance stream:

1. Run `code-simplify` across the pull request's complete diff, under `pre-production`'s size
   budget, and push its simplifications through the **Pre-Push Gate**.
2. Run `test-fixture`'s **Sweep** over the tests the task added or changed and, when the diff
   crosses a trust boundary `security-audit` names, run `security-audit`'s **Diff Review** at
   `medium`; push their fixes.
3. Bring in a base that moved since the branch was cut or last incorporated, through
   `merge-conflict`. Then put the complete diff to `acceptance-gate`'s final-acceptance question, or
   its diff question when no pull request exists, with the intent statement. Push the fix for each
   flag as its own increment and put it to the fresh gate that skill's **Bounds** require.
4. Shape the history with `rewrite-git-history`. The first time a pull request is sent for review,
   rebuild it into one commit per material change. Each later **Completion** of the same pull
   request, after a follow-up, folds every change into the commit it amends through that skill's
   fixup route, or adds a new commit for a new material change, and never rebuilds it again, so the
   commits the user already reviewed keep their shape. A rewrite whose tree proof shows an
   identical tree keeps the acceptance verdict.
5. Verify every requested outcome and every incidental fix, confirm tests and relevant validation
   cover each of them and every simplification, confirm intentional contract changes are reflected
   in the expected behavior, and confirm multi-repository delivery artifacts describe only their
   owning repository. Then build this pull request's ready-for-review message, in the shape below,
   from `list-prs` and what the run did.
6. Invoke `land-pr` with the accepted head, merge withheld unless **Task Authorization** finds that
   merge authorized, as its fix rule the **Pre-Push Gate** with each fix folded into its commit
   through `rewrite-git-history`'s fixup route, and step 5's message as its ready message. It marks
   the draft ready, which starts its test jobs once, sends that message before its checks finish,
   then reads the jobs back on the exact head and fixes each failure until they pass. When it
   returns, send one line with the result it read: the checks green on the head, or the gate that
   holds them.

When the task uses several independent final reviewers outside `code-review`, assign distinct
concerns across the complete result rather than asking each the same question. After a repair,
rescan the affected ownership area and consumers, retain valid evidence for unchanged areas, and
return only invalidated review scopes to their reviewers. `code-review` owns this assignment and
rescan within its own invocation.

The ready-for-review message takes exactly this shape, one message per pull request, leaving out
**Noticed, not changed** when nothing is over `pre-production`'s size budget:

```markdown
**Ready for review:** <pull request URL>

- **What landed:** <each requested outcome, one clause each>
- **History:** <n> commits (<subject> · <subject> · …)
- **Fixed on the way:** <each incidental fix, or none>
- **Noticed, not changed** (over the size budget):
  1. <item>
- **Still running:** <CI on the ready pull request (~<n> min) | the guidance fixes from this task (<n> correction(s), own pull request) | nothing>

**Next:** review the pull request; send follow-ups here, or `/merge-pr` when you're happy.
```

The run stays open until both streams finish: the source stream when `land-pr` returns, the guidance
stream when **Ledger Processing** reports its pull request merged or held for the user.

A workflow that already runs final acceptance runs step 3 as its own; one that already invokes
`land-pr` runs step 6 as its own.
