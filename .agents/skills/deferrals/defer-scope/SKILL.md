---
name: defer-scope
description: Record deferred work in the repository it affects, using Linear or that repository's ledger as an availability fallback; with no scope, read its active records. Use when work is consciously left undone, or when asked what is deferred, outstanding, or still open.
---

# Defer Scope

Keep a problem alive after the conversation ends without scheduling its implementation.

## Dependencies

- `linear` — find, create, and update the primary durable issue.
- `acceptance-gate` — admit a record before anything is written.

## Modes

**Record** when a scope is given. Create or reuse its Linear issue through **Recording**. Use
**Repository fallback** only when the session exposes no Linear integration or preflight reports it unavailable
before any write.

**Read** when no scope is given. Report the combined active set from Linear and the legacy
repository ledger, and write nothing.

Use `execute-defer-scope` when the user wants a recorded item assessed and resolved. Use
`defer-execution` only for an unrecorded scope already committed to separate execution.

## When Recording Runs

Fix work instead whenever one focused pass can finish it. A stale reference, rename, wrong path,
missing assertion, lint or type finding, or small extraction costs less to fix than to record.
Attempt the fix before concluding that work is deferrable; `acceptance-gate`'s admission question
lists the only justifications for a record, and a flagged attempt is one of them.

Nothing is written before `acceptance-gate` admits the record, and a refusal is carried out as its
disposition says: fix and do send the work into the change in flight, and close is recorded as a
cancelled issue with its reason and reconsideration criterion so the next run does not present the
finding again. Report the refusal either way. An explicit user invocation with a scope
settles justification, not the confirmed-defect refusal; the gate still confirms the problem is real
and the criteria describe an end state.

Before recording a changed workflow, path, or integration as an external blocker, fetch the current
default branch and inspect the recent commits and pull requests that changed that surface. Treat a
recent intentional replacement as current behavior: follow its replacement mechanism or report the
authorization boundary, rather than deferring the fact that the old mechanism disappeared. A
deferral requires genuinely unfinished work after this reconciliation, not merely a changed design.
An external blocker is something outside the repository the fix cannot be written without — a
credential nobody has issued, a vendor change, an answer only a third party can give. That the code
under change is deployed or running somewhere, a backfill in flight on live data included, is the
order the fix rolls out in, stated in the pull request; it is never a blocker on writing it.

Record work that is genuinely larger than the change in flight and whose need is arguable — a
redesign, a broad sweep somebody could reasonably decline — or that is blocked externally, or that
awaits a decision already put to its owner and still open, or one the user declined in the current
request; a question nobody has asked yet is asked, not recorded. **A confirmed defect is never
recorded** — and a defect is anything the system does that a reader would call broken, work it
cannot finish in useful time, a resource nothing bounds and work a restart throws away included, as
`acceptance-gate`'s admission question states. Whatever its size, however its fix has to be written,
and even when a check would rediscover it, it is fixed in the change in flight, or on a branch off
the default when nothing is in flight to carry it. Neither is the choice offered to the user: asking whether to record a
confirmed defect is how the refusal gets laundered into somebody else's decision, and their answer
settles nothing the gate would admit. When part is small, fix that part and record
only the remainder. Record at the moment work is consciously left undone; chat and pull-request
prose are not durable records.

## Ownership And Identity

Resolve the repository whose work is affected before searching or creating a record. If the work is
blocked by shared infrastructure with no repository of its own, use the repository containing the
blocked work. Write only when that repository is authorized; otherwise report the boundary without
writing elsewhere. Neither the current checkout nor the repository containing this skill establishes
ownership. Use the resolved repository for every Linear query and repository fallback operation.

Give the problem a stable key of a few words naming the problem rather than a proposed fix. Resolve
the canonical repository identity and the current change's pull-request number when one exists.

## Recording

1. Invoke `linear` and require the deferral label the repository's project guidance names to exist.
2. Search every matching active, completed, canceled, and archived issue using the label,
   repository, stable key, pull-request metadata, affected surface, and root cause. Also inspect the
   legacy repository ledger so a pre-transition record is not duplicated.
3. Put the scope, the search results, the draft resolution criteria, and any attempted fix to
   `acceptance-gate`'s admission question. A refusal ends recording. Reusing an active match is
   admitted the same way as creating one; appending to a record is still deferring.
4. Reuse and update a confident active Linear match. Do not reactivate a completed or canceled issue,
   duplicate a legacy record, or choose among ambiguous matches without user direction.
5. Create one issue when no match exists. State what is deferred, why it remains open, the scope of
   picking it up, supporting evidence by durable link or concise excerpt, and concrete resolution
   criteria. Use the metadata contract from `linear` with `Source: defer-scope` and the stable key. Write
   the resolution criteria as the end state the codebase reaches, and name the intent a fix has to
   preserve when the record comes out of a change that is removing a shape. A criterion phrased as
   a mechanical condition — a symbol gone, a file absent — can be satisfied by putting that shape
   back somewhere else, and the record then closes on a regression. Write the admission verdict in
   the issue body below the description.
6. Return the issue identifier and URL, or the matching legacy record. Recording does not create a
   repository branch or pull request when Linear succeeds.

If creation has an unknown outcome, follow `linear`'s bounded reconciliation search and do not retry
the create while ownership is uncertain. If a later Linear write fails after creation or reuse, do
not fall back or dual-write. Preserve the known issue identifier, retry when possible, and report the
blocked update.

## Repository Fallback

Use the pre-transition repository workflow only when Linear preflight is unavailable before any
write:

1. In the resolved affected repository, search `deferrals/<key>/`, `deferrals/declined/<key>/`, and
   open record pull-request diffs from its fetched remote default branch. Reuse an active match and
   never reactivate a declined one without explicit user direction.
2. After the same admission, write `deferrals/<key>/DEFERRAL.md` with the problem, why it remains
   open — the admission verdict goes here — pickup scope, and a table of supporting files. Copy only
   supporting material required to keep the record durable.
3. From a fresh branch off that repository's remote default, commit only that directory, push, and
   open one ready record pull request. Return to the interrupted branch.

Never mix Linear and repository records for one deferral. Existing repository records remain in
place until separately migrated or resolved through `execute-defer-scope`.

## Reading

Read active issues carrying the deferral label the repository's project guidance names through `linear`, then read every direct
`deferrals/` child on the fetched remote default branch and every open record pull request. Exclude
`deferrals/declined/` from the ordinary active view. Deduplicate only on strong repository, stable-key,
pull-request, and problem evidence.

Report one concise entry per deferral with its title, why it remains open, source (`Linear` or
`repository`), and durable link. If Linear is unavailable, report that limitation and return the
repository set rather than claiming the combined ledger is empty.
