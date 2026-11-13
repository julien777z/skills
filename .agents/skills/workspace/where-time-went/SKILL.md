---
name: where-time-went
description: "Report where time and usage went in the current session, including the main agent, waits, subagents, repeated work and scope overlap. Use only when the user invokes it."
short_description: 'Show where session time and usage went.'
---

# Where Time Went

Explain the elapsed time and outcome of this session using its own evidence. By default cover the
whole current session through invocation, including nested agents; honor a requested task or time
range. Read only this session and its descendants, never unrelated chats. A compacted summary does
not narrow the time range: recover earlier records where available and mark gaps where they are not.

## Gather and attribute

Read the available session transcript, task and agent records, tool events, and descendant records.
Use timestamps and actual parentage, task briefs, handoffs, skill runs, rounds, actions and terminal
states. Record assigned scope separately from work actually observed. A running agent remains running
until a record shows a terminal state; report silence and its duration without inferring failure.

Build a chronological timeline of main-agent activity, tool waits, user waits, subagent work and
unexplained intervals. Split at observed boundaries and show concurrent activity together. Elapsed
time is the union of intervals, so a parent's wait and a child's work do not count twice. Subagent-minutes
are the sum of observed subagent lifetimes clipped to the requested range, including overlaps; exclude
the main agent and count each descendant once, separately from any parent-inclusive host totals. They
are not CPU time. For a running agent with a known start, measure through invocation; a missing
completion on an agent not recorded as running remains unknown.
Distinguish unavailable starts or ends from zero duration and do not infer effort from an unknown
interval. Identify evidence gaps and any uncertainty in the resulting totals.

Group loops and rounds from their recorded workflow, launch and handoff provenance. A repeat can be
a later round of the same workflow; identify its cause and outcome where recorded. When grouping is
inferred, label it and explain the evidence; do not create a loop from an arbitrary inactivity gap.
Label every inferred group and round, including individual numeric worker rows. Launch order alone
does not establish round numbering; use unavailable and describe the assignment sequence instead.
Show all groups in scope, not just the latest ones. Use fresh and cached token counts and tool calls
when available; mark missing values unavailable, never estimate them. Respect the host token definitions: cached input may be a subset of total input, not additional
usage. Count native cumulative records once rather than adding successive snapshots or counting
nested totals twice.

Compare assigned and observed scopes, using the evidence for each. Classify overlapping work by its
purpose, such as independent review, handoff, repeated research or duplicate implementation. Shared
files, concurrent lifetimes or multiple reads alone do not establish duplication. Attribute repeated
work to its recorded cause and outcome; state uncertainty where evidence cannot decide. Rank the
largest contributors to elapsed time and classify each as necessary, rework, detour or avoidable only
when evidence supports it; otherwise say unknown. Do not add overlapping contributors as if they
were disjoint elapsed time.

## Output

Lead with the total elapsed time and a one-line outcome, followed by exactly these five tables in
order. Use minutes to one decimal and tokens as K or M. Show unavailable values and uncertainty
explicitly; use “None” for an empty Running now table. Keep whole-range totals in the report even when
detail is sent as a file. Include loop summaries and individual agent rows with their role, parent,
duration, state and result; count distinct agents separately from their rounds. When per-item detail exceeds five items, send that detail in a self-contained
file using the harness's file-sending tool; if none is available, say so and provide the requested
detail inline. The file starts with the table or summary its detail supports.

| Running now | Duration | Last activity | State |
| --- | --- | --- | --- |
| Workflow or task | Elapsed | Timestamp or unavailable | Running activity and silence, if any |

| Timeline | Duration | Activity | Agents | Outcome |
| --- | --- | --- | --- | --- |
| Interval | Elapsed | Concurrent activity or unexplained interval | Roles | Result or uncertainty |

| Loops and subagents (parent) | Rounds | Agent count | Elapsed | Agent-minutes | State / outcome | Available tokens / tools | Repeat cause |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Workflow summary | Recorded IDs, labelled inference, or unavailable | Distinct descendants | Union | Summed subagent lifetimes | State and result | Fresh, cached and calls, or unavailable | Cause and outcome, or unknown |
| Agent role (parent role or main agent) | Recorded IDs, labelled inference, or unavailable | 1 | Observed lifetime | Same lifetime | State and result | Own usage, or unavailable | Cause and outcome, or unknown |

Summary and constituent rows describe the same work; never add their totals together.

| Scope overlap | Evidence | Purpose | Assessment |
| --- | --- | --- | --- |
| Assigned and observed scope | What records show | Review, handoff, research or implementation | Overlap or supported duplication, with uncertainty |

| Where time went | Duration | Classification | Evidence / uncertainty |
| --- | --- | --- | --- |
| Largest contributor | Elapsed | Necessary, rework, detour, avoidable or unknown | Basis and limitations |

Name agents by role or task, never IDs. Do not include raw transcripts or secrets.

## Guardrails

Read-only reporting: never launch agents or reviews, message, stop or resume agents, mutate records,
or repair work. Do not treat this report as authorization to do any of those things.
