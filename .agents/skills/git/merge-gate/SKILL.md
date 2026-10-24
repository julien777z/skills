---
name: merge-gate
description: Merge a pull request its caller is authorized to merge — verify its delivery dependencies before taking it out of draft, gate its exact head, resolve merge conflicts, squash-merge and verify the merge. Use when a workflow reaches an authorized merge — `execute-task`'s Completion, a guidance batch's delivery, a user-invoked `finish-pr` or `merge-now`, or a doctor's merged batch. A pull request leaves draft only here; newly introduced PR or testing dependencies block that transition and merge. Unchanged references already on the default branch are exempt from that dependency gate.
short_description: 'Ready a pull request for its authorized merge, gate its exact head, and merge it.'
---

# Merge Gate

Merge one pull request at the head its caller accepted, and only after every check that head needs
has reached a terminal result. A verified merge completes this skill, except for required Agent Sync
handling after an agent-configuration change.

## Authorization

- This skill merges only a pull request whose merge its caller is authorized to perform: a user
  instruction naming the merge and the pull request, an invoked skill that states its invocation
  authorizes the merge, or a rule that authorizes that merge. It creates no authorization of its own,
  and without one it is not invoked: the pull request stays draft.
- Once that authorization holds, never ask the user for permission to merge and never end by
  offering the merge as the remaining step. What stops a merge is a gate: a relevant required check
  that is not green, a head that no longer matches the accepted SHA, or a conflict still unresolved.
  Report that gate.
- Dispatching a release workflow or creating a deployment is a separate action with its own
  authorization.

## Dependencies

- `merge-conflict` — resolve every base incorporation this skill performs.
- `pre-production` — the encountered-issue policy a failed check falls under.
- `reconcile-skills` — refresh the installed shared guidance after successful Agent Sync when the
  GitHub rules select that route.

## Inputs

The caller supplies the repository, the pull request, the head SHA its final acceptance passed, the
affected behaviors its local tests already cover, and the rule that decides what a fix made here
reopens in its own review. For every local result this gate relies on, obtain a receipt from the
caller or native validation evidence identifying its command and covered behavior, source head,
resolved dependencies, configuration, toolchain and runner inputs, successful result, and durable
output. Missing evidence prevents reusing that result or admitting a local-coverage exclusion; it
never waives hosted coverage. The caller also supplies each validation exclusion: a current-user
direction to leave a named test or check alone, a baseline exclusion established by `execute-task`'s
**Encountered Issues** classification with its default-branch evidence, or evidence that a hosted
runner or provider cancellation meets the GitHub rule's pre-validation and local-coverage
conditions. A caller with no such rule has each fix's diff judged the way it judged the accepted
head before the gate repeats.

## Transport

Use GitHub's REST API for every read, check query and merge. The ready-for-review transition has no
REST endpoint — a REST update ignores `draft` and can answer 200 with the pull request still draft —
so make it through GraphQL `markPullRequestReadyForReview` with the pull request's node id, then
re-read the pull request over REST and require `draft` to be `false` before reading any check.
A rate limit is waited out through the host's wait mechanism and retried on the same transport.

## Check Gate

1. **Bind the accepted head before the gate.** Re-read the pull request and record its head and base
   SHA. Its head must equal the SHA that passed acceptance before dependency inventory, readiness,
   receipt reuse, exclusions, or hosted-result inventory; otherwise send its new commits through the
   caller's rule and restart this gate.
