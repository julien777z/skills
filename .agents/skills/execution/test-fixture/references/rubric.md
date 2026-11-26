# Test Fixture Rubric

Contents: **Test Value And Retention** (deletion evidence, cost, dispositions), **Find The Canonical Test Data**
(boundary representations and decision matrices), **Mirror Source Ownership**, **Choose Test Doubles**
(auditing existing doubles), **Third-Party Calls Use Documented Doubles**, **A Missing Credential
Leaves The Test Alone**, **Literal Sweep**. The Python
and pytest conventions are in the language reference `SKILL.md`'s **Language Router** selects.

Apply these criteria to every test, test-data, test-support, and test-configuration change. The
suites reference beside this file holds the conventions for suites, test modules, test
configuration and time budgets.

## Test Value And Retention

**A test is never redundant with a test of another classification — unit, integration, smoke, or
end-to-end.** End-to-end tests run the real services, integration tests replace some of them with
doubles, and unit tests replace all of them, so the same assertion proves something different in
each: an end-to-end test that an integration test also reaches stays, and so does an integration
test a unit test also reaches. When adding coverage, write the end-to-end test wherever one can
reach the contract, within **Third-Party Calls Use Documented Doubles**.

Before adding a test, answer five questions; a missing answer means do not add it yet:

1. What observable behavior, invariant, or independent contract does it protect?
2. What credible regression makes it fail?
3. Which existing tests of the same classification were read, and why do they not already catch that failure? If they do, add nothing. Prefer
   extending a parameter table or shared fixture over a near-duplicate test; consolidate duplicated
   setup in the same change.
4. Does it need a production seam — an export, flag, wrapper, or injection hook — that no production
   caller needs? If so, move the test to the real boundary instead.
5. Is what it proves worth what it costs to run? Apply **Test Cost** below.

Check new and existing tests against these low-value patterns:

- assertion-free coverage probes, self-comparisons, identity copiers, and expected values produced
  by the helper or renderer under test;
- copied fixtures, inventories, manifests, export lists, or duplicate invocations of one contract;
- exact source, import, or string greps, and private predicate or call-shape tests duplicated by a
  test of the same classification at a real boundary;
- provider-local replays of shared helpers, tests preserving test-only exports or wrappers, and
  production code whose only callers are tests;
- mocks that implement the asserted behavior, one identical mock standing in for different APIs,
  or fixtures supplying the receipt, admission, or callback order the owner should produce;
- persistence asserted against a store the exercised path never writes, and capability tests that
  restate flags instead of exercising the delivery or acknowledgment they promise;
- negative controls that pass for an unrelated reason, and names or fixtures that promise more
  than the input and assertions exercise.

A match fails the gate for a new test unless the test independently guards a contract below. An
existing match is suspect, not automatically deletable. A test that would break under
behavior-preserving source reorganization is asserting implementation rather than behavior; move
it to the owning boundary. Bug regressions fail on the pre-fix code for the intended reason and pass
after the owner repair. One regression per classification that reaches the bug covers it.

For a substantial behavior change, cover the normal path, each meaningful boundary, and the relevant
validation or failure path. A single assertion or a single happy-path case is not sufficient
coverage for a multi-path contract.

Keep a test when it independently enforces a public API, plugin interface, protocol, configuration,
migration, storage, security, platform, default, exact user-facing bytes, generated cross-language,
package, release, or architecture contract. Also keep observable call ordering and regressions with
a credible failure mode. Source inspection can be the cheapest independent guard when it fails as
the user-facing key, byte, or path changes and survives an identifier-only refactor. Static is not
a deletion reason, and neither is ordinary slowness; a disproportionate cost under question 5 is,
as **Test Cost** sets out. A test already failing on the default branch is a baseline failure:
record it as `pre-production`'s **Encountered Issues** says and move on, without reproducing,
investigating or repairing it, and never delete its test for failing.

### Test Deletion Evidence

Before deleting an existing test, record its exact name and location, the failure it can detect,
non-test callers of the covered source or support seam, the proof of the same classification that
remains (or why none is needed), relevant history, the source or support deletion it unlocks, risk,
and a focused validation command. Missing evidence leaves the candidate unready for deletion.
Read the complete test and production owner, entry point, callers, callees, sibling implementations,
overlapping tests, and CI routing; inspect dependency source or types for dependency-backed claims.

### Test Cost

