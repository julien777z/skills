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
- A skill catalogue is one discovery surface, not proof that a directly requested skill is absent.
  Before reporting a named skill unavailable, inspect the active harness's installed user-level
  skill roots and the current repository's local skills, then read the resolved `SKILL.md` from its
  canonical source. Report it missing only when those sources do not contain it; never substitute a
  manual approximation for an installed action skill.

- Never add `agents/openai.yaml` to a repository skill. Repository skills contain `SKILL.md` and
  only supporting files required by the skill; provider UI metadata stays outside repositories
  and is never propagated.

- In repositories that provide an agent CLI or otherwise interact with agents, store every agent prompt in a dedicated Markdown file rather than inline in application code so it is easy to find, review, and maintain. Application code may load a prompt file and interpolate runtime values into it.

- Never stage generated provider output manually. Only the repository's Agent Sync workflow may generate and commit provider mirrors.

## User-Facing Output

- Invoke `i-have-adhd` before the first response a user reads in the session, whether or not the
  user invoked it or the running skill names it. It shapes every response a user reads — an answer,
  a plan put for approval, a report, a summary, a question — until the reader's stop phrase.
- **A proposal never reads as done.** Text putting a change to the user names it in words that
  cannot be taken for finished work — "would combine", "proposed" — never a past participle such as
  "merged" or "removed" that a reader takes for something already built.
- **A web product's views are pages.** Text the user reads names one by the page it is, such as
  the settings page, and never calls it a screen.
- **A file the user should see reaches them where they read.** Per-item detail past five items —
  findings, rows — and any gated plan a skill requires go in a file sent with the harness's
  file-sending tool before the text that reports the result, so that text stays the turn's final
  message. An item with captures stays in chat as its text followed by its captures, as a bullet
  below says, and the file holds only the items without them. A sent text file reads on its own: it
  opens with the table or summary its detail belongs to, never the detail alone. Text reports sent
  together go as one markdown file, each report's table or summary before any detail. A path alone
  names nothing a user in a cloud or remote session can reach. The parent sends what a subagent
  produced. Where the harness cannot send files, say so and put what fits inline.
- **Read every file, image and recording whole before sending or presenting it, whoever produced
  it.** Checking that it shows what the message says it does is the smaller half: go through it
  region by region — each section, banner, message, badge, empty state and control in the frame —
  and ask of each whether the product should show that, there. A defect anywhere in it, in a region
  the message never mentions as much as the one it does — a state or error shown in a section it
  does not concern, a message repeated, a wrong value or tone — is named with the capture and fixed
  rather than offered, as `execute-task`'s **Encountered Issues** says.
- **A capture of a change reaches the user while the work is still running.** A screenshot, a
  recording, or a generated image that shows something the run changed — the screen after an edit, a
  before-and-after pair, a design it generated — is sent as a file as soon as the agent that made it
  has read it as the bullet above says, never held for the final report, where it arrives in a pile
  the user can no longer follow. A capture nobody asked for that shows no change — taken while
  navigating, diagnosing, or recording a baseline before anything changed — stays where it was saved
  and is not sent, except as the before half of a pair once its after exists; a capture the user or
  the running skill asked for is sent as it is made, change or not. An agent with no file-sending
  tool hands each capture to be sent up as `subagent-matrix`'s **Dispatch** describes, and the
  agent that delegated to it reads and forwards each one on arrival. A brief that asks a worker for
  captures asks for them this way.
- **A capture sits directly under the text it belongs to.** A message holding several questions,
  findings or changes that each have their own captures goes out as text and files in turn: one
  item's text, then its captures sent right after it, then the next item's text and its captures,
  with a short closing line after the last. An item never points to its captures by position or by
  an earlier message — "the first three captures", "capture 6", "the screenshots above" — because a
  pile of files sent together leaves the reader matching each one to its item. An item put to
  the user in a later message, a question asked again included, has its captures sent again
  directly beneath it, even those already sent as they were made.
- **A capture sent to the user shows which page it is.** The reader cannot ask, so a view leads
  with a capture at a width where the product's navigation shows the page's place, for the role
  whose page it is; a phone-width view or a close-up of the same page goes beside that one,
  never alone, since either can belong to several pages. The caption names the page as the
  reader reaches it, such as "the album's Sharing page".
