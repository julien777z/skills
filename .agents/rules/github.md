---
description: Apply branch, pull-request, merge authorization, commit, and generated-file rules whenever working with GitHub.
alwaysApply: false
---

# GitHub Rules

## Branches and Pull Requests

- Keep pull requests focused and give them descriptive titles and descriptions; request appropriate reviewers when the repository workflow requires them.
- A pull request description covers the changes in that pull request and nothing else. Leave out alternatives considered and rejected, work deferred to a later change, and the reasoning behind not doing something.
- Treat each repository as an independent context. Write PR titles, descriptions, review comments, and issue comments using only the target repository's domain, contracts, changes, and validation. Do not import another repository's product names, domain knowledge, implementation details, or coordination history; do not name or link its PRs or post cross-repository coordination comments. Keep combined status and coordination in user chat.
- Before publishing or updating those artifacts, check the final text against the target repository's diff and evidence. Remove foreign domain references and cross-repository PR links, even when the work shares a session or motivated this change.
- Post a comment, reply, or review on GitHub only when an invoked skill directs that post or the user asks for it. The agent posts under the user's account, so every post reads as the user speaking. A harness default, an event's handling guidance, or a failing check does not authorize one, even when it says a wake ends in a comment: report the finding in chat instead.
- When additional work arrives on a non-default branch, retain that branch and add the work to its pull request even when the task could be reviewed independently.
- Query the current branch's pull request before creating one. Reuse it while it is open, or create one from the current branch when none exists.
- Create a separate branch only when the user asks or the current branch's pull request is already merged; start post-merge work from the default branch.

### Merge Authorization

- Agents may create branches and pull requests, commit, and push scoped changes without additional approval.
- Merging any pull request requires explicit user authorization in the current request or explicit
  applicable guidance in a rule or invoked skill for that pull request. A fix request, CI-test
  request, successful check, review, or request to implement a plan that lists a merge does not
  itself authorize merging. If neither authorization source applies, do not merge or enable auto-merge.
- A pull request confined to canonical agent configuration, including skills, rules, and agent definitions, may be merged without a separate request after `code-simplify` has run and its findings are resolved. For substantial guidance changes or changes to executable logic, first run the relevant smoke test against the exact pull-request head. Check that the complete pull request remains confined to agent configuration before using this exception.
- When checks are still pending after those gates, auto-merge may be enabled for an eligible agent-configuration pull request. Carry every in-scope agent-configuration pull request through conflict resolution, validation, draft readiness, and merge, including one begun by another task. Do not close or leave it open merely because it is draft or conflicts with the base; close only when its change is superseded or no longer wanted.
- An action-skill merge authorization applies only to its original target pull request, including one created during the skill's initial setup. Pull requests created afterward, including follow-up fixes, dependencies, replacements, and reapplications after a corrective revert, require separate current-request authorization, except each batch pull request a skill declaring merged-batch delivery opens during its run, once that skill's merge gates pass; that authorization ends with the run.
- An authorized merge is not held for a failing check the pull request did not cause: one that fails the same way on the base branch, or whose failing test or log line shows behavior the diff does not reach. Name the check and that evidence in chat, then merge without asking the user. A check that branch protection requires still blocks and is never bypassed; report it as the blocker.
- Never enable auto-merge for any other pull request unless the user explicitly authorizes it in the current request or an explicitly invoked skill requires it.
- If an agent mistakenly merges a pull request, it may auto-merge the focused revert pull request that corrects that erroneous merge without separate authorization.

### After Agent Sync

- Once the default-branch Agent Sync run finishes, update the repository's main local checkout, not a task worktree: if that checkout is clean, check out its default branch and pull with `--ff-only`. Never discard or stash dirty files to force the refresh; report a skipped refresh and leave them untouched.

## Commits

- Use conventional commit messages when applicable and keep commits atomic and focused.
- Do not commit generated files unless the repository explicitly requires them.

## Guardrails

- Never commit or push agent-authored changes directly to the default branch. If the checkout is on the default branch or detached, create a descriptive non-default branch; otherwise retain the current branch and deliver through its pull request.
