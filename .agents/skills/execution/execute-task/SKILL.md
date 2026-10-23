---
name: execute-task
description: "Always run this. Invoke once at the start of every task authorized to change files, before recommending an implementation, delegating edits, or editing — including one whose edits sub-agents make, and one that only begins changing files because work turned up a defect — and keep it active until verified completion or explicit user stop or handoff. It plans source and product changes first, except for trivial changes; canonical guidance changes skip the plan and, while another task is active, are pushed to a draft pull request, recorded, and delivered in bulk at its completion. It then applies the repository's product constraints, fixes the bugs the work encounters rather than reporting them, commits each small step and pushes it promptly once its checks pass, keeps session-created source work to one pull request per repository, finishes each pull request, once the whole task is done, with a review pass over everything not yet reviewed (test sweep, simplification, code review, acceptance) and a history rewrite before sending it for review, checks every outcome it reports at the source of truth, and delivers each repository independently. Never invoke it from inside a skill it runs."
short_description: 'Plan source and product changes for approval; validate canonical guidance changes through their delivery gates.'
---

# Execute Task

Plan source and product changes, get them approved, then run them the same way every time.
**Plan** decides what will be built; canonical guidance changes enter **Execution** directly and
are validated by their evidence, smoke-test, review, and acceptance gates.

## Dependencies

- `pre-production` — the target-contract policy for every repository and its data obligations.
- `run-site` — select browser verification applicability before proposing it in a plan or brief.
- `code-simplify` — the pass over each delegated worker's finished task, and the ownership analysis a plan settles.
- `review-pass` — review, simplify and fix the finished task's unreviewed changes before delivery.
- `acceptance-gate` — judge the finished task's complete diff before local completion, before the pull request is sent for review and before it merges, and each fix for a flag it raises.
- `generic-push` — keep each repository's publishing metadata independent during multi-repository changes.
- `merge-conflict` — bring in a conflicting base as soon as a push read-back shows it.
- `subagent-selection` — the hand-up a worker without an agent tool uses for an independent step.
- `merge-gate` — at **Completion**, when the merge is authorized, ready the pull request, drive its checks to green and merge it.
- `security-audit` — **Building It Safely** while writing code that crosses a trust boundary;
  `review-pass` runs its **Diff Review** of such a change at **Completion**.
- `rewrite-git-history` — one commit per material change before the pull request is sent for review.
- `process-ledger` — process the task's private ledger at **Completion**, including verified guidance corrections.
- `list-prs` — the task's pull requests for the ready-for-review message.
- `session-ledger` — keep the plan and its steps' status current as they change.

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

- **Every source or product change gets a plan put to the user before its first edit, except a
  trivial one.** A trivial change has no design choice in it: a typo, a one-line fix, a rename the
  user named. It goes straight to **Execution**. Canonical guidance changes under `.agents` do not
  wait for a plan or an output-format approval: their request or an encountered guidance gap starts
  the guidance-correction workflow, and their evidence, smoke-test, review, and acceptance gates
  verify it, on the timing `edit-skill`'s **Recording During A Task** sets for an active task,
  whether the user asked for the correction directly or the run noticed it.
- Work the approved plan already covers takes no new plan: an encountered issue, a gate's or a
  review's flag, a failing check, or a guidance correction discovered during the run. `edit-skill`
  records verified guidance corrections and `process-ledger` processes them at **Completion**.

### What The Plan Holds

- Select verification before recommending it, putting it in a plan, or delegating it. Read the
  shared testing rule's **Environments** section and invoke `run-site` to apply its **Principles**
  before selecting browser walkthroughs or rendered UI inspections, including when later review
  or **Completion** proposes additional verification.
- At most five numbered steps, each one bounded action with its wall-clock estimate, then the
  total and what the user does afterwards, then every decision the plan needs. Keep it under 200
  words while `i-have-adhd` is active, and send any detail a caller requires — a gated plan, a
  ledger — as a file, as the global rules' **User-Facing Output** says, instead of restating it.