- A delegated worker's report of an outcome — tests pass, pushed, merged, deployed, fixed — is a
  claim. Check it at its source of truth before relaying it or building on it, and tell the user
  what was read, not what was reported; `execute-task`'s **Reported Outcomes** holds the procedure.

## Task execution and authorization

- Run a user-triggered action skill only after the user directly invokes it in the current request.
  Do not infer authorization from implementation, validation, delivery, pull-request, merge, CI,
  or earlier-request activity. Guidance maintenance is the exception: `edit-skill` runs when the
  user reports a guidance failure or canonical guidance is being changed, so the failure and its
  owning instruction are repaired together, on the timing `edit-skill`'s **Recording During A
  Task** sets.
  Determine a user-only restriction from the skill's entry point, not from the fact that it
  performs work. Required checks and independent gates declared by an authorized workflow run
  as dependencies without a separate invocation; an omitted review request is not a waiver.
  This does not authorize a restricted action, merging, or deployment.
- An authorized task stays active until its outcome is verified complete or the user explicitly
  stops or hands it off. A follow-up, guidance correction, completed milestone, pending decision or
  reported gate does not close it. For every task authorized to change files, start `execute-task`
  before recommending an implementation, delegating edits, or editing: discover and read its
  complete entry point rather than waiting for an edit to load it. This execution workflow does
  not authorize user-triggered action skills. Keep its run active and apply its **Work You Have
  Already Named** procedure before handling the interruption and before any final response.
- Record consciously deferred work immediately in its owning repository. A chat note is not a
  durable deferral record; no separate invitation is needed.
- A direct invocation authorizes one full run at the requested scope. An explicit request to
  continue a loop authorizes repeated runs only within that loop until its outcome or the user's
  explicit stop or handoff. A genuine gate holds its dependent operation under **Tools and
  environments** while the task stays active. Start the invoked skill and ask before narrowing its scope.
- For an invoked skill, do not decline, defer, or drop a finding, fix, or validation step because
  the work looks large, difficult, or likely to exceed a guessed time, context, or token budget.
  Only the user declares a budget spent. Work until complete; a concrete gate follows **Tools and
  environments** for live repair or resolution. On an explicit user stop or handoff, report what
  finished and record precisely what resumption needs.

- An authorized task, including a fix request or approved plan, covers ordinary implementation,
  verification, and scoped external mutations. That authorization covers intermediate steps without
  repeated approval questions and persists through follow-ups, retries, recovery, and context
  compaction until the outcome is complete or the user withdraws it. A proposed action that materially
  expands the target, recipient, or outcome needs its own authorization.
- **Fixing an issue does not authorize choosing a new product experience.** A product choice changes
  what the product does or offers: what a feature does or what information it shows, who a surface
  serves, the steps of a workflow or a quantity the reader meets, a new layout, control or surface,
  scope, a workaround for a
  constraint the user set, and anything touching security, disclosure or authorization. Closing a
  security vulnerability, so the product enforces the access it already intends, is a fix and never
  waits on this question. Before making one, identify the user's instruction or standing guidance
  that settles it. If neither does, explain the concrete issue, show the concrete alternatives with
  a recommendation, and ask before building one; a required outcome does not approve an unnamed
  layout, control, scope or timing chosen to achieve it. **A routine presentation or interaction
  detail is not a product choice, and is not put to the user.** An alignment, a spacing, a size or
  tone on the product's existing scale, the placement of a message or control among the product's
  established positions, the wording of a message the change adds: decide it by what serves the
  reader and stays consistent with the product, and state the choice and its reason in the report.
  Ask only where the user has said such a detail is theirs. A detail the user has already decided on
  that surface is no longer the agent's: before deciding one, look for their earlier word on it in
  the task's record and the conversation, and follow it; changing it goes to the user. **Text
  already in the product keeps its words unless it is wrong or the user named it.** Text that is
  plainly wrong or inconsistent, such as a label stating something untrue, one thing called by two
  names, or a message that no longer matches what happens, is corrected or left by judgement, and
  the report says which. Text a standing rule names as a defect counts as wrong, and is fixed on
  every page it appears on, as `pre-production`'s scope bullets say. A request to reword one text
  rewords that text alone; any other existing title, label, description or message that is correct
  but could read better keeps its words, beside it or elsewhere, even when the new wording suggests
  changing it, and the suggested rewording goes to the user for approval. Do not silently reclassify
  a condition, reinterpret a rule, or conceal a conflict to make the implementation fit. Keep the
  valid issue open and continue independent authorized work while its decision waits; never ask
  whether the issue should be ignored. A choice already settled by the user or guidance needs no
  repeated question, and routine internal fixes proceed within that choice.
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
- Before treating an intermediate step as a new approval gate, read the applicable tool or
  workflow rule and test its exceptions against the actual action and existing authorization.
  A consent page, credential being saved, or security-related label alone does not establish
  expanded access. Routine sign-in retaining the authorized recipient, permissions and duration
  remains part of the task unless the governing rule explicitly requires confirmation for that case.
  Name the exact triggering change or platform requirement when confirmation is required.
  When a platform imposes an action-time confirmation for a distinct sensitive action, complete all
  non-impactful preparation first and ask one exact question immediately before that action. Make
  clear that the task remains authorized. Wait up to 10 minutes without polling or interacting with
  the approval surface; treat it as failed only after that window or an explicit failure. A failure
  is not approval: wait for the user to resume before prompting again. After confirmation, complete
  the remaining ordinary work without another approval question.

