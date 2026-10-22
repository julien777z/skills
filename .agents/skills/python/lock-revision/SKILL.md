---
name: lock-revision
description: Lock the database revisions a branch has added or changed so far, including default-branch revisions it re-parented or edited, because they may be deployed to a test environment, so every later schema or stored-data change goes into a new revision. Each invocation locks the revisions added or changed since the last one.
short_description: 'Lock the current migration revisions before a test deploy; later changes go in a new revision, pushed once the user lets revisions resume.'
disable-model-invocation: true
---

# Lock Revision

Invoking this skill means the user is about to deploy the branch's current changes to an
environment, so its revisions may be applied there. From then on, each of those revisions is history.

The user is waiting to deploy, so the run is the next work in the session, ahead of everything
`execute-task`'s **Priority** ranks below a waiting deploy, and it does only the steps below. It
never stops to ask: the lock marker and a deploy the user reported are the only record that a
revision was applied, so a revision with neither is folded and locked as step 1 says.

## Dependencies

- `database-migrations` — the lock marker and how a revision is locked, the revision rules a locked
  revision falls under, and how later revisions are added.
- `execute-task` — the priority of work a waiting deploy needs.

## Workflow

1. **Find the unlocked revisions.** In every repository in the task that has migration chains,
   list the revisions the branch adds or changes on each chain against its default branch,
   including a default-branch revision the branch re-parented or edited. Leave out any revision
   that already carries the lock marker. If there are none, report that nothing was
   locked. A chain with more than one unlocked revision the branch adds breaks
   `database-migrations`' one-revision rule: fold them into one before locking. A default-branch
   revision keeps its own id and is locked beside them.
2. **Lock each one** with `database-migrations`' lock marker, as that skill's lock-marker rule
   says.
3. **Check only what changed.** A chain that only gained marker lines needs the formatter and the
   migration tool's single-head check. A fold also needs the repository's migration tests, all of
   them: a fold moves the revisions that backfills and earlier revisions' tests are registered
   against. No other suite, walkthrough, review or simplification runs as part of this skill.
4. **Commit and push** the marker lines and any fold on the branch's pull request, one commit per
   repository (`chore(migrations): lock revisions <ids>`), as soon as those checks pass.
5. **Report** each locked revision by chain and file, end with the pushed commit the user can
   deploy, and **ask the user to confirm when revisions may resume**: a revision pushed before that
   deploy runs would ride into it. Record the hold and the pending question with `session-ledger`,
   so both survive compaction and handoff.

## After Locking

A locked revision is history under `database-migrations`' **Applied Is What Makes History**,
whether or not a deploy has run it yet, and that skill's lock-marker rule governs it from then on:
what stays fixed, where the chain's next change goes, and how a base update joins the chain. The
next invocation locks the revision that next change opens, and the cycle repeats.

**Until the user says revisions may resume, a change that needs a new revision stays local.** The
revision, and the code that depends on its schema or stored data, is committed on a local branch
off the pushed head and never pushed, while work that needs no revision keeps pushing as usual, so
no push carries it. Only the user's own words lift the hold; once they do, rebase that work onto the
pull request's branch, validate it as `database-migrations` says, push it, and clear the hold from
the ledger. Each invocation starts a new hold.
