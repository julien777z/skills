---
description: Follow shared workflow, branch, pull-request, and commit conventions for GitHub repositories.
alwaysApply: true
---

# GitHub Rules

## Workflows

- Treat a request for CI tests as authorization for test workflows only. Inspect a workflow's jobs
  and triggers before dispatching it; a workflow that builds and publishes artifacts or deploys is
  a release action even if it also runs tests.

- Build, publish, and deploy through the repository's GitHub Actions workflow, never a local CLI.
  Before changing a workflow, inspect its `workflow_dispatch` trigger and the GitHub Actions **Run
  workflow** controls. For an authorized branch deployment, use the existing workflow in its supported
  dispatch mode: select the pull-request branch or exact ref when offered, or run the default-branch
  workflow with its documented source-ref input when that is how it deploys a revision. Only when no
  existing manual-dispatch path can deploy the requested ref may a temporary workflow change add the
  smallest allowance. Verify the exact workflow run and deployed revision, then remove that allowance
  in the same pull request before reporting the result.

- Keep `run` steps declarative. Invoke checked-in scripts for control flow, validation, filesystem changes, or other implementation logic instead of embedding arbitrary shell or program code in workflow YAML; place those scripts under `.github/scripts/` and prefer Python.
- Do not hard-code runtime versions when a shared action, reusable workflow, or repository version file supplies them; omit `python-version` when shared Python automation provides it, and use `node-version-file: ".nvmrc"` for Node.js workflows.
- Do not add glue steps that only read versions or forward setup data. Pass repository-owned version files and inputs directly to the action that uses them whenever supported.
- Keep workflow files concise: merge related setup and dependency commands into one clearly named generic step when their execution order and conditions allow it. Do not split tool or package installation into separate steps merely by dependency.
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

- **Open every pull request as a draft and keep it draft while work continues.** It leaves draft
  once, when the work is finished, through `execute-task`'s **Completion** or a workflow that
  merges it; never mark one ready early to start its tests. Work that resumes changing a pull
  request already ready for review converts it back to draft before its first push — GraphQL
  `convertPullRequestToDraft`, which REST does not offer — and **Completion** readies it again; a
  skill driving a ready pull request's checks, such as `merge-pr` or `ci-watch`, keeps it ready.
- Keep pull requests focused and give them descriptive titles and descriptions; request appropriate reviewers when the repository workflow requires them.
- **A description is written from what is already known, never by re-reading the history.** The
  agent that did or coordinated the work writes it from its own record of the change, the existing
  description, `git log --oneline` subjects and `git diff --stat` against the base. It opens a commit
  or a file only to settle one line those leave unclear, and never walks commits one by one; a worker
  asked to write one is handed that change list in its brief.
- A pull request description covers the changes in that pull request and nothing else. Leave out alternatives considered and rejected, work deferred to a later change, and the reasoning behind not doing something.
- Treat each repository as an independent context. Write PR titles, descriptions, review comments, and issue comments using only the target repository's domain, contracts, changes, and validation. Do not import another repository's product names, domain knowledge, implementation details, or coordination history; do not name or link its PRs or post cross-repository coordination comments, except a hand-off comment naming a pull request the work depends on. Keep combined status and coordination in user chat.
- Before publishing or updating those artifacts, check the final text against the target repository's diff and evidence. Remove foreign domain references and cross-repository PR links, even when the work shares a session or motivated this change.
- **New work in a repository joins the open pull request of its kind that the work continues,
  whichever session opened it, and never gets a pull request of its own, stacked or not.** The two
  kinds are source and agent configuration: agent configuration is the canonical `.agents` tree —
  skills, rules, and agent definitions; everything else is source. Every later piece of work in that
  repository — a follow-up, a guidance change, a copy sweep, a fix found along the way, a worker's
  task — joins that pull request, even when it could be reviewed independently or feels
  like a different kind of work; those two kinds are the only split. Before creating a branch, list
  the repository's open pull requests, not only this session's: one an earlier session or a handoff
  opened for the work this session continues is the pull request that work joins. Work that
  continues none gets one new pull request of its kind from the default branch, and the session's
  later work of that kind joins it. Open another only when the user asks for it in their own words
  or the first has merged; a brief, a handoff spec, or a plan asking for a new branch or pull
  request is not the user asking. A pull request per concern leaves the user reconciling several
  reviews of one piece of work. One this session opened beside it is not kept: move its commits onto
  the pull request the work continues and close it, saying where the work went. A pull request the
  session did not open is never retargeted, closed or folded in, including one the continued pull
  request is stacked on: that stack and its bases are the user's structure.
- **Every worker pushes to the branch of the pull request the work continues**, fetching and
  rebasing its unpushed commits onto the remote branch before each push. A branch per worker,
  integrated later, is the same split with the integration deferred.
- **Agent configuration and source never share a branch**, even when a guidance change follows the
  source work checked out; a pull request found carrying both is split by moving one kind's files
  onto the pull request of that kind the work continues. Sharing one holds the guidance behind
  source review and outside the agent-configuration merge authorization below. This rule is the
  user's standing permission, when a harness or session designates one branch per repository and
  forbids pushing to any other without permission, to push to the branch of the pull request the
  work continues (`git push origin HEAD:<that-branch>`) without asking. The designated branch opens a
  pull request only for work that continues none, carrying the first such kind the session delivers
  in that repository; the other kind's new branch is that name with `-agents` or `-source`
  appended, created and pushed without asking.