- **An estimate is the executing agent's own wall-clock, never the effort the same work would
  take a person.** Build it from what the run does and waits on, never from how big the change
  feels, round each step to the nearest whole minute, never below 1, and list what the plan needs
  from the user — an approval, a merge, a manual action — separately, with its time, outside the
  total:
  - an edit step — read, edit, commit, push — is 2–3 minutes whatever the file count;
  - each run of a local check, test suite or build is its observed duration, counted once per run
    the plan makes;
  - an independent gate or review dispatch is 2–4 minutes, and each repair round after it about 3
    more; plan two or three rounds for a change other files restate or depend on, none for a
    trivial one;
  - a round of parallel readers or reviewers is about a minute, and a round of auditing reviewers
    over a tree is 5–10 minutes;
  - CI, a deployment or a merge with its follow-up is the observed duration of that job.
- Schedule steps by `subagent-selection`'s **Dispatch**: coupled work stays sequential, and
  independent scopes with separate owners, files and resources overlap once their inputs are
  settled. Estimate the elapsed time with that overlap, counting overlapping work once at the
  longest of the overlapping steps.
- **Settle ownership before the plan is final.** For a plan that introduces a subsystem, runtime
  boundary, or independent consumer, apply `code-simplify`'s ownership analysis to the proposed
  shape and the analogous implementations already in the repository, with one read-only subagent
  inventorying them when the comparison spans subsystems. Invoke `subagent-selection` at its standard
  capability level for that reader, launch the exact resolved identifier, and retain catalogue state,
  identifier, assignment state and host receipt with the plan evidence. The plan states where common
  behavior will live and which policy or wiring stays consumer-specific; it never starts from a parallel
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

### Priority

Record each active task's priority, status and saved next action through `session-ledger`. A
follow-up joins that record; arrival order does not give it priority. Keep the active higher-priority
work in hand unless the user explicitly reprioritizes it, evidence establishes greater urgency, or
that work completes. State and record the reason before switching, preserving the displaced step.

Pending source work — application or library code, as opposed to tests — ranks above test-only
work, whichever was requested or queued first. Test-only work is test cleanup, test refactors, suite
runtime or coverage work and a sweep's test fixes. Start or delegate it only while no source change
the task owes, in any repository, can proceed, and order the plan's steps and every worker's brief
the same way. Test updates a source change needs travel with that change, and running tests to
verify it is verification, not test work. A test-only item in flight when a source change can
proceed pauses at its next safe boundary.

Source work a deploy the user is waiting on needs ranks above simplification, review gates, test
work, guidance delivery and cleanup, whichever started or was queued first. A database revision to
restore or split so the branch deploys safely onto an environment that already ran an earlier
version is the common case. Start it as soon as the need is known; workers on the lower-ranked
activities pause at their next safe boundary with their work pushed and their next action saved, and
resume once the deploy-safety change is pushed and validated. Those later passes may still change
that code, provided what the deploy depends on stays the same and its owning tests prove it — for a
revision, its database outcome.

Restoring an authorized broken deployed operation takes priority over ordinary tests, review gates,
guidance delivery and cleanup. Pause those activities until the actual failed operation succeeds
on the fix branch in every affected environment; use only the reproduction, diagnosis and repairs
needed for that checkpoint, respecting any narrower user restriction. This pause includes ordinary
checks and task-owned workers already running, even on separate files or resources. Pause them at
the runner's next safe boundary, honoring its interruption and cleanup contract; preserve completed
evidence, frozen inputs and the saved next action. An already-started independent cohort is not an
exception permitting continued ordinary work. Deploy through the authorized branch route, then
resume required delivery checks after that live proof. A successful child task,
health response or merge does not establish it. After an authorized merge, repeat the operation
from the default-source deployment; if it fails, resume recovery and pause ordinary delivery work
again. This order grants no deployment or merge authority: **Task Authorization** still governs both. An invoked `incident` supplies its own
recovery, review and source-restoration procedure.

