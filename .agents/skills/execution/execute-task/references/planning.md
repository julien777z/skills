# Planning

How a plan reaches the user, how a follow-up joins the run, and what the ledger records about a
plan. `SKILL.md`'s **Plan** names this file at the point each is read.

Contents: **Showing The Plan**, **Follow-Ups**, **Progress Record**.

## Showing The Plan

- **The user sees a plan once `review-proposal` has accepted it, or, where the running workflow
  states a plan route straight to the Proposal gate, once that gate has, and never before.** A plan
  still being drafted or reviewed stays with the run: nothing the user reads — a report, a summary,
  a status line, a task list, a dashboard or a question — shows its steps, estimates or an outline
  of them, and a draft is never offered as a preview; a report says only that a plan is being
  prepared. This holds back the plan, never its open decisions, which go first.
- Off that route, before showing a plan, invoke `review-proposal` on the detailed plan once the
  user's answers to its decisions are folded in, with its intent and verified ownership evidence;
  the user's short plan consumes that receipt while it adds nothing the detailed plan lacks.
  [Authorization](authorization.md)'s **Approval Boundaries** consumes the receipt, and
  its **Choices Between Versions Of A Page** applies to a decision between versions of a page.
- **A plan with no open decision is shown, and its work starts in the same turn.** An open decision
  is a product, scope, security, disclosure or authorization choice that is the user's and that
  they have not answered. A plan holding one sends those decisions first and starts only
  independent authorized work until they are answered. Once they are, or when the plan never held
  one, the accepted plan goes to the user as a message with no approval question, **Execution**
  starts without waiting for a reply, and the user can interrupt at any point.
- **A plan shown this way is never called approved**: every record, report,
  dashboard and brief says it was shown with no open decision, and when.
- Showing a plan starts ordinary implementation and verification under the task's authorization.
  A merge, deployment, publication or release it lists still waits for what **Task Authorization**
  names, and a substantial skill change the user asked for stays held on its proposed flow.
- An interruption continues the same plan. Never replace or silently revise a plan the user has
  seen: pause the work an amendment affects, fold it into the detailed plan, ask any decision it
  opens, take the plan through `review-proposal` again, and show the complete revised plan.
- **Offering the next step as a choice is a stop wearing a question mark.** "Say the word and I will
  start the next group" hands back an instruction the user gave once. Ask only for a decision that
  is genuinely the user's, and put it in the question rather than in the plan's continuation.

## Follow-Ups

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
  Pause affected work when **Priority** brings the amendment into execution; otherwise retain it
  for after the active work. Resume once any decision it opens is answered and its priority permits. Unaffected work keeps
  running while the user decides.
- **One that narrows scope reaches the work already in flight, at once.** Message every running
  worker to stop the work the cut removes and has not yet done, keeping what it already finished,
  and record the cut in the intent statement every later gate and review receives. A finding in
  the cut work, a defect included, is answered as out of scope rather than fixed, unless this
  change introduced it.
- A follow-up on a pull request already sent for review pushes to the same draft; **Completion**'s
  **Shape the history** folds it into the existing commits.

## Progress Record

- **The ledger holds the plan's current state, so nothing about progress depends on what the chat
  still remembers.** When an accepted plan goes to the user, record it with `session-ledger` as a
  `plan` entry holding the fields `session-ledger` names for one, its status `shown` with that time,
  filled from the planning work even where the plan shown to the user leaves them out. Work the user
  adds to an active task, with or without a plan of its own, becomes a step on that plan or a plan
  entry of its own, with the user's words and the time they added it, before the first
  edit or dispatch it authorizes; a harness task list, the chat or a summary is never where it first
  lives. A step the agent adds, or widens past what the user asked, is recorded as agent-originated,
  proceeds under the task's authorization like the work **When A Plan Is Needed** says a plan in
  execution covers, and is never shown as user-approved; one that is a product choice goes to the user
  before it is built, as `pre-production`'s **Product Choices** says. Update it when the state
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
