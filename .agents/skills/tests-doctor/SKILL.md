---
name: tests-doctor
description: Audit and correct a test suite for consistency, redundancy, naming, runtime, coverage by test, and determinism, preferring fewer higher-quality tests. It aligns every suite with its siblings and the source tree, folds same-shape tests into parametrized cases, times every suite against its budget, maps coverage by test with integration and end-to-end outranking unit, and moves construction out of test modules. Invoke as /tests-doctor to review, clean up, speed up, de-duplicate, rebalance, or find gaps in tests.
disable-model-invocation: true
---

# Tests Doctor

Bring every suite to the shape its siblings share, keep only the tests that prove something, name
them as labels, run them within budget, and cover every flow with the test that proves it.

## Dependencies

- `doctor-protocol` — own the run.
- `test-fixture` — the standard every added or rewritten test meets: canonical data, source
  mirroring, parametrization, the name budget, construction outside tests, and the mutation proof.

Also read the repository's test-runner skill when the skill listing declares one, found by its
description rather than assumed by name. Its locking, service, and pacing rules hold for every run
this doctor makes and are never restated here.

## Inventory

Discover at runtime: source roots and test roots; the groupings the runner distinguishes; each suite,
the ownership boundary it belongs to, and the source it mirrors; where each suite keeps fixtures,
factories, helpers, and shared cases; markers, skip and xfail marks, and commented-out tests; the
runner's targets and the CI jobs that run tests; every double — each `patch`, `patch.object`, and
`monkeypatch.setattr` target and each `Mock`, `AsyncMock`, and `MagicMock` construction — with the
owner of its target, whether the real implementation crosses a process boundary, and the seam the
application declares for that dependency when one exists; and any configured budget, whether a
runner timeout, a CI limit, or a documented target.

The measurement taken once before fan-out is the timing of every runner target through the
runner's own per-test and per-fixture duration reporting, serialized as the runner requires. Add
instrumentation only when the runner cannot report durations, and keep it only when the plan adopts
it. Record wall time per suite and the slowest cases and fixtures. A suite that cannot run locally
is recorded unmeasured with its CI duration when one is available.

The budget is what the repository configures. Absent one, a suite finishes within five minutes of
wall time, and no single case takes more than a small fraction of that.

**The budget binds the run, and a breach is never an end state.** A suite measured over it is worked
until it is under, by the dispositions below — the run is not finished while one stands. Reporting a
breach, recording it, or carrying it into the plan as an observation is the failure this paragraph
exists to prevent: the measurement was taken on day one and the number was already known, so a run
that delivers with the same number has spent the measurement on nothing. Where the work genuinely
cannot land in this run, that is the user's call to make in the current request, with the number and
the cause in front of them; it is never the run's to assume.

**Read setup against assertion before reading any single case.** Sum the per-test call durations and
compare that with the suite's wall time: where the difference is large, the suite's cost is fixture
setup, and the slowest case is a symptom rather than the cause. A per-test fixture that builds a
client, an organization, a persisted aggregate, or an authenticated session is the usual driver, and
it is invisible in a ranking of test bodies. Report both totals per suite.

## Partition The Reviewers

One domain reviewer per suite family — each application, service, and package suite, and each
cross-boundary group such as end-to-end, migration, script, or front-end as its own slice — applies
the redundancy, naming, runtime, doubles, and construction lenses to its slice. The cross-cutting
reviewer owns the layout and coverage lenses and the duplicates across suites, because those are
visible only across slices, and compares the doubles table across suites, since a seam one suite
uses and its sibling patches around is visible only there. A narrow scope gets two independent
passes.

The final adversarial reviewer re-times every suite the run cut or reduced against the reported
numbers, re-checks each merged parametrization and folded assertion for a fact that was dropped,
confirms each retained skip or xfail still has a live condition, and challenges every coverage gap
the run left open.

## Lenses

### Align Structure With Siblings And Source

Establish the convention the majority of sibling suites follow for shared support — a fixture
package, a helper package, a case package, and a `conftest.py` reserved for lifecycle wiring —
then run every check below over the whole scope. Each item is a finding, and each names the
mechanical check that finds every instance rather than the first one noticed:

