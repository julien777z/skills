---
name: widen-scope
description: Turn on, for the rest of the session, fixing the slop and maintainability problems the work runs into, not only bugs. Use only when the user asks for it in their own words, such as "widen scope" or "clean up what you find"; never on the agent's own initiative.
short_description: 'Turn on cleanup of the problems the work runs into for the rest of the session.'
disable-model-invocation: true
---

# Widen Scope

By default the work fixes its own change and every bug it meets, and defers cleanup past
`pre-production`'s size budget. This skill raises that cleanup limit as a session toggle: once the
user turns it on, it holds for every task and follow-up in the session until the user says to stop.
Record that it is on with `session-ledger`, and carry it into every task the session starts: a new
task's ledger copies the entry before the previous ledger is removed, a context summary or handoff
names it, and every worker brief states it. When the user stops it, record it as stopped the same
way, so no later task in the session picks it up again.

## Dependencies
- `acceptance-gate`
- `defer-scope`
- `pre-production`
- `session-ledger`

## What It Allows

- Fix a problem the work runs into — duplicated logic, dead code, a misplaced helper, an
  abstraction with one implementation — when its fix touches about five files or fewer and needs no
  design decision from the user. Bugs are always fixed, as `pre-production` says, whatever their
  size.
- Keep each fix in its own commit, named for what it repairs, so it can be reviewed or reverted on
  its own.
- Defer with `defer-scope` cleanup larger than that, cleanup that would change what the product
  does, and cleanup that would need its own plan. A defect's remedy is never deferred here: it keeps
  the planning and user-decision obligations `pre-production` and the global rules give it.

## Judging Borderline Items

Collect the items you are unsure about rather than gating each one. Once the task's own change is
done, put that list to `acceptance-gate` in a single triage call; it decides fix or defer for each,
and its answer is final for that item.

## Output

Add one line to the task's report: `Widened scope: <n> fixed (<one clause each>) · <n> deferred
(<record links>)`.
