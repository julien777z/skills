---
description: Use APIRouter-based route organization, validate in models, and keep response handling consistent.
globs:
- '**/*.py'
alwaysApply: false
paths:
- '**/*.py'
---

# FastAPI Rules

## Layering: routes → services → lib

- Each app follows one dependency direction: `routes/` → `services/` → `lib/` → generated clients / ORM. Never invert it.
- Layer ownership:
  - `routes/`: `@<surface>_router.<verb>(...)` handlers and the `<surface>_router = APIRouter(...)` declaration, naming the dependencies each handler takes. No business logic, and no dependency alias of its own.
  - `services/<surface>.py`: route-facing orchestration (multi-step flows, policy decisions that span calls, response assembly) and FastAPI dependency functions. Sub-split large surfaces into a `services/<surface>/` package with topic-named modules and an empty `__init__.py`; consumers import the specific submodule.
  - `lib/<domain>/`: gateways (internal-service transport), persistence helpers, caches, and policy/domain helpers with no route-facing signatures.
- **One call per handler**: a handler makes exactly one service call (for flows with policy or orchestration) or one lib-gateway call (pure pass-through). If a handler stitches two calls together, branches on an intermediate result, or shapes data between calls, that orchestration belongs in a service function (for example: fetch → transform → respond, reject → notify, or validate → perform).
- **No data access or response shaping in handlers**: a handler must not query or persist data directly, nor assemble response models from raw rows or records inline; extract a service function that returns the response model and keep the handler to wrap-and-return.
- **An `Annotated` dependency alias belongs in the app's dependency module, never in a route file.** The alias names a guard rather than a route, so the next surface needing that guard either imports it or writes its own copy — and a route file is where nobody looks first, so it writes its own. Two files then spell the same protection two ways, and nothing makes them disagree loudly.
- Keep the whole set in **one module**, so the guards an app offers can be read in one place and a new route picks one instead of inventing it. Routes import each alias by name; the policy body it invokes still lives in `services/` or `lib/`.
- **A parameterized guard factory is one dependency, not a family of route aliases.** Define the factory in the app's dependency module and let a route compose its visible policy with `Depends(factory(...))`. The argument states the operation's policy at the call site; wrapping every argument in a named alias would recreate the duplicate guards this rule prevents.

```python
# Bad: the route file declares the guard it happens to need
RequireReportAccess = Annotated[None, Depends(require_permissions(Permission.VIEW_REPORTS))]


@reports_router.get("/summary")
async def get_report_summary(_: RequireReportAccess) -> ApiEnvelope[ReportSummary]:
    ...


# Good: the guard is declared once in the dependency module and imported by name
from application.dependencies import RequireReportAccess


@reports_router.get("/summary")
async def get_report_summary(_: RequireReportAccess) -> ApiEnvelope[ReportSummary]:
    ...
```

```python
# Good: the dependency module owns one reusable parameterized guard
def require_permissions(*permissions: Permission) -> Callable[..., None]:
    ...


# Good: the route states its operation-specific policy without defining an alias
@reports_router.get("/summary")
async def get_report_summary(
    _: Annotated[None, Depends(require_permissions(Permission.VIEW_REPORTS))],
) -> ApiEnvelope[ReportSummary]:
    ...
```

## Route Organization

- Use `APIRouter` for grouping related routes.
- Keep route handlers thin; delegate business logic to service modules in `services/`.
- Import the service functions a route file calls, by name. A route file that reaches through a service module hides which of its functions the file depends on, and a long symbol list is a signal the route file covers too many surfaces, not a reason to import the module.
- A handler that shares a name with the service function it calls is a naming defect. The handler name is the API contract (it becomes the OpenAPI operation id), so rename the service function for the domain operation it performs.
- Name every router for the surface it serves (`invoices_router`, not `router`), so the application entrypoint imports each one by name instead of reaching through its module.
- **One router per file.** A module declaring two or more `APIRouter(...)` objects is two or more surfaces sharing a namespace, and its handlers no longer read in one sequence — every reader has to track which router each decorator names. Give the surface a package instead, with one module per router named for that router's topic, and let the package `__init__.py` import each router by name and declare them in `__all__`.
- **One handler does not earn a router, and a router does not earn a module for one handler.** The
  rule above caps a module at one surface; it never promises that every handler is a surface. A
  router declared to carry a single operation is the module-per-function shape the Python rules ban,
  wearing a decorator: the reader looking for that operation searches the resource it acts on, and
  finds a file named after the operation instead.
