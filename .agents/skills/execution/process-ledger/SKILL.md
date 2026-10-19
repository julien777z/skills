---
name: process-ledger
description: Process a task's private ledger at task completion or when a user asks to process it. Reconcile verified records, route successful guidance corrections into permanent guidance, and retain only entries with a concrete unresolved next action.
short_description: 'Process verified private-ledger records into durable outcomes.'
---

# Process Ledger

Process the active task's private ledger as one completion workflow. Read and update the ledger only
through `session-ledger`; it stays private task state, while permanent guidance and artifacts remain
at their owners.

## Dependencies

- `session-ledger` — resolve, validate, update, and preserve the private task ledger.
- `edit-skill` — deliver verified `guidance_correction` records into canonical guidance.

## Workflow

1. Resolve and read the active task's ledger through `session-ledger`. Honor `execute-task`'s
   **Priority** before starting permanent guidance delivery; retain its saved next action while
   recovery holds that work. Verify each entry's evidence
   before acting; a missing, invalid, or incomplete ledger is a recovery condition, not an empty
   result.
2. Classify each entry by `kind`, then follow its owning workflow.
   - `guidance_correction`: process it only when its recorded current-work action succeeded and
     evidence proves the requested result. Send it to `edit-skill`'s **Guidance Delivery** route
     so canonical guidance completes its delivery gates.
   - `artifact`, `plan`, `question`, and `decision`: reconcile the state with the artifact owner,
     plan workflow, or user answer. They never create guidance merely because they were processed.
   - `review`: `review-pass`'s reviewed head for a pull request. Keep it while that pull request is
     open, since the next pass sizes itself from it; remove it once the pull request is merged or
     closed.
   - An unrecognized kind: preserve it only when evidence identifies a concrete owning workflow or
     next action; otherwise remove it as invalid.
3. A failed, blocked, unavailable, or unverified requested action is not a `guidance_correction`
   to process. Keep its evidence in the task's verification record, continue recovery or escalate
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

Return a compact list of removed entries with their verified dispositions and retained entries with
their concrete hold and next action. Do not include private ledger contents in pull-request comments
or other public output.

## Guardrails

- Process every entry through its owning workflow; a ledger is an index of evidence, not authority
  to invent a new delivery or modify a different record kind.
- Never turn a failed attempt, proposed workaround, or unavailable environment into permanent
  guidance.
- Never retain a terminal or invalid entry. Never remove an entry whose validity remains plausible
  but cannot be resolved because of a concrete environment or evidence limitation.
