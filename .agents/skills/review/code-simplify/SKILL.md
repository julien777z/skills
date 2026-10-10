---
name: code-simplify
description: Strictly review the requested change and its required dependencies for reuse, simplification, abstraction quality, and maintainability, then fix admitted issues. Seek substantial simplifications within that objective; necessary consumer edits and comparison reads do not authorize unrelated cleanup.
short_description: 'Strictly review the branch''s changes for reuse, simplification, abstraction quality, and maintainability, then fix the issues.'
---

# Code Simplify

Use this skill for an unusually strict review focused on implementation quality, maintainability, abstraction quality, and codebase health.

Be ambitious about simplifying the implementation under judgment: seek restructurings that remove complexity from its actual mechanism. Judge their complete dependency updates and cumulative scope before applying them; a new cleanup objective does not become relevant merely because the pass discovered it.

## Dependencies

- `pre-production` — classify required repairs and bounded local refactoring before widening edits.
- `subagent-selection` — route each reviewer subagent through the running session.
- `test-fixture` — own test value, fixture, and class/file boundaries when the scope reaches tests.
- `list-prs` — reconcile task-work pull requests for the affected-repository comparison.

## Applying fixes

Apply `pre-production`'s scope decision to the observations before prescribing edits. This skill does not stop at review: **apply admitted repairs and simplifications directly to the working tree.** Restructure, extract, delete indirection, collapse branches, reuse the canonical helper, and keep those edits in the commit you are working on. The criteria — what the pass holds itself to, the reuse and ownership searches, the standards, the review questions, what to flag, the remedies, the tone and the approval bar — are `references/rubric.md`. Read it whole before the pass and apply all of it as the checklist for what to fix, not merely what to flag.

## Running the pass

Before resolving the rubric's affected-repository map, invoke `list-prs` for the ongoing task.
Inspect the current heads and relevant implementations of applicable task pull requests, including
unmerged work in other repositories; a default-branch checkout alone can miss the comparison.
Record which related implementations were compared, the shared convention, and the concrete reason
for any retained difference. Exclude unrelated task artifacts with their reason. Reuse a caller's
verified lookup when its scope and heads are still current; discovery grants no new mutation authority.

When the scope includes tests, fixtures, or test support, invoke `test-fixture` before inspecting or changing those surfaces; load its value, retention, and class/file criteria for the review.

**Review small scopes in process.** A scope is small when one reviewer can hold the complete diff, every touched file, and the relevant siblings at once without losing context. Focused changes to one or a few files, especially documentation or configuration changes, normally qualify. Do not spawn subagents merely because the host exposes them, and do not add a cross-cutting reviewer for a small scope.

**Use subagents for scopes that benefit from independent review.** Fan out when the scope is large enough to partition into two or more coherent slices, or when relationships across multiple subsystems materially benefit from a separate cross-cutting review. Partition by app, service, or package rather than arbitrary file counts, and give every reviewer the same complete rubric over its slice. When an introduced subsystem, runtime boundary, or independent consumer has analogues whose complete implementations will not fit comfortably in one review context, add one read-only cross-cutting reviewer to compare their ownership and duplication while slice reviewers cover their own areas. Skip that reviewer when one reviewer can hold the complete change and every analogous implementation at once.

**After fixing a scope's findings, rescan that scope.** Return the updated complete scope and the
fix diff to its reviewer, asking it to check both the remedies and anything else the fixes expose.
Use the same reviewer when available, otherwise a fresh reviewer with the previous findings.
Unaffected clean scopes do not restart. This scope rescan is not a replacement for a separate
acceptance gate or its requirement for a fresh independent gate reviewer.

For final review, assign one read-only reviewer per coherent scope, with the scopes together
covering the complete change. Do not send the same question and scope to duplicate agents. Review
finished features, not intermediate edits, and reuse clean scope results until their code,
dependencies or relationships change.

**Subagents run on the host's mid-sized model** — Sonnet on a Claude host, the equivalent elsewhere — named explicitly, since an unset model inherits the orchestrator's.

**Subagents review; the parent applies.** When subagents are warranted, every subagent returns findings — each anchored to a path and line, with the restructuring it proposes — and edits nothing. Concurrent writers on one tree produce conflicts and half-applied restructurings, and one applier is what keeps the result a single coherent change. The parent resolves the returned findings, drops any that another slice's finding subsumes, applies the survivors itself, and remains answerable for the approval bar.

