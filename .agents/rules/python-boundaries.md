---
description: Apply when changing Python settings, client injection, model placement, caching, external API calls, or error handling.
alwaysApply: false
paths:
- '**/*.py'
---

# Python Boundaries

## Configuration

- Define each configuration owner's settings in one descriptively named `BaseSettings` class such as `ActionConfig` in its `config.py`. A repository may have distinct application, worker, or script configuration owners; do not combine unrelated settings merely to produce one repository-wide class. Keep each config module declarative: instantiate its settings once at that owner's composition boundary, then pass or import that validated object wherever settings are needed.
- Put a value in that settings class when, and only when, its owner is likely to change it on its own — per deployment, per environment, per release, or while running the system — without changing the code that reads it. What kind of value it is never decides this: a timeout, retry count, or batch size the owner expects to revisit is configuration exactly as a credential, a host the deployment chooses, or a feature switch is. Every other value — one nobody expects to change except together with the code that reads it, including every value that code's correctness fixes, such as a pattern it parses with or a format or limit a protocol defines — is a typed module constant beside that code. Where the evidence settles neither side, the value stays where its owner put it.
- Give configurable values typed defaults when the repository has a safe default, as `pre-production`'s **Configuration** defines one, and let `pydantic-settings` load environment values using the settings names governed by the Pydantic rule.
- Use `TypedDict` only for static structured data that is not configuration.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class ActionConfig(BaseSettings):
    model_config = SettingsConfigDict(frozen=True)

    application_tool_cli_version: str = "1.2.3"
    application_service_base_url: str = "https://api.example.com"


# application.py or another composition boundary
APPLICATION_CONFIG = ActionConfig()
```

- Before declaring or reviewing a setting, read its supported operations, consumers, and example/test configuration. A setting `pre-production`'s **Configuration** makes required, including an endpoint, API key or secret, is a required non-nullable Pydantic field with a nonempty field constraint, never `str | None = None` or an empty-string default. Declare a field optional only for the documented absence contract that section allows, at the settings class, never through a missing-value check in a consumer.
- Do not add useless config values like `DEFAULT_ENVIRONMENT`.
- A provider's published sandbox and production hosts are constants in that provider's package, and the application's canonical environment check selects between them. Select a provider's host from that check (such as the settings object's `is_production`), never from a provider-specific environment setting or enum that restates what the deployment environment already decides.
- Do not add helper functions like `_get_environment` when the value already exists on the shared settings object.
- Do not read environment variables directly with `os.getenv`, `os.environ`, or `os.environ.get` in application/service/library code.
- Always read environment-backed values from the typed settings object so defaults, validation, and normalization live in one place.
- **A function whose behavior depends on a setting reads that setting itself.** No parameter carries in a configuration value, or a value derived from one such as an environment check, that a caller read from the settings object — not at many call sites and not at one: `render_receipt(order, show_debug_footer=not APPLICATION_CONFIG.is_production)` is `render_receipt(order)` reading the check inside, and a model method such as `order.is_refundable(window=APPLICATION_CONFIG.refund_window)` is a property `order.is_refundable` reading it. The same holds for any value every caller would take from one shared source: read it from that source where it is used. A test sets the setting through the settings it runs with, never through an argument added for it.
- Exception: one-off scripts may read from `os` when introducing a settings model would be unnecessary overhead.

## Architecture and Boundaries

### Client Dependency Injection

- Pass runtime clients and other stateful collaborators explicitly through constructors or function parameters. Do not hide them behind module globals, service-locator getters, or default parameter values.
- Centralize dependency-container wiring at the application boundary. Request-scoped frameworks may inject clients into routes, while worker, RPC, and tool entrypoints receive their long-lived collaborators from startup wiring.
- Keep one patchable client seam at the owning boundary rather than requiring tests to patch a separately imported client in every consumer module.

### Model Placement

- Define Pydantic `BaseModel` classes and other application data models under the package's `models/` directory.
- Split models into intuitively named files by concept, such as `models/configuration.py` or `models/submission.py`.
- Do not place models beside operational code or collect unrelated models in a catch-all `models.py` module.

- A declaration that describes one external provider — its enums, request and response models, host constants — lives in that provider's package beside its other models, never in a service-wide `core/` or shared enums module. A core enums module holds only the application's own domain vocabulary.

- Files under a `models/` package contain only declarative models, enums, and behavior intrinsic to validating or representing those models. Do not put runtime registries, mappings, instantiated collaborators, filesystem layouts, I/O, or orchestration in model files.
- Put runtime mappings and operational behavior in the module that owns their use. A typed `config.py` built with `pydantic-settings` is the explicit exception for the repository's settings class only; instantiate that class at the application or script composition boundary.

- Do not convert between models you own with `Target(**source.model_dump())`, `Target.model_validate(source.model_dump())`, or `Target(**source.__dict__)`. These dictionary-shaped conversions erase the relationship between the source and target contracts, can collide with explicitly supplied fields, and may re-run normalization or encryption.
- Put the conversion on the target in a typed `from_<source>` or `build_*` classmethod that names the fields. If the copy becomes long, consolidate the models or carry the source model as a nested field instead of flattening it.
- Reserve `model_dump()` for boundaries that leave the typed model layer, such as JSON, persistence, caches, and logs.
- **A value with one canonical form is normalized once, by its field's type on the model.** A case-insensitive identifier such as a username or a hostname, or a code kept trimmed and upper-case, is declared with an annotated type or validator on the model, or a column type that normalizes on write, so every value the model holds is already canonical. Service code never calls `.lower()`, `.strip()` or the like on it, since one call site that misses the call is a bug; input compared against it goes through the same type. Rows already stored are migrated to the canonical form with the change, as `database-migrations` says.

```python
Hostname = Annotated[str, AfterValidator(str.lower)]


