---
name: where-time-went
description: "Show where the current session's working time and scope went as a dashboard: the main agent, subagents, loops and their rounds, and what happened inside each as expandable trees; charts of time by workflow, activity, role and model; the scope of what the changes touched and the agents read, against what was asked; and the agent's own observations on waste and whether the time was justified; beside what is running now and what is still to do. Run only when the user asks for it."
short_description: 'Show where session working time went, as a dashboard.'
---

# Where Time Went

## Dependencies

- `use-dashboard`
- `session-ledger`
- `progress`

Explain where this session's agents spent their working time, what they touched and read, and what
came of it, from the session's own evidence, so the reader can judge it for waste. By default cover the whole current session through invocation, including
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
- **Every figure is clock time**, apart from the Activity charts by kind of activity and by role,
  which are summed over every agent as use-dashboard allows a figure summed over parallel work. A single agent's or assignment's figure is the length of its busy
  intervals. A group's figure, whether a workflow, a round, a phase or the whole session, is the
  length of the union of its members' busy intervals.
- **A worker that receives several assignments** over the session is one entry per assignment, each
  from the message that gave it to the end of the work it did; a continuation of the same work after
  a restart or a context summary joins the assignment it continues.
- **The main agent's own work** is its busy time outside the spans it spent waiting on a foreground
  child.
- An agent still running has no terminal record: count it through invocation and show it Active,
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

Each workflow, round or group, phase, stage, group of commands, agent, assignment and plan step is
in one state, a group's from its members as `use-dashboard` says: **Active**, running now;
**Blocked**, started and waiting on something; **Up next**, not started yet; **Done**, finished,
whatever its verdict or assessment. Its entry's dot and pill follow `use-dashboard`'s **Making A
Dashboard**, and a table cell names the state in words. The pills that stay are a reviewer's verdict
asking for a look, such as Changes or Flag, and a finished workflow's Rework, Detour or Avoidable
where the evidence supports one, all `warning`, and what a blocked entry waits on; finished work
with nothing standing out shows a Done pill in `good`, which the user keeps although it repeats its
dot, and an assessment that says nothing, such as necessary, is never shown. Read the plans of every
ledger this session wrote through `session-ledger`, leaving out withdrawn and complete plans: a step
or part `active` is Active, `blocked` is Blocked, `next` is Up next, `done` is Done and `skipped` is
left out, and a step with parts is read part by part. A plan still waiting on a decision or approval
keeps its steps, each tagged Proposed. Work not started goes under the workflow that ran its plan's
earlier steps, or under an entry of its own named for the plan when none has run. Its estimate is
shown in `meta`, marked `~`, never as a `figure`, and never counts toward working time or the
longest workflow; a total of remaining work is totaled as `session-ledger` totals a plan. A ledger
that cannot be read is a gap the dashboard names, never an empty plan.

## Dashboard

Build a `use-dashboard` spec and deliver it through that skill as a dashboard of session work, so a
later run in the same session updates the same page. `title` is `Where Time Went Dashboard` and
its `icon` `activity`;
`topic` names the session's work in a few words; `subtitle` says what the dashboard shows. Its
pages, in order:

- **Overview** (`overview`). Metrics: the session's working time, the number of agents with the
  split between workers and reviewers as its detail, and the longest workflow's time with its name
  as the detail, and a fourth, Now and next, with "<n> active" from the Active column on the Now
  and next page as its value and "<n> up next · ~<total>" from its Up next column as its
  detail. A `table` of where the time went:
  one row per top-level workflow, with its time and its state, as **States** names it — each row
  opening a short write-up of that workflow in a dialog: what it did, its outcome and its largest
  stages, as **What happened** names them.
  A `chart` of working time by top-level workflow, a `tone` of `warning` on Rework, Detour and Avoidable,
  each item opening the same write-up as its table row through `details`.
  Then **Observations**: an `outline` of what the agent concludes from every page, each item a
  headline with the figures behind it — where effort was wasted or repeated, what ran longer than
  its result needed, work outside what was asked, rework traced to the step that caused it, such as
  a review's suggested fix followed literally, reviewing set against building, runs lost to rate
  limits or redone after a weaker model, and a verdict
  on whether the time was justified for the task, said plainly. Each waste names the guidance change
  that would prevent it, or the guidance that already does and when it took effect. Each observation
  is the agent's judgment of the evidence, never a restatement of a figure, and names the page that
  shows it. A cause an observation states is traced, as the global rules require: one that says the
  agents ignored guidance first reads when that guidance took effect, since a rule merged late in
  the session governed only the work after it.
- **Now and next** (`board`). The Active and Up next columns of `progress`'s `board` "Work", built
  as that skill builds them from the same plans, so both dashboards show the same cards; Active also
  holds each running agent no plan step holds, saying what it does.
- **Activity** (`chart`). Charts of the same working time cut other ways, each a whole as a pie
  or a comparison as bars: time by kind of activity — the model thinking and writing, running
  tests, waiting on other commands, Git and the hosting service, lint and type checks, reading
  files, editing — summed over every agent, with the main agent's waits on its children left out
  so no time counts twice, and each command counted under the program it runs, never under a path
  or word it names, so a lint run over test files is lint, not running tests; time by role, such as implementation, review, gate, council and skill
  test, with each role's agent count as its `detail`; how many times each gate, review or council
  ran, as bars; and agents per model.
  Every item opens what it sums through `details`: an activity its split by role and the agents
  that spent the most on it, running tests also its whole-suite against targeted runs, its time
  before and after any guidance change about when tests run, and its longest commands; a role its
  launches with model and time; a model its launches by role.
- **Scope** (`data`). What the work touched against what was asked. Per pull request, the concerns
  its commits carry, read from their messages and files, each with its file and line counts and
  whether the request, a standing requirement the user set, guidance the agents applied on their
  own, or nothing asked for put it there. A commit belongs to the concern its files serve, never
  to its kind of edit alone: formatting or a lint fix on files the requested work wrote, or required
  by a standing requirement, is that work. Each concern also counts its files that no requested
  work touched, since that count, not the commit count, is how much it widened a review. A `chart`
  per pull request of files changed per concern, the last two kinds in `warning`, each item opening its commits; and
  a `table` of the concerns with both counts, each row opening its commits. Then what the agents read: files read per agent, as its median and its largest with
  who read it, and reads by repository and by area as charts, so a reader sees whether reviewers
  read the change or the whole tree.
- **Loops** (`list`). One `tree`: each workflow, then its rounds or groups, then the agents or
  assignments inside them, each broken down as **What happened** says. Every entry's `figure` is its
  time, or for work up next its estimate in `meta`; its `tone` and any `status` are as **States**
  says; the model a reviewer ran on is its `tag`, named as `use-dashboard` names a model, and its
  label names its role without that model.
- **Timeline** (`calendar`). First a `timeline` of when the work ran: one lane per top-level
  workflow, tagged with its model when one agent ran it, a bar per stretch it worked toned as its
  state, and each pause longer than an hour, such as a rate-limit wait or the user away, a gap
  labeled with its length. Then one `tree` of the session's phases in order, each labeled by the work
  done in it with its time as `figure`. Its children are the agents, assignments and reviewers that
  worked in that phase, in the order they started, each with its time in the phase, its `tone`,
  `status` and `tag` as on the Loops page, and its work in the phase broken down as **What
  happened** says.

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
After delivery, reply with the session's working time, the largest workflow and the observations'
verdict in a few lines.

## Guardrails

Read-only apart from the dashboard: never launch agents or reviews, message, stop or resume agents,
mutate records or repair work. Running this skill authorizes none of those.
