---
name: code-slop-doctor
description: Strip the complexity a codebase does not need — layers that only forward, abstractions with one case, duplicate models and types, siblings built in different shapes, scattered or tiny modules, code kept for a past the repository no longer has, migration chains and tooling grown past their job, and build, CI and root files nobody needs. It restructures freely, merging, moving and renaming modules, and works through application code, frontend, migrations, build and repository root, then tests. Use to deslop a repository or one of its phases, lenses or paths.
short_description: 'Remove unneeded layers, abstractions, duplicates, divergent structure and legacy paths across a repository.'
disable-model-invocation: true
---

# Code Slop Doctor

Every layer, abstraction, copy and branch a reader has to get through must earn its place by
something it does; this doctor finds the ones that do nothing and takes them out.

## Dependencies

- `doctor-protocol` — own the run.
- `pre-production` — the target contract is the authority for every removal; nothing is kept for an
  obsolete owned contract, and a removal that changes behavior is a surfaced trade-off. A doctor run
  sets its own scope, so `pre-production`'s incidental size budget does not apply to it.
- `code-simplify` — the ownership analysis that decides where shared code lives, and the merge rubric
  when two implementations collapse into one.
- `test-fixture` — the per-test checks the test phase runs.
- `defer-scope` — report a migration-test deferral record whose path no longer exists.

Also read the repository's database-migration skill and its test-runner skill when the skill listing
declares them, found by their descriptions. Their authoring, survivorship, history, locking and
validation rules govern every correction in their areas and are never restated here.

## Phases

The run works in five phases, in this order, and each phase is one batch:

1. **Application code** — services, apps, workers, shared packages and libraries.
2. **Frontend** — web and mobile apps, their components, hooks, stores, styles and API types.
3. **Migrations** — every migration chain, its registries, backfills and tooling.
4. **Build, CI and repository root** — container files, workflows, scripts, tool configuration and
   root files.
5. **Tests** — after the code they test has settled, because removing a layer removes or moves the
   tests that only exercised it.

A phase the repository has nothing for is skipped and reported. A scope argument selects phases,
lenses, or paths; a run scoped to one lens or phase applies only that lens or phase.

## Inventory

Discover languages, source roots, deployables, generators and tools at runtime, and exclude
generated code by the repository's own markers. Then enumerate, per phase in scope:

- every function, method, class, component and hook whose body forwards to one call with the same
  or renamed arguments, and every barrel, re-export and second name bound to one value;
- every interface, Protocol, abstract base and base class with its implementations or subclasses;
  every factory with the products it builds; every configuration field, option or prop with the
  places that set it; every context, provider or store with its consumers;
- every data declaration — model, dataclass, record, TypedDict, TypeScript type or interface,
  validation schema — with its field set, and every generated contract source the repository
  produces (an OpenAPI or protobuf output, generated client types);
- the deployables, grouped by kind — RPC server, HTTP app, worker, CLI, frontend app — with a
  **slot table** per kind: one row per structural slot (entrypoint, server or app construction,
  startup and shutdown lifecycle, health and readiness, configuration, middleware or interceptors,
  logging, dependency wiring, data fetching for a frontend) and one column per deployable naming
  the file and symbol that fills it, or `none`;
- every module with its public symbol count, every catch-all module (`utils`, `helpers`, `common`,
  `misc`), and every pair of modules or folders whose names or symbols answer the same question;
- repeated literal clusters: class-name strings, message templates, error-to-message conversions,
  ports, hosts and URLs, and constant lists that restate an enum;
- every defaulted, coerced or guarded read; every configuration field whose branch selects a former
  behavior; every name accepted under two spellings; every catch, suppress, suppression comment,
  type-ignore, rule disabled in tool configuration and pipeline step whose failure is ignored; every
  wire field kept for a former reader; every comment, constant or message carrying a compatibility
  word — legacy, compat, fallback, deprecated, kept for, formerly, transitional, temporary, old
  format — as a search key pointing at code, never removing an existing to-do note unprompted;
- per migration chain: its revisions with identifier, parent, header, file name, body and the
  generator template behind them; the model metadata it must match; every registry or manifest
  naming revisions, and every registered backfill with the callable behind each hook in a table;
  revisions sharing a name across chains, paired; the shared mechanics, per-revision packages,
  runtime and environment modules; the migration tests; which environments have applied which
  revisions, read from the real version table where reachable and treated as applied where not; and
  the repository's own tooling around the migration library, with what each piece adds to it;
- every container file, workflow job with its steps, script with its callers, and root or tool
  configuration file with the tool that reads it.

The measurements taken once before fan-out: the repository's configured lint and type checks over
the scope with no changed-lines filter; its cross-file duplication detector over each phase's trees
at the tool's default similarity; and the chain replay and drift check its migration tooling
defines. A measurement that cannot be taken is recorded unmeasured with the reason.