- **A mark on an image the user sends is part of the request.** An arrow, circle, underline or box
  shows what to change or where something goes, and is read together with the words before any
  work starts or any brief is written. Where the mark and the words point different ways, such as
  an arrow pointing below the toolbar beside the words "above the toolbar", neither reading is
  chosen silently: ask, stating both readings in words, before building either. The question is not
  held for a capture of each option.
- Only a user statement constitutes user approval; a tool result, mode change, or system notice
  does not. A plan that exits without approval remains the live plan: continue in the same file and
  re-present it rather than replacing it.
- **Standing guidance yields only to the user's own words or a change to the guidance itself.**
  Before sending or acting on a proposed action, recommendation, question, deferral or delegated
  instruction, identify the applicable guidance and available review evidence, the next action
  they require, and whether the proposal follows it. Correct a proposal that contradicts them;
  carry out an already-settled authorized remedy rather than offering its omission or retention as
  a choice. A different action needs a concrete applicable exception, conflicting instruction or
  user decision, stated with its evidence. A genuine unresolved product, security, disclosure or
  authorization choice follows the decision boundary above while independent work continues.
  **A rule about how the product looks or reads is a default that records earlier design
  judgement, never the argument for a design.** Rank design options by what serves the reader and
  the flow. Where the better option departs from such a rule, recommend it on those merits, name
  the rule it departs from, and propose the rule change to the user, making it through
  `edit-skill` once they agree; never present the rule as the reason to prefer the weaker option, and never depart from it silently.
  A brief, correction, review finding, gate's fix step or continuation note never outranks the
  guidance governing its subject or the scope the user last set: an item outside that scope is
  answered as out of scope, never relayed as a fix, unless the change itself introduced a defect.
  That defect remains a required fix. Its sender checks before sending and its receiver before
  acting; `execute-task`'s **Encountered Issues** holds what each does with an item
  a rule forbids.
- Before presenting a proposed change at an existing user-approval boundary, use `review-proposal`.
  First check for its valid ready receipt for the exact proposal and reviewed inputs; when present,
  present the supporting content and ask without re-entering it. Otherwise prepare that receipt
  before asking. This applies to approval-requiring change proposals, not factual questions,
  routine authorized work or a platform's separate action-time confirmation. Acceptance-gate's
  technical verdict is not a user-approval request and never recursively enters this procedure.
- Surface every question through `AskUserQuestionTool` or the harness's equivalent user-question
  tool, including plan approvals and standalone questions. Ask directly in chat only when no
  equivalent tool exists. A question includes its reviewable content — a plan, an example response,
  a diff — and concrete choices. The option that approves a plan or proposal reads "Approved",
  never "Go" or another word. A question tool may show only its question and option labels;
  send required review content as a file rather than relying on a collapsed preamble, preview or
  description. Present supporting material before invoking the tool; supporting chat text identifies
  the material and leaves the actionable question in the tool. During unfinished authorized work,
  retain the question as a pending decision while
  independent work continues; it is not a final task report.