- a fixture defined at module level in a test module (grep `@pytest.fixture` in `test_*.py` and
  keep only definitions outside a class), or a domain fixture defined in `conftest.py`;
- a test module that mirrors no source module or package. The check is a table and the table is
  the report: one row per `test_<name>.py` with five columns — its path; the source directory it
  resolves to after the test root, the suite, and the tier are stripped; whether `<name>.py` exists
  there; whether a package `<name>/` exists there; whether the module's own directory is named for a
  source module beside it. Three noes make the row a finding, and nothing the module contains
  overturns that: a module that sweeps every route of a package, drives requests across several
  modules, or tests a concern rather than a file has still claimed a source module that does not
  exist. `routes/test_pagination_bounds.py` with no `routes/pagination_bounds.py` is that finding.
  It moves under the source module it covers, as a behaviour module in a directory named for that
  module, or is named for the package it sweeps beside that package (`test_routes.py` next to
  `routes/`, for the sweep above);
- a module holding more than one test class (count `class Test` per module; report every module
  with its count): a second class is a second subject, and the module becomes a directory named for
  the source module holding one behaviour module per class;
- a test class not named for its module (for every module, compare its class name with `Test`
  followed by the module stem in CamelCase; report every mismatch): the class is renamed for the
  module, and a name narrower than the module because the module holds a second subject is the
  class-count finding above;
- a support `utils/` or `fixtures/` directory that holds `test_*.py` modules: distinguish support
  from source tests by tracing the source owner. Keep all utility tests in `utils/`, move support to
  the nearest fixture or utility package that does not hide that owner, and verify runner targets
  reach its files;
- shared support at a different depth from the siblings, or a helper module named for a catch-all;
- a module at a suite root whose subject is one source module inside a subpackage, when a
  directory in this suite carries that subpackage's name or the tier's sibling suites nest their
  modules by it (list every suite-root module in a table: its subject — the source module its
  imports name, or, for a test that drives a request, the route and service module that request
  reaches, read from the route table — that module's subpackage, whether this suite has a
  directory of that name, whether a sibling suite of the tier nests modules under it; report every
  row): a row with either yes is misplaced and belongs in that directory under the source module's
  own name; a flow that deliberately spans several source modules stays at the shared owner;
- a module named for one source file whose imports cover another (for each module, list the
  source modules it imports and compare them with the source file its name claims): it is
  misnamed, or it duplicates the module that already covers that source, and a test class name
  that appears in two modules is the duplicate;
