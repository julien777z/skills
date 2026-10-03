---
description: Rules that hold in every repository, regardless of its stack or conventions.
alwaysApply: true
---

# Global Rules

## Agent sources

- This guidance is used with multiple models and agent harnesses. Prefer one provider-neutral
  implementation and one canonical source for skills, rules, and agent prompts.
- When a shared implementation is not possible, support both Claude and Codex explicitly: account
  for how each discovers, installs, and uses the guidance, and verify both paths. Include other
  supported harnesses where the same change reaches them.
- Read the other shared rules relevant to the current repository and task. If a harness does not
  load them automatically, open the applicable files from its user-level rules directory.

- Never add `agents/openai.yaml` to a repository skill. Repository skills contain `SKILL.md` and
  only supporting files required by the skill; provider UI metadata stays outside repositories
  and is never propagated.

- In repositories that provide an agent CLI or otherwise interact with agents, store every agent prompt in a dedicated Markdown file rather than inline in application code so it is easy to find, review, and maintain. Application code may load a prompt file and interpolate runtime values into it.

- Never stage generated provider output manually. Only the repository's Agent Sync workflow may generate and commit provider mirrors.

## User-Facing Output

- Invoke `i-have-adhd` before the first response a user reads in the session, whether or not the
  user invoked it or the running skill names it. It shapes every response a user reads — an answer,
  a plan put for approval, a report, a summary, a question — until the reader's stop phrase.
- **A file the user should see reaches them where they read.** Per-item detail past five items —
  findings, rows — and any gated plan a skill requires go in a file sent with the harness's
  file-sending tool before the text that reports the result, so that text stays the turn's final
  message. A sent text file reads on its own: it opens with the table or summary its detail belongs
  to, never the detail alone. Text reports sent together go as one markdown file, each report's
  table or summary before any detail. A path alone names nothing a user in a cloud or remote session
  can reach. The parent sends what a subagent produced. Open every
  file, image and recording before sending or presenting it, whoever produced it, and check that it
  shows what the message says it does; a defect it shows besides is fixed rather than offered, as
  `execute-task`'s **Encountered Issues** says. Where the harness cannot send files, say so and put
  what fits inline.
- **A capture of a change reaches the user while the work is still running.** A screenshot, a
  recording, or a generated image that shows something the run changed — the screen after an edit,
  a before-and-after pair, a design it generated — is sent as a file as soon as the agent that made
  it has opened it, never held for the final report, where it arrives in a pile the user can no
  longer follow. A capture nobody asked for that shows no change — taken while navigating,
  diagnosing, or recording a baseline before anything changed — stays where it was saved and is not
  sent, except as the before half of a pair once its after exists; a capture the user or the running
  skill asked for is sent as it is made, change or not. An agent with no file-sending tool hands each
  capture to be sent up as `subagent-selection`'s **Dispatch** describes, and the agent that
  delegated to it opens and forwards each one on arrival. A brief that asks a worker for captures
  asks for them this way.
- A delegated worker's report of an outcome — tests pass, pushed, merged, deployed, fixed — is a
  claim. Check it at its source of truth before relaying it or building on it, and tell the user
  what was read, not what was reported; `execute-task`'s **Reported Outcomes** holds the procedure.

## Task execution and authorization

- Run a user-triggered action skill only after the user directly invokes it in the current request.
  Do not infer authorization from implementation, validation, delivery, pull-request, merge, CI,
  or earlier-request activity. Guidance maintenance is the exception: `edit-skill` runs when the
  user reports a guidance failure or canonical guidance is being changed, so the failure and its
  owning instruction are repaired together.
- Record consciously deferred work immediately in its owning repository. A chat note is not a
  durable deferral record; no separate invitation is needed.
- A direct invocation authorizes one full run at the requested scope. An explicit request to
  continue a loop authorizes repeated runs only within that loop until its outcome, a user stop,
  or a genuine blocker. Start the invoked skill and ask before narrowing its scope.
