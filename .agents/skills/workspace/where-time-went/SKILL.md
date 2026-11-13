---
name: where-time-went
description: "Show where agent working time and usage went in the current session as a dashboard: the main agent, subagents, loops and their rounds, repeated work and scope overlap, as expandable trees. Use only when the user invokes it."
short_description: 'Show where agent working time went, as a dashboard.'
disable-model-invocation: true
---

# Where Time Went

## Dependencies

- `use-dashboard`

Explain where this session's agents spent their working time, and what came of it, from the
session's own evidence. By default cover the whole current session through invocation, including
nested agents; honor a requested task or time range. Read only this session and its descendants,
never unrelated chats. A compacted summary does not narrow the time range: recover earlier records
where available and mark gaps where they are not.

## Working time

Only time an agent spends doing work counts: thinking and writing, running a tool, or waiting on its
own command, test run or child agent. Time spent waiting on the user is never counted, measured or
shown, whether it is a question-tool request, a turn left open for the user's reply, or a worker
idle until its next assignment arrives; it is excluded from every figure, phase and row, and no
page names it.

- **Busy intervals.** Read each transcript in time order. The span between two records is busy,
  except a span that runs from a turn's last message to the next message from the user or the
  coordinator, and a span inside a request the user must answer. A tool call is busy from its call
  to its result.
- **Agent working time** is the union of every agent's busy intervals, so a parent waiting on a
  child and the child's own work count once.
- **An agent's working time** is the sum of its own busy intervals. A worker that receives several
  assignments over the session is split into one entry per assignment, each from the message that
  gave it to the end of the work it did, so a long-lived worker shows what each round of its work
  cost.
- **Main agent's own work** is its working time outside the spans it spent waiting on a foreground
  child.
- An agent still running has no terminal record: count it through invocation and mark it running,
  never failed. A start or end the records lack is unavailable, never zero. Use fresh and cached
  token counts and tool calls where the host records them, respecting the host's token definitions,
  and mark them unavailable otherwise; never estimate them.

## Gather and attribute

Read the session transcript, task and agent records, tool events and descendant records. Use
timestamps and actual parentage, task briefs, handoffs, skill runs, rounds, actions and terminal
states. Record assigned scope separately from work actually observed.

Group loops and rounds from their recorded workflow, launch and handoff provenance: a review loop's
rounds, a gate's repeated passes, a council, a worker's assignments. A repeat can be a later round
of the same workflow; name its cause and outcome where recorded. When grouping is inferred, label it
and give the evidence; never make a loop from an inactivity gap. Launch order alone does not number
rounds. Show every group in scope, not only the latest.

Compare assigned and observed scopes. Classify overlapping work by its purpose, such as independent
review, handoff, repeated research or duplicate implementation; shared files, concurrent lifetimes
or repeated reads alone do not establish duplication. Rank the largest contributors to working time
and classify each as necessary, rework, detour or avoidable only where evidence supports it,
otherwise unknown. Overlapping contributors are never added as if they were disjoint.

## Dashboard

Build a `use-dashboard` spec and deliver it through that skill as a dashboard of session work, so a
later run in the same session updates the same page. `title` is `Where Time Went Dashboard`;
`topic` names the session's work in a few words; `subtitle` says that only agent working time is
shown. Its pages, in order:

- **Overview** (`overview`). Metrics: agent working time, the main agent's working time with its own
  work as the detail, subagent working time with the count of agents, and tokens. A `table` of where
  working time went, one row per top-level workflow with its working time and classification, and a
  short `notes` section on how working time is measured and any evidence gap.
- **Loops** (`diagram`). One `tree`: each workflow, then its rounds or groups, then the agents or
  assignments inside them. Each entry's `figure` is its working time and `meta` its outcome, with a
  `tone` only for a state the reader scans for, such as running or flagged. An agent or assignment
  opens, through `details`, a table of its longest activities with their tool and minutes.
- **Timeline** (`calendar`). One `tree` of the session's phases in order, each labeled by the work
  done in it with its agent working time as `figure`; its children are the agents, assignments and
  review children active in that phase, in the order they started, each with its working time in
  the phase and, where recorded, its longest activities in `details`.
- **Agents** (`people`). A counted `table`, one row per distinct agent: its role, parent, working
  time, fresh and cached tokens and tool calls, `Unavailable` where the host records none.

Name agents by role or task, never by ID. A spec holds no raw transcript, credential or secret.
After delivery, reply with the page's link or file and one line: agent working time and the largest
contributor.

## Guardrails

Read-only apart from the dashboard: never launch agents or reviews, message, stop or resume agents,
mutate records or repair work. Running this skill authorizes none of those.
