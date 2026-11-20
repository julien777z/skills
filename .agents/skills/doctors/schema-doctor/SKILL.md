---
name: schema-doctor
description: Audit and correct unjustified nullability, model complexity, primary-key design, index design, and table and model declarations that depart from the repository's rules, across repository API contracts, serialized schemas, persisted schemas, and the field flows connecting them. Use to review requiredness, optional fields, nullable columns, duplicated contract models, unnecessary fields, shared model ownership, missing or redundant indexes, primary keys, or schema consistency across a repository. Run only when the user asks for it.
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
is evidence about that language, not about consumers.

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

Tests, fixtures, and factories may reveal assumptions and must validate the resulting contract, but
they are never live consumers or authoritative evidence for requiredness, nullability, field or model
retention, duplication, or ownership. A test cannot prevent a field merge, removal, rename, or move;
update it after deciding the contract from authoritative sources and runtime behavior.

A first-party front end, in this repository or another the user owns, that deserializes a selected
boundary contract **is** a live consumer, and the trace reaches it. Only state that never leaves the interface is outside the
default field inventory. Read generated output and vendored definitions when they are evidence, but
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

A partition lens is judged inside one schema, service or contract owner; a whole-repository lens
needs every model at once, so the cross-cutting reviewer owns it. Every finding is recorded in
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

### Nullability

Flags a declaration or flow edge whose required, nullable or omittable shape its authoritative
source does not support. The checks: every candidate in the pre-pass's nullable list, and every
required field a valid producer cannot supply, each traced through the field-flow graph.

Assign every declaration and flow edge one evidence-backed disposition, then record the resulting
end-to-end conclusion for the field. A field may legitimately change disposition after an owned
generation or validation boundary.

- **Required** when every valid creation path can provide the value and absence is not a supported
  domain or lifecycle state.
- **Nullable** when absence itself is a genuine supported state, including a documented provider
  outcome or a field belonging only to some variants of a broader model.
- **Omittable, non-null when supplied** when an update or partial-selection contract may leave a
  field unspecified but may not explicitly clear it.
- **Unresolved** when authoritative evidence is insufficient or contradictory.

Do not confuse transport omission with a nullable value, a serializer's default with a domain
guarantee, or a database constraint with proof that every producer satisfies the contract. A shared
table or contract may retain a nullable field for legitimate variants even when one producer always
supplies it; document the concrete variant rather than weakening or tightening the shared shape by
assumption.

When requiredness is justified, establish it at the earliest repository-owned boundary where the
guarantee becomes true. Update the complete downstream cascade together: validation, contracts,
serialization, storage, reads, tests, and generated consumers. Do not fix only the database column
or add a runtime fallback that hides an upstream mismatch.

For a requiredness migration, invoke `pre-production` and the repository's migration skill. Their authoritative
data, migration-only placeholder, constraint, survivorship, and validation policies control the
implementation. A placeholder is never evidence that a genuinely optional field should be required.

Left alone: a nullable field whose absence is a supported state, with the variant or provider
outcome named in the ledger.

#### Third-Party Contracts

For data received from an external provider, first find official documentation, published schemas,
or specifications matching the integrated API and version. Then inspect the pinned SDK's models,
generated definitions, and runtime serialization contract. Prefer primary sources and record the
version or contract surface that makes the evidence applicable.

If provider documentation and the integrated SDK disagree, determine whether they describe different
versions or operations. Do not choose whichever source supports a desired conclusion. If the
guarantee remains uncertain, mark that external edge unresolved and make no change that depends on
it. Continue auditing and correcting independently provable internal edges in the same domain.

A local provider-shaped model must represent what the provider can actually send. A narrower
repository model may require a provider field only after an owned validation or selection boundary
proves its presence.

#### Protobuf Presence

Treat protobuf source and descriptors as canonical contract evidence. Inspect field presence,
default-value semantics, messages, optional fields, oneofs, wrappers, validation annotations, RPC
methods, conversion layers, and every producer and consumer.

Do not equate a scalar that decodes to a default value with a required field: some protobuf editions
and field kinds cannot distinguish omission from an explicitly supplied default. Express the intended
guarantee through the repository's canonical protobuf or boundary-validation mechanism. If the
current wire shape cannot express the invariant cleanly, use `pre-production` to choose the cleaner
breaking message shape rather than preserving ambiguity.

Edit protobuf source rather than generated output, update every producer and consumer the user controls, in any repository,
regenerate all owned targets, and run the repository-native generation and contract checks. Never
weaken a compatibility gate. Report the exact expected failure caused by an intentional break and
separate it from any unintended break detected in the same run.

