---
name: propagate-skill
description: Reconcile skills across the user's repository collection. Move reusable guidance into the shared skills repository, preserve repository-specific guidance at its owner, remove generic copies from consumers, and connect editable user-level installations to the canonical checkout. Use when the user asks to propagate, consolidate, or synchronize skills.
---

# Propagate Skill Changes

Keep one canonical copy of each reusable skill. Repository-specific skills remain in the
repository whose commands and contracts they describe. A consumer repository never receives a
copy of a generic skill as part of this workflow.

## Dependency

- `coordinate-repositories` owns repository scope, isolated worktrees, existing pull requests,
  mutation safety, and independent verification.

## Listing

When invoked without a selected skill or change request, list the canonical skills at
`.agents/skills/**/SKILL.md` alphabetically by skill name, then stop. A listing does not discover
or modify repositories.

## Reconciliation

1. Inventory the bounded repository collection from `coordinate-repositories` and the editable
   user-level skill roots exposed by the host. Fetch each remote default branch. Read complete
   skill directories, supporting files, nearby project guidance, and the current canonical
   version; names and matching headings alone do not establish equivalent behavior.
2. Classify each skill by its actual contract. Generic language, platform, framework, authoring,
   review, and workflow guidance belongs in the skills repository. Product commands, deployment
   identities, fixtures, and policies whose correctness depends on one repository remain there.
   A skill that an action loads as part of its own runtime contract may also remain with that
   action, even when its name is generic; verify the code path that reads it before removal.
   Extract reusable principles when a local skill mixes both; move the specific facts to the
   owning repository's project guidance or local skill. Preserve unique content in user-level
   installations until it has been classified the same way.
3. Compare every variant sentence by sentence and include scripts, references, and assets. Keep
   the clearest complete reusable instruction, including useful consumer additions; do not use
   recency, size, or omission alone as a reason to discard guidance. Record the disposition of
   every removed or narrowed instruction. Ask about a genuine unresolved contract conflict as
   `coordinate-repositories` requires, rather than silently choosing one repository's behavior
   for all of them.
4. Finalize the canonical skill first. Keep its paths and examples repository-neutral, validate
   its full directory, and run the skill-edit smoke test when its behavior changes. Do not put
   provider metadata such as `agents/openai.yaml` into a skill directory or edit generated
   `.claude`, `.codex`, or `.cursor` mirrors.
5. Remove each reconciled generic directory from consumer repositories. Keep local skills and
   project guidance, and repair references that pointed at removed paths so they resolve through
   the user-level skill listing or a repository-specific role. Do not introduce a replacement
   generic copy, vendored snapshot, or automatic copy job.
6. For existing editable user-level installations, resolve the real path and ownership. Snapshot
   a conflicting real directory before changing it, reconcile any unique contents, then replace
   the generic copy with a link installed by `bootstrap/install.sh`. Preserve unrelated, managed,
   system, plugin, and read-only installations. The local refresh mechanism updates the canonical
   checkout, never a distributed copy.
7. Use existing relevant skills branches and open pull requests when verified; otherwise open
   focused branches and pull requests from fetched default branches. Validate each proposed head,
   independently audit every remote and local installation, and report a link for every pull
   request. Leave merging to the task's explicit delivery instructions.

## Guardrails

- A generic skill has one source in the skills repository, not one source per consumer.
- A repo-specific skill is never removed just because its name resembles a generic skill.
- Do not remove an action's runtime skill input and replace it with a network dependency merely to
  eliminate a duplicate name.
- Never overwrite dirty checkouts or user-owned skill content to make the inventory look clean.
- Do not propagate secrets, absolute machine paths, or repository-specific operational facts into
  shared skills.
