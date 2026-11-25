---
name: merge-gate
description: Merge a pull request its caller is authorized to merge, once its review has accepted a head. Use when an authorized merge is reached; a pull request leaves draft only here. Holds what authorizes a merge, deployment, publication or release, which failing checks a merge excludes, what follows a merge, the refresh after a merge of agent configuration, and when a pull request may be polled.
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
- **The merge question was answered when the authorization was given.** When the gates are green and
  the head is the accepted one, merge it. What stops a merge is a gate: a relevant required check
  that is not green, a head that no longer matches the accepted SHA, or a conflict still unresolved.
  Report that gate, never a request to merge or an offer of the merge as the remaining step.
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
- **Check Gate**'s **Mark the pull request ready** marks the open pull request ready, after
  **Bind the accepted head** and **Verify delivery dependencies** have bound the accepted head and
  admitted its delivery dependencies, and verifies the state through
  **Transport**. A dependency that blocks the merge leaves the pull request draft.
- Once ready, the pull request stays ready while a check, a conflict or a fix made here holds the
  merge; a fix pushed in that state starts test jobs, and the gate repeats on its head.

## Check Gate

1. **Bind the accepted head before the gate.** Re-read the pull request and record its head and base
   SHA. Its head must equal the SHA that passed acceptance before dependency inventory, receipt
   reuse, exclusions, or hosted-result inventory. Send any new commits through the
   caller's rule and restart this gate.
2. **Verify delivery dependencies before merge.** Inventory what the complete consumer head
   resolves for its build, validation, packaging and delivered behavior and admit or block each input
   as the [delivery dependency criteria](references/delivery-dependencies.md) say, retaining the
   comparison with the freshly fetched default branch beside the admission verdict. A newly
   introduced or changed PR/testing reference in a workflow, application code, manifest or lockfile,
   a testing dependency and missing provenance block the merge even with passing tests, and a
   blocked dependency leaves the pull request draft. After the dependency merges, update every
   consuming reference to the maintained target, revalidate the consumer's new head through the
   caller's fix rule and repeat this inventory before merging.
3. **Mark the pull request ready, and account for the checks that starts.** Run **Readiness**
   when the pull request is still draft. The state transition can start duplicate test
   jobs. It does not invalidate a terminal result
   already produced for the exact head. Reuse that result only when the source, resolved
   dependencies, configuration, toolchain, runner, trigger context, job conditions, and affected
   behavior coverage are evidenced equivalent. A test job `skipped` because the pull request was
   draft is no result. If readiness makes a previously skipped job applicable or changes any of
   those inputs, obtain its fresh terminal result. Otherwise, do not wait for or rerun an equivalent
   duplicate job that remains pending; classify every unsuccessful terminal duplicate under **Classify every unsuccessful check**.
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
   duplicate remains subject to **Classify every unsuccessful check**. Read each test job's suite wall time against the budget
   `test-fixture`'s **Time Budgets** sets, and for a suite past it, against the same job's latest
   run on the base branch. The merge is held only for slowness this pull request caused, so a
   suite it made slower than that base run is an unsuccessful result for **Classify every unsuccessful check** even when its job
   passed. A suite already past its budget that this pull request did not slow does not hold the
   merge: it is a defect the work noticed, and its fix is placed as `pre-production`'s **Scope
   Follows The Defect, Not The Request** says.
   A skipped or neutral job supplies no coverage: establish whether its native condition makes it
   inapplicable, or required validation is missing. Draft skips never supply test coverage. A job
   without a check run or status needs the same applicability decision, not an assumed pass.
   Before using a local receipt, compare its source head and resolved dependency, configuration,
   toolchain and runner inputs with the proposed execution; a branch label alone is insufficient.
   Reuse it only for unchanged inputs or evidenced equivalence, and revalidate the affected coverage
   on drift. That receipt may support an exclusion under **Classify every unsuccessful check**; it never omits the hosted inventory.
