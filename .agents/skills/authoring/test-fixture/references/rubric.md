# Test Fixture Rubric

Apply these criteria to every test, test-data, test-support, and test-configuration change.

## Test Value And Retention

**A test is never redundant with a test of another classification — unit, integration, or
end-to-end.** End-to-end tests run the real services, integration tests replace some of them with
doubles, and unit tests replace all of them, so the same assertion proves something different in
each: an end-to-end test that an integration test also reaches stays, and so does an integration
test a unit test also reaches. When adding coverage, write the end-to-end test wherever one can
reach the contract.

Before adding a test, answer four questions; a missing answer means do not add it yet:

1. What observable behavior, invariant, or independent contract does it protect?
2. What credible regression makes it fail?
3. Which existing tests of the same classification were read, and why do they not already catch that failure? If they do, add nothing. Prefer
   extending a parameter table or shared fixture over a near-duplicate test; consolidate duplicated
   setup in the same change.
4. Does it need a production seam — an export, flag, wrapper, or injection hook — that no production
   caller needs? If so, move the test to the real boundary instead.

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
  restate flags instead of exercising the delivery or acknowledgement they promise;
- negative controls that pass for an unrelated reason, and names or fixtures that promise more
  than the input and assertions exercise.

A match fails the gate for a new test unless the test independently guards a contract below. An
existing match is suspect, not automatically deletable. A test that would break under
behavior-preserving source reorganization is asserting implementation rather than behavior; move
it to the owning boundary. Bug regressions fail on the pre-fix code for the intended reason and pass
after the owner repair. One regression per classification that reaches the bug covers it.

Keep a test when it independently enforces a public API, plugin interface, protocol, configuration,
migration, storage, security, platform, default, exact user-facing bytes, generated cross-language,
package, release, or architecture contract. Also keep observable call ordering and regressions with
a credible failure mode. Source inspection can be the cheapest independent guard when it fails as
the user-facing key, byte, or path changes and survives an identifier-only refactor. Static or slow
is not a deletion reason. A baseline failure may expose a product bug; reproduce it and repair the
owner rather than deleting its test.

Before deleting an existing test, record its exact name and location, the failure it can detect,
non-test callers of the covered source or support seam, the proof of the same classification that
remains (or why none is needed), relevant history, the source or support deletion it unlocks, risk,
and a focused validation command. Missing evidence leaves the candidate unready for deletion.
Read the complete test and production owner, entry point, callers, callees, sibling implementations,
overlapping tests, and CI routing; inspect dependency source or types for dependency-backed claims.

### Dispositions For Existing Tests

Mark each existing test declaration, and each parameter row that needs its own answer, retain,
repair, consolidate, or delete, with its actual assertion and the contract it protects. Judge
assertions, not names or deletion counts. A skip, xfail, or commented-out test whose condition no
longer holds is revived or deleted. For each contract duplicated within one classification, pick the
keeper of that classification and carry every unique assertion into it before removing the replay;
a test of another classification is never the keeper. Repair vacuous assertions and negative
controls that pass for the wrong reason, and verify new or strengthened guarantees through the
mutation proof. A failing baseline test is investigated as a possible product defect, not treated as
cleanup.

## Find The Canonical Test Data

Before adding a value, fixture, factory, or builder, discover the current suite's fixture mechanism
and shared fixture locations, configured factory mechanism, repository-wide shared test utilities,
and analogous tests in sibling services or projects. Read sibling tests for placement, naming,
setup, parametrization, and assertion conventions, but never import from a sibling test suite. Move
genuinely shared support to the nearest common test owner instead.

Trace each reused fixture, sample, or helper import to its defining module before treating it as
canonical. Apply the global **Code layout** boundary between executable consumers and reusable
owners: test-only setup belongs in established test support, while behavior used by applications
and commands belongs in its existing reusable source owner. Move the definition and update all
consumers rather than re-exporting it through a command or copying it into test support. Inspect
the resulting import direction. When executable-owned setup is found, search repository imports
and re-exports of executable modules for other data or helper ownership violations, not only
consumers of the moved symbol. Direct tests of the command itself remain command tests.

Use the value from the fixture or factory that owns the domain object. When that canonical surface
lacks a field the test needs, extend it and update its consumers instead of hard-coding the value,
adding a parallel fixture, or constructing a second representation in the test.

Test data speaks the domain of the source its suite mirrors, or none. Draw names, values,
fixtures, and scenarios from the nouns that source already uses; where it is a library with no
domain of its own, invent neutral placeholders. A consumer's table, schema, model, or product name
never enters a library's tests, the application's nouns and packages never enter the tests of a
generic package beside it, and a setting the application does not serve never enters the
application's tests: each describes a system the source does not own. The vocabulary of a third
party the source integrates with is its own.

