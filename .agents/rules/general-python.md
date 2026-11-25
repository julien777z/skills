---
description: Apply when editing Python typing, imports, modules, constants, functions, control flow, or logging.
alwaysApply: false
paths:
- '**/*.py'
---

# General Python Rules

## Syntax and Typing

- Use modern type hints: `str | None` instead of `Optional[str]`.
- Use built-in generics: `list[T]`, `dict[K, V]` instead of `List[T]`, `Dict[K, V]`.
- Type a class method that returns a new instance of its own class as `Self` from `typing`; any
  other class method names its return type.
- Use `collections.abc` for abstract types: `Callable`, `Iterable`, etc.
- Never use `Protocol` for model typing; use concrete model classes in type annotations.

- Model structured payloads explicitly: use `TypedDict` for mapping-shaped data and Pydantic `BaseModel` for every data-holding class, rather than arbitrary inline dictionaries, `dict[str, object]`, `dataclass`, or `NamedTuple`.
- **No annotation uses `typing.Any`**, in application or test code, and neither do the escape hatches that do its job under another name: a `cast(...)` that silences the checker, or `*args`/`**kwargs` passed through to a callee instead of declaring the parameters it takes. Each hides the contract the checker would have enforced. Reserve a narrowly scoped cast for information the type system genuinely cannot express.
  - A value whose type varies with the caller is a `TypeVar`, a `ParamSpec`, or a generic class.
  - A truly unconstrained input is `object`, narrowed with `isinstance` where it is read. `object` never stands in for a shape you could name.
  - A shape with known members is a `TypedDict` or a model for data, and a `Protocol` for a behavioral interface.
  - Everything else takes the exact type or a precise union.
  - An override of a third-party signature typed `Any` takes `object` for its parameters and returns a generic or concrete type.
- Do not "fix" typing by expanding simple transformations into repetitive key-by-key copy blocks (for example, manually assigning each dict key only to satisfy pyright). Fix the source type hints (or add a precise cast/narrowing of our own types at the boundary) so the transformation can stay concise and readable.
- For persistence/update payloads (for example, `upsert(...)`), define a dedicated `TypedDict` and construct it inline at the call site. Do not add free-floating `build_*`/`make_*` helper functions whose only role is constructing a payload from another shape; the same no-free-floating-builders rule that applies to `BaseModel` applies here.
- Build every `TypedDict` value by **calling** its constructor with keyword arguments (`WidgetUpdate(field=value, ...)`), never by annotating a plain dict literal (`name: WidgetUpdate = {...}`) or passing a bare dict where the parameter is typed. That covers module-level constants and shared blobs, nested rows inside lists (for example `CompoundVariantRule(match={...}, class_name="...")`), and an SDK's typed request parameters and options at every level of nesting (`sdk.params.WidgetCreateParams(owner=sdk.params.WidgetCreateParamsOwner(...))`, `sdk.RequestOptions(idempotency_key=key)`). Tests assert with the same constructors. This keeps the type as the construction site, not only a static annotation on a dict literal.
- **No name you write or reference carries a `TypedDict` suffix.** Name a TypedDict for the shape it holds (`WidgetUpdate`, never `WidgetUpdateTypedDict`), and where an SDK ships a model class beside a `…TypedDict` twin of the same request, pass the model class.

- Group parameters that always travel together and describe one concept into a single typed object, then pass that object rather than threading its fields through every signature and call site.

```python
from typing import TypedDict


class RequestContext(TypedDict):
    source_address: str | None
    client_name: str | None


# Bad: related values threaded as separate arguments
def record_event(event: Event, source_address: str | None, client_name: str | None) -> None:
    ...


# Good: one typed object describing the shared concept
def record_event(event: Event, request_context: RequestContext) -> None:
    ...
```

