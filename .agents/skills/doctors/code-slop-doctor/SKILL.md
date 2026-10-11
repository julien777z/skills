---
name: code-slop-doctor
description: Strip the complexity a codebase does not need and the code a reviewer reads as generated slop — pass-through layers, one-case abstractions, duplicates, divergent siblings, legacy paths, tangled or padded code, and surplus migrations, build files, configuration names and dependencies. Use to deslop a repository or one of its phases, lenses or paths.
short_description: 'Remove unneeded layers, abstractions, duplicates, legacy paths, code that reads as slop, configuration names and dependencies across a repository.'
disable-model-invocation: true
---

# Code Slop Doctor

Every layer, abstraction, copy and branch a reader has to get through must earn its place by
something it does, and every line should read as a careful author wrote it; this doctor finds what
does nothing or makes a reader wince, and takes it out.

## Dependencies

- `doctor-protocol` — own the run.
- `pre-production` — the target contract is the authority for every removal; nothing is kept for an
  obsolete owned contract, and a removal that changes behavior is a surfaced trade-off. A doctor run
  sets its own scope, so `pre-production`'s incidental size budget does not apply to it.
- `code-simplify` — the ownership analysis that decides where shared code lives, and its **Reuse,
  Ownership And Deletions** rubric when two implementations collapse into one.
- `test-fixture` — the per-test checks the test phase runs.
- `defer-scope` — report a migration-test deferral record whose path no longer exists.

Also read, when the skill listing declares them and found by their descriptions, the repository's
database-migration skill, its test-runner skill, its checklist for adding a configuration value and
its deployment skill, and follow its packaging rules for each language it builds. Their rules govern
every correction in their areas and are cited here, never restated; the deployment skill's
read-only guidance is how a deployment's environment is read, and reading activates nothing else it
offers.

## Phases

The run works in five phases, in this order, and each phase is one batch:

1. **Application code** — services, apps, workers, shared packages and libraries.
2. **Frontend** — web and mobile apps, their components, hooks, stores, styles and API types.
3. **Migrations** — every migration chain, its registries, backfills and tooling.
4. **Build, configuration and dependencies** — container files, workflows, scripts, tool and root
   configuration, every place a configuration name is declared or read, manifests and lockfiles.
5. **Tests** — after the code they test has settled. A test an earlier phase's change breaks — one
   importing a moved path, one exercising only a removed layer — is repaired or deleted in that
   phase's batch under **Test Slop**'s remedy, so every batch passes; this phase audits the rest.

A phase the repository has nothing for is skipped and reported. A scope argument selects phases,
lenses, or paths; a run scoped to one lens or phase applies only that lens or phase.

## Inventory

Exclude generated code by the repository's own markers. Enumerate, per phase in scope, every item a
lens's checks name, and build these tables before judging anything:

- the deployables, grouped by kind — RPC server, HTTP app, worker, CLI, frontend app — with a
  **slot table** per kind: one row per structural slot (entrypoint, server or app construction,
  startup and shutdown lifecycle, health and readiness, configuration, middleware or interceptors,
  logging, dependency wiring, data fetching for a frontend) and one column per deployable naming
  the file and symbol that fills it, or `none`;
- every module with its public symbol count, and every catch-all module (`utils`, `helpers`,
  `common`, `misc`);
- every comment, constant or message carrying a compatibility word — legacy, compat, fallback,
  deprecated, kept for, formerly, transitional, temporary, old format — as a search key pointing at
  code, never removing an existing to-do note unprompted;
- per migration chain: its revisions, registries and registered backfills with the callable behind
  each hook, revisions sharing a name across chains, and which environments have applied which
  revisions, read from the real version table where reachable and treated as applied where not;
- a **configuration matrix**: every configuration name by every place it is declared or read — typed
  settings models with each field's type, default and required-ness, environment example files, test
  environment blocks, container, CI and deployment manifests, workspace and cloud-agent environment
  files, documentation, and every reader — application code, a library that reads the variable
  itself, a compose service, a workflow step, a front end — names only, never values. A deployment
  whose environment lives on a hosting platform is one column, read by name through the deployment
  skill; one that cannot be read is recorded unread, never empty. For every field whose default is
  absence, record whether its reader refuses it, branches on it, or passes it through;
