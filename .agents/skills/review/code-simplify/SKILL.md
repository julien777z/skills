---
name: code-simplify
description: Strictly review the branch's changes for reuse, simplification, abstraction quality, and maintainability, then fix the issues. An ambitious code-quality pass that hunts for structural simplifications (code-judo moves), giant files, and spaghetti-condition growth.
---

# Code Simplify

Use this skill for an unusually strict review focused on implementation quality, maintainability, abstraction quality, and codebase health.

Above all, this skill should push the reviewer to be **ambitious** about code structure. Do not merely identify local cleanup opportunities. Actively search for "code judo" moves: restructurings that make the implementation dramatically simpler, smaller, more direct, and more elegant.

## Applying fixes

This skill does not stop at review: **apply the simplifications you identify directly to the working tree.** Restructure, extract, delete indirection, collapse branches, reuse the canonical helper, and keep those edits in the commit you are working on. The criteria — what the pass holds itself to, the reuse and ownership searches, the standards, the review questions, what to flag, the remedies, the tone and the approval bar — are `references/rubric.md`. Read it whole before the pass and apply all of it as the checklist for what to fix, not merely what to flag.

## Running the pass

**Review small scopes in process.** A scope is small when one reviewer can hold the complete diff, every touched file, and the relevant siblings at once without losing context. Focused changes to one or a few files, especially documentation or configuration changes, normally qualify. Do not spawn subagents merely because the host exposes them, and do not add a cross-cutting reviewer for a small scope.

**Use subagents for scopes that benefit from independent review.** Fan out when the scope is large enough to partition into two or more coherent slices, or when relationships across multiple subsystems materially benefit from a separate cross-cutting review. Partition by app, service, or package rather than arbitrary file counts, and give every reviewer the same complete rubric over its slice. When an introduced subsystem, runtime boundary, or independent consumer has analogues whose complete implementations will not fit comfortably in one review context, add one read-only cross-cutting reviewer to compare their ownership and duplication while slice reviewers cover their own areas. Skip that reviewer when one reviewer can hold the complete change and every analogous implementation at once.

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

**Four greps come first.** Before reading the diff for anything else, grep its added lines for four shapes and list
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

A report that lists no hit for any of the four greps says so in those words.

**What a scope contains.** A scope is never the diff hunks alone. Resolving any scope — the pre-push merge-base diff or one a caller names — yields three things: the **diff** itself, the **full contents of every file it touches**, and the **sibling modules in those files' packages**. Hunks show what changed; the whole file shows what the change now sits inside; the siblings show where the logic should have lived. A code-judo move is usually only visible in the third, and `references/rubric.md` applies to everything the scope resolves to, not only to lines the diff added.

**The scope says what must be read, never what may be reported.** It is a floor on the reading, so a
reviewer who read less than it resolves to has not finished; it is not a boundary a finding has to
sit inside. A defect that reading leads to outside those three things — in another package, in a file
the diff never opened — is a finding like any other, and the reviewer who saw it is the one who fixes
it.

The rubric's reuse, ownership and deletions section says what to search for across the resolved scope,
and what holds a finding back; its section on dispositions says what may never hold one back, where
the finding lives among them.

When run as the pre-push pass (for example from the Stop hook), start from the **same diff as code-review's local / pre-push mode**: `git diff $(git merge-base <base> HEAD)` plus any untracked files the branch adds, where `<base>` is the repository's remote default branch (for example `origin/main` — use the actual default branch name; fall back to the local default branch if no remote is configured). This covers branch commits and uncommitted working-tree changes without unrelated upstream commits. Then resolve it into the three things above.

When a caller provides a **broader scope** instead — for example the whole repository or specific directories or files — apply this rubric across **that** scope, not the pre-push diff. The merge-base diff above is only the default for the Stop-hook pre-push pass; always honor an explicit scope from the caller, preserve external contracts, and expand to every internal consumer needed for a complete simplification.

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

Report the repository-wide reuse searches performed for newly introduced abstractions, including the concepts searched and the canonical candidates inspected. A clean result without this evidence is incomplete whenever the diff adds one of those abstractions.

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
