---
description: Follow shared workflow, branch, pull-request, and commit conventions for GitHub repositories.
alwaysApply: true
---

# GitHub Rules

## Workflows

- Treat a request for CI tests as authorization for test workflows only. Inspect a workflow's jobs
  and triggers before dispatching it; a workflow that builds and publishes artifacts or deploys is
  a release action even if it also runs tests.

- Support authorized selected branches in workflows that build, test, publish, migrate or deploy
  application code whenever the operation supports branch execution. Provide native manual dispatch
  where needed for that branch route, and execute the selected branch's workflow and checked-in
  entrypoint. Preserve scheduled and default-branch automatic behavior and repository, environment
  and source authorization bindings. Default-branch-only execution or merging is never a substitute
  for an available selected-branch route.

- Build, publish, and deploy through the repository's existing entrypoint and supported ref
  selection. Use its GitHub Actions workflow when that is the designated route; a native CLI the
  user explicitly authorizes remains available. Inspect the entrypoint's supported inputs before
  invoking it, and verify the resulting run, artifact and deployed revision.
- An authentication, permission or ref-selection failure is repaired at that entrypoint's identity,
  credential, grants or owned configuration. Grant only the authority the authorized operation
  requires. Never add a temporary input, mode, wrapper or alternate workflow to bypass the failure,
  even with a promise to remove it. A genuinely missing durable capability is source work under the
  task's scope and authorization, never an incidental recovery allowance.

- Keep `run` steps declarative. Invoke checked-in scripts for control flow, validation, filesystem changes, or other implementation logic instead of embedding arbitrary shell or program code in workflow YAML; place those scripts under `.github/scripts/` and prefer Python.
- Do not hard-code runtime versions when a shared action, reusable workflow, or repository version file supplies them; omit `python-version` when shared Python automation provides it, and use `node-version-file: ".nvmrc"` for Node.js workflows.
- Name repository-owned Boolean action and workflow inputs `use-<capability>`, so the name states
  what the toggle enables. Update declarations, conditions and callers together; do not retain a
  bare capability name or an old alias. Preserve external actions' input contracts.
- **An owned package the repository depends on is part of every job's setup, never a toggle.** The
  setup action places each one unconditionally at the path the dependency manifest declares, which
  the local bootstrap uses too, so the project-level install picks it up, and it requires the
  credentials that read it. Never add an input that opts a job into one, a condition that skips it
  when credentials are absent, or a second path for CI: one layout every job shares costs less than
  a matrix of variants, so a job that does not need the package still gets it. A `use-<capability>`
  toggle is for a capability that genuinely varies between jobs, never for the repository's own
  dependencies.
- Do not add glue steps that only read versions or forward setup data. Pass repository-owned version files and inputs directly to the action that uses them whenever supported.
- Keep workflow files concise: merge related setup and dependency commands into one clearly named generic step when their execution order and conditions allow it. Do not split tool or package installation into separate steps merely by dependency.
- Keep each workflow job's `name` plain static text. Do not interpolate matrix or other GitHub expressions into a job name: skipped matrix jobs display the source expression instead of a resolved label. Keep matrix values in the strategy and use a concise generic job name that remains readable in every job state.
- Name a workflow and its jobs the way the owner's other repositories name the same kind, such as a
  test workflow whose job runs over a suite matrix or a lint job, and for the role each serves
  across the repository, never for the one language, package or suite the repository holds today.
  Read those repositories' workflows before naming one.
- Environment configuration that tunes a tool — retry counts, timeouts, cache locations, path entries — belongs in the step that installs or runs that tool, not in a step of its own. A step whose whole body writes to `$GITHUB_ENV` is named for a concern rather than an action, and the reader has to look elsewhere to find out which later step it affects. Write those exports at the end of the owning step so the setting and its consumer stay together.
- Add an explanatory comment when an edge case requires an explicit version override.
- **A job that runs under a GitHub environment reads each secret and variable by one plain name**,
  and the environment supplies its value for that stage: `secrets.FEED_URL`, never
  `FEED_URL_STAGING` and `FEED_URL_PRODUCTION` selected by an expression on an input. A job that
  selects between such names is a defect, never a pattern to copy: it moves under `environment:`
  and reads the plain name.