- Use `datetime` objects instead of raw integers (Unix timestamps) for representing time.
- Use `timedelta` for durations instead of raw integers (for example, `timedelta(seconds=10)` instead of `10`).
- For database columns, use `DateTime` or `Date` types from SQLAlchemy.
- For Pydantic models, use `datetime.datetime` or `datetime.date` types.

- Use a leading underscore **only** for nested definitions: a function defined inside another function or method (inner function), and a class defined inside another class (inner class).
- Everything else must **not** start with a leading underscore. This includes module-level functions, classes, Pydantic/ORM models, enums, `TypedDict`s, type aliases, and constants; **methods** (instance methods, `@classmethod`, and `@staticmethod`); and **module / file names**.
- Do not use a leading underscore to mark a method or a module-level helper as "private". Express privacy through module boundaries and `__all__` instead.
- This rule does not govern Python dunders (`__init__`, `__enter__`, …) or single-underscore names owned by third-party/stdlib code.

```python
class Report(BaseModel):
    @classmethod
    def from_rows(cls, rows: list[Row]) -> Self:
        def _format_row(row: Row) -> str:
            return f"{row.id}: {row.name}"

        return cls(lines=[_format_row(row) for row in rows])
```

- Use `Enum` for named internal states. Use `StrEnum` when the string values themselves are part of
  a persisted, serialized, or external contract; format presentation text at the output boundary.

## Imports and Modules

- Before adding a module, inspect the existing owner and its consumers. Extend that module when the new code shares its responsibility, dependencies, and lifecycle; a new operation, small helper, record shape, or compound name does not establish a new boundary. Split only when distinct ownership, dependency direction, or independently used surfaces justify the extra navigation, and consolidate fragments that have no such distinction.
- Use an owner package when several justified modules share that owner; do not convert a module into a package merely because it gains another function or topic. Inside the package, name modules for their responsibility without repeating the owner. Keep established compound nouns together.
- Keep every `__init__.py` empty or limited to explicit re-export imports and a literal `__all__`, including in test packages. Never add definitions, data declarations, computation, or side effects there; they belong in ordinary modules under their responsible owner. A package's public export surface and module-layout rules do not permit implementation in its initializer.
- This rule governs Python modules only. Generated packages and source files owned by another toolchain follow that toolchain's naming conventions.
- Moving a module into a new subpackage invalidates every relative import inside it and any path it derives from `__file__`. Convert those imports to absolute imports and re-anchor the path instead of adding `.parent` until it happens to work.

- Give domain-specific module-level parsers, builders, formatters, and validators domain-qualified names. A generic name such as `parse_response` or `build_payload` falsely promises that a domain helper accepts any compatible input and creates collisions when multiple domains are imported together.
- Reserve unqualified transformation names for genuinely domain-independent helpers in `utils/` whose signatures name no domain type.

- **Import the symbols you use, never the module they live in.** `from pkg.domain import thing` followed by `thing.do_work(...)` reads differently from every neighboring call, hides which of the module's names this file actually depends on, and is the shape an alias ban pushes people into when a name collides. A module import is correct only for a module you genuinely pass around as an object.
- **A collision between a caller and the callee it invokes is a naming defect, not an import problem.** When `do_work` in one layer calls `do_work` in the layer below, the two names claim to describe the same thing while one of them adds behavior the name never mentions. Rename the callee so each layer says what it alone does — the caller's name is usually fixed by an external contract, and the callee's is not.
- Reaching through the module to dodge that collision preserves the defect and hides it. So does aliasing. Fix the name.

```python
# Bad: the collision is real, and reaching through the module only conceals it
from billing.invoice import gateway


async def pay_invoice(invoice_id: UUID) -> Payment:
    ...
    return await gateway.pay_invoice(invoice_id=invoice_id)


# Good: the gateway says it crosses a service boundary, so both names can coexist
from billing.invoice.gateway import pay_invoice_in_ledger


async def pay_invoice(invoice_id: UUID) -> Payment:
    ...
    return await pay_invoice_in_ledger(invoice_id=invoice_id)
```

