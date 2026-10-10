---
name: merge-pr
description: Merge the task's finished source pull requests quickly at the user's command — each once acceptance passes and its CI is green apart from failures the default branch shares — then run CR on what merged and merge the fix pull requests it produces. Use only when the user directly invokes it.
short_description: 'Merge finished pull requests after acceptance and CI, then CR what merged.'
disable-model-invocation: true
---

# Merge PR

Merge the work the user has reviewed without making them wait on a full review loop first, and
review what merged afterwards.

## Authorization

- Only a direct user invocation starts this workflow. Creating or editing this skill, a plan step,
  an earlier run, or an automatic caller is never an invocation.
- The invocation authorizes, for this run only: the squash merge of each target below; `cr` in fix
  mode over each merged range, which `cr` recognizes as delegated from this skill; the fix pull
  requests those findings need, one per repository; and their merges. It authorizes no deployment,
  release, or review of unrelated work.
- Never ask to merge a target and never end by offering a merge; what stops one is a gate under
  **Merge**, reported with its evidence.

## Dependencies

- `list-prs` — the task's open pull requests when the user names none.
- `acceptance-gate` — the final-acceptance verdict on each head before it merges.
- `land-pr` — the exact-head check gate, conflict resolution and the verified squash merge.
- `cr` — the fix-mode review of each merged range, delegated by this invocation.
- `session-ledger` — record each merge, fix pull request and outcome.

## Targets

1. The pull requests the user names, or else every open pull request `list-prs` returns for the
   task. Freeze that set at invocation and verify each head and state on the host.
2. Leave out a pull request confined to agent configuration; guidance delivery merges those.
3. A pull request still in draft is finished first: its task's `execute-task` **Completion** runs,
   unless the user named it, in which case it is taken as it stands.

## Merge

Targets with no dependency on one another proceed concurrently; a consumer waits for the target it
depends on to merge.

1. **Acceptance.** Reuse `acceptance-gate`'s final-acceptance verdict when the head it accepted is
   the current head, or a rewrite whose tree is identical to it. Otherwise put the head to the
   final-acceptance question. A flag is fixed and gated under that skill's **Bounds**; one still
   standing after them holds the target with the open flags.
2. **CI.** Invoke `land-pr` with the accepted head, merge authorized, and every hosted check on
   the head required. A failing check that fails the same way on the default branch's latest run
   is a baseline: pass it to `land-pr` as an exclusion with that run as evidence, and it does not
   block. Every other failure is fixed and the gate repeats on the new head.
3. **Merge.** `land-pr` squash-merges at the gated head and verifies it. Record the merge commit and
   its first parent.

## Review What Merged

1. Run `cr` in fix mode over each `first-parent..merge-commit` range, giving it the original pull
   request. A clean range ends there.
2. Confirmed findings go into one draft fix pull request per repository, cut from the freshly
   fetched default branch. The original merge is never amended or reopened.
3. Each fix pull request takes **Merge** steps 1–3. It gets no further CR round.

## Report

Send exactly this shape. A held target's "Merged at" cell reads `held: <gate and evidence>`, and the
**Not merged** line names it; `none` otherwise. **Next** names the one thing the user may want to do,
or says nothing is needed.

```markdown
**Merged <n> of <total>.** CR found <count> issue(s); <their fix PRs are merged too | clean>.

| PR | Acceptance | CI | Merged at |
| --- | --- | --- | --- |
| [<owner>/<repo>#<number>](<url>) | <reused (head unchanged) | accepted on `<sha>`> | <green | green; `<check>` failing on `<default>` too, not blocking> | `<sha>` |

**CR on what merged**
- <repo>: <clean, no fix PR | <n> confirmed finding(s), <one-line summary>. Fixed in [<repo>#<number>](<url>), accepted, CI green, merged at `<sha>`.>

**Not merged:** <none | <PR> — <gate>>

**Next:** <one action, or nothing needed>
```
