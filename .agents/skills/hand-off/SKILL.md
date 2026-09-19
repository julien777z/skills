---
name: hand-off
description: Wrap up the current session so its open pull requests can be taken to another session with nothing lost. Records deferrals stated in chat, posts a hand-off comment on each pull request carrying the unapproved plan and every item waiting on the user, brings each pull request body up to date, commits and pushes work in flight, and releases every subscription and timer the session holds. Invoke as /hand-off when a session is too bloated to continue and the work moves elsewhere.
disable-model-invocation: true
---

# Hand-Off

End this session's ownership of its pull requests with every loose end written somewhere durable,
and fix nothing along the way.

## Dependencies

- `list-prs` — the session-wide ledger of open pull requests the session changed.
- `defer-scope` — record repository work consciously left undone; it runs the admission gate.

## Scope

- Cover every open pull request the session created or changed, across every repository the
  session was authorized for. Each repository's pull request gets its own comment, and that comment
  describes only its own repository.
- A hand-off is a wrap-up, not a finish. What it cannot finish it names, so the next session starts
  from a list rather than a search.

## Workflow

1. **Build the ledger.** Invoke `list-prs`, add the current branch's pull request when it is
   missing, and record for each pull request its head, base, mergeability, latest check state, and
   unresolved review threads using read-only tooling.
2. **Sweep the session for loose ends** across the whole conversation, compacted summaries and the
   harness task list included: work stated as deferred, skipped, "later", or "follow-up"; a scope
   queued to run after a merge; a plan presented and not explicitly approved, read from wherever the
   host keeps the live plan, where a timeout or a mode exit counts as unapproved; questions put to
   the user and still unanswered; actions the user said they would take; promises the agent made and
   did not complete; anything the session changed outside the repository that is still in a
   temporary state, such as a resized resource or a toggled setting. Classify each as **deferred
   repository work**, **unfinished in-flight work**, or **waiting on the user**.
3. **Record deferred repository work through `defer-scope`**, one scope per item, in the repository
   that owns it, and link each resulting issue or fallback record from the hand-off comment. An
   item `defer-scope` refuses as a confirmed defect is not dropped: it becomes the first item of
   unfinished in-flight work on its pull request, so the next session fixes it in the same change.
4. **Secure every branch.** In each repository with work in flight, commit uncommitted changes with
   a message that says what state they are in, using a `wip:` prefix when they are incomplete, and
   push to the branch's upstream. Apply and commit any stash, or name it as lost. Never rewrite
   history or force-push. When a push is refused, report the exact blocker.
5. **Bring each pull request body up to date** against the full diff from its merge base. Read the
   complete existing body first and keep it a description of the change, as the GitHub rules
   require. When the body cannot be read back completely, leave it as it is and say so in the
   hand-off comment.
6. **Post the hand-off comment** on each pull request in the template below. Post it even when
   nothing is pending, because it marks the hand-off head; omit sections that would be empty.
7. **Release everything the session holds:** every pull-request activity subscription, every
   watch on an external resource, every scheduled wake-up, reminder, or routine the session created,
   and every background monitor, loop, or long-running task. Confirm each release with the matching
   listing read where one exists.
8. **Report** with the completion template.

## Hand-Off Comment

```markdown
## Hand-off

Head `<sha>` on `<branch>` → `<base>`. Checks: <green, or red with the failing names> · Mergeable: <yes, or conflict> · Unresolved review threads: <n>

### Unfinished in this change
- <item> — <what remains and where it lives>

### Waiting on a decision or action
- <question or action, with the options as they were put>

### Plan presented, not approved
<the plan verbatim>

### Recorded elsewhere
- <issue or record link> — <scope>

### Outside the repository
- <resource> — <temporary state and what restores it>
```

## Guardrails

- Fix nothing. A red check, a review finding, or a lint report is reported, never repaired.
- Never write a checkpoint file; the pull request and its hand-off comment are the record.
- Never arm a timer, wake-up, or subscription during the hand-off, including on a pull request the
  hand-off touches.
- Never merge, close, convert, or re-request review on a pull request.
- Never fabricate a pull request URL, an issue link, or a check state; verify each with a read.
- Write the comment for the next reader, never in the user's voice.

## Completion Report

Return this in chat once every step has run:

```markdown
Hand-off complete

- https://github.com/owner/repository/pull/123 — <checks / mergeable / n threads>; hand-off comment posted
- Deferrals recorded: <links, or None>
- Released: <subscriptions, watches, timers, monitors, or None held>
- Waiting on you: <items, or None>

The pull request(s) above can be taken to another session with `/take-over-pr`.
```

When a step could not complete — a push refused, a comment refused, the deferral ledger unavailable with no
fallback — the heading reads `Hand-off incomplete` and the first bullet names the blocker.