Before applying anything, the parent checks each report against the file list it briefed. A file
with no line in the report is re-briefed on its own, never assumed clean because the report found
nothing else to say.

**Brief each slice by what its modules hold, never by their history.** Name a path and its public
symbol count; "renamed from", "moved from", and "generalized" hand the reviewer a disposition before
it has counted, and the count is what the reviewer owes. A history label the parent attached is the
first thing a reviewer must ignore.

## Scope

**Five greps come first.** Before reading the diff for anything else, grep its added lines for five shapes and list
every hit as a finding ahead of all others, with the remedy the rubric names:

1. **A reader reaching through a table keyed by a model, class or type for a fact about the key**
   — the pattern `[A-Z_]+\[` followed by a model, record, class, `type(` or `cls` expression, as in
   `FORM_TYPES[model].label` or `KINDS[type(record)]`. Each hit is a finding whether or not the diff
   added the table: the value belongs on the key as a class attribute or property, every reader
   moves onto it, and the table goes.
2. **A repository-wide fact held as a loose string** — an email address, a street address, a legal
   entity or product name in a string literal outside one typed model in the package every consumer reads. Each hit
   moves onto that model, which every consumer reads.
3. **A container declared for one member** — the pattern `APIRouter(` (or the framework's router
   constructor) in an added line, followed by a count of the handlers registered on that router in
   the resulting tree. One handler is a finding whether or not the diff added the router, and it is
   the rubric's one-symbol module wearing a decorator: the handler moves onto the router that already
   owns its resource, at a path under that resource, and the router and its module go. A prefix
   ending in a verb or an operation — `/request`, `/remind`, `/export` — is the same finding read
   from the URL.
4. **A data-holding class declared outside model ownership** — every added `BaseModel`, dataclass,
   named tuple, or equivalent record declared outside a `models.py` file or `models/` package. Move
   it to a concept-specific model module. Only a Pydantic `BaseSettings` class is configuration and
   belongs in `config.py` or `config/`; registries, manifests, policies, provider payloads, and
   response schemas remain models. Never move a model into operational code merely to eliminate a
   one-symbol declarative module.
5. **A typed parameter built as a dict** — an annotation on a dict literal, `name: SomeTypedDict = {`
   or `params: sdk.params.X = {`, and a bare dict passed where an SDK or repository signature names a
   `TypedDict`, at any nesting level. Each hit is rewritten as the constructor call
   (`sdk.params.X(...)`, `sdk.RequestOptions(...)`), with tests asserting the same way.

A report that lists no hit for any of the five greps says so in those words.

Before ranking structural findings, scan adjacent statement pairs in every added or substantially
edited function after formatting. List exact line pairs where a completed guard meets setup, one
guard meets the next, a derived value meets its validation, or a copy or mutation meets
postprocessing or comparison. Every missing blank line at those boundaries is a legibility finding;
do not suppress it as a cosmetic nit or omit it because a larger finding exists. Also list every
conditional selecting a fixed set of string statuses, including log-only values, and flag inline
literals where the applicable language rules call for a named finite-state type. In Python use
`Enum` for internal states and `StrEnum` for string contracts; in TypeScript follow the const-object
and value-union rule. A clean report must show the inspected pairs and status conditionals, not just
say readability and types were checked.

List every guard, refusal, validation, or branch the diff adds or edits with the writers of the value
it tests and of what its path reads next, each named by path and function. One whose refused inputs
those writers already exclude, or a check on the path already refuses, is dead code under the
rubric's standard 1 and takes that standard's remedy. A report without that list, or one that keeps
such a guard as legitimate, has not run the check.

**What a scope contains.** A scope is never the diff hunks alone. Resolving any scope — the pre-push merge-base diff or one a caller names — yields three things: the **diff** itself, the **full contents of every file it touches**, and the **sibling modules in those files' packages**. Hunks show what changed; the whole file shows what the change now sits inside; the siblings show where the logic should have lived. A code-judo move is usually only visible in the third, and `references/rubric.md` applies to everything the scope resolves to, not only to lines the diff added.

