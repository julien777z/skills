---
name: defer-scope
description: Record deferred work in the repository it affects, using Linear or that repository's ledger as an availability fallback; with no scope, read its active records, or for a caller's scope read every record that covers it, declined and canceled ones included. Use when work is consciously left undone, when a change would take a recorded deferral out of the active set, or when asked what is deferred, outstanding, or still open.
short_description: 'Record unfinished work in the repository it affects, or read its active records.'
---

# Defer Scope

Keep a problem alive after the conversation ends without scheduling its implementation.

## Dependencies
- `linear`
- `acceptance-gate`
- `pre-production`
- `merge-gate`

## Modes

**Record** when a scope is given. Create or reuse its Linear issue through **Recording**. Use
**Repository fallback** only when the session exposes no Linear integration or preflight reports it unavailable
before any write.

**Read** when no scope is given. Report the combined active set from Linear and the
repository ledger, and write nothing. A recorded item is resolved by the user running
`/execute-defer-scope` on it.

**Read a scope** when a caller that is not recording asks which records cover a scope it is about
to audit or change. **Reading A Scope** returns them, declined and canceled ones included, and
writes nothing.

## When Recording Runs

Fix work instead of recording it whenever one focused pass can finish it within `pre-production`'s size budget, and a defect whatever its size, as below. A stale reference, rename, wrong path,
missing assertion, lint or type finding, or small extraction costs less to fix than to record.
Attempt the fix before concluding that work is deferrable; `acceptance-gate`'s admission question
lists the only justifications for a record, and a flagged attempt is one of them. Work in lines or
files the change in flight wrote, as its pull request's diff against the merge base shows, is that
change's own and is fixed there, never recorded; an admission that turns on where the work sits
carries the gate the file list and diff `acceptance-gate` requires for it.

Nothing is written before `acceptance-gate` admits the record, and a refusal is carried out as its
disposition says: fix and do send the work into the change in flight, and close is recorded as a
canceled issue with its reason and reconsideration criterion so the next run does not present the
finding again. Report the refusal either way. An explicit user invocation with a scope
settles justification, not the confirmed-defect refusal; the gate still confirms the problem is real
and the criteria describe an end state.

Before recording a changed workflow, path, or integration as an external blocker, fetch the current
default branch and inspect the recent commits and pull requests that changed that surface. Treat a
recent intentional replacement as current behavior: follow its replacement mechanism or report the
authorization boundary, rather than deferring the fact that the old mechanism disappeared. A
deferral requires genuinely unfinished work after this reconciliation, not merely a changed design.
What counts as an external blocker is `acceptance-gate`'s defer test, owned libraries included.

Record only work on a ground `acceptance-gate`'s defer test names, such as work comparable in
size to the change in flight, the two together too large for one careful read — a redesign or a
broad sweep somebody could reasonably decline, its need arguable, unless it is incidental cleanup —
work an external blocker holds, and
work that awaits a decision already put to its owner and still open, or one the user declined in
the current request; a question nobody has asked yet is asked, not recorded. **A defect is never
recorded**, a defect as `pre-production`'s **Scope
Follows The Defect, Not The Request** defines one, whether the change introduced it, the task asked
to fix it or the work only ran into it. Fix it now where `pre-production` places it, and investigate a
suspected one whose confirmation is in reach there, as that section says. Only cleanup that fixes
no defect follows `pre-production`'s size budget.
Never offer the user the choice between fixing and recording. When part of a cleanup is small, fix
that part and record only the remainder. Record consciously deferred work immediately, at the
moment it is left undone, in the repository that owns it as **Ownership And Identity** resolves; no
separate invitation is needed, and a chat note or pull-request prose is not a durable deferral
record.

## Changing A Record

A record whose problem still exists leaves the active set only on `acceptance-gate`'s triage
verdict, put with its evidence and who owns the work, so it is declined only on a close. A resolved record is retired only after tree evidence proves the default branch no longer has the
problem. A record that never described work is void only with evidence of the mistake, duplication,
or finding proved wrong. No record is declined, voided or
retired inline on the author's own reading; report the verdict or the evidence with the change.

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
   repository ledger so a record already kept there is not duplicated.
