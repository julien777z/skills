---
name: merge-now
description: Merge the task's finished source pull requests quickly at the user's command — each once acceptance and its canonical check gate pass — then review the merged changes no earlier review pass covered and merge the fix pull requests that review produces. Use only when the user directly invokes it.
short_description: 'Merge finished pull requests now, then review what merged unreviewed.'
disable-model-invocation: true
---

# Merge Now

Merge the work the user has reviewed without a review loop at merge time, and review afterwards
whatever merged without an earlier `review-pass`.

## Authorization

- Only a direct user invocation starts this workflow. Creating or editing this skill, a plan step,
  an earlier run, or an automatic caller is never an invocation.
- The invocation authorizes, for this run only: the squash merge of each target below;
  `review-pass` over each merged range; the fix pull requests its findings need, one per
  repository; and their merges. It authorizes no deployment,
  release, or review of unrelated work.
- Never ask to merge a target and never end by offering a merge; what stops one is a gate under
  **Merge**, reported with its evidence.

## Dependencies

- `list-prs` — the task's open pull requests when the user names none.
- `acceptance-gate` — the final-acceptance verdict on each head before it merges.
- `merge-gate` — the exact-head check gate, conflict resolution and the verified squash merge.
- `review-pass` — the review and fix loop over each merged range's unreviewed changes.
- `session-ledger` — record each merge, fix pull request and outcome.

## Targets

1. The pull requests the user names, or else every open pull request `list-prs` returns for the
   task. Freeze that set at invocation and verify each head and state on the host.
2. Leave out a pull request confined to agent configuration; guidance delivery merges those.
3. A pull request whose task's `execute-task` **Completion** has not sent its review message is
   finished first: that **Completion** runs, unless the user named the pull request, in which case
   it is taken as it stands. Every pull request is a draft until `merge-gate` merges it, so being a
   draft says nothing about whether it is finished.

## Merge

Targets with no dependency on one another proceed concurrently; a consumer waits for the target it
depends on to merge.

1. **Acceptance.** Reuse `acceptance-gate`'s final-acceptance verdict when the head it accepted is
   the current head, or a rewrite whose tree is identical to it. Otherwise put the head to the
   final-acceptance question. A flag is fixed and gated under that skill's **Bounds**; the
   target waits while one stands.
2. **Check gate.** Invoke `merge-gate` with the accepted head, validation receipts and established
   exclusions. Its **Check Gate** owns complete-diff classification, check inventory, failure
   handling and the evidence required before merging.
3. **Merge.** `merge-gate` squash-merges at the gated head and verifies it. Record the merge commit and
   its first parent.

## Review What Merged

1. Run `review-pass` over each `first-parent..merge-commit` range, giving it the original pull
   request. It reviews only what the pull request's last accepted `review-pass` head did not cover,
   so a pull request merged unchanged since its automatic review needs nothing. A clean range ends
   there.
2. Confirmed findings go into one draft fix pull request per repository, cut from the freshly
   fetched default branch. The original merge is never amended or reopened.
3. Each fix pull request takes **Merge** steps 1–3. It gets no further review round.

## Report

Send exactly this shape. A held target's "Merged at" cell reads `held: <gate and evidence>`, and the
**Not merged** line names it; `none` otherwise. **Next** names the one thing the user may want to do,
or says nothing is needed.

```markdown
**Merged <n> of <total>.** Review found <count> issue(s); <their fix PRs are merged too | clean>.

| PR | Acceptance | Check gate | Merged at |
| --- | --- | --- | --- |
| [<owner>/<repo>#<number>](<url>) | <reused (head unchanged) | accepted on `<sha>`> | <passed | passed; verified exclusion: `<check>` — <gate evidence>> | `<sha>` |

**Review of what merged**
- <repo>: <nothing unreviewed | clean, no fix PR | <n> confirmed finding(s), <one-line summary>. Fixed in [<repo>#<number>](<url>), accepted, check gate passed, merged at `<sha>`.>

**Not merged:** <none | <PR> — <gate>>

**Next:** <one action, or nothing needed>
```