2. **Verify delivery dependencies before readiness.** Inventory what the complete consumer head
   resolves for its build, validation, packaging and delivered behavior, following the
   [delivery dependency criteria](references/delivery-dependencies.md). Compare every consuming
   location, configured reference and resolved revision with the freshly fetched default branch;
   retain that comparison with the admission verdict. Newly introduced or changed PR/testing
   references in workflows, application code, manifests or lockfiles block readiness and merge.
   Exempt only the same input already present unchanged at that location on the default branch;
   a new location or changed resolution is not inherited. For nonexempt inputs, verify each
   provider's merged state and each resolved revision's provenance; a branch label or immutable
   identifier alone proves neither. A testing dependency, or missing provenance, keeps the
   consumer draft and blocks both readiness and merge, even with passing tests. Convert an
   already-ready consumer back to draft through GraphQL `convertPullRequestToDraft` and verify
   `draft` true over REST. Surface the provider dependency and its evidence in user chat under the GitHub
   rule's independent publishing context; the body states only the consumer's own delivery requirement. Draft validation and review may continue. After the
   dependency merges, update every consuming reference to the maintained target chosen by the
   user or repository guidance, revalidate the consumer's new head through the caller's fix rule,
   and repeat this inventory before taking it ready. This gate authorizes no dependency merge
   or release; never take a blocked consumer ready to start tests or send a ready message.
3. **Require a pull request ready for review.** Mark a draft ready when review requires it. That
   state-only transition can start duplicate test jobs; it does not invalidate a terminal result
   already produced for the exact head. Reuse that result only when the source, resolved
   dependencies, configuration, toolchain, runner, trigger context, job conditions, and affected
   behavior coverage are evidenced equivalent. A test job `skipped` because the pull request was
   draft is no result. If readiness makes a previously skipped job applicable or changes any of
   those inputs, obtain its fresh terminal result. Otherwise, do not wait for or rerun an equivalent
   duplicate job.
4. **Classify the complete pull-request diff.** A non-runtime diff — one that changes no executable
   source, package or dependency definition, test, runtime configuration, CI workflow, generated
   runtime artifact, or other executed-behavior contract — is validated only by the checks its
   artifacts need, its exact contents, and `git diff --check`; application tests, check runs and CI
   are not consulted. The classification is semantic rather than path-based: instructions,
   documentation, policies, static metadata and non-executable configuration live anywhere.
5. **For a runtime diff, inventory every check on the exact head.** Read every page of check runs
   and legacy statuses, including every workflow job, rather than only required checks or jobs
   selected by local coverage. Inspect the active workflow triggers and job conditions to account
   for missing jobs. Passing local tests never replaces this inventory or a hosted job's result.
   Record each logical job's representative run, head, state and conclusion, every equivalent
   duplicate attempt, and each caller-supplied exclusion with its evidence. A completed successful
   representative covers its equivalent duplicates; a changed trigger, condition, execution input,
   or affected behavior does not.
   A skipped or neutral job supplies no coverage: establish whether its native condition makes it
   inapplicable, or required validation is missing. Draft skips never supply test coverage. A job
   without a check run or status needs the same applicability decision, not an assumed pass.
   Before using a local receipt, compare its source head and resolved dependency, configuration,
   toolchain and runner inputs with the proposed execution; a branch label alone is insufficient.
   Reuse it only for unchanged inputs or evidenced equivalence, and revalidate the affected coverage
   on drift. That receipt may support an exclusion under step 8; it never omits the hosted inventory.
6. **Drive the complete inventory to terminal results.** Re-query the exact head on a bounded
   interval matched to job duration — roughly every 30 to 60 seconds — until every applicable,
   non-excluded logical job has terminal coverage. A completed successful representative means an
   equivalent duplicate attempt does not hold the gate. Local coverage, a green selected job or a
   branch-protection summary does not permit omitting another job. Classify failures under step 8
   and account for missing or skipped required validation before clearing the gate. A new head
   rebuilds the inventory. When the base moves, compare its changes with every execution input
   before reusing evidence; retain a result only with evidence that those inputs are equivalent.
   Otherwise incorporate the base through `merge-conflict`, run the caller's rule over the resolved
   head, and restart this gate. Do not end the turn or hand back while the gate is pending; its poll
   loop is the work.