### Follow-Ups

A source or product follow-up is planned on its own. A canonical guidance correction follows **When A Plan Is Needed** and does not wait for approval; while a guidance batch is in flight it waits for the next batch, as `edit-skill`'s **Recording During A Task** says. **Priority** decides when other follow-ups run and whether affected work pauses now; none of the routes below makes arrival order a reason to preempt active recovery.

- **One that touches nothing in flight** — other files, another outcome — leaves the running work
  going. It gets its own plan, or none when trivial, and runs beside that work once approved when approval is required and
  **Priority** permits, under `subagent-selection`'s **Dispatch**. Send this template only for a
  follow-up that needs a plan:

```markdown
**Running work keeps going:** <step in flight> doesn't touch <what the follow-up changes>.

**Plan for the follow-up. Approve?**
1. <step> (~<n> min)

<No decisions needed. | **Decision needed:** …>
```

- **One that changes what is being built** — a source or product follow-up — records the affected
  work and its saved next step under **Work You Have Already Named**, then puts the amended plan in
  the full shape above.
  Pause affected work when **Priority** brings the amendment into execution; otherwise retain it
  for after the active work. Resume on approval when its priority permits. Unaffected work keeps
  running while the user decides.
- **One that narrows scope reaches the work already in flight, at once.** Message every running
  worker to stop the work the cut removes and has not yet done, keeping what it already finished,
  and record the cut in the intent statement every later gate and review receives. A finding in
  the cut work, a defect included, is answered as out of scope rather than fixed, unless this
  change introduced it.
- A follow-up on a pull request already sent for review pushes to the same draft, and its
  **Completion** folds each change into the history under `rewrite-git-history` rather than
  rebuilding it.

### Progress Record

- **The ledger holds the plan's current state, so nothing about progress depends on what the chat
  still remembers.** When a plan goes to the user, record it with `session-ledger` as a `plan`
  entry with its steps, estimates, overlaps and what it needs from the user. Work the user adds to
  an active task, with or without a plan of its own, becomes a step on that plan or a plan entry of
  its own, with its approval time, or the time the user added it when it has no plan, before the
  first edit or dispatch it authorizes; a harness task list, the chat or a summary is never where it
  first lives. Update it when the
  state changes, not when a report is due: approval, a step starting, finishing, blocking or being
  skipped, a follow-up's plan. A resumed session, a handoff and a progress view all read this
  record rather than reconstructing it.
- **A step estimated over 30 minutes is recorded with its parts**: bounded pieces of that step's
  work, each with its own estimate in whole minutes, at least 1, together adding up to the step's.
  Mark each part done as it finishes, so recorded progress moves while a long step runs. The plan
  the user approves keeps its numbered steps; the parts live in the record.

## Execution

Execution starts once a required plan is approved, or straight away for a trivial change or for a canonical guidance correction, whose timing `edit-skill`'s **Recording During A Task** sets.

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
  implementation details to use where a rule picks one; how to remove duplication the guidance
  treats as a defect — which repository or package owns shared behavior and which mechanism replaces
  parallel copies — which `pre-production` and `code-simplify` settle; and what configuration exists
  or how it is scoped, which is read where it lives. A permission denial leaves the decision where
  it was, as **Environment Refusals** says.
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

- Use the user's `@Chrome` browser for browser work unless the user names another browser.
  Apply the global rules' **Tools and environments** browser selection and stable-tab binding
  procedure before any page read or action, including when attaching a CLI to an existing browser.
  A named CLI session alone does not establish control of the selected tab.
- For the default Chrome route, if connected tab control is unavailable, use regular Chrome with
  the same global selection procedure. It may come to the foreground. Continue through an
  appropriate API or CLI when that is more direct. Report a browser-specific blocker only when the
  authorized browser's normal recovery paths cannot complete the required interaction.

### Environment Refusals