Literal case values are allowed inside `pytest.mark.parametrize`; keep shared fixture-backed context
outside the parameter table. A literal outside parametrization is not a substitute for a fixture
value that exists or belongs on the canonical fixture.

Provider request and response bodies remain domain data when a test uses them as expected values.
Build them from the canonical fixture or response model rather than reproducing their names,
addresses, identifiers, or other field values inline.

A test-only helper has three possible homes, and how many test readers it has decides which. A trivial predicate
or formatter that one module reads may stay in that module. A helper one suite reads goes in that
suite's `utils` module. A helper more than one suite reads goes in the tests' `utils/` package,
under a topic-named module. Reaching into a sibling suite instead is what turns one suite's helper
directory into an unofficial shared home, and once the tests have several of those, nothing
distinguishes real setup from a workaround someone parked next to a failing test.

The suite's canonical root fixtures are the roots of test data. Put reusable subordinate identity,
report, form, billing, and business data on those typed fixture models instead of creating parallel
fixtures, and read nested values off them directly. Keep variant-only fields on typed subclasses of
the root, and select a variant through one aggregate creator with a typed selector rather than a
parallel creator per variant.

## Mirror Source Ownership

Discover the repository's source roots, test roots, distribution roots, build configuration, release
artifacts, suites, and existing ownership conventions. Test suites, fixtures, test helpers, and test
data belong outside every independently built or distributed package root unless that root is the
repository itself. In a multi-package repository, use the repository-level test surface and make its
runner, lint, type-check, CI, test imports, and package-source resolution explicit. A package that
currently excludes nested tests from its artifact still has the wrong ownership boundary; exclusion
does not justify test-only code inside a distributable package.

Mirror source directly beneath the test classification directory. Utility tests, including tests of
test-only source helpers, live in `utils/`; keep test support in the nearest fixture or utility
package that does not hide a source owner. Preserve a repository's revision-support convention for
migrations.

An ordinary test mirrors the source path for the concern it exercises after removing the source and
test roots and test-classification segments such as unit or integration. The paths need not be
character-for-character identical; their ownership hierarchy must be recognizable in both trees.

Before placing or moving a test, compare analogous sibling service tests and their corresponding
source owners. Apply explicit repository guidance first. Otherwise prefer the layout that most
directly mirrors source ownership, using the majority pattern among analogous sibling service tests
as corroborating evidence. Existing sibling tests are evidence, not authority. Preserve a different
layout only when a real ownership or boundary difference explains it; legacy placement alone is not
a reason. If equally valid patterns remain, present the concrete choice to the user instead of moving
tests arbitrarily or adding another variation.

Test-owned structures may follow the testing concern rather than a production path:

- fixture, factory, shared-case, utility, snapshot, and harness packages;
- integration or end-to-end flows that deliberately span several source modules;
- a behavior folder that replaces one heavily tested source module with several focused test
  modules named for independently maintained behaviors, when the file-boundary test below justifies a split.

Place a cross-module test at the nearest shared source owner.

Keep one test class per file, but create a class only for a substantial coherent responsibility. Before creating a class or file, inspect the existing class that owns the source behavior and its parameter sets; extend them for small related cases. A helper, operation, boundary case, or pair of tests does not by itself earn a class. When several small classes cover one owner, merge their related cases into the broader owning class and its file, preserving independent coverage; split a substantial suite only where independently maintained responsibilities justify separate classes.

Before adding or relocating model-factory machinery, discover and extend the established shared
factory owner named by project guidance. Apply the general New Modules rule to all related
implementations and consumers; a package that accepts a new factory is not necessarily its owner.
Complete any ownership move rather than leaving existing factories in a competing location. Keep
lifecycle helpers with their own responsibilities and inject application model types when needed
to preserve dependency direction.
Inspect construction functions and nested builders as well as factory subclasses. For each related
implementation, verify that it was consolidated, replaced, or retained for demonstrated lifecycle,
I/O, registration, or scenario responsibilities; returning a model under a fixture decorator does
not by itself establish a separate owner.

## Prefer Parametrized Cases

Before adding a test, inspect the existing tests for the same behavior. When setup, exercised flow,
and assertions are the same and only inputs or expected outcomes differ, extend or convert the
existing test with `pytest.mark.parametrize` instead of adding another test method. Give cases
readable IDs, parametrize with readable lists or tuples and convert to a set inside the test when
the subject needs one, and keep shared fixture context outside the parameter table.

Add a separate test when its setup, control flow, asserted behavior, or failure meaning materially
differs. Do not force unrelated scenarios into one parameter table merely because they call the same
function.