Use existing runner duration reporting,
including setup where existing reporting attributes it. Missing attribution remains unmeasured;
use available suite timing without inferring individual costs. A test or
parametrized family whose durations sum to more than a minute, or a module whose tests together
take two minutes or more, is disproportionate. Make it cheap through its own setup —
build an immutable resource once, cut the cases to the ones that differ — or remove the tests
that still cost more than they prove, keeping a cheaper test of the same classification where
the contract still needs one. A speedup that needs code existing only for tests — a production
seam, flag, shortened timer or test-only branch — does not make it cheap, and neither does any
way of absorbing a slow test listed below. Below those lines the same trade still
applies: a test whose runtime is large beside the failure it could catch is folded into a case
already paying that setup, or cut.

**A test, parametrized family or module that dominates its suite's runtime is the cause, not the
suite around it.** A disproportionate one is made cheap or removed, as above. Absorbing it instead
keeps the cost and hides it, exactly as a raised timeout does: retuning the runner's distribution
mode, worker count, ordering or grouping, giving it a job of its own, skipping it, marking it for a
run pull requests deselect, or moving it to a scheduled workflow. The suites reference's **Time
Budgets** set the budget a whole suite fits.

### Dispositions For Existing Tests

Mark each existing test declaration, and each parameter row that needs its own answer, retain,
repair, consolidate, or delete, with its actual assertion and the contract it protects. Judge
assertions, not names or deletion counts. A skip, xfail, or commented-out test whose condition no
longer holds is revived or deleted. For each contract duplicated within one classification, pick the
keeper of that classification and carry every unique assertion into it before removing the replay;
a test of another classification is never the keeper. Repair vacuous assertions and negative
controls that pass for the wrong reason, and validate new or strengthened guarantees through the
existing-check procedure in the owning entry point. A test already failing on the default branch
is recorded and left as **Test Value And Retention** says: it is not reproduced, investigated or
repaired, and is not removed as cleanup.

## Find The Canonical Test Data

Before adding a value, fixture, factory, or builder, discover the current suite's fixture mechanism
and shared fixture locations, configured factory mechanism, repository-wide shared test utilities,
and analogous tests in sibling services or projects. Read sibling tests for placement, naming,
setup, parametrization, and assertion conventions, but never import from a sibling test suite. Move
genuinely shared support to the nearest common test owner instead.

Trace each reused fixture, sample, or helper import to its defining module before treating it as
canonical. Apply `pre-production`'s **Code Layout** boundary between executable consumers and reusable
owners: test-only setup belongs in established test support, while behavior used by applications
and commands belongs in its existing reusable source owner. Move the definition and update all
consumers rather than re-exporting it through a command or copying it into test support. Inspect
the resulting import direction. When executable-owned setup is found, search repository imports
and re-exports of executable modules for other data or helper ownership violations, not only
consumers of the moved symbol. Direct tests of the command itself remain command tests.

Use the value from the fixture or factory that owns the domain object. When that canonical surface
lacks a field the test needs, extend it and update its consumers instead of hard-coding the value,
adding a parallel fixture, or constructing a second representation in the test:
`UUID("00000000-...")` is `entity_fixture.id`, `name="John Doe"` is `user_fixture.name`, and
`email="test@example.com"` is `user_fixture.email`. Where a model exists for sample, request,
response, or provider data, construct the typed model; never maintain a parallel hand-written
dictionary of that contract.

Use clearly synthetic data that is unique to each test or parametrized case unless an exact protocol
or catalog literal is the contract under test.

Test data speaks the domain of the source its suite mirrors, or none. Draw names, values,
fixtures, and scenarios from the nouns that source already uses; where it is a library with no
domain of its own, invent neutral placeholders. A consumer's table, schema, model, or product name
never enters a library's tests, the application's nouns and packages never enter the tests of a
generic package beside it, and a setting the application does not serve never enters the
application's tests: each describes a system the source does not own. The vocabulary of a third
party the source integrates with is its own.

Provider request and response bodies remain domain data when a test uses them as expected values.
Build them from the canonical fixture or response model rather than reproducing their names,
addresses, identifiers, or other field values inline.