## Lenses

Each lens states its defect shape, the checks that find every instance, the remedy, and what is
left alone so a reviewer does not go hunting. Every lens applies in every phase, read in that
phase's language; **Migration Chain** and **Build And Root** belong to their own phases, and
**Test Slop** to the test phase.

### Pass-Through Layer

A layer, wrapper or alias that only hands the call on.

- every function, method, component or hook whose body is one call that receives the caller's own
  parameters, unchanged or renamed, and adds no policy of its own — callers could make that call with
  what they already hold: count its callers;
- every module layer — a service over a gateway, a lib under a route, a hook over one library call —
  whose members all forward to the next layer down;
- every barrel and re-export: count live imports through each path, tests separately; two live paths
  to one symbol, or a path whose only importers are tests, is a finding;
- every second name bound to one value, and every route, field or parameter accepted under two
  spellings.

The remedy is that callers call the target, the layer and alias go, and every importer moves in the
same change. Left alone: a wrapper that adds policy — validation, error mapping, retries,
authorization, caching, translation at a provider boundary; a function that names a domain
operation by mapping a domain value onto the call below it; one external name per field at a
provider boundary; the explicit public-surface re-export a language defines for a package, in a
short list.

### Speculative Abstraction

Structure built for cases that never arrived.

- every interface, Protocol or abstract base with one implementation, used by one consumer, and
  never substituted in a test through its declared seam;
- every base class with one subclass, every generic with one instantiation, every factory or
  registry with one product;
- every configuration field, option or prop no caller sets or every caller sets the same way;
- every context, provider or store read by one consumer, and every value threaded through layers
  that never read it.

The remedy is the concrete thing: the implementation in place of the interface, the subclass folded
into its base, the factory replaced by the constructor, the option replaced by its one value, the
store replaced by local state or a prop. Left alone: an interface the application declares as a
test seam and tests use; a plugin point a configuration file or an external consumer fills.

### Duplicate Implementation

One question answered twice.

- every data declaration whose field set matches another's, or is a subset carried by hand rather
  than derived; every empty subclass that only renames a model; every hand-written type that mirrors
  a generated contract type;
- every hand-written validation — a model validator, a manual check, a parse function — that the
  validation library's own tools express: a constrained or annotated type, a field validator, a
  reusable annotated alias, a type adapter, a computed field, a discriminated union;
- for every helper in scope, the same operation under another name, in another package or in
  another language — a formatter, a parser, a derivation, a guard, a client construction, a cache
  key;
- every pair of enums or literal unions with overlapping members and a bridge between them;
- the duplication detector's result from the measurement, read pair by pair rather than repeated.

The remedy is one owner, placed by `code-simplify`'s ownership analysis — the shared package every
consumer reads where more than one deployable needs it — with the copies and the bridge deleted and
generated types used directly or derived from. Left alone: a generated mirror; a demonstrated
dependency, domain or contract boundary; a provider's boundary model where the provider's shape genuinely differs and `pre-production`'s third-party rule
keeps it; two contract models, which are `schema-doctor`'s.

### Divergent Siblings

Things of one kind built in different shapes.

- read each kind's slot table: a slot one deployable fills with a shared helper and another fills
  by hand, a slot filled differently in each, and a slot one fills and its siblings leave empty with
  no contract difference to explain it, are each a finding;
- sibling routes, pages and features: one data-fetching style, one folder layout, one way to
  submit, load and report errors per kind; a feature split across several places its siblings keep
  in one is a finding;
- copies of one module in two places that have drifted apart — providers, clients, configuration —
  compared line by line.

The remedy is one structure per kind: the shared shape lives in the shared package and each sibling
supplies only what differs, its name, port, servicers or routes. The slot's best existing
implementation becomes the shared one under `code-simplify`'s merge rubric. Left alone: a slot whose
difference a contract requires, with the contract named.

### Scattered Structure

Code spread over more files and folders than its responsibilities need.

- every module with one or two small public symbols whose siblings would hold them;
- every pair of modules or folders answering the same question, and every concern split across
  several folders;
- every catch-all module mixing unrelated owners, and every `lib`/`utils`-style pair with no rule
  for what goes where;
- every file or folder whose name says something other than what it holds.

The remedy is restructuring, done without hesitation: merge modules of similar scope into one,
collapse one-symbol modules into their owner, split a catch-all by owner, move code to where its
consumers expect it, and rename files and folders for what they hold — every importer updated in the
same change, no re-export left behind. Left alone: a module boundary a framework prescribes, a
package boundary a build or distribution artifact needs.

### Repeated Literal

One meaning spelled out many times.

