---
name: council
description: Put a question, a review or a disputed finding to three strong models, from more than one provider, and return what each thinks; or review work with them in rounds, fixing what they find, until they agree. Use when the user says "council" or "use council", asks what several models think of something, or as a step that needs several models' independent read.
short_description: 'Ask three strong models what they think, or review with them in rounds until they agree.'
---

# Council

## Dependencies
- `subagent-matrix`
- `pre-production`

## Modes

- **Ask:** one round, and no edits. Use it when the user asks a question and wants the council's
  view, such as "what do you think of this approach? use council", and when an invocation hands
  the council a brief to answer: a review of a change, or a ruling on one disputed finding.
  Return each member's answer under **Output**; the asker decides what to do with it. A ruling is
  the majority of the three unless the asker sets another threshold, and a question that is a product, scope, security, disclosure or authorization choice
  is the user's: the council's answers go to them as advice. A ruling between more than two
  options, such as simplify, revert or accept, takes the option most members pick first; with no
  majority, the two leading options go to a vote among all three, and a tie there takes the
  option that changes least.
- **Loop:** the user asks the council to review or give feedback on work, such as "council this
  pull request". Run **Rounds**, fixing between them.

## Members

Use the members the user's instructions name. Otherwise take the three seats the `subagent-matrix`
skill's model capabilities reference lists under **Review panel**, each at its latest version on
the host and at high effort, and resolve each launch through that skill. Start the three in
parallel, read-only, each starting no subagents of its own.

- When a listed family is unreachable, fill its seat with the strongest other reachable model and
  say so in the result. A named member who is unavailable is reported, never replaced silently.
- **Brief:** a brief the invocation supplies is sent as it stands to every member. Otherwise give
  each the question or request, the intent, the material (a diff, files, a plan), and any check
  results. A review asks for findings, each with a file and line, rated `blocker` (the intended case
  is wrong), `should` (a real bug, an unsafe input or a workaround) or `nit`, and a score out of 10.
  A ruling asks for `fix` or `drop` with the reason.
- **Members keep their context between rounds.** In **Loop**, each member is started once and every
  later round is sent to that same member, carrying only the answers to its findings and what
  changed, so it re-reads nothing it already holds. A member that has ended or errored is replaced
  by a fresh one given the full brief and the ledger so far, and the result says so.

## Rounds

Before round 1, answer outstanding pull-request comments, fix known issues and run the relevant
checks, so the council reviews the current work. When the user wants to drop the implementation and
explore new ideas, skip fixes to code that is being replaced.

1. Send each member the brief and collect the replies. Summarise the useful findings, where members
   disagree, and the next steps.
2. Make the changes you agree with, and answer each finding: fixed, or declined with evidence. A
   finding outside the request is fixed when it fits `pre-production`'s size budget; the rest is
   listed in the result as left for recording.
3. Send the next round to the same members, with those answers and the diff since the last round.
   Each full review pass is one round.
4. Stop when every member is satisfied, or after three rounds. An open disagreement then is settled
   by the members' majority and listed with its ruling; one that is a product, scope, security, disclosure or authorization choice goes
   to the user.

## Harness Compatibility

- **T3 Code:** resolve the models with `orchestrator_capabilities`, and start each member with its
  own `delegate_task` (`role: "review"`). In **Loop**, send each later round to that member's own
  thread rather than starting a new task, so it keeps its context.
- **Claude Code:** start each member as a subagent, and send each later round to it with
  `SendMessage`.
- **Codex:** start each member as a subagent, and send each later round to that same agent.

## Output

**Ask** returns this to its asker, the user or the calling step:

```markdown
**Council:** <the question, in one line>

| Member | Answer |
| --- | --- |
| <model> | <its answer, verdict or ruling, with its reason> |

- **Agree on:** <points every member made, or none>
- **Split on:** <point: who holds which side, or none>
- **Findings:** <id [severity] file:line claim — members raising it, or not a review>
```

**Loop** puts this section in the pull request's description, before the model and harness line,
by editing the description rather than posting a comment; with no pull request, in the final reply.
Write `no score` for a member who gave none; never invent one.

```markdown
## Council review

Rounds: <n>

| Member | Round 1 | Round <n> |
| --- | --- | --- |
| <model> | <score>/10 | <score>/10 |
```