- Keep all imports at the top of the file.
- Never import inside functions, methods, or test cases.
- Group imports: stdlib, third-party, local (separated by blank lines).
- Prefer **absolute imports** from the top-level package (for example `from application.routes.resources import resources_router`) over **relative imports** with parent segments (for example `from ....routes.resources import resources_router`). Absolute imports are stable when modules move, easier to grep, and avoid brittle `..` depth. Same rule applies to other installable packages: always anchor imports on the package name, not on the file’s directory depth.
- Never use import aliases for project modules; import the canonical symbol/module name and update call sites to that name instead of aliasing. The one form that is not a rename is the explicit re-export marker `from pkg.module import Name as Name`, which PEP 484 defines as a package declaring `Name` part of its own public surface. Use it only in a package's `__init__.py` alongside `__all__`, never to give a symbol a second name.
- Never define variables or call functions in between import statements; all imports must be contiguous at the top of the file.
- Never create shim modules that only re-export symbols from another package for backwards compatibility; update all consumers to import from the canonical source instead.
- **A folder holding one module is not a folder.** `thing/thing.py` costs every reader a directory
  hop and every importer a longer path, and buys nothing the bare `thing.py` did not already give.
  Collapse it: the module moves up, the package goes away, and the import shortens.
- Keep the folder only when the topic genuinely has more than one module in it, or when the split
  is already drafted and imminent — a package created for a second module that does not arrive is
  the same defect a month later.
- **A folder naming a category the codebase will keep extending is the exception, and it earns its
  place on the first member.** A directory for third-party adapters holds one today and another the
  next time a framework is supported; the name states the axis, so a reader knows where the next one
  goes and no rename is needed when it arrives. That is a decision about the category, not a
  prediction about one file.
- **So is a folder that fences off code the shipped source does not use** — test helpers, fixtures,
  and other scaffolding a consumer imports but the library never does. There the folder marks a
  boundary rather than a topic, and it holds at one module because the boundary is the point.

```python
# Bad: one module behind a package that adds only a hop
mypackage/
    validation/
        __init__.py
        validation.py

# Good: the module stands on its own
mypackage/
    validation.py

# Good: the category will hold more, and says where the next one goes
mypackage/
    adapters/
        __init__.py
        redis.py
```

- Place generic, stateless, cross-cutting helpers in a `utils.py` module or `utils/` package.
- Use a `utils.py` module for a small cohesive set of utilities; use a `utils/` package when separate focused utility modules are warranted.
- Keep owner-specific helpers with their existing domain owner. Use its utility submodule only when the responsibility/dependency test above justifies that boundary. Place independently reusable cross-cutting topics under an existing utility owner; a filename alone never requires a move or package.
- Give a `utils/` package topic-named modules rather than one flat module.
- Consumers of a `utils/` package import from the specific submodule.
- Keep domain and orchestration behavior in their owning modules. Do not use utilities as a dumping ground.
- Narrow exception: `__main__.py` entrypoints may use same-package relative imports for bootstrap (for example `from .runtime import main`), and `__init__.py` may use explicit relative imports when assembling the package’s public surface.

### Entrypoints

- Keep command-line parsing and execution together in `__main__.py`; do not create a separate `cli.py`
  or a trivial `main()` wrapper solely to delegate from the module guard.
- Invoke package CLIs with `python -m <package>` when no independently reusable console entrypoint is
  required.
- Do not layer `run()`, `main()`, and an `if __name__ == "__main__":` guard for the same entrypoint.
- Model reusable command outcomes with a descriptive enum. Convert that outcome to an integer exit code only at the CLI boundary; never carry or return bare status integers through application code.

```python
# Bad: shim module that only re-exports symbols
from .http_transport import fetch, fetch_with_cache

__all__ = ["fetch", "fetch_with_cache"]

# Bad: consuming through a shim module
from myapp.http import fetch

# Good: import from the canonical source directly
from myapp.http_transport import fetch
```

