# Schema Doctor Lenses

Contents: Nullability (Third-Party Contracts, Protobuf Presence), Convergence, Model Surplus,
Keys And Indexes, Declarations.

The criteria behind the **Lenses** table in `SKILL.md`: each lens states the defect shape, the
checks, the remedy and what is left alone.

## Nullability

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

### Third-Party Contracts

For data received from an external provider, first find official documentation, published schemas,
or specifications matching the integrated API and version. Then inspect the pinned SDK's models,
generated definitions, and runtime serialization contract. Prefer primary sources and record the
version or contract surface that makes the evidence applicable.

If provider documentation and the integrated SDK disagree, determine whether they describe different
versions or operations. Do not choose whichever source supports a desired conclusion. If the
guarantee remains uncertain, the external edge lacks the evidence **Dispositions** asks for. Continue auditing and correcting independently provable internal edges in the same domain.

A local provider-shaped model must represent what the provider can actually send. A narrower
repository model may require a provider field only after an owned validation or selection boundary
proves its presence.

### Protobuf Presence

Treat protobuf source and descriptors as canonical contract evidence. Inspect field presence,
default-value semantics, messages, optional fields, oneofs, wrappers, validation annotations, RPC
methods, conversion layers, and every producer and consumer.

Do not equate a scalar that decodes to a default value with a required field: some protobuf editions
and field kinds cannot distinguish omission from an explicitly supplied default. Express the intended
guarantee through the repository's canonical protobuf or boundary-validation mechanism. If the
current wire shape cannot express the invariant cleanly, use `pre-production` to choose the cleaner
breaking message shape rather than preserving ambiguity.

Edit protobuf source rather than generated output, update every producer and consumer the user controls, in any repository,
regenerate all owned targets, and run the repository-native generation and contract checks. Treat
the compatibility gate as `pre-production`'s **Target Contract** says.

## Convergence

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
  as a divergence, not just a different base type. Resolve each annotation through the validation
  library's own metadata, never by unwrapping the type by hand, which reports the library's own
  normalization as a divergence.
- **Divergent names** — one concept spelled two ways across models that otherwise overlap, such as
  an identifier named `id` on one and `<noun>_id` on another, or a composed name spelled `name` on
  one and `full_name` on another.
- **Within-model inconsistency** — sibling fields of the same concept validated differently inside
  one class. A field that loses its annotated type when it becomes required is the recurring form,
  because requiredness and normalization are independent and a requiredness change invites
  entangling them.

**Unifying a divergence is preferred over deriving around it.** A helper that intersects two models'
field sets, or subtracts one from the other, is a second mechanism papering over the first; the fix
is one declaration. A contract break to reach it is made as **Dispositions** says.

The retention test in **Model Surplus** applies to every unification.

Left alone: an implementation-only declaration that crosses no serialized or stored boundary, which
another doctor owns; and a pair whose difference **Model Surplus** retains.

## Model Surplus

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
recommendation does not erase domain meaning merely to reduce the declaration count. Equivalence or
ownership lacks evidence while such a distinction cannot be ruled out.

A provider difference is not one of those distinctions: a third-party provider's contract cannot
change and one the user owns can, so the repository's model moves toward what the provider sends,
and a second model beside it with a converter between them is not the answer. Take these in order;
the first that fits is the answer:

- **A difference in encoding is an annotation on the field** — a validator coercing the string the
  provider sends into the type the model holds, an alias naming its key, an alias path reaching its
  nested one. Two models that mirror each other field for field, joined by a conversion method, are
  an encoding difference standing as a model.
- **A difference in content earns a separate model**: the provider carries fields the repository
  deliberately does not, or a shape no annotation can express.
- **Adapting is not imitating.** The provider's encoding crosses into the model — its tokens, its
  date formats, its nesting, its keys. Its vocabulary does not: field names, casing, and domain terms
  stay the repository's own, reached through aliases.

**Third-Party Contracts** still holds: a local provider-shaped model must represent what the
provider can actually send, and that constrains what the model may require.

## Keys And Indexes

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
change. A workload-dependent decision lacks evidence while the required plans or statistics are
unavailable; continue correcting structurally provable gaps such as a referential action that must
scan an unbounded referencing table. Apply each change through the canonical schema and
the repository's migration skill, including its data safety, lock-risk, reversibility, and
validation requirements.

Left alone: an index whose worth depends on workload evidence the run cannot read, recorded
unresolved with the missing plan or statistic.

## Declarations

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