- **An environment refusal is a route to find, not a blocker to report.** A repository missing from
  the session is attached or cloned as a writable checkout; a host the environment refuses is reached
  through a path it does serve, and a tool that took the refused path is fixed to take the served
  one. Failed routes alone do not establish an external blocker: diagnose the refused contract
  at its owner and check whether owned code, configuration, credentials or lifecycle can satisfy
  it through the supported route. Report an external gate only with the concrete unavailable
  capability, evidence that supported recovery and authorized owned repairs are exhausted, and
  the saved next action when it returns. Repeating the same rejection is not that evidence.
  A command a permission check refuses falls under the next bullet instead, even when it targets
  a host; never bypass that boundary as recovery.
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

Resolve broad words in the context of the outcome the user named before selecting or inventorying
implementation targets. State the operational category covered by the request, then check each
candidate's actual role against it. A shared filename, label, directory or provider does not make
unrelated automation part of that scope. Expand to a required dependency or an explicitly broader
user instruction, never to everything a text search happens to return.

Before recommending an implementation or delegating its edits, trace the requested behavior from
the caller to its owner and inspect that owner's existing capabilities. Reconcile the complete
accepted target with the user's instructions, approved plan, repository guidance and observed
mechanism; record each settled outcome or constraint with its source and the evidence the proposed
implementation will need to satisfy it. Identify unresolved facts rather than silently replacing
them with an assumption. Compare the proposal against every part of this receipt before selecting
it: resolving the reported symptom or passing a component check cannot excuse violating another
settled requirement. A proposal that fails one is repaired before implementation; a genuinely
unresolved user decision follows **Task Authorization**. Apply the guidance and analogous
implementations below to that choice, not only to the later edit.

For an ownership or scope change, build `acceptance-gate`'s owned-boundary receipt before selecting
the implementation. Follow the runtime binding as well as the source owner: who executes the
operation, which resources it may reach, and which destinations must not receive its components,
data or authority. Carry this receipt into review and deployment verification; a component check
or an internally consistent configuration does not replace it.

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
  feature does or what information it presents, the steps of a workflow or a quantity the reader
  meets, a workaround for a constraint the user set, what a record keeps, who a surface serves, a
  contract a consumer outside the user's control speaks — never whether an encountered issue gets
  fixed.
- **An instruction one agent passes another — a brief, a correction, a review finding, a gate's fix
  step, a note or summary an earlier turn left for a later one — is checked against the standing
  guidance before it is sent and again before it is acted on**, because it never outranks that
  guidance, as the global rules' **Task execution and authorization** says. Each side reads every
  item against the rules and skills governing the surface it changes — the language, framework,
  copy and testing rules, and the skills the worker runs — opening them at that moment where it has
  not read them yet — and against the user's recorded decisions on that surface. An item calling a
  detail decided names who decided it and where; one the agent decided itself says so. Every brief
  for work that can change a surface the user has decided on, a simplification or review pass
  included, carries those decisions in the user's words, so the worker keeps them rather than
  undoing them; an item that would undo one goes to the user. The class is any item asking for what a rule rules out: a review finding
  asking for the catch-all exception handler the language rule bans, a brief telling a worker to
  skip a check a skill requires before a push, a correction asking for copy the copy rules forbid,
  one asking for a boat-rental waiver to arrive filled in from the renter's last booking when the
  forms rule says a form someone attests to starts empty. It also takes in an item adding a stop,
  a question or an approval the guidance does not call for, such as a brief telling a worker to
  stop and ask before adding the schema revision a migration skill puts its change in: the guidance
  settled that step, and the added gate hands the user a question with one answer.
  - **The agent writing it** rewrites an item a rule forbids into a shape the rule allows, or drops
    it where none exists. One the user asked for in their own words goes out with those words quoted
    and the rule they set aside named; a rule the agent thinks is wrong is put to the user, never
    overridden by an instruction.
  - **The agent receiving it** carries out every other item. For the forbidden one, it fixes the
    defect the item names in a shape the rule allows, where one exists, and leaves only the
    forbidden shape undone; for an added gate, it does the work the gate held. It names that item
    and the rule it breaks to the sender, through the next hand-up or report, and neither
    implements nor drops it silently. Only the user's own words, quoted, with the rule they set
    aside named, override it.
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

