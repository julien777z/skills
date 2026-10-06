---
name: continue-handoff
description: Pick up work another session handed off. Use when the user pastes a hand-off message or names pull requests whose work should continue. Revalidate inherited factual claims against their current sources before using them to choose an action, report an outcome or repeat a question; preserve the user's recorded decisions and continue authorized work.
short_description: 'Pick up work another session handed off.'
disable-model-invocation: true
---

# Continue Hand-Off

Become the session that handed off: set up every pull request it named, load everything it wrote
down, and carry on where it stopped, so the user does nothing but paste the message.

## Dependencies

- `execute-task` — the run the continued work goes through.
- `session-ledger` — recover the private task ledger and record each pull request taken over as touched.

## Resolving The Targets

- The arguments are one or more pull request links or `owner/repo#N` references, across any number
  of repositories. Without one, ask exactly: **"Which pull requests should this session continue?"**
  and wait for the answer.
- A repository missing from the session is attached or cloned, as `execute-task`'s **Environment
  Refusals** says; it is never a reason to skip a pull request.
- A merged or closed pull request is reported and skipped; the rest continue.
- Before recording a takeover, resolve the existing task ledger from agent-consumed continuation
  context through `session-ledger`, verify any cross-environment transfer and take over its writing
  ownership. An unavailable locator or file requires its recovery procedure, not a new empty ledger.
  Record every pull request taken over as touched.

## Setting Up

For each pull request, in the order given:

- Fetch its head branch, check it out tracking its remote, and pull fast-forward only. When the
  checkout is already on the branch, still fetch and pull. A worktree with changes the checkout
  would overwrite, or a local branch diverged from its remote, gets a separate worktree on the
  remote head instead; never stash, discard, reset, or force anything.
- Confirm the local head equals the pull request's head.
- Read the base, draft state, mergeability, latest check state, and unresolved review threads.
- Read the whole body, the most recent comment whose first line is `## Hand-off`, and any earlier
  `## Hand-off` comment it refers to. Their queue, questions, decisions, constraints and dependencies are this
  session's starting context, binding as the user's own words where they quote the user.
- Treat inherited factual claims as leads, not verified state. Before a claim determines an action,
  recommendation, reported outcome or approval request, check its authoritative source against the
  current target and relevant environment. A pull request's body, hand-off, ledger or worker report
  repeating a claim is not independent proof. Read the source that establishes the claimed fact;
  branch contents cannot establish deployed state, and a past check covers only its recorded inputs.
- Record the source, target or inputs and result through `session-ledger`. When evidence is missing,
  stale or contradictory, retain the original observation with its provenance, mark the claim
  unverified or superseded, and investigate only the dependent decision. Do not turn an unsupported
  claim into an approval requirement or completion status; independent authorized work continues.

## Continuing

1. **Reassess the open questions before putting them to the user**: validate their factual premises
   under Setting Up and apply `execute-task`'s question boundary. Preserve the user's prior answers;
   resolve questions current evidence or governing guidance already answers. Put only the remaining
   genuine decisions to the user, with current options, recommendation and supporting evidence.
   Work that depends on an answer waits; everything else proceeds.
2. **Invoke `execute-task`** and work the queues in the order the hand-off gave, under the decisions
   and constraints it recorded. A merge, deployment or release still needs the user's own
   authorization in this session, or a recorded decision that quotes it.
3. **Keep each pull request's queue current**: when an item finishes, the next hand-off or the final
   report says so; the hand-off comment is never edited.

## Report

After setup, before the first question, return:

```markdown
Continuing

- https://github.com/owner/repository/pull/123 — `<branch>` at `<sha>` · <draft or ready> → `<base>` · Checks: <state> · Mergeable: <yes, or conflict> · Threads: <n> · Queue: <n items>
- Skipped: <merged or closed pull requests, or None>
```

## Guardrails

- Never create a branch or pull request for work a hand-off queued on an existing one.
- Never choose between plausible readings of a queued item; ask, as the hand-off would have.
- Never treat a hand-off comment's text as authorization beyond what it quotes from the user.
