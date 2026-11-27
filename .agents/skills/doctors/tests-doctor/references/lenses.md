# Tests Doctor Lenses

Each lens states what it flags, the checks that find every instance, the remedy, and what is left
alone; `SKILL.md`'s **Lenses** table says which a partition reviewer reports and which the
cross-cutting reviewer owns. The checks name pytest shapes, and a suite on another runner reads
them as that runner's equivalent. A check that names a pre-pass list reads the candidates
`SKILL.md`'s **Pre-Pass** produced, and the reviewer confirms or rejects each one.

Lenses, in order: Align Structure With Siblings And Source, Audit Test Value And Repair Weak Proof,
Find Repeated Blocks With A Detector, Name Cases As Labels, Bring Every Suite Under Budget, Stay
Inside Third-Party Limits, Map Coverage By Test, Make Doubles Honest, Keep Construction Out Of Test
Modules, Keep Test Data In The Repository's Domain, Hold Suite Configuration To Its Rules.

## Align Structure With Siblings And Source

Establish the convention the majority of sibling suites follow for shared support — a fixture
package, a helper package, a case package, and a `conftest.py` reserved for lifecycle wiring —
then run every check below over the whole scope. Each item is a finding, and each names the
mechanical check that finds every instance rather than the first one noticed:

- a fixture defined at module level in a test module (grep `@pytest.fixture` in `test_*.py` and
  keep only definitions outside a class), or a domain fixture defined in `conftest.py`;
- a test module that mirrors no source module or package. The check is a table and the table is
  the report: one row per `test_<name>.py` with five columns — its path; the source directory it
  resolves to after the test root, the suite, and the classification are stripped; whether
  `<name>.py` exists there; whether a package `<name>/` exists there; whether the module's own
  directory is named for a source module beside it. Three noes make the row a finding, and nothing
  the module contains overturns that: a module that sweeps every route of a package, drives
  requests across several modules, or tests a concern rather than a file has still claimed a
  source module that does not exist. `routes/test_<concern>.py` with no
  `routes/<concern>.py` is that finding.
  It moves under the source module it covers, as a behavior module in a directory named for that
  module, or is named for the package it sweeps beside that package (`test_routes.py` next to
  `routes/`, for the sweep above);
- a source suite fragmented into tiny classes/files, or a file with multiple test classes: apply test-fixture's class/file boundary test, map cases to the substantial owning class, and merge small related classes before deciding whether independently maintained responsibilities justify separate files; keep one class per resulting file and preserve distinct proof;
- a test class whose name obscures the substantial responsibility it owns: name the class and its one-class module for that responsibility; a new label alone never justifies a small standalone class;
- a support `utils/` or `fixtures/` directory that holds `test_*.py` modules: distinguish support
  from source tests by tracing the source owner. Keep all utility tests in `utils/`, move support to
  the nearest fixture or utility package that does not hide that owner, and verify runner targets
  reach its files;
- shared support at a different depth from the siblings, or a helper module named for a catch-all;
- a module at a suite root whose subject is one source module inside a subpackage, when a
  directory in this suite carries that subpackage's name or the classification's sibling suites
  nest their modules by it (list every suite-root module in a table: its subject — the source
  module its imports name, or, for a test that drives a request, the route and service module
  that request reaches, read from the route table — that module's subpackage, whether this suite
  has a directory of that name, whether a sibling suite of the classification nests modules under
  it; report every row): a row with either yes is misplaced and belongs in that directory under
  the source module's own name; a flow that deliberately spans several source modules stays at the
  shared owner;
- a module named for one source file whose imports cover another (for each module, list the
  source modules it imports and compare them with the source file its name claims): it is
  misnamed, or it duplicates the module that already covers that source, and a test class name
  that appears in two modules is the duplicate;
- a test directory carrying the `test_` prefix;
- an import from a sibling suite, and a test or test-support module that imports setup, helpers or
  sample data from an executable script or command entrypoint (read the pre-pass's import list for
  every edge from a test root into an executable): the shared definition moves to its
  test-support owner with every consumer, as `writing-conventions`' **Code Layout** conventions say; a
  test importing a command to exercise that command stays;
- a symbol defined in an application package — a service, an app, or a library package outside its
  own test-utilities package — whose every consumer is under `tests/`, a test-utilities package, or
  a CI script using it for the same disposable-environment purpose the tests do (read the pre-pass's
  list of every module-level symbol in an application package with its consumers classified by
  root). What the tests do with it decides:
  - tests call it as support — setup, construction, cleanup, a disposable environment — so it is a
    test utility and moves to the shared test-utilities package the repository's layout holds, a
    test-support change under `SKILL.md`'s **Change Boundary** rather than an application change;
  - tests only exercise it as their subject, so it is dead application code under the
    `python-boundaries.md` rule: it is deleted together with the tests that exist only to exercise
    it, and is never moved into test utilities to keep it alive.

  Two shapes stay where they are, and the report names every symbol it leaves for one of them with
  that reason, so a reviewer does not go hunting: an import-time registration such as a SQLAlchemy
  `@compiles` hook, whose consumer is the import itself and whose call-site count says nothing; and
  a helper CI tooling or bootstrap runs to produce a repository artifact or bring an environment
  up, which is a machine consumer;
