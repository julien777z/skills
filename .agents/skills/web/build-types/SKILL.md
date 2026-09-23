---
name: build-types
description: Regenerate generated API types from an OpenAPI document, using a local API checkout when it is present and the deployed API otherwise. Use when API request or response shapes change, when tsc reports a property missing on a generated schema, or when asked to refresh, rebuild, or sync the API types.
---

# Build Types

Treat generated API types as output of the canonical OpenAPI contract. Regenerate them instead of hand-editing a stale contract; inspect the project profile for the generated-file path and its consumers.

## Pick the source of the OpenAPI document

Read the repository operational profile for the local exporter, generated-file path, deployed contract URL, and runner commands. Prefer the local API checkout when changing its branch; use the deployed source only when no relevant checkout is available.

## After generating

Run the project's configured type check, formatter, and affected tests. Update every consumer to the generated API shape, including string-based field access that a type check can miss. Fix the upstream schema when the intended field is absent. Review the complete generated diff for unintended source or version drift.

## Guardrails

- Never hand-edit the generated contract. A hand-written entry that happens to
  typecheck hides drift instead of reporting it, which is the failure the
  generated file exists to prevent.
- Use the project's pinned generator version so a regeneration
  does not reformat the entire file alongside the contract change.
- Regenerate the whole file. Splicing in one schema leaves the rest describing
  an older contract.
- When a field is genuinely absent from both the backend and the deployed API,
  the fix belongs in the backend contract, not in this file.
