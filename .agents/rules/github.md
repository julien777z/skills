---
description: Follow shared workflow, branch, pull-request, and commit conventions for GitHub repositories.
alwaysApply: true
---

# GitHub Rules

## Workflows

- Treat a request for CI tests as authorization for test workflows only. Inspect a workflow's jobs
  and triggers before dispatching it; a workflow that builds and publishes artifacts or deploys is
  a release action even if it also runs tests.

- Keep `run` steps declarative. Invoke checked-in scripts for control flow, validation, filesystem changes, or other implementation logic instead of embedding arbitrary shell or program code in workflow YAML; place those scripts under `.github/scripts/` and prefer Python.
- Do not hard-code runtime versions when a shared action, reusable workflow, or repository version file supplies them; omit `python-version` when shared Python automation provides it, and use `node-version-file: ".nvmrc"` for Node.js workflows.
- Do not add glue steps that only read versions or forward setup data. Pass repository-owned version files and inputs directly to the action that uses them whenever supported.
- Keep workflow files concise: merge related setup and dependency commands into one clearly named generic step when their execution order and conditions allow it. Do not split tool or package installation into separate steps merely by dependency.
- Environment configuration that tunes a tool — retry counts, timeouts, cache locations, path entries — belongs in the step that installs or runs that tool, not in a step of its own. A step whose whole body writes to `$GITHUB_ENV` is named for a concern rather than an action, and the reader has to look elsewhere to find out which later step it affects. Write those exports at the end of the owning step so the setting and its consumer stay together.
- Add an explanatory comment when an edge case requires an explicit version override.

## Branches and Pull Requests

- Keep pull requests focused and give them descriptive titles and descriptions; request appropriate reviewers when the repository workflow requires them.
- A pull request description covers the changes in that pull request and nothing else. Leave out alternatives considered and rejected, work deferred to a later change, and the reasoning behind not doing something.
- Treat each repository as an independent context. Write PR titles, descriptions, review comments, and issue comments using only the target repository's domain, contracts, changes, and validation. Do not import another repository's product names, domain knowledge, implementation details, or coordination history; do not name or link its PRs or post cross-repository coordination comments. Keep combined status and coordination in user chat.
- Before publishing or updating those artifacts, check the final text against the target repository's diff and evidence. Remove foreign domain references and cross-repository PR links, even when the work shares a session or motivated this change.
- **A session delivers at most two pull requests per repository: one for source and one for agent configuration.** Agent configuration is the canonical `.agents` tree — skills, rules, and agent definitions; everything else is source. Every later piece of work in that repository — a follow-up, a guidance change, a copy sweep, a fix found along the way — joins the open pull request of its kind, even when it could be reviewed independently or feels like a different kind of work; those two kinds are the only split. Before creating a branch, query the session's open pull requests in that repository and the current branch's. Open a second pull request of one kind only when the user asks or the first has merged; a pull request per concern leaves the user reconciling several reviews of one piece of work. One already opened is not kept: move its commits onto the pull request of its kind in flight and close it, saying where the work went.
- **Agent configuration and source never share a branch**, even when a guidance change follows the source work checked out; a pull request found carrying both is split by moving one kind's files onto the pull request of that kind. Sharing one holds the guidance behind source review and outside the agent-configuration merge authorization below.
- A new branch starts from the default branch, or, while a pull request the user named as holding their current work stays open, from that pull request's branch when it is of the same kind; an agent-configuration branch never starts from a source branch. A skill whose contract names its own base keeps it. A branch already carrying another open pull request's unmerged commits is stacked on that pull request: keep those commits, build on top of them, and open its pull request against that pull request's branch. Restarting a stacked branch from the default branch drops the work it was built on, and nothing reports the loss.
- Never commit or push agent-authored changes directly to the default branch. If the checkout is on the default branch, detached, or on a branch of the other kind, move to the session's open branch of the work's kind or, with none, create a descriptive non-default branch; otherwise retain the current branch and deliver through its pull request.

### Merge Authorization

