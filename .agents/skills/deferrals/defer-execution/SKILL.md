---
name: defer-execution
description: Schedule an unrecorded scope of work on its own branch off the default branch rather than folding it into the change in flight, either after the originating pull request merges or immediately in a worktree. Use to hand over new work to do separately, not for work that already has a deferral record. Run only when the user asks for it.
short_description: 'Schedule separate work on its own branch, either now or after the current pull request merges.'
---

# Defer Execution

Take a scope of work and get it **done** on a branch of its own, off the default branch, instead
of folding it into the change already in flight.

**This skill accepts unrecorded scopes and creates no deferral record.** Work `defer-scope` already
records is a recorded deferral and not this skill's: decline it, name its record, and tell the user
to run `/execute-defer-scope` on it, so its record and implementation receive one disposition. A
scope handed here is already spoken for; recording it would leave the next reader to distinguish
work awaiting a decision from work awaiting a merge.

When a scope should be both — done after the merge *and* durable if this session ends first — that
is two invocations, and the user asks for both.

## Dependencies
- `subagent-matrix`
- `session-ledger`
- `defer-scope`

## The decision

Every invocation resolves to one of two routes. Make the call explicitly and say which one was
taken and why.

**Execute now, in a worktree.** Take this route whenever the scope cannot conflict with the change
in flight and does not depend on what that change lands, whatever its size, including a scope
large enough to need a plan.

**Execute after the merge.** Take this route only when the merge supplies something the scope
uses: it touches files the current branch also touches, or its correct shape depends on what the
current change lands. Name which of the two applies; that is the trigger the queued item carries.

### What "cannot conflict" means

Conflict is about the files, not the topic. Resolve it by looking, not by guessing:

```
git diff --name-only $(git merge-base origin/<default-branch> HEAD)
```

The scope cannot conflict when no path it will touch appears in that list. A scope that only adds
new files cannot conflict. A scope that renames or moves a file the current branch edits
conflicts, however small it looks.

Where the current branch is still being worked, judge against what it will touch, not only what it
has touched so far: read its plan and its planned files. An overlap left unclear after that is
resolved by reading further, never by defaulting to the merge.

## Route one: execute now, in a worktree

The worktree leaves the current branch's working tree untouched.

1. **Branch from the fetched default branch**, never from the current branch.

   ```
   git fetch origin <default-branch>
   git worktree add <path> -b <required-prefix><slug> origin/<default-branch>
   ```

   `<required-prefix>` is the branch-name prefix the harness or the repository's guidance requires
   for agent branches; where neither names one, the branch is named `<slug>` alone.

2. **Do the work in the worktree**: directly when it is a few edits, and through one subagent
   scoped to that worktree otherwise, once no other building worker in the session is changing the
   same files or resources. A subagent keeps the parent session's context and working directory
   free for the change in flight; a few edits cost less done directly. To delegate, invoke
   `subagent-matrix` at its standard capability level, launch its exact resolved identifier, and
   retain catalog state, identifier, assignment state and host receipt with the scope's evidence in
   the task ledger through `session-ledger`, as `subagent-matrix`'s **Dispatch** requires. Give the
   worker the scope, the worktree path, and the commit and push cadence the GitHub rule's
   **Pre-Push Gate** sets for delegated edits.

3. **Validate inside the worktree** with the checks the GitHub rule's **Pre-Push Gate** requires.

4. **Push and open a pull request** as a draft, titled for the work.

5. **Remove the worktree** when the branch is pushed, and confirm the original working tree is
   unchanged.

Merging that pull request needs the same authorization as any other. This skill schedules work; it
does not merge it.

## Route two: execute after the merge

The work is owed once the originating pull request lands.

1. **Name the originating pull request**, and record the scope in the task ledger through
   `session-ledger`, as a step whose text names that pull request as its trigger: "After #NNNN
   merges: `<scope>`". The step is what a later turn reads. Where the harness has a task list, add the
   same item there as well, so anyone scanning it can tell a queued-on-merge item from an ordinary
   pending one without this skill being loaded at all. Both are session bookkeeping rather than a
   deferral record, and the guardrail against creating one stands.

2. **Tell the user the scope is queued behind that pull request**, in those terms. Say what will be
   executed and what it is waiting on. Then name it and its blocking pull request again in every
   turn's report while it stays queued, so a commitment that slips surfaces in the next message
   rather than an hour later.

3. **The merge is observed, never watched for.** It arrives through something delivered or something
   already being read: the merge call's own result, a pull-request-closed notification, a fetch
   showing the squash commit on the default branch, or the user saying it merged. Never arm a timer,
   monitor, or scheduled check-in for it. The ban on polling a pull request holds here, and this route
   needs no exception to it, because the trigger arrives on its own.

4. **The turn that observes the merge is the turn the branch is created.** Post-merge finalization
   already in flight finishes first; the scope then starts in that same turn. A new user request
   does not discharge the commitment. **No turn ends with the scope still queued once its pull
   request has merged** — either the branch exists, or that turn says exactly what is blocking it.

   ```
   git fetch origin <default-branch>
   git checkout -b <required-prefix><slug> origin/<default-branch>
   ```

   Never branch from the merged working branch, and never stack the work on top of it.

5. **Push and open a pull request** as a draft, then report it.

### The authorization outlives the merge

A queued scope is an outstanding obligation, not a completed execution. Its own invocation authorizes
it until the branch exists. The merge of the pull request it waits on, by whatever route, does not
consume the invocation that queued it, and the scope needs no re-invocation to proceed.

After a context compaction, a session resume, or any summary, re-establish the scope from its step
in the task ledger, check whether its pull request merged, and start it if it has. Resuming this route is not
re-executing this skill — the skill has not finished until the branch exists, so a notice telling a
later turn not to re-run skills that already ran does not reach it.

The ledger step is the session's durable record of the scope, and a task-list item only mirrors it;
neither is a deferral record.

## Continuing deferred execution

**A further deferred scope joins an open or queued deferred branch only when it is on the same
subject**, so each pull request stays one change a reviewer can judge and merge on its own. Same
subject means the reviewer would read the two scopes together: the same feature, defect or area of
the code, such as a second fix to the export page the queued scope already changes. A scope on any
other subject starts its own branch from the default branch, on whichever route fits it, even while
an earlier deferred pull request is open or still being implemented.

- Before starting, check both the session's queued work and its open deferred pull requests for one
  on the scope's subject.
- A scope that joins does so on the branch of its kind: agent configuration and source stay apart,
  except guidance that rides the source pull request it depends on, as the GitHub rule's
  **Branches and Pull Requests** says and the guidance-editing skill's pull-request reference sets
  out.
- A same-subject scope that arrives before the first pull request opens joins the same future
  branch.
- Update the pull request body to cover the added work when appending. A body describing half of a
  branch is worse than no body.

## Guardrails

- A would-be fix from the change under review is never handed here to get it out of that change:
  that is a deferral, and `defer-scope`'s admission decides whether it may leave the change.
- Report which route was taken and why, every time; "deferred" without them tells the user nothing
  about when to expect the work.