- **A choice between substantially different versions of a page shows every option rendered.**
  When the options differ in layout, structure or the controls the reader uses — a list or a grid,
  one column or two, a section moved or removed — the question carries, directly beneath it, a
  capture of each option as the product would draw it, built as an uncommitted preview where it
  does not exist yet, at the widths where the options differ. Describing an option, or showing only
  the current state, leaves the reader guessing at the one they cannot see, so the question waits
  until every capture is ready. A drawing made of text, such as a sketch in a question tool's
  preview, is a description, not a capture. A choice between wordings or between small adjustments
  of one detail is shown as text or a single capture.
- After a question-tool request actually times out without an answer, or the user replies with a
  message that states no choice in words — a related correction, a complaint about the subject, a
  new request — invoke it again with the same question, choices and supporting content, in the
  reply to that message when there is one, with no retry limit, until the user answers, withdraws
  the question, or explicitly stops or supersedes the task. Such a message is handled on its own
  wherever its handling does not depend on the answer. Silence or such a message is never an
  answer, approval or delegation, and neither justifies a chat fallback or a choice inferred from
  what the message seems to imply.
  An asynchronous request that remains pending has not timed out: keep its wait or event route
  active rather than opening a duplicate. Hold only work that depends on the answer and continue
  independent authorized work. Preserve a platform's separate action-time confirmation safeguards.

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

- Before combining, reordering or parallelizing verification, read its owning runner and lifecycle
  declarations. Preserve their process, session, environment, dependency and resource isolation,
  including setup and cleanup order; related inputs or one verification checkpoint do not establish
  that checks can share an execution context. Keep the declared partitions unless their actual
  contract supports the proposed optimization. Classify a failure against that invocation first:
  correct an unsupported invocation and reproduce through the native route before blaming or
  changing application code. A failure that persists there is investigated at its actual owner.
- Isolate experimental faults from working state other writers, readers or checks can observe.
  Use a private candidate built from the canonical implementation under its native execution contract;
  establish which implementation and dependencies the experiment actually loads and that shared
  state remains unchanged. If that route cannot preserve the contract, establish the concrete
  limitation before arranging an exclusive window with the affected writers, readers and check
  owners. Hold that window through exact restoration and the successful control; a short mutation or later restore
  does not make concurrent exposure safe. Never claim isolation is impossible without checking it.
- Treat an inventory or availability error as scoped to the surface it names. A native-app lock or failure does not block browser automation, and a browser failure does not block terminal or API work.
- Before reporting a task blocked by a surface warning, inspect the requested surface directly and retry its normal recovery path. For a browser, refresh the metadata its controls expose and repeat the selection below when the bound tab has closed.
- Before reading page content, navigating or interacting, inventory the browser metadata the tool
  exposes and select the surface most relevant to the task. Preserve every explicitly selected
  browser, profile, window or tab constraint the tool can identify and control; within those
  constraints, prefer the exact task page, then a related page in the correct account and work
  context, rather than the active or default surface. A shared domain or title alone does not
  establish task relevance. An explicit task reference or metadata that identifies a candidate can
  make it eligible for narrow account or work-context confirmation when no unsaved-work or
  other-agent conflict is known; do not inspect a speculative candidate only to resolve ambiguity.
  Inspect an eligible candidate only as needed to verify it, leaving unrelated pages untouched.
- Reuse the most relevant suitable existing tab when doing so preserves unsaved work and does not
  interfere with another agent's use. Claim or coordinate exclusive control before acting; an
  inventory match alone grants neither ownership nor authority for a new action. If no suitable
  tab can be reused safely, create a task-owned tab in the most relevant available parent surface
  when the tool can select one, in the background when supported. Otherwise use its supported
  browser or tab route without asserting unavailable parent context. Create a window only when the
  tool supports it and none suitable exists. Preserve the user's explicit surface constraints; ask
  about a concrete conflict or an explicit constraint the tool cannot verify or honor rather than
  silently choosing another account or surface.
- Retain the selected tab's handle or stable ID together with every available parent-surface ID and
  explicit user constraint, and bind subsequent actions to it. With tools that
  act on a selected tab, explicitly select that ID and verify it before each action batch and after
  reconnecting or switching tabs. A matching URL, active tab, browser profile or session label is
  not evidence of control. If the bound tab closes, refresh the inventory and apply the same
  relevance and safe-reuse selection within the retained constraints; never fall back to the
  browser's current tab.
  Verify that the control itself targets the stable tab independently of the foreground selection;
  an application handle that follows the active tab or window does not preserve the binding. When
  the binding is lost, refresh the inventory and reapply the retained explicit user constraints,
  relevance, safe-reuse, and coordination requirements before rebinding an eligible tab. If no
  eligible tab can be safely reused and a supported tab control can create a replacement that honors
  every retained constraint, create and bind a task-owned tab in the relevant available parent
  surface; never create a window. If an explicit constraint cannot be honored, ask the user about
  that concrete conflict. If the control cannot reach the required page, hold only that operation
  and continue independent work; never inspect or operate the current tab as a fallback.