- **Pull-request test jobs skip draft pull requests and run once one is marked ready for review**,
  so the pushes a draft takes while work is in flight start no test runs. The trigger's `types` add
  `ready_for_review` to `opened`, `synchronize`, and `reopened`, and each test job carries
  `if: github.event.pull_request.draft == false`. When a repository's pull-request test jobs still
  run on drafts, add this once, as a permanent workflow change in that repository's source pull
  request; never add it and revert it within a session. Cheaper non-test checks, such as lint, may
  keep running on drafts. This bounds what drafts cost and is never a way past a failing test: no
  test is skipped, disabled, or quarantined to reach green.

## Branches and Pull Requests

- When the user asks to list pull requests, use `list-prs`; its default scope is open pull requests created or worked on for the ongoing task, including handoffs and drafts across chats. Honor explicit scope and state requests.
- Record every pull request with `session-ledger` immediately after the hosting service returns its canonical URL. A task-scoped pull-request lookup reconciles verified task records through that ledger and verifies each selected URL remotely; never infer task membership from the current checkout, a branch name, a transcript, or a broad hosting-service search.

- **Open every pull request as a draft and keep it draft until it merges.** The user reviews it as
  a draft; it leaves draft once, as the first step of an authorized merge through `merge-gate`, so its
  test jobs run once, on the head about to merge. Never mark one ready to start its tests, to show
  it finished, or to hand it to the user; a follow-up keeps pushing to the draft.
- Keep pull requests focused and give them descriptive titles and descriptions; request appropriate reviewers when the repository workflow requires them.
- **A description is written from what is already known, never by re-reading the history.** The
  agent that did or coordinated the work writes it from its own record of the change, the existing
  description, `git log --oneline` subjects and `git diff --stat` against the base. It opens a commit
  or a file only to settle one line those leave unclear, and never walks commits one by one; a worker
  asked to write one is handed that change list in its brief.
- A pull request description covers the changes in that pull request and nothing else. Leave out alternatives considered and rejected, work deferred to a later change, and the reasoning behind not doing something.
- Treat each repository as an independent publishing context. PR titles, descriptions, comments,
  issue text, branch names and commit messages use the target repository's domain, contracts,
  changes and validation. Never cross-reference another repository's pull request or issue there,
  including by URL, qualified identifier, shorthand number, hand-off note or dependency disclosure.
  Dependencies create no exception. Keep cross-repository links, identities, implementation details,
  coordination and combined status in user chat and private task evidence.
- Before publishing or updating those artifacts, check the final text against the target
  repository's diff and evidence. Remove foreign references, including from dependency and delivery
  notes, and replace every example value the user supplied with an invented one, as the global
  rules' **Repository guidance** says. Describe a consumed interface or unresolved delivery
  requirement in terms of this repository's own contract; disclose provider PR links and merge
  ordering to the user in chat.
  `merge-gate` still owns the complete dependency inventory and readiness gate.
- **Each session opens its own source pull request in each repository.** Later source work in the
  same session joins that pull request rather than creating one per concern or worker. Continue a
  source pull request from another session only when the user, an applicable invoked skill, or a
  repository rule explicitly directs that continuation. A matching topic, existing branch, open
  state, or recorded touch does not supply that instruction. Verify the selected pull request's
  owner, state and scope before updating it; leave other sessions' pull requests and branches untouched.
- **Each session opens its own agent-configuration pull request in each repository.** Agent
  configuration is the canonical `.agents` tree — skills, each with its own scripts, assets and
  templates; rules; and agent definitions. Nonbehavioral text and guidance-reference corrections in
  agent hooks and installers also follow this workflow. Changes to execution, timing, installation,
  discovery, permissions or mutation scope remain source work. Everything else is source.
  Select an open pull request only when the current session's ledger records its creation receipt,
  or the user explicitly directs continuation of that pull request. A touch or reference receipt,
  matching topic, branch, open state or batch record alone does not establish creation or authorize
  continuation. Verify its state and scope remotely. If none qualifies, open a new pull request from
  the freshly fetched default branch. Later guidance edits and worker tasks join the selected pull
  request. Consolidate a duplicate this session opened onto it and close the duplicate, saying where
  the work went; never retarget, close or fold in one this session did not open.
- **Every worker pushes to the branch of the pull request the work continues**, fetching and
  rebasing its unpushed commits onto the remote branch before each push. A branch per worker,
  integrated later, is the same split with the integration deferred.
