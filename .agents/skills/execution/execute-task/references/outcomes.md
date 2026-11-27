# Reported outcomes

What `SKILL.md`'s **Pre-Push Gate And Reported Outcomes** applies before a result is reported or
built on.

- **After any action that changes shared state, read the resulting state before reporting it or
  starting the next item.** A push, merge, deployment, migration, or refresh reports that it ran,
  not the state it left, so read that state where it lives.
  - After a push, that is the pull request on the pushed head, or, before one exists, the remote
    branch head: its mergeable state and the checks that run for its state starting — a draft
    starts no test jobs — since the base can move while the push runs.
  - A status sent to the user states what was just read and where, never what was reported or
    expected: conflicted, failing, running, or passing, on the head or target named, with "done",
    "ready", a merge step or a review hand-off written only once that read says so and nothing this
    run started still changes it, the report otherwise saying it is still changing; a file sent
    with it is read whole first, as `share-media`'s **What reaches the user, and when** requires.
  - A milestone report, gate classification or final response reads the authorized outcome's state
    and owning diagnostics the same way and reconciles every required step with the task record: a
    successful substep does not establish the parent outcome, and its saved next action resumes
    while that outcome is unmet.
- **Whatever that read shows wrong is the next thing done**, ahead of every queued item, and is
  never carried to "the next push" or bundled behind other work. A conflict is brought in through
  `merge-conflict`, delivered under the GitHub rule's **Pre-Push Gate**, and read back. A base that
  only moved, with no conflict, is brought in once, by `review-pass` at the selected workflow's
  completion, before the final acceptance.
- **A delegated worker's report of an outcome is a claim, never evidence.** Before relaying it or
  building on it, check it at its source: "tests pass" against the run or the CI result on that
  commit, "pushed" or "exists" against the branch, "merged" or "refreshed" against the default
  branch or the installed copy, "deployed" or "healthy" against the host, "fixed" by reproducing it
  or reading the evidence, "the screenshot shows it" by looking at the image, "no references
  remain" by searching. A claim the check contradicts is handled as the bullet above orders: sent
  back to the worker with what the read showed, or fixed here.
- **What a worker reports leaving alone is classified before it reaches the user.** Read each item
  against `scope-of-change`'s **Scope Follows The Defect, Not The Request** bullets: a defect, code
  the pull request wrote, a parallel copy of the change's own mechanism or a shape a standing rule
  names goes back to the worker or is fixed here; other cleanup is done or placed as the size budget
  says, an item that budget reserves a record for goes to a record with `defer-scope`, and only a
  recorded one and an item those bullets leave to the user are reported, as what it is and never as
  a question whether to fix it.
- **A cause stated to the user is traced first, whether or not they asked for it**: a root cause,
  and any explanation the agent offers of why something failed, why a value is what it is, or why a
  check, test, gate or review let something through.
  - Follow the operation from its entry point to the component that produced the outcome, reading
    the code or configuration that decides it, such as how a check selects what it checks, and
    verify that the cause explains the observation through direct evidence or a controlled
    reproduction. A cause read from a component's name, a remembered list or what seems likely is
    not stated as the cause.
  - Track causal diagnosis separately from mitigation, restoration, and regression coverage. If the
    failure stops reproducing, inspect retained diagnostics and compare the failed and recovered
    runtimes.
  - Before reporting a hold, exhaust available safe diagnostic and reproduction paths. Name the
    missing evidence, why it is unavailable, and the specific observation or external action that
    can resume the investigation.