The final simplification runs once, inside `review-pass` at **Completion**, never per push.

Own each coherent feature through integration: the primary agent settles dependencies, product
decisions and the combined result. Simplify a feature as it is built; the final pass
still covers every change not yet reviewed. Assign a worker an independently owned scope with a concrete
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
    a sibling-only read cannot find the canonical implementation another package owns. A copy of
    the change's own mechanism is the change's scope under `pre-production`'s **Scope Follows The
    Defect**: give the mechanism one owner, move every consumer onto it and delete the copies.
    Other code the change resembles and should be one thing with is made one thing within
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
review alike; nothing holds committed work on one machine — not a gate, review or simplification
pass pending on it, an integration merge, or a plan that orders one first. The final `code-simplify` pass and `acceptance-gate`'s
diff question do not run per push: they run once over the finished task's unreviewed changes, inside
`review-pass` at **Completion**. A fix pushed for a flag a gate or review raised gets one fresh `acceptance-gate`
run over that fix's increment, read with the whole branch diff as its originating diff, as
`acceptance-gate`'s **Bounds** require; that fresh verdict is what other skills mean by an
increment's **Pre-Push Gate** verdict.

Read the shared testing rule before planning test runs or briefing an implementation worker.
Its **Verification Cadence** governs tests, builds, browser walkthroughs and reviews, including
pre-push checks. Deferred feature verification does not hold an intermediate push and remains
required afterward, and a suite still running holds none either: the testing rule's superseded-run
bullet says what happens to it. Run the relevant batch after the feature is complete, then the required final
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
  fixed — never at the end of a unit or task. Define coherence against `pre-production`'s
  complete target boundary, not the latest edited files: required consumer updates, superseded
  owners and declarations, generated contracts and retained-data migration are implementation,
  never later cleanup. An intermediate push may preserve ongoing work; it neither narrows the
  remaining obligation nor qualifies that feature for completion, review delivery or rollout.
  A push is what lets the user review and test the work, and the only copy that
  outlives the machine: a recycled container or an ended session takes every commit and edit no
  remote holds.
- **Nothing outside the change holds a push, a check or a walkthrough, or becomes a question about
  pushing or merging.** A dependency
  still in review in another repository, an unreleased package version, a sibling pull request not
  yet merged, CI expected to stay red until one of those lands: the branch consumes the
  dependency's pull-request branch, or its default branch once merged — in the manifest, the
  lockfile and any workflow checkout, as the global rules' version-reference bullet allows while
  developing — or builds on a same-repository sibling's branch as the GitHub rule's branch bullets
  set out, and pushes. Every build, test and walkthrough runs against that checked-in reference,
  never a local copy the manifest does not name. A consumer that cannot build until its dependency
  merges is a manifest still naming the default branch: point it at the pull-request branch, never
  ask for the dependency's merge or report the consumer blocked on it. Which branch it consumes,
  and a red check that dependency explains, are
  surfaced in user chat under the GitHub rule's independent publishing context rather than waited on; adopting
  its maintained delivery target is named work for when the dependency merges.
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
- **Pull requests stay draft until they merge**, so these pushes start no test jobs, as the
  GitHub rule's **Workflows** section sets up; the tests run once, when an authorized merge takes
  the pull request out of draft, as the GitHub rule's **Branches and Pull Requests** says. The
  local checks above are what stand between a push and that one hosted run.
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
  moved, with no conflict, is brought in once, by `review-pass` at **Completion**, before the final
  acceptance.
