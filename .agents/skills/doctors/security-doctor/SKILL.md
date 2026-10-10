---
name: security-doctor
description: Find and fix the exploitable vulnerabilities in a codebase — injection, broken access control, unsafe file and resource handling, weak cryptography and leaked secrets, business-logic and feature abuse, chained trust gaps, and code built without the guard its siblings carry — each proven with a concrete attack and closed with the smallest fix and a regression test. Use to audit and repair a codebase's security, or to fix the findings of a security audit.
short_description: 'Find and fix the exploitable vulnerabilities in a codebase, each proven by a concrete attack.'
disable-model-invocation: true
---

# Security Doctor

Every finding names an attacker, what they send and what they get, and every fix is the smallest
one that makes that attack fail and a test that proves it does.

## Dependencies

- `doctor-protocol` — own the run.
- `security-audit` — its rubric is the bar for every finding, its precedents and its smallest-fix
  order; its reconnaissance, hunting, validation and independent verification are how a finding is
  found and proven; its attack-class catalogue holds each lens's checks.
- `pre-production` — a fix that changes behavior is stated, and no fix keeps a vulnerable path
  alive for compatibility.
- `test-fixture` — the regression test each fix carries.

## Inventory

`security-audit`'s Phase 1 reconnaissance, taken once before fan-out: what the application is and
its comparable baseline; per deployable, its trust boundaries, authentication and authorization
mechanism, and every input surface — routes, handlers, jobs, webhooks, message consumers, CLI
entry points, file and archive readers, outbound requests, and configuration that reaches
behavior. Reviewers partition by that map: by subsystem and attack class, the riskiest first.

Findings a supplied `security-audit` report names enter as candidates by their ids. Reviewers hunt
as a `security-audit` codebase audit does, at `high`, or at `medium` when the invocation states
`medium` or `low`, and every candidate passes that skill's validation and independent verification
against the current tree before it enters the ledger. A candidate a precedent rejects is kept
outside the findings with its location and the precedent that rejected it, and counted in the
report.

## Lenses

Each lens runs the checks its section of `security-audit`'s attack-class catalogue lists;
**Missing Construction** runs the rubric's **Building It Safely** checks *Use the guard that already
exists*, *Assert what a provider already tells you* and *Add no surface the request does not need*,
as its section bounds them. Evidence is the rubric's **What A Surviving Finding Has Been Put
Through**, traced as file and line, and the remedy is its smallest-fix order.

### Injection

Untrusted input reaching a query, command, template or parser without the binding or allow-list
that keeps it data, directly or second-order through storage.

### Access Control

A caller performing an action or reading a record the system gates from them: a weaker permission
on another path to the same state change, a body field overriding a restriction, a bulk operation
checking the batch and not each item, an endpoint that authenticates and never authorizes, a record
read or written without the owner scoping **Building It Safely**'s *Authorize the object, not only
the route* requires. A route, handler or job missing the guard its siblings carry is **Missing
Construction**'s.

### Resource And File Handling

Path traversal, archive extraction outside its root, server-side request forgery with control of
the host or protocol, unsafe deserialization, and check-then-use races on files.

### Cryptography And Secrets

Predictable values where secrecy matters, a secret in source, logs, errors, URLs or client
bundles, a signature or MAC checked wrongly — the wrong key, a non-constant-time comparison, a
failure accepted — misused primitives, and an error path that falls back to no protection. A
check that never runs at all is **Missing Construction**'s.

### Business Logic And Feature Abuse

A workflow's steps skipped, replayed or raced into an invalid state; quantities and boundaries
abused; a legitimate feature — export, import, search, preview, webhook, notification — used to
reach data or actions above the caller's access; an enumeration oracle.

### Chained Trust

Individually safe behaviors that combine into an attack: a component trusting another's
validation that differs from its own, a token or scope wider than its name, a gap between
revocation and enforcement, a rollback restoring more than it should.

### Missing Construction

Code built without what **Building It Safely** requires: a route, handler or job missing the
guard its siblings carry, a provider's guarantee — a webhook or token signature, a verified flag,
an expiry — the code never checks although the provider supplies it, and a surface — permissive
fallback, optional bypass, unused mode — the product does not need.

### Exposed Defaults

The literal checks in the catalogue's **Obvious things**: committed secret files and working seed
credentials, debug or dev mode reachable in production, unprotected administrative and
diagnostic endpoints, permissive cross-origin settings with credentials, session cookies without
protective attributes, unvalidated redirects, and errors returning internals.

## Dispositions

1. **Change boundary.** The fix for each confirmed finding: the code, tests, configuration,
   contracts and data migration it needs, and the guard that holds it. Refactoring and dependency
   upgrades are outside it.
2. **A remedy that is a product decision** — requiring an invitation, dropping a feature,
   narrowing who may act — is the user's; the finding stays open until they choose.
3. **Each fix carries a regression test** that performs the attack and fails without the fix and
   passes with it, built under `test-fixture`.
4. **A hardening note is reported, never changed** in this run.
5. **A recurring shape's guard** is a lint rule against the unsafe call, or a structural test that
   fails on a route or handler registered without its guard.
6. **The cross-cutting reviewer compares** every access path to the same resource across
   partitions, the validation one component assumes another performed, and data stored safely
   by one path and used unsafely by another.
7. **The final reviewer challenges** each hardening note, each candidate a precedent rejected, and
   each retained surface, for an attack the run dismissed too early.

## Report Additions

Ahead of the protocol's skeleton, a summary line: the scope and effort, findings fixed, findings
waiting on the user, hardening notes, and the pull request. Then:

- a findings table — id, severity, the attack in one line, the fix shipped, and the simpler option
  offered or `none`; a finding waiting on the user shows its options and the recommended one in the
  fix cell;
- hardening notes by id, each with why it is not exploitable;
- candidates rejected by a precedent, counted by precedent;
- guards added, each with the shape it holds;
- what the codebase does well;
- coverage: partitions or classes not reached, the statement that no run shows the code is clean,
  and the next run recommended;
- **Next:** the one decision or review the user owes.