- For an invoked skill, do not decline, defer, or drop a finding, fix, or validation step because
  the work looks large, difficult, or likely to exceed a guessed time, context, or token budget.
  Only the user declares a budget spent. Work until complete or actually blocked; if an interruption
  ends the run, report what finished and record precisely what the next session needs to resume.

- An authorized task, including a fix request or approved plan, covers ordinary implementation,
  verification, and scoped external mutations. That authorization covers intermediate steps without
  repeated approval questions and persists through follow-ups, retries, recovery, and context
  compaction until the outcome is complete or the user withdraws it. A proposed action that materially
  expands the target, recipient, or outcome needs its own authorization.
- Merge, deployment, publication, and release require the user's explicit authorization for the
  action and target, or an applicable rule or invoked skill that expressly authorizes them. A fix
  request, approved plan, or instruction to implement a plan does not itself authorize these
  outcomes, even when the plan lists them. A task-wide "all approved" covers ordinary sub-tasks
  within its stated outcome without overriding this separate boundary.
- Authorization to send messages to another agent or external session covers only the messages and
  purpose the user specified. Permission for a bounded exchange does not authorize later updates
  to the same recipient; ask before sending more unless the user explicitly approved an ongoing
  exchange.
- Do not ask the user to restate task authority with "continue", "proceed", or an equivalent
  intermediate question. State progress and take the next ordinary authorized action.
- When a platform imposes an action-time confirmation for a distinct sensitive action, complete all
  non-impactful preparation first and ask one exact question immediately before that action. Make
  clear that the task remains authorized. Wait up to 10 minutes without polling or interacting with
  the approval surface; treat it as failed only after that window or an explicit failure. A failure
  is not approval: wait for the user to resume before prompting again. After confirmation, complete
  the remaining ordinary work without another approval question.

- Only a user statement constitutes user approval; a tool result, mode change, or system notice
  does not. A plan that exits without approval remains the live plan: continue in the same file and
  re-present it rather than replacing it.
- Send what a question asks about — a plan, an example response, a diff — as the final message of
  a turn, with the question in that message as plain text. The question tool shows only the question
  and its option labels, and text written in the same turn as a tool call can reach the user only as
  a collapsed summary, so content placed in a preview, a description, or before a tool call is lost.
- When a question is presented through the question tool and no answer comes back, never fall
  back to picking an option. Post the question and its options as plain text in chat and wait
  for the answer.

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

## Tools and environments

- Treat an inventory or availability error as scoped to the surface it names. A native-app lock or failure does not block browser automation, and a browser failure does not block terminal or API work.
- Before reporting a task blocked by a surface warning, inspect the requested surface directly and retry its normal recovery path. For a browser, refresh the tab inventory and reopen an authenticated task tab when the prior agent-owned tab has closed.
- Prefer an isolated agent-owned browser tab. When the user explicitly directs use of an existing
  browser tab or window for the current task, that instruction overrides the isolation preference;
  use only the authorized surface and leave every other user-owned surface untouched.
- Report a block only when the requested surface itself cannot complete the next required action and safe alternatives have been exhausted.

- **Local stack resources are disposable, and repairing them is part of the work, never a question for the user.** Local databases and their migration state, Redis, Docker containers, volumes, networks, images and the daemon itself can be repaired, reset, dropped or recreated whenever the task needs them working. A database stuck on a revision a branch has since regenerated, a stale cache, a wedged container: fix it and carry on. The one limit is a resource another run is actively using, such as a test runner holding the stack's lock. Wait for it or use a separate resource; never stop it. Deployed and shared remote environments are not local; the following live-deployment rules govern them.

- Treat create, update, and delete requests against a live deployment as data mutations, not health
  checks. Run them only against a target that the repository explicitly designates for mutation
  testing; when no such target exists, live smoke testing is read-only.
- When the same artifact and materially equivalent configuration run in several environments, one
  successful write test on the designated mutation target plus read-only health and routing checks
  on the others validates the shared path. Never create persistent synthetic records in a stable or
  shared staging environment merely to smoke-test a deployment.

