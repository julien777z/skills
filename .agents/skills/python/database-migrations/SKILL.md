---
name: database-migrations
description: Guide for authoring, rebasing, and troubleshooting Alembic database migrations, including how to avoid and fix branched migration graphs.
---

# Database Migrations

Read the operational profile named by project rules for migration layouts, runner commands, CI jobs, and fixture ownership before applying this policy. Resolve every role below through that profile; do not invent local paths.

## Structure

Migrations live under the project's revision directory. Each service has one canonical migration
chain shared by every configured deployment domain.

Every chain is **replayable from an empty database**: its root revision (the project's initial-schema revision name pattern) creates the service schema and all objects, and `alembic upgrade head` on an empty database must always succeed. The migration suite replays all chains from empty on every PR and verifies the result matches the current SQLAlchemy metadata — a migration that cannot deploy fails CI before merge.

Every chain is also replayed **populated**: the project's populated replay test fills every table with generated rows before each revision and compares an exact per-row census before and after each step. Every stored value of every row must survive byte-identical unless the revision's entry in the project's survivorship policy registry declares the change and verifies it per row. A revision that loses or corrupts any row's data without a declaration fails CI. The destructive-operation check additionally scans each revision's `upgrade()` for destructive operations (drops, type changes, UPDATE/DELETE statements, unclassifiable SQL) and requires each one to carry an exact acknowledgment in the same policy registry — missing and stale acknowledgments both fail.

Shared tooling lives in the repository operational profile's shared migration package (runner, revision-graph helpers, drift comparison, file validation); the repository operational profile's migration CI entry point and the test suite both build on it.

## Authoring Rules

- **Autogenerate is the default for a schema change** — the CI workflow generates the revision.
  Correct an existing revision only under **Applied Is What Makes History** below.
- **A column rename is always hand-written.** Autogenerate compares two schema snapshots, in which a
  rename is indistinguishable from a drop plus an add, so it renders every rename as `drop_column` +
  `add_column` and discards the column's data. Write `op.alter_column(table, old_name,
  new_column_name=new_name)`, which moves the values with the column, and mirror it in `downgrade()`.
  `reject_implicit_column_renames` refuses to emit the drop-plus-add shape, so this fails at
  generation rather than in production.
- Handwritten backfill and schema-repair migrations keep their Alembic entrypoints in `versions/`
  and place substantial revision-specific logic in the project's revision-owned backfill package.
- Put generic backfill and rollback mechanics in the project's shared backfill runtime package, with
  engine-specific helpers under that package's engine owner. Do not promote
  one-off migration behavior into the shared package.
- Revision IDs must be real hex strings, not placeholder values like `a1b2c3d4e5f6`.
- A revision-specific helper under the project's revision-specific fixture package uses the migration filename with
  its leading revision hash and underscore removed. Its test module uses the same name prefixed
  with `test_`: `<revision_id>_<migration_name>.py` pairs with
  `revisions/<migration_name>.py` and `test_<migration_name>.py`.
- **Migration scenarios use typed fixtures for every identity.** Reuse the suite's canonical user,
  organization, and related-record fixtures instead of creating ad hoc UUIDs or synthetic rows.
  When a scenario needs a related identifier the fixtures do not model, add a typed fixture at the
  nearest shared test boundary; promote it to the repository operational profile's shared test-utility owner only when multiple test
  surfaces can reuse it. Generated whole-schema population remains the sole owner of arbitrary
  values needed to exercise unknown historical tables.
- **A destructive upgrade operation requires a policy entry.** Any `drop_column`, `drop_table`,
  `drop_constraint`, column type change, UPDATE/DELETE statement, or SQL the audit cannot prove
  read-only must be acknowledged in the project's survivorship policy registry with its exact
  kind, table, target, and statement digest. Rewrites and backfills additionally declare a per-row
  verifier there, and data-reading migrations get a `prepare` hook that arranges the generated
  population into the eligible, ineligible, and boundary cases the migration must handle.
- **A migration that enqueues background jobs declares their execution contract.** Use the project's job-migration contract and validation registry to specify payload shape, initial status, and handler compatibility. Test the persisted payload against the real job registry. If migration and worker activation are separate release phases, keep jobs unclaimable by the old worker and verify activation through the real persistence boundary.

## What A Change Owes The Rows It Breaks

- **A migration converts what a change would otherwise strand.** When a change leaves stored values
  unreadable or invalid under the new contract — a retyped column, a re-keyed encryption context, a
  reshaped payload — those values are part of the change, and the revision carries them across.
- **Never write a migration on the assumption that the data can be thrown away.** "It is only dummy
  data" describes today, stops being true without announcement, and is invisible in the revision
  afterwards. The migration that assumed it is the one that runs against real rows later, and by then
  nobody is reading its body to check.
- Reach for these in order, and take the first that reaches the new shape:
  1. **A cast**, where the stored values are already valid in the new type — `postgresql_using` retypes
     the column and keeps every row.
  2. **A conversion**, where they are not: read each value, transform it, write it back. This is the
     case a re-encryption, a re-encoding, or a unit change falls into, and it is ordinary work rather
     than a reason to reach further down this list.
  3. **Removal**, only where neither reaches the new shape and the rows block their own `ALTER` — a
     column whose stored values are not valid members of the type it is becoming. Clearing that table
     is then a precondition of the schema step rather than cleanup after it, and the policy entry
     **Authoring Rules** requires above is what states publicly what it destroys.
- That last step is narrow. It covers only the table the altered column belongs to; it never licenses
  deleting rows to spare a read path from a shape it should reject, or to tidy records a change merely
  made uninteresting. Say in the pull request that it removes rows.
- A conversion that needs a live external service — a key service to re-encrypt through, an API to
  re-resolve against — is still a migration. Say in the pull request what it needs and what happens to
  a row it cannot convert; never let it silently skip one.
- **An acknowledgment documents destruction; it does not make data loss safe.** Before a destructive
  operation discards a stored value, either carry that value into the new shape or retain enough exact
  recovery material for `downgrade()` to restore it. A revision with neither a backfill nor a tested
  restoration path does not pass finalization.

## Stored-Format Transitions

- A migration reads the representation stored by the revision immediately before it, not the ORM or
  decoder as they exist after the application change. Prepare tests with raw pre-revision values so an
  expected old format cannot reach a new decoder and abort the upgrade.
- Test the transition in both directions: upgrade real old-format values into the new representation,
  verify their domain value under the new reader, downgrade real new-format values, and verify the old
  reader sees the original domain value again. Compare stored bytes too when the operation promises to
  move rather than rewrite them.
- When a migration can commit in batches, call an external service, resume after failure, or encounter
  legitimately mixed storage, recognize both representations explicitly. Treat an already-converted
  row as complete and transform only the old representation; test mixed rows and retrying the operation.
- An encryption change carries every decrypt capability needed for the old ciphertext through the
  rewrite and verifies ciphertext written for the new backend or key. Do not switch configuration first
  and then assume the new backend can decode the value being replaced. Downgrade either restores the
  original ciphertext or re-encrypts the same plaintext for the old reader with a tested key path.
- Never classify a row as malformed merely because it has the format the migration exists to replace.
  An unconvertible row fails the revision with its sensitive value omitted from logs; it is never
  silently skipped, nulled, or deleted.

## Applied Is What Makes History

- The database behavior of a revision any environment has run is history. Its schema result, stored-data
  transformation, upgrade and downgrade outcome, ordering, transaction boundaries, retry behavior, and
  failure behavior stay unchanged. A behavior-preserving refactor may edit its implementation only when
  focused migration tests prove those outcomes equivalent. A correction or intended behavior change is
  a **new** migration on top. Auto-generated migrations from the GitHub workflow follow the same rule.
- **A revision no environment has applied yet is not history — edit it in place.** There is no replay
  to preserve, so correct the revision itself rather than layering a second one on top to undo it.
  This holds whatever the mistake is: a destructive body, a wrong constraint name, a missing index. Say
  in the pull request that you edited it.
- Establish "not applied yet" from the real `alembic_version` row in every environment, never from
  assumption. That fact is the whole basis for editing rather than adding.
- Once any environment has applied it, a later revision is the only route, and for a destructive body
  it is not a repair: that database lost the values and will never re-run the corrected body, a fresh
  one keeps them, and both land on an identical schema — so drift detection stays silent about the
  divergence. Recovering the data is an operational restore at that point, not a migration.

## Validation

- **Preflight a handwritten migration before the full target.** Review its version entrypoint,
  backfill, survivorship policy, and revision scenario as one change. Then run
  the project's migration preflight command.
  This reports every stale or missing destructive-operation acknowledgment and every populated-row
  preservation failure together. Fix the complete preflight result and rerun it before starting the
  full target; do not use a full migration replay to discover those policy and verifier errors one at
  a time.
- Run the project's full migration validation command before pushing. It replays every chain from an empty
  database and compares the result against the current SQLAlchemy metadata, so a model change without a
  migration, a branched graph, or a broken `upgrade()` body all fail locally.
- **A rollback test must target its own revision, not `"-1"`.** Relative downgrades are resolved
  against the current head, so any later migration silently redirects them at the wrong revision.
  Resolve the revision under test from the migration graph instead.

## Migration Support Packages

- The project's shared migration runtime package contains the Alembic runtime and helpers with multiple migration-set
  consumers. Its chain-owner module owns everything a chain is addressed by: its target, the database
  URL it reads, and whether that database carries the revisions this code does.
- The project's shared backfill runtime package contains generic backfill and rollback mechanics, grouped further by
  database engine where their behavior is engine-specific.
- The project's revision-owned backfill package contains behaviorally immutable implementation code owned
  by one logical handwritten migration set, including provider and database adapters used only by
  that backfill. Keep it for as long as any deployed database may replay that revision.
- Revision files under `versions/` remain the Alembic entrypoints and call the owning backfill
  package when the migration is too substantial to keep inline.

### Where A Revision's Test Scaffolding Lives

- **Test helpers written for one revision are disposable, and their location must say so.** A prepare
  or verify hook that exists to exercise a single migration dies the moment that revision is
  rebaselined away, so it lives under the project's revision-specific fixture package in a topic module that can be
  deleted whole, not in the module holding the registries.
- `revisions/` sits at the migration-test root rather than inside `survivorship/`, because the chain
  tests under `api/` and the shared `conftest.py` read from it too. A package only one suite may
  import belongs inside that suite; this one never was.
- The project's survivorship policy registry holds only the registries mapping a revision to its
  expectations. Anything it points at that is specific to one revision — a row-transform verifier, a
  population value factory, a fixture arranging the rows a migration will rewrite — is imported from
  `revisions/`, never defined inline.
- A rebaseline that drops the migration history is an ordinary possibility here rather than a remote
  one. Keeping the disposable half separable is what makes that a deletion instead of an audit.
- **The project's durable migration-test helper package is for helpers that outlive every revision, and the test is whether a
  helper names a table.** A helper spelling out columns in raw SQL is pinned to the schema as it stood
  at one revision: the next rename falsifies it and a rebaseline deletes the migration it was written
  for, so it belongs in `revisions/` however many modules import it. A helper that only drives the
  database engine — suspending foreign-key enforcement, reading a session setting — knows no schema
  and stays.
- **The tests do not mirror the project's shared migration runtime package, because the project's durable migration-test helper package is already the
  durable-helper package above.** A module under the project's shared migration runtime package is covered at the migration-test
  root instead, following the project's declared test layout and package boundaries.
- Reach for `utils/` because a helper is schema-independent, never because a second test wanted it.
  Two revisions needing the same seeding is ordinary, and it makes that seeder shared, not durable;
  promoting it on import count is what leaves the tests' `utils/` package holding the very rows a
  rebaseline is supposed to take with it.

### Temporary Backfill Tables

- Put a temporary, migration-owned table that must remain visible to ORM metadata under the owning
  application's declared temporary backfill table package.
- The `tables/backfills/__init__.py` module exports one metadata registry. The normal table package
  imports that registry so drift detection sees every temporary table, but it must not export the
  individual table models as application tables.
- Application services, routes, and libraries must not import or query backfill table models. If a
  table becomes part of runtime behavior, move it to its permanent domain package and treat that as
  an explicit lifecycle change.
- Before placing backfill-related code under the application package, identify at least one non-test
  application consumer. Code used only by a migration or backfill belongs in
  the project's revision-owned backfill package.
- Keep a temporary table and its metadata registration until the rollback or recovery obligation it
  supports has ended. Its cleanup migration and removal from ORM metadata land together.
- Do not let a temporary backfill table become an implicit permanent application dependency.

## The Branched Migration Graph Problem

### What it is

Each service's canonical migration chain must be **strictly linear** — one head, one tail, no
forks. Migration-chain validation fails with:

> `Expected exactly one head revision, found 2: [...]`

or

> `Local migration graph for <service> is not linear. Manual edits are required.`

### How it happens

1. Your branch is created when the latest migration is revision `X`.
2. You add a migration with `down_revision = "X"`.
3. Meanwhile, another migration `Y` (also with `down_revision = "X"`) is merged to main.
4. Now two revisions share the same parent — a fork.

### How to fix it

1. Identify the actual latest revision on main:
   Inspect the revision directory identified by the operational profile.
   Find which file has no other file pointing to it as `down_revision` — that is the current head.

2. Update your migration's `down_revision` to that head:
   ```python
   down_revision: Union[str, None] = "<actual-head-on-main>"
   ```

3. Also update the `Revises:` comment in the docstring to match.

### How to prevent it

- **Before opening a PR**, check whether any new migrations have landed on main in the same environment/service since your branch point.
- **After rebasing or merging main**, re-check `down_revision` in every migration file on your branch.
- When multiple PRs touch migrations simultaneously, coordinate to ensure only one is open at a
  time per service, or chain them explicitly.

## Checklist When Adding a Handwritten Migration

- [ ] `down_revision` points to the service's **actual current head**
- [ ] Revision ID is a real unique hex string (not a placeholder)
- [ ] `Revises:` docstring comment matches `down_revision`
- [ ] Every deployment domain consumes the same canonical revision file
- [ ] Shared and operation-specific helpers use their correct package
- [ ] Migration-only provider and database adapters live in the project's revision-owned backfill package
- [ ] Temporary support tables live under `tables/backfills/`, appear in its metadata registry, and
      have no application consumers
- [ ] A temporary table's cleanup migration removes its ORM metadata registration in the same change
- [ ] `downgrade()` reverses every `upgrade()` step in the correct order (indexes before columns)
- [ ] No manual edits to auto-generated migration files
- [ ] Destructive operations, rewrites, and backfills are declared in
      the project's survivorship policy registry with per-row verifiers and exact acknowledgments
- [ ] Every inserted background job has the declared migration contract; a phased release holds it until a compatible worker activates it
- [ ] Every discarded value is converted or recoverable through a tested downgrade path
- [ ] Stored-format changes test old-to-new upgrade and new-to-old downgrade with raw stored values
- [ ] Resumable or mixed-format rewrites recognize already-converted rows and pass retry coverage
- [ ] The configured migration suite passes — the chain must replay from an empty database,
      preserve every populated row, and downgrade cleanly at every revision

## Debugging CI Failures

| CI check name | Likely cause |
|---|---|
| `test-suites (migrations)` (Run Tests) | Branched graph, a runtime error in an `upgrade()` body, or model changes without a matching migration — the failure output names the service chain and shows the missing operations |
| `Migrations: Generate` | A generated revision is invalid or the chain is no longer linear |
| `Submit Release (<domain>)` | The release deployment could not be created for that domain |
| A release deployment stuck at `queued` | No runner is polling that domain, or an earlier release is still migrating |
| A release deployment reporting `failure` | A pending chain is invalid, two revisions share the same `down_revision`, or the guard refused the activation |

Run the suite locally with the project's full migration validation command; it replays every chain against the local
Postgres services, so failures reproduce without touching staging.

When a branched-graph error appears ("Expected exactly one head revision"), follow the **How to fix it** steps above.
