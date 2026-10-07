---
name: session-ledger
description: Persist and retrieve verified task context in one private file across chats, delegation, compaction, and handoffs. Use when a workflow creates, selects or reports task artifacts, records decisions, batches guidance corrections, or resumes task work. Resolve the task’s exact ledger locator before reading or writing; missing or unreadable storage is not an empty ledger.
short_description: 'Keep verified task artifacts in one private task file.'
---

# Session Ledger

Keep one structured ledger in a private task file outside repository checkouts. The file is the
source of truth; chat context and native task state carry its exact absolute locator and task
identity, never a second authoritative copy of its records.

## Storage

- Resolve the locator from the active task's metadata before every retrieval or update. For a new
  task with no prior ledger, choose a task-specific file in the harness's private task-state
  directory; when none is provided, use the user's private state directory. Record the absolute
  locator and stable task identity in task context before using it. Keep the directory private to
  its owner and the file owner-readable and writable only.
- An established task's missing locator, absent file, unreadable file, or invalid content is a
  recovery condition, not an empty ledger. Reconcile available canonical artifact receipts,
  continuation records and worker returns for that task. Recover or reconstruct the file from
  verified evidence, preserving provenance and existing records. If evidence remains unavailable,
  report the incomplete retrieval; never create an empty replacement or claim a complete result.
  Only a successfully read valid file with `entries: []`, or a genuinely new task's initialized
  file, establishes an empty ledger.
- Keep local evidence needed to resume work or reuse a verdict in private task storage with the
  ledger's restart and handoff durability. Before recording a local locator, retain and read back
  its required scenarios, frozen inputs, reports or logs there, recording their provenance and
  covered inputs or revision. Disposable working copies may remain temporary; a durable record must not
  depend on their survival. The task owner supplies workers distinct evidence destinations and
  verifies their returned artifacts before recording them.
- A readable ledger with missing referenced evidence is incomplete retrieval. Recover the artifact
  from its verified source or retained copy; if neither exists, preserve the prior observation as
  such, mark its proof unavailable and rerun only the verification that needs it. Reconstructing
  inputs does not reconstruct a past result. Never invent a replacement report or silently treat
  its absence as an empty or completed task.
- The task owner is the sole writer. Workers receive the locator and relevant entries and return
  new records and observations; they never write the owner's file or replace it with their
  snapshots. Serialize owner updates, reread the current file for each merge, and preserve all
  unrelated entries. Transfer writing ownership only after the previous writer has stopped and
  the receiving owner has read the current file. Overlapping owners must settle that transfer
  before either writes.
- Write the complete validated document to a private temporary file beside the ledger, then
  atomically replace the ledger and read it back before reporting persistence or continuing.
  Preserve the previous valid file when validation or writing fails; a failed write remains owed.

## Workflow

1. Resolve and read the task file under Storage before recording or retrieving context. Use the
   Output format for every entry, with record-specific facts in `data`; append new entries in
   first-recorded order. Persist each record or update through the owner’s atomic write procedure.
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
   - For a question, retain a stable decision ID, its actual wording and choices, recommendation or
     trade-off, whether it is optional, dependent work and the source that asked it. Record an agent
     assumption or action separately from the user's answer. Update its disposition only with the
     answer, withdrawal, governing evidence or later instruction that resolves or supersedes it;
     keep any unresolved part. Silence, optional status or elapsed time supplies no selection.
     Before returning pending decisions, reconcile the latest user message and retain all unresolved
     choices, including assumptions awaiting confirmation; exclude only evidenced resolutions.
   - For active work, record its owner, next action, dependencies and concrete blockers so a handoff
     can resume it without reconstructing the task. Preserve reusable check evidence with the input
     or head it covers, and invalidate only what a change affects. When tracking delay, distinguish
     a duration measured from observed start and end times from an estimate inferred from status;
     record the basis rather than turning an estimate into an elapsed-time claim.
3. Update an entry's current `data` and append observations for later lifecycle facts, checks and
   dispositions. Preserve its initial observation and provenance. Clear a correction's pending
   status only after verified delivery or a recorded disposition, never because work moved on.
4. Preserve the file locator, task identity and ownership across delegation, handoff and compaction.
   Merge worker receipts by stable entry ID, or canonical URL for an artifact, without replacing
   unrelated entries or reordering existing ones. Carry the locator in agent-consumed task metadata
   and continuation context so the next reader can resolve the existing file.
   - A receiver in the same environment must read and validate the existing file before taking over.
   - Across environments, transfer the file and its required local evidence through an authorized
     private artifact channel. The receiver saves them outside checkouts, validates their contents
     against the source, and records the new ledger and evidence locators. An old absolute path is
     not portable. Keep the source until receipt, content verification and ownership transfer
     succeed; report a genuine transfer blocker when no authorized private channel exists. Never
     publish ledger contents or private evidence in pull-request comments.
5. Retrieve by record kind or facts such as artifact kind, repository, branch or canonical URL.
   Deduplicate artifact URLs while preserving first-recorded order.
   - A task-scoped pull-request lookup reads the recorded pull requests first, then verifies
     their current state with the hosting service. Exclude closed and merged pull requests unless
     explicitly requested. A handoff includes open pull requests recorded as created or touched.
   - An explicit user-provided URL remains the target: verify it directly without substituting
     another ledger record or a same-named branch.
   - For an artifact created before this skill was available, reconstruct its missing entry from
     verified task evidence, then use the ledger for later lookups.

## Output

Store this YAML document in the private task file and return its records to the calling workflow,
not as a user-facing report. Task metadata carries only the locator and task identity.
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

- Do not commit a ledger file or its private evidence, or parse a transcript. Never record
  credentials, tokens, request bodies, other secrets, or unrelated session details. Remove task
  ledger files, retained evidence and transfer copies after the task ends and no receiver or active
  worker still needs them; a handoff continues the task and is not its end.
- Never infer a record from a repository directory, local branch, remembered pull-request number,
  or search result alone.
- A missing record is not permission to broaden a query. Ask for the target when the current task
  and verified records leave multiple plausible artifacts.