A test-only helper has three possible homes, and how many test readers it has decides which. A trivial,
non-construction predicate, formatter, or assertion adapter such as `to_comparable_string` that one
module reads may stay in that module. A helper one suite reads goes in that
suite's `utils` module. A helper more than one suite reads goes in the tests' `utils/` package,
under a topic-named module. Reaching into a sibling suite instead is what turns one suite's helper
directory into an unofficial shared home, and once the tests have several of those, nothing
distinguishes real setup from a workaround someone parked next to a failing test. A helper is
defined at module level, never inside a test, with a single-line docstring. A helper that only
formats one URL or returns one fixture or model field is not written: inline a one-off value, or
reuse an existing shared boundary when the operation is repeated or nontrivial.

The suite's canonical root fixtures are the roots of test data. Put reusable subordinate identity,
report, form, billing, and business data on those typed fixture models instead of creating parallel
fixtures, and read nested values off them directly. Keep variant-only fields on typed subclasses of
the root, and select a variant through one aggregate creator with a typed selector rather than a
parallel creator per variant.

### Boundary Representations And Decision Matrices

When a test supplies an external response, request, queue message, file, cache entry, or stored
payload, build its data from the canonical fixture or boundary model and encode it as the real
consumer receives it. Where production owns the encoding, select its explicit provider or storage
serialization options — such as field aliases, omission rules, enum values, casing, nesting, and
JSON mode — rather than passing internal Python field names or a default dump through a permissive
parser. A test that constructs a model and hands its fields directly to the reader proves only
in-memory model behavior; it does not prove the boundary contract. When production only consumes a
representation, construct the native wire data from canonical fixture values in the established
typed test support. Repair production only when its actual parsing or emission contract is
incomplete, never to add an encoder that no production caller needs.

For a decision that filters, selects, stops, retries, falls back, merges, or persists values, trace
every input field and collection condition the production path reads before choosing cases. Extend
the owning parameter table with the distinct states that can change the outcome: a matching value,
contradictory value, omitted optional evidence, absent required evidence, and one versus multiple
candidates where each applies. Cover interactions only when the production predicates combine
them; this is a decision matrix, not an arbitrary cross-product. Each row asserts the externally
observable result — for example, early completion versus a fallback request — rather than only the
decoded intermediate model. Before implementing or changing the test cases, prepare these rows as the `Boundary matrix` the
skill's workflow records and reports, so review can find a missing state or an internal
representation substituted for the consumer contract.

After strengthening one such boundary test, inspect the sibling tests and shared fixtures that emit
the same representation. Update every one that simulates the same production boundary with internal
field names or an incomplete decision state; keep tests of an in-memory model on its native
in-memory contract.

## Mirror Source Ownership

Discover the repository's source roots, test roots, distribution roots, build configuration, release
artifacts, suites, and existing ownership conventions. Test suites, fixtures, test helpers, and test
data belong outside every independently built or distributed package root unless that root is the
repository itself. In a multi-package repository, use the repository-level test surface and make its
runner, lint, type-check, CI, test imports, and package-source resolution explicit. A package that
currently excludes nested tests from its artifact still has the wrong ownership boundary; exclusion
does not justify test-only code inside a distributable package.

Mirror source directly beneath the test classification directory: where the source has `core/`,
`models/`, `routes/`, or `services/`, the `unit/` and `integration/` folders keep those boundaries,
and a test sits beside the source subdomain it verifies, not in a loosely related folder. Utility
tests, including tests of test-only source helpers, live in `utils/`; keep test support in the
nearest fixture or utility package that does not hide a source owner. Preserve a repository's
revision-support convention for migrations, and drop a generated revision or timestamp prefix from a
migration test's name, keeping the descriptive remainder. The suites reference sets the layout of
smoke tests, which this mirroring does not govern.

Proto conversion round-trip tests are unit tests. Keep tests of the serialization layer itself in a
dedicated `proto/` test folder; gateway, runtime, and servicer tests that merely consume proto
messages stay beside their owning source subdomain.

An ordinary test mirrors the source path for the concern it exercises after removing the source and
test roots and test-classification segments such as unit or integration. The paths need not be
character-for-character identical; their ownership hierarchy must be recognizable in both trees.

**One source file has one test module, named for it** by the language's test-file convention: a
source file `pkg/invoices.py` is tested by `test_invoices.py` at the mirrored path, and
`src/invoices.ts` by `invoices.test.ts`. That module holds the tests of every function and class
in the file, unless independently maintained behaviors justify a behavior folder, as the list below says, whose modules pass
this check. A folder named for a source file, holding a test file per function or class, is not a
mirror: its paths resemble the source, but the source file has no test module, so the next test of
that file gets a file of its own instead of joining the others. Check it mechanically: list every
test module in scope and compare its name, without the test-file marker, with the source file at the mirrored
path. A test module named for a function or class inside a source file is a finding; its tests fold
into that source file's test module, organized as this section's class rule and **Prefer
Parametrized Cases** say, within `pre-production`'s size budget, the rest handled as that budget
says.