class Mirror(BaseModel):
    hostname: Hostname
```

- Application code (a function, method, property, class, constant, or field) with **zero non-test consumers** is dead code and must be deleted, along with the tests that only exist to exercise it. Consumers, and the writers a guard below is checked against, are counted where the change will land, as `code-simplify`'s rubric says.
- **Tests do not justify keeping otherwise-unused application code.** A test that asserts a symbol no other application code reads is testing a fabricated contract; delete the symbol and that test together rather than preserving the symbol "because it's covered".
- "Consumer" means live application/library code that reads the symbol — call sites, internal use by another live symbol, serialization, or a public package export in `__all__` that external packages import. Test modules are not consumers.
- A symbol reached only indirectly through another symbol that is itself dead is also dead; remove the whole unused chain.
- A guard, validation, or branch for a state no writer can produce is dead code too. Before adding one, read every path that creates or changes the value it tests, concurrent writers included, and what its path reads next; when they already exclude the state, or a check already on the path refuses every input the guard would, leave the guard out, with its message constant and its tests. An earlier check refuses only what held when it ran: when another request or transaction can change the value between the two, across an `await`, a lock wait, a transaction boundary, or the gap between a read and the write or debit that depends on it, the later check, including a re-read after acquiring the lock, is the one that decides and is not a duplicate.
- Defense in depth, a clearer status code, and a future writer are not reasons to keep such a guard: a writer that could produce the state carries its own check.
- Where the state is reachable, the check goes on every sibling path answering the same question, not only the new one.
- **Settings fields that populate environment variables consumed by a third-party library are not dead code**, even when no application code reads the field directly. If a dependency we rely on reads an env var at runtime (for example a library whose `Settings` reads `ENCRYPTION_METHOD`/`ENCRYPTION_KEY`), the field must stay on the shared settings object so the application sets that env var — the library is the consumer. Keep such fields and validate them where the environment requires it.

- For values persisted in databases, queues, or cross-service contracts (for example handler names, event names, state keys), use explicit constants or enums.
- Do not derive durable identifiers from implementation details like `function.__name__`.
- Keep durable identifiers in shared model/contract modules when they are used across services.

```python
from enum import StrEnum


class TaskHandlerKey(StrEnum):
    PROCESS_RESOURCE = "process_resource"

# Good: explicit durable key
register_task(task_type=TaskType.PROCESS_RESOURCE, handler_name=TaskHandlerKey.PROCESS_RESOURCE.value)