- **A delegated worker's report of an outcome is a claim, never evidence.** Before relaying it or
  building on it, check it at its source: "tests pass" against the run or the CI result on that
  commit, "pushed" or "exists" against the branch, "merged" or "refreshed" against the default
  branch or the installed copy, "deployed" or "healthy" against the host, "fixed" by reproducing it
  or reading the evidence, "the screenshot shows it" by looking at the image, "no references
  remain" by searching. A claim the check contradicts is the next thing done, ahead of queued
  work: sent back to the worker with what the read showed, or fixed here.
- **What a worker reports leaving alone is classified before it reaches the user.** Read each item
  against `pre-production`'s **Scope Follows The Defect, Not The Request** bullets: a defect, a
  parallel implementation or a shape a standing rule names goes back to the worker or is fixed
  here; only an item those bullets leave to the user, or one over the size budget, is reported, as
  what it is and never as a question whether to fix it.
- **A deferral inside a report — "I'll do X next" — is named work of this run** under **Work You
  Have Already Named**, tracked until done; the report does not close it.
- Before a milestone report, gate classification or final response, read the authorized outcome's
  current state and owning diagnostics, then reconcile every required step with the task record.
  A successful substep does not establish the parent outcome: resume its saved next action when
  that outcome remains unmet. Report intermediate results in commentary while an authorized
  remedy remains; a gate must meet **Environment Refusals** or **Task Authorization**, not merely
  repeat the last failed attempt.
- **A status sent to the user states what was just read and where**, never what was reported or
  expected: conflicted, failing, running, or passing, on the head or target named. "Done" or
  "ready" is written only when that read says so, and a file sent with it is checked first as the
  global rules' **User-Facing Output** requires.

### Pull Requests

The GitHub rule's **Branches and Pull Requests** owns pull-request selection: source work defaults
to this session's pull request, while agent configuration follows its shared batching route.
Apply that ownership decision before preserving a checked-out branch or updating an existing pull
request. A guidance change rides the source branch in flight only where that rule puts it there.
Verify selected pull requests remotely, and leave another session's branch and pull request
untouched unless the selected route explicitly directs continuing it.

### Multi-Repository Delivery

When one change spans multiple repositories, treat each repository as an independent delivery
context, with **Pull Requests** applying inside each of them.

- Invoke `generic-push` separately for each repository before committing or publishing.
- Write every branch name, commit message, pull-request title, pull-request description, review
  comment, code comment, and repository-local report solely from that repository's perspective.
- Apply the GitHub rule's independent publishing context to those artifacts, including dependency
  and hand-off notes; foreign references and coordination belong in user chat.
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

**Priority** decides which named work runs now; lower-priority work retains its saved step and
paused status until that boundary permits it. Recording a commitment never advances it ahead of
active recovery.

**Naming work as next is a commitment, and it stays this run's obligation across every later turn**
— including a turn whose own request changes no files, which would otherwise not run this skill at
all. The run that named the work owns it until it is done, and naming it is what keeps the run open
under **One Run Per Task**.

**A new request, an interruption, or a context summary cancels none of it**, and the work each one
displaces is named work whether or not a report named it: an approved plan short of its last entry,
commits a remote lacks, a checkout left mid-edit. The turn that serves the new request also moves
it — the user asking about something else is not the user withdrawing what they asked for before.

- **Write it down before anything else starts.** The displaced work is recorded as **Progress
  Record** says, with its next step, before the first step of whatever displaced it.
- **An interruption pauses the step in flight; it never ends the run.** After a follow-up
  finishes, mark the displaced work active again in the ledger and
  execute its saved next step without waiting for "continue". A promise to resume is not that
  step, and neither is a report that ends by naming what comes next: a turn that relays a worker's
  result or finishes a unit starts the next named step before it ends. Completing
  its own delivery — including a guidance merge and refresh, a diagnostic answer, or a local
  environment repair — does not complete the surrounding task. Report that intermediate result
  while continuing. A held item keeps its saved next action; repair, resolution and waiting follow
  the global rules' **Tools and environments** boundary. End only when the task is verified
  complete or the user explicitly stops or hands it off.
  "Continue", or anything meaning it, resumes exactly the paused step and is never answered with
  nothing.
