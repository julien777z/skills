---
name: stop-gates
description: Pause all of the current session's work on its task — the agent's own implementation, every worker, review, gate and check run — so the user and agent can correct a problem before any of it goes on, and keep the pause in force until the user resumes it. Use when the user asks to stop or hold the gates, reviews, checks, workers or the task. Run only when the user asks for it.
short_description: 'Pause the task, its workers, reviews, gates and checks until the user resumes them.'
---

# Stop Gates

The user has seen something they want corrected before more work runs on top of it. Pause
everything at once, keep what is needed to restart it, and work with the user on the problem.

## Dependencies

- `session-ledger`

## What Stops

Everything the session does on its task, so nothing builds on the state being corrected:

- the task's own implementation, in the main session as much as in workers: the edit in hand is
  committed and pushed as it stands, and nothing further is built;
- reviews, acceptance gates, council rounds, skill-test readers and security audits;
- implementation and fix workers, and any coordinator running them;
- slow verification: test suites, browser walkthroughs, anything needing a running stack;
- merge gates, guidance delivery and ledger processing.

Conversation with the user does not stop, and neither does the work they ask for during the pause:
investigating, editing, committing and pushing a fix, with the fast checks a push needs.

## Procedure

1. **Stop each running item.** Stop your own work on the task at the next point it can be
   committed, and push it. Tell each worker to push what it has and stop, then end it; cancel
   each running review, gate and check run. Never discard a worker's unpushed work: wait for its
   push or copy its worktree's changes to the task's working-files folder first.
2. **Record the pause** in the task ledger through `session-ledger`, as a `hold` entry whose open
   state is the session's gates-off flag, read before every launch and every merge: when it
   started, the user's words, the task's saved step, and one line per stopped or queued item with its pull request or
   scope, head, stage reached, brief location and next action, so the resume can restart each
   from where it stopped. A result that arrives after the stop is kept in the entry and not acted on.
3. **Report it**: one line per item stopped, then answer what the user raised.

## While Paused

- **The pause holds until the user resumes it**, by asking to resume the gates or in their own words. A
  context summary, a new message, a finished fix, a notification or a schedule never lifts it, and
  no reply asks whether to resume.
- **Before any launch, read the ledger for an open `hold`.** A review, gate, worker or check run
  it covers is not started; it is added to the entry's queue instead.
- **Named work stays named, not resumed.** Work the agent already said it would do is recorded in
  the entry and waits; the pause outranks any rule that resumes it without being asked.
- **Resuming the task asks first.** When the user asks to resume the task's execution with the
  hold open, confirm that resuming with gates paused is intentional before continuing it.
- **A merge asks first.** With the hold open, a merge, even one the user authorized, waits for
  the user to confirm that merging with gates paused is intentional.
- Corrections and decisions made during the pause are recorded as usual, so the resumed work can
  act on them.
