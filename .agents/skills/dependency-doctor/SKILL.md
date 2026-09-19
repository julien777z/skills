---
name: dependency-doctor
description: Reconcile declared dependencies with what the code imports and the checks invoke, for every language the repository builds. It finds unused declarations, undeclared imports, conflicting constraints across manifests, lockfile drift, and audit tooling declared but never run. Invoke as /dependency-doctor to audit dependencies, package manifests, lockfiles, version constraints, or unused packages.
disable-model-invocation: true
---

# Dependency Doctor

A manifest declares what the code imports and the checks invoke, once, at one constraint, with a
lockfile that matches it. This doctor finds every place that stops being true.

## Dependencies

- `doctor-protocol` — own the run.
- `pre-production` — a constraint change that alters behavior is stated, never hidden.

Follow the repository's packaging rules for each language it builds; this doctor never restates
how a manifest or lockfile is edited.

## Inventory

Per language and per project: every manifest and its sections — runtime, development, optional
groups; every lockfile; tools a workflow installs outside a manifest; first-party imports across
source, tests, scripts, and workflow helpers; and every tool invocation in CI, scripts, and hooks.

## Lenses

### Declared But Unused

A package no first-party module imports and no check invokes, including a development tool
nothing runs. An audit tool declared and never wired into a check is the recurring case: it
reports nothing while looking like coverage.

### Used But Undeclared

An import satisfied only transitively, through a package that may drop it in its next release.

### Conflicting Constraints

One package pinned with different floors or ranges across manifests in the same repository, or a
shared package whose floor sits below a sibling's so the two resolve differently.

### Lockfile Drift

A lockfile older than its manifest, a lock entry the manifest no longer declares, or two lockfiles
resolving overlapping sets from manifests with different floors.

### Superseded

Two libraries declared for one job, or a package the platform, framework, or runtime already
provides.

## Dispositions

- Remove the unused declaration and its lock entries; wire an audit tool into an existing check or
  remove it.
- Declare an undeclared import in the manifest of the project that imports it.
- Align conflicting constraints to one range chosen from actual usage, stated where it changes
  behavior.
- Regenerate a lockfile only through the package manager's own command; never hand-edit one.
- Collapse two libraries doing one job to the one the rest of the repository uses.

The cross-cutting reviewer compares manifests with each other: the same package pinned differently
across projects or languages, and a check one project runs that its sibling does not. The final
adversarial reviewer re-traces every retained package to an importer or an invocation and confirms
each regenerated lockfile still resolves the stated constraints.

## Report Additions

- per manifest: declarations removed, added, and re-ranged;
- lockfiles regenerated and the command that regenerated each;
- audit tools wired into a check or removed.