- per language and project: every manifest and its sections, every lockfile, tools a workflow
  installs outside a manifest, first-party imports across source, tests, scripts and workflow
  helpers, and every tool invocation in CI, scripts and hooks.

The measurements taken once before fan-out: the repository's configured lint and type checks over
the scope with no changed-lines filter; its cross-file duplication detector over each phase's trees
at the tool's default similarity; the chain replay and drift check its migration tooling defines;
and each deployment's configuration column, read by name once.

## Lenses

Each lens states its defect shape, the checks that find every instance, the remedy, and what is left
alone so a reviewer does not go hunting. Every lens applies in every phase, read in that phase's
language; **Migration Chain** belongs to the migrations phase, **Build And Root**, **Configuration
Drift** and **Dependency Drift** to the build phase, and **Test Slop** to the test phase.

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
dependency, domain or contract boundary; two contract models, which are `schema-doctor`'s.

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
implementation becomes the shared one under `code-simplify`'s **Reuse, Ownership And Deletions**.
Left alone: a slot whose difference a contract requires, with the contract named.

### Scattered Structure

Code spread over more files and folders than its responsibilities need.

- every module with one or two small public symbols whose siblings would hold them;
- every pair of modules or folders answering the same question, and every concern split across
  several folders;
- every catch-all module mixing unrelated owners, and every `lib`/`utils`-style pair with no rule
  for what goes where;
- every file or folder whose name says something other than what it holds;
- every declaration list ordered by when its entries were added rather than by what they describe
  — the fields of a message or model, an enum's members, a configuration's keys — so one concept's
  entries sit apart, and every owned wire contract whose field numbers record that history.

The remedy is restructuring, done without hesitation: merge modules of similar scope into one,
collapse one-symbol modules into their owner, split a catch-all by owner, move code to where its
consumers expect it, rename files and folders for what they hold, and regroup each declaration list
by concept, renumbering an owned wire contract's fields to match — every importer, producer and
consumer updated and every generated target regenerated in the same change, no re-export left
behind. Left alone: a module boundary a framework prescribes, a package boundary a build or
distribution artifact needs.

### Repeated Literal

One meaning spelled out many times.

- count every class-name or style string literal across the components in scope — extract each
  `className`, `class`, style-token or `cn(...)` argument string and tally identical values — and
  report every value that appears in three or more places with its count and locations;
- every error-to-message conversion written inline beside a helper that does it; every port, host or
  URL declared in more than one place; every message template spelled out at more than one site;
  every list restating an enum's members.

The remedy is one owned definition — a component or style token, the existing helper, one
configuration source, the enum itself — and every site reading it.

### Reads As Slop

Code a reviewer recognizes as generated: correct, and still a shape no careful author writes. The
test is the reader's: would someone opening this file wince? Every check below makes that test
concrete, and a shape the test catches that no check names is still a finding.

- **Tangled control flow** — nesting three or more levels deep; nested loops that a lookup map, a
  set or one pass replaces; an if/else ladder that a table, a match or early returns flatten; a
  boolean parameter that switches a function between two behaviors.
- **Narrating comments and docs** — a comment restating the line below it; a docstring repeating
  the signature; banner or section-divider comments; a comment explaining what a better name would
  show.
- **Ceremony** — a temporary assigned and returned on the next line; a branch returning `True` or
  `False` to restate its own condition; comparing to `True`, `False` or `None` with `==`; a
  hand-written loop that a comprehension, builtin or standard-library call already does; a helper
  re-implementing the standard library.
- **Defensive noise** — a try/except around code that cannot raise what it catches; catch, log and
  re-raise repeated at each layer.
- **Placeholder names** — `data`, `result`, `temp`, `info`, `helper`, `manager` or `handler` naming
  something specific; `_new`, `_v2`, `_final` or `_fixed` suffixes; a name saying how rather than
  what.
- **Padding** — a function past about sixty lines doing several separable phases; log lines
  narrating normal flow; emoji or exclamation in comments and logs; a to-do placeholder in shipped
  code.