- Put the handler on the router that already owns its resource, and give it a path **under** that
  resource rather than a sibling segment beside it. A body one record holds is read at
  `/records/{record_id}/body`, never at `/records/bodies/{body_id}` on a router of its own.
- A new router earns its place when it serves a resource no existing router addresses, or when it
  needs a prefix, tag, or guard the existing one cannot carry. A different verb, a different response
  model, or being the newest thing added is not that, and neither is expecting more handlers later —
  move it when the second one arrives.
- Where one router mounts another — a stage surface carrying an extra dependency, for example — do that `include_router` call in the package `__init__.py` beside the imports, not inside either router's own module.
- Name handlers for the domain action they perform: use `create_<resource>`, `update_<resource>`, and `leave_<resource>`, never HTTP-verb names or persistence-mechanics suffixes.
- Do not name route modules or routers `write`; name the domain topic they serve, such as `stages` or `invitations`. This does not apply to rate-limit configuration.
- Public routes expose reversible membership changes such as leaving an organization, not deletion of organizations or members; lifecycle deletion remains available only through the library surface that owns it.
- Include routers via a `for` loop over a tuple; for a single router, use a one-item tuple with a trailing comma.
- Route files should contain only `@<surface>_router.<verb>(...)` handlers and the router declaration; cache-key builders, response shapers, validation/transform helpers, shared sub-handlers, and dependency aliases belong in `services/`, `lib/`, or the app's dependency module.
- Do not place a non-routing module under `routes/` so other route files can import from it; helper modules belong in `services/` or `lib/`.

```python
for router in (resources_router, reports_router):
    app.include_router(router)
```

## Webhooks

- Inbound webhooks from external providers do not belong in `routes/` with the application's own API routers. Put them in a dedicated `webhooks/` package, organized by provider (for example `webhooks/provider_x.py`).
- Treat webhooks as a separate surface from the first-party API: they are authenticated by provider signature verification rather than the app's auth, carry provider-defined payloads, and follow different rate-limit rules (a per-user/per-IP limit would throttle a provider's single source IP). Keeping them out of `routes/` keeps that boundary clear.

## Parameters

- Use `Depends()` for dependency injection (database sessions, auth, etc.).
- Use `Body(...)` for request body parameters.
- Use `Path(...)` for path parameters.
- Use `Query(...)` for query parameters with defaults and validation.

## Request Validation

- Validate lengths/types in Pydantic request models, not in route handlers.
- Prefer dedicated field types from the project's shared model layer or from `pydantic` / `pydantic_extra_types` when they express the constraint clearly.
- Do not add runtime field-presence checks in route handlers or route-facing services for request-shape validation.
- Make required request fields required on the Pydantic model.
- Use `model_validator(...)` only when validity depends on multiple fields together. Do not add a model validator just to restate that independently required fields are required.

```python
from typing import Self

from pydantic import BaseModel, Field, model_validator
from pydantic_extra_types.phone_numbers import PhoneNumber


class VerifyPayload(BaseModel):
    phone_number: PhoneNumber
    retry_count: int = Field(ge=0, le=5)


# Bad: runtime request-shape validation in the route/service layer
if not payload.name or not payload.source_id:
    raise ApiError(status_code=HTTPStatus.BAD_REQUEST, detail="Missing required fields")


# Good: independently required fields are just required fields
class CreateResourcePayload(BaseModel):
    name: str
    source_id: str


# Good: use model_validator only for cross-field rules
class InvitePayload(BaseModel):
    email: str
    name: str
    team_name: str | None = None
    is_team_invite: bool = False

    @model_validator(mode="after")
    def validate_team_fields(self) -> Self:
        if self.is_team_invite and not self.team_name:
            raise ValueError("team_name is required for team invites")

        return self
```

