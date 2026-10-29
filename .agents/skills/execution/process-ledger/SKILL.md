---
name: process-ledger
description: Process a task's private ledger at task completion or when a user asks to process it. Reconcile verified records, route admitted guidance corrections, direct guidance requests included, into permanent guidance, and retain only entries with a concrete unresolved next action.
short_description: 'Process verified private-ledger records into durable outcomes.'
---

# Process Ledger

Process the active task's private ledger as one completion workflow. Read and update the ledger only
through `session-ledger`; it stays private task state, while permanent guidance and artifacts remain
at their owners.

## Dependencies

- `session-ledger` — resolve, validate, update, and preserve the private task ledger.
- `edit-skill` — deliver admitted `guidance_correction` records into canonical guidance.

## Batches

**One guidance batch is in flight at a time, frozen when its delivery starts.** A batch is in
flight from its freeze until it is done: every entry in it has a verified delivery or a recorded
hold. A held entry does not keep its batch in flight.

- **Freezing.** Mark with one batch id every `pending` `guidance_correction` entry that `edit-skill`'s
  **Recording During A Task** admits and that either carries no batch id or is held by a hold that
  has since resolved, which resumes at its recorded stage. That set is the batch. Record the run
  delivering it as its owner through `session-ledger`.
- **While a batch is in flight**, an entry recorded then, the user asking to change a file the batch
  is changing included, carries no batch id and waits for the next batch: the batch never takes it
  in, reopens an edit for it, or reruns a reviewer, gate or smoke round because of it. A repair the
  batch's own review, gate or smoke round requires is the batch's work under `acceptance-gate`'s
  **Bounds** and `test-skill`, never a new entry. Only the user's explicit instruction to add an
  entry to the batch in flight puts it there.
- **A run that finds a batch in flight** freezes nothing. It leaves the batch to its owner while the
  owner's record shows it delivering and the owner is live; otherwise it takes ownership under
  `session-ledger`'s transfer rule and resumes the batch at its recorded first nonterminal stage.
- **When a batch is done**, its owner freezes and delivers the next batch. When no entry qualifies,
  it returns, reporting each remaining hold; a waiting entry is never reported as a hold.

## Workflow

1. Resolve and read the active task's ledger through `session-ledger`. Honor `execute-task`'s
   **Priority** before starting permanent guidance delivery; retain its saved next action while
   recovery holds that work. Before freezing or prioritizing a batch, reconcile every recorded hold
   with its current owner and authoritative dependency evidence. Discharge a completed dependency,
   retain a genuine authorization or dependency hold with its saved next action, and resume any
   nonterminal delivery stage without repeating a verified receipt. Verify each entry's evidence
   before acting; a missing, invalid, or incomplete ledger is a recovery condition, not an empty
   result.
2. Classify each entry by `kind`, then follow its owning workflow.
   - `guidance_correction`: process it only when it belongs to the batch this run delivers under
     **Batches**. Send it to `edit-skill`'s **Guidance Delivery** route so canonical guidance
     completes its delivery gates.
   - `artifact`, `plan`, `question`, and `decision`: reconcile the state with the artifact owner,
     plan workflow, or user answer. They never create guidance merely because they were processed.
     A complete `plan` stays while its task is active, since `progress` counts the finished work of
     every plan the task has had; remove it once the task's outcome is verified complete.
   - `review`: `review-pass`'s reviewed head for a pull request. Keep it while that pull request is
     open, since the next pass sizes itself from it; remove it once the pull request is merged or
     closed.
   - An unrecognized kind: preserve it only when evidence identifies a concrete owning workflow or
     next action; otherwise remove it as invalid.
3. A failed, blocked, unavailable, or unverified requested action — which a direct guidance request
   never is, since its delivery is its action — is not a `guidance_correction` to process. Keep its evidence in the task's verification record, continue recovery or escalate
   the live task as needed, and do not create, amend, or deliver permanent guidance from it.
4. Judge terminality against each record's complete owning outcome, including its required delivery
   and verification. Remove it only when that outcome is verified complete or evidence proves the
   record invalid. Current-work success alone does not complete a pending guidance delivery; retain
   that entry with its concrete hold and next action until the required delivery is verified
   complete or withdrawn. Reporting a hold does not complete that delivery. Keep every other
   unresolved dependency, uncertainty or next action the same way.
   A ledger is fully processed only when it has no entries other than kept `review` records,
   which are pull-request state: report them as kept; they carry no hold.

## Output

Return a compact list of removed entries with their verified dispositions, retained entries with
their concrete hold and next action, and kept `review` records as kept. Do not include private
ledger contents in pull-request comments or other public output, other than the generic recovery
comment `edit-skill` keeps on a guidance pull request.

## Guardrails

- Process every entry through its owning workflow; a ledger is an index of evidence, not authority
  to invent a new delivery or modify a different record kind.
- Never turn a failed attempt, proposed workaround, or unavailable environment into permanent
  guidance.
- Never retain a terminal or invalid entry. Never remove an entry whose validity remains plausible
  but cannot be resolved because of a concrete environment or evidence limitation.
