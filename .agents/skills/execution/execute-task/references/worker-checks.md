# Worker checks

How `SKILL.md`'s **Assigning Work** keeps watch over each worker the session starts while it runs:
whether it is alive, whether what it makes looks right, and whether its pull requests follow the
branch rules.

**A running worker is never assumed healthy until it reports.** Each worker the session started is
checked on a schedule that backs off from its launch, since most stalls happen right at the start.
This is the user's standing instruction and holds over a harness default against polling a delegate.

- **Schedule:** 10 seconds, 30 seconds and 5 minutes after it starts, then every 30 minutes while
  it runs. A short background timer or the host's scheduler, such as a recurring scheduled
  prompt, sets it, and a worker's checks end when it finishes. Each check ends by re-arming the
  next: it confirms the timer is still scheduled and sets it again when it is gone. A session-only
  timer can lapse across a restart, compaction or handoff without firing, so the first turn after
  one confirms and re-arms it the same way while a worker runs. The scheduled check is removed
  once no worker runs.
- **Reading:** each check reads the worker's latest activity from whatever the host exposes for
  it: its thread items, the files it writes, the processes or background tasks it runs. A worker
  whose host shows nothing until it finishes is judged by those other signals before it is
  cancelled, never by the empty thread alone.
- **Look-over:** each 30-minute check also looks at what the worker produced since the last
  one: its commits, its reported progress and every capture or other media it made that the
  coordinator has not already read, each read whole, compared with its brief and the design it
  carries. The early checks only read liveness. The look-over is a coordinator's quick read,
  never a review pass, a gate, or a request that the worker record or test more, since its own
  workflow runs those. Something wrong, odd or unclear goes to the worker as a queued question or
  a request to look into it, and its answer is read when it arrives.
- **Pull-request spot check:** each 30-minute check also lists, from the host, the open pull
  requests in every repository the session's workers push to. It compares them with the
  session's own creation receipts and its workers' briefs, never with the ledger alone. A pull
  request a worker opened carries no receipt, and the comparison is how the coordinator sees one.
  It spot-checks the session's pull requests against the GitHub rule's **Branches and Pull
  Requests**. Each repository should have at most one open agent-configuration pull request for
  the session.
  No branch should mix guidance and source. No pull request should be outside its brief, and none
  should be another session's pull request carrying the session's commits. A miss goes to the
  running worker that made it, or the coordinator fixes its own, with the consolidation that rule
  requires. Like the look-over, this is a quick read, never a review pass.
- **Finished:** a worker has finished once it reports its task done, even while its thread stays
  open waiting on a review or a reply, as much as when the host shows it ended. It has its result
  checked as [reported outcomes](outcomes.md) says, its captures held to its brief and design as
  the look-over holds them, and its pull requests spot-checked, before its result is relayed. A miss it left goes to a fresh worker as
  `subagent-matrix`'s **Dispatch** says for a follow-up, never back to the finished one.
- **Rate-limited:** a worker a rate limit or quota stopped is not stalled. It is resumed at once
  as `subagent-matrix`'s capacity rule says for a running worker, never scheduled for the reset
  time the refusal names.
- **Stalled:** at an early check, one with no activity at all since launch, or whose last step
  failed and nothing followed. At a later check, one with no activity for 30 minutes, counted
  from its last activity and not before, unless a long command of its own is in progress;
  waiting on anything else does not excuse it.
- **Response:** a stalled worker is cancelled and relaunched, through `subagent-matrix`'s
  **Dispatch**, with its brief plus what stalled it, such as a failed command it never
  recovered from, input it waits on that nobody sees, or a provider error it never reported. One
  that finished without its completion arriving has its result collected.
- **Scope:** the check is scheduled for workers only. Its pull-request spot check reads pull
  requests without waiting on any; a pull request is still waited on as `merge-gate`'s **Pull
  Request Activity** says. A question put to the user is not a worker.
