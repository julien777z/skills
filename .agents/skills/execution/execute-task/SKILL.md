---
name: execute-task
description: "Run for reports of broken behavior and at the start of every task authorized to change files — including one whose edits sub-agents make or that starts because work turned up a defect — before recommending, delegating or making edits, and keep it active until verified completion or the user stops or hands it off. Never invoke it from inside a skill it runs. Its references also govern, in any task whether or not it changes files, what an invocation or authorization covers, approval boundaries, steps only the user can take, steps that cannot be taken back, reading state after a push or merge, checking a worker's claim and tracing a cause before reporting it, where working files go, reading an installed app's version or metadata, waits and awaited results, and verification cadence and suite choice."
short_description: 'Plan source and product changes and show the plan; validate canonical guidance changes through their delivery gates.'
---

# Execute Task

Plan source and product changes, show the plan, then run it the same way every time. **Plan**
decides what will be built; canonical guidance changes enter **Execution** directly and are
validated by the gate set `edit-skill`'s **Guidance Delivery** selects for an
agent-configuration pull request.

## Dependencies
- `review-proposal`
- `pre-production`
- `scope-of-change`
- `engineering-conventions`
- `banned-terminology`
- `run-site`
- `code-simplify`
- `review-pass`
- `defer-scope`
- `acceptance-gate`
- `merge-conflict`
- `subagent-matrix`
- `merge-gate`
- `security-audit`
- `rewrite-git-history`
- `process-ledger`
- `list-prs`
- `session-ledger`
- `stop-gates`
- `edit-skill`
- `guidance-flow`
- `test-skill`
- `i-have-adhd`
- `user-facing-output`
- `council`
- `share-media`
- `use-browser`
- `test-fixture`

## One Run Per Task

Follow the explicitly selected workflow’s own declared sequence, checks and delivery holds throughout
the task. Where it owns a stage, return its result to this run rather than starting a parallel stage.

- A report of broken behavior starts a repair unless the user asks for diagnosis only. Invoke this
  skill once at the start of each authorized change, before recommending, delegating or editing.
  Carry defect reports through diagnosis, repair and verification within **Task Authorization**.
  A workaround can help while repair proceeds. **Work You Have Already Named** keeps the run active
  through reports, waits and interruptions, until verified completion or the user stops or hands it off.
- The session agent selects independently applicable specialized skills from their descriptions once.
  They return outcomes, pending decisions and required coordinator work to the caller.
- A selected workflow presents its own plan through the route it declares, an approval it requires included.
- A read-only task uses the relevant reference without running this skill. Delegating edits
  counts as editing. A read-only turn keeps an open run active and advances its named work.

## Plan

Every task that changes files starts here, and so does every follow-up that arrives while one runs.
Before reading code for a plan or selecting targets, load `pre-production`, `scope-of-change` and
`engineering-conventions` whole, each once per task, then apply
**Product Constraints** and **Task Authorization**.

Before choosing a design, and before the first edit on a path that takes no plan, apply
`code-simplify`'s **Before Choosing A Design** check to everything the change will add and write
its receipt in the task record, even for a small follow-up, a bug fix or a worker's task with no
plan of its own; only an edit that adds nothing skips it.

### When A Plan Is Needed

- **Every source or product change gets a plan shown to the user before its first edit, except a
  trivial change or a small, clearly specified follow-up to active work.** A trivial change has no
  design choice in it: a typo, a one-line fix, a rename the user named. A small follow-up directly
  extends the active task using an established behavior or component, with the user naming the
  desired outcome and no unresolved material product, scope, security or disclosure choice. Both
  go straight to **Execution**: the request authorizes their ordinary implementation and
  verification, even when more than one file or an internal dependency must change. Record the
  added work and state the next action; do not turn its implementation outline into another
  approval question. Ask only about a concrete unresolved choice and continue independent work.
  Completing that choice takes no separate plan. Canonical guidance changes under `.agents` do not
  wait for a plan or an output-format approval: their request or an encountered guidance gap
  starts the guidance-correction workflow, and the gate set `edit-skill`'s **Guidance Delivery**
  selects verifies it, on the timing `edit-skill`'s **Recording During A Task** sets for an active task,
  whether the user asked for the correction directly or the run noticed it.
