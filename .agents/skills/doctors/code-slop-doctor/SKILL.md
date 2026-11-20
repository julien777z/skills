---
name: code-slop-doctor
description: Strip the complexity a codebase does not need and the code a reviewer reads as generated slop — pass-through layers and wrapper components, one-case abstractions, use cases split across many calls, duplicates, divergent siblings, legacy paths, hand-written styling in apps, tangled or padded code, and surplus migrations, build files, configuration names and dependencies. Use to deslop a repository or one of its phases, lenses or paths. Run only when the user asks for it.
short_description: 'Remove unneeded layers, wrappers, abstractions, duplicates, legacy paths, hand-written styling, code that reads as slop, configuration names and dependencies.'
---

# Code Slop Doctor

Every layer, abstraction, copy and branch a reader has to get through must earn its place by
something it does, and every line should read as a careful author wrote it; this doctor finds what
does nothing or makes a reader wince, and takes it out.

## Dependencies
- `doctor-protocol`
- `pre-production`
- `code-simplify`
- `test-fixture`
- `defer-scope`
- `acceptance-gate`
- `get-doctors`

## Phases

Also read, when the skill listing declares them and found by their descriptions, the repository's
database-migration skill, its test-runner skill, its checklist for adding a configuration value and
its deployment skill, and follow its packaging rules for each language it builds. Their rules govern
every correction in their areas and are cited here, never restated; the deployment skill's
read-only guidance is how a deployment's environment is read, and reading activates nothing else it
offers.

The run works in five phases, in this order, and each phase is one batch:

1. **Application code** — services, apps, workers, shared packages and libraries other than UI
   ones.
2. **Frontend** — every shared UI package the audited apps consume, first, then web and mobile apps,
   their components, hooks, stores, styles and API types. A scope naming an app includes the shared
   UI packages it consumes, because that is where its styling and wrapper fixes land.
3. **Migrations** — every migration chain, its registries, backfills and tooling.
4. **Build, configuration and dependencies** — container files, workflows, scripts, tool and root
   configuration, every place a configuration name is declared or read, manifests and lockfiles.
5. **Tests** — after the code they test has settled. A test an earlier phase's change breaks — one
   importing a moved path, one exercising only a removed layer — is repaired or deleted in that
   phase's batch under **Test Slop**'s remedy, so every batch passes; this phase audits the rest.

A phase the repository has nothing for is skipped and reported. A scope argument selects phases,
lenses, or paths; a run scoped to one lens or phase applies only that lens or phase.

## Inventory

Run `doctor-protocol`.

Exclude generated code by the repository's own markers. Enumerate, per phase in scope, every item a
lens's checks name, and build these tables before judging anything:

- the deployables, grouped by kind — RPC server, HTTP app, worker, CLI, frontend app — with a
  **slot table** per kind: one row per structural slot (entrypoint, server or app construction,
  startup and shutdown lifecycle, health and readiness, configuration, middleware or interceptors,
  logging, dependency wiring, data fetching for a frontend) and one column per deployable naming
  the file and symbol that fills it, or `none`;
- every module with its public symbol count and the concern it serves, and every catch-all module
  (`utils`, `helpers`, `common`, `misc`);
- every comment, constant or message carrying a compatibility word — legacy, compat, fallback,
  deprecated, kept for, formerly, transitional, temporary, old format — as a search key pointing at
  code, never removing an existing to-do note unprompted;
- per migration chain: its revisions, registries and registered backfills with the callable behind
  each hook, revisions sharing a name across chains, and which environments have applied which
  revisions, read from the real version table where reachable and treated as applied where not;
- a **configuration matrix**: every configuration name by every place it is declared or read — typed
  settings models with each field's type, default and required-ness, environment example files, test
  environment blocks, container, CI and deployment manifests, workspace and cloud-agent environment
  files, documentation, and every reader — application code, a library that reads the variable
  itself, a compose service, a workflow step, a front end — names only, never values. A deployment
  whose environment lives on a hosting platform is one column, read by name through the deployment
  skill; one that cannot be read is recorded unread, never empty. For every field whose default is
  absence, record whether its reader refuses it, branches on it, or passes it through;
- a **use-case table**: one row per use case — a page loading, a user action, a job run, a
  request handler or RPC operation serving its caller — naming its entry point and every call it
  makes to an operation the repository owns, whether an HTTP endpoint, an RPC operation or another
  internal service, at every hop behind it, with which calls wait on another's result and how long
  the use case waits; a frontend use case is read from the network log of the loaded page, an
  internal one from traces or service logs;
- per language and project: every manifest and its sections, every lockfile, tools a workflow
  installs outside a manifest, first-party imports across source, tests, scripts and workflow
  helpers, and every tool invocation in CI, scripts and hooks.

The measurements taken once before fan-out: the repository's configured lint and type checks over
the scope with no changed-lines filter; its cross-file duplication detector over each phase's trees
at the tool's default similarity; the chain replay and drift check its migration tooling defines;
each use case's calls and timing on the running local stack; each app's hand-written styling count,
as **Hand-Written Styling** defines it; and each deployment's configuration column, read by name
once.

## Lenses

Each lens states its defect shape, the checks that find every instance, the remedy, and what is left
alone so a reviewer does not go hunting. Every lens applies in every phase, read in that phase's
language; **Hand-Written Styling** belongs to the frontend phase, **Migration Chain** to the
migrations phase, **Build And Root**, **Configuration Drift** and **Dependency Drift** to the build
phase, and **Test Slop** to the test phase.

Read [the lens criteria](references/lenses.md) before building the inventory, and give them to every
reviewer with its phase: each lens named here and in this skill's other sections is a section of
that reference.