The remedy is the plain shape a careful author writes: flatten, look up, return early, inline,
delete the comment and rename instead, split the function at its phases. Behavior stays exactly as
it was, and the repository's tests prove it before and after; a shape no test covers gets one
first. Left alone: a nested loop over small fixed sets; a comment recording a third-party quirk or
a reason the code cannot show; a long function whose phases share state a split would have to
pass around.

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
- **Survivorship** — every revision meets the migration skill's **Authoring Rules** for a
  destructive operation's policy entry and a data-reading migration's preparation hook, and its
  **What A Change Owes The Rows It Breaks** and **Stored-Format Transitions**; verify and reverse
  hooks that resolve to unconditional success verify nothing; an exactness check the tests already
  enforce is verified to run, never re-implemented.
- **Parity** — replay from empty matches the current models; a model change without a revision, a
  revision changing what no model declares, and a historical revision importing a current model are
  each a finding.
- **Placement** — revision code, backfill packages and temporary tables where the migration skill's
  **Migration Support Packages** and **Temporary Backfill Tables** place them; a value list a
  revision repeats is read from the migration package's own declaration where one holds it, and a
  historical revision never imports a current application model to get it.
- **Environment and CI** — per-chain environment modules differ only in the service they name; no
  hand-maintained path filter or table beside the manifest that derives it; every documented
  migration command exists.
- **Tests** — lifecycle wiring only in the shared test setup; fixtures and helpers where the
  migration skill's **Where A Revision's Test Scaffolding Lives** puts them; a revision-to-test
  pairing rule the repository states holds; a migration-test deferral record pointing at a path that
  no longer exists is reported to `defer-scope`.
- **History** — the migration skill's **Applied Is What Makes History** decides whether a revision
  is corrected in place or by stacking; a create-then-rename across unapplied revisions collapses; a
  merge-of-main revision carrying unrelated operations is split or rebaselined; a hand edit to a
  generated revision is stated in the change.
- **Tooling** — each piece of repository tooling around the migration library is weighed against
  what the library already does and what its extension points can do: a rewriter, renderer or
  post-processing pass is a finding when it restates the library's own output, or when the library's
  generation hooks — a render hook, a revision-directive hook, a custom template — can emit the same
  result as the revision is written. Read those hooks' documentation and the repository's current
  use of them before keeping the pass. A runner that wraps the library's command with nothing added
  is a finding too.

The remedy is the one shape: re-pointed parents, regenerated headers and the shared helper in place
of per-revision idioms, each only where **Applied Is What Makes History** allows editing that
revision; the missing policy, hook or downgrade added; code moved to its owner, tooling the library
makes redundant deleted with its callers switched to the library, and the repository's migration
skill followed for every correction. Where project guidance says no environment keeps data, a chain
grown long is collapsed into one baseline revision.

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

### Configuration Drift

A configuration name that the matrix shows out of step:

- **Missing** — a field a settings model declares that an environment booting that model does not
  supply, test environment included, or a default its reader refuses while no deployment sets it;
- **Orphaned** — a name an example file, manifest or environment block supplies that no model
  declares and no reader reads;
- **Mismatched** — one name with different types, defaults, placeholder styles or required-ness
  across locations, or an override present in one sibling environment and absent from another that
  boots the same model;
- **Misdeclared** — one name declared on several models with the same type and default, or a name
  a process receives and reads that no model it owns declares;
- **Unused** — a field with no reader, or one whose default is absence that no deployment sets while
  its reader branches on it; tests are not readers, and a test block or local example file is not a
  setter;
- **Bypassed** — an environment read in application code outside the typed model.

The remedy: a missing value declared wherever its siblings are, with a placeholder in test and
example locations and no real value committed anywhere; an orphaned or unused name deleted with
every vestige — the example line, the manifest entry, the test placeholder, the doc sentence; a
mismatch reconciled toward the typed model's declaration, a per-environment override stating its
reason; one declaration the processes needing it share, on the shared base or on a model scoped to
the capability that the processes without it never load, and a subclass that deliberately narrows
the shared declaration saying so on the field rather than restating it; a bypassed read routed
through the typed model; and, where the repository can derive an example file or test block from the
models, that derivation proposed as the guard.

