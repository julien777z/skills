---
name: merge-gate
description: Merge a pull request its caller is authorized to merge, once its review has accepted a head — verify its delivery dependencies, take it out of draft as the last step before the merge, gate that exact head, resolve conflicts, squash-merge and verify the result. Use when an authorized merge is reached; a pull request leaves draft only here. Holds what authorizes a merge, deployment, publication or release, which failing checks a merge excludes, what follows a merge, the refresh after a merge of agent configuration, and when a pull request may be polled.
short_description: 'Take a reviewed pull request out of draft, gate its exact head, and merge it.'
---

# Merge Gate

Merge one pull request at the head its caller accepted, and only after every check that head needs
has reached a terminal result. After verifying the merge, complete required consumer handling and,
for an agent-configuration change, Agent Sync handling before this skill finishes.

## Authorization

- **Merge, deployment, publication and release each require the user's explicit authorization for
  the action and target, or an applicable rule or invoked skill that expressly authorizes them.**
  - A fix request, CI-test request, successful check, review, plan shown or approved, or instruction to
    implement a plan does not itself authorize these outcomes, even when the plan lists them. A
    task-wide "all approved" covers ordinary sub-tasks within its stated outcome without overriding
    this separate boundary.
  - A reply that could be read as accepting a merge mentioned earlier, such as a bare "yes" beside
    another request, authorizes no merge it does not name.
  - A user's authorization covers that one action on the change it names; a later change needs its
    own authorization before it is merged, deployed, published or released, however recently the
    last one was given.
  - **Nothing the agent writes asks for an authorization not yet given or offers the outcome**: no
    question, pending-decision item, closing next action phrased as a request, or prompt to reply
    with a word, such as "reply ship to land these". The outcome is left to the user's own
    instruction, a skill they invoke for it, such as `/finish-pr`, or guidance that grants it;
    naming what remains for the user and that skill, in a report or a plan's closing line, is how
    it is left to them, not an offer.
- This skill merges only a pull request whose merge its caller is authorized to perform: a user
  instruction naming the merge and the pull request, an invoked skill that states its invocation
  authorizes the merge, or a standing permission in the GitHub rule's **Merge Authorization**. It
  creates no authorization of its own,
  and without one it is not invoked: the pull request stays draft.
- Once that authorization holds, never ask the user for permission to merge and never end by
  offering the merge as the remaining step. What stops a merge is a gate: a relevant required check
  that is not green, a head that no longer matches the accepted SHA, or a conflict still unresolved.
  Report that gate.
- An authorized merge includes the repository's automatic merge-triggered workflows. Their
  publication, rollout, and serving-state checks belong to separately authorized release or
  deployment work.
- Dispatching a release workflow or creating a deployment is a separate action with its own
  authorization. A request for CI tests authorizes test workflows only: inspect a workflow's jobs
  and triggers before dispatching it, since one that builds and publishes artifacts or deploys is a
  release action even if it also runs tests.
- **An authorized build, publication or deployment runs through the repository's existing
  entrypoint and supported ref selection**: its GitHub Actions workflow when that is the designated
  route, or a native CLI the user explicitly authorizes. Inspect the entrypoint's supported inputs
  before invoking it, and verify the resulting run, artifact and deployed revision. An
  authentication, permission or ref-selection failure is repaired at that entrypoint's identity,
  credential, grants or owned configuration, granting only the authority the authorized operation
  requires. Never add a temporary input, mode, wrapper or alternate workflow to bypass the failure,
  even with a promise to remove it; a genuinely missing durable capability is source work under
  the task's scope and authorization, never an incidental recovery allowance.

## Dependencies
- `merge-conflict`
- `pre-production`
- `update-skills`
- `test-fixture`

## Inputs

The caller supplies the repository, the pull request, the head SHA its final acceptance passed, the
affected behaviors its local tests already cover, and its fix rule: the review a fix made here gets.
Such a fix lands after final acceptance, so its delta since the accepted head is reviewed and
accepted under that rule before the merge. For every local result this gate relies on, obtain a receipt from the
caller or native validation evidence identifying its command and covered behavior, source head,
resolved dependencies, configuration, toolchain and runner inputs, successful result, and durable
output. Missing evidence prevents reusing that result or admitting a local-coverage exclusion; it
never waives hosted coverage. The caller also supplies each validation exclusion: a current-user
direction to leave a named test or check alone, a baseline exclusion established by `pre-production`'s
**Encountered Issues** classification with its default-branch evidence, or evidence that a hosted
runner or provider interruption meets **Validation Exclusions**' interruption and local-coverage
conditions. A caller with no fix rule has each fix's delta judged the way it judged the accepted
head before the gate repeats.