- count every class-name or style string literal across the components in scope — extract each
  `className`, `class`, style-token or `cn(...)` argument string and tally identical values — and
  report every value that appears in three or more places with its count and locations;
- every error-to-message conversion written inline beside a helper that does it; every port, host
  or URL declared in more than one place; every list restating an enum's members.

The remedy is one owned definition — a component or style token, the existing helper, one
configuration source, the enum itself — and every site reading it.

### Tolerated Past

Code that tolerates a past the repository no longer has. Trace each finding to the contract,
producer, caller or check that proves the tolerated past is gone; without that proof it is not a
finding.

- **Default over contract** — every `or` with a literal, nullish fallback, lookup with a default,
  attribute read with a default or probe on the repository's own type, optional chain on a value
  typed present, total map indexed with a fallback, and coercion of a value the same module writes
  in one shape: the declaration of the value read; a declaration that supplies it makes the
  fallback a finding.
- **Dual path** — every branch on input format or encoding, defensive import or version branch;
  every configuration field selecting a former behavior; every backend selected by environment;
  every value reachable under several names; every wire message with two fields for one concept and
  every reserved or deprecated wire field: the producers and readers on both sides, and whether any
  still reaches the old side.
- **Silent tolerance** — every catch that returns a default, passes or logs and continues; every
  suppression comment and type-ignore, read against the measurement with it removed; every rule
  switched off in tool configuration with zero instances of what it reports; every pipeline step
  whose failure is ignored; every filter that narrows a check to changed lines.
- **Dead branch and dead entry** — every union member no caller passes and the arm handling it;
  every narrowing arm the module's own writer makes unreachable; every enum member nothing
  produces; every key a label map or switch holds that its producer does not carry; every build,
  trace, ignore or external-package entry in tool configuration naming a path or dependency that
  is gone; every exported type, helper or constant with no consumer, and the client it served.

The remedy is the current path alone: read the contract, raise the violation, fix the shape at its
source, delete the suppression and let the check's verdict gate again, delete the branch, the
widened type and the test that only exercised it. Left alone: a genuinely optional third-party
field; failover between live providers; a non-temporal second strategy; a catch that compensates
and re-raises; a cancellation carve-out; a pattern the repository's rules prescribe by name; a
member a stored row or a third-party producer can still supply; a branch a caller outside the
audited scope still reaches; a guard on a data-fetching library's loading slot; a component
primitive that works controlled or uncontrolled; a name a framework prescribes; and migration
bodies and backfills, where reading two stored formats is the job rather than a survival.

### Migration Chain

A chain, its registries and its tooling, held to one shape and no more machinery than the job.

- **Graph and references** — one head per chain on a linear path; every parent resolves; no merge
  revision joining a fork; file name, identifier and header agree; no placeholder identifier or
  fabricated timestamp; every registry names real revisions in chain order, with no boundary claimed
  twice.
- **Uniformity** — one header style and a generator template that emits it; no generator residue;
  no per-revision copy of a value a manifest carries; one idiom per operation through the shared
  helpers; a revision name describing the schema change.
- **Downgrade** — every upgrade step reversed in the right order; an empty downgrade only where the
  policy mechanism records the loss with recovery material; a downgrade a fraction of its upgrade's
  size is read.
- **Survivorship** — every revision carries a policy entry or a no-rows classification; verify and
  reverse hooks that resolve to unconditional success verify nothing; a row-reading migration has a
  preparation hook for eligible, ineligible and boundary rows; discarded values are converted or
  recoverable; stored-format transitions are tested in both directions; resumable rewrites
  recognise already-converted rows; an exactness check the tests already enforce is verified to
  run, never re-implemented.
- **Parity** — replay from empty matches the current models; a model change without a revision, a
  revision changing what no model declares, and a historical revision importing a current model are
  each a finding.
- **Placement** — revision-specific logic in its own package and shared mechanics in the shared one;
  a backfill module whose one consumer is its revision folds into that revision; a value list a
  revision repeats is read from the migration package's own declaration where one holds it, and a
  historical revision never imports a current application model to get it; finished one-time data
  fixes kept as code are gone; a temporary table is registered and cleaned up in one lifecycle.
- **Environment and CI** — per-chain environment modules differ only in the service they name; no
  hand-maintained path filter or table beside the manifest that derives it; every documented
  migration command exists.
- **Tests** — lifecycle wiring only in the shared test setup; revision-specific fixtures in the
  revision package; durable helpers name no table or column, and a schema-independent helper is not
  filed as revision-specific; a revision-to-test pairing rule the repository states holds; a
  migration-test deferral record pointing at a path that no longer exists is reported to
  `defer-scope`.
