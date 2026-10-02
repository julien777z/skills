---
name: list-prs
description: Use when asked which pull requests are open or for links to them. By default, list currently open pull requests created during the entire current session, including drafts; widen the scope only when the user explicitly requests it.
short_description: 'List currently open pull requests created during the entire current session, including drafts.'
---

# List Pull Requests

Return a deduplicated list of currently open pull requests created during the entire current session, not only the latest turn. Honor an explicitly requested broader scope.

## Workflow

1. Build a session-wide pull-request ledger from the conversation, tool history, compacted summaries, GitHub results, and current branch associations.
2. Include pull requests created during this session. Updating, reviewing, reopening, resolving conflicts in, or working on a pre-existing pull request does not make it session-created. Include those only when the user explicitly requests a broader scope. Verify creation from session evidence; current branch association alone is not proof.
3. Include draft and ready-for-review pull requests only while their current state is open. Exclude merged and closed pull requests.
4. Recover direct canonical web URLs and verify current state with read-only repository tooling. Never infer a PR number or fabricate a URL.
5. Preserve creation order and list each pull request once. If no pull requests qualify, return `- None`.

## Output

Return only this heading and Markdown list, with no status summary or extra prose:

```markdown
Pull requests

- https://github.com/owner/repository/pull/123
```
