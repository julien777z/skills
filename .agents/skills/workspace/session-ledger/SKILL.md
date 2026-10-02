---
name: session-ledger
description: Record and retrieve verified external artifacts created during the current task, including pull requests across repositories. Use as a dependency whenever a workflow creates, selects, or reports session-created external artifacts.
short_description: 'Keep verified task artifacts available across a long session.'
---

# Session Ledger

Keep one structured ledger in the active task's state so information created early in a long
session remains available after repository changes, delegation, or conversation compaction.

The task owner keeps the ledger under one `session_ledger` task-state key. A harness with native
task state reads and writes that key directly. Otherwise, the owner keeps the same structured value
in its active task context, includes it with each delegated assignment, and appends the worker's
returned records before the next action. A worker never replaces the owner's ledger.

## Records

- Record an external artifact only after its owner confirms it. Keep its canonical URL, artifact
  kind, repository URL when applicable, creation order, and verified identifiers needed to read it
  again, such as a pull request number, branch, head SHA, or deployment ID.
- Pull requests are recorded immediately after the hosting service returns their canonical URL and
  before reporting the creation or moving to another repository.
- When the task first selects, updates, reviews, or otherwise acts on a pre-existing artifact,
  record a verified `touched` observation with its canonical URL and provenance. That observation
  does not make the artifact session-created.
- Record later lifecycle facts, such as a verified merge, deployment, release, issue creation, or
  external configuration change, as observations attached to the original artifact. Do not replace
  its creation record.
- Use the active harness's task-scoped state store. Do not commit a ledger file, parse a transcript,
  or retain records after the task ends. Never record credentials, tokens, request bodies, or other
  secrets.
- When delegating, give the worker the current ledger entries relevant to its task and require it to
  return every newly verified artifact record. The parent appends those records to the task ledger.

## Retrieval

- Retrieve records by artifact kind, repository, branch, or canonical URL. Deduplicate canonical
  URLs while preserving their first-recorded order.
- A session-scoped pull-request lookup reads the recorded pull requests first, then verifies each
  current state with the hosting service. Exclude closed and merged pull requests unless the caller
  explicitly asks for them.
- A hand-off lookup includes open pull requests recorded as created or touched during the task.
- An explicit user-provided URL remains the target. Verify it directly and do not substitute a
  same-named branch or another ledger record.
- If an existing task has no ledger entry for an artifact created before this skill was available,
  reconstruct one record from verified task evidence, then use the ledger for every later lookup.

## Guardrails

- Never infer a record from a repository directory, local branch, remembered pull-request number,
  or search result alone.
- A missing record is not permission to broaden a query. Ask for the target when the current task
  and verified records leave multiple plausible artifacts.
