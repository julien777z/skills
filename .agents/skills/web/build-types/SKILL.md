---
name: build-types
description: Regenerate generated API types from an OpenAPI document, using the API contract this branch deploys with. Use when API request or response shapes change, including on an API branch this branch deploys with, when tsc reports a property missing on a generated schema, or when asked to refresh, rebuild, or sync the API types.
short_description: 'Regenerate generated API types from an OpenAPI document, using the API contract this branch deploys with.'
---

# Build Types

Treat generated API types as output of the canonical OpenAPI contract. Regenerate them instead of hand-editing a stale contract; read the generated-file path and its consumers from the repository's project guidance, opening every `.agents/references/` file its `project.md` points to.

## Pick the source of the OpenAPI document

Read the repository's project guidance for the local exporter, generated-file path, deployed contract URL, and runner commands. The document comes from the API this branch deploys with: a checkout of the API branch whose change it consumes, exported locally, or the deployed API when this branch needs nothing that is not deployed yet.

## Keep the types on the pull request that consumes the change

**The pull request that consumes an API change carries its regenerated types**, whenever that change lands on the API branch: never a pull request branched off it, and never a follow-up once the API deploys. That pull request then deploys with or after the API change, and its description states the API contract it needs in its own repository's terms. Keeping it deployable on its own is never a reason to put the types anywhere else, and where they go is not a question for the user.

## After generating

Run the pre-push checks the GitHub rule’s **Pre-Push Gate** defines. Update every consumer to the generated API shape, including string-based field access that a type check can miss. Fix the upstream schema when the intended field is absent. Review the complete generated diff for unintended source or version drift.

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
