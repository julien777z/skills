---
name: execute-task
description: "Always run this. Invoke once at the start of every task authorized to change files — including one whose edits sub-agents make or that starts because work turned up a defect — before recommending, delegating or making edits, and keep it active until verified completion or the user stops or hands it off. Never invoke it from inside a skill it runs. Its references also govern, in any task whether or not it changes files, what an invocation or authorization covers, approval boundaries, steps only the user can take, what to do when the environment or a permission check refuses an action, steps that cannot be taken back, reading state after a push or merge, checking a worker's claim and tracing a cause before reporting it, where working files go and which browser a task drives, deleting the copies a sync service leaves behind, waits and awaited results, and verification cadence, suite choice and tests that touch the user's desktop."
short_description: 'Plan source and product changes and show the plan; validate canonical guidance changes through their delivery gates.'
---

# Execute Task

Plan source and product changes, show the plan, then run it the same way every time. **Plan**
decides what will be built; canonical guidance changes enter **Execution** directly and are
validated by the gate set `edit-skill`'s **Guidance Delivery** selects for an
agent-configuration pull request, except a substantial skill change the user asks for, whose plan
is a proposed flow.

## Dependencies
- `review-proposal`
- `pre-production`
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

- Invoke this skill once when a task is authorized to change files, before its implementation
  recommendation, delegated edits, or first edit. A run stays active until
  the task's outcome is verified complete or the user explicitly stops or hands it off. **Work You
  Have Already Named** retains outstanding items and their next actions through reports, gates and
  interruptions. Nothing in the task re-enters the skill; the run simply has not ended.
- The session agent selects independently applicable specialized skills from their descriptions once.
  They return outcomes, pending decisions and required coordinator work to the caller.
- A selected workflow presents its own plan through the route it declares, an approval it requires included.
- A read-only task — a question answered from the code, a listing, a report with no edit — does
  not run this skill, though it still reads the reference of this skill that governs a subject it
  meets, as the description lists them; a task whose edits sub-agents make is not read-only for the
  agent that delegated them. A read-only turn does not close an open run either: a run still holding named
  work stays active through such a turn, and that turn moves its items.

## Plan

Every task that changes files starts here, and so does every follow-up that arrives while one runs.
Before drafting a plan or selecting targets, apply **Product Constraints** and **Task Authorization**.

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
  Completing that choice takes no separate plan. Canonical guidance changes
  under `.agents`, apart from the substantial skill change the next bullet holds, do not wait for a plan or an output-format approval: their request or an encountered guidance gap starts
  the guidance-correction workflow, and the gate set `edit-skill`'s **Guidance Delivery**
  selects verifies it, on the timing `edit-skill`'s **Recording During A Task** sets for an active task,
  whether the user asked for the correction directly or the run noticed it.
- **A guidance change whose flow is affected is shown as a proposed flow.** Whenever a change's
  statement of scope records `flow affected`, as `edit-skill`'s **Scope Statement** defines it,
  whatever kind of guidance change it is, build `guidance-flow`'s proposed-flow comparison of its
  pushed branch against the default branch and show it to the user; delivery proceeds unless that
  statement lists something waiting for them. **A substantial skill change the user asks for is
  held on it**, in place of a written plan, where a source change of its size would get one: until
  the user approves it in their own words, that pull request gets no `test-skill` round, no merge
  and no auto-merge; each edit they ask for lands on that branch and it is rendered again in place.
- Work a plan in execution already covers takes no new plan: an encountered issue, a gate's or a
  review's flag, a failing check, or a guidance correction discovered during the run. `edit-skill`
  records verified guidance corrections and `process-ledger` processes them at **Completion**.

### What The Plan Holds

- For a bug, establish the intended behavior and apply `pre-production`'s **Trade-Offs Are
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
  outside the total, with no time, since the agent cannot know how long the user takes.
- Schedule steps by `subagent-matrix`'s **Dispatch**: coupled work stays sequential, and
  independent scopes with separate owners, files and resources overlap once their inputs are
  settled. Estimate the elapsed time with that overlap, totaled as `session-ledger` totals a plan.