- **Guidance that is true only once a still-open source pull request merges goes on that pull
  request when the current session created it, as its ledger receipt proves, or the user explicitly
  directs its continuation**: it describes
  behavior that pull request introduces, drops guidance about something it removes, or needs a
  workflow or tool change it carries. It merges with the change that makes it true. Fold a separate
  agent-configuration pull request this session opened for such guidance into the source pull request
  and close it, saying where the work went. Otherwise the guidance joins the agent-configuration pull
  request selected above and is held until the source pull request merges, whether that source is in
  this repository or another. A dependency never authorizes continuing another session's pull request
  or opening a second agent-configuration pull request.
- **Every other agent configuration and source never share a branch**, even when a guidance change
  follows the source work checked out; a pull request found carrying both is split by moving one
  kind's files onto the pull request of that kind the work continues. Sharing one holds the guidance
  behind source review and outside the agent-configuration merge authorization below. This rule is
  the user's standing permission, when a harness or session designates one branch per repository and
  forbids pushing to any other without permission, to push to the branch of the pull request the
  work continues (`git push origin HEAD:<that-branch>`) without asking. Select that pull request
  under the source or agent-configuration ownership rule above. The other kind's new branch is the
  designated name with `-agents` or `-source` appended, created and pushed without asking.
- A new branch starts from the freshly fetched default branch; an agent-configuration branch
  never starts from a source branch. A skill or rule explicitly naming another base or an existing
  pull request keeps that route. Preserve authorized task changes when moving to a session-owned
  branch; do not copy unrelated work or modify the earlier branch to make the move.
- Never commit or push agent-authored changes directly to the default branch. Select the pull
  request under the ownership rules above before retaining a checkout's branch. If the checkout
  is on the default branch, detached, of the other kind, or owned by another session without a
  continuation instruction, move to the selected branch or create a descriptive non-default branch.

### Merge Authorization

- Agents may create branches and pull requests, commit, and push scoped changes without additional approval.
- Merging any pull request requires explicit user authorization in the current request or explicit
  applicable guidance in a rule or invoked skill for that pull request. A fix request, CI-test
  request, successful check, review, or request to implement a plan that lists a merge does not
  itself authorize merging. A reply that could be read as accepting a merge the agent offered, such
  as a bare "yes" beside another request, authorizes no merge it does not name. If neither
  authorization source applies, do not merge or enable auto-merge.
- Honor the selected workflow's delivery hold before the standing permissions below; a pull
  request held for user review cannot use those exceptions or auto-merge.
- Before asking for merge permission, classify the complete actual diff against the standing
  permissions below. A filename, extension, line count or change label is not a behavioral
  classification. Preserve genuine edits; never remove them merely to qualify for an exception.
- A pull request limited to minor type, lint, import, formatting or text corrections may merge
  without a separate request when it preserves intended product, security and contract behavior.
  Aligning types with an existing canonical contract qualifies. Mixed substantive changes require
  their existing explicit merge authority. Required checks and dependency admission remain; this
  permission grants no new product, credential, security or trust change and no deployment or release.
- A focused pull request may merge without a separate request when it repairs a lockfile defect
  demonstrated on the current default branch, or corrects a non-default testing reference to the
  maintained target selected by the user or repository guidance. Verify the complete diff consists
  only of that repair and its necessary manifest, lockfile or reference updates. Unrelated source
  changes need their own merge authorization; including a lockfile does not authorize a mixed
  pull request. Required validation and dependency admission still apply, subject to current user
  pauses and exclusions; this permission authorizes no deployment or release.
- A pull request confined to agent configuration — skills with their own scripts, assets and
  templates; rules; agent definitions; and static metadata — may be merged without a separate
  request once `code-simplify` has run and its findings are resolved and a skill's changed scripts
  pass the checks they own, such as a type check or a test render. One that adds a doctor skill
  waits instead for the user's review together with everything in its batch. A workflow, installer,
  or repository tooling outside a skill's folder is source work when its execution changes, even
  when it sits under `.agents`.
  When the user asked for the change to be tested, first run the skill test against the exact
  pull-request head. Check that the complete pull request remains confined to this agent
  configuration before using this exception.
