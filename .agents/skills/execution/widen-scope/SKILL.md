---
name: widen-scope
description: Turn on, for the rest of the session, fixing the slop and maintainability problems the work runs into, not only bugs. Use only when the user asks for it in their own words, such as "widen scope" or "clean up what you find"; never on the agent's own initiative.
short_description: 'Turn on cleanup of the problems the work runs into for the rest of the session.'
disable-model-invocation: true
---

# Widen Scope

This skill switches on `pre-production`'s widened cleanup budget as a session toggle: once the user
turns it on, it holds for every task and follow-up in the session until the user says to stop. Bugs
are fixed whatever their size either way, as `pre-production` says.

## Dependencies
- `acceptance-gate`
- `pre-production`
- `session-ledger`

## Switching It On And Off

- Record it with `session-ledger` as a decision the user scoped to the whole session, so it reaches
  every later task, context summary, handoff and worker brief.
- When the user stops it, record the stop the same way.

## Judging Borderline Items

Collect the items you are unsure about rather than gating each one. Once the task's own change is
done, put that list to `acceptance-gate` in a single triage call; it decides fix or defer for each,
and its answer is final for that item.

## Output

Add one line to the task's report: `Widened scope: <n> fixed (<one clause each>) · <n> deferred
(<record links>)`.
