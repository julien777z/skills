---
name: config-doctor
description: Reconcile configuration names across every place they are declared, each deployment's own environment included, and remove settings nothing reads or nothing deployed sets. Declarations live in typed settings models, environment example files, test environment blocks, container, CI, and deployment manifests, hosting-platform application specifications, and docs. Invoke as /config-doctor to audit environment variables, settings, configuration drift, or an environment example file.
disable-model-invocation: true
---

# Config Doctor

Every configuration name has one authoritative declaration and an echo wherever an environment
boots. This doctor finds where the echoes disagree, which names nothing reads, and which names
nothing deployed sets.

## Dependencies

- `doctor-protocol` — own the run.
- `pre-production` — decide whether removing a flag that changes behavior is the clean target.

Also read the repository's checklist for adding a configuration value when the skill listing
declares one, found by its description. It names the locations a value must reach; this doctor
never restates them. Read the repository's deployment skill the same way when one is declared: its
read-only guidance is how a deployment's environment is read here, and reading activates nothing
else it offers.

## Inventory

Discover every place a configuration name is declared or read: typed settings models with each
field's type, default, and required-ness; environment example files; test environment blocks in
tool configuration; container, CI, and deployment manifests; workspace and cloud-agent environment
files; documentation that names a variable; and every reader — application code, a library that
reads the variable itself, a compose service, a workflow step, a front end. Build a
name-by-location matrix before judging anything. Record names and locations, never values.

A deployment whose environment is declared outside the tree — on a hosting platform's application
specification — is one column of that matrix, read by name through the deployment skill. That read
is the measurement taken once before fan-out: names only, one column per deployment, and a
deployment that cannot be read is a column recorded as unread, never as empty, because an empty
column makes every field with a default look unset everywhere.

For every field whose default is absence — `None`, an empty value, off — record what its reader
does with that default: refuses it, branches on it, or passes it through. The Missing and Unused
lenses read that column.

## Lenses

### Missing

A field a settings model declares that an environment booting that model does not supply,
including the test environment. The failure surfaces only in that environment, at startup, where
nobody was looking for it.

The same shape hides behind a default: a field declared with one that its reader refuses — raising
on the default, or passing it to a call that rejects it — while no deployment column sets it. The
declaration conceals a demand the environment does not meet, and the failure moves from startup to
first use.

### Orphaned

A name an example file, manifest, or environment block supplies that no model declares and no
reader reads: a vestige of a removed setting, or a read that bypasses the typed model.

### Mismatched

One name with different types, defaults, placeholder styles, or required-ness across locations, or
an override present in one sibling environment and absent from another that boots the same model.

### Misdeclared

A name declared somewhere other than where the processes needing it can share one declaration.
Mismatched catches this only when the copies disagree, so both shapes below pass every other lens.

One name declared on two or more models with the *same* type and default is one concept written
several times and held in step only by review. The next edit to one copy is the divergence
Mismatched will eventually report; the duplication is the defect that produces it.

A process whose environment supplies a name, and whose code reaches a reader for it, that declares
that name on no model it owns is the mirror image. The value still arrives, so nothing fails at
startup — it is validated by whichever model does declare it, often a third-party library's, under
weaker bounds than the owning services impose. Read the deployment columns and the readers
together: a name in a column with no declaration on that process's model is this shape, not
Orphaned, whenever any reader in that process consumes it.

### Unused

A settings field with no reader, or a field whose default is absence that no deployment column sets
while its reader branches on it: the branch its value selects runs only where test and
local-development locations set it, and nothing that ships reaches it. Trace readers the way a live
consumer is traced: application code, a library reading the variable directly, a compose service, a
workflow step, a front end. Tests are not readers, and a test environment block or a local example
file is not a setter. Check every field whose default is absence against the deployment columns and
report each one, field by field.

### Bypassed

An environment read in application code outside the typed model. The matrix cannot see it and the
example file cannot document it.

## Dispositions

- Missing: declare the value wherever its siblings are declared, with a placeholder in test and
  example locations and no real value committed anywhere.
- A default its reader refuses is declared nowhere until the disagreement is settled, because the
  deployment's silence and the reader's demand are equally likely to be the wrong side: the reader
  is wrong when nothing that ships can use the value, the declaration and the deployment column are
  wrong when something can, and where the target contract does not show which, both fixes go to
  the user.
- Orphaned or unused: delete the name and every vestige — the example line, the manifest entry, the
  test placeholder, the doc sentence. Removing a flag that changes behavior is a surfaced trade-off
  under `pre-production`, never a silent deletion.
- A field nothing deployed sets is that trade-off with three outcomes, and the plan names all
  three: a deployment should carry it, so it is Missing in that column and declared there; it is a
  local-development tool, retained with the tool and the branch named in the ledger; or it is a
  capability no deployment can use, deleted with the branch its value selects and every vestige.
- Mismatched: reconcile toward the typed model's declaration; a per-environment override earns a
  stated reason.
- Misdeclared: give the concept one declaration the processes needing it share, and delete the
  copies. Where that set is every process, the declaration belongs on the shared base; where it is
  a capability only some of them have, it belongs on a model scoped to that capability, which the
  processes without it never load. A subclass that deliberately narrows what the shared declaration
  allows says so on the field rather than restating it.
- Bypassed: route the read through the typed model.
- Where the repository can derive an example file or a test block from the models, propose that
  derivation as the guard, so the matrix cannot drift again.

The cross-cutting reviewer compares models with each other — one name declared on two models,
whether or not the declarations agree — and the locations each checklist, manifest, and example
file names against the matrix. It also reads each deployment column against the model that process
loads, which is where a name a process receives but declares nowhere becomes visible. The final adversarial reviewer re-derives the matrix for every retained
mismatch, re-reads the deployment columns for every field retained as a local-development tool,
and confirms that each removed name has no surviving reader.

## Report Additions

- the name-by-location matrix, with every cell that changed;
- the deployment columns read, and each column unread with the reason;
- names declared, removed, and reconciled, by location;
- the readers traced for each removal;
- for every field no deployment sets, its outcome.
