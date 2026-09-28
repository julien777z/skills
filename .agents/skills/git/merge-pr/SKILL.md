---
name: merge-pr
description: Take a reviewed pull request through its exact-head check gate, resolve merge conflicts, and squash-merge it at the gated head, verifying the merge. Use when merging a specific pull request is authorized — the user naming it, or a workflow reaching its merge step, such as a review workflow, a doctor's merged batch, or a guidance change's delivery.
---

# Merge Pull Request

Merge one pull request at the head its caller accepted, and only after every check that head needs
has reached a terminal result.

## Authorization

- This skill merges only a pull request whose merge its caller is authorized to perform: a user
  instruction naming the merge and the pull request, an invoked skill that states its invocation
  authorizes the merge, or a rule that authorizes that merge. It creates no authorization of its own.
- Once that authorization holds, never ask the user for permission to merge and never end by
  offering the merge as the remaining step. What stops a merge is a gate: a check that is not green,
  a head that no longer matches the accepted SHA, or a conflict still unresolved. Report that gate.
- Dispatching a release workflow or creating a deployment is a separate action with its own
  authorization.

## Dependencies

- `merge-conflict` — resolve every base incorporation this skill performs.

## Inputs

The caller supplies the repository, the pull request, the head SHA its final acceptance passed, the
affected behaviors its local tests already cover, and the rule that decides what a fix made here
reopens in its own review. A caller with no such rule has each fix's diff judged the way it judged
the accepted head before the gate repeats.

## Transport

Use GitHub's REST API for every read, check query, ready-for-review transition and merge. Fall back
to GraphQL for the ready-for-review transition only after REST fails, reporting the failed response.
A rate limit is waited out through the host's wait mechanism and retried on the same transport.

## Check Gate

1. Make a draft pull request ready for review.
2. **Classify the complete pull-request diff.** A non-runtime diff — one that changes no executable
   source, package or dependency definition, test, runtime configuration, CI workflow, generated
   runtime artifact, or other executed-behavior contract — is validated only by the checks its
   artifacts need, its exact contents, and `git diff --check`; application tests, check runs and CI
   are not consulted. The classification is semantic rather than path-based: instructions,
   documentation, policies, static metadata and non-executable configuration live anywhere.
3. **For a runtime diff, gate only the coverage local tests could not establish.** For the affected
   behaviors the caller's local tests do not cover, query check runs and legacy statuses only for a
   job that supplies that missing coverage — unavailable credentials, provider-only or
   runner-specific behavior, or a dependency the local environment cannot host. When every affected
   behavior has passing local coverage, the gate is satisfied without querying GitHub. When a needed
   job has no check run or status, inspect the active workflow definitions for pull request
   triggers; if none can supply the coverage, report that blocker rather than waiting on unrelated
   checks.
4. **Poll a relevant check until it reaches a terminal state.** Re-query the exact head on a bounded
   interval matched to how long that job takes — roughly every 30 to 60 seconds — until it is
   `success`, `failure`, `cancelled`, `timed_out`, `skipped` or `neutral`. Never poll an unrelated job
   or wait on a whole workflow whose other jobs cover nothing affected. Do not end the turn, report
   "still running", or hand back to the user while a relevant check is pending; the poll loop is the
   work.
5. **A pending status is a cache, not evidence.** Status endpoints keep reporting `in_progress` after
   a job has finished, sometimes for an hour or more. Learn what the job normally costs from the same
   job on an earlier head or on the base branch; once a check is pending well past that, read the
   job's own output — the run's jobs listing and decisively its log, which a finished job ends with
   its summary and cleanup. A log showing completion **is** the terminal result. Never diagnose a
   hang, push a speculative fix, cancel, re-run, or report the run stuck from a pending status alone.
6. **A failed check is root-caused and fixed.** Read its annotations and complete log, fix the
   repository input responsible — code, test, configuration or workflow — and commit and push it.
   Never rerun a deterministic failure without addressing its cause. Retry a diagnosed transient
   external failure with no repository fix once the service can run it again; report a blocker only
   when the missing coverage needs user input, unavailable credentials, or an external recovery, with
   the check, evidence and remediation attempted.
7. Never stop, restart, reconfigure or claim a local service the calling workflow did not start:
   another agent or person may be using it. When relevant validation needs local services and one it
   did not start is running, use the matching hosted check as the fallback rather than running a
   competing service-managed test.
8. Every fix made here goes through the caller's rule from **Inputs**, and the gate repeats on the
   new head.

## Merge Conflicts

When GitHub reports a conflict, or the merge is rejected for one:

- Incorporate the base through `merge-conflict`; the resolution is a fix under **Check Gate** step 8.
- Report a blocker only when a safe resolution needs a product or contract decision nobody has
  authorized.

## Merge

Re-read the pull request immediately before merging and require its head SHA to equal the head that
passed acceptance and the check gate. Squash-merge with that SHA in the request —
`PUT /repos/{owner}/{repo}/pulls/{number}/merge` with `merge_method=squash` and `sha` — so GitHub
refuses a concurrent head change. On a mismatch, put the commits the new head adds through the
caller's rule from **Inputs**, then repeat the check gate. After the merge, re-read the pull request
and require it to report merged.

When the merged diff changes agent configuration, poll the default-branch Agent Sync run the merge
started as **Check Gate** steps 4–5 poll a check, then run the refresh the GitHub rules' **After
Agent Sync** section describes. A run ending in anything but success is diagnosed from its log and
reported, and the refresh still runs.

## Report

```markdown
Merged: [<owner>/<repo>#<number>](<url>) at <short sha> — checks: <local only | names of hosted checks and results> — sync: <run result | not agent configuration>; refresh: <done at <sha> | skipped: <dirty paths> | not run>
```

Or, when a gate holds: `Not merged: <link> — <gate>: <evidence>`. The evidence includes each
relevant check's terminal result, read from its log where its status was stale.
