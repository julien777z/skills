---
name: merge-post-review
description: Use only at the user's explicit request to merge and deploy session-created pull requests before reviewing their merged diffs with CR and delivering confirmed fixes through new pull requests. This bounded exception never becomes the default order for later work.
disable-model-invocation: true
---

# Merge Post Review

Merge and deploy the session's pull requests before their CR review, for this invocation only.
Creating or editing this skill is not an invocation.

## Authorization

- Only a direct user invocation starts this workflow. Never choose it as an implementation,
  delivery, merge, or deployment dependency, or infer it from a previous run.
- That invocation authorizes the captured pull requests' merges, applicable deployments, CR on
  their merged diffs, and the new fix pull requests and deployments required by confirmed findings.
  It explicitly delegates CR for these targets; this does not authorize CR on unrelated work.
- The exception changes the order of CR, not required source validation or merge check gates.
  Later ordinary pull requests retain their normal review-before-merge workflow.

## Dependencies

- `session-ledger` — identify and retain verified session-created pull requests and outcomes.
- `merge-pr` — enforce exact-head checks and verify each authorized merge.
- `cr` — review the captured merged diffs in high-effort fix mode, including its fix gates.
- The repository's deployment skill, discovered by its deployment role in the skill listing —
  deploy and verify applicable changes using the repository's own targets and commands.

## Targets

1. Read the session ledger's creation records, excluding pull requests merely touched or adopted.
   Freeze the batch's canonical URLs and repositories at invocation, and verify their current heads
   and states with the hosting service. When task evidence cannot establish the session's created
   targets, ask for the missing scope rather than including every open pull request.
2. Include an already merged session-created pull request when its merged diff still needs this
   run's review. Skip a closed unmerged pull request. Keep later unrelated creations out of the
   batch; only confirmed-finding fix pull requests belong to its follow-up work.
3. For each merge, record the actual merge commit and its first parent. Their ref range is the
   delivered diff, including the merge's actual reconciliation, rather than a closed pull request
   substituted with whatever now occupies its branch.

## Delivery

1. Complete outstanding implementation and required source checks, then use `merge-pr` on each
   captured open pull request at its accepted head. Do not run CR before this batch's initial
   merges. Preserve repository-local ownership and dependency order.
2. Deploy each applicable merged change through its repository's deployment skill. When the merge
   already triggers deployment, verify that rollout rather than dispatching a duplicate. Verify
   the actual artifact and live behavior; a successful workflow alone is insufficient. A change
   with no deployable effect needs no deployment.
3. Once the batch's applicable initial deployments are verified, run `cr` against each recorded
   first-parent-to-merge ref range, with high effort and fix mode. Give it the original pull request,
   complete immutable diff, and verified deployment evidence. The merged target is reviewable;
   the ordinary closed-pull-request eligibility check does not exclude this explicit ref range.
4. Keep each original merge immutable. Confirmed findings are implemented from the freshly fetched
   default branch in a new draft fix pull request in their owning repository. Consolidate findings
   into that repository's appropriate fix pull request; do not create a pull request for a clean
   result. Apply CR's review, validation, acceptance, and exact-head merge gates to the fixes before
   merging them. Never reopen or amend an original merged pull request.
5. Deploy verified fixes where they change the running result. Compare each fix with the artifact's
   actual source: proven behavior-preserving cleanup alone requires no rebuild, publication, or
   rollout. Report the artifact's real commit and digest. Do not automatically start another
   post-merge review cycle for the fix pull requests or extend this exception to later work.

## Completion

Keep the run active through every captured target's review and every confirmed finding's fix,
merge, and applicable deployment. Record verified outcomes in the session ledger and report them
with any concrete external blocker. A clean result creates no follow-up pull request or rollout.
The authorization ends when this bounded run completes or the user stops it.
