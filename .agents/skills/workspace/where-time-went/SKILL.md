---
name: where-time-went
description: "Show where the current session's working time went as a dashboard: the main agent, subagents, loops and their rounds, and the longest activities inside them, as expandable trees. Use only when the user invokes it."
short_description: 'Show where session working time went, as a dashboard.'
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

Working time is clock time during which an agent was working: thinking and writing, running a tool,
or waiting on its own command, test run or child agent. Time spent waiting on the user is never
counted: a question-tool request, a turn left open for the user's reply, and a worker idle until its
next assignment arrives are all outside it.

- **Busy intervals.** Read each transcript in time order. The span between two records is busy,
  except a span that runs from a turn's last message to the next message from the user or the
  coordinator, and a span inside a request the user must answer. A tool call is busy from its call
  to its result.
- **Every figure is clock time.** A single agent's or assignment's figure is the length of its busy
  intervals. A group's figure, whether a workflow, a round, a phase or the whole session, is the
  length of the union of its members' busy intervals, so work that ran in parallel counts once and
  no figure is longer than the clock time it spans.
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
states. Record assigned scope separately from work actually observed.

Group loops and rounds from their recorded workflow, launch and handoff provenance: a review loop's
rounds, a gate's repeated passes, a council, a worker's assignments. A repeat can be a later round
of the same workflow; name its cause and outcome where recorded. When grouping is inferred, label it
from the evidence; never make a loop from an inactivity gap. Launch order alone does not number
rounds. Show every group in scope, not only the latest.

Classify overlapping work by its purpose, such as independent review, handoff, repeated research or
duplicate implementation; shared files, concurrent lifetimes or repeated reads alone do not establish
duplication. Assess each top-level workflow as necessary, rework, detour or avoidable only where
evidence supports it, otherwise unknown.

## Dashboard

Build a `use-dashboard` spec and deliver it through that skill as a dashboard of session work, so a
later run in the same session updates the same page. `title` is `Where Time Went Dashboard`;
`topic` names the session's work in a few words; `subtitle` says what the dashboard shows. Its
pages, in order:

- **Overview** (`overview`). Metrics: the session's working time, the number of agents with the
  split between workers and reviewers as its detail, and the longest workflow's time with its name
  as the detail. A `table` of where the time went: one row per top-level workflow, with its time and
  assessment.
- **Loops** (`diagram`). One `tree`: each workflow, then its rounds or groups, then the agents or
  assignments inside them, then each one's longest activities as its children. Every entry's
  `figure` is its time; its outcome is its `status` pill in the matching tone, such as Done, Running,
  Approved, Changes or Flag; the model a reviewer ran on is its `tag`.
- **Timeline** (`calendar`). One `tree` of the session's phases in order, each labeled by the work
  done in it with its time as `figure`. Its children are the agents, assignments and reviewers that
  worked in that phase, in the order they started, each with its time in the phase, its `status` and
  `tag`, and its longest activities in the phase as children.

Name agents by role or task, never by ID. A spec holds no raw transcript, credential or secret.
After delivery, reply with one line: the session's working time and the largest workflow.

## Guardrails

Read-only apart from the dashboard: never launch agents or reviews, message, stop or resume agents,
mutate records or repair work. Running this skill authorizes none of those.