## Suppressions

- **Never add an inline suppression**: no `# pylint: disable`, `# pyright: ignore`, `# type: ignore`, or `# noqa` — except on the outermost-wrapper catch-all the Python boundaries rule's **External APIs and Errors** allows. Fix what the checker reports about our own code — a precise annotation, a correctly typed decorator (a `ParamSpec` rather than a `Callable` that erases parameter names), the right import. A per-line disable reads the same whether its author weighed the finding or never looked, and once copied onto every sibling it hides the cause behind a pattern nobody questions.
- **A third-party package's missing or incomplete types are that package's gap, never ours.** Write
  no stub file, `typings/` directory, cast, wrapper, checker plugin, inference transform or script to
  quiet them or to teach a tool a third-party construct it misreads, and delete any that exists together with its tests; the answer is the category-wide
  configuration entry below, never code. A package the user owns is not third-party wherever it
  lives: its types are published at its source — a `py.typed` marker and the annotations its public
  surface needs. Read ownership from whose repository it is.
- A category is turned off once in the tool's configuration, or filtered once by the repository's
  lint gate, with its reason beside it, in two cases: it reports a third-party package's missing or
  unknown types, or it misreads a construct the codebase deliberately relies on everywhere — a
  third-party library's generic annotations on the codebase's models, or coroutines implementing a
  generated synchronous base, say. It applies to every package and every
  file, never to one named package. A category turned off for dependencies is off for our own code
  too; the checks that stay on, such as argument types and annotations on our own functions, keep
  our own errors reported. Code a generator emits keeps whatever directives its generator writes.

## Constants

- Group dependency-independent module constants, enums and type aliases after imports, before functions and classes. A declaration that needs a class or other runtime definition follows that prerequisite, before the next unrelated definition; do not scatter independent constants between functions.
- When assembling a structured string from variable parts, define one named template and use `str.format(...)` rather than composing separate prefix and suffix constants. Use native template strings only when they are supported across the project's full Python version range.
- Use `Final[T]` from `typing` and UPPER_SNAKE_CASE names for constants.
- Compile regular expressions once at module scope and call methods on the compiled pattern instead of passing pattern strings repeatedly to `re.match`, `re.search`, `re.fullmatch`, or `re.sub`.
- **When several constants form one family of the same shape** — parallel compiled patterns, per-kind values, same-shaped lookup entries — define one mapping keyed by an enum or other typed key instead of a pile of individually named constants, and iterate or index that mapping at the use site. A few unrelated constants are fine as standalone names; a family of related ones is a data structure. The family test is what the constants configure, never their types or a shared name prefix: several things each set up by the same settings — locks and rate limiters each with a key and a window — are one mapping keyed by an enum of those things, each entry a small model holding that thing's settings, so every entry has the same shape. Adding another constant to such a run is the moment to convert it, never to extend it.

```python
# Bad: a parallel pile of same-shaped constants
CREATED_EVENT_PATTERN: Final[re.Pattern[str]] = re.compile(r"^created:")
UPDATED_EVENT_PATTERN: Final[re.Pattern[str]] = re.compile(r"^updated:")
REMOVED_EVENT_PATTERN: Final[re.Pattern[str]] = re.compile(r"^removed:")

# Good: one mapping keyed by the domain enum, iterated at the use site
EVENT_PATTERNS: Final[dict[EventKind, re.Pattern[str]]] = {
    EventKind.CREATED: re.compile(r"^created:"),
    EventKind.UPDATED: re.compile(r"^updated:"),
    EventKind.REMOVED: re.compile(r"^removed:"),
}
```
- When a mutable object is annotated with `Final`, complete any setup-time mutation in the same expression as initialization instead of binding it first and mutating it on the next line.
- Only extract literals when they are reused or carry domain meaning; keep trivial single-use literals inline (for example, delimiters like `"-"` or `"."`).
- Never hard-code constants like HTTP status codes; use `HTTPStatus` from the `http` module instead.
- Prefer enums for error identifiers/messages instead of a constant per error string.

