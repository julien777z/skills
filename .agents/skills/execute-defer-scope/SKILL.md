---
name: execute-defer-scope
description: Evaluate and resolve recorded deferrals from Linear and the legacy repository ledger, using the current session or an explicit issue, key, path, pull request, or aggregate scope. Invoke as /execute-defer-scope to execute, resolve, reconsider, or act on recorded deferrals.
disable-model-invocation: true
---

# Execute Defer Scope

Resolve recorded deferrals instead of treating their proposed work as automatically owed.

## Dependencies

- `defer-scope` — supply the record and ownership contract.
- `linear` — find and update Linear-owned records.
- `pre-production` — decide which problems and target contracts belong in the release.
- `code-simplify` — find the smallest coherent resolution for each legitimate problem.
- `acceptance-gate` — judge the proposed resolution and the finished diff against the originating
  change.

## Select The Records

With no explicit scope, build the session ledger from conversation and tool history, compacted
summaries, exact issue identifiers, repository paths, and pull-request associations. Query Linear
issues carrying the deferral label the repository's project guidance names using the repository and origin or resolution PR metadata
written by `defer-scope`. Include legacy records and record pull requests created in the session.
Never infer an issue, stable key, path, or pull-request number.

An explicit scope replaces that default:

- A Linear issue identifier or URL, stable key, or repository path selects its exact confident
  match. A pull request selects every record whose exact origin or resolution metadata names it;
  ambiguous fuzzy references select nothing until the user resolves them.
- `all` selects every active Linear deferral issue for the repository plus active legacy records
  on the fetched remote default branch and open record pull requests.
- `all including declined` also selects canceled or archived Linear issues and records under
  `deferrals/declined/`.
- An exact canceled issue or declined legacy path selects it without the broader phrase.

Fetch the remote default branch and current pull-request state before inventorying. Include
completed, canceled, and archived Linear results during deduplication even when they are not part of
the selected active scope. Deduplicate only on strong repository, stable-key, pull-request, affected
surface, and problem evidence. If the selection is empty, report it and mutate nothing.

If Linear preflight is unavailable, continue any selected legacy records, report that Linear records
could not be inventoried, and do not claim an aggregate or session scope is complete.

## Assess Every Record

Read the complete Linear issue with comments or the complete legacy record with supporting files and
record pull request. Read the current implementation and history of the code it names. Confirm that
the problem still exists before considering its proposed solution.

Put each record whose problem still exists to `acceptance-gate`'s triage question and carry its
disposition: fix and do become **Implement** or **Simplify and incorporate**, defer keeps the record
active or marks it **Blocked**, and close becomes **Decline**. **Already resolved** and **Void** come
from the tree read before the gate. The dispositions:

- **Implement** — correct a real release problem with the clean target implementation.
- **Simplify and incorporate** — solve it through a smaller correction, reuse, deletion,
  consolidation, or better owner.
- **Already resolved** — retire a stale record after proving the default branch no longer has it.
- **Decline** — retain the evidence while rejecting obsolete, speculative, or harmful work.
- **Void** — remove a record that never described work: a mistake, a duplicate, or a finding that
  proved wrong.
- **Blocked** — keep it active only for a genuine external dependency or unresolved user decision.

A record is evidence, not an implementation instruction. Consolidate duplicate records under the
one resolution that addresses their shared cause.

**Its resolution criteria describe the end state, never a licence to reach it.** They were written
when the problem was found, by someone who had not yet written the fix, so they bind what the
codebase must end up like and nothing about what may be written to get there. Every rule the
repository states holds inside a resolution exactly as it holds anywhere else, and so does the
intent of the change the record came out of.

Read that originating change before writing the fix — the record names it — and treat what it
removed as removed. A resolution that satisfies the sentence by encoding what that change deleted
has closed the record and reopened the thing the change was for: a hand-maintained name list put
back to make a set derivable, a model relocated across a service boundary to escape an import
cycle, a flag reintroduced to carry a distinction the change had moved onto a declaration. Each of
those reads as progress because a criterion now passes, and each leaves the codebase worse than the
open record did.