3. Put the scope, the search results, the draft resolution criteria, and any attempted fix to
   `acceptance-gate`'s admission question. A refusal ends recording. Reusing an active match is
   admitted the same way as creating one; appending to a record is still deferring.
4. Reuse and update a confident active Linear match. Do not reactivate a completed or canceled issue,
   duplicate a repository-ledger record, or choose among ambiguous matches without user direction.
5. Create one issue when no match exists. State what is deferred, why it remains open, the scope of
   picking it up, supporting evidence by durable link or concise excerpt, and concrete resolution
   criteria. Use the metadata contract from `linear` with `Source: defer-scope` and the stable key. Write
   the resolution criteria as the end state the codebase reaches, naming checks only of what the
   problem affects, each within the guidance that governs it, and name the intent a fix has to
   preserve when the record comes out of a change that is removing a shape. A criterion phrased as
   a mechanical condition — a symbol gone, a file absent — can be satisfied by putting that shape
   back somewhere else, and the record then closes on a regression. Write the admission verdict in
   the issue body below the description.
6. Return the issue identifier and URL, or the matching repository-ledger record. Recording does not create a
   repository branch or pull request when Linear succeeds.

If creation has an unknown outcome, follow `linear`'s bounded reconciliation search and do not retry
the create while ownership is uncertain. If a later Linear write fails after creation or reuse, do
not fall back or dual-write. Preserve the known issue identifier, retry when possible, and report the
blocked update.

## Repository Fallback

Use the repository ledger below only when Linear preflight is unavailable before any
write:

1. In the resolved affected repository, search `deferrals/<key>/`, `deferrals/declined/<key>/`, and
   the `deferrals/` diffs of its open pull requests, from its fetched remote default branch. Reuse an active match and
   never reactivate a declined one without explicit user direction.
2. After the same admission, write `deferrals/<key>/DEFERRAL.md` with the problem, why it remains
   open — the admission verdict goes here — pickup scope, and a table of supporting files. Copy only
   supporting material required to keep the record durable.
3. Commit only that directory on this session's source pull request in that repository, the one the
   GitHub rules' source-ownership bullet selects, and push it there; it merges with that pull
   request. Only when the session has no open source pull request there does the record go on a pull
   request holding only deferral records, the session's open one or a new draft from the default
   branch, which later records join. Once its records are pushed, put its complete diff to
   `acceptance-gate`'s final-acceptance question, one gate per such pull request, then invoke
   `merge-gate` under the GitHub rule's deferral-record permission with the accepted head, no local
   test coverage, and the rule that a fix it makes goes back to final acceptance over that fix's
   delta, one more gate per fix, within the limit of 3 review rounds per change. It is never left
   open, and no report or next action leaves its merge to the user.

Never mix Linear and repository records for one deferral. Existing repository records remain in
place until separately migrated or resolved.

## Reading

Read active issues carrying the deferral label the repository's project guidance names through `linear`, then read every direct
`deferrals/` child on the fetched remote default branch and every open pull request's `deferrals/` diff. Exclude
`deferrals/declined/` from the ordinary active view. Deduplicate only on strong repository, stable-key,
pull-request, and problem evidence.

Report one concise entry per deferral with its title, why it remains open, source (`Linear` or
`repository`), and durable link. If Linear is unavailable, report that limitation and return the
repository set rather than claiming the combined ledger is empty.

### Reading A Scope

For a scope a caller names — a repository, or a domain, service or path inside it — return every
record whose affected surface falls in that scope, whatever its state:

- from Linear, the issues carrying the deferral label in every state, completed, canceled and
  archived included;
- from the repository ledger, every `deferrals/` child, `deferrals/declined/` included, on the
  fetched remote default branch and in each open pull request's `deferrals/` diff.

Report one entry per record: its stable key, title, affected surface, state (active, declined,
canceled or resolved), source and durable link. A declined or canceled entry also carries the
reason it was declined and its reconsideration criterion, which is what would reopen it, both
quoted from the record; one that states neither is reported as missing them, never filled in.
The caller decides what a returned record means for its own findings; this read changes no record
and admits none.