6. **Drive the complete inventory to terminal results.** Re-query the exact head on a bounded
   interval matched to job duration — roughly every 30 to 60 seconds — until every applicable,
   non-excluded logical job has terminal coverage. Apply **Classify every unsuccessful check** as unsuccessful attempts become
   terminal so an interrupted job can recover while other jobs run. A successful representative
   means a pending equivalent duplicate does not hold the gate. Local coverage, a green selected
   job or a branch-protection summary does not permit omitting another job. Classify failures under
   **Classify every unsuccessful check** and account for missing or skipped required validation before clearing the gate. A new
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
8. **Classify every unsuccessful check before repair.**
   - **Exclusions.** A caller-supplied exclusion, or a current-user waiver naming the test or check,
     is excluded. Preserve established baseline classifications; classify a newly encountered
     possible baseline under `pre-production`'s **Encountered Issues**, without reentering that
     skill's active run. A non-essential check failing only on findings `pre-production`'s
     essential-checks bullet leaves red is an exclusion too. Record an exclusion's evidence, remove
     it from required coverage, and do not repair, rerun, or wait for it. Apply **Validation
     Exclusions**' interrupted-check exclusion automatically: record a qualified check as skipped
     and do not rerun or wait for a green hosted result.
   - **An interrupted attempt.** For a canceled or otherwise interrupted attempt with no recorded
     validation failure and no exclusion, use an equivalent successful hosted attempt or follow a
     pending replacement through **Drive the complete inventory to terminal results**. If neither
     exists, obtain equivalent local validation when it can qualify for the exclusion, or retry the
     hosted check on the same head using
     `POST /repos/{owner}/{repo}/actions/jobs/{job_id}/rerun`. Verify the retried job's head and
     required context before using its result. Missing logs or an unknown cancellation cause cannot
     justify local substitution; recover hosted coverage in that case. A canceled attempt alone does
     not end the gate.
   - **Every other failure** is relevant. Read its annotations and complete log, fix the repository
     input responsible — code, test, configuration or workflow — and commit it.
     - **Every relevant failure on the head goes into one push**: read all of them before fixing
       any, reproduce each with the job's own command where it can run locally, and push only once
       each reproduced failure passes locally, so the next hosted run is the last.
     - Only a failure that cannot run locally — a hosted service or credentials this session itself
       found absent from where the repository configures them, never taken on a reviewer's,
       worker's or plan's word, or runner-specific behavior, never disk, memory or ports the session
       can free — is pushed without local proof. A relevant external-service failure is an
       encountered issue under `pre-production` and is fixed the same way.
   - **Never** rerun a failing validation to get a green result, or skip, disable, or quarantine a
     test or confine its job to drafts to get past it. Report a blocker only when relevant missing
     coverage needs user input or unavailable credentials, with the check, evidence and remediation
     attempted.
9. **Leave services this workflow did not start alone.** Never stop, restart, reconfigure or claim a local service the calling workflow did not start:
   another agent or person may be using it. When relevant validation needs local services and one it
   did not start is running, use the matching hosted check as the fallback rather than running a
   competing service-managed test.
10. **Send every fix through the caller's rule.** Every fix made here goes through the caller's
   fix rule from **Inputs**, and the gate repeats on the head that review accepts.

## Merge Conflicts

When GitHub reports a conflict, or the merge is rejected for one:

- Incorporate the base through `merge-conflict`; the resolution is a fix under **Check Gate**'s **Send every fix through the caller's rule**.
- A resolution `merge-conflict` cannot make safely is reported as the blocker it describes.

## Merge

Recheck delivery dependency state, resolved revisions and the recorded default-branch comparison,
then re-read the pull request after the check gate and require its head to equal the head that passed
acceptance. On a head mismatch, put the added commits through the caller's rule and repeat the check
gate. On a base mismatch, apply the execution-input comparison of **For a runtime diff, inventory every check** and, when equivalence is not
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
in the inventory. For that context, **Classify every unsuccessful check** cannot apply local substitution or reuse a result the
provider already rejected. Follow its matching replacement or retry under **Check Gate**. Re-read
the required context and attempt the merge once GitHub reports it passing. For other exclusions, or if hosted
recovery is unavailable, report the actual rejection and its provider evidence. Never bypass protection.

Once the merge is verified, run **CI Commits To The Target Branch**. For agent configuration, complete
**After Agent Sync** alongside it, reusing its Agent Sync result. Refresh the checkout once after
those steps settle. **No Verification Or Deploy Work** governs release and deployment checks.

## CI Commits To The Target Branch

A checkout refresh includes commits that CI writes to the target branch because of the merge.
Read the merged repository's workflow triggers, branch and path filters, and the relevant job
conditions and scripts. Identify automatic jobs that can push generated files to the target branch,
including jobs reached through another workflow. Match direct push runs by merge SHA and ref.
For a downstream run, follow the triggering upstream run and event on that branch. Verify the
downstream checkout contains the merged source if it uses the moving branch tip. A job that only
uploads artifacts, creates a release, or deploys stays outside this step.