| Lens | Defect shape |
| --- | --- |
| **Pass-Through Layer** | A layer, wrapper or alias that only hands the call on. |
| **Speculative Abstraction** | Structure built for cases that never arrived. |
| **Duplicate Implementation** | One question answered twice. |
| **Fragmented Use Case** | One use case paying for many calls to operations the repository owns. |
| **Divergent Siblings** | Things of one kind built in different shapes. |
| **Scattered Structure** | Code spread over more files and folders than its responsibilities need. |
| **Repeated Literal** | One meaning spelled out many times. |
| **Hand-Written Styling** | Styling written by hand where a shared component owns it. |
| **Reads As Slop** | Code a reviewer recognizes as generated: correct, and still a shape no careful author writes. |
| **Tolerated Past** | Code that tolerates a past the repository no longer has. |
| **Migration Chain** | A chain, its registries and its tooling, held to one shape and no more machinery than the job. |
| **Build And Root** | Build, CI and root files carrying more than they need. |
| **Configuration Drift** | A configuration name that the matrix shows out of step. |
| **Dependency Drift** | Declared dependencies out of step with what the code imports and the checks invoke. |
| **Test Slop** | Tests that cost reading time and prove nothing, found after the code has settled. |

## Dispositions

- Restructuring is ordinary work here: merges, moves, renames, collapses and regroupings land with
  every importer updated in the same change and nothing left to resolve the old path. No finding is
  too small: one regrouped message or one renamed file is fixed like a merged package.
- **Breaking an owned contract to remove slop is ordinary work, never a question**, made as
  `pre-production`'s **Target Contract** says; a removal is never narrowed, shimmed or dropped to
  keep an owned shape stable.
- Data a removal leaves in the old shape — a flag whose retirement backfill has not run, a chain to
  collapse — follows `pre-production`'s **Product State** and **Target Contract** and the
  repository's database-migration skill, never a question.
- The user decides what `pre-production`'s **Product Choices** reserves
  for them. A contract a consumer outside the user's control speaks stays as it is and is reported,
  under its **Target Contract**.
- Fix the reader or the writer, never both. A tolerance that hides a wiring defect is a confirmed
  defect and is fixed. An unsupported historical record is never a finding and never receives a
  fallback.
- A migration correction follows the migration skill's **Applied Is What Makes History**, stacked
  when applied state cannot be established; a data-loss path with no recovery is a blocker to
  report.
- A configuration default its reader refuses is declared nowhere until the disagreement is settled:
  the reader is wrong when nothing that ships can use the value, the declaration and deployment are
  wrong when something can, and where the target contract does not show which, both fixes go to the
  user. A field nothing deployed sets takes one of three outcomes the plan names: a deployment
  should carry it, it is a local-development tool retained with the tool and the branch named in the
  ledger, or it is deleted with the branch its value selects.
- An even split between two sibling structures equally fit for the kind goes to the one leaving the
  fewest mechanisms and moving the fewest importers, stated in the pull request.
- A cleanup finding another doctor owns — documentation, a contract model, a deep test audit — is
  not fixed here; the report names it with that doctor, found through `get-doctors`. A confirmed
  defect or vulnerability met in another doctor's area is fixed in this run, as `doctor-protocol`'s
  **Resolve The Scope** says.

The cross-cutting reviewer compares each kind's slot table across its deployables, one shape across
packages, apps and languages, and every value defaulted in one package against its producer in
another; compares migration chains and registries with each other; reads each deployment column
against the settings model its process loads, one name declared on two models, and the locations
each checklist, manifest and example file names against the configuration matrix; and compares
manifests for one package pinned differently across projects or languages and a check one project
runs that its sibling does not. The final adversarial reviewer tries to reach each removed layer,
branch, alias and operation from a live caller, confirms each merged operation returns only what
every run of its use cases needs, each batch or merged operation authorizes each item and each
returned field as the operations it replaced did, and each use case waits no longer than before,
confirms no import of a moved or renamed module still points at its old path, replays every chain
the run touched, confirms a stacked migration correction did not narrow the approved downgrade or
survivorship coverage, challenges every revision kept as applied without version-table evidence,
confirms each removed configuration name and package has no surviving reader or importer, re-traces
every retained package to an importer or an invocation, re-derives the matrix for every retained
mismatch, re-reads the deployment columns for every field kept as a local-development tool, confirms
each regenerated lockfile resolves its constraints, re-counts every app's hand-written styling and
confirms it reads zero, and confirms that the repository's tests pass on each batch.

## Report Additions

- per phase and lens: findings and dispositions by package and language;
- each kind's slot table before and after;
- each module merged, moved, renamed, collapsed or split, with its importers moved;
- each layer, abstraction and alias removed, with its callers;
- the use-case table before and after: calls and wait per use case, each operation merged, batched
  or deleted with its callers moved, and each merge put to the user with its recommendation and
  their answer;
- each duplicate and its surviving owner;
- each flag gating a former behavior, its readers and retiring backfill; each suppression removed
  and the rule code proposed as its guard; each check whose verdict gates again;
- per migration chain: heads, revisions checked by lens, corrections, policy coverage before and
  after, and the evidence for applied state;
- each build, CI and root file consolidated or deleted;
- the configuration matrix with every changed cell, and each deployment column read or unread with
  the reason; the readers traced for each removal; for every field no deployment sets, its outcome;
- per manifest: declarations removed, added and re-ranged; each lockfile regenerated with its
  command; audit tools wired in or removed;
- each app's hand-written styling count before and after, and each variant or prop added to a shared
  component in its place;
- each shape **Reads As Slop** rewrote, by check, with the test proving each executable rewrite's
  behavior unchanged and the test that carries each deleted comment's behavioral guarantee;
- each test removed or repaired with the layer it exercised;
- each finding another doctor owns, named with that doctor.