- **An agent-configuration pull request whose guidance depends on a still-open source pull request is held until that merge**, whatever its other gates say, unless the guidance rides that source pull request under **Branches and Pull Requests**. Guidance true on the default branch as it stands waits for nothing.
- A hold does not authorize merging the source pull request or asking for its merge solely to unblock the agent-configuration pull request. Finish both pull requests' independent checks, report the dependency, and leave the source pull request reviewable until its merge is separately authorized. After the source pull request merges, continue the held one under the selection rule above: incorporate the updated base and rerun the affected gates before using the agent-configuration merge exception.
- When checks are still pending after those gates, auto-merge may be enabled for an eligible agent-configuration pull request; one held for a source pull request becomes eligible once that pull request has merged. Carry every in-scope agent-configuration pull request through conflict resolution, validation, draft readiness, and merge, when selected under the ownership rules above. Do not close or leave it open merely because it is draft or conflicts with the base; close only one this session opened, and only when its change is superseded or no longer wanted.
- An action-skill merge authorization applies only to its original target pull request, including one created during the skill's initial setup. Pull requests created afterward, including follow-up fixes, dependencies, replacements, and reapplications after a corrective revert, require separate current-request authorization, except each fix pull request a directly user-invoked skill's own authorization names, once that skill's merge gates pass; that authorization ends with the run.
- An authorized merge is not held for a failing check the current user explicitly waives or an
  established baseline exclusion under `pre-production`'s **Encountered Issues** classification.
  Name the check and its exclusion evidence in chat, then attempt the authorized merge without
  asking the user. Preserve that classification rather than excluding a required repair merely
  because the same failure also appears on the default branch.
- Apply established validation exclusions before repairing failures. An interrupted hosted check
  supplies no validation result for the work it did not complete. When the logs establish a
  runner or provider interruption without a validation failure, exclude the interrupted attempt
  if equivalent local validation passed for the proposed merge head. Record the run, the
  interruption evidence, and the matching local commands and results; do not rerun or wait merely
  to get a green hosted result. A recorded validation failure remains a failure even if the run
  was later canceled. Missing equivalent coverage must be obtained before merging. This
  exception applies only to hosted checks: a locally run validation failure caused by setup,
  dependency, checkout, proxy or certificate trust, or container build configuration is an
  encountered repository issue. Repair its canonical bootstrap or container build configuration and
  rerun it. If branch protection rejects the merge because it requires an excluded hosted
  interruption to pass, obtain the required hosted result. Never bypass branch protection.
- Never enable auto-merge for any other pull request unless the user explicitly authorizes it in the current request or an explicitly invoked skill requires it.
- If an agent mistakenly merges a pull request, it may auto-merge the focused revert pull request that corrects that erroneous merge without separate authorization.

### After Agent Sync

- **Refresh immediately after Agent Sync succeeds.** After a pull request that changes agent
  configuration merges and its default-branch Agent Sync run succeeds, complete the refresh below
  and verify the installed links before reporting delivery complete. The refresh is part of the
  merge's delivery, including when the merge is the session's final work. Report the installed
  source and commit, or the concrete blocker preventing refresh.
- The shared SessionStart hook repairs installation links on startup and resume after local pulls;
  it fetches remote updates only on installations that opt in and never rebuilds pending overlays.
  Use the refresh below when pending work needs reconciliation.
- Select the refresh route before checking local changes. When the repository supplies the installed
  shared skills, invoke `update-skills`; it keeps pending agent-configuration changes in effect,
  dirty checkouts and open pull requests alike. The checkout-only restriction below does not apply
  to this route. For the skill's first merge, read it from the merged commit before invoking it. A
  session follows the copy it loaded until this refresh completes.
- For every other repository, refresh its main local checkout, not a task worktree: if it is clean,
  check out its default branch and pull with `--ff-only`. Never discard or stash dirty files to force
  this checkout-only refresh; report a skipped refresh and leave them untouched.

## Comments

- **A comment, a review, a reply, a reaction, a thread resolution, and an edit or deletion of any of
  them go out under the user's account and read as the user speaking.** Post one only when the user
  asks for that post in the current request, or an invoked skill explicitly authorizes that kind of
  post on that pull request or issue.
- A harness default, an event's handling guidance, a failing check, or a system notice is never that
  authorization, even when it says a wake ends in a comment. Put the text the post would have carried
  in chat instead, and say where it would have gone.

## Commits

- Use conventional commit messages when applicable and keep commits atomic and focused.
- Commit each small coherent step and push it promptly once the pre-push checks **Pre-Push Gate** defines pass, sub-agents included; work only one machine holds is lost with it.
- Do not commit generated files unless the repository explicitly requires them.

## Dependency Installation

- Declare project dependencies used by workflows in the repository's dependency manifests and commit their lockfiles.
- Run project-level installation commands such as `poetry install` or `npm install` in workflows.
- Do not install individual project packages or embed their versions directly in workflow commands.

## Repository Artifact Text

