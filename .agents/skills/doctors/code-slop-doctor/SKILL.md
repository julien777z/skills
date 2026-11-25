---
name: code-slop-doctor
description: Strip the complexity a codebase does not need and the code a reviewer reads as generated slop — pass-through layers and wrapper components, one-case abstractions, use cases split across many calls or left unbounded, duplicates, divergent siblings, legacy paths, dead code, suppressions, censored logs and deprecated usage, hand-written styling in apps, tangled or padded code, names that do not say their subject, prompts held in code, tests that cost reading time and prove nothing, and surplus or outdated migrations, build and workflow files, configuration names and dependencies. Use to deslop a whole repository or one of its areas, lenses or paths. Run only when the user asks for it.
short_description: 'Remove unneeded layers, wrappers, abstractions, duplicates, legacy paths, dead and suppressed code, hand-written styling, code that reads as slop, and stale configuration, workflows and dependencies.'
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
- `banned-terminology`
- `defer-scope`
- `get-doctors`
- `council`

## Areas

Also read, when the skill listing declares them and found by their descriptions, the repository's
database-migration skill, its test-runner skill, its checklist for adding a configuration value and
its deployment skill, and follow its packaging rules for each language it builds. Their rules govern
every correction in their areas and are cited here, never restated; the deployment skill's
read-only guidance is how a deployment's environment is read, and reading activates nothing else it
offers.

The run is one audit, one plan and one set of waves, as `doctor-protocol` runs them. The five areas
below are how the inventory is partitioned and the order the plan gives its groups; none is an
audit, a plan or an approval of its own:

1. **Application code** — services, apps, workers, shared packages and libraries other than UI
   ones.
2. **Frontend** — every shared UI package the audited apps consume, first, then web and mobile apps,
   their components, hooks, stores, styles and API types. A scope naming an app includes the shared
   UI packages it consumes, because that is where its styling and wrapper fixes land.
3. **Migrations** — every migration chain, its registries, backfills and tooling.
4. **Build, configuration and dependencies** — container files, workflows, scripts, tool and root
   configuration, every place a configuration name is declared or read, manifests and lockfiles.
5. **Tests** — audited in the same audit as the code, under **Test Slop**, with their fixes ordered
   after the fixes to the code they test. A test another group's change breaks — one importing a
   moved path, one exercising only a removed layer — is repaired or deleted in that group under
   **Test Slop**'s remedy, so every wave passes.

An area the repository has nothing for is skipped and reported. A scope argument selects areas,
lenses, or paths; a run scoped to one lens or area applies only that lens or area.

## Inventory

Run `doctor-protocol`.

Exclude generated code by the repository's own markers, and vendored code, since neither is fixed where it sits. Enumerate, per area in scope, every item a
lens's checks name. The pre-pass builds these tables before anything is judged, and a reviewer reads
a table rather than rebuilding it:

- the deployables, grouped by kind — RPC server, HTTP app, worker, CLI, frontend app — with a
  **slot table** per kind: one row per structural slot (entrypoint, server or app construction,
  startup and shutdown lifecycle, health and readiness, configuration, middleware or interceptors,
  logging, dependency wiring, data fetching for a frontend) and one column per deployable naming
  the file and symbol that fills it, or `none`;
- a **module table**: every module with its line count, its public symbol count and the concern it
  serves, and every catch-all module (`utils`, `helpers`, `common`, `misc`);
- a **symbol index** over the whole repository, whatever the scope: every exported symbol with its
  name, kind, signature, first docstring line and module, and its reference counts split into
  application, test and script;
- every comment, constant or message naming compatibility or a deployment transition — legacy,
  compat, fallback, deprecated, kept for, formerly, transitional, temporary, cutover, rollout,
  mixed version, old format — as a search key pointing at code;
- per migration chain: its revisions, registries and registered backfills with the callable behind
  each hook, revisions sharing a name across chains, and which environments have applied which
  revisions, read from the real version table where reachable and treated as applied where not;
- a **configuration matrix**: every configuration name by every place it is declared or read — typed
  settings models with each field's type, default and required-ness, environment example files, test
  environment blocks, container, CI and deployment manifests, workspace and cloud-agent environment
  files, documentation, and every reader — application code, a library that reads the variable
  itself, a compose service, a workflow step, a front end — names only, never values. A deployment
  whose environment lives on a hosting platform is one column, read by name through the deployment
  skill; one that cannot be read is recorded unread, never empty. For every field with a default,
  record whether a production deployment running on that default gets the value's full behavior,
  and for every field whose default is absence, whether its reader refuses it, branches on it, or
  passes it through;