Before placing or moving a test, compare analogous sibling service tests and their corresponding
source owners. Apply explicit repository guidance first. Otherwise prefer the layout that most
directly mirrors source ownership, using the majority pattern among analogous sibling service tests
as corroborating evidence. Existing sibling tests are evidence, not authority. Preserve a different
layout only when a real ownership or boundary difference explains it; legacy placement alone is not
a reason. Siblings that split a source file into a file per function or class are the finding above,
never the layout a new test copies: the new test goes into the source file's test module, created
where it is absent. If equally valid patterns remain, the agent picks one and states it, as the
skill's workflow says, instead of moving tests arbitrarily or adding another variation.

Test-owned structures may follow the testing concern rather than a production path:

- fixture, factory, shared-case, utility, snapshot, and harness packages;
- integration or end-to-end flows that deliberately span several source modules;
- a behavior folder that replaces one heavily tested source module with several focused test
  modules named for independently maintained behaviors, when those behaviors change for different reasons.
  A function or class is never such a behavior on its own account.

Place a cross-module test at the nearest shared source owner, and name a test that spans a
subsystem for that subsystem.

Keep one test class per file, but create a class only for a substantial coherent responsibility. Before creating a class or file, inspect the existing class that owns the source behavior and its parameter sets; extend them for small related cases. A helper, operation, boundary case, or pair of tests does not by itself earn a class. When several small classes cover one owner, merge their related cases into the broader owning class and its file, preserving independent coverage; split a substantial suite only where independently maintained responsibilities justify separate classes.

Before adding or relocating model-factory machinery, discover and extend the established shared
factory owner the repository's test-utilities package holds. Apply `pre-production`'s **A new file is the last resort** bullet to all related
implementations and consumers; a package that accepts a new factory is not necessarily its owner.
Complete any ownership move rather than leaving existing factories in a competing location. Keep
lifecycle helpers with their own responsibilities and inject application model types when needed
to preserve dependency direction.
Inspect construction functions and nested builders as well as factory subclasses. For each related
implementation, verify that it was consolidated, replaced, or retained for demonstrated lifecycle,
I/O, registration, or scenario responsibilities; returning a model under a fixture decorator does
not by itself establish a separate owner.

## Choose Test Doubles

Run the real code first. A repository-owned callable whose implementation is deterministic and stays
in the process — a predicate, a policy, a formatter, a normalization helper, a model method — runs
as itself, with its input arranged by the suite's fixtures. A repository-owned object — a request, a
settings object, a domain model, an ORM row, a result model, a scope or context object — is a real
instance from the suite's fixtures, its factories, or its own constructor. A flow that needs a row
is proven in the tests that have the real database, never by patching persistence in a test without
one; a conflict the database raises is produced by inserting the conflicting row,
never by patching `insert` to raise.

A double is for what the process cannot cross — a third-party SDK, the network, another service, the
filesystem, the clock, randomness, a subprocess — or for a fault the real path cannot produce. It
sits at the seam the application declares: the provider override, the fake, or the consuming
module's binding of the gateway. A patch one layer above that seam, a service wrapper instead of the
gateway binding it fronts, discards the logic the wrapper owns. Reach for doubles in this order, and
take the first that fits:

1. an injected fake or an override of the provider the application already exposes for the
   dependency, which is the seam the application declares;
2. a fake the third-party library ships or the repository maintains for it;
3. a reusable mock shape from the shared test-utilities package — an async context manager in
   place of a session factory, a connection, or a transaction is the same four lines wherever it
   appears, and each hand-rolled copy is a chance to get `__aexit__` subtly wrong, so it is built
   once, takes the yielded object as an argument, and is imported;
4. a patch, at the consuming module's own binding rather than the module that defines the symbol.

**Depth is a separate question from kind, and every one of the four is answerable at the wrong
depth.** Reaching for the provider override the application declares settles which seam the test
uses; it says nothing about what the override is pointed at, so a fake transport installed through
it is as deep as any patch and reads as compliant because the kind was right.