- Agents may create branches and pull requests, commit, and push scoped changes without additional approval.
- Merging any pull request requires explicit user authorization in the current request or explicit
  applicable guidance in a rule or invoked skill for that pull request. A fix request, CI-test
  request, successful check, review, or request to implement a plan that lists a merge does not
  itself authorize merging. If neither authorization source applies, do not merge or enable auto-merge.
- A pull request confined to canonical agent configuration, including skills, rules, and agent definitions, may be merged without a separate request after `code-simplify` has run and its findings are resolved. For substantial guidance changes or changes to executable logic, first run the relevant smoke test against the exact pull-request head. Check that the complete pull request remains confined to agent configuration before using this exception. Guidance that describes behaviour a still-open source pull request introduces, or needs a workflow or tool change it carries — a project guidance paragraph about a helper that branch adds, say — merges only after that source pull request has merged; guidance that holds on the default branch as it stands waits for nothing.
- When checks are still pending after those gates, auto-merge may be enabled for an eligible agent-configuration pull request; one held for a source pull request becomes eligible once that pull request has merged. Carry every in-scope agent-configuration pull request through conflict resolution, validation, draft readiness, and merge, including one begun by another task. Do not close or leave it open merely because it is draft or conflicts with the base; close only when its change is superseded or no longer wanted.
- An action-skill merge authorization applies only to its original target pull request, including one created during the skill's initial setup. Pull requests created afterward, including follow-up fixes, dependencies, replacements, and reapplications after a corrective revert, require separate current-request authorization, except each batch pull request a skill declaring merged-batch delivery opens during its run, once that skill's merge gates pass; that authorization ends with the run.
- An authorized merge is not held for a failing check the pull request did not cause: one that fails the same way on the base branch, or whose failing test or log line shows behavior the diff does not reach. Name the check and that evidence in chat, then merge without asking the user. A check that branch protection requires still blocks and is never bypassed; report it as the blocker.
- Never enable auto-merge for any other pull request unless the user explicitly authorizes it in the current request or an explicitly invoked skill requires it.
- If an agent mistakenly merges a pull request, it may auto-merge the focused revert pull request that corrects that erroneous merge without separate authorization.

### After Agent Sync

- After a pull request that changes agent configuration merges and its default-branch Agent Sync run finishes, update the repository's main local checkout, not a task worktree: if it is clean, check out its default branch and pull with `--ff-only`. Never discard or stash dirty files to force the refresh; report a skipped refresh and leave them untouched.
- When the merged repository is the skills repository, update the installed copy the session loads its skills and rules from the same way, rerun the installer its README names so new skills link, and re-read the rules the merge changed. A session follows the copy it loaded until then, including rules other sessions merged after it started.

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
- Do not commit generated files unless the repository explicitly requires them.

## Dependency Installation

- Declare project dependencies used by workflows in the repository's dependency manifests and commit their lockfiles.
- Run project-level installation commands such as `poetry install` or `npm install` in workflows.
- Do not install individual project packages or embed their versions directly in workflow commands.

## README

- Describe available capabilities without assuming how consumers will use the project or framing guidance as prohibitions such as "never do X."
- Remove repeated explanations and prefer short sections, bullets, tables, and focused examples over long prose.

### GitHub Actions And Libraries

- Lead with the consumer-facing purpose; do not state that an action or library is reusable when that is already evident from the project.
- Place a concise, list-based Features section immediately after the introduction.
- Include little to no implementation or internal technical detail; describe public capabilities and outcomes instead.
- Follow Features with an Example or Examples section.
- Introduce each example with a one- or two-line description of its purpose, followed by a small code example.
- In cron-based examples, use a conventional schedule such as every Monday and add an inline comment translating the cron expression into that plain-language schedule.
- For reusable GitHub Actions, include an Inputs table with the input name, default value, and purpose.
- Include a Local Development section with the commands needed to install, run, and validate the project locally.

### Titles

- Write the top-level heading in every `README.md` in title case.
- Convert slug-style project names into readable words, such as `example-service` becoming `Example Service`.