- **A context summary's pending list is this run's named work**, not background, **and its state is
  read from the record, never from the summary.** After a compaction or handoff, and before
  starting, delegating or reporting any plan work, read each step's state from the plan entry in
  `session-ledger` and from the repository — merged commits, pushed heads — and let them overrule
  the summary: a step that the ledger entry or the repository shows done is not started again, and
  one the summary left out is still owed. The first turn then moves the oldest item still open as
  well as whatever the summary's next step names. A constraint it carries, such as "ask before X", is an earlier turn's instruction,
  checked under **Encountered Issues** before it is obeyed.
- **Commits a remote lacks are undelivered work**; their next step is the pre-push checks and the
  push. A hook or status line counting unpushed commits whose checks pass reports a push owed now,
  not something to explain.

**The failure is a report, not a refusal.** It reads as diligence: the item appears under "still to
do", the turn ends, the next message arrives, and the item appears again, unchanged, in the next
report. Nothing was declined and nothing was done, and each repetition makes the next one easier,
because the item now looks like a standing note rather than work somebody is waiting for.

So the test is the item's own line. Before a report goes out, compare each outstanding item against
the line the last report carried for it. A line that has not changed means the item is finished in
this turn, before the report is sent, when **Priority** permits it; otherwise record the active
higher-priority task that holds it and its saved next action. Moving it a little or dropping it
from the list does not satisfy that obligation.

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
question or confirmation — start the authorized, already-named work that **Priority** permits and that neither needs the
awaited result nor touches the files or resources the awaited work is changing. Each item held for the wait
names what it uses that only the awaited result will supply; absent that dependency or a hold under
**Priority**, it starts now: coming later in the plan, belonging to the same feature, or consuming a shape already agreed
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

First reconcile **Priority** against the actual deployed operation. Its unmet branch checkpoint
or failed default-source retry keeps this checkpoint paused; a completed diagnostic or implementation
substep does not start either delivery stream.

Run this checkpoint before reporting a change complete, including a local-only result with no
pull request. In that case, source-stream step 1 and step 3's verification review the complete
task diff and its validation prerequisites, and the history, the message and `merge-gate` apply only
when a pull request exists. A failed local setup
operation remains encountered work under **Encountered Issues**, not an unverified-completion caveat. The independent gate
receives its affected-repository map and comparison evidence along with the diff.

Before the final delivery steps below, select the applicable verification route under the shared
testing rule's **Environments** section, then verify the requested behavior on the change's branch
within the authorized scope, including reachable dependency branches. When a requested flow failed,
repair and push the fix, exercise that branch through the applicable route, and repeat the complete
failed flow until its requested outcome is verified. A narrower health check or passing component
test cannot replace that flow. When a deployment entrypoint consumes configuration, its verification
also proves that entrypoint receives the required settings and reads values in the deployed
representation; a local fixture using different settings or a different representation does not
establish the deployed route.
Trace the verification route to the code it actually loads before treating its result as proof or
proposing a merge: record the exact pull-request head, changed entrypoint and relevant event-specific
paths. Selecting an application's branch does not prove that the workflow, publisher or other
changed command ran from that branch. Use the authorized selected-branch route and verify that its
workflow identity and executed code agree; never assume a trusted workflow must execute default-
branch code. Where an actual security contract prevents live branch execution, first exercise an
equivalent native isolated branch route preserving authentication, permissions and input contracts,
and state precisely which live behavior remains unverified. Do not add a temporary workflow bypass.
Missing merge approval holds merging, never available branch verification. Merge is delivery after
verification, never a substitute for an available branch test.

Then finish each pull request the task changed, once, with its work finished. A follow-up arriving
after the streams ran is built, then
reaches this checkpoint again when it is finished; `review-pass` reviews only what changed since the
head it last accepted, so a small follow-up costs a small review and a large one a full review of the
new work.