## Code layout

- In every language, use blank lines to separate setup, validation, transformations, side effects, and returns. Keep adjacent statements together only when they form one small operation; do not turn a function into an uninterrupted paragraph merely because a formatter permits it. Apply this to existing code in files you change.
- Use current language syntax for simple operations. For one-off Python interpolation, use f-strings instead of string concatenation or `.format()`, and keep spacing in the final string rather than a fragment with a hidden leading space. Follow the Python rule for reusable structured templates.

```python
# Good: each phase is visible.
records = load_records()

if not records:
    return []

normalized = [normalize(record) for record in records]

save_records(normalized)

return normalized

# Bad: unrelated phases run together.
records = load_records()
if not records:
    return []
normalized = [normalize(record) for record in records]
save_records(normalized)
return normalized
```

```typescript
// Good: separate the request, guard, state change, and result.
const response = await fetchRecords();

if (!response.ok) {
  throw new Error('Could not load records');
}

const records = await response.json();

setRecords(records);

return records;
```

- A bootstrap or setup folder holds only its entrypoint at its root, such as `setup/run.sh`; every
  supporting script, module, or data file it uses goes in `setup/resources/`.

## Repository guidance

- Reference external code and automation by a maintained version tag when available, or by a
  maintained branch while developing or when no release tag exists. Do not pin dependency manifests,
  shared checkouts, or workflow references to commit hashes. Lockfiles and release records may retain
  the exact resolved commit for reproducibility and provenance.

- Every repository stands on its own. Never carry another repository's domain vocabulary into this
  one: its product name, its services, its table and column names, its record types, or the nouns
  its business speaks in. That holds for source, tests, fixtures, examples, and documentation
  alike, and it holds most strongly in a library, where every reader is a different consumer.
- Name things for the shape being exercised, not for whichever caller happened to prompt the work.
  A test needing a table with a secret column names it for that — a record with a secret — rather
  than borrowing the one real table the change was made for.
- Sample values follow the same rule: prefer plainly synthetic literals over ones shaped like a
  real identifier from another system's domain.

- `.agents/global.md` states guidance that holds in every repository, and every `.agents/rules/*.md`
  file guidance that holds in any repository using its technology. Keep their examples generic —
  invented names and placeholder shapes, never this repository's modules, helpers, packages, paths,
  or domain vocabulary, and never the product, tool, or platform whose incident prompted the change.
- `.agents/project.md` is the home for repository-specific guidance: its base classes, helpers,
  packages, layout, documentation structure, inventories, and generated sections.
- Repository facts only some work needs — a local stack, test accounts, deployment targets, a
  migration layout — go in `.agents/references/<name>.md`, named for their content and read on
  demand, and `.agents/project.md` points to each file in one line. A repository's project guidance
  is `project.md` together with the reference files it points to.
- A rule that cannot be stated without naming something this repository owns belongs in
  `.agents/project.md`. Move it there rather than rewording it into something generic but untrue.

- **Every document holds only what its reader needs for its purpose.** A README, project guidance, a
  skill, a rule, a design document, a pull request description, a code comment: each has one reader
  and one job, and content goes to the document whose reader acts on it. Being nearby, or already
  covering the area, is no reason to add to a document; an operator's runbook in a README, an
  incident timeline in a skill, and a design specification in a code comment are each content in the
  wrong document. A change adds to a document only what alters that document's reader's work.
- Document current behavior only. Never describe what a symbol used to do, what was removed,
  renamed, or deprecated, and never write migration tables or upgrade notes.
- Git history is the record of what changed; documentation describes what exists now.
- The same applies to code comments and docstrings: no "formerly", "replaces", or "kept for
  backwards compatibility" notes.
- Use an environment's exact domain name for both it and its tailnet; never append owner or
  organization aliases. Name provider accounts and projects only as separate resources.

- When a request replaces a route, API contract, or behavior, remove the prior alias or fallback. Retain legacy compatibility only when the user explicitly authorizes it in the current request; if retention is unclear, ask before adding it.
