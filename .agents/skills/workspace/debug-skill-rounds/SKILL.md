---
name: debug-skill-rounds
description: "Report in chat what this session's subagents and review rounds are doing: what is running now and the last five loops, each with its rounds, how long each subagent ran, the tokens it spent, how many subagents read each scope and where scopes overlap, so the user can see what is consuming time and usage. Use only when the user invokes it."
short_description: 'Show in chat which subagents and rounds are using time and tokens.'
disable-model-invocation: true
---

# Debug Skill Rounds

Tell the user, in chat, where this session's subagent time and tokens are going. It reads the
session's records and changes nothing.

## Gather

1. Run `python3 scripts/rounds.py` from this skill's folder. In Claude Code it finds the current
   session's transcript from `CLAUDE_CODE_SESSION_ID`; `--session <id>` reads another session and
   `--previous <n>` changes how many finished loops it returns, 5 by default. It prints JSON with:
   - `running` and `previous`: loops, the most recent first. A loop is a stretch of subagent work
     with no pause longer than 10 minutes, and `skills` names the skills invoked during it.
   - `rounds`: the subagents of a loop launched within 90 seconds of each other.
   - per subagent: its `state` — `running`, `finished`, or `stopped` when it never finished and has
     been silent for over 10 minutes — its start, last activity, seconds, `fresh_tokens`,
     `cached_tokens` (cache reads), tool uses and `scope`.
   - per loop: totals, `per_scope` (how many subagents named each path) and `overlapping_scope`
     (paths more than one subagent named).
2. On a harness whose transcript the script cannot read, such as Codex, gather the same facts from
   the session's own record of the subagents it launched — each one's role, description, start,
   end and brief — and say in the report which numbers that record does not hold.
3. Treat `scope` as a starting point. It lists the paths each subagent's brief names; drop an entry
   that is not a file or folder, and add a path the brief names that it missed.

## Report

Write it in chat, with these headings in this order, so what is running never mixes with what has
finished:

- **Running now**: "None" when nothing runs. Otherwise each running loop: its skills and how long it
  has run, then each round by number with one line per subagent — its role and description, its
  state, how long it has run, its fresh tokens and its scope.
- **Previous loops**: the last five finished loops, the most recent first, each as a short block:
  its skills, when it started and how long it ran, how many rounds and subagents, fresh and cached
  tokens, its longest subagent, each scope more than one subagent read with how many, and any
  overlapping scope.
- **Where the usage went**: at most five lines across both, ranking what cost the most by time and
  by fresh tokens — a subagent, a round that repeated, a scope read several times — each saying
  what it was and its numbers, such as "Final acceptance of the skills PR: 15.2 min, 1.05M fresh
  tokens, the longest subagent".

Show durations in minutes to one decimal and tokens as K or M. Never show agent ids or quote a
subagent's transcript; name a subagent by its description.

## Guardrails

- Read only: never stop, resume or message a subagent, and never change the session's records.
