---
name: current-changes
description: Summarize what the current branch changes against the default branch as one paragraph and one sentence per material change, each linked to the code that makes it, with test changes folded into a single line. Invoke as /current-changes or $current-changes, or when the user asks what the branch or its pull request changes.
---

# Current Changes

Tell a reader what the branch does, at the level a reviewer wants before opening the diff: the
change as a whole, then each material change as one sentence with a link to exactly the code that
makes it.

## Dependencies

- `rebuild-git-history` — the branch's commits are made to correspond to its changes before
  they are linked.

## Workflow

1. **Resolve the target without asking.** The branch is the one checked out; its base is the merge
   base with the remote default branch, falling back to the local default branch when no remote is
   configured; its pull request is the open one for that branch, found with the repository tooling.
   Diff the branch against the base, `git diff $(git merge-base <base> HEAD)`, plus any untracked
   files the branch adds. Read the diff itself, not its file list; a file list says where the change
   is, never what it does.
2. **Group the hunks into material changes.** A material change is a unit of intent a reviewer would
   name — a shared owner introduced to remove duplication, a contract broken on purpose, a behaviour
   added or removed, a mechanism replaced by another — never a file, a hunk, or a rename on its own.
   Several hunks across several files usually make one change; one file rarely makes two.
3. **Fold the tests.** Test changes become one sentence at the end of the list, however many files
   they span. Two things earn a test change its own line: the branch is itself about tests, or a test
   change carries weight of its own, such as a new harness or fixture layer, or a refactor unrelated
   to the application change it sits beside.
4. **Write each sentence for what it does and why it matters**, in plain words: "Introduces a shared
   registry so the two services stop keeping their own copies", not a list of files or symbols. A
   deliberate break of a route, payload, or stored shape is named as a break.
5. **Give each change one link: the commit that makes it.** A reader clicks it and sees how the
   change is made, so the link is one, not a list. The GitHub rules say a commit carries one material
   change, so on a branch that keeps them the bullets and the commits correspond one to one.
   - When the branch is yours and its commits do not split that way, run `rebuild-git-history`
     first — one commit per material change, the same final tree, the old head kept under a backup
     ref — then link the commits. The summary is written after the history is right, not around it.
   - When the branch is not yours to rewrite, link the diff of the one file that implements the heart
     of the change, through the pull request's files view anchored at that file,
     `<pull request url>/files#diff-<anchor>` where the anchor is the SHA-256 hex digest of the file's
     repository path, named by the file's basename. Never list every file a change touches.
   - The `Tests:` line links its commit the same way, or the test file that carries the most of it.
   - With no pull request open, link commits on the remote branch; with nothing pushed, say the code
     is local and name the commit or file instead of linking.

## Output

Return exactly this shape, with no headings, no status, and nothing after the list:

```markdown
Changes on `<branch>` — [<pull request title>](<pull request url>)

<one paragraph summarizing the change as a whole>

- <one sentence per material change> ([<commit or file>](<link>))
- <one sentence per material change> ([<commit or file>](<link>))
- Tests: <one sentence> ([<file>](<link>))
```

Without an open pull request the first line reads `Changes on <branch> against <base>`. Omit the
`Tests:` line when the branch changes no tests. When the branch has no changes against the base,
return the single line `No changes against <base>.`