- Write repository artifact text for its reader: describe behavior, configuration, contracts and
  validation, without narrating the task that produced it. This includes action and workflow
  metadata, configuration descriptions, code comments, documentation, commit messages and
  pull-request text. Do not add attribution to user requests, approvals or agent compliance, such
  as “as requested” or “per your instructions”; apply the instruction to the result itself.
  Record an exchange only when the user explicitly asks to document that exchange, in a document
  whose purpose is that record.

### README

- A README's reader is a person using or developing the project, so a README holds what the
  project is, how to run or use it, where a developer finds its parts, and a Local Development
  section with the commands to install, run, and validate it locally. Anything only an agent acts on
  goes in the repository's rules and skills instead, with repository-specific facts in
  `.agents/project.md` or a reference it points to: an environment variable or credential an agent
  session reads, even one a person adds to a cloud environment for the agent; a tool installed for
  agents; a procedure only agents follow.
- After drafting or editing READMEs and other reference documentation, compare each statement with
  the current capabilities and required steps. When their positive description already communicates
  the operation, delete corresponding claims about absent behavior or unneeded operations,
  including positive paraphrases. Retain a limitation only when it contributes a supported input,
  option, constraint or required step not otherwise stated. Remove historical comparisons. Describe
  available capabilities without assuming how consumers will use the project or framing guidance as
  prohibitions such as "never do X."
- Remove repeated explanations and prefer short sections, bullets, tables, and focused examples over long prose.
- **Order sections for a reader arriving cold, never by what landed most recently.** A section goes
  where its vocabulary is already established: one whose examples are all of some construct follows
  the section that introduces that construct, however central the behavior it describes is.
- A section grown into a wall of prose carries rules a table states better: move those rules into a
  table and leave the prose only what a table cannot say, such as caveats, reasons and exceptions.
- Write in plain language, as if explaining the repository to a colleague. Avoid repeating internal
  terms such as `canonical`; name the file or say `source` when that is clearer.

- Write the top-level heading in every `README.md` in title case.
- Convert slug-style project names into readable words, such as `example-service` becoming `Example Service`.

#### GitHub Actions And Libraries

- Lead with the consumer-facing purpose; do not state that an action or library is reusable when that is already evident from the project.
- Place a concise, list-based Features section immediately after the introduction.
- Include little to no implementation or internal technical detail; describe public capabilities and outcomes instead.
- Follow Features with an Example or Examples section.
- Introduce each example with a one- or two-line description of its purpose, followed by a small code example.
- In cron-based examples, use a conventional schedule such as every Monday and add an inline comment translating the cron expression into that plain-language schedule.
- For reusable GitHub Actions, include an Inputs table with the input name, default value, and purpose.

## Pre-Push Gate

Every push goes out once the pre-push checks below pass, on a draft and on a pull request ready for
review alike. Follow an explicitly selected workflow’s own declared check sequence and delivery
constraints where it specifies them; nothing holds committed work on one machine — not a gate, review or simplification
pass pending on it, an integration merge, or a plan that orders one first. The one exception is
commits that `lock-revision`'s **After Locking** hold keeps local until the user lets revisions
resume. `code-simplify` and `acceptance-gate` do not run per push; `execute-task` and `review-pass`
set when they run. A fix pushed for a flag a review or gate raised is checked
by the agent that made it: it re-reads the changed lines against the flag and reruns the checks
covering that code, unless `acceptance-gate`'s **Bounds** send it to a fresh gate; that recorded
check, or that gate's verdict, is what other skills mean by an increment's **Pre-Push Gate** verdict.

Read the shared testing rule before planning test runs or briefing an implementation worker.
Its **Verification Cadence** governs tests, builds, browser walkthroughs and reviews, including
pre-push checks. Deferred feature verification does not hold an intermediate push and remains
required afterward, and a suite still running holds none either: the testing rule's superseded-run
bullet says what happens to it. Run the relevant batch after the feature is complete, then the required final
checks before delivery; retain evidence that the change has not invalidated.

- **Required checks use CI’s commands and scope, at the verification checkpoints above.** Read
  the workflow files that trigger on a pull request and run every checking job that can run
  locally — lint, format, type checks, build, tests, generated-output drift, docs or coverage
  checks — with the job's own command and scope, plus any check a skill in use requires. Do not
  restart the batch for each push; retain results whose code and inputs remain unchanged. Project
  guidance that lists those commands is a shortcut to the workflows, never a
  substitute; where the two disagree, the workflow is right. A job that needs a hosted service or a
  running stack, or is too slow to run before every push, joins the slow verification below and is
  named in the report. Room on this machine never leaves a job to its hosted run: a shortage of
  disk, memory or ports is recovered as the global rules' local-stack bullet says, and the job runs
  here. Only a hosted service or credentials the session lacks, each established as the testing
  rules' cannot-run bullet says, or runner-specific behavior does.
