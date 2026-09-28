---
globs:
- '**/*.py'
- '**/*.ts'
- '**/*.tsx'
alwaysApply: false
paths:
- '**/*.py'
- '**/*.ts'
- '**/*.tsx'
---

# HTTP Rules

## Clients

- Before writing provider HTTP calls, check whether its official SDK covers the required endpoints and protocol features. Use the SDK for operations it covers and the repository's shared HTTP helper or established client for those it does not.
- Prefer the repository's shared HTTP helper or client abstraction over spawning ad-hoc clients deep in application code.
- If the project already centralizes retries, auth headers, or response parsing, reuse that shared layer instead of reimplementing it per call site.
- Keep raw `response.json()` parsing at the boundary layer; do not scatter transport parsing logic across core business logic.
- For requests to internal services, prefer a generated or shared typed client when one exists.
- If no shared client exists for a service boundary that is used repeatedly, create or generate one instead of hand-rolling the same HTTP integration in multiple places.

## Response Statuses

- **A service answers with the common statuses only.** Every success is 200, a create and a delete
  included, never 201, 202 or 204. A failure is one of 400 (invalid client-provided data included,
  never 422), 401, 403, 404, 409, 429 or 500. A rarer status — 408, 412, 413, 422, 501 and the rest
  — is a distinction no caller branches on, and the message carries what it would have said.
- **Never answer with 502, 503, or 504.** A reverse proxy generates those three for itself, so a
  platform edge replaces the body with its own error page and the message the code wrote never
  reaches the caller. Answer 500 and log the upstream's own status at the failure site.
- A table mapping another protocol's codes onto HTTP, such as gRPC status codes, maps onto that set
  and lets every code it does not list fall to 500. A generated API schema documents the statuses
  the service sends, not a framework's defaults it overrides.
- A redirect keeps its `3xx`, and a status a protocol the service implements prescribes — an OAuth
  dynamic client registration's 201, say — follows that protocol.
- A caller of a service this repository does not own accepts that service's whole `2xx` range.