# Bad: fragile runtime-derived key
register_task(task_type=TaskType.PROCESS_RESOURCE, handler_name=handler.__name__)
```

- Avoid monolithic service modules that mix orchestration, third-party API calls, policy decisions, and data mappers.
- Split large services into focused modules, for example:
  - orchestration module (route-facing flow)
  - gateway module (external/internal API client calls)
  - domain helper modules (policy/state decisions, AI resolution, etc.)
- Keep public service function signatures stable while refactoring internals.
- **No upward imports**: `lib/` must never import from `services/`. Shared infrastructure both layers need (client factories, session wiring, config) lives in `core/`, which either layer may import.
- **Orchestration does not live under `lib/`**: a module whose functions are route-facing entry points (they accept request-shaped inputs and return response models) belongs in `services/`, even if it started life as a helper. Keep the pure helpers (query builders, row/CSV machinery, mappers) in `lib/` and move only the orchestrator.
- **A transport-only "service" is a gateway**: a `services/` module whose functions only wrap internal-service or external API calls belongs in `lib/<domain>/gateway.py`; keeping it under `services/` invites upward imports from other lib modules.

- When multiple functions compute the same derived state (for example completion/missing stage lists), centralize that logic in one helper.
- Reuse the helper across read paths to avoid behavior drift.

- Keep external calls at their owning dependency boundary; tests patch the binding that boundary already reads rather than adding a forwarding helper solely as a patch target.
- **Patch the consuming module's own binding, not the module that defines the symbol.** A symbol import binds the object at import time, so the consumer holds its own reference: patching the defining module rebinds a name the consumer never reads again. Nothing raises, the mock never fires, and the test passes while asserting nothing.
- Patch the shallowest seam the consumer actually reads, rather than an internal several calls below it.

```python
# consumer.py binds the object at import time
from billing.ledger.gateway import charge_card

# Bad: resolves cleanly, rebinds a name consumer.py no longer reads, mock never fires
monkeypatch.setattr("billing.ledger.gateway.charge_card", mock)

# Good: rebinds the reference the consumer actually calls
monkeypatch.setattr("billing.consumer.charge_card", mock)
```

## Runtime Data and Caching

- Never use plain dictionaries (module-level, class-level, or any other in-process container) as caches for data that must stay correct across requests, workers, or deployments. In-process dict caches silently go stale, diverge between workers, and cannot be invalidated remotely.
- For cross-request or cross-process caching, use a distributed caching library such as Redis or the repository's shared caching layer, and always set an explicit TTL.
- Pair every cache write path with an explicit invalidation path for mutations that change the cached value.
- Request-scoped memoization is the only acceptable dict-shaped cache: it must be held in a `ContextVar`, reset at the start of every request, and invalidated on writes within the request.

- Use `@cache` (from `functools`) for expensive, deterministic builders that should be created once per process (for example, AI agents, parsed static configs, immutable lookup tables).
- Only cache functions whose return value is safe to reuse and does not depend on request-scoped state.
- Do not cache values that depend on mutable runtime inputs (per-request user data, DB sessions, auth context, timestamps).
- Keep cached builders side-effect free and parameter-light.

```python
from functools import cache

@cache
def build_classification_agent() -> Agent[None, ClassificationResult]:
    return Agent(...)
```

## External APIs and Errors

- Run a synchronous SDK's calls off the event loop (for example with `asyncio.to_thread`) when the application is asynchronous.
- Verify SDK method availability before coding integrations:
  - Prefer checking the official docs, or
  - Inspect the installed SDK directly (for example with Python `inspect`/`hasattr`) in the current environment.
- Do not add defensive attribute checks or fallback branches for third-party SDK methods (for example, catching `AttributeError` to try an alternate call path).
- Call the expected SDK method directly; if the integration changes, update it explicitly rather than supporting multiple speculative shapes in runtime code.

```python
# Bad: speculative fallback for a "maybe async, maybe sync" SDK shape
try:
    resources = await sdk.resources.list_async(
        scope_id=scope_id,
        resource_id=[resource_id],
        limit=1,
    )
except AttributeError:
    resource = sdk.resources.get(
        scope_id=scope_id,
        resource_id=resource_id,
    )

