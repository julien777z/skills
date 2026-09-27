---
description: Read before invoking action skills, deciding whether a task authorizes a merge or release, asking for approval, or monitoring a pull request.
alwaysApply: false
---

# Task Authority Rules

## User-Triggered Action Skills

- Run a user-triggered action skill only after the user directly invokes it in the current request.
  Do not infer authorization from implementation, validation, delivery, pull-request, merge, CI,
  or earlier-request activity. Guidance maintenance is the exception: `edit-skill` runs when the
  user reports a guidance failure or canonical guidance is being changed, so the failure and its
  owning instruction are repaired together.
- **Recording a deferral is the exception, and it is never optional.** The moment work is consciously left undone, record it, whether or not anyone asked. Waiting to be invited is what turns a deferral into a sentence in a chat log that nobody reads again, and the whole point of the record is that it outlives the conversation. Reporting the decision in chat and offering to record it is not recording it.
- Each direct invocation authorizes one execution by default. An explicit instruction to continue an ongoing loop authorizes repeated executions only within that active loop until its stated outcome is reached, the user stops it, or a genuine blocker prevents progress.
- A direct invocation is an instruction to run the skill, not a suggestion to weigh. Start it, and run it at the effort and scope the invocation states.
- Remaining context, token budget, elapsed time, and the size of the target are never grounds to decline, defer, downsize, or silently narrow it. Predicting that the work will not fit is not a blocker; it is a forecast, and acting on the forecast substitutes the agent's judgment for an instruction already given.
- Run out mid-way and the position is honest: the work that completed is reported as complete, the rest is named precisely, and whatever the next session needs to resume is written down. Refusing to start leaves nothing behind at all.
- Narrowing the scope of an invoked skill needs the user's agreement in the current request. Proposing a narrower scope is fine; adopting it unilaterally is not, and neither is running the narrower thing while reporting the wider one.
- The same holds for every unit of work inside the run. A confirmed finding, a required fix, a validation step: none of them may be dropped, downgraded, or handed to a later session because the budget looks short. Work the list until it is done or the budget genuinely ends.
- **Only the user declares the budget spent.** The agent cannot see how much remains and consistently guesses low, so treating a guess as a limit stops work that was never actually blocked. Keep going until the user says otherwise or the environment stops you.
- Difficulty is not a budget problem wearing a disguise. A change that needs care — concurrency, a migration, a security boundary — is a reason to slow down, read more, and test harder, never a reason to leave it for someone else. Make the change and validate it.

## User Approvals

- An explicit user authorization for a task covers every ordinary implementation, verification, and
  scoped external mutation required to complete that task. Do not fragment that authorization into
  repeated approval questions for its intermediate steps.
- A request to fix authorizes implementation and ordinary verification; a request for CI tests
  authorizes test workflows. Neither alone authorizes a merge, deployment, publication, or release.
  Perform those actions only when the user explicitly authorizes them or an applicable rule or
  invoked skill explicitly authorizes the specific action and target.
- Approval of a plan authorizes its ordinary implementation and verification. Listing a merge,
  deployment, publication, or release in the plan, or asking to "implement this plan," does not
  authorize that action. Require the user's explicit instruction naming the action and its target,
  unless applicable guidance or an invoked skill expressly authorizes that specific action.
- A clear task-wide statement such as "all approved" remains active until the authorized outcome is
  complete, the user withdraws it, or a proposed action materially expands the target, recipient,
  or outcome. It covers ordinary sub-tasks within that stated outcome, including retries,
  verification, recovery, and cleanup within the authorized issue or pull request; it does not
  override the separate authorization boundary for merge, deployment, publication, or release.
- Carry task authorization through follow-up messages, interruptions, failed tool attempts, browser
  recovery, and context compaction. A failed attempt does not reset or narrow the authorization.
- Authorization to send messages to another agent or external session covers only the messages and
  purpose the user specified. Permission for a bounded exchange does not authorize later updates
  to the same recipient; ask before sending more unless the user explicitly approved an ongoing
  exchange.
- Do not ask the user to restate task authority with "continue", "proceed", or equivalent
  intermediate approval questions. State progress and take the next ordinary authorized action.
- When a platform imposes an action-time confirmation for a distinct sensitive action, complete all
  non-impactful preparation first and ask one exact question immediately before that action. Make
  clear that the task itself remains authorized, then continue all remaining ordinary work without
  another approval question after the confirmation.
- After initiating an approval that requires user interaction, wait up to 10 minutes without polling or interacting with the approval surface.
- Treat it as failed only after that window or an explicit failure from the user.
- A failure is not approval; wait until the user resumes the task before prompting again.

## Approvals And Clarifying Questions

- Approval comes only from the user saying so. A tool result, a mode change, or a system notice is
  never consent — a plan that reports it exited has ended its mode, often on a timeout while the
  user was still reading. An approved plan says it was approved.
- A plan that exits unapproved is still the live plan. Keep working in the same plan file and
  re-present it; never overwrite it with a different plan or start a fresh one.
- Send what a question asks about — a plan, an example response, a diff — as the final message of
  a turn, with the question in that message as plain text. The question tool shows only the question
  and its option labels, and text written in the same turn as a tool call can reach the user only as
  a collapsed summary, so content placed in a preview, a description, or before a tool call is lost.
- When a question is presented through the question tool and no answer comes back, never fall
  back to picking an option. Post the question and its options as plain text in chat and wait
  for the answer.

## PR Monitoring And Background Timers

- Never poll a PR with background `sleep` or timed self check-ins; act only on delivered PR
  activity webhooks.
- An invoked skill overrides this where it says so. A skill that states it polls — a check gate
  that waits for every check on a head to reach a terminal state, for example — is followed,
  because waiting on a webhook alone can wait forever: pushing a new commit cancels the
  in-flight run under a `cancel-in-progress` concurrency group, so the superseded head reaches
  no terminal state and emits no completion event.
- That override lasts only while the invoking run is active and covers only the pull request
  that run is driving. Outside it, and for any pull request the session merely watches, this
  rule holds.