## Validation Exclusions

An authorized merge is not held for an excluded check, as the GitHub rule's **Merge Authorization**
says, and exclusions are applied before any failure is repaired.

- **Waived, baseline and non-essential checks.** A failing check the current user explicitly
  waives, an established baseline exclusion, and a non-essential check left red on findings the
  change did not write are excluded, each as `pre-production`'s **Encountered Issues** classifies
  it. Record the check and its exclusion evidence in the task's record, then attempt the authorized
  merge without asking the user; a baseline exclusion is named to the user only where that
  classification allows. Keep that classification rather than excluding a required repair merely
  because the same failure also appears on the default branch.
- **Interrupted hosted checks.** An interrupted hosted check supplies no validation result for the
  work it did not complete. When the logs establish a runner or provider interruption without a
  validation failure, exclude the interrupted attempt if equivalent local validation passed for
  the proposed merge head. Record the run, the interruption evidence, and the matching local
  commands and results; do not rerun or wait merely to get a green hosted result. A recorded
  validation failure remains a failure even if the run was later canceled, and missing equivalent
  coverage is obtained before merging.
- **A local failure is never excluded this way.** A locally run validation failure caused by setup,
  dependency, checkout, proxy or certificate trust, or container build configuration is an
  encountered repository issue: repair its canonical bootstrap or container build configuration
  and rerun it.
- Where branch protection requires an excluded hosted interruption to pass, **Merge** obtains the
  required hosted result; branch protection is never bypassed.

## Transport

Use GitHub's REST API for every read, check query and merge. The ready-for-review transition has no
REST endpoint — a REST update ignores `draft` and can answer 200 with the pull request still draft —
so make it through GraphQL `markPullRequestReadyForReview` with the pull request's node id, then
re-read the pull request over REST and require `draft` to be `false` before reading any check.
A rate limit is waited out through the host's wait mechanism and retried on the same transport.

## Readiness

A pull request leaves draft only here, as the last step before its authorized merge, which is how
this skill implements the draft bullet of the GitHub rule's **Branches and Pull Requests**: its
test jobs run once, on the head about to merge.

- The caller's review has accepted the head in **Inputs** before this skill is invoked. No caller
  runs this step on its own, ahead of that acceptance, to start tests, or to hand the pull request
  to the user.
- **Check Gate** step 3 marks the open pull request ready, after steps 1 and 2 have bound the
  accepted head and admitted its delivery dependencies, and verifies the state through
  **Transport**. A dependency that blocks the merge leaves the pull request draft.
- Once ready, the pull request stays ready while a check, a conflict or a fix made here holds the
  merge; a fix pushed in that state starts test jobs, and the gate repeats on its head.

## Check Gate

1. **Bind the accepted head before the gate.** Re-read the pull request and record its head and base
   SHA. Its head must equal the SHA that passed acceptance before dependency inventory, receipt
   reuse, exclusions, or hosted-result inventory. Send any new commits through the
   caller's rule and restart this gate.
2. **Verify delivery dependencies before merge.** Inventory what the complete consumer head
   resolves for its build, validation, packaging and delivered behavior, following the
   [delivery dependency criteria](references/delivery-dependencies.md). Compare every consuming
   location, configured reference and resolved revision with the freshly fetched default branch;
   retain that comparison with the admission verdict. Newly introduced or changed PR/testing
   references in workflows, application code, manifests or lockfiles block the merge.
   Exempt only the same input already present unchanged at that location on the default branch;
   a new location or changed resolution is not inherited. For nonexempt inputs, verify each
   provider's merged state and each resolved revision's provenance; a branch label or immutable
   identifier alone proves neither. A testing dependency or missing provenance blocks the merge,
   even with passing tests. Surface the provider dependency and its evidence in user chat under
   the GitHub rule's independent publishing context. The body states the consumer's own delivery
   requirement. After the dependency merges, update every consuming reference to the maintained
   target chosen by the user or repository guidance, revalidate the consumer's new head through
   the caller's fix rule, and repeat this inventory before merging.