- a **use-case table**, built from the code first: one row per use case — a page loading, a user
  action, a job run, a request handler or RPC operation serving its caller — naming its entry point
  and every call it makes to an operation the repository owns, whether an HTTP endpoint, an RPC
  operation or another internal service, at every hop behind it. A row is a candidate when it makes
  several owned calls, makes a call inside a loop, a list render or a fan-out, awaits calls in turn
  where no later call reads an earlier result, or reads a collection with no bound. Only candidate
  rows are run: each is loaded on the running local stack and its calls, their order and its wait
  recorded, a frontend use case from the network log of the loaded page and an internal one from
  traces or service logs. A row the code clears is never loaded;
- per language and project: every manifest and its sections, every lockfile, every runtime version
  file and container base image, tools a workflow installs outside a manifest, first-party imports
  across source, tests, scripts and workflow helpers, and every tool invocation in CI, scripts and
  hooks.

**Shared index.** From the index `doctor-protocol`'s **Share The Index** keeps, this doctor reads
the file inventory, symbol and import tables and dependency list. It writes the module table, the
symbol index, the import graph, the slot tables, the configuration matrix and the dependency list
with each manifest's declarations.

### Pre-Pass

These are the mechanical commands `doctor-protocol` runs once before any reviewer reads, each
listing candidates for the lens named beside it. A tool the repository does not configure is handled
as `doctor-protocol`'s **Measure Before Fan-Out** says. The commands below name the usual tool per
language.

- **Lint and type findings** — the repository's configured lint and type checks over the scope with
  no changed-lines filter.
- **Tangled flow, ceremony and long functions** (**Reads As Slop**) — the repository's linter with
  its complexity and simplification rules switched on for this one run: for Python the first or
  second command below, for TypeScript Biome's complexity group.
- **Copied blocks** (**Duplicate Implementation**) — the repository's cross-file duplication
  detector over each area's trees other than tests, at the tool's default similarity.
- **Dead code** (**Tolerated Past**) — Python: `vulture`, once with the test roots included and
  once without, so a symbol only tests consume stands out; TypeScript: `knip`.
- **Dependencies** (**Dependency Drift**) — unused, undeclared and transitive-only packages from
  `deptry` or `knip`; outdated ones from the package manager, with each runtime version file and
  each container file's `FROM` line set beside the newest stable release; advisories from the
  package manager's audit; and commit-hash pins from the search below, run over workflows,
  manifests and shared checkouts.
- **One-call wrappers** (**Pass-Through Layer**) — a syntax-tree script kept in the run's working
  files, on Python's `ast` or TypeScript's `ts-morph`: every function whose body, after its
  docstring, is one returned or bare call whose arguments are its own parameter names or constants,
  printed with its target and caller count.
- **Single-implementation abstractions** (**Speculative Abstraction**) — the same kind of script:
  every Protocol, abstract base, interface or abstract class with its implementers and subclasses
  counted across the whole tree, listing those with zero or one.
- **Module table, symbol index and import graph** (**Scattered Structure**, **Duplicate
  Implementation**, **Divergent Siblings**) — public names per module from the syntax tree, the
  catch-all search and line counts below, and the import graph from `import-linter` contracts or
  `pydeps` for Python and `madge` for TypeScript, with every edge into an executable marked.
- **Suppressions and escape hatches** (**Tolerated Past**) — the suppression search below, counted
  per file.
- **Warnings** (**Tolerated Past**) — every warning printed in the saved output of
  `doctor-protocol`'s baseline checks, which already run install, build and each suite once, kept
  as a list. The pre-pass runs nothing again with warnings as errors, which would cost as long as
  the suites again to find warnings that output already shows.
- **Environment reads** (**Configuration Drift**) — the environment search below outside the
  settings modules, and each deployment's configuration column, read by name once.
- **One-machine paths and banned terms** (**Repeated Literal**, **Reads As Slop**) — the path
  search below over committed files, and a whole-word, case-insensitive search for each term
  `banned-terminology`'s list and the repository's own table hold, over identifiers and file names.
- **Migration replay** (**Migration Chain**) — the chain replay and drift check the repository's
  migration tooling defines.
- **Use-case candidates** (**Fragmented Use Case**) — the use-case table's candidate rows, each
  loaded and timed as **Inventory** says.
- **Styling count** (**Hand-Written Styling**) — each app's hand-written styling count, as that
  lens defines it.