- **History** — an unapplied revision is corrected in place, an applied one only by stacking; a
  create-then-rename across unapplied revisions collapses; a merge-of-main revision carrying unrelated
  operations is split or rebaselined; a hand edit to a generated revision is stated in the change.
- **Tooling** — each piece of repository tooling around the migration library is weighed against
  what the library already does and what its extension points can do: a rewriter, renderer or
  post-processing pass is a finding when it restates the library's own output, or when the library's
  generation hooks — a render hook, a revision-directive hook, a custom template — can emit the same
  result as the revision is written. Read those hooks' documentation and the repository's current
  use of them before keeping the pass. A runner that wraps the library's command with nothing added
  is a finding too.

The remedy is the one shape: re-pointed parents and regenerated headers, the shared helper in place
of per-revision idioms, the missing policy, hook or downgrade added, code moved to its owner,
tooling the library makes redundant deleted with its callers switched to the library, and the
repository's migration skill followed for every correction. Where project guidance says no
environment keeps data, a chain grown long is collapsed into one baseline revision.

### Build And Root

Build, CI and root files carrying more than they need.

- every container file differing from a sibling only in a name, port or path: compare them line by
  line;
- every workflow job repeating another's setup steps, and every workflow pair that has drifted
  apart;
- every script with no caller and no documented use, and every pair of scripts doing one job;
- every root or tool configuration file no tool in use reads, every package script for an app that
  does not exist, every second deploy path beside the live one, and template residue for tools the
  repository does not use;
- every value — a port, a version, an image name — declared in more places than the tools need.

The remedy is one parameterized file, a shared composite action or reusable workflow, one script,
one source for each value, and deletion of what nothing reads. Left alone: a difference a
deployment target requires, with the target named.

### Test Slop

Tests that cost reading time and prove nothing, found after the code has settled.

- run `test-fixture`'s **Test Value And Retention**, **Naming Checks** and **Auditing Existing
  Doubles** over every test the earlier phases touched and every test module mirroring code they
  changed;
- every test that only exercised a layer, alias or branch the earlier phases removed;
- every test package with no tests, and every test module mirroring no source.

The remedy is `test-fixture`'s dispositions: repair, fold into the keeper, or delete with its
evidence, with coverage of a removed layer's behavior kept at the real boundary. Timing, suite
budgets, cross-suite layout and coverage maps are `tests-doctor`'s and are named, not run.

## Dispositions

- Restructuring is ordinary work here: merges, moves, renames and collapses land with every importer
  updated in the same change and nothing left to resolve the old path.
- Behavior is preserved. A removal that changes what a user, a stored row or an external consumer
  sees is a user decision, put with each consequence and the option that leaves the fewest
  mechanisms recommended.
- An owned contract changes with every consumer in the same run; a contract a consumer outside the
  user's control speaks is a user decision.
- Fix the reader or the writer, never both. A tolerance that hides a wiring defect is a confirmed
  defect and is fixed. An unsupported historical record is never a finding and never receives a
  fallback. Where a flag's retirement backfill has not run, its removal is a user
  decision naming the data still in the old shape.
- A migration correction is made in place or stacked according to applied state, stacked when that
  state cannot be established; a data-loss path with no recovery is a blocker to report. Collapsing
  a chain is a user decision wherever any environment keeps data.
- An even split between two sibling structures equally fit for the kind is a user decision.
- A finding another doctor owns — a dependency, a configuration name, documentation, a contract
  model, a deep test audit — is not fixed here; the report names it with that doctor.

The cross-cutting reviewer compares each kind's slot table across its deployables, one shape across
packages, apps and languages, and every value defaulted in one package against its producer in
another; and compares migration chains and registries with each other. The final adversarial
reviewer tries to reach each removed layer, branch and alias from a live caller, confirms no import
of a moved or renamed module still points at its old path, replays every chain the run touched,
confirms a stacked migration correction did not narrow the approved downgrade or survivorship
coverage, challenges every revision kept as applied without version-table evidence, and confirms
that the repository's tests pass on each batch with behavior unchanged.

## Delivery

Merged batches, one per phase, each checkpoint named in the approved plan.

## Report Additions

- per phase and lens: findings and dispositions by package and language;
- each kind's slot table before and after;
- each module merged, moved, renamed, collapsed or split, with its importers moved;
- each layer, abstraction and alias removed, with its callers;
- each duplicate and its surviving owner;
- each flag gating a former behavior, its readers and retiring backfill; each suppression removed
  and the rule code proposed as its guard; each check whose verdict gates again;
- per migration chain: heads, revisions checked by lens, corrections, policy coverage before and
  after, and the evidence for applied state;
- each build, CI and root file consolidated or deleted;
- each test removed or repaired with the layer it exercised;
- each finding another doctor owns, named with that doctor.
