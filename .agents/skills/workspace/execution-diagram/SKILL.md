---
name: execution-diagram
description: "Show the current skill execution flow or where subagents spawn, from current canonical guidance. Require explicit diagram direction, distinguish invocation from spawning and borrowed rubrics, and delegate rendering to use-diagram. Read-only mapping never executes the depicted workflows."
short_description: 'Map current skill execution and optional subagent launch points.'
---

# Execution Diagram

## Dependencies

- `use-diagram` — render the source-derived map with an explicit direction.

## Workflow

1. Resolve scope and explicit direction from the request or caller; ask for direction when absent.
   A named skill focuses the map. Otherwise start with execute-task, review-proposal, pre-production,
   session-ledger, review-pass, code-simplify, code-review, acceptance-gate, edit-skill guidance
   delivery, process-ledger, finish-pr, merge-now and merge-gate. These are source subjects, not
   workflows to invoke.
2. Locate current canonical sources through the repository or installed canonical links; do not
   assume the working directory contains the shared collection. Record paths, revision/content
   identities and dirty-source status. Read the selected entry points and follow reachable
   invocation, spawning and rubric references as needed for the requested graph. Include conditional
   security-audit and test-skill sources when reached. For a spawning view, also read subagent-matrix
   and its model-capabilities reference as source evidence, without dispatching workers.
3. Map actual order, choices, parallel streams, repair/invalidation loops and ownership. Use
   distinct edges for execution, dependency/borrowed criteria and delegation. A skill invocation or
   rubric reference is not itself an extra agent. Keep proposed changes separate from current flow.
   When revising a supplied graph, preserve its topology unless a requested semantic change or
   verified source change requires a labelled revision.
4. For a requested spawning view, show each direct launch owner, role/tier, mandatory or conditional
   trigger, per-round count, nesting and recurrence. Label counts as conditional structural counts,
   not measured time or cost. A plain map does not trigger an optimization audit or require an
   alternative for every node. Include recommendations only when requested and supported by evidence.
5. Recheck source identities before output. Remap changed inputs; never present a mixed snapshot as
   current. Missing/conflicting sources or repeated drift produce an explicitly incomplete map with
   the known snapshot and unresolved condition. Pass the verified map and explicit direction to
   use-diagram. No subagents are needed by default.

## Output

Return the Mermaid diagram and necessary legend through use-diagram, then a compact source-snapshot
note with any incomplete edges. A spawning view includes the conditional counts; detailed source
evidence and requested optimization comparisons follow the current file-delivery rules.
