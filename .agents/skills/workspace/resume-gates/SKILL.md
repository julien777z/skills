---
name: resume-gates
description: Lift a stop-gates pause and restart every review, gate, check run and worker it stopped, plus the task the agent was doing, all acting on what the user and agent changed or agreed during the pause. Lists for the user what the restarted work will do differently, and asks whether to open a pull request first when an agreed guidance change is on none. Use when the user asks to resume the gates, reviews, checks or workers. Run only when the user asks for it.
short_description: 'Restart the paused gates, checks and workers on the corrected state.'
---

# Resume Gates

Restart the work stop-gates paused, so it runs on what the pause corrected, not on what it was
stopped from building on.

## Dependencies

- `session-ledger`
- `subagent-matrix`
- `update-skills`
- `execute-task`

## Procedure

1. **Read the pause.** Load the open `hold` entry from the task ledger through `session-ledger`,
   its stopped and queued items, and every correction, decision and push recorded since it
   started. Read the conversation since the stop for what the user and agent agreed that the
   ledger does not yet hold, and record it. With no open `hold`, the items to restart are the
   reviews, gates, checks and workers the user's words or the ledger show stopped.
2. **Work out what changed for each item**: a new head to judge, guidance it now runs under, a
   scope cut or added, a finding already fixed, an item no longer needed. A verdict from before the
   stop on a head or guidance that has since changed is stale and is not reused.
3. **Put agreed guidance changes where the restarted work can read them.**
   - Committed on a pull request but not yet installed: run `update-skills`, so every launched
     agent loads them.
   - Agreed but on no pull request: ask the user through the question tool whether to open one
     before resuming, recommending that. Without one, the restarted work carries each change in
     its brief, quoted with the installed text it amends, from the ledger, never from a harness's
     memory.
4. **Tell the user what resumes differently**: a short list, one line per item whose restarted run
   changes, such as "acceptance gate on the guidance pull request now judges the new head, with the
   shorter matrix skill". Omit items that restart unchanged, and the list when none change.
5. **Restart everything** in its original order: each review, gate and reader as a fresh launch
   through `subagent-matrix`, never a resumed one; each worker as a fresh worker on its branch,
   with its brief updated by step 2; each check run on the current head. Resume the task the agent
   was doing at its saved step through `execute-task`.
6. **Close the pause**: mark the `hold` entry resumed, with the time and what was restarted.