Use **Check Gate**'s bounded polling until the branch-writing step has a verified terminal result.
Use the job's terminal result when the step cannot be tracked separately. When a downstream
trigger or required installation depends on the workflow conclusion, also verify that conclusion
on the same run. Use the same polling for run discovery while an eligible writer is being scheduled, including
downstream runs after their prerequisites finish. Follow prerequisites only to establish whether the
writer can run. If a later run cancels or replaces it, follow that writer only after verifying that it covers the merged source and the same
outputs on the same branch. Distinguish a job skipped by its selection filters from a selected writer blocked by a failed
or canceled prerequisite. If a selected write remains unresolved because of a failure, missing run,
or uncertain coverage, fetch and refresh all available commits and report the job and cause.

Read the writer's final pushed revision from its result or logs, accounting for any rebase before
the push, and fetch the target branch. Verify the
branch tip contains the merge and its generated commits. A successful writer may emit a no-changes
result during execution. Use the emitted result to settle the writer without requiring a new commit.
A preview of the script containing the no-changes message supplies no evidence.
For multiple writers, use the fetched tip after all applicable writes settle. Pass that tip and
the job results to **Refresh The Primary Checkout**.

## Refresh The Primary Checkout

Follow the [checkout preservation and fast-forward procedure](references/checkout-refresh.md) for
the merged target branch after the applicable writers and any Agent Sync installation settle.
When the caller owns refresh, return the verified tip, writer results, and any installation result
for the caller to apply the same procedure before reporting completion.

## After Agent Sync

When the merged diff changes agent configuration, reuse the terminal Agent Sync workflow result
from **CI Commits To The Target Branch**, including a replacement with verified coverage when
applicable. Require workflow success before installation. Diagnose any unresolved synchronization
failure from the relevant log.

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
Finish with **Refresh The Primary Checkout**, which includes all installed guidance and any
generated commits pushed by downstream workflows.

## No Verification Or Deploy Work

**A merge leaves no verification or deploy work.** Whatever a change needs verified — tests, a
playtest, a walkthrough, an audit, a fresh-eye review — runs before its merge. Once the merge is
verified, nothing runs again to check it: no check by any route of whether the change is live (a
provider's deployment status, a release run, the site itself), no following of release, publication,
artifact upload or deployment outcomes, no inspecting or following of
merge-triggered release, publication, artifact or deployment workflows, no test, walk or audit of
what the merge deployed or of the merged default branch, and no scheduled re-check, wait for a
deploy, or assumption that one is coming. **CI Commits To The Target Branch** covers only Git writes needed for the checkout refresh,
even when the same workflow also publishes or deploys.

A verification step still open at the merge closes with it, and nothing waits on such a run or on a
deploy: no plan step, ledger or guidance hold, worker brief or report's next action. Other
authorized work after a merge is unaffected, such as a run's next batch, a consumer repointed once
its dependency merged, or the refresh **CI Commits To The Target Branch** and **After Agent Sync**
require. A task whose own outcome the
user stated as a deployment, publication or release, or as restoring a broken deployed operation,
follows that outcome past the merge, and a workflow the user invokes to merge before its review
keeps that review.

## Pull Request Activity

**Never poll a pull request with background `sleep` or timed self check-ins; act only on delivered
pull-request activity webhooks.** The exception is an invoked skill that states it polls, such as
**Check Gate**, which waits for every check on a head to reach a terminal state, and then only
while its run is active and for the pull request that run is driving. There a webhook alone can
wait forever: pushing a new commit cancels the in-flight run under a `cancel-in-progress`
concurrency group, so the superseded head reaches no terminal state and emits no completion event.

## Report

```markdown
Merged: [<owner>/<repo>#<number>](<url>) at <short sha> — checks: <local only | names of hosted checks and results> — consumers: <none pinned | repointed: <consumer PR> at <short sha> | owned elsewhere: <consumer PR> pins <reference>> — sync: <run result | not agent configuration>; refresh: <verified checkout tip and CI writer results, plus installed guidance source when applicable | blocked: exact reason>
```

The checks field leaves out baseline failures and non-essential checks left red, as
`pre-production`'s **Encountered Issues** says.

Or, when a gate holds: `Not merged: <link> — <gate>: <evidence>`. The evidence includes each
relevant check's terminal result, read from its log where its status was stale.