- **Never commit development or test secret values into application or library code** — not even to compare against them. Embedding a known dev key (or its hash) so the code can reject it just moves the secret *into* the codebase, which is the opposite of the goal. Real secrets live in the secrets manager; test secrets live in test configuration (`pyproject.toml` env), never in `.py` source.
- **Do not branch on the environment in application code to relax or vary security posture** (`if ENVIRONMENT == "development": allow the weaker cipher / skip the check`). Which crypto backend, keys, and credentials are used is a deployment concern: production sets the real backend and secrets, tests set test values via test config. Application code states the single required contract (for example "tokens are signed by the managed key service") and lets it hold everywhere.
- **Let the owning library validate its own contract; do not duplicate it behind an environment gate.** If a third-party SDK already requires a key for its selected method, do not re-implement that check in our config with environment branches — that is redundant and drifts.

## Functions and Interfaces

Avoid trivial wrapper functions that add no value. A function that just returns its argument or applies a trivial fallback is noise:

- **A function whose body is one call to the canonical function is banned**, whether it forwards the arguments unchanged or supplies a fixed value for one of them. Call the canonical function directly at the use site and name the argument there. Partial application does not earn a name: `send_welcome_email()` wrapping `send_email(template=WELCOME)` reads as a layer while adding none, and the wrapper has to be opened to learn what it does.
- The pressure to write one usually comes from several call sites passing the same constant, which is not a defect on its own. Where the argument genuinely must not vary, encode that in the callee's signature or its type — do not station a wrapper in front of it to hold the value.
- The same rule applies to third-party constructors and functions: call their native operation directly with the required arguments. An external signature does not justify a fixed-argument forwarding helper.
- Return `bool` for binary domain outcomes; never return integer `0` or `1` as a boolean substitute. Translate booleans into process exit codes only at the CLI boundary.
- Return an enum for an outcome with more than two states or states whose names carry meaning. Never return bare integers as application status codes.
- A subprocess return code is an external value and may remain an `int` at that boundary. Convert it into the domain outcome enum before carrying it through the application.
- Do not rebind function arguments to a second local name when the value is unchanged (for example, `profile = obj`); name the parameter correctly at the signature instead.
- When omission and an explicit `None` have different meanings for a parameter, use one reusable `Undefined` sentinel from a neutral shared owner; do not define a database-, transport-, or feature-specific sentinel for a general presence distinction.
- **Name a guard for the condition it asserts, not for the outcome it prevents.** A function that
  raises when an invariant is broken is named `assert_<invariant>`, so the call site reads as the
  condition that must hold. Prose names built around the refusal — `refuse_dropping_the_last_key`,
  `prevent_orphaned_record` — describe the failure rather than the rule, and a reader has to
  reconstruct the invariant from the sentence before knowing what the call guarantees.
- Keep the assertion truthful: the name states what the guard actually checks, never a broader
  property it does not establish.

```python
# Bad: the name narrates the outcome it is avoiding
def refuse_dropping_the_last_key(key: ApiKey) -> None:
    ...


# Good: the name states the condition that must hold
def assert_revocable_key(key: ApiKey) -> None:
    """Refuse to revoke the account's only active key."""

    if key.is_only_active:
        raise DomainError("An account keeps one active key.")
```

- Prefer normal attribute assignment over `object.__setattr__(...)` when mutating Pydantic models in validators or helper methods.
- Only use `object.__setattr__(...)` when normal assignment is genuinely unavailable (for example frozen models or descriptor bypass requirements), and keep that escape hatch explicit and justified.