### Convergence

Flags models that answer one question in two shapes. The checks are the four comparisons below,
run over the pre-pass's field dump.

Enumerate every first-party model in scope and **compare them pairwise**. Reading files and noting
what looks familiar catches only what a reader happens to notice, and it reliably misses a type
divergence spread across twenty shared field names. The pre-pass's field dump runs the comparison
over the whole repository, and its output drives the simplification below.

Report each of these, with the pair and the fields:

- **Duplicate field sets** — two models with substantial field-name overlap and no inheritance
  relationship between them, including one that is a strict subset of the other. Each is a candidate
  for one shared base both derive from.
- **Divergent types** — one field name declared by two models with different annotations. Count a
  normalizer, validator, constraint, or permission annotation present on one and absent on the other
  as a divergence, not just a different base type. Resolve the annotation through the shared
  metadata helpers rather than a `get_args()` walk, which reports pydantic's own hoisting as a
  finding.
- **Divergent names** — one concept spelled two ways across models that otherwise overlap, such as
  an identifier named `id` on one and `<noun>_id` on another, or a composed name spelled `name` on
  one and `full_name` on another.
- **Within-model inconsistency** — sibling fields of the same concept validated differently inside
  one class. A field that loses its annotated type when it becomes required is the recurring form,
  because requiredness and normalization are independent and a requiredness change invites
  entangling them.

**Unifying a divergence is preferred over deriving around it.** A helper that intersects two models'
field sets, or subtracts one from the other, is a second mechanism papering over the first; the fix
is one declaration. Under `pre-production` an API, protobuf, or model contract break is the
preferred resolution rather than a compatibility path — the reverse of the instinct to keep both
shapes working.

The guard in **Model Surplus** below still applies to every unification: a real
authorization, disclosure, persistence, or wire distinction is never erased merely to reduce the
declaration count.

Left alone: an implementation-only declaration that crosses no serialized or stored boundary, which
another doctor owns; and a pair whose difference **Model Surplus** retains.

### Model Surplus

Flags a field, model, wrapper or conversion with no live producer-to-consumer purpose, and a second
model standing where an annotation would do. The checks and each one's remedy:

Challenge every in-scope field and contract model after establishing its runtime flow. Prefer the
smallest set of models and fields that preserves the domain, lifecycle, authorization, disclosure,
persistence, and wire distinctions the live system actually needs.

- Remove a field with no live producer-to-consumer purpose, once the forward trace has crossed every
  boundary it travels — the serialized contract, the stored row, any mask built from a model's whole
  field set, and the language boundary into a first-party front end. Preservation-only serialization
  and conversions between otherwise-unused shapes do not make it live.
- Remove a model or translation layer with no live consumer, or collapse it into its owner when it
  expresses no distinct contract or policy boundary.
- Merge semantically duplicate fields only after proving they share meaning, authoritative source,
  normalization, units, lifecycle, disclosure rules, and runtime consumers. Similar names or shapes
  are not evidence of equivalence.
- Consolidate overlapping models when they represent the same concept with the same guarantees.
  Update every consumer the user controls, in any repository, and remove superseded shapes rather
  than adding another adapter.
- Prefer an existing shared contract or model owner when multiple independent consumers need the
  same representation. Discover that owner and its dependency rules at runtime; do not assume a
  package name or force consumer-specific policy, persistence, provider, or transport dependencies
  into it.
- Introduce a shared owner only when no suitable one exists, multiple independent live consumers
  establish shared ownership, and the new dependency direction does not invert an existing boundary.

Retain separate fields or models when their apparent duplication encodes a real semantic, lifecycle,
authorization, disclosure, persistence, or wire distinction. Record that distinction so a
recommendation does not erase domain meaning merely to reduce the declaration count. Mark uncertain
equivalence or ownership unresolved and make no simplification that depends on it.

A provider difference is not one of those distinctions, because the two sides of that boundary are
not equally fixed. **A contract the user owns can change; a third-party provider's cannot.**
Only one side can move, so a provider difference is always resolved by moving the repository's model
toward what the provider sends — never by standing a second model beside it and converting. Calling
such a pair "a genuine third-party boundary" describes the one thing that is not a boundary at all:
where both sides are fixed there is a boundary, and here one side never is.

Take these in order, and the first that fits is the answer:

- **A difference in encoding is an annotation on the field** — a validator coercing the string the
  provider sends into the type the model holds, an alias naming its key, an alias path reaching its
  nested one. Never a second model.