- **A guidance change whose flow is affected is shown as a proposed flow.** Whenever a change's
  statement of scope records `flow affected`, as `edit-skill`'s **Scope Statement** defines it,
  whatever kind of guidance change it is, build `guidance-flow`'s proposed-flow comparison of its
  pushed branch against the default branch and show it to the user; delivery proceeds unless that
  statement lists something waiting for them. `edit-skill`'s **Guidance Changes Proceed
  Automatically** says when one reaches the user.
- Work a plan in execution already covers takes no new plan: an encountered issue, a gate's or a
  review's flag, a failing check, or a guidance correction discovered during the run. `edit-skill`
  records verified guidance corrections for delivery from the next milestone and `process-ledger` processes the rest at **Completion**.

### What The Plan Holds

- For a bug, establish the intended behavior and apply `scope-of-change`'s **Trade-Offs Are
  Surfaced, Never Enforced** before choosing the remedy or presenting an alternative. Use the
  same check when a worker, reviewer, or failed approach changes the proposed remedy.
- Select verification before recommending it, putting it in a plan, or delegating it. Read
  [verification](references/verification.md): its **Verification Cadence** sets when tests, builds,
  walkthroughs and reviews run, its **Suites And Failures** which suites a run covers and how a
  failure is read, and its **Environments** where each runs. Invoke `run-site` to apply its
  **Principles** before selecting browser walkthroughs or rendered UI inspections, including when
  later review or **Completion** proposes additional verification.
- **A plan is written twice: in detail for the run, and short for the user.** The detailed plan —
  the request restated, verified facts, evidence, each step's files and checks — is what
  `review-proposal` reviews and what workers and gates receive; it never goes to the user. While a
  decision the plan depends on is open, the user receives the decisions alone, each with only the
  context it needs; the steps follow once they are answered, written for the answers, never
  conditional on one. The plan the user reads summarizes the detailed plan, adding no step or scope
  it lacks: at most five numbered steps, each one plain line naming one bounded action with its
  wall-clock estimate, as `i-have-adhd` numbers steps, then the total and what the user does
  afterwards. Keep it short enough to read at a glance.
- **A plan's last step for repository changes is the merge**, or the reviewable pull request when
  no merge is authorized. Every verification it needs runs before that; no step, verification, hold
  or user action after it re-verifies the merged change, walks the deployed site, checks a rollout
  or waits for a deploy, apart from the tasks `merge-gate`'s **No Verification Or Deploy Work**
  excepts.
- **An estimate is the executing agent's own wall-clock, never the effort the same work would
  take a person.** Build each step's from [plan estimates](references/plan-estimates.md), and list
  what the plan needs from the user — a review, a merge, a manual action — separately and
  outside the total, with no time, since the agent cannot know how long the user takes; a step
  only a deployment needs follows `user-facing-output`'s rule for it.
- Schedule steps by `subagent-matrix`'s **Dispatch**: coupled work stays sequential, and
  independent scopes with separate owners, files and resources overlap once their inputs are
  settled. Estimate the elapsed time with that overlap, totaled as `session-ledger` totals a plan.
- **Settle ownership before the plan is final.** When the design comparison for a shared operation,
  contract, subsystem, runtime boundary, or independent consumer spans subsystems, delegate its
  inventory to one read-only subagent. Invoke `subagent-matrix` at its standard
  capability level for that reader, launch the exact resolved model, and retain its `subagent-matrix`
  **Output** dispatch line with the plan evidence. The plan states where common
  behavior will live and which policy or wiring stays consumer-specific; it never starts from a parallel
  structure and leaves ownership for implementation.
- Send each message as `user-facing-output` and `share-media` require: any open decisions first,
  on their own, through the global rules' **Asking the user** procedure; then, once they are
  answered and folded into both plans, or when there were none, the user's plan as a message:

```markdown
**Decision needed:**
1. **<subject>** — <what happens today, as fact, and where>. <what each option would change>. I recommend <option>, because <reason>.
```

```markdown
**Plan, starting now**

1. <step> (~<n> min)
2. <step> (~<n> min)

**Total: ~<n> min.** Then <what the user does next, such as review or merge; never a deploy the request does not name>. Interrupt to change any of it.

<**Fixed after the final review:** one line per `last_fixes` item, only when there are any>
```

### Showing The Plan

