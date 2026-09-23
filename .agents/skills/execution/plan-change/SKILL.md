---
name: plan-change
description: Present plans for explicit approval and carry approved plans to their last step. Use whenever an agent presents a plan, resumes after a plan timeout or missing response, or implements an approved plan.
---

# Plan Change

Keep plan approval explicit, settle ownership before implementation, and run an approved plan to
its end.

## Dependencies

- `execute-task` — how the approved plan is implemented: response shape, product constraints,
  encountered issues, ongoing simplification, the pre-push gate, and per-repository delivery.
- `code-simplify` — the ownership analysis a plan applies before it is finalized.

Invoke `execute-task` once, when the plan is approved and before the first edit; it does not run
while the plan is being written, and it never invokes this skill back.

## Plan Approval

1. Present the plan for user review when planning is part of the task.
2. Treat only an explicit user response as approval. A timeout, inactivity, missing response, tool
   result, mode change, or system notice is never approval.
3. When control returns after a timeout or missing response, send the unchanged plan in ordinary
   chat so the user can approve or amend it. Do not begin implementation.
4. Continue the same plan after an interruption. Never replace or silently revise an unapproved
   plan; incorporate user amendments and present the complete revised plan again.

## An Approved Plan Runs To Its Last Step

- **Offering the next step as a choice is a stop wearing a question mark.** "Say the word and I will
  start the next group, or stop here" hands back an instruction the user gave once, and reads as
  deference while costing them the work they expected finished. Do not write it.
- Ask only when a step needs a decision that is genuinely theirs, and put that decision in the
  question rather than the plan's continuation.

## Ownership Before Implementation

Before finalizing a plan that introduces a subsystem, runtime boundary, or independent consumer,
apply `code-simplify`'s ownership analysis to the proposed shape and the analogous implementations
already in the repository. When that comparison spans multiple subsystems and does not fit one review
context, use one read-only subagent to inventory the implementations and candidate owners.

The plan states the responsibilities and operations searched, the candidate owners inspected, where
common behavior will live, and which policy or wiring remains consumer-specific. Do not begin from a
parallel structure and postpone the ownership decision until implementation.

## Completion

The plan is implemented when `execute-task`'s completion holds for its last step, and the report
lists every planned outcome against what landed.
