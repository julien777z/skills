---
name: schema-doctor
description: Audit and correct unjustified nullability, model complexity, primary-key design, index design, and table and model declarations that depart from the repository's rules, across repository API contracts, serialized schemas, persisted schemas, and the field flows connecting them. Use to review requiredness, optional fields, nullable columns, duplicated contract models, unnecessary fields, shared model ownership, missing or redundant indexes, primary keys, or schema consistency across a repository, or to map how fields flow between contracts and storage. Run only when the user asks for it.
short_description: 'Check models and schemas for unnecessary nulls, complexity, keys, and indexes.'
---

# Schema Doctor

Trace every selected field and contract model from its authoritative source through live consumers
and storage, then replace unjustified nullability, model complexity, and access paths with the clean
contract and index design.

## Dependencies
- `doctor-protocol`
- `pre-production`

## Inventory

Run `doctor-protocol`.

Also read the repository's migration skill when the skill listing declares one, found by its
description. Its migration mechanics, data survivorship, and validation rules govern every
requiredness cascade and index change; this doctor never restates them.

Trace each selected declaration across repository ownership boundaries far enough to cover its
authoritative source, every producer and live consumer, persistence, generated contracts, and
affected validation.

A **live consumer** is anything that reads the value, whatever language it is written in: a call
site, another live symbol, a serializer or read mask that names the field, a wire contract, a stored
column, a first-party front end, in this repository or another the user owns, that deserializes it, or a third-party library
reading an environment variable a settings field populates. Absence from call sites in one language
is evidence about that language, not about consumers. Only state that never leaves the interface is
outside the default field inventory.

Two shapes hide a reader routinely, and the trace reaches past both. A read mask or serializer built
from a model's whole field set carries every field across the boundary while no line names any one of
them. A hand-written type in another language mirroring the model is the only place the field is
read, and no search of this language will find it.

Within scope, inventory every discovered first-party field and its containing contract model in:

- inbound and outbound API requests and responses;
- internal RPCs, events, commands, queues, and other serialized contracts;
- protobuf source definitions, descriptors, validation rules, and generated consumers;
- persistence models, database schemas, constraints, indexes, and migrations;
- local models that mirror, narrow, proxy, or persist third-party data.

Inspect serializers, converters, validators, producers, and live runtime consumers, including
administrative interfaces, frontend applications, API clients, workers, exports, and other user- or
system-facing reads. Do not inventory arbitrary implementation-only fields as though they were
application contracts.

For persisted models, also inspect the live application queries and mutations that filter, join,
order, group, paginate, update, or delete rows. Trace foreign-key actions and other constraint work
through the referencing tables so index decisions reflect the operations the database must perform,
not only the table declaration.

Tests, fixtures, and factories may reveal assumptions and, where the repository keeps them, must validate the resulting contract, but
they are never live consumers or authoritative evidence for requiredness, nullability, field or model
retention, duplication, or ownership. A test cannot prevent a field merge, removal, rename, or move;
update it after deciding the contract from authoritative sources and runtime behavior.

Read generated output and vendored definitions when they are evidence, but
edit their canonical source or regenerate them through their owner.

### Ledgers

Keep a field ledger, a model ledger and an index ledger for the complete audit, each entry holding
what [the ledger reference](references/ledgers.md) lists for its kind, as the detail behind the
protocol's ledger entries.

Build the corresponding directed field-flow graph while auditing even when the caller did not ask
to see a diagram. Group equivalent fields only when they have the same guarantees and traverse the
same edges; never let grouping hide a field whose nullability differs.

Do not infer a domain invariant from current non-null rows, one observed payload, one fixture, one
producer, or a test written around the current shape. Enumerate every valid producer and live
consumer before tightening or simplifying a shared field.

**Shared index.** From the index `doctor-protocol`'s **Share The Index** keeps, this doctor reads
the file inventory, symbol and import tables and dependency list. It writes the model field table —
every model with its field names, annotations, owner and boundary — and the table and index
inventory.

### Pre-Pass

These are the mechanical steps `doctor-protocol` runs once before any reviewer reads; a reviewer
confirms or rejects their candidates and traces the flows no command can. A tool the repository does
not configure is handled as `doctor-protocol`'s **Measure Before Fan-Out** says. A database the run
cannot reach read-only is recorded the same way.

- **Field dump** — a script kept in the run's working files loads every first-party model and
  prints its field names and annotations: a validation library's declared fields, the ORM's table
  metadata, protobuf descriptors, and exported types in another language through its compiler. It
  then prints, per pair of models, the shared names, the names one holds and the other lacks, and
  each shared name whose annotations differ.
- **Nullable declarations** — every optional annotation, nullable column, optional protobuf field
  and default of absence, by declaration.
- **Drift** — the migration tool's own check that the models and the migrated schema agree.
- **Declaration shapes** — the searches below for the shapes **Declarations** names.
- **Indexes**, where a database is reachable read-only — its index definitions, the indexes its
  usage statistics show unused, and every foreign key with no index leading on its columns. The
  queries below are PostgreSQL's; another engine uses its own catalog.
- **Null counts**, where a database is reachable read-only — rows holding null per nullable
  column, as supporting evidence only: current non-null rows prove no invariant.

```sh
rg -n 'Optional\[|\| None|nullable=True|\boptional\b'
rg -n '@dataclass|NamedTuple|create_model\(|Field\(description='
rg -n '\bColumn\(|lazy=|DateTime\(|\btext\(|execute\(f?"'
```

