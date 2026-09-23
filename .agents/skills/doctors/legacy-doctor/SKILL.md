---
name: legacy-doctor
description: "Find and remove code that tolerates a past the repository no longer has: fallbacks, compatibility branches, kept aliases, silent tolerance, and second implementations of one thing. Every finding is traced to the contract, producer, caller, or check that proves the tolerated past is gone. Use to audit backwards compatibility, fallbacks, defaults over a contract, or more than one way of doing one thing."
disable-model-invocation: true
---

# Legacy Doctor

Code that tolerates a past — a shape nothing produces, a name nothing calls by, a branch nothing
reaches, a failure nothing should survive — is the version the next reader extends. This doctor
finds each survival, proves the past it serves is gone, and removes it.

## Dependencies

- `doctor-protocol` — own the run.
- `pre-production` — the target contract is the authority for every removal, and a removal that
  changes behavior is a surfaced trade-off rather than a silent deletion.
- `code-simplify` — the merge rubric when two implementations collapse into one.

## Inventory

Discover the languages and source roots at runtime. Exclude generated code by the repository's own
markers, and exclude migration bodies and backfill packages, where reading two stored formats is
the job rather than a survival. Then enumerate the items below; the lens that owns each item says
what evidence it is traced to:

- every defaulted, coerced, or guarded read — an `or` with a literal, a lookup with a default,
  an attribute read with a default or an attribute probe on the repository's own type, a
  nullish or optional-chaining fallback, an `isinstance` or type-narrowing branch;
- every configuration field whose on or off branch selects a former behavior;
- every barrel, re-export, forwarding function, and name accepted under two spellings;
- every catch, suppress, suppression comment, type-ignore, rule disabled in tool configuration,
  and check whose failure a pipeline ignores, in repository-owned code and configuration;
- every wire-contract field kept for a former reader — a reserved number, a deprecated mark, a
  second field for one concept;
- every comment, docstring, constant, or message carrying a compatibility word — legacy,
  compat, fallback, deprecated, kept for, formerly, transitional, temporary, old format — as a
  search key that points at code. The prose itself belongs to `docs-doctor`, and an existing
  to-do note is never removed unprompted.

The measurement taken once before fan-out is the repository's configured lint and type checks
run over the scope with no changed-lines filter, so every reviewer reads one result for what
enforcement already reports and what suppressions hide from it. A pipeline that filters
diagnostics to lines a branch wrote never surfaces a surviving instance, so that result, not the
pipeline's, is the evidence.

## Lenses

Each lens states its defect shape, then the checks that find every instance of it, then its remedy
and what is left alone so a reviewer does not go hunting.

### Default Over Contract

A reader defaults, coerces, or guards a value the contract already supplies.

- every `or` with a literal, every nullish or logical-or fallback, and every lookup with a default:
  resolve the declaration of the value read — the model field and its optionality, the overload's
  return type, a default factory, the column's nullability, the query that fetched the row, the
  writer in the same module; a declaration that supplies the value makes the fallback a finding;
- every attribute read with a default and every attribute probe whose target is the repository's
  own type: the type's declaration; a declared attribute makes the probe a finding;
- every optional-chaining read on a value the client or contract types as present;
- every label or lookup map declared total over a union or an enum that is indexed with a
  fallback;
- every coercion of a value the same module writes in one shape.

The remedy is to read the contract; where the contract is what is wrong — a field that should stop
being optional — the fix is `schema-doctor`'s and is handed to it. Left alone: a third-party
payload whose field is genuinely optional; a value legitimately blank in the artifact produced; a
legitimate expected state of canonical data; a guard on a data-fetching library's loading slot; an
attribute probe used to investigate rather than shipped.

### Dual Path

Two paths for one operation kept alive together.

- every branch on input format or encoding — two shapes narrowed by type, a former encoding decoded
  beside the current one, a defensive-import or version branch: the producers of the value and
  whether any still produces the old shape;
- every configuration field whose on or off branch selects a former behavior (read each field's
  branches, and search the settings models for names carrying legacy, compat, accept, allow,
  fallback, old, transitional): every reader, every environment that can set it, and whether any
  producer still reaches the old side;
- every backend or implementation selected by environment;
- every value reachable under several names, settings fields filling each other included: each
  name's producers;
- every wire message carrying two fields for one concept — a packed string beside its structured
  form, a date beside a period, a name beside its parts — and every reserved or deprecated wire
  field: the readers on both sides of the boundary; a reader that falls back from one field to
  the other is the tell.

The remedy is the current path alone; a flag gating a former behavior goes with its branches once
the backfill that retires it has run, and until then is reported with that backfill. Left alone:
failover between live providers; a second algorithmic strategy that is not temporal; a
controlled-or-uncontrolled component primitive; a name a framework itself prescribes.

