---
name: handoff
description: Move the current session's work to another session with nothing lost and nothing left for the user to do. Stops running workers once their work is pushed and posts their queues, brings every pull request body up to date, closes the pull requests this session made stale, posts a hand-off comment on each pull request carrying every piece of context the next agent needs, releases every subscription and timer, and ends with the exact message the user pastes into the next session. Use when a session is too bloated to continue and the work moves elsewhere.
short_description: 'Move the current session''s work to another session with nothing lost and nothing left for the user to do.'
disable-model-invocation: true
---

# Handoff

Continue this session elsewhere. Everything the next agent needs — the work left, the order, the
files, the user's decisions and words, the questions still open — goes onto the pull requests,
because the next session starts with nothing else. The private task ledger transfers separately
through `session-ledger`; its contents never go into those published comments. The user's only part is pasting the message this
skill ends with.

## Dependencies

- `list-prs`
- `defer-scope`
- `session-ledger`

## Scope

- Invoking this skill authorizes, on every pull request it covers, the hand-off comment, the
  comment closing a stale pull request, and the body rewrite, as the GitHub rule's **Comments**
  requires.
- Cover every open pull request the session created or changed, across every repository the
  session was authorized for. Each pull request gets its own comment, written for the agent that
  continues it.
- Complete every hand-off step, working through environment obstacles. When private-ledger recovery or verified transfer is genuinely unavailable, preserve
  the source and report the concrete blocker. Use the completion template only after all steps,
  including ledger transfer and ownership verification, succeed.
- Nothing in the hand-off or its report is addressed to the user as a task. An action that needs the
  user — a decision, an approval, a merge they have not authorized — is written in the hand-off
  comment as an instruction to the next agent to put that question to the user and wait, exactly as
  this session would have.

## Workflow

1. **Build the ledger.** Invoke `list-prs`. Resolve the private task ledger through `session-ledger`,
   retain its exact locator and task identity in agent-consumed continuation context, and keep
   source writing ownership while workers finish and final records are merged. Record for each
   pull request its head, base, mergeability, latest check state,
   and unresolved review threads using read-only tooling.
2. **Stop every running worker after its work is out.** Tell each sub-agent or worker still running
   to finish only the step in hand, commit it, push it to the pull request the work continues, and
   reply with its remaining queue: each item in order, its exact files, and the user's words where an
   item came from the user. Wait for every reply; a worker that has already ended is read from its
   last report and its worktree. Stop any background process a worker left running.
3. **Sweep the session for loose ends** across the whole conversation, compacted summaries and the
   harness task list included: work stated as deferred, skipped, "later", or "follow-up"; a scope
   queued to run after a merge; a plan presented and not explicitly approved, read from wherever the
   host keeps the live plan, where a timeout or a mode exit counts as unapproved; questions put to
   the user and still unanswered; decisions the user made and the words they made them in; standing
   constraints the user set for the work, such as accounts never to touch or actions that need their
   say-so; promises the agent made and did not complete; anything the session changed outside the
   repository that is still in a temporary state. Classify each as **queued work**, **a question for
   the user**, **context**, or **deferred repository work**.
4. **Record deferred repository work through `defer-scope`**, one scope per item, in the repository
   that owns it, and link each resulting record or Linear issue from the hand-off comments in that
   repository alone. An item `defer-scope`
   refuses as a confirmed defect goes first in the queue on its pull request instead.
5. **Secure every branch.** Every commit the session or a worker made reaches the pull request the
   work continues: a worktree's commits are pushed to that pull request's branch, merged in first
   when the branch has moved, and a branch outside it that holds work for it is merged into it when
   the merge is clean or named in the queue with the exact merge still to do. Commit uncommitted
   changes with a message that says what state they are in, using a `wip:` prefix when they are
   incomplete. Then run the pre-push checks
   the GitHub rule’s **Pre-Push Gate** defines, report-only: every failing check is pushed unfixed and
   goes first in the queue — the one push that does not wait on its checks, because unpushed work
   is lost with the session. Apply and commit any stash. Never rewrite history or force-push.