```python
@pytest.mark.parametrize(
    ("postal_code", "expected_region"),
    [
        ("03301", "NH"),
        ("90001", "CA"),
    ],
)
def test_lookup_region(postal_code: str, expected_region: str) -> None:
    result = lookup_postal_region(postal_code)

    assert result is not None
    assert result.region == expected_region
```

Derive the values a case ranges over from the production type that already declares them rather
than restating them: parametrize over the enum's own members, because a hand-written list of its
values is a second copy that no rename will reach.

A case is a scenario the tests invent: a table of inputs and their expected outcomes, a stored
`pytest.mark.parametrize` decorator, the `ids` naming those scenarios, and any descriptor model the
scenarios are built from. A case shared by more than one test module lives in a `test_cases`
package, never in a general-purpose `utils.py`. Put the package at the level its consumers span, the
way `conftest.py` already sits at shared boundaries, with a module per domain and an `__init__.py`
that re-exports what tests import. A table only one module reads stays in that module: promote it
when a second module needs it, not before. Name a case for the domain it addresses rather than its
position in the module it came from, since the name has to stand on its own once the definition no
longer sits above its tests.

An inventory of production symbols a test iterates is not a case, even though it reaches
`parametrize` the same way. A registry of the endpoint classes to check, the models a contract
covers, or the config files that must all behave alike describes the subject under test rather than
a scenario, so it stays in the module that tests it.

Treat a test name as a short case label, not a sentence. State only what distinguishes the case from
the subject already named by its module and class; remove filler and repeated subject words. Follow a
configured repository limit when one exists. Otherwise aim for four or five words after `test_` and
never exceed eight. The docstring carries the full sentence: the condition, the expected result, and
why it matters.

When a name is over, that is the order to cut in: the articles and connective prose first — `a`,
`the`, `that`, `it`, `its` — then every noun the module or the class already states, then a numeric
status code, replaced by its semantic name. What is left is the behavior under test, which is the
only part the name owes a reader. A leading article, a numeric status code, and a noun the class
already states are findings at any length, not only past the budget. A name inside the limit that
carries none of them is finished.

```python
class TestRedeemCoupon:
    """Test redeeming a coupon against its expiry and usage limits."""

    # Bad: the name restates the whole assertion, and the docstring repeats it
    def test_a_coupon_past_its_expiry_date_is_refused_and_leaves_the_balance_alone(self) -> None:
        """Test that a coupon past its expiry is refused and leaves the balance alone."""

    # Bad: the article is filler; the class already supplies the grammar
    def test_an_expired_coupon(self) -> None:
        """Test that redeeming past the expiry is refused and leaves the balance alone."""

    # Good: the name identifies the case, the docstring states the behavior
    def test_expired_coupon(self) -> None:
        """Test that redeeming past the expiry is refused and leaves the balance alone."""
```

### Naming Checks

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

Cut in the order above: the article and connective prose first, then every noun the class already
states, then the numeric code. A name that clears all four checks is finished;
one that fails any is a finding whatever its length.

A fixture or factory is named for the domain role or state it provides, as **Place Construction
Outside Tests** below sets out. A name coined from an abstraction or an adjective — an `-less` word,
a mechanism, a synonym for the thing — where the concrete thing it provides or lacks would name it is a finding,
renamed for that thing.

A test class names its substantial coherent responsibility. Remove filler and misleading synonyms; small related cases extend their existing owning class rather than earning a separate class by being named. A helper that builds a model in a suite's `utils/` or `fixtures/`
package is named `create_<shape>` (list every module-level `def` in those packages whose return type
is a model, with its name; report every row): a bare noun (`flag`), a mechanics prefix
(`stored_driver_license`), or a coinage (`flag_page`) is renamed `create_<shape>`, and the same shape
built under two names in two files or two suites is one name across all of them. Every other
module-level `def` in those packages is named for the domain act it performs, as that section sets out
(list each with its first word; report every row whose first word is `post`, `put`, `patch`, a
transport verb, or a word saying how its value was made): `post_order` is renamed for what it asks
the application to do, and a `stored_customer` fixture for the role that customer plays.
Read names across
sibling files and sibling suites before settling one: a suite's vocabulary is its source's, and the
word the sibling suite already uses for the same shape wins over a new one.

## Place Construction Outside Tests

Never define a builder in a test module, including for its first caller.

- Put structured model construction in the repository's shared test-utilities package, using
  its configured factory mechanism. No `ModelFactory` or `SQLAlchemyFactory` class belongs
  anywhere under `tests/`, even for its first or only consumer. Let the factory generate valid
  incidental values and express cross-field constraints without a manual replacement `build()`.
  Inject application model types into shared machinery when importing them would invert
  dependencies. Suite fixtures may bind those model types and scenario inputs; keep lifecycle
  wiring local. Use the concrete factory type rather than a parallel `Protocol`.