```python
# Bad: a wrapper that only fixes one argument
def notify_owner(account: Account) -> None:
    return send_notification(account, channel=Channel.EMAIL)


# Good: the call site names the argument
send_notification(account, channel=Channel.EMAIL)


# Good: call the third-party constructor directly
ExternalColumn(column_name, ExternalTimestamp(with_zone=True), track_history=True)


# Bad: useless wrapper
def resolve_config(config: Settings | None) -> Settings:
    return config or APPLICATION_CONFIG

def get_auth_secret(config: Settings | None = None) -> str:
    resolved = resolve_config(config)  # Unnecessary indirection
    return resolved.SECRET

# Good: inline the fallback
def get_auth_secret(config: Settings | None = None) -> str:
    resolved = config or APPLICATION_CONFIG
    return resolved.SECRET
```

## Control Flow and Collections

- Combine conditional branches with `or` when they have the same body (including separate `if` statements and `if`/`elif` chains).
- Do not use an `if`/`else` block just to choose which attribute or mapping values to read. When the goal is only to select a source object and then read the same fields, resolve the source once with `or` and read from that single variable.

```python
# Good: combined conditions in one branch
if not principal.scope_id or principal.scope_id != scope_id:
    raise PermissionError("Principal cannot access this scope")

# Bad: separate branches with identical bodies
if not principal.scope_id:
    raise PermissionError("Principal cannot access this scope")

if principal.scope_id != scope_id:
    raise PermissionError("Principal cannot access this scope")
```

```python
# Good: resolve the source once, then read fields once
request_payload = request or {"name": ""}
resolved_name = request_payload["name"]
resolved_slug = request_payload.get("slug") or ""

# Bad: duplicated field extraction across branches
if request is None:
    resolved_name = ""
    resolved_slug = ""
else:
    resolved_name = request["name"]
    resolved_slug = request.get("slug") or ""
```

- For find-first patterns, use `next()` with a generator expression instead of a `for` loop with a nested `if` and early `return`/`break`.
- For filtering, prefer generator expressions or `filter(...)` over `for` loops that conditionally append to a list.

```python
# Bad: for loop with trivial nested if for find-first
for item in items:
    if item.id == target_id:
        return item.value

# Good: next() with generator expression
return next(
    (item.value for item in items if item.id == target_id),
    None,
)
```

- **Dispatch on one subject with `match`.** Any sequence of conditionals that tests the same subject against several enum members, literal values or discriminant values is a `match` statement, whatever shape the sequence takes: an `if`/`elif` chain, or consecutive `if subject is Member: return ...` guards followed by a fallback return. Each tested value becomes a `case`, and the fallback becomes `case _`.

```python
# Bad: early-return guards on one subject
if self is Shelf.FICTION:
    return "A-F"
if self is Shelf.REFERENCE:
    return "R"
return None

# Good
match self:
    case Shelf.FICTION:
        return "A-F"
    case Shelf.REFERENCE:
        return "R"
    case _:
        return None
```

- For data-driven column/field selection with many independent boolean flags, prefer a declarative mapping iterated in a loop over repeated `if` blocks.
- Use enums with descriptive string values for column names, header labels, and other user-facing strings instead of raw string literals scattered across functions.

## Logging

- Use the `logging` module instead of `print()` for debugging, status, progress, or diagnostics in any code, including scripts and CLI tools.
- Configure logging once, centrally at the application or script entry point; each ordinary module only creates its logger at the top: `logger = logging.getLogger(__name__)`.
- Treat logger instances as runtime collaborators: name them `logger`, never `LOGGER`, and do not annotate them as `Final`.
- Use appropriate log levels: `debug`, `info`, `warning`, `error`, `critical`.

## Guardrails

- Do not remove intentional feature logic merely because it looks extra; verify the active request, nearby tests, and call sites before deleting newly added code.
- If style-cleanup instructions conflict with clear feature intent, preserve behavior first and ask a clarifying question instead of removing the feature code.