```sh
ruff check --select SIM,RET,C90,PLR,ARG --no-fix <source roots>
pylint --disable=all --enable=R1702,R0915,R0912,C0121,R1703,R1705,R1719,W0611 <source roots>
vulture <source roots> <test roots> --min-confidence 80
vulture <source roots> --min-confidence 80
npx knip --reporter json
deptry .
npx knip --dependencies
poetry show --outdated
npm outdated --json
pip-audit
npm audit --omit=dev
rg -n 'uses: .+@[0-9a-f]{40}' .github
rg -n '\b[0-9a-f]{40}\b' <manifests>
rg --files -g '{utils,helpers,common,misc}*'
git ls-files | xargs wc -l
pydeps --show-deps <package>
npx madge --circular --json <source root>
rg -c 'type: ignore|pyright: ignore|noqa|pylint: disable|@ts-ignore|@ts-expect-error|biome-ignore|eslint-disable|\bAny\b|cast\('
rg -n 'os\.environ|os\.getenv|process\.env|import\.meta\.env'
rg -n '/home/|/Users/|/tmp/|[A-Za-z]:\\'
```

### Measures

The counts `doctor-protocol` takes before the audit and again after the fixes: lines and files per
project (`cloc`, or `wc -l` over tracked files); exported symbols; declared dependencies, and how
many are outdated or carry an advisory; suppressions and escape hatches; duplication-detector pairs;
lint and type findings; dead-code, one-call-wrapper and single-implementation candidates; files past
the size limit; warnings printed by install, build and suites; environment reads outside the
settings modules; each app's hand-written styling count; and, per use case the run changed, its
calls and wait.

## Lenses

Read [the lens criteria](references/lenses.md) before building the inventory: each lens named here
and in this skill's other sections is a section of that reference, stating what the lens flags, the
checks that find every instance, the remedy, and what is left alone so a reviewer does not go
hunting. Its **Behavior Kept** section binds every lens that removes or rewrites executable code.
Every lens applies in every area, read in that area's language; **Hand-Written Styling** belongs to
the frontend area, **Migration Chain** to the migrations area, **Build And Root**, **Configuration
Drift** and **Dependency Drift** to the build area, and **Test Slop** to the tests area. Test Slop
runs `test-fixture`'s **Test Value And Retention**, **Naming Checks** and **Auditing Existing
Doubles** over every test module a finding in another lens changes; a migration-test deferral
record whose path no longer exists is reported to `defer-scope`.

| Lens | Flags | Reach |
| --- | --- | --- |
| **Pass-Through Layer** | A layer, wrapper or alias that only hands the call on. | Partition; caller and importer counts come from the symbol index. |
| **Speculative Abstraction** | Structure built for cases that never arrived. | Whole repository: implementers and callers are counted across the tree. |
| **Duplicate Implementation** | One question answered twice. | Whole repository. |
| **Fragmented Use Case** | One use case paying for many calls to owned operations, or for unbounded work. | Partition, by use case. |
| **Divergent Siblings** | Things of one kind built in different shapes. | Whole repository. |
| **Scattered Structure** | Code spread over more files and folders than its responsibilities need, or held in the wrong kind of file. | Partition; module pairs and split concerns are whole repository. |
| **Repeated Literal** | One meaning spelled out many times, or a literal that belongs to one machine. | Whole repository. |
| **Hand-Written Styling** | Styling written by hand where a shared component owns it. | Partition, by app. |
| **Reads As Slop** | Code a reviewer recognizes as generated: correct, and still a shape no careful author writes. | Partition. |
| **Tolerated Past** | Code that tolerates a past the repository no longer has, or silences what would report it. | Partition; dead entries and unused exports are whole repository. |
| **Migration Chain** | A chain, its registries and its tooling, held to one shape and no more machinery than the job. | Partition, by chain; chains are compared across the repository. |
| **Build And Root** | Build, CI and root files carrying more than they need, or built against the workflow rules. | Whole repository. |
| **Configuration Drift** | A configuration name out of step in the matrix, or optional where a deployment needs it. | Whole repository. |
| **Dependency Drift** | Dependencies out of step with what the code imports, or behind their owners' releases. | Whole repository. |
| **Test Slop** | Tests that cost reading time and prove nothing. | Partition. |

Every finding is recorded in `doctor-protocol`'s finding shape. Its fix names the surviving owner,
each caller or importer that moves and what is deleted; its proving check is the covering check
**Behavior Kept** requires.

## Reviewers

Reviewers are capped as `doctor-protocol`'s **Launches** sets. The
areas dictate the partition cut: a partition never spans two areas, and inside an area it follows
the repository's ownership boundaries. The lens catalog a reviewer is given is the lens criteria
reference together with the **Lenses** table.

