---
name: lock-revision
description: Lock the database revisions a branch has added or changed so far, including default-branch revisions it re-parented or edited, because the user is about to deploy them to a test environment; until the user unlocks, no revision change and no source change that depends on one is pushed. Each invocation locks the revisions added or changed since the last one. Use to lock the branch's revisions. Run only when the user asks for it.
short_description: 'Lock the current migration revisions before a test deploy; revision changes are held unpushed until the user unlocks.'
---

# Lock Revision

Invoking this skill means the user is about to deploy the branch's current changes to an
environment, so its revisions may be applied there. The lock is a push hold and nothing more, as
**After Locking** says.

The user is waiting to deploy, so this run is the next work in the session, ahead of all work
that ranks below a waiting deploy, and it does only the steps below. Those numbered steps
are the plan the user approved by invoking it. It never asks whether a revision was applied: the
lock marker and a deploy the user reported are the only record, and a revision with neither is
locked.

## Dependencies
- `database-migrations`
- `session-ledger`

## Workflow

1. **Find the unlocked revisions.** In every repository in the task that has migration chains,
   list the revisions the branch adds or changes on each chain against its default branch,
   including a default-branch revision the branch re-parented or edited. Leave out any revision
   that already carries the lock marker. If there are none, report that nothing was
   locked. A chain with more than one unlocked revision the branch adds is folded into one first,
   as `database-migrations`' one-revision rule says.
2. **Lock each one** with `database-migrations`' lock marker.
3. **Check only what changed.** A chain that only gained marker lines needs the formatter and the
   migration tool's single-head check. A fold also needs the repository's migration tests, all of
   them: a fold moves the revisions that backfills and earlier revisions' tests are registered
   against. No other suite, walkthrough, review or simplification runs as part of this skill.
4. **Commit and push** the marker lines and any fold on the branch's pull request, one commit per
   repository (`chore(migrations): lock revisions <ids>`), as soon as those checks pass.
5. **Report** each locked revision by chain and file, end with the pushed commit the user can
   deploy, and **state that revision changes stay local until the user unlocks**: one pushed before
   that deploy runs would ride into it. That line is a notice, never a question: put it in the
   report, not to a question tool, and record no pending question. Record the lock with
   `session-ledger`, so it survives compaction; once a held local branch exists, the record names
   that branch and its head.

## After Locking

`database-migrations`' lock-marker rule is the whole of what a lock means, its push hold included.
This hold is the exception the GitHub rule's **Pre-Push Gate** allows an invoked skill to state.

Only the user's own words unlock. Once they do, integrate and push the held local branch as that rule
says, and record the unlock with `session-ledger`.
