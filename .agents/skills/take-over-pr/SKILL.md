---
name: take-over-pr
description: Make a pull request's branch the working checkout so its work continues in this session. Resolves a pull request link or branch name to one repository and branch, switches to it, pulls the latest head, identifies its open pull request, and restates the pull request's state and latest hand-off notes without acting on them. Invoke as /take-over-pr <pull request link or branch name> to switch this session onto another pull request.
disable-model-invocation: true
---

# Take Over Pull Request

Put the checkout on the branch the user names, current to its remote head, and say where that pull
request stands.

## Resolving The Target

- The argument is required. Without one, ask exactly: **"Which pull request or branch should this
  session take over?"** and wait for the answer.
- A pull request URL, an `owner/repo#N` reference, or a bare number reads that pull request; a bare
  number resolves against the current repository only. Its repository and head branch are the
  target. A merged or closed pull request is reported and the run stops; nothing is checked out.
- A branch name is matched as an exact remote branch across every repository the session is
  authorized for. More than one match stops the run with the candidates listed; no match stops it
  with that fact. Never create a branch.
- Query the hosting service for the open pull request whose head is exactly that branch; never
  infer it from a local branch, a remembered URL, or prior output. A branch with no pull request is
  still taken over, and the report says so.

## Switching

- When the checkout is already on the branch, skip the checkout and still fetch and pull.
- A worktree holding uncommitted tracked changes, staged changes, or untracked files the checkout
  would overwrite stops the run with those files named. The user decides whether to commit, stash,
  or discard them; this skill does none of it.
- Fetch the branch, check it out tracking its remote, and pull fast-forward only. A local branch
  that has diverged from its remote stops the run with both heads named; never reset, rebase, or
  force anything.
- After the pull, confirm the local head equals the pull request's head and report a mismatch.

## Reading The Pull Request

- Record the base, draft or ready state, mergeability, latest check state, and unresolved review
  threads, using read-only tooling.
- Find the most recent comment whose first line is `## Hand-off` and restate its sections as they
  were written: unfinished work, items waiting on a decision, the unapproved plan, work recorded
  elsewhere, and state left outside the repository. Act on none of it; the next invocation decides
  what happens.

## Guardrails

- Never create a branch or a pull request, and never write to the pull request.
- Never stash, commit, discard, reset, or force-push.
- Never choose between plausible candidates; stop and name them.
- Never arm a subscription, watch, or timer.

## Completion Report

```markdown
Taken over

- Repository: owner/repository · Branch: `<branch>` at `<sha>` (<fast-forwarded n commits, or already current>)
- Pull request: https://github.com/owner/repository/pull/123 — <draft or ready> → `<base>` · Checks: <state> · Mergeable: <yes, or conflict> · Unresolved review threads: <n>
- Hand-off notes: <restated sections, or None posted>
```

A run that stops reads `Take-over stopped`, names the reason in its first bullet, and leaves the
checkout exactly as it was found.