- **The user sees a plan once `review-proposal` returns it ready, or, where the running workflow
  states a plan route straight to the Proposal gate, once that gate has, and never before.** A plan
  still being drafted or reviewed stays with the run: nothing the user reads — a report, a summary,
  a status line, a task list, a dashboard or a question — shows its steps, estimates or an outline
  of them, and a draft is never offered as a preview; a report says only that a plan is being
  prepared. This holds back the plan, never its open decisions, which go first.
- Off that route, before showing a plan, invoke `review-proposal` on the detailed plan once the
  user's answers to its decisions are folded in, with its intent and verified ownership evidence;
  the user's short plan consumes that receipt while it adds nothing the detailed plan lacks.
  [Authorization](references/authorization.md)'s **Approval Boundaries** consumes the receipt, and
  its **Choices Between Versions Of A Page** applies to a decision between versions of a page.
- **A plan with no open decision is shown, and its work starts in the same turn.** An open decision
  is a product, scope, security, disclosure or authorization choice that is the user's and that
  they have not answered. A plan holding one sends those decisions first and starts only
  independent authorized work until they are answered. Once they are, or when the plan never held
  one, the ready plan goes to the user as a message with no approval question, **Execution**
  starts without waiting for a reply, and the user can interrupt at any point.
- **A plan shown this way is never called approved**: every record, report,
  dashboard and brief says it was shown with no open decision, and when.
- Showing a plan starts ordinary implementation and verification under the task's authorization.
  A merge, deployment, publication or release it lists still waits for what **Task Authorization**
  names.
- An interruption continues the same plan. Never replace or silently revise a plan the user has
  seen: pause the work an amendment affects, fold it into the detailed plan, ask any decision it
  opens, take the plan through `review-proposal` again, and show the complete revised plan.
- **Offering the next step as a choice is a stop wearing a question mark.** "Say the word and I will
  start the next group" hands back an instruction the user gave once. Ask only for a decision that
  is genuinely the user's, and put it in the question rather than in the plan's continuation.

### Priority

Record each active task's priority, status and saved next action through `session-ledger`. A
follow-up joins that record; arrival order does not give it priority. Keep the active higher-priority
work in hand unless the user explicitly reprioritizes it, evidence establishes greater urgency, or
that work completes. State and record the reason before switching, preserving the displaced step.
[Priority](references/priority.md) sets the order and what each rank pauses:

- pending source work ranks above test-only work, whichever was requested or queued first;
- source work a deploy the user is waiting on needs ranks above simplification, review gates, test
  work, guidance delivery and cleanup;
- restoring an authorized broken deployed operation ranks above ordinary tests, review gates,
  guidance delivery and cleanup, and ends with the deployment back on its own sources.

This order grants no deployment or merge authority: **Task Authorization** still governs both.

### Follow-Ups

**Source or product work that adds to what the task delivers is never parked.** A request, a
discussion or an answered decision that extends the task's own outcome, such as a check the user
designs mid-task through answered questions, becomes a step of the active plan record in the turn
it is requested or its last open decision is answered, and starts in that turn unless **Priority**
holds it behind higher-ranked work, its line then recording the holding work and saved next action
as **Work You Have Already Named** says. It lands on the task's pull request and is never reported
as next. Whether the amended plan is shown first follows **When A Plan Is Needed** and **Showing
The Plan**.

Classify each source or product follow-up under **When A Plan Is Needed** before preparing a plan. A small, clearly specified follow-up executes on the user's request; only a follow-up outside that exception needs its own plan. A canonical guidance correction follows **When A Plan Is Needed** and waits for no plan; while a guidance batch is in flight it joins that batch, as `edit-skill`'s **Recording During A Task** says. **Priority** decides when other follow-ups run and whether affected work pauses now; none of the routes below makes arrival order a reason to preempt active recovery.

- **One that touches nothing in flight** — other files, another outcome — leaves the running work
  going. It gets a plan only when **When A Plan Is Needed** calls for one, and runs beside that work
  once any decision it opens is answered and **Priority** permits, under `subagent-matrix`'s
  **Dispatch**. Send this template only for a follow-up that needs a plan:

```markdown
**Running work keeps going:** <step in flight> doesn't touch <what the follow-up changes>.

<**Decision needed:** …, asked on its own first | **Plan for the follow-up, starting now**, once no decision is open>
1. <step> (~<n> min)
```

