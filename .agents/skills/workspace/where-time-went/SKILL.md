---
name: where-time-went
description: "Show where the current session's working time and scope went as a dashboard: the main agent, subagents, loops and their rounds, and what happened inside each as expandable trees; charts of time by workflow, activity, role and model; the scope of what the changes touched and the agents read, against what was asked; and the agent's own observations on waste and whether the time was justified. Run only when the user asks for it."
short_description: 'Show where session working time went, as a dashboard.'
---

# Where Time Went

## Dependencies

- `use-dashboard`

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

Assess each top-level workflow as necessary, rework, detour or avoidable only where evidence supports
it, otherwise unknown.

## Dashboard

Build a `use-dashboard` spec and deliver it through that skill as a dashboard of session work, so a
later run in the same session updates the same page. `title` is `Where Time Went Dashboard`;
`topic` names the session's work in a few words; `subtitle` says what the dashboard shows. Its
pages, in order:

- **Overview** (`overview`). Metrics: the session's working time, the number of agents with the
  split between workers and reviewers as its detail, and the longest workflow's time with its name
  as the detail. A `table` of where the time went: one row per top-level workflow, with its time and
  assessment, each row opening a short write-up of that workflow in a dialog: what it did, its
  outcome and its largest stages, as **What happened** names them.
  A `chart` of working time by top-level workflow, a `tone` of `warning` on rework and detours,
  each item opening the same write-up as its table row through `details`.
  Then **Observations**: an `outline` of what the agent concludes from every page, each item a
  headline with the figures behind it — where effort was wasted or repeated, what ran longer than
  its result needed, work outside what was asked, rework traced to the step that caused it, such as
  a review's suggested fix followed literally, reviewing set against building, runs lost to rate
  limits or redone after a weaker model, what still stands between the work and done, and a verdict
  on whether the time was justified for the task, said plainly. Each waste names the guidance change
  that would prevent it, or the guidance that already does and when it took effect. Each observation
  is the agent's judgment of the evidence, never a restatement of a figure, and names the page that
  shows it. A cause an observation states is traced, as the global rules require: one that says the
  agents ignored guidance first reads when that guidance took effect, since a rule merged late in
  the session governed only the work after it.
- **Activity** (`activity`). Charts of the same working time cut other ways, each a whole as a pie
  or a comparison as bars: time by kind of activity — the model thinking and writing, running
  tests, waiting on other commands, Git and the hosting service, lint and type checks, reading
  files, editing — summed over every agent, with the main agent's waits on its children left out
  so no time counts twice, and each command counted under the program it runs, never under a path
  or word it names, so a lint run over test files is lint, not running tests; time by role, such as implementation, review, gate, council and skill
  test, with each role's agent count as its `detail`; how many times each gate, review or council
  ran, as bars; and agents per exact model and version. A summed figure says in the chart's
  `description` that it is agent time, which runs past clock time where agents worked in parallel.
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
  of files changed per concern, the last two kinds in `warning`, each item opening its commits; and
  a `table` of the concerns with both counts, each row opening its commits. Then what the agents read: files read per agent, as its median and its largest with
  who read it, and reads by repository and by area as charts, so a reader sees whether reviewers
  read the change or the whole tree.
- **Loops** (`list`). One `tree`: each workflow, then its rounds or groups, then the agents or
  assignments inside them, each broken down as **What happened** says. Every entry's `figure` is its
  time; its outcome is its `status` pill in the matching tone, such as Done, Running, Approved,
  Changes or Flag; the exact model and version a reviewer ran on, such as Opus 5.5, is its `tag`.
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
After delivery, reply with the session's working time, the largest workflow and the observations'
verdict in a few lines.

## Guardrails

Read-only apart from the dashboard: never launch agents or reviews, message, stop or resume agents,
mutate records or repair work. Running this skill authorizes none of those.
