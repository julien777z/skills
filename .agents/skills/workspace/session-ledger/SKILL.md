---
name: session-ledger
description: Record and retrieve task context and verified external artifacts during the current task. Use when a workflow creates, selects or reports task artifacts, records decisions, or batches observed guidance issues and reproduction scenarios for later verification.
short_description: 'Keep verified task artifacts available across a long session.'
---

# Session Ledger

Keep one structured ledger in the active task's state so context recorded early in a long session
remains available after repository changes, delegation, or conversation compaction.

The task owner keeps the ledger under one `session_ledger` task-state key. A harness with native
task state reads and writes that key directly. Otherwise, the owner keeps the same structured value
in its active task context, includes it with each delegated assignment, and appends the worker's
returned records before the next action. A worker never replaces the owner's ledger.

## Workflow

1. Read the current ledger before recording or retrieving context. Use the Output format for every
   entry, with record-specific facts in `data`; append new entries in first-recorded order.
2. Record the facts and their provenance as soon as they are known.
   - For an external artifact, require confirmation from its owner. Keep its canonical URL,
     artifact kind, repository URL when applicable, creation order, and verified identifiers needed
     to read it again, such as a pull request number, branch, head SHA, or deployment ID. Record a
     pull request immediately after the hosting service returns its canonical URL, before reporting
     creation or moving to another repository. The first observation records `created` or `touched`;
     acting on a pre-existing artifact never makes it session-created.
   - For a correction, keep the observed issue, evidence or user instruction, reproduction scenario,
     intended behavior, canonical files, local branch, checkpoint and delivery status. Keep other
     context needed to resume: decisions and constraints, affected callers, dependencies, check
     results and their validity conditions, open questions and next actions. Choose useful `data`
     fields for the record; local work is never an externally verified artifact claim.
   - For active work, record its owner, next action, dependencies and concrete blockers so a handoff
     can resume it without reconstructing the task. Preserve reusable check evidence with the input
     or head it covers, and invalidate only what a change affects. When tracking delay, distinguish
     a duration measured from observed start and end times from an estimate inferred from status;
     record the basis rather than turning an estimate into an elapsed-time claim.
3. Update an entry's current `data` and append observations for later lifecycle facts, checks and
   dispositions. Preserve its initial observation and provenance. Clear a correction's pending
   status only after verified delivery or a recorded disposition, never because work moved on.
4. Preserve the ledger across delegation, handoff and compaction. Give workers the relevant entries
   and require new records and observations back. The task owner merges them by stable entry ID,
   or canonical URL for an artifact, without replacing unrelated entries or reordering existing ones.
5. Retrieve by record kind or facts such as artifact kind, repository, branch or canonical URL.
   Deduplicate artifact URLs while preserving first-recorded order.
   - A session-scoped pull-request lookup reads the recorded pull requests first, then verifies
     their current state with the hosting service. Exclude closed and merged pull requests unless
     explicitly requested. A handoff includes open pull requests recorded as created or touched.
   - An explicit user-provided URL remains the target: verify it directly without substituting
     another ledger record or a same-named branch.
   - For an artifact created before this skill was available, reconstruct its missing entry from
     verified task evidence, then use the ledger for later lookups.

## Output

Store and return this YAML structure to the calling workflow, not as a user-facing report. The
native task-state value is the mapping beneath `session_ledger`, not another wrapper inside it.
Keep every entry's envelope fixed; `kind` distinguishes records such as `artifact`,
`guidance_correction` or `decision`, and both `data` mappings hold only the facts that record needs.
Keep `id` stable and unique within the task. Use `observations: []` when none have been recorded.

```yaml
session_ledger:
  entries:
    - id: "<stable task-local identifier>"
      kind: "<record kind>"
      summary: "<one-sentence description>"
      data: {}
      observations:
        - event: "<observed event>"
          evidence: "<source confirming it>"
          data: {}
```

An empty ledger is `session_ledger: {entries: []}`. Add record-specific fields within `data`, not
new top-level collections or an envelope per kind.

## Guardrails

- Do not commit a ledger file, parse a transcript, or retain records after the task ends. Never
  record credentials, tokens, request bodies, other secrets, or unrelated session details.
- Never infer a record from a repository directory, local branch, remembered pull-request number,
  or search result alone.
- A missing record is not permission to broaden a query. Ask for the target when the current task
  and verified records leave multiple plausible artifacts.
