# Python Tests

The Python and pytest conventions `SKILL.md`'s **Language Router** selects, beside the language-neutral
criteria of the rubric.

Contents: **Test Module Directories**, **Parametrized Literal Values**, **Prefer Parametrized Cases**
(naming checks), **Place Construction Outside Tests** (factory contents), **Python Doubles**.

## Test Module Directories

**The `test_` prefix marks modules, never the directories that hold them.** A directory holding
tests is named for the source it mirrors, so `test_identity/` is `identity/`. Pytest collects on
the module name, so the prefix earns nothing on a folder while making every import path read as
though the directory were itself a test. A directory that holds material the tests read rather than
tests themselves keeps the prefix, because there it is not a marker: `test_cases/` holds the
scenarios other modules import, and `test_utils/` covers a source package named that, so the name is
the subject rather than a label.

## Parametrized Literal Values

Literal case values are allowed inside `pytest.mark.parametrize`; keep shared fixture-backed context
outside the parameter table. A literal outside parametrization is not a substitute for a fixture
value that exists or belongs on the canonical fixture.

## Prefer Parametrized Cases

Before adding a test, inspect the existing tests for the same behavior. When setup, exercised flow,
and assertions are the same and only inputs or expected outcomes differ — authorization errors,
not-found beside invalid-id, different name formats — extend or convert the
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
status code, replaced by its semantic name, such as `not_found` or `forbidden`. What is left is the behavior under test, which is the
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

A name identifies the case; the docstring carries the behavior sentence. Run
`scripts/naming_checks.py` from the skill directory over the scope's paths and report each block it
prints, an empty one included; it finds four name findings at any length: a name led by an article
(`a`, `an`, `the`), a name past eight words, a numeric HTTP status token, and a word restating a noun
the enclosing class or module already states.

Cut in the order above: the article and connective prose first, then every noun the class already
states, then the numeric code. A name that clears all four checks is finished;
one that fails any is a finding whatever its length.

A fixture or factory is named for the domain role or state it provides, as **Place Construction
Outside Tests** below sets out. A name coined from an abstraction or an adjective — an `-less` word,
a mechanism, a synonym for the thing — where the concrete thing it provides or lacks would name it is a finding,
renamed for that thing.

Name several results in one test for their scenario or domain role, such as
`invited_member_response` and `created_member_response`, never with a letter or a number, such as
`response_a`, `response_b`, `result_1`, or `result_2`.

A test class names its substantial coherent responsibility. Remove filler and misleading synonyms; small related cases extend their existing owning class rather than earning a separate class by being named. A helper that builds a model in a suite's `utils/` or `fixtures/`
package is named `create_<shape>` (the script lists every module-level `def` in those packages whose return type
is a model, with its name; report every row): a bare noun (`flag`), a mechanics prefix
(`stored_driver_license`), or a coinage (`flag_page`) is renamed `create_<shape>`, and the same shape
built under two names in two files or two suites is one name across all of them. Every other
module-level `def` in those packages is named for the domain act it performs, as that section sets out
(the script lists each with its first word; report every row whose first word is `post`, `put`,
`patch`, a transport verb, or a word saying how its value was made): `post_order` is renamed for what it asks
the application to do, and a `stored_customer` fixture for the role that customer plays.
Read names across
sibling files and sibling suites before settling one: a suite's vocabulary is its source's, and the
word the sibling suite already uses for the same shape wins over a new one.

## Place Construction Outside Tests

Never define a builder in a test module, including for its first caller.

- Put structured model construction in the repository's shared test-utilities package, using
  its configured factory mechanism. For Pydantic and SQLAlchemy data that is Polyfactory: a
  concrete `ModelFactory` or `SQLAlchemyFactory` class that sets `__model__`, provides
  deterministic, realistic domain defaults, constructs real nested relationships, and is called
  from tests directly as `.build(**overrides)`; `SQLAlchemyFactory` builds non-persisted ORM models.
  Common structured payloads come from such a class for the real request model, and from a
  service-specific pytest fixture in the suite's fixture package only where no model or Polyfactory
  path exists. No `ModelFactory` or `SQLAlchemyFactory` class belongs
  anywhere under `tests/`, even for its first or only consumer. Let the factory generate valid
  incidental values and express cross-field constraints without a manual replacement `build()`.
  Never wrap a factory class in a callable pytest fixture solely for dependency injection.
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
`create_customer` — never generic such as `record_factory`, numbered, prefixed with setup mechanics such as `persisted_*`,
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

```python
async def create_entity(
    client: httpx.AsyncClient, tenant_id: str, payload: CreateEntityPayload
) -> CreateEntityResponse:
    """Create an entity."""

    return parse_response(
        await client.post(...),
        CreateEntityResponse,
    )
```

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
places for the same thing. Keep `conftest.py` at shared test boundaries rather than scattering
topic-local ones. Name shared test modules for the domain or boundary they own rather than
introducing a `models.py`, `helpers.py`, or `utils.py` catch-all where a focused module is the
natural home.

Never declare a reusable request, response, persistence-payload or fixture model inside a test
module or lifecycle wiring, and never duplicate a helper model or utility type across test files.
Use the production boundary model when one exists; otherwise the typed declaration lives once in
its shared fixture or model owner.

When several tests need the same configuration overrides, expose one fixture helper in the suite's
fixture package instead of repeating `monkeypatch.setattr(...)` in each test.

For HTTP endpoint tests, build request payloads from the request models the application's routes
and services use, and use their native serialization with explicit contract-required options, such
as `model_dump(mode="json")`, never an ad-hoc inline dictionary passed to `json=` where a request
model exists. Share serialization behavior only when it adds a transformation or
contract decision beyond the model's native options; repeated calls with the same options do not
justify a fixed-argument forwarding helper. Use enum members rather than hard-coded strings, derive
an invalid payload from a valid one and mutate it deliberately, and serialize mocked response bodies
from the application's response models, or shared contract response models, rather than
hand-rolled dictionaries. A test-only
`BaseModel` mirroring a contract is the fallback where no application model exists; a
`SimpleNamespace` never is.

```python
class TreeNode(BaseModel):
    name: str
    children: list["TreeNode"] = Field(default_factory=list)
```

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

## Python Doubles

Use `AsyncMock` for async functions. `MagicMock` is acceptable for external boundaries such as SDK
response containers, subprocess handles, and network wrappers, and never for ORM or domain entities,
which come from concrete factories, ready fixtures, or domain-named creation fixtures returning real
instances. A mocked third-party library raises its real exception types, such as
`stripe.error.StripeError`, never a mock-specific custom exception, and a reusable fake prefers
real SDK or HTTP models and response objects over `MagicMock`.
