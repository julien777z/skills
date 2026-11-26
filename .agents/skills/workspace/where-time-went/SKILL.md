---
name: where-time-went
description: "Show where the current session's working time went as a dashboard: the main agent, subagents, loops and their rounds, and what happened inside each — its stages of work, check runs and the agents it started — as expandable trees, beside what is running now and what is still to do. Run only when the user asks for it."
short_description: 'Show where session working time went, as a dashboard.'
---

# Where Time Went

## Dependencies

- `use-dashboard`
- `session-ledger`

Explain where this session's agents spent their working time, and what came of it, from the
session's own evidence. By default cover the whole current session through invocation, including
nested agents; honor a requested task or time range. Read only this session and its descendants,
never unrelated chats. A compacted summary does not narrow the time range: recover earlier records
where available and mark gaps where they are not.

## Working time

Working time is clock time during which an agent was working: thinking and writing, running a tool,
or waiting on its own command, test run or child agent. Time an agent spends idle waiting on the
user is never counted: a blocking question-tool request, a turn left open for the user's reply, and a
worker idle until its next assignment arrives are all outside it. Work done while a question is
pending, by the agent that asked or by any other, still counts.

- **Busy intervals.** Read each transcript in time order. The span between two records is busy,
  except a span that runs from a turn's last message to the next message from the user or the
  coordinator, and a span in which the agent's only activity is a pending user request. A tool call
  is busy from its call to its result.
- **Every figure is clock time.** A single agent's or assignment's figure is the length of its busy
  intervals. A group's figure, whether a workflow, a round, a phase or the whole session, is the
  length of the union of its members' busy intervals.
- **A worker that receives several assignments** over the session is one entry per assignment, each
  from the message that gave it to the end of the work it did; a continuation of the same work after
  a restart or a context summary joins the assignment it continues.
- **The main agent's own work** is its busy time outside the spans it spent waiting on a foreground
  child.
- An agent still running has no terminal record: count it through invocation and mark it running,
  never failed. A start or end the records lack is left out of the figures, never counted as zero.

## Gather and attribute

Read the session transcript, task and agent records, tool events and descendant records. Use
timestamps and actual parentage, task briefs, handoffs, skill runs, rounds, actions and terminal
states.

Group loops and rounds from their recorded workflow, launch and handoff provenance: a review loop's
rounds, a gate's repeated passes, a council, a worker's assignments. A repeat can be a later round
of the same workflow; name its cause and outcome where recorded. When grouping is inferred, label it
from the evidence; never make a loop from an inactivity gap. Launch order alone does not number
rounds. Show every group in scope, not only the latest.

Assess each top-level workflow as rework, detour or avoidable only where evidence supports it;
anything else carries no assessment.

### States

Each workflow, agent, assignment and plan step is in one state, with its pill and tone: **Active**,
`accent`, running now; **Blocked**, `critical`, started and waiting on something; **Up next**,
`next`, not started yet; **Done**, `good`, finished. A reviewer's verdict, such as Approved, Changes
or Flag, takes the place of Done on a review, and a workflow's Rework, Detour or Avoidable,
`warning`, takes its place where the evidence supports one; finished work with nothing standing out
shows Done alone, the one such pill the user keeps, and an assessment that says nothing, such as
necessary, is never shown. Read the plans of every ledger this session wrote through
`session-ledger`, leaving out withdrawn and complete plans: a step or part `active` is Active,
`blocked` is Blocked, `next` is Up next with its estimate, `done` is Done and `skipped` is left out.
Work not started goes under the workflow it continues, or under a workflow of its own when nothing
has started it, whose time is its remaining work totaled as `session-ledger` totals a plan, marked
`~`. A ledger that cannot be read is a gap the dashboard names, never an empty plan.

## Dashboard

Build a `use-dashboard` spec and deliver it through that skill as a dashboard of session work, so a
later run in the same session updates the same page. `title` is `Where Time Went Dashboard`;
`topic` names the session's work in a few words; `subtitle` says what the dashboard shows. Its
pages, in order:

- **Overview** (`overview`). Metrics: the session's working time, the number of agents with the
  split between workers and reviewers as its detail, and the longest workflow's time with its name
  as the detail, and a fourth, Now and next, with the count of the Active column's cards on the Now
  and next page as its value, and the Up next column's card count and remaining work, totaled as
  `session-ledger` totals a plan and marked `~`, as its detail. A `table` of where the time went:
  one row per top-level workflow, with its time and its State, as **States** names it — each row
  opening a short write-up of that workflow in a dialog: what it did, its outcome and its largest
  stages, as **What happened** names them.
- **Now and next** (`board`). One `board` with the columns Active (`accent`) and Up next (`next`).
  Each card is one plan step or part, or a running agent no plan step holds, saying what the work
  does: Active holds active and blocked ones, a blocked card carrying `status` Blocked in
  `critical` and an active one no pill; Up next holds those not started, each with its estimate and,
  when the session has several plans, the plan it belongs to in `tag`.
- **Loops** (`list`). One `tree`: each workflow, then its rounds or groups, then the agents or
  assignments inside them, each broken down as **What happened** says. Every entry's `figure` is its
  time, or for work up next its estimate in `meta`; its `status` is a pill as **States**
  says, in the matching tone; the model a reviewer ran on is its `tag`.
- **Timeline** (`calendar`). One `tree` of the session's phases in order, each labeled by the work
  done in it with its time as `figure`. Its children are the agents, assignments and reviewers that
  worked in that phase, in the order they started, each with its time in the phase, its `status` and
  `tag`, and its work in the phase broken down as **What happened** says.

### What happened

A tree entry with a time says what filled it. Its children, in order, are the stages of its work,
each named by what it achieved from the entry's own evidence — its commits, the brief, its reports
and command descriptions — such as a plan step built, a merge resolved, a failing test traced or a
fix applied. Under each stage come its commands and every agent, gate, review round or loop it
started, each broken down the same way. Commands are grouped, never listed one per entry: a stage's
commands become one entry per kind of work, named by what it did and how often, such as running the
records suite four times or reading and editing the gate code, and a single command stands alone
only when it alone fills a large share of its stage. The children account for the entry's time: what
no stage holds is one more child that says what it was, such as reading code or writing the report,
never left out, and a stage with children is accounted for the same way. A listing of an entry's
longest single activities is not a breakdown.

Name agents by role or task, never by ID. A spec holds no raw transcript, credential or secret.
After delivery, reply with one line: the session's working time and the largest workflow.

## Guardrails

Read-only apart from the dashboard: never launch agents or reviews, message, stop or resume agents,
mutate records or repair work. Running this skill authorizes none of those.
