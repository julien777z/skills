# Schema Doctor Ledgers

The three ledgers a schema audit keeps beside the protocol's own, and what each records. `SKILL.md`'s
**Inventory** names this file where the ledgers are built.

## Field Ledger

One entry per field in the complete audit, recording:

- its domain and canonical declaration;
- its authoritative source and presence guarantee;
- every producer, validation or transformation step, serialized boundary, persistence target, and
  live read consumer;
- the required, nullable, omitted, defaulted, or presence-indistinguishable shape at each edge;
- the evidence supporting the disposition and any unresolved edge.

## Model Ledger

One entry per contract model, recording:

- its authoritative owner, dependency direction, producers, and live consumers;
- the distinct lifecycle, authorization, disclosure, persistence, and wire guarantees it represents;
- overlapping models and fields, conversion layers, wrappers, aliases, enums, and intermediate
  representations serving the same concept;
- fields and models with no live consumer;
- the evidence for retaining, removing, merging, reshaping, or sharing it, plus any unresolved
  ownership or semantic distinction.

## Index Ledger

One entry per persisted table in scope, recording:

- the table's primary-key constraint or justified keyless design, any database-specific physical
  primary or clustered arrangement, and each unique, foreign-key-supporting, standalone, composite,
  partial, expression, and covering index the database and canonical schema actually define;
- its ordered keys, included values, predicate, uniqueness, access method, and owning constraint;
- every live query, join, ordering, grouping, pagination path, mutation, or referential action it
  serves;
- overlap with other indexes, expected read benefit, write and storage cost, and available query-plan
  or database-statistics evidence;
- the evidence for retaining, adding, reshaping, or removing it, plus any unresolved workload or
  selectivity question.