3. **Mark the pull request ready, and account for the checks that starts.** Run **Readiness**
   when the pull request is still draft. The state transition can start duplicate test
   jobs. It does not invalidate a terminal result
   already produced for the exact head. Reuse that result only when the source, resolved
   dependencies, configuration, toolchain, runner, trigger context, job conditions, and affected
   behavior coverage are evidenced equivalent. A test job `skipped` because the pull request was
   draft is no result. If readiness makes a previously skipped job applicable or changes any of
   those inputs, obtain its fresh terminal result. Otherwise, do not wait for or rerun an equivalent
   duplicate job that remains pending; classify every unsuccessful terminal duplicate under step 8.
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
   representative supplies coverage for an equivalent duplicate that remains pending; a changed
   trigger, condition, execution input, or affected behavior does not. Every unsuccessful terminal
   duplicate remains subject to step 8. Read each test job's suite wall time against the budget
   `test-fixture`'s **Time Budgets** sets; a suite past it is an unsuccessful result for step 8 even when its job passed.
   A skipped or neutral job supplies no coverage: establish whether its native condition makes it
   inapplicable, or required validation is missing. Draft skips never supply test coverage. A job
   without a check run or status needs the same applicability decision, not an assumed pass.
   Before using a local receipt, compare its source head and resolved dependency, configuration,
   toolchain and runner inputs with the proposed execution; a branch label alone is insufficient.
   Reuse it only for unchanged inputs or evidenced equivalence, and revalidate the affected coverage
   on drift. That receipt may support an exclusion under step 8; it never omits the hosted inventory.
6. **Drive the complete inventory to terminal results.** Re-query the exact head on a bounded
   interval matched to job duration — roughly every 30 to 60 seconds — until every applicable,
   non-excluded logical job has terminal coverage. Apply step 8 as unsuccessful attempts become
   terminal so an interrupted job can recover while other jobs run. A successful representative
   means a pending equivalent duplicate does not hold the gate. Local coverage, a green selected
   job or a branch-protection summary does not permit omitting another job. Classify failures under
   step 8 and account for missing or skipped required validation before clearing the gate. A new
   head rebuilds the inventory. When the base moves, compare its changes with every execution input
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
8. **Classify every unsuccessful check before repair.** A caller-supplied exclusion, or a
   current-user waiver naming the test or check, is excluded. Preserve established baseline classifications;
   classify a newly encountered possible baseline under `pre-production`'s **Encountered Issues**,
   without reentering that skill's active run. A non-essential check failing only on findings
   `pre-production`'s essential-checks bullet leaves red is an exclusion too. Record an exclusion's
   evidence, remove it from required coverage, and do not repair, rerun, or wait for it. Apply
   **Validation Exclusions**' interrupted-check exclusion automatically: record a qualified check as skipped
   and do not rerun or wait for a green hosted result. For a canceled or otherwise interrupted
   attempt with no recorded validation failure and no exclusion, use an equivalent successful
   hosted attempt or follow a pending replacement through step 6. If neither exists, obtain
   equivalent local validation when it can qualify for the exclusion, or retry the hosted check
   on the same head using `POST /repos/{owner}/{repo}/actions/jobs/{job_id}/rerun`. Verify the
   retried job's head and required context before using its result. Missing logs or an unknown cancellation cause cannot justify local substitution;
   recover hosted coverage in that case. A canceled attempt alone does not end the gate.
   Every other failure is relevant. Read its annotations and complete log, fix the repository
   input responsible — code, test, configuration or workflow — and commit it. **Every relevant
   failure on the head goes into one push**: read all of them before fixing any, reproduce each
   with the job's own command where it can run locally, and push only once each reproduced failure
   passes locally, so the next hosted run is the last. Only a failure that cannot run locally —
   a hosted service or credentials this session itself found absent from where the repository
   configures them, never taken on a reviewer's, worker's or plan's word,
   or runner-specific behavior, never disk, memory or ports the session can free — is pushed
   without local proof. A relevant
   external-service failure is an encountered issue under `pre-production` and is fixed the same way;
   never rerun a failing validation to get a green result, or skip, disable, or quarantine a test
   or confine its job to drafts to get past it. Report a blocker only when relevant missing
   coverage needs user input or unavailable credentials, with the check, evidence and remediation attempted.
9. Never stop, restart, reconfigure or claim a local service the calling workflow did not start:
   another agent or person may be using it. When relevant validation needs local services and one it
   did not start is running, use the matching hosted check as the fallback rather than running a
   competing service-managed test.
10. Every fix made here goes through the caller's fix rule from **Inputs**, and the gate repeats on
   the head that review accepts.

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