- Put persisted flows, filesystem materialization, dependency lifecycles, and multi-object scenarios
  in a domain-named pytest factory fixture at the repository-established shared fixture location.
  Such a fixture returns a keyword-only inner builder named `_build` or for its specific action,
  never a bare `factory`. Filesystem and other I/O materialization takes typed factory-built models
  and explicit target paths.
- Keep a test module focused on composing fixtures, exercising behavior, and asserting outcomes.

Factories construct meaningful aggregates, complete boundary models, persisted roots, or
multi-object scenarios; a leaf value, a relationship row, or a payload fragment gets no factory and
is built through its owning root. A factory's name is domain-qualified — `create_order`,
`create_customer` — never generic, numbered, prefixed with setup mechanics such as `persisted_*`,
or suffixed with persistence mechanics such as `*_orm_factory`. Its inputs are typed aggregates or
boundary models rather than positional identity scalars, nested override dictionaries, relationship
rows, or payload fragments.

Extend the shared factory owner when it already builds the shape. A single-suite consumer does
not create an exception to shared ownership; scenario-specific values belong in suite fixtures.

Name every test helper so a reader who has never opened it knows what it does and what it hands
back. A helper named for its mechanism — an HTTP verb that is not also the act (`post_order`,
`put_invoice`), the transport (`send_`, `fetch_`), or how its value was made (`stored_customer`,
`persisted_order`) — says how and leaves what to be guessed. Name the domain act or the role, and
where siblings differ only in what they return, the difference (`request_order_creation` returns
the response a failure test reads, `create_order` the parsed result). A reader that returns what
storage holds, in a test about storage, is named for that and keeps the word.

Prefer a ready, function-scoped fixture named for a domain role or state — the concrete thing it
provides or lacks, never a coined adjective — when each test needs one standard
instance, and prefer one that returns a real ORM instance for ORM-heavy tests. Add a callable
creation fixture only when tests genuinely need arbitrary independently configured instances.

A fixture is never defined in a test module either. A fixture beside the tests that use it is
invisible to every other module, so the next suite needing the same setup writes its own copy, and
one concept ends up with three implementations. Move it to the suite's fixture package, and where it
was autouse, keep its exact reach with a module-level `pytestmark = pytest.mark.usefixtures(...)`
rather than letting a shared definition widen it to the whole suite. The one fixture that may stay
nested is one defined inside a single test class, because nesting already scopes it to that class
and moving it would widen it.

A suite keeps its reusable fixtures in a `fixtures/` package of topic-named modules that its
`conftest.py` imports or registers, and keeps `conftest.py` for lifecycle wiring: the database
session, the event loop, autouse environment setup, plugin registration. A suite that puts domain
fixtures in `conftest.py` while its sibling puts them in `fixtures/` makes a reader look in two
places for the same thing. Name shared test modules for the domain or boundary they own rather than
introducing a `models.py`, `helpers.py`, or `utils.py` catch-all where a focused module is the
natural home.

When several tests need the same configuration overrides, expose one fixture helper in the suite's
fixture package instead of repeating `monkeypatch.setattr(...)` in each test.

For HTTP endpoint tests, build request payloads from the request models the application's routes
and services use, and use their native serialization with explicit contract-required options, such
as `model_dump(mode="json")`. Share serialization behavior only when it adds a transformation or
contract decision beyond the model's native options; repeated calls with the same options do not
justify a fixed-argument forwarding helper. Use enum members rather than hard-coded strings, derive
an invalid payload from a valid one and mutate it deliberately, and serialize mocked response bodies
from the application's response models rather than hand-rolled dictionaries. A test-only
`BaseModel` mirroring a contract is the fallback where no application model exists; a
`SimpleNamespace` never is.

```python
# Bad: a hard-coded property in a test payload
payload = {
    "website": "https://example.com",
}

# Good: add website to the shared fixture setup and use fixture data
assert account_fixture.website is not None
payload = {
    "website": account_fixture.website,
}
```

### Factory Contents

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

Use `AsyncMock` for async functions. `MagicMock` is acceptable for external boundaries such as SDK
response containers, subprocess handles, and network wrappers, and never for ORM or domain entities,
which come from concrete factories, ready fixtures, or domain-named creation fixtures returning real
instances. A mocked third-party library raises its real exception types, and a reusable fake prefers
real SDK or HTTP models and response objects over `MagicMock`.

Test the documented and implemented SDK contract, not speculative runtime shapes: no defensive test
for a surface the integration contract guarantees, and tests of a required SDK method focus on its
valid responses and real failure modes. Keep names and docstrings about behavior and outcomes rather
than SDK internals.

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