7. **A pending status is a cache, not evidence.** Status endpoints keep reporting `in_progress` after
   a job has finished, sometimes for an hour or more. Learn what the job normally costs from the same
   job on an earlier head or on the base branch; once a check is pending well past that, read the
   job's own output — the run's jobs listing and decisively its log, which a finished job ends with
   its summary and cleanup. A log showing completion **is** the terminal result. Never diagnose a
   hang, push a speculative fix, cancel, re-run, or report the run stuck from a pending status alone.
8. **Classify every unsuccessful check before repair.** A caller-supplied exclusion, a current-user
   waiver for its named test or check is excluded. Preserve established baseline classifications;
   classify a newly encountered possible baseline under `execute-task`'s **Encountered Issues**,
   without reentering that skill's active run. Record an exclusion's evidence, remove it from
   required coverage, and do not repair, rerun, or wait for it. Apply the
   GitHub rule's runner-infrastructure exclusion automatically: record a qualified check as skipped
   and do not rerun or wait for a green hosted result. Every other failure is relevant. Read its
   annotations and complete log, fix the repository
   input responsible — code, test, configuration or workflow — and commit it. **Every relevant
   failure on the head goes into one push**: read all of them before fixing any, reproduce each
   with the job's own command where it can run locally, and push only once each reproduced failure
   passes locally, so the next hosted run is the last. Only a failure that cannot run locally —
   a hosted service, credentials, runner-specific behavior — is pushed without local proof. A relevant
   external-service failure is an encountered issue under `pre-production` and is fixed the same way;
   never re-run a job, or skip, disable, or quarantine a test or confine its job to drafts, to get
   past it. Report a blocker only when relevant missing coverage needs user input or unavailable
   credentials, with the check, evidence and remediation attempted.
9. Never stop, restart, reconfigure or claim a local service the calling workflow did not start:
   another agent or person may be using it. When relevant validation needs local services and one it
   did not start is running, use the matching hosted check as the fallback rather than running a
   competing service-managed test.
10. Every fix made here goes through the caller's rule from **Inputs**, and the gate repeats on the
   new head.

## Merge Conflicts

When GitHub reports a conflict, or the merge is rejected for one:

- Incorporate the base through `merge-conflict`; the resolution is a fix under **Check Gate** step 10.
- Report a blocker only when a safe resolution needs an unauthorized product decision, or a change
  to a contract a consumer outside the user's control speaks.

## Merge

Recheck delivery dependency state, resolved revisions and the recorded default-branch comparison,
then re-read the pull request after the check gate and require its head to equal the head that passed
acceptance. On a head mismatch, put the added commits through the caller's rule and repeat the check
gate. On a base mismatch, apply step 5's execution-input comparison and, when equivalence is not
evidenced, incorporate it through `merge-conflict`, run the caller's rule, and repeat the gate. Then
squash-merge
with the accepted head SHA in the request —
`PUT /repos/{owner}/{repo}/pulls/{number}/merge` with `merge_method=squash` and `sha` — so GitHub
refuses a concurrent head change. After the merge, re-read the pull request and require it to report
merged.

An excluded failed check does not prevent that ordinary authorized merge attempt. If the provider
rejects it because branch protection requires the excluded check, leave the pull request open and
report that actual rejection and its provider evidence; do not bypass protection.

Do not inspect or follow merge-triggered release, publication, artifact, or deployment workflows.
A separate direct delivery or release task owns that work and its verification.

When the merged diff changes agent configuration, poll the default-branch Agent Sync run the merge
started as **Check Gate** steps 6–7 poll a check. A run ending in anything but success is diagnosed
from its log and reported. After a successful run, complete the refresh selected by the GitHub
rules' **After Agent Sync** section and verify its installed links before reporting completion.

## Report

```markdown
Merged: [<owner>/<repo>#<number>](<url>) at <short sha> — checks: <local only | names of hosted checks and results> — sync: <run result | not agent configuration>; refresh: <installed source and commit | blocked: exact reason | not agent configuration>
```

Or, when a gate holds: `Not merged: <link> — <gate>: <evidence>`. The evidence includes each
relevant check's terminal result, read from its log where its status was stale.