### Alias Kept

A name kept so old callers still resolve.

- every barrel and re-export: count live imports through each path, tests separately; two live
  paths to one symbol, or a path whose only importers are tests, is a finding;
- every function whose body is one call to another with the same arguments;
- every second name bound to one value at module scope;
- every route, field, or parameter accepted under two spellings;
- every exported type, helper, or constant with no consumer, and the client it served.

The remedy is one path, every importer moved in the same change, the alias deleted. Left alone:
one external name per field at a provider boundary; the explicit re-export form a language defines
for a package's own public surface, in a short list.

### Silent Tolerance

A failure that should surface is swallowed — in code, in tool configuration, or in a pipeline.

- every catch that returns a default, passes, or logs and continues, and every suppress: the
  exception's origin, the repository's own wiring or a third party; a broad catch is read against
  the measurement's result;
- every suppression comment and type-ignore in repository-owned code: what the measurement reports
  when it is removed;
- every rule switched off in tool configuration: count the instances of what it would report; zero
  instances makes the switch-off the vestige, and that is the finding;
- every pipeline step whose failure is ignored and every job switched off: the gate that reads its
  verdict; a gate that asks only whether the step ran, or no gate at all, is a finding;
- every filter that narrows a check to changed lines: the instances it hides, which this doctor
  reports.

The remedy is that the violation raises, the shape mismatch is fixed at its source, the suppression
goes, the check's verdict gates again, and the rule code the configuration lacks is the guard. Left
alone: a catch that compensates and re-raises unconditionally; a cancellation carve-out; a pattern
the repository's rules prescribe by name.

### Two Ways To Do One Thing

One question answered twice.

- for every helper in scope, search the repository for the same operation under another name or
  in another language — a formatter, a parser, a derivation, a guard: both sides named with their
  live callers;
- every hand-written check in a class or module that also carries an annotation, decorator, or
  validator performing the same check on a sibling: both named;
- every pair of enums or literal unions with overlapping members and a bridge or translation
  between them;
- the whole-file duplicate-code check's result from the measurement, read rather than repeated.

The remedy is one owner, per `code-simplify`'s merge rubric, and two vocabularies collapse to one.
Left alone: a generated mirror; a demonstrated dependency, domain, or contract boundary; two
contract models, which are `schema-doctor`'s.

### Dead Branch And Dead Entry

Something kept for a caller, a key, or a path that no longer exists.

- every parameter annotated as a union: list every caller with the static type it passes; a member
  no caller passes, with the arm that handles it, is the finding;
- every type-narrowing arm the same module's writer makes unreachable — Dual Path's when a
  producer outside the module could still supply the old shape, otherwise this lens's;
- every enum member nothing produces;
- every label map, switch, or branch keyed on field names, listed for the whole scope and each
  compared key by key with the message or model that produces the value; a key the producer does
  not carry is the finding;
- every build, trace, ignore, or external-package entry in every tool configuration file in scope,
  listed before any is judged: the directory, path, or dependency it names, checked against the
  tree and the manifests.

The remedy is that the branch and the widened type go, the test that only exercised the branch goes
with it, and the entry goes. Left alone: a branch a caller outside the audited scope still reaches;
an enum member a stored row or a third-party producer can still supply.

## Dispositions

- A tolerance that hides a wiring defect is a confirmed defect and is fixed in the run, whatever
  its size.
- Fix the reader or the writer, never both.
- Where a flag's retirement backfill has not run, its removal is a user decision naming the data
  still in the old shape.
- An unsupported historical record is never a finding and never receives a fallback.
- A finding a sibling doctor owns is handed to it by name and counted in the report, not fixed
  here.

The cross-cutting reviewer compares one shape across packages and languages — a helper
reimplemented in a sibling, a memoization written twice across apps, a status derivation written
three times with different casing — and traces every value defaulted in one package to its
producer in another. The final adversarial reviewer tries to reach each removed branch and each
deleted alias from a live caller, re-checks every retained default against its declared
contract, and confirms no proposed guard asserts the absence of a retired implementation.

## Report Additions

- per lens, findings by package and by language;
- each flag gating a former behavior, with its readers, the backfill that retires it, and
  whether the old side is still reachable;
- each alias removed, with the importers moved;
- each duplicate pair and its surviving owner;
- each suppression removed and the rule code proposed as its guard;
- each check whose verdict gates again;
- each finding a sibling doctor owns, named with the doctor that rediscovers it;
- each conflict met between the repository's own rule files, handed to `guidance-doctor`.
