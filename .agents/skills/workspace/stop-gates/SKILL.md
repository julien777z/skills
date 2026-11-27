---
name: stop-gates
description: Pause every review, gate, check run and worker in the current session, so the user and agent can correct a problem before any of them goes on, and keep the pause in force until the user resumes it. Use when the user asks to stop or hold the gates, reviews, checks or workers. Run only when the user asks for it.
short_description: 'Pause every review, gate, check run and worker until the user resumes them.'
---

# Stop Gates

The user has seen something they want corrected before more work runs on top of it. Stop the
automated work now, keep everything needed to restart it, and work with the user on the problem.

## Dependencies

- `session-ledger`

## What Stops

Everything the session runs on its own, so nothing builds on the state being corrected:

- reviews, acceptance gates, council rounds, skill-test readers and security audits;
- implementation and fix workers, and any coordinator running them;
- slow verification: test suites, browser walkthroughs, anything needing a running stack;
- merge gates, guidance delivery and ledger processing.

Conversation with the user does not stop, and neither does the work they ask for during the pause:
investigating, editing, committing and pushing a fix, with the fast checks a push needs.

## Procedure

1. **Stop each running item.** Tell each worker to push what it has and stop, then end it; cancel
   each running review, gate and check run. Never discard a worker's unpushed work: wait for its
   push or copy its worktree's changes to the task's working-files folder first.
2. **Record the pause** in the task ledger through `session-ledger`, as a `hold` entry: when it
   started, the user's words, and one line per stopped or queued item with its pull request or
   scope, head, stage reached, brief location and next action, so the resume can restart each
   from where it stopped. A result that arrives after the stop is kept in the entry and not acted on.
3. **Report it**: one line per item stopped, then answer what the user raised.

## While Paused

- **The pause holds until the user resumes it**, by asking to resume the gates or in their own words. A
  context summary, a new message, a finished fix, a notification or a schedule never lifts it, and
  no reply asks whether to resume.
- **Before any launch, read the ledger for an open `hold`.** A review, gate, worker or check run
  it covers is not started; it is added to the entry's queue instead.
- Corrections and decisions made during the pause are recorded as usual, so the resumed work can
  act on them.