- **A local variant of a CI check is not that check**, and each of these passes locally and fails
  in CI: lint or type checks scoped to the changed files, where CI's whole-tree run finds an import
  another change left unused in a file the branch never touched; a formatter or linter in write
  mode, which rewrites what CI's check mode reports; a tool at a version or with a config other than
  the one CI resolves; a job left out because the diff looks unrelated to it, such as a
  generated-output drift check or a whole-tree check that every shared component has a docs page.

Before each push, list the exact adjacent line pairs where setup, a guard, transformation, side effect,
or return meets the next phase without the blank line required by the global code-layout rule.
For changed Python files, `review-pass`'s `paragraph_candidates.py` script lists the candidate pairs.
Fix every listed boundary in the lines the change writes or edits, and elsewhere in the changed files
within `pre-production`'s incidental size budget, as the global code-layout rule says; an unrelated
bug or a passing formatter does not satisfy this spacing check.

- **Commit each small coherent step and push it as soon as its checks pass**, and at least every
  five minutes of work — a function and its callers updated, a test brought to pass, one finding
  fixed — never at the end of a unit or task. Define coherence against `pre-production`'s
  complete target boundary, not the latest edited files: required consumer updates, superseded
  owners and declarations, generated contracts and retained-data migration are implementation,
  never later cleanup. An intermediate push may preserve ongoing work; it neither narrows the
  remaining obligation nor qualifies that feature for completion, review delivery or rollout.
  A push is what lets the user review and test the work, and the only copy that
  outlives the machine: a recycled container or an ended session takes every commit and edit no
  remote holds.
- **Nothing outside the change holds a push, a check or a walkthrough, or becomes a question about
  pushing or merging.** A dependency
  still in review in another repository, an unreleased package version, a sibling pull request not
  yet merged, CI expected to stay red until one of those lands: the branch consumes the
  dependency's pull-request branch, or its default branch once merged — in the manifest, the
  lockfile and any workflow checkout, as the global rules' version-reference bullet allows while
  developing — or builds on a same-repository sibling's branch as the GitHub rule's branch bullets
  set out, and pushes. Every build, test and walkthrough runs against that checked-in reference,
  never a local copy the manifest does not name. A consumer that cannot build until its dependency
  merges is a manifest still naming the default branch: point it at the pull-request branch, never
  ask for the dependency's merge or report the consumer blocked on it. Which branch it consumes,
  and a red check that dependency explains, are
  surfaced in user chat under the GitHub rule's independent publishing context rather than waited on; adopting
  its maintained delivery target is named work for when the dependency merges.
- **No edit sits uncommitted through a long wait outside the checks.** Before the slow verification
  below, a background worker, CI on the pushed head, or a question to the user, bring the work to a
  coherent step, commit it, and push it; the checks' own runs are part of the push, not such a wait.
- **Delegated edits run at this cadence.** A brief handing a worker edits states it, names the
  branch the worker pushes to — the branch of the pull request the work continues, under **Branches and Pull Requests** — and names the exact files to change, under `subagent-matrix`'s **Dispatch**. The
  worker pushes each step once its checks pass and reports the branch and head. The brief has the
  worker fix every defect it meets, in the product or the repository's tooling, and report as left
  alone only cleanup past `pre-production`'s size budget and any item
  `pre-production`'s scope bullets leave to the user. The delegating agent reads that head under
  the global rules’ **Reported Outcomes** before any dependent work starts. The worker
  ends with nothing uncommitted and nothing unpushed beyond the **Pre-Push Gate**'s one exception,
  never amends or rebases a pushed commit, and
  its report names the branch and head.
- **Pull requests stay draft until the authorized merge gate readies them**, so these pushes may
  start no test jobs. Readiness can enqueue duplicate hosted jobs without changing the head;
  `merge-gate` decides whether completed exact-head evidence is equivalent before it waits for
  fresh coverage. The local checks above are what stand between a push and hosted validation.
- **The order is change, checks, push, then the slow verification**: a browser walkthrough, a full
  or end-to-end suite, a run against a service without the change, root-causing a failure seen
  along the way — anything slow or needing a running stack. What it finds goes out as fix pushes, each once its checks pass.
- **Pushed is not done**: the change is reported done only once that verification has passed.