- **One that changes what is being built** — a source or product follow-up — records the affected
  work and its saved next step under **Work You Have Already Named**, then updates the active
  plan record. Show an amended plan, as **Showing The Plan** says, only when **When A Plan Is
  Needed** requires one; a small, clearly specified follow-up starts without one.
  Pause the in-flight step it affects when **Priority** permits, fold the amendment into that step
  or its worker's brief, and resume the step with it once any decision it opens is answered.
  Unaffected work keeps running while the user decides.
- **One that narrows scope reaches the work already in flight, at once.** Message every running
  worker to stop the work the cut removes and has not yet done, keeping what it already finished,
  and record the cut in the intent statement every later gate and review receives. A finding in
  the cut work, a defect included, is answered as out of scope rather than fixed, unless this
  change introduced it.
- A follow-up on a pull request already sent for review pushes to the same draft, and its
  **Completion** folds each change into the history under `rewrite-git-history`, never rebuilding it.

### Progress Record

- **The ledger holds the plan's current state, so nothing about progress depends on what the chat
  still remembers.** When a ready plan goes to the user, record it with `session-ledger` as a
  `plan` entry holding the fields `session-ledger` names for one, its status `shown` with that time,
  filled from the planning work even where the plan shown to the user leaves them out. Work the user
  adds to an active task, with or without a plan of its own, becomes a step on that plan or a plan
  entry of its own, with the user's words and the time they added it, before the first
  edit or dispatch it authorizes; a harness task list, the chat or a summary is never where it first
  lives. A step the agent adds, or widens past what the user asked, is recorded as agent-originated,
  proceeds under the task's authorization like the work **When A Plan Is Needed** says a plan in
  execution covers, and is never shown as user-approved; one that is a product choice goes to the user
  before it is built, as `scope-of-change`'s **Product Choices** says. Update it when the state
  changes, not when a report is due: the plan being shown, a step starting, finishing, blocking or being
  skipped, a follow-up's plan.
- **A step that waits on other work records what it waits for**: the gate, merge or result whose
  outcome lets it start. Every relayed result is checked against those records, and a result that
  clears one starts the waiting step in that same turn, whichever stream produced it. A report that
  lists only what is still running has not read the plan.
- **A step estimated over 30 minutes is recorded with its parts**: bounded pieces of that step's
  work, each with its own estimate in whole minutes, at least 1, together adding up to the step's.
  Mark each part done as it finishes, so recorded progress moves while a long step runs. The plan
  the user reads keeps its numbered steps; the parts live in the record.

## Execution

Execution starts once a required plan has been shown, or immediately when **When A Plan Is Needed** requires no plan. Canonical guidance corrections follow `edit-skill`'s **Recording During A Task** timing.

### Assigning Work

Before implementation and whenever new work is admitted, delegate the work `subagent-matrix`'s
**When To Delegate** gives to a subagent, launched under its **Dispatch**; a task waiting on a worker never holds another
independent one. Reassess ownership after each finding or follow-up. Each editing worker gets a
worktree of its own and `subagent-matrix`'s worker brief, filled with the plan's reuse receipts. Its
report carries a receipt for each thing it added; one without them goes back to the worker before
its head is built on. Before writing a script or doing a check by hand, the agent
and every worker look in the repository's `.agents/tools/` and write, run and maintain helpers
there as [repository helpers](references/repository-helpers.md) says. While a worker runs, it is
checked on a schedule, its output looked over and its pull requests spot-checked, as
[worker checks](references/worker-checks.md) says.

### Task Authorization

Apply [authorization](references/authorization.md) throughout the run: what the task's
authorization covers, when an intermediate step is a new approval boundary, how a step only the
user can take and a choice between versions of a page are put to them, and which questions the
guidance already answers.

- Carry the user's authorization for the task through its ordinary work, and ask only where its
  **What An Authorization Covers** says a new authorization is needed.
- Merge, deployment, publication and release are separate outcomes, authorized as `merge-gate`'s
  **Authorization** says. Without it, the task is complete at the reviewable draft pull request whose
  local checks and **Completion** review have passed; hosted test jobs are required only at the merge.
- With the merge authorized, the pull request stays draft through the source stream's review;
  `merge-gate` marks it ready, as the last step before the merge, once `review-pass` has accepted
  its head.
- A change that has failed 3 review rounds is not repaired again: put its disposition to `council`
  in **Ask** mode as [review rounds](references/review-rounds.md) says, and follow its ruling.

### Working Environment

