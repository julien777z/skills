---
description: Rules that hold in every repository, regardless of its stack or conventions.
alwaysApply: true
---

# Global Rules

## Agent And Harness Portability

- This guidance is used with multiple models and agent harnesses. Prefer one provider-neutral
  implementation and one canonical source for skills, rules, and agent prompts.
- When a shared implementation is not possible, support both Claude and Codex explicitly: account
  for how each discovers, installs, and uses the guidance, and verify both paths. Include other
  supported harnesses where the same change reaches them.
- Read the other shared rules relevant to the current repository and task. If a harness does not
  load them automatically, open the applicable files from its user-level rules directory.

## Repository Skills

- Never add `agents/openai.yaml` to a repository skill. Repository skills contain `SKILL.md` and
  only supporting files required by the skill; provider UI metadata stays outside repositories
  and is never propagated.

## Agent Prompts

- In repositories that provide an agent CLI or otherwise interact with agents, store every agent prompt in a dedicated Markdown file rather than inline in application code so it is easy to find, review, and maintain. Application code may load a prompt file and interpolate runtime values into it.

## Generated Agent Outputs

- Never stage generated provider output manually. Only the repository's Agent Sync workflow may generate and commit provider mirrors.

## Source References

- Reference external code and automation by a maintained version tag when available, or by a
  maintained branch while developing or when no release tag exists. Do not pin dependency manifests,
  shared checkouts, or workflow references to commit hashes. Lockfiles and release records may retain
  the exact resolved commit for reproducibility and provenance.

## Credential Names

- Name persistent API keys and other credentials for their durable role or consumer, such as
  `CI tests` or `Backend API`. Avoid a single test case, experiment, or creation date in the name.
- Reuse or rotate the credential that owns that role. Do not create a second key merely to validate
  a new key or retry setup; first check whether the intended key already exists.
- Express expiry through the provider's expiry setting or an explicit rotation record, not through
  the credential's name.

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
- A clear task-wide statement such as "all approved" remains active until the authorized outcome is
  complete, the user withdraws it, or a proposed action materially expands the target, recipient,
  or outcome. It covers every foreseeable sub-task within that stated outcome, including retries,
  verification, recovery, and cleanup within the authorized issue or pull request.
- Carry task authorization through follow-up messages, interruptions, failed tool attempts, browser
  recovery, and context compaction. A failed attempt does not reset or narrow the authorization.
- Do not ask the user to restate task authority with "continue", "proceed", or equivalent
  intermediate approval questions. State progress and take the next ordinary authorized action.
- When a platform imposes an action-time confirmation for a distinct sensitive action, complete all
  non-impactful preparation first and ask one exact question immediately before that action. Make
  clear that the task itself remains authorized, then continue all remaining ordinary work without
  another approval question after the confirmation.
- After initiating an approval that requires user interaction, wait up to 10 minutes without polling or interacting with the approval surface.
- Treat it as failed only after that window or an explicit failure from the user.
- A failure is not approval; wait until the user resumes the task before prompting again.

## Computer-Use Surface Failures

- Treat an inventory or availability error as scoped to the surface it names. A native-app lock or failure does not block browser automation, and a browser failure does not block terminal or API work.
- Before reporting a task blocked by a surface warning, inspect the requested surface directly and retry its normal recovery path. For a browser, refresh the tab inventory and reopen an authenticated task tab when the prior agent-owned tab has closed.
- Prefer an isolated agent-owned browser tab. When the user explicitly directs use of an existing
  browser tab or window for the current task, that instruction overrides the isolation preference;
  use only the authorized surface and leave every other user-owned surface untouched.
- Report a block only when the requested surface itself cannot complete the next required action and safe alternatives have been exhausted.

## Live Deployment Validation

- Treat create, update, and delete requests against a live deployment as data mutations, not health
  checks. Run them only against a target that the repository explicitly designates for mutation
  testing; when no such target exists, live smoke testing is read-only.
- When the same artifact and materially equivalent configuration run in several environments, one
  successful write test on the designated mutation target plus read-only health and routing checks
  on the others validates the shared path. Never create persistent synthetic records in a stable or
  shared staging environment merely to smoke-test a deployment.

## Repository Independence

- Every repository stands on its own. Never carry another repository's domain vocabulary into this
  one: its product name, its services, its table and column names, its record types, or the nouns
  its business speaks in. That holds for source, tests, fixtures, examples, and documentation
  alike, and it holds most strongly in a library, where every reader is a different consumer.
- Name things for the shape being exercised, not for whichever caller happened to prompt the work.
  A test needing a table with a secret column names it for that — a record with a secret — rather
  than borrowing the one real table the change was made for.
- Sample values follow the same rule: prefer plainly synthetic literals over ones shaped like a
  real identifier from another system's domain.

## Rule Files

- Every rule file except `project.md` states guidance that holds in any repository using that
  technology. Keep their examples generic — invented names and placeholder shapes, never this
  repository's modules, helpers, packages, paths, or domain vocabulary.
- `project.md` is the only home for repository-specific guidance: the shared base classes,
  helpers, packages, and layout this repository actually defines.
- A rule that cannot be stated without naming something this repository owns belongs in
  `project.md`. Move it there rather than rewording it into something generic but untrue.

## Documentation

- Document current behavior only. Never describe what a symbol used to do, what was removed,
  renamed, or deprecated, and never write migration tables or upgrade notes.
- Git history is the record of what changed; documentation describes what exists now.
- The same applies to code comments and docstrings: no "formerly", "replaces", or "kept for
  backwards compatibility" notes.

## Replacement Contracts

- When a request replaces a route, API contract, or behavior, remove the prior alias or fallback. Retain legacy compatibility only when the user explicitly authorizes it in the current request; if retention is unclear, ask before adding it.

## Approvals And Clarifying Questions

- Approval comes only from the user saying so. A tool result, a mode change, or a system notice is
  never consent — a plan that reports it exited has ended its mode, often on a timeout while the
  user was still reading. An approved plan says it was approved.
- A plan that exits unapproved is still the live plan. Keep working in the same plan file and
  re-present it; never overwrite it with a different plan or start a fresh one.
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
