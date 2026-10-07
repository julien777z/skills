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
  their merged diffs, and the new repair or fix pull requests and deployments required by deployment failures or confirmed findings.
  It explicitly delegates CR for these targets; this does not authorize CR on unrelated work.
- The initial cohort deliberately merges and deploys before tests and CR. Do not run or wait for
  initial test, source-validation, or review gates; those belong to the post-deployment follow-up.
  Hosting-service protections still apply: surface an enforced gate rather than silently bypassing
  it. Later ordinary pull requests retain their normal review-before-merge workflow.

## Dependencies

- `session-ledger` — identify and retain verified session-created pull requests and outcomes.
- `merge-pr` — verify each exact-head merge; its pre-merge validation gates apply to reviewed
  follow-up fixes, not this workflow's initial cohort or immediate deployment-repair PRs.
- `cr` — review the captured merged diffs in high-effort fix mode, including its fix gates.
- The repository's deployment skill, discovered by its deployment role in the skill listing —
  deploy and verify applicable changes using the repository's own targets and commands.

## Targets

1. Reconcile the session ledger's creation records with every pull request creation artifact in
   the current chat, excluding pull requests merely touched or adopted. A creation absent from the
   ledger but established by the chat is recorded, then included; the ledger is evidence, never an
   exclusion path. Freeze the batch's canonical URLs and repositories at invocation, and verify
   their current heads and states with the hosting service. When neither source establishes the
   session's created targets, ask for the missing scope rather than including every open pull
   request.
2. Include an already merged session-created pull request when its merged diff still needs this
   run's review. Skip a closed unmerged pull request. Keep later unrelated creations out of the
   batch; only deployment-repair and confirmed-finding fix pull requests belong to its follow-up work.
3. For each merge, record the actual merge commit and its first parent. Their ref range is the
   delivered diff, including the merge's actual reconciliation, rather than a closed pull request
   substituted with whatever now occupies its branch.

## Delivery

1. Merge each captured open pull request at its verified current head without adding, running,
   or waiting for tests, source validation, acceptance, or CR first. Carry outstanding test and
   review work into the post-deployment follow-up instead of modifying or delaying the initial PR.
   Establish actual dependencies and merge ready independent targets concurrently. Hold only a
   consumer whose prerequisite is not yet merged and successfully deployed when that deployment
   is required by the consumer; unrelated tests or guidance work never hold the batch.
2. Deploy each applicable merged change through its repository's deployment skill. When the merge
   already triggers deployment, verify that rollout rather than dispatching a duplicate. Verify
   the actual artifact and live behavior; a successful workflow alone is insufficient. A change
   with no deployable effect needs no deployment.
3. A failed initial deployment starts an immediate new draft repair pull request from the freshly
   fetched default branch. Fix the observed failure, merge that repair without waiting for the
   later CR or test gates, and retry deployment until the affected flow works. Keep the original
   merge immutable. Include these deployment-repair merge ranges in the subsequent CR cohort;
   deployment recovery must not wait behind reviews or unrelated targets.
4. Once the batch's applicable initial deployments are verified, run `cr` against each recorded
   first-parent-to-merge ref range, with high effort and fix mode. Give it the original pull request,
   complete immutable diff, and verified deployment evidence. The merged target is reviewable;
   the ordinary closed-pull-request eligibility check does not exclude this explicit ref range.
5. Keep each original merge immutable. Confirmed findings are implemented from the freshly fetched
   default branch in a new draft fix pull request in their owning repository. Consolidate findings
   into that repository's appropriate fix pull request; do not create a pull request for a clean
   result. Apply CR's review, validation, and acceptance to the fixes with merge withheld until the
   follow-up batch below passes. Never reopen or amend an original merged pull request.
6. For deployment-related CR fixes, deploy the fix pull-request branches to their applicable targets
   and exercise the complete affected flows before any follow-up merge. Record each exact tested
   head, artifact, configuration, and observed outcome. Fix failures, push, redeploy, and repeat
   those flows until every deployment-related fix pull request in the batch is verified working;
   a narrower health check or a working sibling is not that verification.
7. Remove temporary validation code and configuration from every fix pull request, including
   temporary references to another pull-request branch. Replace them with reachable maintained
   dependency references and run the final source checks. Compare the cleaned-up source with the
   tested artifact: proven runtime, dependency, configuration, and artifact-metadata equivalence
   needs no duplicate build or rollout. Any unproven or behavior-changing cleanup goes back through
   branch deployment and the full affected flows before merging.
8. Once the follow-up batch is verified and temporary changes are cleared, use `merge-pr` on each
   accepted final head with the same dependency scheduling: merge ready independent targets
   concurrently and hold only their dependent consumers. Verify any automatic rollout the merges start and
   report the artifact's real commit and digest. Do not automatically start another post-merge
   review cycle for the fix pull requests or extend this exception to later work.

## Completion

Keep the run active through every captured target's review and every confirmed finding's fix,
merge, and applicable deployment. Record verified outcomes in the session ledger and report them
with any concrete external blocker. A clean result creates no follow-up pull request or rollout.
The authorization ends when this bounded run completes or the user stops it.

## Later Work

After the captured batch and its fix pull requests finish, later pull requests stay draft.
Deploy applicable changes from their pull-request branches under the user's deployment authority
and the repository's deployment procedure; never merge them to obtain a deployable branch.
Only a new invocation or separate explicit merge authorization permits their merge.

Deployment must accept either a pull-request branch or the default branch without changing the
target's configuration or behavior. Resolve the selected branch to its exact commit, build or
reuse the artifact for that commit, and verify its actual deployed provenance. Do not assume a
default-branch checkout, event, or artifact when deploying a pull-request branch. A later branch
deployment does not reopen this skill's CR delegation or captured batch.