Apply [working environment](references/environment.md): its **Working Files** puts everything
the run writes for itself or its workers in `.agent_sources/` at the worktree's root; its **Copies A
Sync Service Left Behind** deletes each such copy before anything stages, stashes or snapshots the
tree; its **Browser Access** runs browser work in the browser `use-browser` selects; its **Installed Apps** reads an app's version from its files, never by running it; its **Environment Refusals** treats an environment refusal as a route to find, and what a permission check refuses as not attempted again;
and its **Steps That Cannot Be Taken Back** runs a deletion, overwrite, push, merge or post only
after its gating check has been read, outside the command, chain or batch that runs the check.

### Product Constraints

`pre-production`, `scope-of-change` and `engineering-conventions` are active in every change task,
loaded whole as **Plan** says, before the first edit. Read the product state from project guidance
before changing a contract or stored value.

Before reading code for a plan or selecting targets, as **Plan** says, and again before recommending
an implementation, asking a question that presupposes one, or delegating its edits, apply [product
constraints](references/product-constraints.md) and **Task Authorization**: resolve the request's
targets in the named outcome's context, trace the requested behavior through its runtime path into
the target receipt, and read the rules and analogous files governing every surface an edit reaches.
A proposal failing a settled requirement is repaired before implementation; an ownership or scope
change builds `acceptance-gate`'s owned-boundary receipt before the implementation is selected.

Before an edit that crosses a trust boundary `security-audit` names, invoke it and apply its
**While Writing Code**.

### Encountered Issues

Apply `scope-of-change`'s **Encountered Issues** while making the change, as [encountered
issues](references/encountered-issues.md) says: its **Disposition** says what is fixed in the change
in flight and what is recorded with `defer-scope`, how an instruction one agent passes another is
checked against the standing guidance before it is sent and before it is acted on, and when a
correction is asked about, offering a fix to the user being no disposition; its **CI Gates And
Deliberate Breaks**, how a required check that detects deliberate changes, red on an intentional
break, is reported, never suppressed or designed around; its **Widened Scope**, the borderline-item
triage.

### Ongoing Simplification

A finished plan step or worker task gets its local checks under the GitHub rule's **Pre-Push Gate**. When a later
step builds on it — reads its schema, calls its interface, extends its code — it also gets one
`acceptance-gate` Diff question over its diff, with the intent statement, before that later step
starts, so a wrong foundation is caught before more is built on it. A step nothing later depends
on gets no gate, and no simplification pass or review runs per step, per worker task or per fix.
`review-pass`'s review loop and one final `acceptance-gate` run once over every change not yet
reviewed at **Completion**. Before any gate over Python files, mid-task or final, its caller runs
`acceptance-gate`'s pre-gate check, `scripts/python_rule_findings.py`, on them.

Simplify a feature as it is built, owning it through integration:
[simplification scope](references/simplification-scope.md) says who owns what and that the pass
covers the changes, the similar code they resemble and the sibling modules around them.

### Pre-Push Gate And Reported Outcomes

Apply the GitHub rule's **Pre-Push Gate** to each push, read with
[verification](references/verification.md)'s **Pre-Push Checks**, which names what this skill
supplies for it, and [reported outcomes](references/outcomes.md) before reporting or building on a result: read the
state an action left, at its source, and do whatever that read shows wrong next, invoking
`merge-conflict` when a push read-back shows a conflicting base.

### Pull Requests

The GitHub rule's **Branches and Pull Requests** owns pull-request selection, a guidance change
riding a source branch included: apply it before keeping a checked-out branch or updating a pull
request, verify the selection remotely, and leave another session's branch and pull request
untouched unless the selected route directs continuing it.

**Every task that changes repository files opens or updates its draft pull request.** At the first
validated commit, push and open the draft in the same step, then read back its URL and head. An
open question, a later step, or a batch still collecting changes holds none of it back. If a
required check or the host prevents delivery, keep the push and pull request as pending work.

**A pull request's title and description are brought up to date at every milestone, not at every
push.** A milestone is a finished plan step or worker task whose checks pass, and a guidance correction pushed onto the pull request carrying it. After it, add
what the milestone changed and rewrite whatever no longer holds, as `engineering-conventions`' **Repository
Text** says, before the milestone is reported. A push inside a step, such as a repair or a rebase,
leaves the description for that step's milestone. `review-pass`'s **Description Refresh** still
checks it before review.

### Multi-Repository Delivery

