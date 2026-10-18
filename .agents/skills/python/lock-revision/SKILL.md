---
name: lock-revision
description: Lock the database revisions a branch has added so far, because they may be deployed to a test environment, so every later schema or stored-data change goes into a new revision. Each invocation locks the revisions added since the last one.
short_description: 'Lock the current migration revisions before a test deploy; later changes go in a new revision.'
disable-model-invocation: true
---

# Lock Revision

Invoking this skill means the user is about to deploy the branch's current changes to an
environment, so its revisions may be applied there. From then on, each of those revisions is history.

## Dependencies

- `database-migrations` — the revision rules a locked revision falls under, and how later
  revisions are added and validated.

## Workflow

1. **Find the unlocked revisions.** In every repository in the task that has migration chains,
   list the revisions the branch adds or changes on each chain against its default branch,
   including a default-branch revision the branch re-parented or edited. Leave out any revision
   that already carries the lock marker. If there are none, report that nothing was
   locked. A chain with more than one unlocked revision the branch adds breaks
   `database-migrations`' one-revision rule: fold them into one, validated as that skill says,
   before locking. A default-branch revision keeps its own id and is locked beside them.
2. **Lock each one.** Add the marker as the first line of each revision file, above its docstring:

   ```python
   # Locked: an environment may have applied this revision. Put later changes in a new revision.
   ```

   Change nothing else in the file.
3. **Commit and push** the marker lines on the branch's pull request, one commit per repository
   (`chore(migrations): lock revisions <ids>`), after the repository's migration file checks pass.
4. **Report** each locked revision by chain and file, and the commit that locked it.

## After Locking

- A locked revision is history under `database-migrations`' **Applied Is What Makes History**,
  whether or not a deploy has run it yet. Its id, parent and database outcome never change, so it is
  never folded, re-parented or regenerated. Its code may still be simplified or refactored when the
  migration tests prove the database outcome unchanged.
- The next schema or stored-data change on that chain goes into one new revision on top of the
  locked one. While that revision is unlocked, later changes go into it, as the at-most-one rule
  says. The next invocation locks it, and the cycle repeats.
- When a base update adds revisions to a chain that holds a locked revision, join the two heads
  as `database-migrations` says. Never re-parent a locked revision: an environment that applied it
  would sit on a chain it never ran.