- **Settle ownership before the plan is final.** When the design comparison for a shared operation,
  contract, subsystem, runtime boundary, or independent consumer spans subsystems, delegate its
  inventory to one read-only subagent. Invoke `subagent-matrix` at its standard
  capability level for that reader, launch the exact resolved identifier, and retain catalog state,
  identifier, assignment state and host receipt with the plan evidence. The plan states where common
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
```

### Showing The Plan

The user sees a plan only once `review-proposal` has accepted it, and its work starts in the same
turn when no decision is open. [Planning](references/planning.md)'s **Showing The Plan** holds the
route, read before a plan is shown.

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

A small, clearly specified follow-up executes on the user's request, and any other is classified
under **When A Plan Is Needed**. [Planning](references/planning.md)'s **Follow-Ups** holds the
routes and templates, read when a follow-up arrives.

### Progress Record

The ledger holds the plan's current state through `session-ledger`, updated when the state changes.
[Planning](references/planning.md)'s **Progress Record** holds what is recorded, read before a plan is
recorded or a step is added.

## Execution

Execution starts once a required plan has been shown, or immediately when **When A Plan Is Needed** requires no plan. Canonical guidance corrections follow `edit-skill`'s **Recording During A Task** timing.

### Assigning Work

Before implementation and whenever new work is admitted, delegate the work `subagent-matrix`'s
**When To Delegate** gives to a subagent, launched under its **Dispatch**. Reassess ownership after each finding or follow-up. Each editing worker gets a
worktree of its own and `subagent-matrix`'s worker brief, filled with the plan's reuse receipts. Its
report carries a receipt for each thing it added; one without them goes back to the worker before
its head is built on. Before writing a script or doing a check by hand, the agent
and every worker look in the repository's `.agents/tools/`. In a
repository the owner runs, an operation the task will run more than once, or is about to run again,
is first written as a helper there, created with its folder if missing, committed as source work on
the pull request the GitHub rule selects for it, and run from there each time; a shell function,
heredoc or temporary script is not a helper, though a skill's execution checks stay untracked.

### Task Authorization

Apply [authorization](references/authorization.md) throughout the run: what the task's
authorization covers, when an intermediate step is a new approval boundary, how a step only the
user can take and a choice between versions of a page are put to them, and which questions the
guidance already answers.

- Carry the user's authorization for the task through its ordinary work, and ask only where its
  **What An Authorization Covers** says a new authorization is needed.
- Merge, deployment, publication and release are separate outcomes, authorized as `merge-gate`'s
  **Authorization** says. Without it, the task is complete at the reviewable draft pull request whose
  local checks and **Completion** review have passed.
- With the merge authorized, the pull request stays draft through the source stream's review, and
  `merge-gate`'s **Readiness** takes it out of draft.
- A change that has used its review rounds is not repaired again: put its disposition to `council`
  in **Ask** mode as [review rounds](references/review-rounds.md) says, and follow its ruling.

### Working Environment

Apply [working environment](references/environment.md): its **Working Files** puts everything
the run writes for itself or its workers in `.agent_sources/` at the worktree's root; its **Copies A
Sync Service Left Behind** deletes each such copy before anything stages, stashes or snapshots the
tree; its **Browser Access** selects the browser; its **Environment Refusals** treats an
environment refusal as a route to find, and what a permission check refuses as not attempted again;
and its **Steps That Cannot Be Taken Back** runs a deletion, overwrite, push, merge or post only
after its gating check has been read, outside the command, chain or batch that runs the check.

### Product Constraints

`pre-production` is active in every change task: read it whole and invoke it before the first
edit. Read the product state from project guidance before changing a contract or stored value.

Before drafting a plan or selecting targets, as **Plan** says, and again before recommending an
implementation, asking a question that presupposes one, or delegating its edits, apply [product
constraints](references/product-constraints.md) and **Task Authorization**: resolve the request's
targets in the named outcome's context, trace the requested behavior through its runtime path into
the target receipt, and read the rules and analogous files governing every surface an edit reaches.
A proposal failing a settled requirement is repaired before implementation; an ownership or scope
change builds `acceptance-gate`'s owned-boundary receipt before the implementation is selected.

Before an edit that crosses a trust boundary `security-audit` names, invoke it and apply its
**While Writing Code**.

### Encountered Issues

Apply `pre-production`'s encountered-issues policy while making the change, handled as
[encountered issues](references/encountered-issues.md) says:

- Its **Disposition** says what is fixed in the change in flight and what is recorded with
  `defer-scope`, how an instruction one agent passes another is checked against the standing
  guidance before it is sent and before it is acted on, and when a correction is asked about.
  Offering a fix to the user is not a disposition.
- Its **CI Gates And Deliberate Breaks** says how a required check that exists to detect deliberate
  changes, going red on an intentional break, is reported and never suppressed or designed around.

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
request, verify the selection remotely (for a guidance change, `edit-skill`'s `references/guidance-pull-requests.md` sets it out), and leave another session's branch and pull request
untouched unless the selected route directs continuing it.

**Every task that changes repository files opens or updates its draft pull request.** At the first
validated commit, push and open the draft in the same step, then read back its URL and head. An
open question, a later step, or a batch still collecting changes holds none of it back. If a
required check or the host prevents delivery, keep the push and pull request as pending work.

**A pull request's title and description are brought up to date at every milestone, not at every
push.** A milestone is a finished plan step or worker task whose checks pass, and a guidance correction pushed onto the pull request carrying it. After it, add
what the milestone changed and rewrite whatever no longer holds, as `pre-production`'s **Repository
Text** says, before the milestone is reported. A push inside a step, such as a repair or a rebase,
leaves the description for that step's milestone. `review-pass`'s **Description Refresh** still
checks it before review.

### Multi-Repository Delivery

When one change spans multiple repositories, treat each repository as an independent delivery
context, with **Pull Requests** applying inside each of them. Write each repository's artifacts and
contents solely from its own perspective and in its own vocabulary, as
[multi-repository delivery](references/multi-repository.md) says, and where the run touched more
than one repository, run its sweep for borrowed names before delivering.

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
  never from the summary.
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
[branch verification](references/branch-verification.md) says. Branch verification runs whether
or not a merge is authorized, since missing merge approval holds only the merge. A merge is
delivery after verification and replaces no available branch test.

Then finish each pull request the task changed, once, with its work finished. A follow-up arriving
after the streams ran is built, then reaches this checkpoint again when it is finished;
`review-pass` reviews only what changed since the head it last accepted, so a small follow-up costs
a small review and a large one a full review of the new work.

Follow the selected workflow’s declared verification and delivery sequence and any hold it places on delivery.

Two streams run side by side from here: the guidance stream and the source stream. When the set
`review-pass`'s **Set and timing** defines holds more than one pull request, invoke its **Combined
Review** once each has its accepted head.

The guidance stream and the source stream, with the steps of each, are in
[completion streams](references/completion.md), read when this checkpoint starts. The source
stream runs **Review the pull request**, **Shape the history**, **Reconcile the result** and **Merge
when authorized** in that order for each source pull request; an agent-configuration pull request
belongs to the guidance stream.

The ready-for-review message takes exactly this shape, one message per pull request, leaving out
**Deferred** when nothing was deferred:

```markdown
**Ready for review:** <pull request URL>

- **What landed:** <each requested outcome, one clause each>
- **Review:** <full | delta `<reviewed head>..<head>` | nothing new> · review loop <n> round(s), <n> finding(s) fixed · acceptance passed on `<head>` — leave out each count `review-pass` did not run
- **History:** <n> commits (<subject> · <subject> · …)
- **Fixed on the way:** <each incidental fix, or none>
- **Deferred** (over the size budget):
  1. <item> — <record link>
- **Still running:** <the authorized merge through `merge-gate` (CI ~<n> min) | the guidance fixes from this task that have their own pull request (<n> correction(s)) | nothing>

**Next:** <review the pull request; send follow-ups here, `/finish-pr` to review what this pass has not and merge, or `/merge-now` to merge first and review after | review the pull request; it merges once its checks pass>
```

The run stays open until both streams finish: the source stream when its message is sent, or when
`merge-gate` returns from an authorized merge; the guidance stream when `process-ledger` reports no
remaining entries other than kept `review` records, or a concrete retained hold.

A workflow that already runs `review-pass` runs **Review the pull request** as its own; one that already invokes
`merge-gate` runs **Merge when authorized** as its own.