The cross-cutting reviewer owns the whole-repository lenses, working from the symbol index, the
module table, the import graph, every slot table, the configuration matrix and the dependency lists
in the pre-pass output. It matches helpers, declarations and modules that answer one question
across partitions, counts each abstraction's implementers and each export's consumers across the
tree, and lists every kind built in two shapes. It compares each kind's slot table across its
deployables, one shape across
packages, apps and languages, and every value defaulted in one package against its producer in
another; compares migration chains and registries with each other; reads each deployment column
against the settings model its process loads, one name declared on two models, and the locations
each checklist, manifest and example file names against the configuration matrix; and compares
manifests for one package pinned differently across projects or languages and a check one project
runs that its sibling does not.

The final reviewer tries to reach each removed layer,
branch, alias and operation from a live caller, confirms each merged operation returns only what
every run of its use cases needs, each batch or merged operation authorizes each item and each
returned field as the operations it replaced did, and each use case waits no longer than before,
confirms no import of a moved or renamed module still points at its old path, replays every chain
the run touched, confirms a stacked migration correction did not narrow the planned downgrade or
survivorship coverage, challenges every revision kept as applied without version-table evidence,
confirms each removed configuration name and package has no surviving reader or importer, re-traces
every retained package to an importer or an invocation, re-derives the matrix for every retained
mismatch, re-reads the deployment columns for every field kept as a local-development tool, confirms
each regenerated lockfile resolves its constraints, re-counts every app's hand-written styling and
confirms it reads zero, and re-runs each rewrite's covering check.

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
- A product or scope choice a remedy makes goes to the user as a reserved entry, as
  `doctor-protocol`'s **Gate And Show The Plan** says; the rest of a remedy's calls are this run's.
  A contract a consumer outside the user's control speaks stays as it is and
  is reported, under `pre-production`'s **Target Contract**.
- Fix the side that is wrong and delete the tolerance on the other, so one shape remains; a
  fallback that keeps both shapes working is the slop this doctor removes. A tolerance that hides a
  wiring defect is a confirmed defect and is fixed. An unsupported historical record is never a finding and never receives a
  fallback.
- A migration correction follows the migration skill's **Applied Is What Makes History**, stacked
  when applied state cannot be established; a data-loss path with no recovery is a blocker to
  report.
- A configuration default its reader refuses is declared nowhere until the disagreement is settled:
  the reader is wrong when nothing that ships can use the value, the declaration and deployment are
  wrong when something can, and where the target contract does not show which, the run puts the
  two fixes to `council` and makes the one it rules for. A field nothing deployed sets takes one
  of three outcomes the plan names: a deployment
  should carry it, it is a local-development tool retained with the tool and the branch named in the
  ledger, or it is deleted with the branch its value selects.
- An even split between two sibling structures equally fit for the kind goes to the one leaving the
  fewest mechanisms and moving the fewest importers, stated in the pull request.
- A cleanup finding another doctor owns — documentation, a contract model, a deep test audit — is
  not fixed here; the report names it with that doctor, found through `get-doctors`. A confirmed
  defect or vulnerability met in another doctor's area is fixed in this run, as `doctor-protocol`'s
  **Resolve The Scope** says.

## Report Additions

- per area and lens: findings and dispositions by package and language;
- each pre-pass command with the tool that ran it;
- each kind's slot table before and after;
- each module merged, moved, renamed, collapsed or split, with its importers moved;
- each layer, abstraction and alias removed, with its callers;
- the use-case table's candidate rows before and after: calls and wait per use case, each operation
  merged, batched, bounded or deleted with its callers moved, and each merge decided with its
  reason;
- each duplicate and its surviving owner; each kind brought to one shape, and each better shape
  adopted with the instances it converted;
- each flag gating a former behavior, its readers and retiring backfill; each suppression and
  escape hatch removed and the rule code added as its guard; each check whose verdict gates
  again; each warning cleared and each deprecated usage replaced;
- per migration chain: heads, revisions checked by lens, corrections, policy coverage before and
  after, and the evidence for applied state;
- each build, CI and root file consolidated or deleted, and each workflow finding by the bullet it
  broke;
- the configuration matrix with every changed cell, and each deployment column read or unread with
  the reason; the readers traced for each removal; for every field no deployment sets, its outcome;
  each value made required with the absence branch deleted;
- per manifest: declarations removed, added, upgraded and re-ranged; each runtime and base image
  moved; each pin replaced; each lockfile regenerated with its command; audit tools wired in or
  removed; each package held back with the failure that holds it;
- each app's hand-written styling count before and after, and each variant or prop added to a shared
  component in its place;
- each shape **Reads As Slop** rewrote, by check, each rule change it made on its agent-configuration pull request for a
  shape a rule keeps, and the test that carries each deleted comment's behavioral guarantee;
- each rewrite's covering check with its result before and after, and each test written first
  because none reached the code;
- each test removed or repaired with the layer it exercised;
- each finding another doctor owns, named with that doctor.