## Route Metadata

- Do not pass `name`, `summary`, or `description` to route decorators; FastAPI uses the handler docstring.

```python
@router.post("/verify")
async def verify_resource(payload: VerifyPayload) -> ApiEnvelope[VerifyResponse]:
    """Verify a resource and return status."""
```

- **A handler's docstring states the operation, not the router it hangs from.** The prefix, the tag
  and the guard already say who may call and what surface this is, so repeating any of it inside every
  docstring adds a clause that is true of the whole file. Under a router only admins reach, write
  "Change the identity fields of a user", never "Change the identity fields an admin may correct on a
  user".
- Naming the caller also makes the sentence wrong the day the guard changes, because a docstring is
  not what any test or type checker reads.

## Privileged Surfaces

- **A privileged router inside an app the public reaches is declared `include_in_schema=False`.** That
  app's document describes the API its consumers are meant to call, and a surface gated on an elevated
  role is not that: listing it beside the public routes hands every reader the route, its payload shape
  and its parameters, which is a map of what to try rather than something they can use.
- This is one part of a defence rather than the whole of it. The guard on the route is what refuses
  the caller; leaving the route out of the document only declines to advertise it. Never let the
  omission stand in for the check.
- Judge it by who reaches the app, not by the path or the role. A privileged router mounted beside
  public ones is hidden wherever it lives; a public route under an `/admin` prefix is not.
- Keep the router's tag as it would be if published, so the grouping is already right the day the
  surface is exposed.

```python
admin_users_router = APIRouter(prefix="/admin/users", tags=["admin"], include_in_schema=False)
```

### A Private Service Publishes Its Own Document

- **An app the public never reaches publishes every route it serves.** Its document has one audience —
  the client built against it — so the reasoning above inverts: there is nobody to hide the routes
  from, and hiding them costs that client the generated types, the request shapes and the browsable
  reference it would otherwise read straight off the service.
- The test is whether an unauthenticated stranger can reach the process at all, not whether the routes
  are privileged once inside. A service reachable only from a private network or an internal origin
  qualifies however elevated the role its routes demand.
- `include_in_schema=False` in such an app hides the routes from the only people entitled to see them
  while protecting nothing, so leave the flag off entirely rather than setting it `True`.

## Response Types

- Use the repository's standard response envelope or response models consistently across handlers.
- Prefer one clear pattern for success, pagination, and error responses rather than mixing many response shapes in the same API surface.
- **A response carries data, never display text.** A label, a title, a step name, a description:
  each belongs to whichever client renders it, and a response that ships one hands every client a
  second copy of its own copy — one that drifts the moment either side is reworded, and that most
  clients never read because they already have their own. Send the identifier the client keys its
  own text off; let the client say it.
- That holds for a server-composed error too. An error names what went wrong in words the reader
  can act on, and never assembles itself from the names of steps, pages, fields, or states the
  client also owns: where the sentence would need one of those to read well, it is written
  generically instead. A value that exists in the response only so an error can be phrased from it
  is the display-text case above wearing a different name, and it goes.

### Success without a payload

- When an endpoint succeeds but has **no response body beyond `{ success: true }`**, use the project's standard no-payload success envelope with `response_model_exclude_unset=True`.
- Do **not** use a generic envelope specialized as `None` with `data=None`: it emits OpenAPI where `data` is typed as JSON `null` only, which breaks generated clients and is not a useful contract.
- Do **not** invent empty Pydantic models just to satisfy a generic response wrapper when there is no payload; use the project's standard no-payload success response instead.

