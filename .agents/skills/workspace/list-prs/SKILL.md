---
name: list-prs
description: Before a repository-wide pull-request query, use when a user asks to list, show, or link pull requests — including "list the open PRs", "open PRs", "current PRs", and "what PRs are open". By default, reconcile the task ledger and list open PRs created or worked on for the ongoing task, including handoff PRs and drafts across its chats. Honor explicit scope and state requests.
short_description: 'List the ongoing task’s open PRs.'
---

# List Pull Requests

Return a deduplicated list of open pull requests created or worked on for the entire ongoing task,
including work continued from a handoff or earlier chat. Honor explicit scope and state requests.

## Dependencies

- `session-ledger` — provides the task's verified pull-request records and reconstructs missing entries.

## Workflow

1. Retrieve the task's pull-request records through `session-ledger`. Reconcile them with available
   task metadata, artifact receipts, and continuation or handoff records, including delegated
   creation and touch receipts. Have `session-ledger` reconstruct missing entries from verified
   task evidence before filtering. A missing or partial cache does not establish a complete ledger
   or an empty result; when evidence remains unavailable, report the incomplete lookup instead of
   returning a complete list or `- None`.
2. Select pull requests created or worked on for this task, whether recorded as created or touched.
   Include pre-existing pull requests the task continued, updated, reviewed, reopened, or resolved
   conflicts in. A reference or example alone does not make a pull request task work. Do not infer
   task membership from a directory, branch, author, date, or repository-wide search. Broaden scope
   beyond the task only when explicitly requested.
3. Verify each selected canonical URL with read-only hosting-service tooling. Default to currently
   open pull requests, including drafts and ready-for-review pull requests. Include closed or
   merged pull requests only when the requested state includes them.
4. Deduplicate canonical URLs in first-recorded order. If the reconciled, verified records contain
   no qualifying pull requests, return `- None`.

## Output

Return only this heading and Markdown list, with no status summary or extra prose. For an incomplete
lookup, replace the URL list with one bullet naming the unavailable task evidence.

```markdown
Pull requests

- https://github.com/owner/repository/pull/123
```