6. **Close the pull requests this session made stale.** One whose commits now live on the pull
   request the work continues, or whose change is superseded, is closed with a comment naming where
   the work went, as the GitHub rule's **Branches and Pull Requests** says. A pull request the
   session did not open is never closed, retargeted or folded.
7. **Bring each pull request body up to date**: read the complete existing body, then rewrite it
   to describe everything the branch now changes, written the way the GitHub rule's description
   bullets say — from the session's own record of the work, not a walk through its commits. Every open pull request in the ledger gets this, however long its body.
8. **Post the hand-off comment** on each pull request in the template below, written so an agent with
   no other context can continue: the queue in order with exact files, every question with the
   options as they were put, and every decision and constraint that governs this repository's work.
   It is published in this repository, so it follows the GitHub rule's independent publishing
   context exactly as `session-ledger`'s backup comments do: it states this repository's work in
   this repository's own terms and never names or links another repository, its pull requests or
   its constraints, a dependency included. The queue, the questions, the user's words and the plan
   are carried verbatim except where they refer to another repository, its pull requests or its
   vocabulary; each such reference is replaced by this repository's own contract, such as "a
   consumer of this branch's API repoints once it merges". Which pull request that is, and every
   cross-repository identity and constraint, lives in the private ledger step 9 transfers. It carries the task token `session-ledger`'s
   backup comments carry, so a session that cannot reach the ledger file can tell which of them
   are this task's. Never put a secret, credential or access token in it.
9. **Transfer the finalized private ledger.** After all workers' receipts and final hand-off facts
   are recorded, follow `session-ledger` to verify the receiver's complete file, exact locator and
   writing-ownership takeover. Retain the source until that verification succeeds; never release
   source context or declare completion with recovery or transfer still blocked.
10. **Release everything the session holds:** every pull-request activity subscription, every watch
   on an external resource, every scheduled wake-up, reminder, or routine the session created, and
   every background monitor, loop, or long-running task. Confirm each release with the matching
   listing read where one exists.
11. **Report** with the completion template.

## Hand-Off Comment

```markdown
## Hand-off

Head `<sha>` on `<branch>` → `<base>`. Checks: <green, or red with the failing names> · Mergeable: <yes, or conflict> · Unresolved review threads: <n>

Task: `<task token>`

### Queue
1. <item> — <exact files> — <the user's words, where the item came from the user>

### Ask the user before acting
- <question, with the options as they were put and the recommendation> — <what waits on the answer>

### Decisions and constraints
- <decision or standing constraint governing this repository, in the user's words or paraphrased in this repository's terms>

### Depends on
- <what this branch needs from, or offers to, other work, as this repository's own contract>

### Plan presented, not approved
<the plan verbatim, with references to other repositories replaced as step 8 says>

### Recorded elsewhere
- <record link> — <scope>

### Outside the repository
- <resource> — <temporary state and what restores it>
```

## Guardrails

- Do no new work. A red check, a review finding, or a lint report goes into the queue, never into a
  fix; completing the hand-off's own steps is not new work.
- Keep published project handoff context on the pull requests; the private task ledger is owned
  and transferred by `session-ledger`. Do not create a separate checkpoint file.
- Never arm a timer, wake-up, or subscription during the hand-off.
- Never merge, mark ready, or re-request review on a pull request.
- Never fabricate a pull request URL, a record link, or a check state; verify each with a read.
- Write every comment for the next agent, never in the user's voice and never addressed to the user.

## Completion Report

Return this in chat once every step has run, and nothing after it:

```markdown
Hand-off complete

- https://github.com/owner/repository/pull/123 — <checks / mergeable / n threads>; body updated; hand-off comment posted
- Closed as stale: <links, with where the work went, or None>
- Released: <subscriptions, watches, timers, monitors, or None held>

Paste this into the next session:

    /continue-handoff https://github.com/owner/repository/pull/123 https://github.com/owner/other/pull/45
```

The paste line lists every open pull request the hand-off covered, in the order the next session
should work them.
