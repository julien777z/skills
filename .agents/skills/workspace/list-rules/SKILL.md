---
name: list-rules
description: List and reconcile canonical rules across a bounded collection of local repositories. Use when the user asks which rules repositories have, where they occur, or whether a shared rule has conflicting language.
short_description: 'List and reconcile canonical rules across a bounded collection of local repositories.'
---

# List Rules

## Discovery

Determine the bounded repository collection from the user's scope, the current repository,
accessible sibling repositories and worktrees, and targets already established in the task.
Discover Git repositories independently of whether they contain rules, normalize remote identities,
and deduplicate worktrees of the same remote. Do not crawl unrelated locations; when the environment
cannot establish the collection, ask for the missing scope. Read each repository's current remote
default branch without changing its checkout or unrelated work.

Read each applicable repository's canonical `.agents/rules/<name>.md` files. Exclude repositories whose primary purpose is developing, packaging, testing, or operating the agent-synchronization system itself unless the user explicitly includes them.

For each rule name, merge the repository names that contain it. Compare complete canonical rule text, including frontmatter. Group identical texts and use the largest group as the baseline. If any other group exists, report every repository outside that baseline as having conflicting language. If two or more groups tie for largest, report all tied groups as conflicting rather than choosing an arbitrary baseline.

## Output

Return only these headings and sorted Markdown lists, with no status summary or extra prose:

```markdown
Rules

- rule-name — (repo-one, repo-two)

## Conflicting Rule Language

- rule-name
  - Baseline: repo-one, repo-two
  - Different language: repo-three
```

Omit `## Conflicting Rule Language` when no differences exist. If no rules exist, return `- None` under `Rules`.
