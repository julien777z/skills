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
investigating, editing, committing and pushing a fix, with the fast checks a push needs. A guidance
edit is the usual case: it is written, committed and pushed to its draft pull request and installed
as usual, while its review, skill test and merge wait in the queue. That is the pause working as
meant, so it raises no question; **Asking While Paused** applies only when the user asks to finish,
merge or resume something.

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

- **Answers explain more than usual.** The user paused because they noticed a problem, so each
  answer about the work traces what led to it: the step or agent that made the decision, the
  guidance or input it acted on, and the evidence for each link, before what to change. A short
  answer that names only the outcome leaves them without what they paused to see. This lasts only
  while the pause is open: once every gate resumes, answers return to their usual length, and
  resuming gates for one scope leaves it on.

- **The pause holds until the user resumes it**, through **Asking While Paused** below, by asking
  to resume the gates, or in their own words. A context summary, a new message, a finished fix, a
  notification or a schedule never lifts it, and no reply asks whether to resume.
- **The pause covers every scope except those resumed one at a time.** The `hold` entry lists each
  resumed scope, a pull request or the task's execution; that scope's reviews, gates, checks and
  workers run as normal while everything else stays paused.
- **Before any launch, read the ledger for an open `hold`.** A review, gate, worker or check run
  in a scope it still covers is not started; it is added to the entry's queue instead.
- **Named work stays named, not resumed.** Work the agent already said it would do is recorded in
  the entry and waits; the pause outranks any rule that resumes it without being asked.
- Corrections and decisions made during the pause are recorded as usual, so the resumed work can
  act on them.

## Asking While Paused

When the user asks for work the pause still covers, such as finishing or merging a pull request or
resuming the task's execution, ask through the question tool before starting it, naming the work
and when the pause started. A request already asked about in this run is not asked again.

- **Resume all gates**, listed first and recommended, since the user most often wants everything
  back: lifts the whole pause, as resuming the gates does.
- **Resume gates for this only**, offered only when the request covers one scope, one pull request
  or the task's execution: adds that scope to the entry's resumed scopes, and the work runs with its
  reviews, gates, checks and workers while every other scope stays paused.
- **Continue with gates paused**: the work runs, what the pause covers stays queued, and a merge
  goes ahead without those reviews, its report saying the gates were paused.
- **Stop**: nothing runs, and the reply says that asking to resume the gates restarts everything.

A request covering several pull requests or every scope has no "for this only" option, since it is
already everything.
