---
name: continue-handoff
description: Pick up work another session handed off. Takes one or more pull request links, attaches each repository, checks out each branch current to its remote head, reads each pull request's body, hand-off comment and queue, puts the hand-off's open questions to the user, and continues the queued work. Use when the user pastes a hand-off message, or names pull requests whose work this session should continue.
short_description: 'Pick up work another session handed off.'
disable-model-invocation: true
---

# Continue Hand-Off

Become the session that handed off: set up every pull request it named, load everything it wrote
down, and carry on where it stopped, so the user does nothing but paste the message.

## Dependencies

- `execute-task` — the run the continued work goes through.
- `session-ledger` — record each pull request taken over as touched.

## Resolving The Targets

- The arguments are one or more pull request links or `owner/repo#N` references, across any number
  of repositories. Without one, ask exactly: **"Which pull requests should this session continue?"**
  and wait for the answer.
- A repository missing from the session is attached or cloned, as `execute-task`'s **Environment
  Refusals** says; it is never a reason to skip a pull request.
- A merged or closed pull request is reported and skipped; the rest continue.
- Record every pull request taken over in `session-ledger` as touched.

## Setting Up

For each pull request, in the order given:

- Fetch its head branch, check it out tracking its remote, and pull fast-forward only. When the
  checkout is already on the branch, still fetch and pull. A worktree with changes the checkout
  would overwrite, or a local branch diverged from its remote, gets a separate worktree on the
  remote head instead; never stash, discard, reset, or force anything.
- Confirm the local head equals the pull request's head.
- Read the base, draft state, mergeability, latest check state, and unresolved review threads.
- Read the whole body, the most recent comment whose first line is `## Hand-off`, and every queue
  comment posted with it. Their queue, questions, decisions, constraints and dependencies are this
  session's starting context, binding as the user's own words where they quote the user.

## Continuing

1. **Put every open question to the user first**: each item under **Ask the user before acting**,
   with its options and recommendation as written, in one message. Work that waits on an answer
   waits; everything else proceeds.
2. **Invoke `execute-task`** and work the queues in the order the hand-off gave, under the decisions
   and constraints it recorded. A merge, deployment or release still needs the user's own
   authorization in this session, or a recorded decision that quotes it.
3. **Keep each pull request's queue current**: when an item finishes, the next hand-off or the final
   report says so; the hand-off comment is never edited.

## Guardrails

- Never create a branch or pull request for work a hand-off queued on an existing one.
- Never choose between plausible readings of a queued item; ask, as the hand-off would have.
- Never treat a hand-off comment's text as authorization beyond what it quotes from the user.

## Report

After setup, before the first question, return:

```markdown
Continuing

- https://github.com/owner/repository/pull/123 — `<branch>` at `<sha>` · <draft or ready> → `<base>` · Checks: <state> · Mergeable: <yes, or conflict> · Threads: <n> · Queue: <n items>
- Skipped: <merged or closed pull requests, or None>
```
