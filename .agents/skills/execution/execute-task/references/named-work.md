# Named work

What `SKILL.md`'s **Work You Have Already Named** applies to work the run has named, displaced or
is waiting on.

## Displaced Work

**A new request, an interruption, or a context summary cancels none of it**, and the work each one
displaces is named work whether or not a report named it: an approved plan short of its last entry,
commits a remote lacks, a checkout left mid-edit. The turn that serves the new request also moves
it — the user asking about something else is not the user withdrawing what they asked for before.

- **Write it down before anything else starts.** The displaced work is recorded as **Progress
  Record** says, with its next step, before the first step of whatever displaced it.
- **An interruption pauses the step in flight; it never ends the run.** After a follow-up finishes,
  mark the displaced work active again in the ledger and execute its saved next step without waiting
  for "continue". A promise to resume is not that step, and neither is a report that ends by naming
  what comes next: a turn that relays a worker's result, finishes a unit or answers a question
  starts the next named step before it ends, and every step that result unblocks, as **Progress
  Record** records them. A defect a turn finds while answering is handled in that turn as
  **Encountered Issues** says, one its own change made always fixed, and the answer reports it fixed
  or recorded; it never goes out as work the agent will do. Completing its own delivery — including
  a guidance merge and refresh, a diagnostic answer, or a local environment repair — does not
  complete the surrounding task. Report that intermediate result while continuing. A held item keeps
  its saved next action; repair, resolution and waiting follow **Waits And Awaited Results** below.
  End only when the task is verified complete or the user explicitly stops
  or hands it off. "Continue", or anything meaning it, resumes exactly the paused step and is never
  answered with nothing.
- **A context summary's pending list is this run's named work**, not background, **and its state is
  read from the record, never from the summary.** After a compaction or handoff, and before
  starting, delegating or reporting any plan work, read each step's state, and each decision or
  answered question whose work is open, from `session-ledger` and from the repository — merged
  commits, pushed heads — and let them overrule the summary: an item the record shows done is not
  started again, and one the summary left out is still owed. The first turn then moves the oldest
  item still open as well as whatever the summary's next step names. A constraint it carries, such
  as "ask before X", is an earlier turn's instruction, checked under **Encountered Issues** before
  it is obeyed.
- **Commits a remote lacks are undelivered work**; their next step is the pre-push checks and the
  push. A hook or status line counting unpushed commits whose checks pass reports a push owed now,
  not something to explain, apart from the commits the [pre-push gate](pre-push.md)'s one exception holds.

## The Unchanged Line

**The failure is a report, not a refusal.** It reads as diligence: the item appears under "still to
do", the turn ends, the next message arrives, and the item appears again, unchanged, in the next
report. Nothing was declined and nothing was done, and each repetition makes the next one easier,
because the item now looks like a standing note rather than work somebody is waiting for.

So the test is the item's own line. Before a report goes out, compare each outstanding item against
the line the last report carried for it. A line that has not changed means the item is finished in
this turn, before the report is sent, when **Priority** permits it; otherwise record the active
higher-priority task that holds it and its saved next action. Moving it a little or dropping it
from the list does not satisfy that obligation.

Each item's line records its current disposition:

- it is done;
- a named gate holds its dependent action — including an unanswered question or missing
  authorization — with its evidence, saved next action and live repair, resolution or wait route;
- it is no longer work, because the user withdrew it or a later request superseded it, said with
  that reason.

A held item remains outstanding; naming its gate or reporting it does not end the run. Withdrawal
or supersession removes only the work the user's instruction actually cancels.

**At the review-round limit, record the disposition as [review rounds](review-rounds.md) says.** If
the approved outcome still needs work, update the active plan and start the replacement's first
step **Priority** permits under the existing authorization, without another plan approval.

## Waits And Awaited Results

**A wait blocks only the work that depends on what is awaited.** While one item waits on something
outside the run's hands — a background agent, CI, a review, a build, a shared machine, device or
lock another session holds, the user's answer to one question or confirmation — start the
authorized, already-named work that **Priority** permits and that neither needs the awaited result
nor touches the files or resources the awaited work is changing.

- **Each item held for the wait names what it uses that only the awaited result will supply**;
  absent that dependency or a hold under **Priority**, it starts now: coming later in the plan,
  belonging to the same feature, or consuming a shape already agreed with the awaited work, such as
  a planned contract, is not such a thing, so build against that shape.
- **Every wait applies this test to the whole plan record** before the turn's report: to each step
  and part not yet started, in every later step as well as the current one, starting or delegating
  each that passes it.
- When the awaited work is a building worker, another edit starts only in an independently owned
  scope with separate files and resources, under `subagent-matrix`'s **Dispatch**; otherwise do
  read-only verification, review or question preparation while it runs.
- **Classify an awaited result from its observed state before treating it as a blocker.** Startup,
  recovery, a queued review or an unanswered request is pending until it has a terminal result;
  current unavailability, a quiet interval or a bounded wait yielding without a result is not
  failure.
- **A status report is not a stopping point.** A message sent while authorized work or a wait
  remains goes out together with the next wait or action, never as the turn's last output, and is
  never the task's report. When every remaining item depends on an awaited result, keep the
  available host wait or event route active until the result arrives, then resume its saved next
  action.
- An unresolved user choice holds its dependent work, not the whole run: it neither closes the run
  nor cancels independent work. A guidance correction is recorded and the run carries on; it is
  processed at **Completion**, never a reason to end or pause the surrounding task.
- **Report a blocker only on concrete evidence**: a terminal failure, exhausted recovery or a
  missing host wait route is a concrete gate to surface for repair or resolution, with its evidence
  and saved next action, while the task stays active.
