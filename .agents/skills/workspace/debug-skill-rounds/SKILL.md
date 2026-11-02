---
name: debug-skill-rounds
description: "Report in chat what this session's subagents and review rounds are doing: what is running now and the last five loops, each with its rounds, how long each subagent ran, the tokens it spent, how many subagents read each scope and where scopes overlap, so the user can see what is consuming time and usage. Use only when the user invokes it."
short_description: 'Show in chat which subagents and rounds are using time and tokens.'
disable-model-invocation: true
---

# Debug Skill Rounds

Tell the user, in chat, where this session's subagent time and tokens are going. It reads the
session's own records and changes nothing.

## Gather

Read the session's record of the subagents it has launched, wherever the harness keeps it: its
transcript, its task or agent list, and each subagent's own record. For every subagent, take:

- its role and the description it was launched with;
- the skill whose run launched it, and the step or round it belongs to;
- when it started and when it last did anything;
- its state: running, finished, or stopped when it never finished and has been silent for over 10
  minutes;
- the tokens it spent, fresh and cached apart when the record separates them, and its tool calls;
- its scope: the files and folders its brief told it to read.

Group them for the report:

- **A loop** is one skill's run of subagents, or, where the record does not say which skill started
  one, a stretch of subagent work with no pause longer than 10 minutes, named for the skills
  invoked during it.
- **A round** is the subagents a loop launched together, or a repeat the skill ran, such as a
  second review after a repair.

A fact the record does not hold is reported as missing, never estimated.

## Report

Write it in chat, with these headings in this order, so what is running never mixes with what has
finished:

- **Running now**: "None" when nothing runs. Otherwise each running loop: its skills and how long it
  has run, then each round by number with one line per subagent — its role and description, its
  state, how long it has run, its fresh tokens and its scope.
- **Previous loops**: the last five finished loops, the most recent first, each as a short block:
  its skills, when it started and how long it ran, how many rounds and subagents, its tokens, its
  longest subagent, each scope more than one subagent read with how many, and any overlapping scope.
- **Where the usage went**: at most five lines across both, ranking what cost the most by time and
  by tokens — a subagent, a round that repeated, a scope read several times — each saying what it
  was and its numbers, such as "Final acceptance of the skills PR: 15.2 min, 1.05M fresh tokens,
  the longest subagent".

Show durations in minutes to one decimal and tokens as K or M. Never show agent ids or quote a
subagent's transcript; name a subagent by its description.

## Guardrails

- Read only: never stop, resume or message a subagent, and never change the session's records.