### Dependency Drift

Declared dependencies out of step with what the code imports and the checks invoke.

- every package no first-party module imports and no check invokes, including an audit tool never
  wired into a check;
- every import satisfied only transitively;
- one package pinned with different floors or ranges across manifests, or a shared floor below a
  sibling's;
- a lockfile older than its manifest, a lock entry the manifest no longer declares, or two
  lockfiles resolving overlapping sets from different floors;
- two libraries declared for one job, or a package the platform, framework or runtime provides.

The remedy: the unused declaration removed with its lock entries; an audit tool wired into an
existing check or removed; an undeclared import declared in the project that imports it; one range
chosen from actual usage, stated where it changes behavior; a lockfile regenerated only through the
package manager's own command; one library for one job, the one the rest of the repository uses.

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

- Restructuring is ordinary work here: merges, moves, renames, collapses and regroupings land with
  every importer updated in the same change and nothing left to resolve the old path. No finding is
  too small: one regrouped message or one renamed file is fixed like a merged package.
- **Breaking an owned contract to remove slop is ordinary work, never a question**, made as
  `pre-production`'s **Target Contract** says; a removal is never narrowed, shimmed or dropped to
  keep an owned shape stable.
- Data a removal leaves in the old shape — a flag whose retirement backfill has not run, a chain to
  collapse — follows `pre-production`'s **Product State** and **Target Contract** and the
  repository's database-migration skill, never a question.
- The user decides what `pre-production`'s **Trade-Offs Are Surfaced, Never Enforced** reserves
  for them. A contract a consumer outside the user's control speaks stays as it is and is reported,
  under its **Target Contract**.
- Fix the reader or the writer, never both. A tolerance that hides a wiring defect is a confirmed
  defect and is fixed. An unsupported historical record is never a finding and never receives a
  fallback.
- A migration correction follows the migration skill's **Applied Is What Makes History**, stacked
  when applied state cannot be established; a data-loss path with no recovery is a blocker to
  report.
- A configuration default its reader refuses is declared nowhere until the disagreement is settled:
  the reader is wrong when nothing that ships can use the value, the declaration and deployment are
  wrong when something can, and where the target contract does not show which, both fixes go to the
  user. A field nothing deployed sets takes one of three outcomes the plan names: a deployment
  should carry it, it is a local-development tool retained with the tool and the branch named in the
  ledger, or it is deleted with the branch its value selects.
- An even split between two sibling structures equally fit for the kind goes to the one leaving the
  fewest mechanisms and moving the fewest importers, stated in the pull request.
- A finding another doctor owns — documentation, a contract model, a deep test audit — is not fixed
  here; the report names it with that doctor.

The cross-cutting reviewer compares each kind's slot table across its deployables, one shape across
packages, apps and languages, and every value defaulted in one package against its producer in
another; compares migration chains and registries with each other; reads each deployment column
against the settings model its process loads, one name declared on two models, and the locations
each checklist, manifest and example file names against the configuration matrix; and compares
manifests for one package pinned differently across projects or languages and a check one project
runs that its sibling does not. The final adversarial reviewer tries to reach each removed layer,
branch and alias from a live caller, confirms no import of a moved or renamed module still points at
its old path, replays every chain the run touched, confirms a stacked migration correction did not
narrow the approved downgrade or survivorship coverage, challenges every revision kept as applied
without version-table evidence, confirms each removed configuration name and package has no
surviving reader or importer, re-traces every retained package to an importer or an invocation,
re-derives the matrix for every retained mismatch, re-reads the deployment columns for every field
kept as a local-development tool, confirms each regenerated lockfile resolves its constraints, and
confirms that the repository's tests pass on each batch.

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
- the configuration matrix with every changed cell, and each deployment column read or unread with
  the reason; the readers traced for each removal; for every field no deployment sets, its outcome;
- per manifest: declarations removed, added and re-ranged; each lockfile regenerated with its
  command; audit tools wired in or removed;
- each shape **Reads As Slop** rewrote, by check, with the test proving its behavior unchanged;
- each test removed or repaired with the layer it exercised;
- each finding another doctor owns, named with that doctor.