**When the criteria cannot be met without reintroducing it, that is a finding about the criteria.**
Solve the part that can be solved cleanly and re-scope the record to name the rest, or assign
**Blocked** with the conflict stated. Never move a record to a completed state on a change that puts
back what its originating change deleted — an open record costs a line in a ledger, and closing it
that way costs the regression plus the fact that nothing is now tracking it.

## Gate Every Resolution

The agent writing a resolution has already decided the work is owed, which is the worst position
from which to judge whether its fix reintroduces what the originating change removed.
`acceptance-gate` answers that twice, and both answers come before any record leaves an active state.

Put the proposed implementation to the **proposal** question before writing it, with the record, the
originating change's diff, and the plan. Put the finished diff to the **diff** question, with the
same record and change, through a different gate. Each item gets the one rewrite `acceptance-gate`
allows; a second flag has these dispositions here:

- a flagged proposal is re-scoped to the part that can be solved cleanly, with the record re-stated
  for the rest, or the record is marked **Blocked** with the conflict;
- a flagged diff is reverted: revert the resolution commits, leave the record active with the flag
  written on it, and report the conflict as the outcome. Satisfying the criteria by encoding slop is
  the exact failure the gate exists to catch, so a flagged change is never kept on that ground.

**What merges is what the gates govern.** A resolution that reaches the default branch carrying the
shape its originating change deleted has undone that change, and the record it closed is no longer
tracking the problem, so nothing will find it again. A resolution already merged that a later
reading shows to be slop is refactored to the intent rather than left standing.

## Resolve Linear Records

For implement and simplify dispositions, add factual progress before editing and update the issue to
a started-category state when available. Work from a fresh remote-default branch in an isolated
worktree when another change is in flight. Prefer one coherent resolution pull request; split only
across independent deployment, migration, rollout, or validation boundaries.

Apply dispositions as follows:

- **Implement** or **Simplify and incorporate** — make the complete correction and update every
  affected test, contract, migration, generated artifact, and consumer.
- **Already resolved** — add the evidence and move the issue to a completed-category state.
- **Decline** — add the reason and the concrete fact that would justify reconsideration, then move
  the issue to a canceled-category state. The work is real and someone may pick it up, so the
  record stays.
- **Void** — the record describes nothing to do: opened by mistake, a duplicate, a finding that
  proved wrong, or work a landed change already made irrelevant. Delete it rather than cancelling
  it, following the cancel-or-delete rule in `linear`, which also covers what to do when the
  integration exposes no delete operation.
- **Blocked** — record the blocker and required decision or external change; keep the issue active.

As soon as a validated resolution pull request is ready **and `acceptance-gate` accepted both the
proposal and the diff**, update every
included Linear issue's `Resolution PR` metadata and move implemented or simplified issues to a
completed-category state. A flagged resolution moves nothing: the issue stays active.
The user's completion condition is a ready validated pull request, not its merge. Do not merge the
resolution pull request without separate authorization.

When inventorying, reconcile completed issues whose resolution pull request later closed without
merging. Record that evidence and return them to the appropriate active state so ordinary `all`
selection cannot hide work that never reached the default branch.

## Resolve Legacy Records

Do not migrate existing repository records to Linear in this run. Preserve their current lifecycle:

- implemented, simplified, and already-resolved records are removed in the resolution pull request;
- declined records and evidence move under `deferrals/declined/<key>/` with the reason and
  reconsideration criterion;
- blocked records and their record pull requests remain unchanged.

Once the validated
resolution pull request is ready, comment on and close each superseded open record pull request with
the replacement and disposition. Close only records included in that replacement.

## Validate And Report

Run `code-simplify` across the implementation, complete changed files, analogous code, and sibling
modules. Run the repository's required validation for every behavioral change and every specialized
migration or contract check. A legacy disposition-only documentation diff gets artifact validation
and `git diff --check`, not application tests.

Report every selected record, source, disposition, both gate outcomes, Linear state change,
replacement pull request, closed legacy record pull request, and active blocker. A gate objection
or flag is reported with what it named, whether or not the resolution went on to land. If Linear becomes unavailable after a record
was found or updated, keep its identifier and report the blocked update rather than dual-writing a
repository record.