When one change spans multiple repositories, treat each repository as an independent delivery
context, with **Pull Requests** applying inside each of them. Write each repository's artifacts and
contents solely from its own perspective and in its own vocabulary, as
[multi-repository delivery](references/multi-repository.md) says, and where the run touched more
than one repository, run its sweep for borrowed names before delivering.

### Resuming While Gates Are Paused

When the user asks to resume the task itself — its execution or implementation, not a question
about the change — follow `stop-gates`' **Asking While Paused** before continuing at the saved
step. Until then the hold suspends **Work You Have Already Named**: named work stays recorded with
its next step and is not resumed.

### Work You Have Already Named

**Priority** decides which named work runs now; lower-priority work retains its saved step and paused
status until that boundary permits it. Recording a commitment never advances it ahead of active recovery.

**Naming work as next is a commitment, and it stays this run's obligation across every later turn**
— including a turn whose own request changes no files, which would otherwise not run this skill at
all. The run that named the work owns it until it is done, and naming it is what keeps the run open
under **One Run Per Task**.

Apply [named work](references/named-work.md):

- A new request, an interruption or a context summary cancels none of it. Record displaced work
  with its next step before whatever displaced it starts, and resume it without waiting for
  "continue".
- After a compaction or handoff, read each step's state from `session-ledger` and the repository,
  never from the summary, and confirm each running worker's check timer.
- Before a report goes out, compare each outstanding item against the line the last report carried
  for it; an unchanged line means the item is finished in this turn when **Priority** permits it.
- A wait blocks only the work that depends on what is awaited. Every wait applies that test to the
  whole plan record, and an awaited result is pending, never a blocker, until it is terminal.

### Completion

When **Priority**'s broken-deployed-operation recovery applies, first reconcile it against the
actual deployed operation. Its unmet branch checkpoint or failed default-source retry keeps this
checkpoint paused; a completed diagnostic or implementation substep does not start either stream.

When an operational, external, or other non-source outcome reaches its authoritative terminal state,
re-enter this checkpoint before any final report. Reconcile the saved work and pending guidance
delivery from their current owners, then resume each first nonterminal delivery stage. A completed
operation, a read-only interruption, or the absence of a source diff or pull request never makes a
pending guidance delivery terminal; a genuine authorization or dependency hold still holds only its
dependent action.

Run this checkpoint before reporting a change complete. Verify that each changed repository has a
pull request carrying the task's final commit. A local installation, configuration, or recovery
can verify the change or restore service while its pull request is in flight. A failed local
setup operation remains work under **Encountered Issues**. The independent gate receives the
affected-repository map and comparison evidence along with the diff.

Before the final delivery steps below, select the applicable verification route under
[verification](references/verification.md)'s **Environments**, then verify the requested behavior
on the change's branch within the authorized scope, including reachable dependency branches, as
[branch verification](references/branch-verification.md) says. Missing merge approval holds
merging, never available branch verification. Merge is delivery after verification, never a
substitute for an available branch test.

Then finish each pull request the task changed, once, with its work finished. A follow-up arriving
after the streams ran is built, then reaches this checkpoint again when it is finished;
`review-pass` reviews only what changed since the head it last accepted, so a small follow-up costs
a small review and a large one a full review of the new work.

Follow the selected workflow’s declared verification and delivery sequence and any hold it places on delivery.

Two streams run side by side from here: the guidance stream and the source stream. When the set
`review-pass`'s **Set and timing** defines holds more than one pull request, invoke its **Combined
Review** once each has its accepted head.

- **Guidance stream.** Invoke `process-ledger` for the task's private ledger. It sends the
  `guidance_correction` batch it freezes to `edit-skill`'s **Guidance Delivery** route, which the
  primary agent coordinates so its review and checks never wait on the source stream. Before a source pull request's **Review the pull request**,
  every pending `guidance_correction` entry the GitHub rule's **Branches and Pull Requests** puts
  on it, in the batch in flight or the one after it, is pushed to it and passes its source check,
  as **Guidance Delivery**'s **Resume the batch** says, so its review pass, history and ready message cover them. An entry recorded after the batch in flight merged is delivered in the batch frozen
  once that one is done, so the source stream then waits for that delivery too, and for nothing
  else before **Review the pull request**. Each such entry's skill-test round runs on the head **Review the pull request** accepted, before
  **Shape the history**, and a repair it makes returns to review as **Guidance Delivery**'s **Conclude the skill test** says. A task with none has no guidance stream.