```sql
SELECT schemaname, tablename, indexname, indexdef FROM pg_indexes
WHERE schemaname NOT IN ('pg_catalog', 'information_schema');

SELECT relname, indexrelname, idx_scan FROM pg_stat_user_indexes WHERE idx_scan = 0;

SELECT c.conrelid::regclass AS referencing_table, c.conname
FROM pg_constraint c
WHERE c.contype = 'f'
  AND NOT EXISTS (
    SELECT 1 FROM pg_index i
    WHERE i.indrelid = c.conrelid
      AND (i.indkey::int2[])[0:cardinality(c.conkey) - 1] @> c.conkey
  );
```

### Measures

The counts `doctor-protocol` takes before the audit and again after the fixes: contract models and
fields; nullable declarations; model pairs with overlapping field sets, and shared names with
divergent annotations; drift-check findings; declaration-shape hits; and, where a database was read,
indexes, unused indexes and foreign keys with no supporting index.

## Lenses

Every finding is recorded in
`doctor-protocol`'s finding shape: its fix names the declaration that changes and every producer,
consumer, migration and generated output that changes with it, and its proving check is the
repository's contract, generation and migration checks over that cascade.

| Lens | Flags | Reach |
| --- | --- | --- |
| **Nullability** | A field nullable, omittable or defaulted where no supported state is absent, or required where one is. | Partition; a field crossing services is traced across the repository. |
| **Convergence** | Models that overlap, diverge in type or name, or validate one concept two ways. | Whole repository. |
| **Model Surplus** | A field, model or translation layer the live system does not need. | Whole repository: a live consumer may sit in any partition or language. |
| **Keys And Indexes** | A primary key or index the live operations do not justify, or one they need and lack. | Partition, by persisted schema. |
| **Declarations** | A table or model declared against the repository's declaration rules. | Partition. |

Read [the lens criteria](references/lenses.md) before building the inventory: each lens in the
table is a section of it, stating the defect shape, the checks, the remedy and what is left alone.

## Reviewers

Reviewers are capped as `doctor-protocol`'s **Launches** sets. The
schema, service, or contract owner dictates the partition cut, and each partition reviewer returns
ledger entries for its declarations.

The cross-cutting reviewer owns **Convergence** and **Model Surplus**, working from the field dump
with its pairwise comparison in the pre-pass output and from the domain ledgers. It compares the
domain ledgers, traces shared and cross-service fields and models, finds missing producers or live consumers, identifies canonical
shared owners, compares database access paths with index coverage, and challenges every proposed
requiredness, simplification, or index change whose evidence does not establish the full flow and
semantics. The parent states the end-to-end conclusion for each selected field, model, and
persisted table.

The final reviewer challenges the requiredness and simplification decisions, retained nullable and
separate states, shared ownership and index dispositions, and cross-boundary consistency; the
completion check confirms every planned field and model cascade reached each live consumer.

## Dispositions

- **Change boundary.** This doctor changes contract and persistence declarations, their
  validation, serialization, migrations and generated outputs, and every producer and consumer the
  user controls, in any repository, that a changed field, model, key or index reaches. Application
  logic beyond those edges is outside it.
- Breaking an owned API, protobuf or model contract to reach the clean shape is ordinary work, made
  as `pre-production`'s **Target Contract** says; a contract a party outside the user's control
  speaks stays as it is and is reported.
- Remove a nullable path kept only for a transition in the same change, as `pre-production`'s
  **Target Contract** says of transitional support; the placeholder a requiredness migration uses
  while it backfills belongs to that migration, as the repository's migration skill governs it.
- Every schema change lands through the canonical schema and the repository's migration skill. For
  index changes, also run the repository's database-specific schema checks and representative
  read-only query-plan validation when configured.
- An external, equivalence, ownership or workload question the evidence does not settle is
  recorded unresolved, and no change that depends on it is made.

## Requested Maps

When the caller asks for a map, return Mermaid flowcharts in the response unless they explicitly ask
for a repository artifact.

- Produce one detailed map per domain showing authoritative sources, owned models, validation and
  transformation boundaries, serialized contracts, persistence, and material consumers.
- Produce a separate overview containing only connections between domains or services.
- Do not repeat each domain's internal edges in the overview.
- Annotate transitions whose values are required, nullable, omittable-but-non-null, or unresolved.
- Show consolidated or retained model ownership where it explains a cross-consumer boundary.
- Show index coverage where a persisted access path or referential action materially depends on it.
- Split or group nodes for readability without concealing a nullability transition or unresolved
  source guarantee.

## Report Additions

Append to the protocol's report:

- the resolved scope and every domain, schema, and contract inventoried;
- per-domain and per-contract declaration and flow-edge counts by disposition, including declarations
  that were already correctly required and needed no change, plus the total end-to-end field flows;
- each corrected requiredness cascade and its authoritative evidence;
- each removed, merged, reshaped, consolidated, or newly shared field and model, its live consumers,
  and the evidence for its final owner and shape;
- each retained overlapping model or field and the semantic or boundary distinction that requires it;
- each retained nullable or omittable field and the supported state that requires it;
- each retained, added, reshaped, or intentionally absent primary key and the identity, access,
  write, storage, and database-engine evidence for its disposition;
- each added, reshaped, removed, and retained index, the live operations it serves, and the evidence
  for its disposition;
- every unresolved index decision and the missing workload, plan, statistics, or engine evidence;
- every unresolved provider or schema edge and the sources that were unavailable or contradictory;
- migrations, backfills or placeholders, generated outputs, and deliberate contract breaks;
- expected compatibility failures, separated from any unintended break.
- each database the pre-pass could not read;
- each declaration brought to its rule, by rule section.
