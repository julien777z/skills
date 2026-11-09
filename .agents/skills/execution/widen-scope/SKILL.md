---
name: widen-scope
description: Let the current task also fix the slop and maintainability problems it runs into, not only bugs. Use only when the user asks for it in their own words, such as "widen scope" or "clean up what you find"; never on the agent's own initiative.
short_description: 'Let the current task also fix the problems it runs into, within a size budget.'
disable-model-invocation: true
---

# Widen Scope

By default a task fixes its own change and any bug it meets within `pre-production`'s size budget;
everything else it meets is deferred. This skill raises that limit for the current
task only, until it finishes or the user says to stop.

## Dependencies
- `acceptance-gate`
- `defer-scope`

## What It Allows

- Fix a problem the work runs into — a bug, duplicated logic, dead code, a misplaced helper, an
  abstraction with one implementation — when its fix touches about five files or fewer and needs no
  design decision from the user.
- Keep each fix in its own commit, named for what it repairs, so it can be reviewed or reverted on
  its own.
- Defer with `defer-scope` anything larger, anything that changes what the product does, and
  anything that would need its own plan.

## Judging Borderline Items

Collect the items you are unsure about rather than gating each one. Once the task's own change is
done, put that list to `acceptance-gate` in a single triage call; it decides fix or defer for each,
and its answer is final for this task.

## Output

Add one line to the task's report: `Widened scope: <n> fixed (<one clause each>) · <n> deferred
(<record links>)`.
