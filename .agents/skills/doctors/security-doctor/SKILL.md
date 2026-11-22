---
name: security-doctor
description: Find and fix the exploitable vulnerabilities in a codebase — injection, broken access control, unsafe file and resource handling, weak cryptography and leaked secrets, business-logic and feature abuse, chained trust gaps, and code built without the guard its siblings carry — each proven with a concrete attack and closed with the smallest fix and a regression test. Use to audit, pen-test or repair a codebase's security, or to fix the findings of a security review. Run only when the user asks for it.
short_description: 'Find and fix the exploitable vulnerabilities in a codebase, each proven by a concrete attack.'
---

# Security Doctor

Every finding names an attacker, what they send and what they get, and every fix is the smallest
one that makes that attack fail and a test that proves it does.

## Dependencies
- `doctor-protocol`
- `security-audit`
- `subagent-matrix`
- `pre-production`
- `test-fixture`
- `get-doctors`

## Inventory

Run `doctor-protocol` with specialist capability for its audit, cross-cutting, and final
reviewers, setting their Claude fallback tier to `advanced`. Its implementation workers retain the protocol default.

Reconnaissance, taken once before fan-out as the doctor's
[reconnaissance](references/reconnaissance.md) reference maps it: what the application is and
its comparable baseline; per deployable, its trust boundaries, authentication and authorization
mechanism, and every input surface — routes, handlers, jobs, webhooks, message consumers, CLI
entry points, file and archive readers, outbound requests, and configuration that reaches
behavior. Generated and vendored code is excluded, since neither is fixed where it sits.

**Shared index.** From the index `doctor-protocol`'s **Share The Index** keeps, this doctor reads
the file inventory, symbol and import tables and dependency list. It writes the deployables with
their entry points and input surfaces, and the configuration names that reach behavior.

Findings a supplied security review names, such as a `security-audit` result, enter as candidates
by their ids. Every candidate, including one from the cross-cutting reviewer, passes **Validation**
against the current tree before it enters the ledger. A candidate a precedent rejects is kept
outside the findings with its location and the precedent that rejected it, and counted in the
report.

### Pre-Pass

These are the mechanical commands `doctor-protocol` runs once before fan-out, and every reviewer
reads their output: a hit is a candidate to trace, never a finding, and each still passes
**Validation**. A tool the repository does not configure is handled as
`doctor-protocol`'s **Measure Before Fan-Out** says. The commands below name the usual scanner for
each job.

- **Secrets** — a secret scan over the tree and its history.
- **Obvious things** — the literal searches the catalog's **Obvious things** class lists: secret
  words and key headers, security to-do comments, committed secret files, dynamic evaluation,
  permissive cross-origin settings, cookie attributes, and redirect parameters.
- **Package advisories** — the package manager's audit of every lockfile.
- **Unguarded surfaces** — every route, handler, job and consumer from the reconnaissance map with
  the guard it declares, listing those that declare none their siblings carry, and every privileged
  router the public application's schema lists.
- **Controls with optional settings** — every key, secret, allow-list or limit a control reads
  whose settings field is optional, and every branch on the environment's name in application code.

```sh
gitleaks detect --redact
rg -n -i 'password|secret|apikey|api_key|token|Bearer |-----BEGIN'
rg -n -i '(TODO|FIXME|HACK|XXX).*(auth|permission|validat|secur)'
rg -n 'eval\(|exec\(|child_process|new Function\(|vm\.runInContext|pickle\.loads|yaml\.load\('
rg -n -i 'Access-Control-Allow-Origin|allow_origins|allow_credentials|httponly|samesite'
rg -n -i '(redirect|return|next|url|goto|continue)(_to|_url)?\s*='
pip-audit
npm audit --omit=dev
```

The pre-pass output saved in the run records keeps each hit's file, line and kind, with any matched
value redacted to its first four characters and its length. A value is read in place, where the
source holds it, to validate it, and never written into the run records.

### Measures

The counts `doctor-protocol` takes before the audit and again after the fixes: secret-scan hits, in
the tree and in history; hits per literal search; advisories per lockfile; surfaces with no guard;
controls whose setting is optional; and confirmed findings by severity, which read zero open when
the run is finished.

## Lenses

Each lens runs the checks its section of `security-audit`'s attack-class catalog lists, check by
check. Evidence is the rubric's **What A Surviving Finding Has Been Put Through**, traced as file
and line, the remedy is its smallest-fix order, and what a lens leaves alone is what the rubric's
**Precedents** reject.

Every finding is recorded in `doctor-protocol`'s finding shape: its evidence is the attack, who
sends what and what they get, with the rubric's severity rating; its fix is the smallest one that makes
the attack fail; and its proving check is the regression test that performs the attack. A finding
of **Unsafe Construction A Rule Names** carries the rule it cites and the source lines instead of
an attack, and its proving check fails while the construction stands.

