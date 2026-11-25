# Support Packages

Contents: **Migration Support Packages**, **Where A Revision's Test Scaffolding Lives**, **Temporary Backfill Tables**.

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
- The revision-specific fixture package sits at the migration-test root, beside every suite and
  shared fixture module that reads it, rather than inside any one suite's package. A package only
  one suite may import belongs inside that suite.
- The project's survivorship policy registry holds only the registries mapping a revision to its
  expectations. Anything it points at that is specific to one revision — a row-transform verifier, a
  population value factory, a fixture arranging the rows a migration will rewrite — is imported from
  the revision-specific fixture package, never defined inline.
- A rebaseline that drops the migration history is an ordinary possibility here rather than a remote
  one. Keeping the disposable half separable is what makes that a deletion instead of an audit.
- **The project's durable migration-test helper package is for helpers that outlive every revision, and the test is whether a
  helper names a table.** A helper spelling out columns in raw SQL is pinned to the schema as it stood
  at one revision: the next rename falsifies it and a rebaseline deletes the migration it was written
  for, so it belongs in the revision-specific fixture package however many modules import it. A helper that only drives the
  database engine — suspending foreign-key enforcement, reading a session setting — knows no schema
  and stays.
- **A module under the project's shared migration runtime package is tested at the migration-test
  root**, following the project's declared test layout and package boundaries; the tests keep no
  package that mirrors the runtime package.
- Reach for the durable helper package because a helper is schema-independent, never because a
  second test wanted it. Two revisions needing the same seeding is ordinary, and it makes that seeder
  shared, not durable; promoting it on import count is what leaves the durable package holding the
  very rows a rebaseline is supposed to take with it.

### Temporary Backfill Tables

- Put a temporary, migration-owned table that must remain visible to ORM metadata under the owning
  application's declared temporary backfill table package.
- That package's `__init__` module exports one metadata registry. The normal table package
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
