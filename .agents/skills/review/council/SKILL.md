---
name: council
description: Put a question, a review or a disputed finding to three independent reviewers and return what each thinks; or review work with them in rounds, fixing what they find, until they agree. Use when the user says "council" or "use council", asks what several models think of something, or as a step that needs several models' independent read.
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
  the majority of the members, normally three, unless the asker sets another threshold, and a question that is a product, scope, security, disclosure or authorization choice
  is the user's: the council's answers go to them as advice. A ruling between more than two
  options, such as simplify, revert or accept, takes the option most members pick first; a
  three-way split takes the option the asker lists first. A ruling never accepts a confirmed
  defect, an exploitable vulnerability or a failing required check.
- **Loop:** the user asks the council to review or give feedback on work, such as "council this
  pull request". Run **Rounds**, fixing between them.

## Members

Use the members the user names. For an unnamed panel on a provider required by the calling
skill, dispatch three independent reviewers at the advanced tier on that provider. When
neither the user nor the calling skill sets the selection, use the three seats listed under
**Review panel** in the `subagent-matrix` model capabilities reference. Resolve each launch
through that skill at high effort. Start the three in parallel, read-only, with no subagents
of their own.

- **A default seat whose launch on another provider does not start** is relaunched on the
  session's own provider at the seat's level, as `subagent-matrix`'s **Workflow** says, and the
  result names the substitution; the seat is never left empty or waited on for that provider.
- **Missing members.** Resolve an unavailable default seat through `subagent-matrix` down to
  the `standard` tier. Report a missing named or caller-constrained member and use only launches
  that meet the original requirement. With two members available, name the empty seat and report
  that the ruling came from two members. Two who agree decide. On a split, use the option the
  asker lists first, as for a three-way split. With fewer than two available, report the panel as
  incomplete and return no ruling. Distinguish members by seat when model names repeat.
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

Before round 1, triage outstanding pull-request comments and fix what they raise, posting nothing
the user did not ask for, fix known issues and run the relevant checks, so the council reviews the current work. When the user wants to drop the implementation and
explore new ideas, skip fixes to code that is being replaced.

1. Send each member the brief and collect the replies. Summarize the useful findings, where members
   disagree, and the next steps.
2. Make the changes you agree with, and answer each finding: fixed, or declined with evidence. A
   defect outside the request is fixed where `pre-production` places it. Apply that skill's size
   budget to cleanup and list deferred work for recording.
3. Send the next round to the same members, with those answers and the diff since the last round.
   Each full review pass is one round.
4. Stop when every member is satisfied, or after three rounds. An open disagreement then is settled
   by the members' majority, within the limit **Ask** sets on what a ruling accepts, and listed
   with its ruling; one that is a product, scope, security, disclosure or authorization choice goes
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