### Injection

Untrusted input reaching a query, command, template or parser without the binding or allow-list
that keeps it data, directly or second-order through storage. Reach: partition; a second-order
path that crosses subsystems is the cross-cutting reviewer's.

### Access Control

A caller performing an action or reading a record the system gates from them: a weaker permission
on another path to the same state change, a body field overriding a restriction, a bulk operation
checking the batch and not each item, an endpoint that authenticates and never authorizes, a record
read or written without the owner scoping **Building It Safely**'s *Enforce caller policy at the
trust boundary* requires. A route, handler or job missing the guard its siblings carry is **Missing
Construction**'s. Reach: partition; every path to one resource is compared across the
repository.

### Resource And File Handling

Path traversal, archive extraction outside its root, server-side request forgery with control of
the host or protocol, unsafe deserialization, and check-then-use races on files. Reach: partition.

### Cryptography And Secrets

Predictable values where secrecy matters, a secret in source, logs, errors, URLs or client
bundles, a signature or MAC checked wrongly — the wrong key, a non-constant-time comparison, a
failure accepted — misused primitives, and an error path that falls back to no protection. A
check that never runs at all is **Missing Construction**'s. The pre-pass's secret scan and literal
searches supply the candidates. Reach: partition.

### Business Logic And Feature Abuse

A workflow's steps skipped, replayed or raced into an invalid state; quantities and boundaries
abused; a legitimate feature — export, import, search, preview, webhook, notification — used to
reach data or actions above the caller's access; an enumeration oracle. Reach: partition.

### Chained Trust

Individually safe behaviors that combine into an attack: a component trusting another's
validation that differs from its own, a token or scope wider than its name, a gap between
revocation and enforcement, a rollback restoring more than it should. Reach: whole repository.

### Missing Construction

Code built without what the rubric's **Building It Safely** requires. It runs four of that
section's checks, as the section bounds them, and the other three belong to **Access Control**,
**Injection** and **Cryptography And Secrets**:

- *Use the guard that already exists* — the pre-pass's unguarded surfaces: a route, handler or job
  missing the guard its siblings carry;
- *Assert what a provider already tells you* — a provider's guarantee, a webhook or token
  signature, a verified flag, an expiry, the code never checks although the provider supplies it;
- *Add no surface the request does not need* — a permissive fallback, optional bypass or unused
  mode the product does not need;
- *A control's own setting is required* — the pre-pass's controls with optional settings: a
  control that skips or weakens itself when its key, secret, allow-list or limit is unset.

Reach: whole repository, since a missing guard shows only beside the siblings that carry it.

### Exposed Defaults

The literal checks in the catalog's **Obvious things**: committed secret files and working seed
credentials, debug or dev mode reachable in production, unprotected administrative and
diagnostic endpoints, permissive cross-origin settings with credentials, session cookies without
protective attributes, unvalidated redirects, and errors returning internals. The pre-pass's
literal searches supply every candidate, and each is traced to its impact before it is a finding.
Reach: whole repository.

### Wildcard

The catalog's **Wildcard** class: what no named class looks for — the strangest code, half-finished
features, calls the API allows and no client makes, features mixed that were not designed
together, and what the history reverted. No reviewer is added for it: the cross-cutting reviewer
runs it, reading across the classes. Reach: whole repository.

### Unsafe Construction A Rule Names

Construction a rule file names as a defect, whether or not an attack reaches it today: a privileged
router listed in the schema of an application the public reaches, against the FastAPI rules'
**Privileged Surfaces**; a development or test secret value in application or library code; and a
branch on the environment that relaxes or varies security posture, both against the general Python
rule. The pre-pass's unguarded-surface and environment-branch lists supply the candidates.
Remedy: the shape the rule states. Left alone: construction no rule names and no attack reaches,
which stays a hardening note. Reach: partition.

## Reviewers

The audit reviewers are `doctor-protocol`'s, at its counts, and hunt: the reconnaissance map
dictates their cut, by subsystem and attack class, the riskiest first, as `security-audit`'s hunting
reference splits a surface. Each reviewer's brief carries what that reference says every hunter
prompt includes — the architecture summary verbatim, its attack classes and scope, its starting
paths, the hunting methodology and the validation rules — beside the protocol's partition inputs.
A reviewer may start at most two research agents over its hunt, as that reference allows, each
launched like the reviewer through `subagent-matrix` at specialist capability with `advanced` as
its fallback.

The cross-cutting reviewer owns the whole-repository lenses, working from the reconnaissance map,
the pre-pass output and every candidate. It compares every access path to the same
resource across partitions, the validation one component assumes another performed, and data
stored safely by one path and used unsafely by another, and runs **Wildcard**.

