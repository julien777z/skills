---
name: docs-doctor
description: Find and fix documentation that no longer matches the code. It covers paths, commands, symbols, variables, and flags that do not exist, behavior the code no longer has, history narration, repeated explanations, and README structure against the repository's README rules. Invoke as /docs-doctor to audit docs, READMEs, docstrings, or stale references.
disable-model-invocation: true
---

# Docs Doctor

Documentation describes what exists now. This doctor finds every sentence that describes something
else.

## Dependencies

- `doctor-protocol` — own the run.
- `pre-production` — documentation describes the clean target contract, never a transitional one.

Apply the repository's documentation and README rules; this doctor never restates them.

## Inventory

Every README and documentation tree; every docstring; and, for each, every path, command, symbol,
variable, flag, URL, and described behavior it names. Agent guidance files are `guidance-doctor`'s,
every lens included. Resolve each reference against the current tree, the commands the
manifests declare, the runner's targets, and the settings models.

## Lenses

### Unresolvable References

A path, command, symbol, variable, or flag named in prose that the tree, a manifest, or the runner
does not have.

### Retired Behavior

A described behavior the code no longer has, or a described default, order, or response the code
contradicts.

### History Narration

"Formerly", "used to", "replaces", migration tables, upgrade notes, and deprecation prose. Git
history is the record of what changed.

### Structure

README shape against the repository's README rules, and one explanation repeated across documents
where one home and a link would do.

Docstring style belongs to `code-simplify`; this doctor takes only a docstring that names a
nonexistent thing or a retired behavior.

## Dispositions

- Fix a reference to what exists.
- Delete a sentence describing what no longer exists rather than rewording it as history.
- Restructure a README to the rules rather than patching one heading.
- Collapse a repeated explanation to one home and a link.
- A documented command that ought to exist but does not is a finding about the manifest, presented
  as a user decision: declare the command or delete the sentence.

The cross-cutting reviewer compares documents with each other: one command, path, or behavior
described differently in two places. The final adversarial reviewer re-resolves every retained
reference against the current tree and confirms that a collapsed explanation lost no distinct fact.

## Report Additions

- per document: references checked, fixed, and deleted;
- structural changes made.
