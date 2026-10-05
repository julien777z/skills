---
name: list-prs
description: Before a repository-wide pull-request query, use when a user asks to list, show, or link pull requests — including "list the open PRs", "open PRs", "current PRs", and "what PRs are open". By default, use the session ledger and list only session-created PRs still open, including drafts; widen to pre-existing or repository-wide PRs only when the user explicitly asks.
short_description: 'List the current session’s open PRs.'
---

# List Pull Requests

Return a deduplicated list of currently open pull requests created during the entire current session, not only the latest turn. Honor an explicitly requested broader scope.

## Dependencies

- `session-ledger` — provides the task's verified pull-request records.

## Workflow

1. Retrieve pull-request creation records from `session-ledger` in first-recorded order.
2. Include only records created during this session. Updating, reviewing, reopening, resolving conflicts in, or working on a pre-existing pull request does not create a session record. Include pre-existing pull requests only when the user explicitly requests a broader scope.
3. Verify each recorded canonical URL with read-only hosting-service tooling. Include draft and ready-for-review pull requests only while their current state is open. Exclude merged and closed pull requests.
4. Deduplicate canonical URLs while preserving creation order. If no pull requests qualify, return `- None`.

## Output

Return only this heading and Markdown list, with no status summary or extra prose:

```markdown
Pull requests

- https://github.com/owner/repository/pull/123
```
