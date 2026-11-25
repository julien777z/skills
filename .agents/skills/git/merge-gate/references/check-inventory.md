# Check inventory

The inventory, terminal-result and classification steps **Check Gate** runs for a runtime diff.

Contents: **For a runtime diff, inventory every check on the exact head**, **Drive the complete
inventory to terminal results**, **A pending status is a cache, not evidence**, **Classify every
unsuccessful check before repair**.

## For a runtime diff, inventory every check on the exact head

Read every page of check runs and legacy statuses, including every workflow job, rather than only
required checks or jobs selected by local coverage. Inspect the active workflow triggers and job
conditions to account for missing jobs. Passing local tests never replaces this inventory or a
hosted job's result. Record each logical job's representative run, head, state and conclusion, every
equivalent duplicate attempt, and each caller-supplied exclusion with its evidence. A completed
successful representative supplies coverage for an equivalent duplicate that remains pending; a
changed trigger, condition, execution input, or affected behavior does not. Every unsuccessful
terminal duplicate remains subject to **Classify every unsuccessful check**. Read each test job's
suite wall time against the budget `test-fixture`'s **Time Budgets** sets, and for a suite past it,
against the same job's latest run on the base branch. The merge is held only for slowness this pull
request caused, so a suite it made slower than that base run is an unsuccessful result for
**Classify every unsuccessful check** even when its job passed. A suite already past its budget that
this pull request did not slow does not hold the merge: it is a defect the work noticed, and its fix
is placed as `pre-production`'s **Scope Follows The Defect, Not The Request** says. A skipped or
neutral job supplies no coverage: establish whether its native condition makes it inapplicable, or
required validation is missing. Draft skips never supply test coverage. A job without a check run or
status needs the same applicability decision, not an assumed pass. Before using a local receipt,
compare its source head and resolved dependency, configuration, toolchain and runner inputs with the
proposed execution; a branch label alone is insufficient. Reuse it only for unchanged inputs or
evidenced equivalence, and revalidate the affected coverage on drift. That receipt may support an
exclusion under **Classify every unsuccessful check**; it never omits the hosted inventory.

## Drive the complete inventory to terminal results

Re-query the exact head on a bounded interval matched to job duration — roughly every 30 to 60
seconds — until every applicable, non-excluded logical job has terminal coverage. Apply **Classify
every unsuccessful check** as unsuccessful attempts become terminal so an interrupted job can
recover while other jobs run. A successful representative means a pending equivalent duplicate does
not hold the gate. Local coverage, a green selected job or a branch-protection summary does not
permit omitting another job. Classify failures under **Classify every unsuccessful check** and
account for missing or skipped required validation before clearing the gate. A new head rebuilds the
inventory. When the base moves, compare its changes with every execution input before reusing
evidence; retain a result only with evidence that those inputs are equivalent. Otherwise incorporate
the base through `merge-conflict`, run the caller's rule over the resolved head, and restart this
gate. Do not end the turn or hand back while the gate is pending; its poll loop is the work.

## A pending status is a cache, not evidence

Status endpoints keep reporting `in_progress` after a job has finished, sometimes for an hour or
more. Learn what the job normally costs from the same job on an earlier head or on the base branch;
once a check is pending well past that, read the job's own output — the run's jobs listing and
decisively its log, which a finished job ends with its summary and cleanup. A log showing completion
**is** the terminal result. Never diagnose a hang, push a speculative fix, cancel, re-run, or report
the run stuck from a pending status alone.

## Classify every unsuccessful check before repair

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