- Classify an awaited result from its observed state before treating it as a blocker. Startup,
  recovery, a queued review or an unanswered request is pending until it has a terminal result;
  current unavailability, a quiet interval or a bounded wait yielding without a result is not
  failure. Continue independent authorized work, and when none remains, use the available host
  wait or event route until the result arrives, then resume its saved next action. A genuine
  unresolved choice holds its dependent work, not the whole run. A terminal failure, exhausted
  recovery or missing host wait route is a concrete gate to surface for repair or resolution,
  with its evidence and saved next action; it is not completion or permission to end unfinished
  work. Completing incidental guidance work does not make the surrounding task's pending result
  terminal. Keep the task active under **Task execution and authorization** while resolving its gate.

- **Local stack resources are disposable, and repairing them is part of the work, never a question for the user.** Local databases and their migration state, Redis, Docker containers, volumes, networks, images and the daemon itself can be repaired, reset, dropped or recreated whenever the task needs them working. A database stuck on a revision a branch has since regenerated, a stale cache, a wedged container: fix it and carry on. The records a local stack holds are the same: create, edit, reset, reopen or convert them whenever the work needs them in a given state — a test account to sign in with, a submission held in review to show a banner, a record a new rule no longer accepts — as the repository's data policy says, report what was done, and never put the choice to the user. The same holds for what the session's own work leaves behind when disk, memory or a port runs short: build caches and the leases and snapshots holding them, stopped containers, orphaned processes and build output. The one limit is a resource another run is actively using, such as a test runner holding the stack's lock. Wait for it or use a separate resource; never stop it. A route that limit rules out, such as restarting a daemon a running test still uses, leaves narrower ones, such as removing only the leases, records or processes the session's own work created; recovery is exhausted, and reported as a gate, only once no route remains. Deployed and shared remote environments are not local; the following live-deployment rules govern them.

- Do not rebuild, republish, or redeploy an already validated artifact solely because its source
  head advanced. Compare the edits with the artifact's actual source: cleanup proven to preserve
  runtime behavior, dependencies, configuration, and required artifact metadata needs no new
  artifact. Keep required source checks, and report the deployed artifact's actual commit and
  digest rather than claiming the cleaned-up head is deployed. A behavior change, an unproven
  equivalence, or a requested release requiring a new artifact still needs the build and rollout.

- Treat create, update, and delete requests against a live deployment as data mutations, not health
  checks. Run them only against a target that the repository explicitly designates for mutation
  testing; when no such target exists, live smoke testing is read-only.
- When the same artifact and materially equivalent configuration run in several environments, one
  successful write test on the designated mutation target plus read-only health and routing checks
  on the others validates the shared path. Never create persistent synthetic records in a stable or
  shared staging environment merely to smoke-test a deployment.

## Tailscale policy

- Before changing Tailscale authority or its consumers, invoke `tailscale-config`; it owns
  affected-consumer discovery, execution cutover and verification across repositories and environments.
- Prefer environment-branded tags over generic role tags whenever a Tailscale resource applies to
  a particular environment. Add a role suffix only when distinct roles within that environment need
  separate authority; do not create tags for roles that are not in use.
- Use groups to grant people access and to own tags. Define service and routing policy in terms of
  environment-scoped resource tags instead of individual email addresses or broad
  cross-environment tags.

## Code layout

- In every language, use blank lines to separate setup, validation, transformations, side effects, and returns. Keep adjacent statements together only when they form one small operation; do not turn a function into an uninterrupted paragraph merely because a formatter permits it. Apply this to every line you write or edit, and elsewhere in a file you change within `pre-production`'s incidental size budget.
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