**The assertion says which depth you chose.** When it reads a representation the library produced —
a form body, a query string, a URL path, serialized JSON, a wire frame — the double sits below the
boundary and the test is exercising the library's encoder. Double the collaborator the application
calls instead, assert the arguments it was called with and the value it answered, and let the
library's own tests cover the encoding. A test that hand-writes that encoding to read a value back
is rebuilding the library to check what the caller passed it.

Test the documented and implemented SDK contract, not speculative runtime shapes: no defensive test
for a surface the integration contract guarantees, and tests of a required SDK method focus on its
valid responses and real failure modes. Keep names and docstrings about behavior and outcomes rather
than SDK internals: no exact required-method name, and no wording such as "when `<method>` is
available."

For database verification, query the database directly and compare fields.

### Auditing Existing Doubles

List every double in scope — its target, the target's owner, whether the real implementation
crosses a process boundary, and the seam the application declares — and run every check below over
that list:

- a repository-owned callable patched whose real implementation is deterministic and in-process:
  it runs as itself, as above, and the fixture that arranges its input usually exists;
- a repository-owned persistence call patched — an ORM class method, a repository function, a
  service that reads rows — or a persistence method assigned onto a real row: the rule above
  applies, and a conflict is produced by the conflicting row;
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
  suite: one fixture helper in the suite's fixture package;
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
gateway function, the seam this section names for a hop to another service; a third-party function
imported into a repository module and patched at that binding; a repository wrapper that is the
last hop before the HTTP client; a replacement that calls through to the real function after
arranging an interleaving the database would not produce on its own; a fault injected to prove
the surrounding write still commits; a fake that raises the library's real exception to simulate
an outage; a double container installed through the lifecycle override that carries real wire
messages; a private attribute of a third-party object; a settings module tested as its own
subject; a same-module symbol that constructs a third-party client.

## Third-Party Calls Use Documented Doubles

**A test or check an agent adds or runs for code that calls a third-party service with
credentials** — such as a model provider, a paid API, or an identity or payment provider — uses a
double built from that provider's documented request and response structures, such as its API
reference and SDK types, at the seam **Choose Test Doubles** names, never a live call with real
credentials. New live cases, in a new suite or an existing one, are written only when the user asks
for them; an existing live test whose covered behavior the change breaks or alters is updated to
match that behavior, adding no further live call. The one exception is a suite the repository
already runs across that boundary: it runs as written, with the credentials where the repository
configures them, under **A Missing Credential Leaves The Test Alone**. A plan, review or gate that
asks for a live call is answered with this section.

## A Missing Credential Leaves The Test Alone

**A credential, endpoint or environment nobody has issued is an external blocker, and an external
blocker never changes the test.** A test that cannot pass because a real key does not exist is
already reporting the truth, and its red check is what gets the key issued. Leave it failing, name
the missing credential where the run reports it, and go on.

**Three moves all remove that pressure, and they are one move.** A fake standing in for the
provider makes the test pass against something nobody ships; a skip conditioned on whether the
credential is present makes it pass by not running, in a way nobody sees in a green suite; deleting
it makes it pass by having no test. Each converts a stated debt into a quiet one, and each is
reached for while telling yourself the coverage was never real anyway.

**This governs the suite written to cross a boundary for real** — the end-to-end run, the
integration test against the live dependency — where the credential is the whole point and standing
one in defeats it. Where the process genuinely cannot cross a boundary, **Choose Test Doubles**
governs, and its answer there is unaffected by whether a credential exists.

## Literal Sweep

Inspect the diff with a search broader than the query that found the original test. In a review,
report every changed literal family and classify it as one of:

1. canonical fixture or factory data, which must be read from that owner;
2. a production-declared protocol or enum value, which must be derived from that declaration;
3. an external protocol literal with no typed production owner when that contract is the subject,
   which may remain local;
4. an explicit parametrized case value, which may remain local;
5. a non-domain, non-sample behavioral or control value with no fixture, factory, or production
   owner, which may remain local; or
6. an unexplained duplicate, which must be removed.

Treat names, addresses, identifiers, tax values, contact details, dates, and provider sample facts as
fixture data. Their appearance in provider documentation does not make a duplicate test literal
canonical when the repository already declares the sample through a typed fixture or model.

The skill's **Sweep** sets which tests and files the same check reaches beyond the diff; validate
only the targets the final diff reaches.
