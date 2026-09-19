---
name: defer-execution
description: Schedule an unrecorded scope of work on its own branch off the default branch rather than folding it into the change in flight, either after the originating pull request merges or immediately in a worktree. Use to hand over new work to do separately; use execute-defer-scope for an existing deferral record.
disable-model-invocation: true
---

# Defer Execution

Take a scope of work and get it **done** on a branch of its own, off the default branch, instead
of folding it into the change already in flight.

**This skill accepts unrecorded scopes and creates no deferral record.** `defer-scope` records the
durable Linear or repository-fallback entry, and `execute-defer-scope` resolves it. When work already
has a Linear issue, legacy directory, or record pull request, invoke `execute-defer-scope` so its
record and implementation receive one disposition. A scope handed here is already spoken for;
recording it would leave the next reader to distinguish work awaiting a decision from work awaiting
a merge.

When a scope should be both — done after the merge *and* durable if this session ends first — that
is two invocations, and the user asks for both.

## The decision

Every invocation resolves to one of two routes. Make the call explicitly and say which one was
taken and why.

**Execute now, in a worktree.** Take this route when the scope is small enough for one focused
pass **and** cannot conflict with the change in flight. Both halves must hold.

**Execute after the merge.** Take this route otherwise — the scope is large, or it touches files
the current branch also touches, or its correct shape depends on what the current change lands.

When the two routes are genuinely close, prefer executing now. A branch that exists is worth more
than a promise, and the merge route's whole cost is that nothing happens until someone comes back.

### What "cannot conflict" means

Conflict is about the files, not the topic. Resolve it by looking, not by guessing:

```
git diff --name-only $(git merge-base origin/<default-branch> HEAD)
```

The scope cannot conflict when no path it will touch appears in that list. A scope that only adds
new files cannot conflict. A scope that renames or moves a file the current branch edits
conflicts, however small it looks.

Where the current branch is still being worked, judge against what it will touch, not only what it
has touched so far. When that is unclear, take the merge route.

### What "small" means

One focused pass by one agent: a rename, a move, a helper extraction, a documentation correction,
a directory restructure whose call sites are mechanical. If the scope needs its own plan, spans
subsystems, or would need review as a design change, it is not small.

## Route one: execute now, in a worktree

The point of the worktree is that the current branch's working tree is never touched, so the
change in flight keeps running while this work happens beside it.

1. **Branch from the fetched default branch**, never from the current branch.

   ```
   git fetch origin <default-branch>
   git worktree add <path> -b claude/<slug> origin/<default-branch>
   ```

2. **Delegate the work to a subagent** scoped to that worktree, so the parent session's own state
   and working directory stay where they were. Give it the scope, the worktree path, and the
   instruction to commit there.

3. **Validate inside the worktree** with the repository's own checks for what changed. A scope
   small enough for this route is small enough to validate.

4. **Push and open a pull request** as ready for review, titled for the work.

5. **Remove the worktree** when the branch is pushed, and confirm the original working tree is
   unchanged.

Merging that pull request needs the same authorization as any other. This skill schedules work; it
does not merge it.

## Route two: execute after the merge

The work is owed once the originating pull request lands.

1. **Name the originating pull request**, and write the scope as one item in the harness task list,
   where the harness has one, whose text names that pull request as its trigger: "After #NNNN
   merges: `<scope>`". The item is what a later turn reads, so anyone scanning the list can tell a
   queued-on-merge item from an ordinary pending one without this skill being loaded at all. That is
   session bookkeeping rather than a deferral record, and the guardrail against creating one stands.

2. **Tell the user the scope is queued behind that pull request**, in those terms. Say what will be
   executed and what it is waiting on. Then name it and its blocking pull request again in every
   turn's report while it stays queued, so a commitment that slips surfaces in the next message
   rather than an hour later.

3. **The merge is observed, never watched for.** It arrives through something delivered or something
   already being read: the merge call's own result, a pull-request-closed notification, a fetch
   showing the squash commit on the default branch, or the user saying it merged. Never arm a timer,
   monitor, or scheduled check-in for it. The repository's ban on those holds here, and this route
   needs no exception to it, because the trigger arrives on its own.

4. **The turn that observes the merge is the turn the branch is created.** Post-merge finalization
   already in flight finishes first; the scope then starts in that same turn. A new user request
   does not discharge the commitment. **No turn ends with the scope still queued once its pull
   request has merged** — either the branch exists, or that turn says exactly what is blocking it.

   ```
   git fetch origin <default-branch>
   git checkout -b claude/<slug> origin/<default-branch>
   ```

   Never branch from the merged working branch, and never stack the work on top of it.

5. **Push and open a pull request** as ready for review, then report it.

### The authorization outlives the merge

A queued scope is an outstanding obligation, not a completed execution. Its own invocation authorizes
it until the branch exists, and no other skill's completion or authorization boundary closes it: a
workflow that ends by merging the very pull request this scope waits on has not consumed the
invocation that queued it, and the scope needs no re-invocation to proceed.

After a context compaction, a session resume, or any summary, re-establish the scope from the task
list, check whether its pull request merged, and start it if it has. Resuming this route is not
re-executing this skill — the skill has not finished until the branch exists, so a notice telling a
later turn not to re-run skills that already ran does not reach it.

The task-list item is the session's bookkeeping and not a durable record. A scope that must outlive
the session whatever happens is one to record with `defer-scope` as well, which the user asks for.

## Continuing deferred execution

When a scope is already queued or a deferred pull request from this skill is open, **add every
further deferred scope to that same branch and pull request**. This includes an active deferred
pull request whose implementation is still in progress: do not create a second post-merge branch
for related deferred work. Check both the session's queued work and open pull requests before
starting. A scope that arrives before the first pull request opens joins the same future branch.

Update the pull request body to cover the added work when appending. A body describing half of a
branch is worse than no body.

## Guardrails

- Never fold the deferred scope into the branch it came from. That is the whole point: it must be
  reviewable and mergeable on its own.
- Never hand a would-be fix from the change under review here to get it out of that change. That is
  a deferral, and the deferral mechanism's admission decides whether it may leave the change.
- Never create a Linear deferral or repository-fallback record for a scope handed only to this skill.
  Deferral records describe problems nobody has committed to; this skill's scopes are committed to
  by definition.
- Never branch a deferred scope from the working branch, on either route.
- Never arm a timer, monitor, or scheduled check-in to notice the merge. The observation is
  delivered or already being read.
- A queued scope that outlives its pull request's merge by a turn has been dropped, whatever else
  that turn accomplished.
- A queued scope survives a summary. Re-establish it and check its pull request rather than reading
  a skill listed as already run as a scope already done.
- Reuse the existing deferred branch and pull request for every later scope.
- Report which route was taken and why, every time. "Deferred" without the route and its reason
  tells the user nothing about when to expect the work.
- Scheduling is not merging. Opening the pull request completes this skill; merging it is a
  separate authorization.