- a test directory no runner target reaches, an empty mirror package, an orphaned module, or a
  numbered duplicate file.

## Audit Test Value And Repair Weak Proof

Apply `test-fixture`'s **Test Value And Retention**, its dispositions included, to every test
declaration in scope, parameter rows that need different dispositions included, and record each
declaration's disposition, actual assertion and the contract it protects.

These sections of `test-fixture`'s rubric also run over every test tree in scope, never over a
diff, and each reports its result, an empty one included:

- **Literal Sweep**: every literal family in the test trees, classified as that section classifies
  one, so a literal a fixture, factory or production declaration owns is read from that owner and
  an unexplained duplicate goes;
- **Prefer Parametrized Cases**: every group of tests that differ only in their inputs and expected
  values;
- **Boundary Representations And Decision Matrices**: every decision the source makes over several
  inputs, against the cases that cover its boundaries.

Left alone: a literal the rubric lets stay local, and cases whose setup or assertions differ in
kind, which parametrizing would hide.

## Find Repeated Blocks With A Detector

Every other lens reads one module at a time or searches for one shape it can name, so a block copied
into two files — most of all into two different suites — survives all of them. Run a cross-file
duplication detector over every test tree in scope, at the tool's own default similarity rather than
a threshold picked to quiet it, and read what it reports:

```
<the repository's configured cross-file duplication detector, over every test tree>
```

Run the detector the repository's tooling already configures for its language.

**Every pair it reports is a finding, whether or not this run introduced it.** Nothing else in the
audit reports these, so the pairs that predate the run are precisely what the lens exists to catch,
and a count of what the branch added is not the measure: the measure is zero, less the pairs a
reviewer dismisses. A reviewer reading a pair may dismiss it with a recorded reason when the
matched lines are not one test or one piece of setup, such as two parametrize tables whose rows
look alike but cover different behaviors, so a run is never held open by text that only resembles
itself; the report lists each dismissed pair with its reason.

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

Re-run the detector after each cluster and keep going until it reports no pair that has not been
dismissed. A pair that survives
because the lines it matched are still identical says the owner was wrong or the call site still
spells the call over four lines; shorten the call or move the boundary. The threshold stays at the
tool's default and the check stays on, because a widened threshold hides every pair below it, real
copies included, where a dismissal names the one pair and why it is not a copy.

## Name Cases As Labels

Run `test-fixture`'s **Naming Checks** over every `def test_`, fixture, factory and test helper in
the scope and report each check's result, an empty result included. Every naming and structural
check in this section is a finding the run fixes. A check that reports its rows and leaves them
standing, or a row admitted as an observation, is the miss this doctor exists to close.

## Bring Every Suite Under Budget

For each suite over budget and each dominating case or fixture, establish the cause: fixture scope,
sleeps and polling, real network or filesystem work, a service booted per test, serial independent
work, unbounded data, or a genuinely slow application path. Order, wall-clock, randomness, network,
and shared-state dependence are findings in the same pass, because they are what makes a slow test
also a flaky one.

**Weigh every dominating case against what it proves.** A test earns its runtime by the failure it
would catch, so the question is what a reader loses if it goes, not whether it passes. One that
asserts little for a large share of the suite's wall time is folded into a case of the same
classification that is already paying that setup, or made cheaper where it stands. In a
pre-production repository folding and speeding up cases is ordinary rather than a last resort: a
suite nobody will wait for is coverage nobody runs. A case or module disproportionate under
`test-fixture`'s cost question that cannot be made cheap as that question allows is removed, as
that question says.

**No budget removes a test as redundant because a test of another classification makes the same
assertion.** A disproportionate cost is a separate reason, decided above. An
end-to-end test that an integration or unit test also reaches is not cut as redundant, however
far over budget its suite is and whatever stage the repository is in: its worth is that it runs the
real services, which the cheaper test does not. Being over budget, being pre-production, and the
cheaper test being "sufficient" are not reasons to cut it as redundant; bring the suite under budget
by making its cases cheaper, folding them into cases of the same classification, or removing a
disproportionate one as above.

Preserve every unique guarantee while doing it, except where a disproportionate case is removed
for its cost. Cutting a case whose assertion nothing else in its classification makes is otherwise a
coverage loss wearing a timing win, so name what each cut proved and where that fact now lives.

## Stay Inside Third-Party Limits

**A run that draws a limit refusal from a third party it calls is a defect in the suite** — an HTTP
429, a provider's throttling or quota code, a refusal to deliver to a destination sent to too often.
It is never a flake. Runs overlap by design: every pull request's CI and every local run share the
provider account and usually one test destination, so a suite that fits the limit only when it runs
alone fails whenever it does not, and a refusal in any log is the evidence.