- **Source stream**, in this order for each source pull request; an agent-configuration pull
  request belongs to the guidance stream, and a side pull request carrying both kinds to this one:

1. **Review the pull request.** Invoke `review-pass` on the pull request with the
   intent statement. It runs its review loop and one final `acceptance-gate` over the changes no
   earlier pass reviewed, brings in a moved base, and returns the head its final acceptance passed.
2. **Shape the history** with `rewrite-git-history`. The first time a pull request is sent for review,
   rebuild it into one commit per material change. Each later **Completion** of the same pull
   request, after a follow-up, folds every change into the commit it amends through that skill's
   fixup route, or adds a new commit for a new material change, and never rebuilds it again, so the
   commits the user already reviewed keep their shape. A rewrite whose tree proof shows an identical
   tree keeps the acceptance verdict and moves `review-pass`'s reviewed head to the rewritten head.
3. **Reconcile the result** with **Product Constraints**' target receipt, updating its sources when
   accepted requirements changed. Verify every requested outcome and every incidental fix, confirm tests and relevant validation
   cover each of them and every simplification, confirm intentional contract changes are reflected
   in the expected behavior, and confirm multi-repository delivery artifacts describe only their
   owning repository. Then build this pull request's ready-for-review message, in the shape below,
   from `list-prs`, what the run did and `review-pass`'s **Output**; side work never holds it.
4. **Merge when authorized.** When **Task Authorization** finds the merge authorized, send **Reconcile the result**'s message together with the
   invocation of `merge-gate`, passing the accepted head, `review-pass`'s **Checks** results with their
   commands and head as the behaviors local tests already cover, every exclusion it returned with
   its evidence, and, as its fix rule, `review-pass` over each fix's delta since the accepted head and the
   GitHub rule's **Pre-Push Gate**, with each fix folded into its commit through `rewrite-git-history`'s
   fixup route. It inventories exact-head hosted coverage, obtains fresh results only where no
   equivalent terminal coverage exists, fixes what relevant checks report and merges; when it returns, send one line with the
   result it read: the merge, or the gate that holds it. Otherwise send **Reconcile the result**'s message; the pull
   request stays draft.

The ready-for-review message takes exactly this shape, one message per pull request, in every report
that hands a pull request to the reader for review, a follow-up's included, whether or not the steps
before it ran; a step that did not run is left out of **Review** as that line says, never reported
under another label. Its line
labels are these and no others: each requested outcome, each new behavior worded as new and each
defect the change needed go in **What landed**, and a fix the change did not need goes in **Side
work** with the side pull request carrying it. It leaves out
**Deferred** when nothing was deferred, **Before deploy** when the change needs nothing outside the
code to deploy, **Still running** when none of this pull request's own work is active, and **Side
work** when none is open. Use the message as the material for the review request in the question
tool, as `user-facing-output` directs; the question asks for the review alone, and its own text
leaves out the **Before deploy** line:

```markdown
**Ready for review:** <pull request URL>

- **What landed:** <each requested outcome, each new behavior named as new, and each defect fixed because the change needed it, one clause each>
- **Review:** <full | delta `<reviewed head>..<head>` | nothing new> · review loop <n> round(s), <n> finding(s) fixed · acceptance passed on `<head>` — leave out each count `review-pass` did not run
- **History:** <n> commits (<subject> · <subject> · …)
- **Deferred:**
  1. <item> — <ground> — <record link>
- **Before deploy:** <each step only a deployment needs, such as a secret to add, in plain text>
- **Still running:** <only this pull request's work: the authorized merge through `merge-gate` (CI ~<n> min)>
- **Side work, not holding this review:** <each side pull request, guidance delivery or skill test still open: link — each incidental fix or other change it carries — its state>

**Next:** <review the pull request; send follow-ups here, `/finish-pr` to review what this pass has not and merge, or `/merge-now` to merge first and review after | review the pull request; it merges once its checks pass>
```

The run stays open until both streams finish: the source stream when its message is sent, or when
`merge-gate` returns from an authorized merge; the guidance stream when `process-ledger` reports no
remaining entries other than kept `review` records, or a concrete retained hold.

A workflow that already runs `review-pass` runs **Review the pull request** as its own; one that already invokes
`merge-gate` runs **Merge when authorized** as its own.
