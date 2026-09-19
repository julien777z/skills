---
name: refactor
description: Resolve and confirm a repository refactor scope, use multiple independent reviewers to plan structural improvements, then implement an approved plan. Invoke as /refactor to refactor a repository, change request, branch, path, symbol, or concern.
disable-model-invocation: true
---

# Refactor

Refactor an approved scope without assuming a repository layout, language, framework, hosting
provider, validation command, or branch convention.

## Dependencies

- `plan-change` — govern the separate plan approval and its complete implementation.
- `code-simplify` — supply the review rubric and implementation-time simplification pass.

## Resolve The Scope

Inspect the repository guidance and version-control state. Refresh the authoritative default line and
change-request metadata through the repository-native mechanism, then resolve scope in this order:

1. A whole-repository request or a change request, ref, path, directory, symbol, or concern supplied
   by the caller replaces automatic selection. Resolve a narrow selection to concrete files and
   ownership boundaries rather than treating the caller's wording as a filename pattern. Use the
   complete local state of that selection and its required consumers unless the caller selected a
   specific revision; preserve and list unrelated local changes without adding them to scope.
2. Otherwise, when an open pull request or equivalent change request owns the current checkout, use
   its actual base and the complete local change state. Include published revisions and tracked local
   edits. Include an untracked path only when it lies inside a selected changed ownership area or the
   caller named it. Give every untracked path an explicit included or excluded disposition in the
   scope proposal so the caller can correct it. Distinguish local additions from the change request's
   published head.
3. Without an open change request, when the checkout has revisions beyond the refreshed default line
   or local changes, use the repository-native common-ancestor diff plus tracked changes. Apply the
   same untracked-path rule as the preceding step.
4. When there is no open change request and no selected local change from the refreshed default line,
   use the whole executable repository at the refreshed default head, even when the clean checkout is
   behind it. Review and edit that exact snapshot through a synchronized or isolated checkout; never
   substitute an older clean checkout.

Use Git branches, remotes, merge bases, and worktrees only when the repository uses Git. For another
version-control or review system, use its equivalent default line, revisions, local-change view, and
change-request update mechanism. If no authoritative default or comparison source exists, state that
limit in the proposed scope instead of inventing one.

A change-request, branch, or explicit scope begins with the selected files and expands only to their
complete contents, sibling modules, analogous implementations, canonical owners, required consumers,
and affected tests. This context may change as part of a complete refactor, but it does not authorize
proactive cleanup of unrelated areas.

A whole-repository scope proactively covers every discovered first-party project: source, tests,
scripts, dependency definitions, executed automation, and runtime configuration. Discover and list
project and ownership roots from repository metadata, build and dependency definitions, local
guidance, generator declarations, and version-control boundaries. Exclude prose, agent configuration,
planning and audit records, vendored dependencies, generated output, lockfiles, and build artifacts
from proactive hunting. Read or regenerate an excluded consumer when an approved source change
requires it; never hand-edit output owned by a generator.

## Confirm The Scope

Before launching reviewers, writing an implementation plan, or changing files, present:

- the resolved scope mode and target;
- its base and head or equivalent revisions, or the concrete explicit selection;
- a short description of included ownership areas and exclusions, plus the individual disposition
  of every untracked path;
- that multiple read-only reviewers will identify structural simplifications before `plan-change`
  presents a separate implementation plan.

End the message exactly with:

`Reply approved to accept this scope, or describe the correction.`

Only an explicit `approved` accepting the currently presented scope counts. A correction, timeout,
missing response, mode change, or tool result is not approval. Resolve and present a corrected scope
again. Scope approval authorizes analysis only; it does not approve a plan or any mutation.

## Review And Plan

After scope approval, launch at least two independent read-only reviewers:

- one applies the complete `code-simplify` rubric to structural simplification;
- one searches for duplication, inconsistent ownership, canonical implementations, and
  cross-boundary consolidation.

For a larger scope, partition coherent ownership areas among additional reviewers and add one
cross-cutting reviewer. Discover those areas from the repository; never assume fixed top-level
directories or divide work by arbitrary file counts. Every reviewer reads the context needed to
compare its area with siblings and consumers, returns evidence-backed findings, and edits nothing.

The parent verifies each finding against the current tree, deduplicates overlapping remedies, and
rejects unsupported churn. If no validated refactor remains, report that result and stop without an
implementation plan. Otherwise invoke `plan-change` to present one decision-complete plan covering
the validated findings, affected consumers, validation, and publishing behavior. Scope approval does
not approve that plan; wait for its separate explicit approval.

## Implement

After plan approval, the parent is the sole editor. Implement the complete approved plan, update all
affected consumers together, and apply repository-local contract, migration, compatibility, and
encountered-issue policies discovered from applicable guidance. Do not preserve a partial migration
or add a compatibility layer merely to keep the refactor local.

The parent invokes and applies `code-simplify` after each meaningful implementation batch and once
over the complete result. Its scope starts from the approved refactor and expands only through files
required to complete and validate an accepted finding. A newly discovered architectural decision
that changes the approved scope returns to `plan-change`; it is not silently adopted.

## Verify

Discover and run every applicable repository-native check that covers the changed behavior and its
consumers, including configured formatting, static analysis, tests, builds, and generated-output
verification. Report an absent category as not configured; do not invent a replacement or substitute
a familiar command from another repository.

Then launch at least two independent read-only final reviewers. One checks completion against the
approved scope and plan. The other independently audits the parent's completed `code-simplify` pass
for missed cross-cutting simplification and ownership findings; it does not repeat implementation.
The parent validates their findings, fixes every confirmed in-scope issue, reruns affected
validation, and repeats the relevant review until no confirmed finding remains or a genuine user
decision or external blocker prevents completion.

## Publish And Report

When the scope came from an existing open change request, verify it is still open and update that
same change request through the repository's native revision or publishing mechanism. Never merge it
automatically or open a replacement silently.

When no open change request existed, create an isolated non-default line of development before
editing when the version-control system requires one, and leave the validated result local. Do not
publish it, open a change request, or merge without a separate delivery instruction.

Report the resolved scope, completed refactors, intentional behavior or contract changes, reviewer
coverage, validation results, publishing state, and every unresolved user decision or external
blocker.