**Reading scope and editing scope differ.** Read the complete files and relevant siblings to
understand ownership and verify the change. Apply `pre-production`'s scope decision before turning
an observation into a required edit: a confirmed defect and a flaw in the changed design require a
complete repair, including consumers outside the starting files; an independent structural
improvement must earn inclusion as a bounded local refactor. A newly touched consumer does not
become another cleanup frontier. Explicitly requested broad reviews retain their stated scope.

The rubric's reuse, ownership and deletions section says what to search for across the resolved scope,
and what holds a finding back; its section on dispositions says what may never hold one back, where
the finding lives among them.

When run as the pre-push pass (for example from the Stop hook), start from the **same diff as code-review's local / pre-push mode**: `git diff $(git merge-base <base> HEAD)` plus any untracked files the branch adds, where `<base>` is the repository's remote default branch (for example `origin/main` — use the actual default branch name; fall back to the local default branch if no remote is configured). This covers branch commits and uncommitted working-tree changes without unrelated upstream commits. Then resolve it into the three things above.

When a caller provides a **scope** instead — for example the whole repository or specific directories or files — apply this rubric across **that** scope, not the pre-push diff. The merge-base diff above is only the default for the Stop-hook pre-push pass; always honor an explicit scope from the caller, preserve what a consumer outside the user's control observes, and expand to every owned consumer, in any repository, needed for a complete simplification.

## Output Expectations

The report opens with the slice's file list and carries a line for every entry. The list is every
path the briefing names and every path the diff touches, in the briefing's order: the modules the
change adds, the files it only modifies, the files it deletes or renames away, and each sibling read
for comparison. A consumer the change edits and a sibling read for its pattern are entries like any
new module, never context for the entries. Each appears by path with its disposition: for a module,
its public symbol count and the finding against it or the word clean per standard; for a deleted
file, what replaced it; for a sibling, what it holds that the change should have used. A file the
report does not name has not been reviewed, whatever else the report says. A report that covers some
files in its slice and stays silent on the rest is a partial review, and the standards it applied to
the files it did name do not transfer to the ones it did not.
The questions a briefing asks steer emphasis, never scope: a file no question mentions is reviewed
and reported like every other, and answering the questions is not the review.

Report the flow receipt required by the rubric’s **Trace Changed Flows**, including the affected-repository map, repository-wide reuse searches, and canonical candidates inspected. Apply it to changed existing operations as well as newly introduced abstractions; a clean result without this evidence is incomplete.

For every new public concept, list the existing peer interfaces and owners inspected, state whether
the new behavior is a variant under one of them or needs an independent contract, and verify the
resulting registry, command, package, and consumer boundaries. A clean report without that comparison
is incomplete when the change adds a public concept.

For every new independent consumer or boundary, report the analogous implementations inspected, the
candidate shared owners, the common mechanism and consumer-specific behavior identified, and the
reason each parallel implementation was consolidated or retained.

For every new module or package, report its public symbol count, the sibling modules in its package
with the same shape, the importers and candidate owners inspected, and why the boundary was retained,
flattened, or merged. A new module reported without its count is an unreviewed module.

For every new enum, constant set, mapping, alias, or model, report the member names or keys you
searched the repository for — the members themselves, never the declaration's own name — and every
existing declaration found holding any of them, or the enum modules and packages searched and found
without one. For every new model, also report its model-owned path or flag its placement. For every
module-level assignment the diff adds, quote the line and state whether it
carries a type. A declaration reported without that search, or an assignment reported without its
type, is an unreviewed declaration.

Prioritize findings by what kind of problem each is, in this order. Where a finding sits does not
depend on whether the diff introduced it: a pre-existing structural problem is a structural problem.

1. Structural code-quality problems
2. Missed opportunities for dramatic simplification / code-judo restructuring
3. Spaghetti / branching complexity
4. Boundary / abstraction / type-contract problems that make the code harder to reason about
5. File-size and decomposition concerns
6. Modularity and abstraction issues
7. Legibility and maintainability concerns

Do not flood the review with low-value nits if there are larger structural issues.
Prefer a smaller number of high-conviction comments over a long list of cosmetic notes.

For every test module the diff adds or changes, list its module-level definitions that are not test
classes — functions, constants, models — and the `utils/` or `fixtures/` module each one moved to. A
test module reported without that list is unreviewed.
