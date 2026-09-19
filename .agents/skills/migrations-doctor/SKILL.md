---
name: migrations-doctor
description: Audit and correct a repository's database migration chains, revisions, registries, and test scaffolding. It covers graph integrity, revision uniformity, downgrade adequacy, survivorship presence, schema parity, ownership, environment consistency, and history discipline. Invoke as /migrations-doctor to audit migrations, a forked or branched chain, revision headers, downgrades, backfills, or migration tests.
disable-model-invocation: true
---

# Migrations Doctor

A migration chain is linear, replays from empty to the current models, reverses cleanly, keeps every
row it does not declare it destroys, and reads the same in every revision. This doctor finds where a
chain stopped being that.

## Dependencies

- `doctor-protocol` — own the run.
- `pre-production` — decide the clean target where a correction changes stored shape.

Also read the repository's migration skill when the skill listing declares one, found by its
description. Its authoring, survivorship, history, and validation rules govern every correction;
this doctor never restates them.

## Inventory

Discover the migration framework and every chain at runtime. For each chain: its revisions, with
each revision's identifier, parent, header, file name, body, and the generator template that
produced it; the model metadata the chain must match; every registry or manifest that names
revisions — checkpoint boundaries, backfill registrations, survivorship policies, target
manifests, workflow path filters; every registered backfill or data operation, with the callable
behind each of its hooks laid out in a table, because a registry reads cleanly at its call site
while hiding what the hooks resolve to; revisions that share a name across chains, paired for
comparison; the shared migration mechanics and the per-revision packages; the migration runtime
and each chain's environment module; the migration tests and their scaffolding; and which
environments have applied which revisions, read from the real version table where reachable and
treated as applied where not.

The chain replay and drift check the repository already defines are the measurement taken once
before fan-out.

## Lenses

### Graph And References

One head per chain and a linear path to it; every parent resolves; no merge revision joining a
fork. File name, identifier, and header agree. A placeholder identifier, and a creation timestamp
on a round minute or one that another revision repeats, are fabricated and are findings. Every
registry and manifest names real revisions in chain order, and no two operations claim one
boundary.

### Revision Uniformity

One header style across every revision, and a generator template that emits exactly that style.
No generator residue — autogen markers, unused imports, a module docstring where the repository's
rules ban one. No per-revision copy of a value the target manifest carries. One idiom per
operation — enum creation and removal, qualified identifiers, batch loops — reached through the
shared helpers rather than re-implemented in each revision. A revision name describes the schema
change, not the git operation that produced it.

### Downgrade Adequacy

Every upgrade step reversed in the right order: for each dropped column, no index or constraint on
the same table is dropped after it. A docstring-only or `pass` downgrade only where the policy
mechanism records the loss as acknowledged with recovery material. A downgrade a fraction of its
upgrade's size is read, not assumed adequate.

### Survivorship Presence And Wiring

Every revision carries a policy entry or an explicit no-rows classification. An operation whose
verify and reverse hooks resolve to the same unconditional success verifies nothing. A migration
that reads rows has a preparation hook arranging the eligible, ineligible, and boundary cases it
must handle. Discarded values are converted or recoverable; stored-format transitions are tested in
both directions; resumable rewrites recognize already-converted rows. The exactness check the test
tests already enforce is verified to run, never re-implemented.

### Schema Parity

Replay from empty matches the current models. A model change without a revision, a revision
changing what no model declares, and a historical revision importing a current application model
instead of stating the shape it needs are each a finding.

### Ownership And Placement

Revision-specific logic in its own package and shared mechanics in the shared one. A shared module
naming one table or revision, a package of one tiny module, a stuttering package and module name,
a runtime module past the size limit mixing target construction, rendering, and runners, and
migration-only code inside an application package are each a finding. A temporary table is
registered and cleaned up in the same lifecycle. The same change hand-copied into two chains is weighed
for one shared operation: two chains carrying a revision of the same name are compared line by
line.

### Environment And CI Consistency

Per-chain environment modules diverge only in the service they name; one chain registering
operations the others omit is a finding. A hand-maintained workflow path filter beside the manifest
that derives it, the same table of schema names or metadata references derived from the manifest
in two modules (a CI script and a test conftest, two test modules), and a documented migration
command that does not exist are each a finding.

### Test Scaffolding

The tests' `conftest.py` is reserved for lifecycle wiring; revision-specific fixtures and
schema-specific tables live in the revision package; a durable helper names no table or column; a
schema-independent helper is not filed as revision-specific. Where the repository states a
revision-to-test pairing rule, the pairing holds; otherwise policy coverage is the index. A deferral
record for these tests that points at a path that no longer exists is reported to `defer-scope`.

### History Discipline

An unapplied revision is corrected in place; an applied one only by stacking a new revision. A
create-then-rename within a few unapplied revisions collapses. A merge-of-main revision carrying
dozens of unrelated operations is split, or rebaselined where the repository supports it. A hand
edit to a generated revision is stated in the change.

## Dispositions

- Re-point a parent to the real head and fix the header; regenerate the template and re-emit
  headers from it; strip generator residue.
- Replace per-revision constants and idioms with the shared helper, and fold a hand-copied pair
  into one shared operation where the chains genuinely share it.
- Add the missing policy entry, preparation hook, or downgrade step; a data-loss path with no
  recovery is a blocker to report, never a loss to acknowledge on the run's own authority.
- Move code to its owner; reconcile environment modules, manifests, and filters to one source.
- A model change with no revision gets one; a revision changing what no model declares is corrected
  according to its applied state; a historical revision importing a current application model is
  rewritten to state the shape it needs.
- Edit in place or stack according to applied state; a correction whose applied state cannot be
  established is stacked.

The cross-cutting reviewer compares chains and registries with each other: a registry and a chain
that disagree, two chains claiming one boundary, and the same change hand-copied into two chains.
The final adversarial reviewer replays every chain the run touched, confirms that a stacked
correction did not narrow the approved downgrade or survivorship coverage, and challenges every
revision the run retained as applied without version-table evidence.

## Report Additions

- per chain: heads found, revisions checked by lens, and corrections applied;
- policy coverage before and after;
- the evidence source for applied state in each environment.
