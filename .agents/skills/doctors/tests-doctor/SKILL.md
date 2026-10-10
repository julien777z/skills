---
name: tests-doctor
description: Audit and correct existing tests for contract value, redundancy, weak assertions, naming, runtime, third-party rate limits, coverage by test, and determinism. It aligns suites with their source owners, consolidates duplicate proof, preserves independent contracts, measures runtime, and repairs proven defects. Use to review, clean up, speed up, de-duplicate, or find gaps in tests.
short_description: 'Audit tests for contract value, redundant proof, weak assertions, runtime, provider rate limits, and determinism.'
disable-model-invocation: true
---

# Tests Doctor

Bring every suite to the shape its siblings share, repair or remove tests that prove nothing, name
them as labels, run them within budget, and cover each contract in every classification that can
reach it.

## Dependencies

- `doctor-protocol` — own the run.
- `test-fixture` — every per-test check this doctor runs — value and dispositions, naming, factory
  contents, doubles — and the standard every added or rewritten test meets for data, placement,
  doubles, and mutation proof.

Also read the repository's test-runner skill when the skill listing declares one, found by its
description rather than assumed by name. Its locking, service, and pacing rules hold for every run
this doctor makes and are never restated here.

## Inventory

Discover at runtime: source roots and test roots; the classifications the runner distinguishes; each suite,
the ownership boundary it belongs to, and the source it mirrors; where each suite keeps fixtures,
factories, helpers, and shared cases; markers, skip and xfail marks, and commented-out tests; the
runner's targets and the CI jobs that run tests; every double — each `patch`, `patch.object`, and
`monkeypatch.setattr` target and each `Mock`, `AsyncMock`, and `MagicMock` construction — with the
owner of its target, whether the real implementation crosses a process boundary, and the seam the
application declares for that dependency when one exists; each third party a suite calls for real,
with the calls one run makes to it per account and per destination; and any configured budget,
whether a runner timeout, a CI limit, or a documented target.

The measurement taken once before fan-out is the timing of every runner target through the
runner's own per-test and per-fixture duration reporting, serialized as the runner requires. Add
instrumentation only when the runner cannot report durations, and keep it only when the plan adopts
it. Record baseline pass/fail state, wall time per suite, and the slowest cases and fixtures. A suite
that cannot run locally is recorded unmeasured with its CI duration when one is available.

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
the redundancy, naming, runtime, third-party limit, doubles, and construction lenses to its slice.
The cross-cutting reviewer owns the layout and coverage lenses and the duplicates across suites of
one classification, because those are visible only across slices, and compares the doubles table
across suites, since a seam one suite uses and its sibling patches around is visible only there. It
also sums each provider's per-run calls per account and per destination across slices, since a
shared account's total is visible only there. A narrow scope gets two independent passes.

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
  resolves to after the test root, the suite, and the classification are stripped; whether
  `<name>.py` exists there; whether a package `<name>/` exists there; whether the module's own
  directory is named for a source module beside it. Three noes make the row a finding, and nothing
  the module contains overturns that: a module that sweeps every route of a package, drives
  requests across several modules, or tests a concern rather than a file has still claimed a
  source module that does not exist. `routes/test_pagination_bounds.py` with no
  `routes/pagination_bounds.py` is that finding.
  It moves under the source module it covers, as a behaviour module in a directory named for that
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

### Audit Test Value And Repair Weak Proof

Apply `test-fixture`'s **Test Value And Retention**, its dispositions included, to every test
declaration in scope, parameter rows that need different dispositions included, and record each
declaration's disposition, actual assertion and the contract it protects.

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

Run `test-fixture`'s **Naming Checks** over every `def test_`, fixture, factory and test helper in
the scope and report each check's result, an empty result included. Every naming and structural
check in this section is a finding the run fixes. A check that reports its rows and leaves them
standing, or a row admitted as an observation, is the miss this doctor exists to close.

### Bring Every Suite Under Budget

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
suite nobody will wait for is coverage nobody runs.

**No budget removes a test because a test of another classification makes the same assertion.** An
end-to-end test that an integration or unit test also reaches stays, however far over budget its
suite is and whatever stage the repository is in: its worth is that it runs the real services, which
the cheaper test does not. Being over budget, being pre-production, and the cheaper test being
"sufficient" are not reasons to cut it; bring the suite under budget by making its cases cheaper or
folding them into cases of the same classification.

Preserve every unique guarantee while doing it. Cutting a case whose assertion nothing else in its
classification makes is a coverage loss wearing a timing win, so name what each cut proved and where
that fact now lives.

### Stay Inside Third-Party Limits

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

### Map Coverage By Test

Map entry points — routes, RPC methods, commands, jobs, event consumers — gateways and clients,
persistence and migrations, and user journeys to the tests that exercise them in each
classification. A journey with no end-to-end test, a boundary crossing with no integration test, and a flow covered
only with its boundary mocked are gaps; a pure function covered only end-to-end is a unit gap.
Integration and end-to-end coverage outrank unit coverage for anything that crosses a boundary: a
unit test added for a flow whose integration or end-to-end path is untested is itself the gap.

### Make Doubles Honest

The inventory's table of doubles — target, owner, boundary, declared seam — is the evidence. Run
`test-fixture`'s **Auditing Existing Doubles** checks over it and report each check's result, an
empty result included, and name each double it leaves alone with its reason.

