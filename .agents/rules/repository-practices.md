---
description: Read when naming shared source, writing documentation or code comments, choosing dependency references, or replacing an existing contract.
alwaysApply: false
---

# Repository Practices Rules

## Source References

- Reference external code and automation by a maintained version tag when available, or by a
  maintained branch while developing or when no release tag exists. Do not pin dependency manifests,
  shared checkouts, or workflow references to commit hashes. Lockfiles and release records may retain
  the exact resolved commit for reproducibility and provenance.

## Repository Independence

- Every repository stands on its own. Never carry another repository's domain vocabulary into this
  one: its product name, its services, its table and column names, its record types, or the nouns
  its business speaks in. That holds for source, tests, fixtures, examples, and documentation
  alike, and it holds most strongly in a library, where every reader is a different consumer.
- Name things for the shape being exercised, not for whichever caller happened to prompt the work.
  A test needing a table with a secret column names it for that — a record with a secret — rather
  than borrowing the one real table the change was made for.
- Sample values follow the same rule: prefer plainly synthetic literals over ones shaped like a
  real identifier from another system's domain.

## Documentation

- Document current behavior only. Never describe what a symbol used to do, what was removed,
  renamed, or deprecated, and never write migration tables or upgrade notes.
- Git history is the record of what changed; documentation describes what exists now.
- The same applies to code comments and docstrings: no "formerly", "replaces", or "kept for
  backwards compatibility" notes.
- Use an environment's exact domain name for both it and its tailnet; never append owner or
  organization aliases. Name provider accounts and projects only as separate resources.

## Replacement Contracts

- When a request replaces a route, API contract, or behavior, remove the prior alias or fallback. Retain legacy compatibility only when the user explicitly authorizes it in the current request; if retention is unclear, ask before adding it.