The final reviewer challenges each hardening note, each candidate a precedent rejected, each
advisory left for the dependency owner and each retained surface, for an attack the run dismissed
too early.

## Validation

A hunter is biased toward keeping what it found, so every candidate faces agents that try to kill
it before it enters the ledger, using the prompts in `security-audit`'s validation reference:

1. **Refute.** The parent merges candidates that share a root cause, then gives each remaining
   candidate one fresh read-only refuter, all in parallel.
2. **Verify independently.** Each confirmed finding gets one fresh read-only verifier, who did not
   write it, checking every factual claim against the source; its corrections are applied and
   named in the report, and a rejected finding is dropped or reported as investigated.

Exploit validation, with its attacker and attack test, applies to vulnerabilities only. A candidate
of **Unsafe Construction A Rule Names** is refuted and verified against the rule it cites and its
source evidence: whether that rule names the construction and the source holds it.

Each step starts at most ten agents a round, launched through `subagent-matrix` like the reviewers; past ten
candidates or findings, each agent takes those of one subsystem. On the small route both steps run
in process, against the same prompts.

## Hunting Rounds

One round finds roughly half of what several surface, because each reviewer digs where its own
reading leads, so the hunt repeats until a round adds nothing. A round is the audit reviewers'
hunt followed by **Validation**. Reconnaissance runs once, before the first.

- **Rounds repeat until a completed round yields no new candidate that survives Validation**, with
  no cap on the number of rounds: stopping earlier leaves findings a further round would have
  surfaced. A rejected candidate or a duplicate does not extend the loop, and an incomplete round —
  a partition unread, a reviewer that did not return — is incomplete, never a clean round.
- **Each later round hunts only what earlier rounds did not cover**: the partitions and attack
  classes where the last round confirmed a finding, which mark ground the hunt has not exhausted,
  and any partition or class no round has reached. Its reviewers are fresh and get every prior
  finding and rejected candidate, so they look past what is already known.
- **Launches per round.** On the whole route a round starts the audit reviewers it re-hunts, at
  most `doctor-protocol`'s cap and one per partition it covers, each with up to two research
  agents; one cross-cutting reviewer when the round's candidates span partitions; and up to ten
  refuters and ten verifiers. Reconnaissance adds up to three agents once, and three more when an
  area needs mapping again. On the small route every round runs in process and adds none. The
  number of rounds grows with what the hunt keeps finding.

## Dispositions

1. **Change boundary.** The fix for each confirmed finding: the code, tests, configuration,
   contracts and data migration it needs, and the guard that holds it. Refactoring is outside it,
   and so is a dependency upgrade apart from the one that closes a confirmed finding. A confirmed
   defect the run notices that is no vulnerability is fixed in this run too, as `doctor-protocol`'s
   **Resolve The Scope** says.
2. **Every confirmed finding is closed in this run** with the smallest fix that enforces the access
   the product already intends, as `pre-production`'s security bullet says. A change that
   widens access or changes who may see a record is a reserved decision, asked as
   `doctor-protocol`'s **Gate And Show The Plan** says.
3. **Each fix carries a regression test** that performs the attack and fails without the fix and
   passes with it, built under `test-fixture`.
4. **A hardening note is reported, never changed** in this run, apart from one a rule file names
   as a defect, which **Unsafe Construction A Rule Names** fixes.
5. **A package advisory is a candidate, never a finding on its own**, as the rubric's
   **Precedents** say of vulnerable dependencies. One whose vulnerable code an attacker reaches
   through this application is traced and fixed by upgrading that package. Every other advisory is
   listed in the report with its package, version and fixing release for the doctor `get-doctors`
   lists for dependency drift, which owns the upgrade.
6. **A recurring shape's guard** is a lint rule against the unsafe call, or a structural test that
   fails on a route or handler registered without its guard.

## Report Additions

Ahead of the protocol's skeleton, a summary line: the scope and audit coverage, the baseline
comparable the severities were calibrated against, findings fixed, reserved decisions asked, with each
answer or still open, hardening notes, and the pull request. Keep the report short: one longer than the
codebase deserves is padding. Then:

- a findings table — id, severity, the attack in one line, the fix shipped, and the reserved decision
  asked, with its answer or still open, or `none`;
- hardening notes by id, each with why it is not exploitable;
- candidates rejected by a precedent, counted by precedent;
- package advisories: each one traced and upgraded, and each one listed for the dependency owner;
- each construction a rule names that the run corrected;
- guards added, each with the shape it holds;
- what the codebase does well;
- coverage: partitions or classes not reached, the statement that no run shows the code is clean,
  since each run explores different paths and the best single run finds roughly half of what
  several surface, and the next run recommended.
