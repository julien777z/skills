---
name: review-loop
description: Review a change with one independent reviewer in a short loop until both agree. Use when the user asks for a code review, a review loop or "sol loop", and when `review-pass` reviews a pull request.
short_description: 'Review a change with one independent reviewer, fix what it finds, and loop until both agree.'
---

# Review Loop

One reviewer reads the change, the author answers each finding, and a fresh round checks only what
changed. Make the smallest changes that answer real findings, and push back on the rest.

## Dependencies
- `defer-scope`

## Budget

- Three rounds. Round 1 reviews the whole change; later rounds review the changed code and the
  findings still open.
- Five rounds only for security, permissions, auth, data loss, or concurrency, while a blocker or
  should stays open with evidence, or when the user asks.
- Stop early when a round returns only nits. A declined nit, or a fix to comments, docs or
  formatting, needs no new round.
- One reviewer per round, which starts no subagents of its own.

## 1. Scope

1. Run `git status --short`. Never stash, discard, or include unrelated changes.
2. Find the base after `git fetch origin`: for a pull request, `git merge-base HEAD
   origin/<baseRefName>`; otherwise `git merge-base HEAD origin/<default-branch>`. Use the same
   diff command in every round.
3. Write the intent and what is out of scope in one or two sentences, from the user's request.
4. Run the checks CI runs over the touched area, and fix what the change broke before the review.

## 2. Choose The Reviewer

Use the strongest model of a different provider from the author when one is reachable, so the
reviewer does not share the author's blind spots; the user may name another.

- **T3 Code:** call `orchestrator_capabilities` once, pick the latest flagship of another provider
  at high effort, and start each round with a new `delegate_task` (`role: "review"`). Never use
  `t3_thread_send` for a later round.
- **Elsewhere:** start a native subagent on another provider's model where the harness offers one;
  otherwise a fresh subagent on the strongest available model.
- Do not edit the reviewed files while a round runs. A timeout, an error or no reply is not
  approval.

## 3. The Brief

The reviewer gets no history, so the brief carries everything:

```text
Review only. Do not edit, commit, push, comment on PRs, or start subagents.
Repo: <abs path> Base: <sha> Intent: <intent> Out of scope: <scope> Checks: <results>
See: git diff <base> [-- <paths>]; git status --short (read untracked files).
Read surrounding code. Find bugs, broken callers, mismatch with intent, and unsafe
handling of user input (paths, patterns, queries, markup).
Flag new code that re-implements a helper the repo already has (cite it), and
abstractions with a single implementation.
Skip style unless it hides a bug. Flag code, tests or guards the intent does not need.
blocker = intended case wrong. should = a real bug callers will hit, an unsafe input,
or a duplicate of an existing helper. nit = the rest.
List problems you see outside the change separately, with the files a fix would touch.
Reply:
VERDICT: APPROVE or CHANGES
S1 [blocker|should|nit] <file>:<line> <claim>. Fix: <suggestion>
O1 [outside] <files> <claim>
```

## 4. Answer The Findings

Check each finding and its severity against the code yourself.

- **Agree:** make the smallest fix. Prefer deleting or narrowing code over a new lock, cache,
  helper or option. Add one focused test that fails without the fix when the repository has a test
  setup and the intent needs it.
- **Disagree:** say why, with evidence: file and line, a test, or output.
- **Nit:** fix it when it is a one-line change in a line the change already touches; otherwise
  decline it in one line.
- **Outside the change:** fix a bug that is one focused fix in about two files or fewer. Record
  everything else with `defer-scope`, unless `widen-scope` is active for this task.

Rerun the checks and `git diff --shortstat <base>`. If review grew the diff past what the intent
needs, cut first. Never agree just to end the loop.

## 5. Next Round

Start one only while budget remains and a blocker or should is open, or behaviour code changed
since the last approval. Send the round 1 brief, the ledger (`fixed:`, `disagree:`, `declined:`,
each with evidence), the same base diff and the change since the last round. Ask the reviewer to
check open ids and changed code only, marking each `resolved` or `still open: <reason>`.

## 6. Stop

- **Agreed:** APPROVE on the current diff, no blocker or should open, no concern of your own.
- **Stuck:** a finding stays disputed after two replies, or the budget runs out. Show both sides in
  two or three lines each; the user decides. A spent budget is not approval.

When the user only asked for a review, stop after round 1 and report the findings without fixing.

## Output

```markdown
**Review loop:** <n> round(s) with <model> — <approved | stuck on <ids> | review only>

- **Fixed:** <id: one clause each, or none>
- **Declined:** <id: reason each, or none>
- **Outside the change:** <fixed id | deferred id with record link, or none>
- **Diff:** <shortstat before> → <shortstat after>
```