## Response Construction

- Do not inline awaited service calls inside response construction.
- Fetch the data first, then return the response object.

```python
from application.services.resources import get_resource_status

# Bad
return ApiEnvelope(success=True, data=await get_resource_status(principal, session))

# Good
data = await get_resource_status(principal, session)

return ApiEnvelope(success=True, data=data)
```

## Error Handling

- Raise the project's standard API error response directly with an appropriate `HTTPStatus`. Do not wrap it in a helper (for example, `bad_request("...")` or `not_found("...")`) just to set the status code; the call site already states the failure mode, and the helper only adds indirection.
- This includes log-and-raise wrappers (for example a `raise_internal_api_error(...)` that logs then raises): log and `raise ApiError(...) from exc` inline at the failure site instead.
- Always pass `status_code=HTTPStatus.X` and `detail="..."` at the `raise` site so the status is visible without jumping to a helper.
- For bad or invalid client-provided data, raise the project's standard API error response with `HTTPStatus.BAD_REQUEST`.
- Do not use `HTTPStatus.UNPROCESSABLE_ENTITY` for bad-data validation errors.
- Service functions may raise the project's standard API error when a domain check maps directly to an HTTP error (e.g., returning a 403 for authorization failures). Do not force these cases into route-layer-only error raising.

```python
from http import HTTPStatus

from application.api.errors import ApiError

# Good: raise the standard API error directly at the failure site
raise ApiError(
    status_code=HTTPStatus.BAD_REQUEST,
    detail="Invalid payload",
)


# Bad: wrapping the API error in a status-specific helper
def bad_request(message: str) -> ApiError:
    return ApiError(status_code=HTTPStatus.BAD_REQUEST, detail=message)


raise bad_request("Invalid payload")
```

```python
# Good: log and raise inline at the failure site
try:
    response = await client.get_resource(...)
except third_party_client.ApiException as exc:
    logger.error("Resource fetch failed: %s", exc)

    raise ApiError(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        detail="Failed to fetch resource",
    ) from exc

# Bad: routing the log + raise through a shared wrapper
except third_party_client.ApiException as exc:
    raise_internal_error_response(error="Failed to fetch resource", log_message="...", exc=exc)
```

## Gateway Statuses

- **Never answer a request with 502, 503, or 504.** A reverse proxy generates those three for
  itself, so a platform edge replaces the body with its own error page and the message the code
  wrote never reaches the caller. Return `HTTPStatus.INTERNAL_SERVER_ERROR`, log the upstream's own
  status at the failure site, and leave all three out of any status-code map rather than listing
  them.

## Pagination

- Never have unbounded query endpoints; always paginate if an endpoint can return more than 100 entries.
- Always add `offset` and `limit` query parameters to list/export endpoints.
- `limit=10000` or any hardcoded large limit is a code smell — paginate instead.
- **Never offer a fetch-all helper from producer-side code** — not from a client, a gateway, or any other shared surface a caller reaches for. Draining every page presents an unbounded cost as one call, and the name reads the same whether the collection holds three rows or three million. Wrapping the cost does not remove it; it only stops it being visible where it is paid.
- A consumer that genuinely needs every page writes that loop at its own call site, against the paginated read, and stops as soon as its own purpose is met. Two consumers writing the same short loop is the correct outcome, not duplication to factor out.
- Establish that the whole collection is required before writing that loop. Needing the primary, the latest, or a count is not needing every page, and an operation that exists only to act on every record is usually the thing to delete.
- **The one exception is a domain service owning a single complete-read of its own collection**, and it holds only when every consumer genuinely needs every page and the literal alternative is that same loop copied into each of them. One such reader per collection, paging against the bounded read, named for what it returns — never a second one, and never on the client or gateway.
- Respect the project's central pagination limit — passing a larger limit should raise `ValueError`.