### Keep Construction Out Of Test Modules

Model-factory machinery belongs in the repository's established shared factory owner, including
when only one suite uses it. Fixture lifecycle wiring and scenario inputs stay in the suite.
Inject application model types where a shared import would invert dependencies.
Discover that owner from existing implementations and project guidance before relocating anything.
Apply the general New Modules ownership-completion rule: inspect every related implementation and
consumer, and flag a partial move even when the factory left behind was already there. Generic
lifecycle helpers retain their own owners; a shared word does not establish shared responsibility.

Run `test-fixture`'s **Factory Contents** checks over every factory module in the suite, with
the inventory and check rows that section requires in the report.

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

Application changes qualify only for the performance exception below, removal of a proven dead
test-only seam, or repair of a product defect exposed by a baseline failing test. For a seam,
inspect non-test callers and history, move coverage to its real owner boundary, then remove the
unused export, flag, wrapper, injection hook, or dead path without a compatibility alias. For a
baseline failure, reproduce the product defect, fix it at its owner in a separate commit, and show
the same harness failing with the fix absent and passing with it present. Do not weaken, skip, or
delete tests to conceal a defect. Other application correctness and structural changes remain
outside this doctor's boundary and are reported with evidence.

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
coverage guarantee unique within its classification; never cut tests solely to achieve a timing
target. A missed budget or unverified improvement remains unresolved rather than being reported as a successful performance fix.

Reviewers check every application performance change against this exception at proposal and final
review, including changes introduced during conflict resolution. Temporary application mutations used to
prove tests may bypass the performance exception only while running the proof; restore every one
before delivery and verify that none enters the delivered diff.

### Findings

- A slow suite, in order: widen the scope of the fixtures that dominate it, so an expensive world is
  built once for the tests that share it rather than per test; fold the cases whose runtime is out of
  proportion to what they prove into a case of the same classification already paying that setup,
  or make them cheaper where they stand; fix the remaining test-side causes; admit a focused
  application fix only through the performance exception; parallelize where the runner and shared
  resources allow, never across a shared database or lock. Re-time after implementation against the
  same workload. A suite still over budget is unfinished work, not a line in the report: carry on
  with the next disposition, or put the remaining cause and its cost to the user in the current
  request.
- A third-party limit finding clears the refusal by the order in **Stay Inside Third-Party
  Limits**, and is verified by the per-run count, per account and per destination, fitting the
  provider's documented limit with room for the runs that overlap it, and by running the affected
  suite twice back to back with neither drawing a refusal.
- A redundant test merges into the survivor of its own classification; an assertion nobody else
  in that classification makes is never dropped.
- A test-only production seam with no non-test caller is removed after its contract has a keeper;
  a baseline test exposing a product defect is repaired at the owner with failing control and
  passing candidate proof.
- A name any naming check reports — a leading article, more than eight words, a numeric status
  code, a restated class noun — is renamed to a label within `test-fixture`'s word budget; the
  condition the name lost moves into the docstring, and a rename that would leave fewer than two
  words takes a hand-chosen label rather than the mechanical residue.
- A layout finding moves to the pattern `test-fixture`'s ownership rules select; an even split
  between equally valid patterns is a user decision.
- A coverage gap is closed by the test that proves it, and a misplaced test moves between suites.
  Every added or rewritten test follows `test-fixture`, including its mutation proof per batch.
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

**This run posts one comment on each of its pull requests ranking the ten slowest tests and the ten slowest
fixtures, with each suite's wall time against the budget.** It is a declared outcome of the skill, so
invoking the skill authorizes that comment under the comment rules, and it is posted whether the run
brought every suite under budget or not.

The comment exists because a duration is the one finding with nowhere else to live. A pull request
body carries no measurements by rule, the diff cannot show a number, and a report in chat is gone by
the next session — so without this the run measures a breach on day one, delivers, and leaves nothing
a later reader can act on. Ranked in one place, the next run has its baseline and anyone deciding
what to cut can see what the time is being spent on.

Post it once per pull request, updating the same comment when a later push changes the numbers
rather than adding a second; each batch's pull request carries the ranking measured at its merge
head, so the last one holds the final numbers against the baseline. Give it the measured durations and nothing else: no narration of what the run did about them,
which the body and the diff already carry.

## Delivery

Tests-doctor delivers in merged batches under `doctor-protocol`'s **Deliver**. A test remediation
touches files across every suite, and one pull request held open for the whole plan conflicts with
every change landing beside it.

## Report Additions

- per suite: wall time before and after against the budget, and unmeasured suites with the reason;
- per suite: the sum of test call durations against wall time, naming setup-dominated suites;
- each case folded or made cheaper for disproportionate runtime, with what it proved and where that
  now lives;
- per suite: tests removed, parametrized, renamed, moved, and added;
- skip and xfail marks resolved;
- per suite, foreign domain nouns removed and the fixtures that carried them;
- the coverage map by test, with gaps closed and gaps recorded;
- per provider, account and destination: real calls per run before and after, and the refusals
  the baseline drew;
- determinism corrections; per suite, doubles of repository-owned code removed, moved to the suite
  with the real boundary, or retained with the fault they inject; and declared seams no test used
  before the run;
- each cut presented and the decision that authorized it.