- a test directory carrying the `test_` prefix;
- an import from a sibling suite;
- a symbol defined in an application package — a service, an app, or a library package outside its
  own test-utilities package — whose every consumer is under `tests/`, a test-utilities package, or
  a CI script using it for the same disposable-environment purpose the tests do (for every
  module-level `def` and `class` the scope adds or touches, grep the symbol across the repository
  and classify each hit's root): it is a test utility and moves to the shared test-utilities owner
  project guidance names, a test-support change under **Change Boundary** rather than an
  application change. Two shapes stay where they are, and the report names every symbol it leaves
  for one of them with that reason, so a reviewer does not go hunting: an import-time registration
  such as a SQLAlchemy `@compiles` hook, whose consumer is the import itself and whose call-site
  count says nothing; and a helper CI tooling or bootstrap runs to produce a repository artefact or
  bring an environment up, which is a machine consumer;
- a test directory no runner target reaches, an empty mirror package, an orphaned module, or a
  numbered duplicate file;
- runner configuration blocks that disagree on markers or environment.

### Remove Redundancy And Weak Assertions

Tests with the same setup, flow, and assertions that differ only in inputs become one parametrized
case with ids. A new fact about a scenario an existing test already exercises is an extra assertion
on that test, renamed when the name no longer fits, never a new test. A test that asserts nothing,
asserts the double's own input, computes its expected value with the code under test, or exercises
only the framework is deleted or given a real expectation. A lower-level test replaying what a
higher-level test proves through the real boundary keeps only the branch the flow cannot reach. A skip, xfail,
or commented-out test whose condition no longer holds is revived or deleted. Removals count as
wins: fewer, stronger tests beat more tests.

### Find Repeated Blocks With A Detector

Every other lens reads one module at a time or searches for one shape it can name, so a block copied
into two files — most of all into two different suites — survives all of them. Run a cross-file
duplication detector over every test tree in scope, at the tool's own default similarity rather than
a threshold picked to quiet it, and read what it reports:

```
<the repository's configured cross-file duplication detector, over every test tree>
```

Run the detector the repository's tooling already configures for its language; the checks below
name pytest shapes, and a suite on another runner reads them as that runner's equivalent.

**Every pair it reports is a finding, whether or not this run introduced it.** Nothing else in the
audit reports these, so the pairs that predate the run are precisely what the lens exists to catch,
and a count of what the branch added is not the measure: the measure is zero.

Name the owner each block moves to before editing: repeated setup goes to the fixture package of the
suite that reads it, a repeated call to that suite's utility package, repeated model construction to
the repository's established shared factory owner, and a repeated list of field or column names
derives from the model or table that declares them. Where two callers differ only in a value, the
owner takes it as a parameter rather than growing a second copy.

**The report names the detector and what it returned, whatever it returned.** Reading the modules,
or grepping for a shape somebody already suspects, is not this lens and does not stand in for it: the
pairs it exists to catch are the ones nobody suspects, which is why nothing else in the audit reports
them. Where the detector cannot be run at all, say that and say why, rather than presenting an
inspection as its result.

Re-run the detector after each cluster and keep going until it reports none. A pair that survives
because the lines it matched are still identical says the owner was wrong or the call site still
spells the call over four lines; shorten the call or move the boundary, and never settle it by
widening the tool's threshold or disabling the check.

### Name Cases As Labels

A name identifies the case; the docstring carries the behavior sentence. Run every check below
over every `def test_` in the scope and report each result, an empty result included; each is a
finding at any length, and each names the mechanical check that finds every instance:

- a name whose first word after `test_` is `a`, `an`, or `the` (regex `def test_(a|an|the)_` over
  every test module);
- a name past eight words (split on `_` and count);
- a numeric status token in a name (a `_`-delimited token that is a member of the runtime's HTTP
  status enumeration);
- a word restating a noun the enclosing class or module already states (tokenize the class name,
  stem singular and plural, intersect with the name's words).

Cut in the order `test-fixture` states: the article and connective prose first, then every noun
the class already states, then the numeric code. A name that clears all four checks is finished;
one that fails any is a finding whatever its length.

A fixture or factory is named for the domain role or state it provides, per `test-fixture`'s
naming standard. A name coined from an abstraction or an adjective — an `-less` word, a mechanism,
a synonym for the thing — where the concrete thing it provides or lacks would name it is a finding,
renamed for that thing.

A test class is named for its module and nothing else, so an article, a verb phrase, or a synonym
inside a class name (`TestEngagingAContractor` in `test_contractors.py`) is a finding renamed to the
module's name (`TestContractors`). A helper that builds a model in a suite's `utils/` or `fixtures/`
package is named `create_<shape>` (list every module-level `def` in those packages whose return type
is a model, with its name; report every row): a bare noun (`flag`), a mechanics prefix
(`stored_driver_license`), or a coinage (`flag_page`) is renamed `create_<shape>`, and the same shape
built under two names in two files or two suites is one name across all of them. Read names across
sibling files and sibling suites before settling one: a suite's vocabulary is its source's, and the
word the sibling suite already uses for the same shape wins over a new one.

Every naming and structural check in this section is a finding the run fixes. A check that reports its rows and leaves them
standing, or a row admitted as an observation, is the miss this doctor exists to close.

### Bring Every Suite Under Budget

For each suite over budget and each dominating case or fixture, establish the cause: fixture scope,
sleeps and polling, real network or filesystem work, a service booted per test, serial independent
work, unbounded data, or a genuinely slow application path. Order, wall-clock, randomness, network,
and shared-state dependence are findings in the same pass, because they are what makes a slow test
also a flaky one.

**Weigh every dominating case against what it proves.** A test earns its runtime by the failure it
would catch, so the question is what a reader loses if it goes, not whether it passes. One that
rebuilds an expensive world to assert something a cheaper test at another level already reaches, or
that asserts little for a large share of the suite's wall time, is cut, folded into a case that is
already paying that setup, or moved to the level where its setup is free. In a pre-production
repository that trade is ordinary rather than a last resort: a suite nobody will wait for is
coverage nobody runs.

Preserve every unique guarantee while doing it. Cutting a case whose assertion nothing else makes is
a coverage loss wearing a timing win, so name what each cut proved and where that fact now lives.

### Map Coverage By Test

Map entry points — routes, RPC methods, commands, jobs, event consumers — gateways and clients,
persistence and migrations, and user journeys to the tests that exercise them at each level. A
journey with no end-to-end test, a boundary crossing with no integration test, and a flow covered
only with its boundary mocked are gaps; a pure function covered only end-to-end is misplaced cost.
Integration and end-to-end coverage outrank unit coverage for anything that crosses a boundary: a
unit test added for a flow whose integration or end-to-end path is untested is itself the gap.

### Make Doubles Honest

The inventory's table of doubles — target, owner, boundary, declared seam — is the evidence. Run
every check below over it and report each check's result, an empty result included:

- a repository-owned callable patched whose real implementation is deterministic and in-process:
  it runs as itself, per `test-fixture`, and the fixture that arranges its input usually exists;
- a repository-owned persistence call patched — an ORM class method, a repository function, a
  service that reads rows — or a persistence method assigned onto a real row: `test-fixture`'s
  test rule applies, and a conflict is produced by the conflicting row;
- a double in place of a repository-owned object where a fixture, factory, or constructor exists:
  the real instance;
- the subject under test patched, a method patched on its class so every subclass sees it, or a
  guard the surface exists to enforce replaced by a pass-through: the real path with its input
  arranged;
- a patch one layer above the seam the application declares: moved to the seam;
- a provider override, fake, or configuration fixture the application or suite already declares
  while the test patches a module path instead: the seam is used, and a declared seam no test uses
  is reported;
- a configuration attribute patched inline in more than one test, or in two spellings across a
  suite: one fixture helper in the suite's fixture package, per `test-fixture`;
- a module whose doubles outnumber its `assert` statements, or whose only outcomes are
  `assert_called` or `assert_awaited` on its own doubles, an identity assertion against the value
  a double returned, or a string match on rendered SQL (count doubles and assertions per module
  and report the ratio): it proves wiring, not behavior, and is rewritten against the real path
  or cut;
- a fixture-package member that installs doubles of repository-owned code for every consumer: the
  finding is the fixture, and fixing it counts once for every module it serves;
- a suite whose autouse session fixture is a double: it is the root of every persistence patch
  beneath it, reported once as such, and its persistence-shaped modules move to the suite with the
  real database;
- a patch target that no longer binds where the consumer reads it, a literal where a fixture
  provides the value, and data shaped like a real person's.

Left alone, and named so a reviewer does not go hunting: the consuming module's binding of a
gateway function, the seam `test-fixture` names for a hop to another service; a third-party function
imported into a repository module and patched at that binding; a repository wrapper that is the
last hop before the HTTP client; a replacement that calls through to the real function after
arranging an interleaving the database would not produce on its own; a fault injected to prove
the surrounding write still commits; a fake that raises the library's real exception to simulate
an outage; a double container installed through the lifecycle override that carries real wire
messages; a private attribute of a third-party object; a settings module tested as its own
subject; a same-module symbol that constructs a third-party client.

### Keep Construction Out Of Test Modules

Model-factory machinery belongs in the repository's established shared factory owner, including
when only one suite uses it. Fixture lifecycle wiring and scenario inputs stay in the suite.
Inject application model types where a shared import would invert dependencies.
Discover that owner from existing implementations and project guidance before relocating anything.
Apply the general New Modules ownership-completion rule: inspect every related implementation and
consumer, and flag a partial move even when the factory left behind was already there. Generic
lifecycle helpers retain their own owners; a shared word does not establish shared responsibility.

Four checks read what a factory contains rather than where it lives. A provider is whatever fills
a field: a plain class attribute, a `Use(...)`, a `PostGenerated(...)`, or a classmethod named for
the field; a `PostGenerated` assignment is a provider like any other and takes its own inventory
row, never a footnote about the generator it wraps. Before any of
the four is judged, the report carries an inventory: one row per provider on every factory in the
module, subclasses included, with the columns factory, base, provider, and body — the body being
the one expression it is (a `return` line, or the value a `Use` or a `PostGenerated` wraps, the
docstring left out) or the word `multi` when it is longer. The four checks are read off that inventory, each as rows with
the columns check, factory, symbol, this side, other side, equal, and the report carries those rows
too. A row whose last column is yes is a finding, stated as a finding and never as an exception;
the reasons a reader reaches for to keep the copy are named under each check, and none of them is a
reason.

1. **Restated override** — every inventory row whose provider is a classmethod and whose name the
   factory's base also declares. This side: the subclass body. Other side: the base body.
   `return cls.address()` on the base and again on a subclass is the shape. Inside an inherited
   classmethod `cls` is already the subclass, so an equal row changes nothing but its annotation
   and goes. That the body delegates to another method, that the subclass defines the method it
   delegates to, and that the annotation or the docstring differ are each true of every instance
   of this shape; none keeps it.
2. **Restated default** — every inventory row on a factory whose `__use_defaults__` is true, and on
   no other. This side: the value the provider returns. Other side: the field's declared default,
   read from the model the factory builds — following the import when that model lives in a
   dependency — so an empty mapping meets an empty-mapping default factory and `None` meets a
   `None` default. An equal row repeats the model and goes.
3. **Repeated provider** — every provider name that two inventory rows on factories sharing a base
   carry with a one-expression body. Find those names with one search over the module for lines
   indented four spaces that begin `def ` or that assign a name (`name = `), attribute each hit to
   the class above it, carry that list in the report, and keep every name that appears under more
   than one sibling — the `def` hits as much as the assignments; a name kept this way is a row even
   when its body is a single `return` line, and the largest method on the class is not the place
   to look. This side: one sibling's expression with its faker instance,
   locale, and constants blanked. Other side: the other sibling's expression blanked the same way.
   A phone number built from a faker's number generator once with the default faker and once with
   a localized one is the shape. An equal row is one module-level generator taking the value that
   varied, bound on each factory with `Use`. That each copy names its own locale, country, or
   constant is the shape itself and not a justification: two expressions that differ only there
   are one generator, however deliberate the variation.
4. **Constant behind `Use`** — every inventory row whose body is `Use(callable, constant)`. This
   side: what the call returns. Other side: the constant. `Use(SomeEnum, SomeEnum.MEMBER)` is the
   usual shape, and an equal row is a plain class attribute holding the member.

Every placement check below runs over the whole suite; each names the mechanical check that finds
every instance:

- a `ModelFactory` or `SQLAlchemyFactory` subclass anywhere under `tests/`, including
  `fixtures/`, `utils/`, and factory modules; enumerate direct and indirect factory subclasses,
  and move the machinery to the shared test-utilities owner named by project guidance;
- model-generation functions, methods, or nested builders anywhere under the test tree, including
  `conftest.py`, fixture packages, and utilities: trace constructor calls and returned models, then
  apply `test-fixture`'s ownership dispositions to each implementation and its consumers; a clean
  factory-subclass search alone does not cover construction;
- a module-level function in a test module that builds a domain model, request, response,
  scenario, or options object, whatever it is called (list the module-level `def`s in every
  `test_*.py`);
- a test-only type, in a test module or in the fixture package, that mirrors a contract the
  application already declares (list every `TypedDict` and model the suite declares; for each,
  grep the application source for a class of the same name and for the same field set, and report
  the match or its absence): a match is the finding, and sibling suites carrying their own copies
  are more instances of it, never a convention that excuses it;
- the same inline aggregate construction repeated across tests;
- a random or hand-typed identity where a canonical fixture owns that identity, and a factory
  whose model carries a person's or organization's identity — an email, a name, credentials, an
  account at a third party (list every factory in a table: the model it builds, the fields that
  model declares, which of them a root fixture already owns, and whether the model names a person,
  an organization, or an account at a third party; report every row): a row whose fields a root
  fixture owns is a finding — the identity is read from the fixture, whatever field a test
  overrides and whatever the test asserts — and a row whose model names a person, an organization,
  or a third-party account is a second finding: the factory belongs in the shared test-utilities
  package, extended, never in one suite's module;
- a fixture that differs from a sibling fixture by one field or flag (list every fixture that
  inserts a row in a table: the table, the fields its payload sets; report every row): two rows for
  one table whose payloads differ by one field or flag are one fixture with a typed selector, per
  `test-fixture`, never a parallel fixture; the role each docstring claims is what the selector's
  value expresses, never a reason to keep two.

The permitted residue is a trivial predicate or formatter one module reads.

### Keep Test Data In The Repository's Domain

A suite speaks the vocabulary of the source it mirrors, or none. Its data, names, fixtures, and
scenarios draw on the nouns that source already uses — an application's tests are about the
businesses and people it serves, a library's tests about the shapes the library defines — and on
neutral placeholders where that source has no domain of its own. A consumer's table, schema, model,
or product name in a library's tests, the application's nouns in the tests of a generic package
beside it, and a setting the application does not serve invented for one test are all a domain the
source does not own leaking into its suite, and the tests then describe somebody else's system.

The check is mechanical and reported noun by noun: for each suite, list every domain noun it uses —
in identifiers, string values, fixture and scenario names, and the fixtures it imports — that the
source it mirrors never uses, and report each with the tests and fixtures that carry it. The same
leak has a dependency form: a generic package's suite that imports the application's packages, its
fixtures, or its test utilities depends on a system its source does not, and could not run were the
package extracted; list every such import beside the nouns. Left alone: the vocabulary of a third
party the source integrates with, a standard placeholder such as an example address, and a neutral
noun the suite's own fixtures invent.

## Dispositions

### Change Boundary

This doctor changes tests, test-only support, and test execution configuration. Classify an edit
by its purpose and runtime consumers, not its directory: a shared bootstrap or configuration edit
that changes application execution is an application change. Reading source to understand a test
does not authorize changing it.

**A suite's architecture is inside that boundary, whole.** How tests isolate from one another, how
state is seeded, shared and cleared, what scope the expensive fixtures hold, and how the application's
own sessions are bound during a test are test execution configuration, and rewriting them across an
entire suite is this doctor's ordinary work. The purpose of the run is a suite in good working
condition, and the slop that keeps one out of it is usually structural — a cleanup contract that
rebuilds the same world per test, a fixture every module reaches for at the wrong scope — so a run
that fixes every symptom and leaves the structure has not done the job.

Neither the number of modules a rewrite reaches nor the number of call sites naming a fixture is a
reason to hold it back, split it into a change of its own, or hand it to a later run. A fixture kept
under its existing name costs its callers nothing however many there are, and a rewrite that changes
the isolation model is verified the same way as any other edit here: the affected suites re-run
green, and the durations are re-taken against the same workload.

Application changes qualify only for the performance exception below. Application correctness
defects, configuration cleanup, missing injection seams, and structural refactoring are not
independent reasons to change application code. Report those findings with evidence without adding
their implementation to this doctor's plan. Do not weaken, skip, or delete tests to conceal them;
report an unresolved failure honestly and continue the remaining test work.

### Application Performance Exception

Before proposing an application change, establish all three conditions:

1. A repository-native suite exceeds its configured wall-time budget, or the five-minute default.
2. Profiling or repeated measurements attribute the overrun to an application path. First address
   test-side causes such as fixture setup, repeated startup, excessive data, and timing sleeps.
3. The focused application fix is necessary to bring that suite within budget, alone or alongside
   identified test fixes. An isolated 10 ms saving qualifies only when its measured cumulative cost
   satisfies these conditions; a faster microbenchmark or a suite already within budget does not.

Record the workload, baseline, budget, bottleneck evidence, expected suite-level improvement, and
correctness guarantees before adding a distinct performance entry to the remediation plan. Missing
measurements and differences within measurement noise leave the exception unproven. Approval of a
generated plan does not substitute for this evidence.

After implementation, repeat the same suite workload, verify its budget outcome and correctness,
and report the before/after evidence. The improvement must exceed measurement noise. Preserve every
unique coverage guarantee; never cut tests solely to achieve a timing target. A missed budget or
unverified improvement remains unresolved rather than being reported as a successful performance fix.

Reviewers check every application change against this exception at proposal and final review,
including changes introduced during conflict resolution. Temporary application mutations used to
prove tests may bypass the performance exception only while running the proof; restore every one
before delivery and verify that none enters the delivered diff.

### Findings

- A slow suite, in order: widen the scope of the fixtures that dominate it, so an expensive world is
  built once for the tests that share it rather than per test; cut or move the cases whose runtime
  is out of proportion to what they prove; fix the remaining test-side causes; admit a focused
  application fix only through the performance exception; parallelize where the runner and shared
  resources allow, never across a shared database or lock. Re-time after implementation against the
  same workload. A suite still over budget is unfinished work, not a line in the report: carry on
  with the next disposition, or put the remaining cause and its cost to the user in the current
  request.
- A redundant test merges into the survivor; an assertion nobody else makes is never dropped.
- A name any naming check reports — a leading article, more than eight words, a numeric status
  code, a restated class noun — is renamed to a label within `test-fixture`'s word budget; the
  condition the name lost moves into the docstring, and a rename that would leave fewer than two
  words takes a hand-chosen label rather than the mechanical residue.
- A layout finding moves to the pattern `test-fixture`'s ownership rules select; an even split
  between equally valid patterns is a user decision.
- A coverage gap is closed by the test that proves it, a misplaced test moves between suites, and
  the redundant lower copy is removed. Every added or rewritten test follows `test-fixture`,
  including its mutation proof per batch.
- A construction finding moves the construction to the suite's shared home and reads identities
  from the canonical fixtures. A factory-content finding deletes the override or the provider, or
  folds the repeated shape into one generator taking the value that varied; the model's default and
  the plain attribute already say the same thing.
- A test utility found in application code moves to the shared test-utilities owner with every
  consumer, in the same change.
- A foreign-domain finding rewrites the data in the mirrored source's own nouns where it has them
  and in neutral placeholders where it is a library with none; a fixture that introduced the noun
  is the finding, fixed once for every test it serves.
- A doubles finding runs the real code; one that needs the database follows the coverage
  disposition above and is counted there; a fault the real path cannot produce keeps its double at
  the declared seam, with the fault named in the ledger.

## Declared Outcome: The Slowest Tests Are Posted

**This run posts one comment on its pull request ranking the ten slowest tests and the ten slowest
fixtures, with each suite's wall time against the budget.** It is a declared outcome of the skill, so
invoking the skill authorizes that comment under the comment rules, and it is posted whether the run
brought every suite under budget or not.

The comment exists because a duration is the one finding with nowhere else to live. A pull request
body carries no measurements by rule, the diff cannot show a number, and a report in chat is gone by
the next session — so without this the run measures a breach on day one, delivers, and leaves nothing
a later reader can act on. Ranked in one place, the next run has its baseline and anyone deciding
what to cut can see what the time is being spent on.

Post it once, updating the same comment when a later push changes the numbers rather than adding a
second. Give it the measured durations and nothing else: no narration of what the run did about them,
which the body and the diff already carry.

## Report Additions

- per suite: wall time before and after against the budget, and unmeasured suites with the reason;
- per suite: the sum of test call durations against wall time, naming setup-dominated suites;
- each case cut or moved for disproportionate runtime, with what it proved and where that now lives;
- per suite: tests removed, parametrized, renamed, moved, and added;
- skip and xfail marks resolved;
- per suite, foreign domain nouns removed and the fixtures that carried them;
- the coverage map by test, with gaps closed and gaps recorded;
- determinism corrections; per suite, doubles of repository-owned code removed, moved to the suite
  with the real boundary, or retained with the fault they inject; and declared seams no test used
  before the run;
- each cut presented and the decision that authorized it.