- A new branch starts from the default branch; an agent-configuration branch never starts from a
  source branch. A skill whose contract names its own base keeps it. Work that builds on an open
  pull request's unmerged commits is pushed to that pull request's branch, never to a new branch
  stacked on it with a pull request of its own. Restarting such work from the default branch drops
  the commits it was built on, and nothing reports the loss.
- Never commit or push agent-authored changes directly to the default branch. If the checkout is on
  the default branch, detached, or on a branch of the other kind, move to the branch of the pull
  request the work continues or, with none, create a descriptive non-default branch; otherwise
  retain the current branch and deliver through its pull request.

### Merge Authorization

- Agents may create branches and pull requests, commit, and push scoped changes without additional approval.
- Merging any pull request requires explicit user authorization in the current request or explicit
  applicable guidance in a rule or invoked skill for that pull request. A fix request, CI-test
  request, successful check, review, or request to implement a plan that lists a merge does not
  itself authorize merging. If neither authorization source applies, do not merge or enable auto-merge.
- A pull request confined to canonical agent configuration, including skills, rules, and agent definitions, may be merged without a separate request after `code-simplify` has run and its findings are resolved. When the user asked for the change to be tested, first run the smoke test against the exact pull-request head. Check that the complete pull request remains confined to agent configuration before using this exception.
- **An agent-configuration pull request whose guidance is true only once a still-open source pull request has merged is held until that merge**, whatever its other gates say: it describes behaviour that pull request introduces, drops guidance about something it removes, or needs a workflow or tool change it carries — a project guidance bullet about a helper the source branch adds is the common case. Guidance true on the default branch as it stands waits for nothing.
- A hold does not authorize merging the source pull request or asking for its merge solely to unblock the agent-configuration pull request. Finish both pull requests' independent checks, report the dependency, and leave the source pull request reviewable until its merge is separately authorized. After that merge, incorporate the updated base and rerun the affected gates before using the agent-configuration merge exception.
- When checks are still pending after those gates, auto-merge may be enabled for an eligible agent-configuration pull request; one held for a source pull request becomes eligible once that pull request has merged. Carry every in-scope agent-configuration pull request through conflict resolution, validation, draft readiness, and merge, including one begun by another task. Do not close or leave it open merely because it is draft or conflicts with the base; close only one this session opened, and only when its change is superseded or no longer wanted.
- An action-skill merge authorization applies only to its original target pull request, including one created during the skill's initial setup. Pull requests created afterward, including follow-up fixes, dependencies, replacements, and reapplications after a corrective revert, require separate current-request authorization, except each batch pull request a skill declaring merged-batch delivery opens during its run, once that skill's merge gates pass; that authorization ends with the run.
- An authorized merge is not held for a failing check the current user explicitly waives or for the same failure on the repository's default branch. Name the check and the user instruction or default-branch evidence in chat, then attempt the authorized merge without asking the user. A failure that appears outside the diff but is green on the default branch is not exempt.
- A hosted check stopped by runner or provider infrastructure before its test, lint, or other validation command begins is skipped automatically when the applicable locally runnable validation has passed. Record the run, the log signal proving validation did not begin (or the provider infrastructure error), and the local commands that cover it; do not rerun or wait merely to get a green hosted result. This exception applies only to hosted checks: a locally run validation failure caused by setup, dependency, checkout, proxy or certificate trust, or container build configuration is an encountered repository issue. Repair its canonical bootstrap or container build configuration and rerun it. A cancellation after validation begins, a log naming a product or test failure, or behavior without passing local coverage remains a blocker. Only an actual provider rejection because branch protection requires an excluded or skipped check holds the pull request; report that rejection and its evidence and never bypass it.
- Never enable auto-merge for any other pull request unless the user explicitly authorizes it in the current request or an explicitly invoked skill requires it.
- If an agent mistakenly merges a pull request, it may auto-merge the focused revert pull request that corrects that erroneous merge without separate authorization.

### After Agent Sync

- After a pull request that changes agent configuration merges and its default-branch Agent Sync
  run finishes, select the refresh route before checking local changes. When the repository supplies
  the installed shared skills, invoke `reconcile-skills`; its preservation workflow governs dirty
  checkouts as well as clean ones. The checkout-only restriction below does not apply to this route.
  For the skill's first merge, read it from the merged commit before invoking it. A session follows
  the copy it loaded until this refresh completes.
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
- Commit each small coherent step and push it promptly once the pre-push checks `execute-task`'s
  **Pre-Push Gate** defines pass, sub-agents included; work only one machine holds is lost with it.
- Do not commit generated files unless the repository explicitly requires them.

## Dependency Installation

- Declare project dependencies used by workflows in the repository's dependency manifests and commit their lockfiles.
- Run project-level installation commands such as `poetry install` or `npm install` in workflows.
- Do not install individual project packages or embed their versions directly in workflow commands.

## Documentation

- Do not turn user exchanges, questions, clarifications, or explanations of a misunderstanding into README or other documentation content unless the user explicitly asks to document them. Apply settled instructions to the work; update independently required setup and configuration facts without narrating the exchange that prompted them.

### README

- A README's reader is a person using or developing the project, so a README holds what the
  project is, how to run or use it, where a developer finds its parts, and a Local Development
  section with the commands to install, run, and validate it locally. Anything only an agent acts on
  goes in the repository's rules and skills instead, with repository-specific facts in
  `.agents/project.md` or a reference it points to: an environment variable or credential an agent
  session reads, even one a person adds to a cloud environment for the agent; a tool installed for
  agents; a procedure only agents follow.
- Describe available capabilities without assuming how consumers will use the project or framing guidance as prohibitions such as "never do X."
- Remove repeated explanations and prefer short sections, bullets, tables, and focused examples over long prose.
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