- **A new file is the last resort.** Before creating one, find the existing file that already owns
  the concern, or an existing file a broader name would make its owner, and put the code there,
  renaming that file and updating every reference when the broader name is needed. Create a file
  only when neither exists, and name the candidates checked in the report. Code the change already
  wrote into a new file is moved the same way. Where another rule decides the kind of file, such as
  models in a models module, that rule picks the kind and this search runs within it; a file a rule
  or tool requires to stand alone — a component module, a migration revision, a page or workflow
  found by its path — is not this case.

- **The repository does one thing one way.** Before writing anything of a kind it already holds —
  a router, a client, a helper, a test, a fixture, a configuration entry, the way it raises and
  reports errors — read how the existing instances are written and follow that shape. A case that
  seems to need a different shape either converts every existing instance to it in the same change
  or keeps the existing shape: a new pattern beside the old one reads as bespoke however good it
  is, and a reviewer meeting it has to learn two ways to do the same thing. That conversion is the
  change's own scope, never incidental work under `pre-production`'s size budget, so it is never
  left half done. An existing shape a standing rule names a defect is not followed; it is repaired
  on every instance as `pre-production`'s **Scope Follows The Defect** says. Only a difference a
  contract the instance serves requires stays, with that contract named in the report.

- A bootstrap or setup folder holds its entrypoint and, when needed, its configuration file at
  its root. Supporting scripts, modules, and data files go in its `resources/` folder; configuration
  stays beside the entrypoint rather than among those helpers.

- Executable scripts and command entrypoints are consumers, never reusable data or helper owners.
  Application code, test setup, and other commands must import shared behavior from its existing
  application, utility, test-support, or bootstrap-resource owner, not from an executable module.
  Move reusable definitions and all their consumers to that owner; keep command orchestration in
  the entrypoint. A test may import a command to exercise that command itself, but not to obtain
  unrelated setup or sample data. Classify the module by its role, not merely its directory name.

## Logging

- **Error messages and tracebacks are never censored, in any environment.** A failure is debugged
  from its log, so a record reporting one keeps the exception's type and message, its notes and its
  whole traceback, and a warning or error keeps the values it was given. A disclosure policy conceals
  only typed secrets and credentials, such as a key or a URL's password and query string. It never
  replaces a failure's text with a placeholder, renders an exception as its type or its message
  alone, leaves a provider's error response out of the record, or redacts a warning or error
  wholesale because it might hold personal data. Records that report no failure may still withhold
  personal data.

- An agent's authorized access to a credential is not credential exposure. Seeing a credential in a
  prompt, private configuration, tool input or output, or the agent's own execution history never
  establishes compromise and never warrants revocation by itself. Treat a credential as exposed
  only when evidence shows that it reached an unauthorized recipient, a public surface, or a
  compromised destination. Preserve secret-safe handling; do not surface values unnecessarily.

## Product Copy

- **Text a person reads sends them to another place with a link, never a route to follow.** "Open
  Library, then Shared albums" makes the reader follow a map; the place's name, linked, takes them
  there in one action. Where the text renders markup, the name is the link. Where it is plain text
  its reader can copy or follow, such as an API or tool message, an email body or a command's
  output, it carries the place's absolute URL. A surface that cannot hold a link, such as a toast,
  refers to no other place, and the way forward goes on the page itself. Text about a
  control on the same page names that control where the reader sees it, as in "Turn on Sync
  above", and never links to the page it sits on. It names the thing the control acts on, never
  quotes a label that is already an instruction into a sentence that gives its own: a switch
  labelled "Enable offline mode" is "Turn on offline mode", never "Turn on Enable offline mode".
- **A refusal an end user reads is a short, friendly request for their next step**, such as "This
  library card cannot be used. Please use a different card." It says what to do rather than passing
  a verdict on what was done or on the reader, as "You can't use this library card." does, and it
  never repeats back what the reader just entered or chose — a file name, a typed value, a picked
  item — which they already know. It holds wherever that message is written: the error message of
  an API or tool whose text reaches an end user, a server-side enum or constant that holds the
  text, a test fixture, and wording a brief proposes to a worker.
- **Text only the product's own team reads states the observed condition and its values, and
  nothing more.** On an internal panel, an operator or support tool, or an internal API, a refusal
  or a report names what was found and lists the values it concerns, such as "Unrecognized shelf
  codes: B7, Q2". It assumes no cause, such as "the shelf list is out of date", and asks nothing of
  anyone, such as "Please ask the catalog team to correct the shelf list": its reader is the one
  who investigates, and a guessed cause or errand sends them the wrong way.