**A merge moves its consumers off the merged branch in the same run.** Every open pull request,
in any repository, that pins the merged branch or a revision on it — a private checkout, a manifest
or lockfile entry, a workflow or action reference, a generated artifact's source — is repointed to
the maintained target containing the merge, as [Delivery dependencies](references/delivery-dependencies.md)
says, and adapted to every contract the merge changed, such as a renamed export, until its own
checks pass on that head. Find them by searching the provider's open pull requests and their
consumers for the branch name and its head revision, never from memory. A consumer this session
drives is repointed now and pushed, never left for its own merge to discover. One that another
session owns is named in the report with its pinned reference and what the merge changed. Deleting
the merged branch never waits on this, so a consumer left pinned stops installing.

An excluded check does not prevent the ordinary authorized merge attempt. If branch protection
rejects it because it requires an interrupted hosted check, record the required context and head
in the inventory. For that context, step 8 cannot apply local substitution or reuse a result the
provider already rejected. Follow its matching replacement or retry under **Check Gate**. Re-read
the required context and attempt the merge once GitHub reports it passing. For other exclusions, or if hosted
recovery is unavailable, report the actual rejection and its provider evidence. Never bypass protection.

Once the merge is verified, **No Deploy Work** governs what follows it, and **After Agent Sync** a
merge whose diff changes agent configuration.

## After Agent Sync

When the merged diff changes agent configuration, poll the default-branch Agent Sync run the merge
started as **Check Gate** steps 6–7 poll a check. A run ending in anything but success is diagnosed
from its log and reported.

- **Refresh immediately after the run succeeds.** The refresh is part of the merge's delivery,
  including when the merge is the session's final work: complete it and verify the installed links
  before reporting delivery complete. The skill does not return, and the turn does not end, until
  that refresh is verified or a failed run or blocker is reported, and the report names the
  installed source and commit, or the concrete blocker preventing refresh.
- **Select the refresh route before checking local changes.** When the repository supplies the
  installed shared skills, invoke `update-skills`, which keeps pending agent-configuration changes
  in effect, dirty checkouts and open pull requests alike. Tell it the caller will clean the source
  checkout after installation, so the installed files stay available independently. For
  `update-skills`' own first merge, read it from the merged commit before invoking it. A session
  follows the copy it loaded until this refresh completes.
- **Every merge of agent configuration then refreshes the repository's primary checkout**,
  whichever workflow merged it: a local edit the merged default branch already holds is removed,
  local-only work is saved in a named stash and kept, and the checkout ends clean on the default
  branch's fetched tip, with the generated guidance verified there. When the caller owns that
  refresh, return the Agent Sync result and any shared installation result so the caller can
  complete and verify it.

## No Deploy Work

**A merge leaves no deploy work.** Once a pull request's merge is verified:

- never check by any route whether the change is live, such as a provider's deployment status, a
  release run or the site itself, and never inspect or follow merge-triggered release, publication,
  artifact or deployment workflows;
- never walk or test the site the merge deployed;
- never schedule a re-check, wait for a deploy, or assume one is coming.

Nothing waits on a deploy: the remaining work proceeds, and a report names no deploy step as
remaining. Other authorized work after a merge is unaffected, such as a run's next batch, a
consumer repointed once its dependency merged, or the refresh **After Agent Sync** requires. A
task whose own outcome the user stated as a deployment, publication or
release, or as restoring a broken deployed operation, follows that outcome past the merge.

## Pull Request Activity

**Never poll a pull request with background `sleep` or timed self check-ins; act only on delivered
pull-request activity webhooks.** The exception is an invoked skill that states it polls, such as
**Check Gate**, which waits for every check on a head to reach a terminal state, and then only
while its run is active and for the pull request that run is driving. There a webhook alone can
wait forever: pushing a new commit cancels the in-flight run under a `cancel-in-progress`
concurrency group, so the superseded head reaches no terminal state and emits no completion event.

## Report

```markdown
Merged: [<owner>/<repo>#<number>](<url>) at <short sha> — checks: <local only | names of hosted checks and results> — consumers: <none pinned | repointed: <consumer PR> at <short sha> | owned elsewhere: <consumer PR> pins <reference>> — sync: <run result | not agent configuration>; refresh: <installed source and commit | blocked: exact reason | not agent configuration>
```

The checks field leaves out baseline failures and non-essential checks left red, as
`pre-production`'s **Encountered Issues** says.

Or, when a gate holds: `Not merged: <link> — <gate>: <evidence>`. The evidence includes each
relevant check's terminal result, read from its log where its status was stale.