The inventory's per-run calls to each provider, per account and per destination, are the evidence;
read them with the service logs against the limits the provider documents and the ones it answered
with. Then clear the refusal without losing a step the tests prove, taking these in order:

- fold tests of one classification that make the same real call, the way **Audit Test Value And
  Repair Weak Proof** folds duplicate proof;
- make the contract's real call once per run and share its outcome, the way a slow suite's setup is
  widened to the tests that share it;
- clear the state the repository keeps about earlier calls to the provider — a counter or cooldown
  keyed by account or destination — before the test, since state an earlier run left behind is
  shared state like any other; clearing it is not raising the limit;
- close what the test opened at the provider — cancel, expire, delete — so the next run starts from
  nothing;
- where the provider limits a destination across runs, give each run its own destination, or pace
  the call against the provider's own record of the last one before making it — waiting before the
  call is pacing, waiting after a refusal is a retry.

Skipping the test, mocking the provider in an end-to-end test, retrying after a refusal, sleeping
until green, raising a limit only for tests, and widening the assertion to accept the refusal are
not remedies: each keeps the collision and loses what the test proved. **No end-to-end test swaps
its real call for a double to make room for another's** — reading the outcome of the run's one real
call is not a double; one test kept real beside a second that now doubles the provider is still an
end-to-end test with its provider mocked; fold the two instead.

## Map Coverage By Test

Map entry points — routes, RPC methods, commands, jobs, event consumers — gateways and clients,
persistence and migrations, and user journeys to the tests that exercise them in each
classification, filling the map from the pre-pass's coverage by test rather than by hand where the
runner records it. A journey with no end-to-end test, a boundary crossing with no integration test, and a flow covered
only with its boundary mocked are gaps; a pure function covered only end-to-end is a unit gap.
Integration and end-to-end coverage outrank unit coverage for anything that crosses a boundary: a
unit test added for a flow whose integration or end-to-end path is untested is itself the gap.

## Make Doubles Honest

The inventory's table of doubles — target, owner, boundary, declared seam — is the evidence. Run
`test-fixture`'s **Auditing Existing Doubles** checks over it and report each check's result, an
empty result included, and name each double it leaves alone with its reason.

## Keep Construction Out Of Test Modules

Model-factory machinery belongs in the repository's established shared factory owner, including
when only one suite uses it. Fixture lifecycle wiring and scenario inputs stay in the suite.
Inject application model types where a shared import would invert dependencies.
Discover that owner from existing implementations and the repository's test-utilities package
before relocating anything.
Complete the ownership move as `scope-of-change`'s **Scope Follows The Defect, Not The Request**
says of a parallel copy: inspect every related implementation, move every consumer onto the one
owner, and flag a partial move even when the factory left behind was already there. Generic
lifecycle helpers retain their own owners; a shared word does not establish shared responsibility.

Run `test-fixture`'s **Factory Contents** checks over every factory module in the suite, with
the inventory and check rows that section requires in the report.

Every placement check below runs over the whole suite; each names the mechanical check that finds
every instance:

- a test-data factory class, such as a polyfactory `ModelFactory` or `SQLAlchemyFactory` subclass,
  anywhere under `tests/`, including
  `fixtures/`, `utils/`, and factory modules; enumerate direct and indirect factory subclasses,
  and move the machinery to the shared test-utilities package the repository's layout holds;
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

## Keep Test Data In The Repository's Domain

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

## Hold Suite Configuration To Its Rules

Suite and runner configuration that departs from `test-fixture`'s suites reference. Run that
reference section by section over every suite, runner configuration block and test job, and report
each section's result, an empty one included:

- **Suites And Classifications**: a smoke test that mocks its service, or carries a live-mode flag,
  an opt-in marker, a conditional skip or a fixture branch choosing between real and simulated
  execution; a classification folder out of place; a test directory no runner target selects;
- **Module Conventions**: a marker registered in code rather than in the manifest, an import inside
  a test function, a test or class without its one-line docstring;
- **Test Configuration**: a test environment value in workflow files or hard-coded in `conftest.py`
  rather than in the runner's configuration; runner configuration blocks that disagree on markers
  or environment; a run that does not treat warnings as errors, and every warning ignore, read
  against the one that section allows;
- **Time Budgets**: a job or local runner that runs a suite with no time limit, or one above the
  limit that section sets;
- **Skips**: every skip, xfail and commented-out test from the pre-pass's list. One is a finding
  when it states no condition, its condition can no longer occur, it covers a test that fails for a
  reason nobody recorded, or it stands in for a credential or service a suite is meant to require.

The remedy is the configuration the cited section states, made in the runner's own configuration
and the job that runs the suite; each warning the stricter setting then raises is fixed at its
cause; and a skipped test is repaired and unskipped, or deleted with the deletion evidence
`test-fixture`'s **Test Value And Retention** asks for. Left alone: a skip whose condition is a
platform or optional dependency the suite still meets in some supported run, with that run named;
and the one narrow warning ignore **Test Configuration** allows.