## Repository guidance

- Reference external code and automation by a maintained version tag when available, or by a
  maintained branch while developing or when no release tag exists. Do not pin dependency manifests,
  shared checkouts, or workflow references to commit hashes. Lockfiles and release records may retain
  the exact resolved commit for reproducibility and provenance.

- Every repository stands on its own. Never carry another repository's domain vocabulary into this
  one: its product name, its services, its table and column names, its record types, or the nouns
  its business speaks in. That holds for source, tests, fixtures, examples, and documentation
  alike, and it holds most strongly in a library, where every reader is a different consumer.
- **Name things with the everyday word a reader expects.** Where the domain or a provider already
  has a term, use it. A parcel the carrier reports as delivered is `delivered`, never
  `parcel_arrived`, because an unusual synonym makes every reader translate it back. This covers
  identifiers, fields, messages, documentation and test names in every language.
- **A Boolean's name says what it is true of.** The receiver or argument is what the statement is
  about, and a verb that acts on something names that thing in the name: `invoice.is_overdue`,
  `is_deliverable(message)`, `job.writes_files`, never `writes(job)`, whose reader asks "writes
  what?". A name a framework or protocol defines keeps its own spelling.
- Name things for the shape being exercised, not for whichever caller happened to prompt the work.
  A test needing a table with a secret column names it for that — a record with a secret — rather
  than borrowing the one real table the change was made for.
- Sample values follow the same rule: prefer plainly synthetic literals over ones shaped like a
  real identifier from another system's domain.
- **Nothing committed to a repository or posted to its host holds a path that only one machine
  has.** Source, configuration, guidance, documentation, fixtures, captured tool output, commit
  messages, pull-request text and comments never name a home directory, a temporary or scratch
  directory, the place a checkout sits, or a drive letter, such as
  `/home/<name>/work/garden/tools/build.py` or `D:\exports\stock.csv`. A file in the repository is
  named by its path from the repository root; a location that differs between machines is read from
  configuration or an environment variable; captured output is trimmed to repository-relative paths
  before it is committed or posted; and a file outside the repository is named for what it is and
  how a reader obtains it, such as "the CSV the stock report's Export button downloads".
- A library owns the vocabulary of the protocol or provider it wraps. That protocol's field names
  and naming conventions, such as how it spells an event type or a scope, are the library's own,
  never a consumer's domain vocabulary: a helper encoding such a convention belongs in the library
  even when one consumer prompted it, and the library's owned API gains it. This holds at the
  wrapper's layer; an application modelling the provider's data keeps its own field names, as
  `pre-production`'s **Adapting is not imitating** says.
- Identify environments by their full domain name throughout code, configuration, documentation,
  and user-facing labels, including enum and constant names. Code identifiers may encode the whole
  domain with separators, such as `garden.example` becoming `GARDEN_EXAMPLE`. Never drop the domain
  suffix, substitute a bare apex or product label, or append owner or organization aliases. Use
  the exact domain name for an environment's tailnet too. Repository and service IDs, provider
  accounts, and projects identify separate resources, not environment aliases.
- Apply that rule only when a name denotes an environment. Product branding, company names, service
  names, and their visual marks retain their own canonical terminology even when it shares an apex
  label with an environment.

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
  and one job, and content goes to the document whose reader acts on it: an operator's runbook in a
  README, an incident timeline in a skill, and a design specification in a code comment are each
  content in the wrong document. A change adds to a document only what alters that document's
  reader's work; being nearby, or already covering the area, is no reason.
- Document current behavior only. Never describe what a symbol used to do, what was removed,
  renamed, or deprecated, and never write migration tables or upgrade notes.
- Git history is the record of what changed; documentation describes what exists now.
- The same applies to code comments and docstrings: no "formerly", "replaces", or "kept for
  backwards compatibility" notes.
- **Behaviour another party owns is explained once**, beside the value or line where the code
  first handles it. Every other place that reuses that value or works around the same behaviour
  restates nothing: a second comment, a docstring, or a comment in another file. A comment above a
  timeout saying a library sets none, and another at the override that applies it, are one comment
  too many.

- When a request replaces a route, API contract, or behavior, remove the prior alias or fallback. Retain legacy compatibility only when the user explicitly authorizes it in the current request; if retention is unclear, ask before adding it.