Two streams run side by side from here: the guidance stream and the source stream.

- **Guidance stream.** Invoke `process-ledger` for the task's private ledger. It sends the
  `guidance_correction` batch it freezes to `edit-skill`'s **Guidance Delivery** route, delegated
  so it never waits on the source stream. Before a source pull request's source-stream step 1,
  every pending `guidance_correction` entry the GitHub rule's **Branches and Pull Requests** puts
  on it, in the batch in flight or waiting for the next one, is pushed to it and passes its source
  check and smoke round, as **Guidance Delivery** step 1 says, so its review pass, history and
  ready message cover them. An entry waiting for the next batch is delivered only once the batch in
  flight is done, so the source stream then waits for that batch too, and for nothing else before
  step 1. A repair step 1's review pass makes to such an entry's wording repeats that entry's smoke
  round on the repaired head before step 2. A task with none has no guidance stream.
- **Source stream**, in this order for each source pull request; an agent-configuration pull
  request belongs to the guidance stream:

1. Invoke `review-pass` on the pull request, or on the local task diff when none exists, with the
   intent statement. It sizes itself from the changes no earlier pass reviewed — the test sweep and
   security review included — brings in a moved base, simplifies, reviews, fixes, and returns the
   head its final acceptance passed.
2. Shape the history with `rewrite-git-history`. The first time a pull request is sent for review,
   rebuild it into one commit per material change. Each later **Completion** of the same pull
   request, after a follow-up, folds every change into the commit it amends through that skill's
   fixup route, or adds a new commit for a new material change, and never rebuilds it again, so the
   commits the user already reviewed keep their shape. A rewrite whose tree proof shows an
   identical tree keeps the acceptance verdict and moves `review-pass`'s reviewed head to the
   rewritten head.
3. Reconcile the result with **Product Constraints**' target receipt, updating its sources when
   accepted requirements changed. Verify every requested outcome and every incidental fix, confirm tests and relevant validation
   cover each of them and every simplification, confirm intentional contract changes are reflected
   in the expected behavior, and confirm multi-repository delivery artifacts describe only their
   owning repository. Then build this pull request's ready-for-review message, in the shape below,
   from `list-prs`, what the run did and `review-pass`'s **Result**.
4. Send step 3's message; the pull request stays draft. Only when **Task Authorization** finds
   the merge authorized, invoke `merge-gate` with the accepted head and, as its fix rule, the
   **Pre-Push Gate** with each fix folded into its commit through `rewrite-git-history`'s fixup
   route. It readies the pull request, which starts its test jobs once, fixes what they report and
   merges; when it returns, send one line with the result it read: the merge, or the gate that
   holds it.

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
- **Review:** <full | delta `<reviewed head>..<head>` | trivial delta `<reviewed head>..<head>` | nothing new> · <n> simplification fix(es) · <n> code-review finding(s) fixed · acceptance passed on `<head>` — leave out each count `review-pass` did not run
- **History:** <n> commits (<subject> · <subject> · …)
- **Fixed on the way:** <each incidental fix, or none>
- **Noticed, not changed** (over the size budget):
  1. <item>
- **Still running:** <the authorized merge through `merge-gate` (CI ~<n> min) | the guidance fixes from this task that have their own pull request (<n> correction(s)) | nothing>

**Next:** <review the pull request; send follow-ups here, `/finish-pr` to review the whole pull request and merge, or `/merge-now` to merge first and review after | review the pull request; it merges once its checks pass>
```

The run stays open until both streams finish: the source stream when its message is sent, or when
`merge-gate` returns from an authorized merge; the guidance stream when `process-ledger` reports no
remaining entries other than kept `review` records, or a concrete retained hold.

A workflow that already runs `review-pass` runs step 1 as its own; one that already invokes
`merge-gate` runs step 4 as its own.