- **A difference in content earns a separate model**: the provider carries fields the repository
  deliberately does not, or a shape no annotation can express.
- **A conversion method between two models that mirror each other field for field is the signal**
  that the second model is an encoding difference wearing a model's clothes.
- **Adapting is not imitating.** The provider's encoding crosses into the model — its tokens, its
  date formats, its nesting, its keys. Its vocabulary does not: field names, casing, and domain terms
  stay the repository's own, reached through aliases.

The separate rule at **Third-Party Contracts** is unaffected: a local provider-shaped model
must still represent what the provider can actually send. That rule constrains what the model may
require; it never licenses a second model to hold it.

### Keys And Indexes

Flags a table with no justified key, a key whose shape its reads and writes do not support, an
access path or referential action with no index, and an index nothing uses or another covers. The
checks, read against the pre-pass's index lists where a database was reachable:

Discover the database engine, version, schema owner, migration mechanism, index features, and
automatic constraint-index behavior at runtime. Never assume that defining a primary key, unique
constraint, or foreign key creates every index needed by related reads or referential actions.

- Check every persisted table for a primary key or an explicitly justified keyless design. Verify
  that the key identifies one logical row, is minimal, non-null, stable, correctly typed, and meets
  the ORM, foreign-key, replication, change-capture, and storage requirements that actually apply.
- Evaluate primary-key shape against live reads and writes. Check composite key order, key width,
  generated-value distribution, insertion hot spots, fragmentation or locality effects, referenced
  type compatibility, and database-specific clustering or primary-storage behavior. Distinguish the
  logical primary-key constraint from any physical primary or clustered index the engine maintains.
- Inspect every foreign key from the referencing side. Determine whether joins and cascading or
  validating updates and deletes can locate matching rows without scanning the referencing table.
- Derive candidate indexes from complete live access paths, including equality and range filters,
  join keys, ordering, grouping, pagination, and high-volume mutations. Choose composite key order,
  predicates, expressions, included values, and access methods from those operations and the
  database's actual capabilities.
- Compare candidates with primary, unique, and existing indexes by usable leading keys, predicates,
  ordering, and covered operations. Prefer reshaping or reusing one justified index over adding a
  redundant near-duplicate.
- Account for write amplification, storage, locking, build duration, and maintenance cost. Do not
  index every column or foreign key mechanically, and do not preserve an unused index merely because
  it already exists.
- Use read-only query plans, schema metadata, and index-usage statistics when safely available. A
  small fixture table, current row count, one observed request, or a test written around the current
  schema does not establish the production access pattern or selectivity.

Add, reshape, or remove an index only when its live operations and database semantics justify the
change. Mark workload-dependent decisions unresolved when the required plans or statistics are
unavailable; continue correcting structurally provable gaps such as a referential action that must
scan an unbounded referencing table. Apply each change through the canonical schema and
the repository's migration skill, including its data safety, lock-risk, reversibility, and
validation requirements. Never issue an ad hoc index change against a live database.

Left alone: an index whose worth depends on workload evidence the run cannot read, recorded
unresolved with the missing plan or statistic.

### Declarations

Flags a table or model declared in a shape the repository's declaration rules name a defect,
whatever its nullability. Run each rule section over every declaration in scope and report each
section's result, an empty one included:

- persisted tables against the SQLAlchemy rules' **Table Definitions**, and that rule file's
  sections on relationships, query methods and time handling: an untyped column, a table without
  its explicit name and arguments, a relationship without the loading strategy the rule sets, a
  timestamp that is not timezone-aware, and a query assembled as a string;
- data-holding classes against the Pydantic rules' **Model Design**, and that rule file's sections
  on model construction and on fields and serialization: a dataclass, named tuple or dynamically
  created model, a Protocol standing for data, a module-level helper that only constructs a model,
  a field declared through the field function only to describe it, and a field named in the
  provider's casing rather than aliased.

Remedy: the shape the cited section states, with every reader updated in the same change and a
migration through the repository's migration skill where the stored shape changes. Left alone: a
declaration a generator emits, corrected at its source; and a settings class, which the
configuration rules own.

## Reviewers

Reviewers are capped as `doctor-protocol`'s **Launches** sets; this doctor sets no lower cap. The
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
- Never retain a transitional nullable path.
- Every schema change lands through the canonical schema and the repository's migration skill. For
  index changes, also run the repository's database-specific schema checks and representative
  read-only query-plan validation when configured.
- An equivalence, ownership or workload question the evidence does not settle is recorded
  unresolved, and no change that depends on it is made.

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