# Good: call the expected method directly
resources = await sdk.resources.list_async(
    scope_id=scope_id,
    resource_id=[resource_id],
    limit=1,
)
```

- Never insert fabricated placeholder values (for example `user-{id}@blank.com`) into database columns in application code to satisfy NOT NULL or UNIQUE constraints.
- If a required field is unavailable at a code path, fetch the real value from its authoritative source (for example an external identity provider API) or make the caller supply it.
- Placeholder backfills for legacy data belong exclusively in database migrations, not in runtime service logic.

- Implement only the single contract used by the current boundary (database schema, SDK contract, or API model).
- Do not widen types or add compatibility branches for alternate shapes that are not part of the real contract.
- Example: If the DB column type is `UUID`, function parameters and call sites should use `UUID` only (not `UUID | str` with runtime conversion).
- Prefer fixing call sites to provide the correct type over adding defensive conversion logic in core helpers.

```python
# Bad: backward-compatible branch for an unsupported secondary shape
async def get_source_id(session: AsyncSession, resource_id: UUID | str) -> str | None:
    resolved_resource_id = UUID(resource_id) if isinstance(resource_id, str) else resource_id
    resource = await Resource.get_one(session, where=Resource.id == resolved_resource_id)
    ...

# Good: single, complete implementation aligned to DB contract
async def get_source_id(session: AsyncSession, resource_id: UUID) -> str | None:
    resource = await Resource.get_one(session, where=Resource.id == resource_id)
    ...

# Good call site: convert once at boundary
raw_resource_id = response.json()["data"]["resource_id"]
source_id = await get_source_id(session, UUID(raw_resource_id))
```

- Read required data from its single canonical source — an SDK catalog/list call, a typed config value, a generated client — and use it directly. The implementation must be complete against that source, not hedged with a fallback.
- Do not wrap a canonical lookup in a `try`/`except` that swallows the failure and continues with a guessed value, a default, or a degraded mode. That hides drift and turns a real outage into silently wrong behavior. Let a genuine failure propagate to the normal error path so it fails loudly and gets fixed at the root.
- Handling a legitimate, expected *state* of the canonical data is fine (for example, a catalog entry that has no optional variant, so you use the base value). Inventing a substitute when the source is *unavailable or malformed* is not.
- If you catch yourself writing "if the lookup fails, use X instead", the fix is to make the lookup reliable (or to fail), not to paper over it with a fallback branch.

```python
# Bad: swallow a catalog failure and silently degrade to the default behavior
try:
    catalog = await client.list_models()
    variant = pick_variant(catalog)
except SomeError:
    variant = None  # silently falls back to the wrong/default behavior

# Good: use the canonical source completely; a real failure propagates to the caller's error path
catalog = await client.list_models()
variant = pick_variant(catalog)
```

- Use `HTTPStatus` enum from the `http` module instead of raw integer status codes.
- Import as: `from http import HTTPStatus`.
- Use your framework's standard error response type instead of hand-rolled JSON response bodies when the project already defines one.

```python
from http import HTTPStatus

# Good: use a typed or framework-standard error response
raise HttpError(
    status_code=HTTPStatus.NOT_FOUND,
    detail="Resource not found",
)

# Bad: using raw integer status code with JSONResponse
return JSONResponse(
    status_code=404,
    content={"error": "Resource not found"},
)
```

- Never catch bare `Exception`; always catch specific exception types, with two exceptions: a test case explicitly exercising that broad exception, and an outermost wrapper — the loop running a worker's jobs, the boundary serving a request — that logs the error with its traceback and turns it into a failure result, its broad-catch lint finding disabled on that line alone. Lint keeps flagging every other catch-all.
- For generated or SDK-backed API clients, catch the library's documented exception type instead of broad exceptions.
- **A function that raises owns the message for the condition it refuses.** One condition has one message, written where the error is raised; no parameter carries error text in, and callers that each want their own wording for the same refusal share that one message, such as "Too many results to show. Narrow the search and try again." A fact the message needs, such as the limit, goes in as data the message formats, never as a sentence. A caller that must tell two refusals apart does so by error type, never by message.

```python
import third_party_client

# Good: catch specific exception
try:
    response = await client.get_resource(...)
except third_party_client.ApiException:
    logger.exception("Resource API call failed")

    raise

# Bad: catch all exceptions
try:
    response = await client.get_resource(...)
except Exception as exc:
    logger.warning("API call failed: %s", exc)
```
