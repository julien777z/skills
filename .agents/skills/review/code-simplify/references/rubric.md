# Code Simplify Rubric

The criteria the code-simplify pass applies to everything its scope resolves to. `SKILL.md` says how
to run the pass; this file says what it judges, and other skills that borrow the rubric read this file.

## What The Pass Holds Itself To

**What the pass writes after the review is reviewed too.** A finding fixed during the pass meets the
rubric by construction. The code written *afterwards* — to satisfy a checker, to turn a red check
green, to answer a reviewer — does not, because the review that would have caught it is already over,
and it lands in the same change reading as reviewed. Hold every later edit to these standards before
pushing it, in the same terms: what it adds, what shape it takes, and whether the thing it sits beside
already owns that concern. The edit answering a tool is the one most likely to escape, because the
report reads as the whole specification and going green reads as done; a green tool says a check
passed, never that the code earned its shape.

**Preserve observable behavior and external contracts beyond the system boundary — including on the default pre-push pass.** Do not change public routes and their request/response shapes, durable identifiers (handler, event, queue, and state keys), or persisted on-disk and on-the-wire formats (DB columns, migrations, serialized payloads). Internal API shapes, shared DTOs, configuration, and cross-repository callers are simplification scope: trace every consumer and update them in the same coordinated change. Do not leave a worthwhile simplification as a written note merely because it crosses a repository or changes an internal contract, and do not add pass-through or compatibility shims — adjust the real call sites instead.

**Tests are not a contract, and a test seam never vetoes a finding.** Tests describe the application code; the application code is never shaped — or left unshaped — to preserve a test's mock, fixture, or monkeypatch target. When a legitimate simplification moves, renames, or absorbs a symbol that tests patch or import, the tests change with it: rewrite the patch targets and fixtures to the new binding as part of the same change, and rerun the affected suite when a runner is available. Declining a finding because "a test patches that symbol" inverts the dependency and is never a valid disposition; the only test-related grounds for holding back is that the pass genuinely cannot update or run the affected tests, and that is reported as an applied-with-caveat or a written note naming the exact tests, never as a rejection of the finding.

## Reuse, Ownership And Deletions

**Read the diff's deletions before its additions.** A change that removes a shape has made that shape
a finding wherever the same change adds it — in a fix for a review finding, in a resolved record, in
a hunk reconciled from the base — and it reads as correct precisely because the rule it breaks is
the one the diff is establishing.

For every new abstraction, helper, client, lifecycle, model, or utility, also search the whole repository by concept, dependency type, and key operations before concluding it is canonical. A sibling-only read cannot find an established implementation owned by another package.

When a change introduces another independent consumer of a cross-cutting mechanism, compare it with
every existing consumer by responsibility, dependencies, inputs, outputs, and side effects — names
and file paths are not the search boundary. A second implementation is presumptive evidence that the
mechanism belongs to a shared owner. Separate that mechanism from consumer-specific policy,
configuration, composition, registration, and dependency wiring; differences confined to those
inputs or to a small additional case normally become parameters or extensions of one implementation,
not reasons for parallel copies.

Consolidation updates every in-repository consumer and removes the superseded implementations; the
newest copy is not the whole scope. Keep implementations separate only when sharing would invert a
dependency, couple unrelated domains, weaken a contract, or force a consumer to depend on capability
it does not use, and establish that boundary from the actual dependency and consumer graph.

Verify ownership completion, not only discovery. For each related implementation found in the
repository-wide search, record whether it was consolidated, replaced, or retained behind a proven
dependency, domain, or contract boundary, then check that disposition against the resulting code
and every consumer. An unchanged implementation left outside its newly declared owner is a
finding against that new boundary, not unrelated pre-existing debt. A clean receipt that lists
candidate owners without verifying the dispositions is incomplete.

Search by responsibility as well as declaration syntax: functions, methods, nested builders, and
constructor calls can own the same model-generation behavior as a factory subclass. Read the bodies
and consumers before accepting a retained implementation as lifecycle, persistence, registration,
or scenario wiring; a different spelling or decorator establishes no ownership boundary.

Treat every new module and package as an abstraction that must earn its boundary. Read its full
contents, every importer, and its parent and sibling modules before accepting it; standard 2
says what to count there. When independent consumers need shared ownership, prefer a flat shared
module over burying it in one consumer. Collapse a package containing only one module unless it
names an established extensible category or enforces a real dependency boundary — multiple
importers justify shared ownership, not an extra directory hop.

The diff narrows where to start looking, not which concrete issue naturally encountered in that
resolved scope must be fixed.

The one thing that does hold a finding back is risk you have not retired. A change whose behavior you cannot yet establish — a limiter whose failure mode differs between two implementations, a shared contract whose callers you have not enumerated — is verified first and then applied, not waved through and not quietly dropped. Establish the behavior, then make the change; where the pass genuinely cannot establish it, say exactly what is unverified and why, per the written-note rule above.

## Guidance Prose Is Not Code

This rubric applies to `.agents` rules and skills as readily as to code — a rule stated twice in two
files, a section grown around a second subject, a heading named for a category with one member. One
kind of repetition is the exception, and it is load-bearing.

**A skill restating a rule is never a finding.** The two are read under different conditions: a skill
is pulled in at the moment its task starts and is short enough to be read whole, while a rule file is
long and ambient. When they say the same thing, the skill's copy is the one that changes behavior.
Deleting it to leave "one home" trades a sentence that gets followed for one that gets skimmed, and
the loss is invisible — the guidance still exists, so nothing looks broken until the work it governs
is done wrong.

- Leave the skill's copy where the two overlap, and leave the rule's copy too. Neither is dead weight.
- Where they disagree, that is a real finding: reconcile them rather than deleting either.
- Duplication **between two rule files**, **between two skills**, or **within one file** stays a
  finding. The exception is specifically the skill-to-rule direction, and it is about which copy an
  agent actually reads at the moment it matters.
- A skill that quotes a rule and adds nothing of its own is still a skill worth having; judge it by
  whether the guidance reaches the reader at the right time, not by whether the words are unique.

## Core Prompt

Start from this baseline:

> Perform a deep code quality audit of the current branch's changes.
> Rethink how to structure / implement the changes to meaningfully improve code quality while preserving behavior outside deliberate target-contract changes.
> Work to improve abstractions, modularity, reduce Spaghetti code, improve succinctness and legibility.
> Be ambitious, if there is a clear path to improving the implementation that involves restructuring some of the codebase, go for it.
> Be extremely thorough and rigorous. Measure twice, cut once.

## Non-Negotiable Additional Standards

Apply the baseline prompt above, plus these explicit review rules:

0. **Be ambitious about structural simplification.**
   - Do not stop at "this could be a bit cleaner."
   - Look for opportunities to reframe the change so that whole branches, helpers, modes, conditionals, or layers disappear entirely.
   - Prefer the solution that makes the code feel inevitable in hindsight.
   - Assume there is often a "code judo" move available: a re-organization that uses the existing architecture more effectively and makes the change dramatically simpler and more elegant.
   - If you see a path to delete complexity rather than rearrange it, push hard for that path.

1. **Ask of every new abstraction whether it should exist at all, before asking whether it duplicates one.**
   - "Is this a duplicate?" and "does this belong here?" both presume the thing is wanted. Answer the
     prior question first: delete it entirely and what breaks? If the answer is "nothing a platform,
     framework, or runtime we already depend on was not already doing", the finding is delete it, and
     no amount of tidy structure changes that.
   - **A clean, well-named, well-placed, non-duplicating abstraction can still be pure cost.** Those
     qualities are what make this one hard to see: it passes every structural check precisely because
     someone wrote it carefully. Judge what it *achieves*, never how it reads.
   - Be most suspicious where the codebase already has a real mechanism for the job — the server's own
     concurrency limits, the framework's lifecycle, the database's constraints, the library's retries.
     A hand-rolled version beside one of those is usually weaker than it appears and has to be argued
     for against the built-in, not merely shown to be tidy.
   - **State what it actually guarantees, not what its name claims.** An in-process counter guarding a
     multi-replica service, a check the caller can bypass by another route, a limit whose real ceiling
     is the stated one times the number of processes: each protects far less than it advertises, and
     the name is what stops anyone noticing. Where the guarantee is weaker than the name, say so in
     those terms.
   - Its author having also written the finding it answers is a reason to look harder, not to defer.
     Nobody else has yet asked whether the problem was real.

2. **A module holding one symbol is a finding before anything else about it is judged.**
   - Count before you read: a module whose public surface is one function, one small class, or one
     constant plus its helper has not earned a file. Say the count in the finding.
   - A router is a container the same way, and a router carrying one handler is the same finding:
     count the handlers registered on every router in scope and say the count. One handler moves
     onto the router that already owns its resource, at a path under that resource, and the router
     goes with its module; a router earns its place only for a resource no existing router
     addresses, or a prefix, tag or guard the existing one cannot carry.
   - Look for the same shape everywhere in scope, not only in the same package: a sender beside a
     sender, a handler beside a handler, whatever directory each landed in. Several modules that each
     hold one symbol of one shape are one module wearing several names. Collapse them into one named
     for the concern they share, widening the module that already exists rather than adding beside it.
   - A sibling with more importers is not exempt. Importer count justifies shared ownership; it never
     justifies a file per symbol. Two one-symbol modules with two importers each are still one module.
   - Merge it into the existing owner when one exists, and an owner is a module that already holds the
     concern, not the nearest small module with room: a destination that is itself one or two symbols
     is another lone module, and moving into it changes the file name and nothing else. Keep a lone
     symbol in its own module only for a dependency boundary you can show from declared dependencies
     and importers, or an entry point the framework or packaging looks up by path.
   - Re-count after every relocation, on the source and on the target, and say both counts.
   - History is not a disposition. Count a module as it stands in scope, whatever the diff calls it —
     new, renamed, moved, generalized, or already there when the change arrived. "It held one symbol
     before" and "the replacement has the same shape as what it replaces" are the pre-existing excuse
     the scope section refuses, restated for one file: a matching count on both sides is the finding
     confirmed twice, never dismissed.
   - A lone symbol that arrives by rename or generalization is the cheapest one to merge. The change
     already rewrites every importer, so filing it with the module that owns its concern costs nothing
     the rename did not, and leaving it alone under a new name spends that rewrite on a file that has
     still not earned its name.
   - **Declarative ownership outranks the count.** Never move a data model into a client, service,
     route, entrypoint, or utility to eliminate a one-symbol model module. Models stay in a
     `models.py` file or concept-specific `models/` package; only Pydantic `BaseSettings` classes
     stay in `config.py` or `config/`. A lone declarative module may be merged only with another
     declarative module under the same ownership boundary, never into operational code.
   - A concern no sibling shares is not a boundary. It is a symbol with no home yet, and "unique
     concern", "idiomatic for this package", "acceptable", "accepted", "stands", and "earns its file"
     never appear against a count of one: each is the disposition this standard takes out of the
     reviewer's hands. The report carries one finding per one-symbol module, headed with the path and
     the count and closing with the module it merges into or the search still owed to find it.
   - Nor is "no owner in this slice" or "several importers" a disposition. Importers are consumers,
     and a boundary is a dependency the module is not allowed to take, shown from declared
     dependencies rather than inferred from who calls it. Siblings that share the one-symbol shape are
     the finding above multiplied, never a convention that excuses one more. A slice that shows no
     owner shows only where the search has not reached: report the module as an open finding that
     names the search still owed, and never write "accepted", "not escalated", or "stands as
     reviewed" against a count of one.

3. **A new declaration that names what the repository already declares is a second copy, wherever it is filed.**
   - Before accepting any new enum, constant set, mapping, alias, or model, search the repository for
     the same set by what identifies its members, never by its name: grep every enum module for a new
     enum's member names, search for a mapping's key set, for a model's discriminator. A duplicate
     arrives under a different name, with different values, in a different package, and a search by
     name never finds it.
   - Two enums with the same member names are one enum. The second one's values — a display label, a
     wire code, a file suffix — are a property on the first, never a sibling declaration and never a
     second enum relocated to the shared package. A mapping keyed by a set an enum already declares
     is the same case: its values belong on that enum's members.
   - File a declaration where its consumers meet. One that two services or packages read belongs in
     the package that declares shared shapes, never beside the first consumer that needed it.
   - Report the search with the finding: the existing declaration found, or what was searched and
     found absent. A new declaration reported without that search is an unreviewed declaration.

4. **A generic helper with one caller is an unfinished sweep, not a finished extraction.**
   - When a helper's contract names no domain type and its logic would serve elsewhere, one call site
     usually means the author stopped at the site that prompted it. Search the repository for the other
     places doing that job **by the operation, never by the name** — they will not share its vocabulary,
     which is exactly why the first pass missed them.
   - Two live implementations of one guard, check, or transform is the defect, whichever came first.
     The duplicate is not excused by having fewer callers, by raising a different error type, or by
     taking its input in a different shape; those are the forms drift takes, not reasons to keep both.
   - **Do not settle this on efficiency.** "Reusing the canonical one costs a lookup" is how a second
     definition of a security check earns its place, and a check defined twice will eventually disagree
     with itself. Widen the canonical one to take what this caller holds; keep two only when merging
     would genuinely make a caller do something wrong, and name that caller.
   - The remedy is one definition and every site calling it, or the helper folded back into its single
     caller. Leaving it generic, named, and used once is the outcome to avoid.

5. **Re-read every function an extraction leaves behind.**
   - Pulling a body into a shared helper routinely reduces its former home to a single forwarding call.
     That is the wrapper ban's exact shape, created by the fix rather than found by it, and it is
     invisible unless the pass looks again at what it just edited.
   - After each extraction ask what remains: if the leftover is one call to the new helper, inline it at
     its call sites or give the helper the signature that removes the need for it.
   - An adapter between two contracts you own is not exempt by default. Where a callback protocol and a
     helper disagree on shape, change one of them — the mismatch is usually the finding, and a function
     parked between them the workaround.
   - **The exception is a mismatch neither side may absorb**, which happens where a package deliberately
     limits what it depends on. A library that stays clear of the application's shared layer cannot take
     that layer's enums or tables into its contract, and a generic helper cannot take the library's
     domain vocabulary; the translation then has nowhere to live but between them. Establish that from
     the package's declared dependencies before accepting it — a boundary nobody chose is just coupling
     that has not been noticed yet.
   - Such an adapter earns its name only while it makes real choices the contracts do not: which table,
     which field, which member of an enum. Strip those away and it is a forward again.

6. **A function whose parameters are one declared shape is a method that shape is missing.**
   - **List them before judging any of them.** Every function in scope whose parameters are one type
     the repository declares, and whose body only reads that parameter, goes in one list with its
     count. The list is the finding. A report that meets such a function on its own has already lost:
     judged one at a time, each looks like a small helper, and a whole method set stays outside the
     shape it belongs to.
   - The count is what shows it. One is a helper worth a second look; several over the same shape are
     that shape's methods scattered across a module, each added by an author who saw only the one
     beside it.
   - **Collapsing them into one parameterized function does not answer this standard.** Folding
     several readers into one reader with flags answers *how many there are*; this standard asks
     *whose behaviour they are*. One free function that still takes the shape and reads it is the same
     finding with a smaller count.
   - Taking the shape and a collaborator is the same finding: a list to search, a callback to apply, a
     registry to consult — none of them moves the operation off the receiver it reads.
   - **Say what the declaration is and whether it can hold a method.** Reporting the functions and
     leaving the declaration unexamined stops one step short of the fix.
   - **A declaration that cannot hold a method is the finding, never the excuse.** Where the shape is
     a mapping-shaped type, generated output, or a third party's class, "the type cannot carry
     methods, so the functions stay" inverts the standard: what keeps them outside the shape is
     exactly what is wrong with the shape. Name what it becomes — the class or model that can hold
     what its readers hold today — and report that change as the remedy. "They would be methods if
     the type supported them" is that refusal in its most common wording, and it is not a
     disposition.
   - "Properly scoped", "independent queries", "no restructuring needed", "correctly kept separate",
     and "appropriate as a module function" never appear against such a list: each is the disposition
     this standard takes out of the reviewer's hands. The remedy is the method, named for the question
     it answers, with every caller reaching it through the value it already holds.

7. **Decompose any file in scope that is over 1000 lines.**
   - Treat this as a strong code-quality smell by default, whether or not the current change is what pushed the file over. A file already over the line when you arrive is still over it when you leave unless you act.
   - Prefer extracting helpers, subcomponents, modules, or local abstractions instead of letting a file sprawl past 1000 lines.
   - Relocate the extracted pieces to the module or package that already owns the concept, rather than leaving a thin file beside the original purely to reduce a line count.
   - Only waive this if there is a compelling structural reason and the resulting file is still clearly organized.

8. **Do not allow random spaghetti growth in existing code.**
   - Be highly suspicious of new ad-hoc conditionals, scattered special cases, or one-off branches inserted into unrelated flows.
   - If a change adds "weird if statements in random places", treat that as a design problem, not a stylistic nit.
   - Prefer pushing the logic into a dedicated abstraction, helper, state machine, policy object, or separate module instead of tangling an existing path.
   - Call out changes that make the surrounding code harder to reason about, even if they technically work.

9. **Treat every suppression the diff adds as a finding, and never add one yourself.**
   - A `# pyright: ignore`, `# type: ignore`, `# noqa`, `# pylint: disable`, a widened `except`, a new
     entry in a linter's ignore list, a lowered threshold, a hand-written stub or `typings/` directory:
     each buys a quiet tool while the thing being reported stays exactly where it was.
   - This is the one class of change that makes a diff *look* cleaner by making the codebase worse, so
     it is invisible to every other check in this rubric. Grep the diff for it explicitly rather than
     hoping it turns up while reading.
   - **A suppression is not evidence the finding was considered.** It reads identically whether the
     author weighed the report and judged it wrong or never looked at it, and the next reader cannot
     tell which. Nothing in the file records the reasoning, so the exemption outlives whoever had one.
   - Check the siblings before believing a suppression is necessary. An untyped import that every other
     call site in the repository imports bare is not a finding this one site has to silence; it is a
     finding somebody added noise to hide.
   - The honest answers are to fix what the tool is reporting, to publish types at the source when the
     package is ours, or to leave the report standing. A red tool carrying known reports is a truthful
     record of work still to do; the same run with them papered over is not.
   - Generated output is out of scope — a suppression inside a file the toolchain writes is that
     toolchain's business, not the author's.
   - This applies to your own edits with no exception. A pass that removes somebody else's suppression
     and adds its own has enforced nothing.

10. **Bias toward cleaning the design, not just accepting working code.**
   - If behavior can stay the same while the structure becomes meaningfully cleaner, push for the cleaner version.
   - Do not rubber-stamp "it works" implementations that leave the codebase messier.
   - Strongly prefer simplifications that remove moving pieces altogether over refactors that merely spread the same complexity around.

11. **Prefer direct, boring, maintainable code over hacky or magical code.**
   - Treat brittle, ad-hoc, or "magic" behavior as a code-quality problem.
   - Be skeptical of generic mechanisms that hide simple data-shape assumptions.
   - Forbid slim pass-through shims: a function whose body is a single call to the canonical function is banned, whether it forwards its arguments unchanged or supplies a fixed value for one of them. Call the canonical function directly at the use site and name the argument there. Several call sites passing the same constant is not a defect on its own and does not earn a wrapper to hold it; where the argument genuinely must not vary, encode that in the callee's own signature or type.

12. **Push hard on type and boundary cleanliness when they affect maintainability.**
   - Question unnecessary optionality, `unknown`, `any`, or cast-heavy code when a clearer type boundary could exist.
   - Every module-level declaration states its type. A constant is declared immutable and typed in
     the language's own form (`Final[T]` in Python, `as const` or an explicit type in TypeScript), a
     mapping names its key and value types, and a table, pattern, or handle built at import time is
     annotated like any other binding. An untyped module-level name is a finding on its own,
     whatever it holds and however obvious the value looks. Grep the diff for added module-level
     assignments without an annotation rather than hoping to notice them while reading.
   - Classify every added constant by whether operators, repositories, or releases may reasonably
     change it. Only true invariants stay module constants: a provider API root fixed by an external
     protocol may be invariant, while credentials, proposal substitutions, repository identities,
     workflow references, timeouts, deployment addresses, and other tunable values belong on the
     owning typed settings model even when they have safe defaults. Capitalization and `Final` do
     not make a configurable value invariant.
   - Every data-holding class lives in a model-owned file or package. Only a Pydantic `BaseSettings`
     class is configuration; registries, manifests, policies, provider payloads, and response
     schemas remain models.
   - Prefer explicit typed models or shared contracts over loosely-shaped ad-hoc objects.
   - If a branch relies on silent fallback to paper over an unclear invariant, ask whether the boundary should be made explicit instead.

13. **Keep logic in the canonical layer and reuse existing helpers.**
   - Call out feature logic leaking into shared paths or implementation details leaking through APIs.
   - Prefer existing canonical utilities/helpers over bespoke one-offs.
   - Push code toward the right package, service, or module instead of normalizing architectural drift.

14. **Treat unnecessary sequential orchestration and non-atomic updates as design smells when the cleaner structure is obvious.**
   - If independent work is serialized for no good reason, ask whether the flow should run in parallel instead.
   - If related updates can leave state half-applied, push for a more atomic structure.
   - Do not over-index on micro-optimizations, but do flag avoidable orchestration complexity that makes the implementation more brittle.

15. **Make code and tests carry behavior, not explanatory prose.**
   - Inspect every source comment and docstring encountered in the resolved scope. Exclude vendored
     and generated output owned by an external tool or source.
   - Treat a comment explaining repository-owned behavior, control flow, an invariant, or a design
     choice as a finding. Delete redundant narration; refactor logic that needs prose to be understood;
     and add or update a test when the prose states a behavioral guarantee.
   - Keep a comment only for externally owned behavior the code cannot make evident, such as a
     surprising third-party or protocol constraint. Make it factual and one physical line when
     possible, with two lines as the absolute maximum.
   - Keep every docstring to one physical line that identifies the symbol rather than narrating its
     implementation. Shorten a multiline docstring instead of moving its prose into a comment.
   - Grep the diff's added lines for a docstring opener that does not close on the same line, and
     report each one as a finding. Reading for structure does not surface a docstring that grew a
     second paragraph, and the paragraph is usually the rationale a test should carry instead. The
     report lists every docstring the diff adds with its line count; a report that declares the
     docstrings clean without that list has not run the check.
   - A docstring is the first statement of the module, class, function, or method it documents.
     Treat a standalone string literal between class fields or other members as an explanatory
     pseudo-docstring: remove it, refactor the surrounding model, or use the repository's canonical
     machine-consumed schema metadata when a tool genuinely requires that description.

16. **Hold every test module in scope to the repository's test layout, whatever its history.**
   - Count `class Test` per test module — added, renamed, or already there when the change arrived —
     and report every count above one as a finding in its own right, before any other observation
     about that module: the module becomes a folder named for the source file it mirrors, holding one
     module per class, and the finding names the folder and each module it would produce. Noting the
     count in passing and moving on is the miss this standard exists to catch.
   - Read the module-level statements of those modules the same way: a function, constant, or model
     beside the classes belongs in the suite's fixtures or utils package, and one that was there before
     the change is the same finding with an older date.

## Primary Review Questions

For every meaningful change, ask:

- Should this exist at all — what breaks if it is deleted outright?
- If this is generic, where else does the repository already do this job by hand?
- What did the extraction leave behind, and is that leftover now a pure forward?
- Does something we already depend on do this job already, better?
- Does this guarantee what its name claims, or noticeably less?
- Is there a "code judo" move that would make this dramatically simpler?
- Can this change be reframed so fewer concepts, branches, or helper layers are needed?
- Does this improve or worsen the local architecture?
- Did the diff add branching complexity where a better abstraction should exist?
- Did a previously cohesive module become more coupled, more stateful, or harder to scan?
- Is this logic living in the right file and layer?
- Is any file or component in scope past a healthy size boundary?
- Are there repeated conditionals that signal a missing model or missing helper?
- Is the implementation direct and legible, or does it rely on special cases and incidental control flow?
- Is this abstraction actually earning its keep, or is it just a wrapper?
- Does any function take one declared shape and only read it — a method that shape is missing — how many of them sit over that same shape, and can that declaration hold a method at all?
- Did the diff introduce casts, optionality, or ad-hoc object shapes that obscure the real invariant?
- Is this logic living in the canonical layer, or did the diff leak details across a boundary?
- Does the module's name say what it holds, and does it sit in the package that owns that concept — or is it filed under the feature that happens to call it?
- How many public symbols does each module in scope hold once its history is ignored — a rename
  or move that carried one symbol across is still one symbol — and do its siblings hold one each too?
- Does any new enum, constant set, mapping, or model re-declare a set the repository already has,
  and does every module-level declaration carry its type?
- Does this represent a value differently from how a sibling already represents the same thing — a bare string where an enum exists, a fresh constant where a canonical type is the established shape?
- Is this orchestration more sequential or less atomic than it needs to be?
- Does any docstring the diff adds run past one line?
- Does any test module in scope hold a second test class, or a helper beside its classes?

## What to Flag Aggressively

**Run four greps over the diff's added lines before reading for anything else, and report every hit
as a finding:**

1. A subscript whose key is a model, class or `type(...)` — `FORM_TYPES[record_model]`,
   `KINDS[type(record)]`, `LABELS[form_model].name`. Each hit is a reader reaching through a lookup
   table for a fact the key should declare on itself; the remedy is a class attribute or property on
   the key, every reader moved onto it, and the table deleted. The table predating the diff changes
   nothing: the added reader is the finding.
2. A string literal holding an email address, a street address, a legal entity name or the product
   name, anywhere outside one typed model in the package every consumer reads. Each hit is a repository-wide fact
   kept as a loose string inside one consumer; the remedy is the typed model in the shared package
   that every consumer reads.
3. A router constructor — `APIRouter(` or the framework's equivalent — followed by a count of the
   handlers registered on that router in the resulting tree. One handler is a container declared for
   one member, whether or not the diff added the router; the remedy is the handler moved onto the
   router that already owns its resource, at a path under that resource, and the router and its
   module deleted. A prefix ending in a verb or an operation is the same finding read from the URL.
4. A data-holding class declared outside a `models.py` file or `models/` package. Match added
   `BaseModel`, dataclass, named-tuple, and equivalent record declarations, then move each to a
   concept-specific model module. Only a Pydantic `BaseSettings` class is configuration and belongs
   in `config.py` or `config/`; registries, manifests, policies, provider payloads, and response
   schemas remain models. Never use operational code as the destination merely to avoid a
   one-symbol declarative module.

A report that declares the diff clean without listing these four greps and their hits has not run
them.

Escalate findings when you see:

- An addition that takes the shape the same diff's deletions remove — a name list restated where one
  was derived away, a second mechanism beside the one the change introduced, a flag reintroduced to
  carry a distinction the change moved onto a declaration.
- A complicated implementation where a cleaner reframing could delete whole categories of complexity.
- Refactors that move code around but fail to reduce the number of concepts a reader must hold in their head.
- A file over 1000 lines anywhere in scope, whatever put it there.
- Any suppression the diff adds — `pyright: ignore`, `type: ignore`, `noqa`, `pylint: disable`, a
  broadened `except`, a new linter-ignore entry, a lowered threshold, a hand-written stub — outside
  generated output. Grep for these; they do not surface from reading for structure.
- A test module holding two or more test classes, whatever put the second one there.
- A docstring the diff adds that runs past one line.
- A function, constant, or model defined in a test module beside its tests, whatever its size or
  caller count. Grep every test module the diff touches for module-level `def` and assignments;
  reading the tests does not surface them.
- New conditionals bolted onto unrelated code paths.
- One-off booleans, nullable modes, or flags that complicate existing control flow.
- Feature-specific logic leaking into general-purpose modules.
- Generic "magic" handling that hides simple structure and makes the code harder to reason about.
- Thin wrappers or identity abstractions that add indirection without simplifying anything.
- A function whose parameters are one shape the repository declares and whose body only reads it, and most of all a family of them over the same shape: that is the shape's method list spelled with the receiver passed by hand.
- A new abstraction that a platform, framework, runtime, or dependency already in the project was
  doing anyway — however cleanly it is written, and whether or not it duplicates anything in-repo.
- A guard whose real guarantee is weaker than its name: an in-process limit on a replicated service,
  a check another code path reaches around, a cap whose true ceiling multiplies by process count.
- Unnecessary casts, `any`, `unknown`, or optional params that muddy the real contract.
- Copy-pasted logic instead of extracted helpers.
- Narrow edge-case handling implemented in the middle of an already busy function.
- Refactors that technically pass tests but make the code less modular or less readable.
- "Temporary" branching that is likely to become permanent debt.
- Bespoke helpers where the codebase already has a canonical utility for the job.
- A generic helper with exactly one caller, especially one this diff just created by extraction. One caller is not proof a helper is unnecessary; it is usually proof the sweep stopped at the first site. Search for the rest by the operation it performs, not by its name, and either use it there or fold it back into its single caller.
- A new enum, constant set, mapping, or model whose members mirror one the repository already
  declares, however differently it is named and wherever it landed; the fix is a property, method,
  or widening on the existing declaration, filed where its consumers meet.
- A module-level constant, mapping, or handle declared without its type.
- A models module holding something other than a declaration. For every module under a `models/`
  package the diff touches, list its module-level assignments; each is `__all__`, a type alias or
  type variable, or a `Final` value that a class, function, or `Annotated[...]` in the same module
  reads, and anything else — a mapping or set nothing in the module reads, a registry, a sample
  instance, an options object, a logger — is reported with the module that owns its use, which is
  the module that reads it. When two modules read it, the owner is the one whose behaviour it
  configures — the plugin, the runner, the service — and the other imports it from there; a new
  module holding only the moved values is the same problem under a different directory name. A set
  of one enum's members is a classmethod on that enum. The enums and models in the same file stay;
  only the values move.
- A module with one public symbol — new, renamed, moved, or already in scope — and a package where
  several modules each hold one. The
  first is a file that has not earned its name; the second is one module split across several files.
  Count symbols per module rather than judging by line count.
- Two utilities performing one operation on different shapes, or with their own separate constants and sentinels for the same idea. Collapse them into one whose parameter covers both callers.
- A helper written narrowly for its first caller when a slightly wider contract would serve places that currently go without. Widening it is the fix; a second near-duplicate later is the cost of not doing it.
- Several hand-rolled call sites doing one job — four log lines each formatting a response their own way, three places assembling the same payload, two sentinels for one masked value. Count them by the job they do, not by how alike their code looks: the point of collapsing them is that a fix to one currently reaches none of the others.
- **That each variant does something slightly different is not a reason to keep it.** A differing field, level, or label is a parameter of the one helper, not a second helper. Fold the variations in as arguments and let every caller reach the whole behaviour; keep them apart only where merging would genuinely make one caller do something wrong, and say which caller and what.
- Logic added in the wrong layer/package when it should live somewhere more central.
- A module named for what it returns rather than the question it answers, or one sitting in a package that does not own its concept — a billing rule filed under the feature that consumes it.
- The same kind of value modelled two ways across siblings: a bare string or one-off constant on one path where a shared enum already covers it on another, especially for anything persisted or sent across a service boundary.
- Sequential async flow where obviously independent work could stay simpler and clearer with parallel execution.
- Partial-update logic that leaves state less atomic than necessary.
- A lookup table keyed by a model, class or table whose values are facts about the key — its wire
  type, its display label, its audit kind — when the key could declare the value on itself as a class
  attribute or property, and equally **a new reader that reaches through such a table** —
  `FORM_TYPES[model].label`, `KINDS[type(record)]` — for a fact the key already knows. The reader is
  the finding whether or not the diff added the table: the remedy is the declaration on the key, with
  every reader, this one first, moved onto it and the table deleted.
- A repository-wide fact — the company's legal name, its support address, its postal address, the
  product name — kept as loose strings inside one consumer, such as an email renderer or a document
  builder, instead of one typed model in the shared package that every consumer reads.

## Preferred Remedies

When you identify a code-quality problem, prefer suggestions like:

- Delete a whole layer of indirection rather than polishing it.
- Delete the abstraction outright and rely on the mechanism that already did its job.
- Fix what the tool is reporting, or leave the report standing — never silence it.
- Reframe the state model so conditionals disappear instead of getting centralized.
- Change the ownership boundary so the feature becomes a natural extension of an existing abstraction.
- Turn special-case logic into a simpler default flow with fewer exceptions.
- Extract a helper or pure function.
- Split a large file into smaller focused modules.
- Collapse one-symbol modules into one module named for what they share, widening the existing one.
- Move feature-specific logic behind a dedicated abstraction.
- Replace condition chains with a typed model or explicit dispatcher.
- Separate orchestration from business logic.
- Collapse duplicate branches into a single clearer flow.
- Delete wrappers that do not meaningfully clarify the API.
- Move a function that only reads one declared shape onto that shape, and give a declaration that cannot hold behavior a form that can.
- Reuse the existing canonical helper instead of introducing a near-duplicate.
- Apply a single-use utility at the other sites that need it, or inline it back into its one caller.
- Widen a narrow helper's contract so it covers the neighbouring cases, rather than leaving them unserved.
- Collapse repeated hand-rolled call sites into one helper, carrying their differences as arguments.
- Make type boundaries more explicit so the control flow gets simpler.
- Move the logic to the package/module/layer that already owns the concept.
- Parallelize independent work when that also simplifies the orchestration.
- Restructure related updates into a more atomic flow when partial state would be harder to reason about.

Do not be satisfied with "maybe rename this" feedback when the real issue is structural.
Do not be satisfied with a merely cleaner version of the same messy idea if there is a plausible path to a much simpler idea.

## Review Tone

Be direct, serious, and demanding about quality.
Do not be rude, but do not soften major maintainability issues into mild suggestions.
If the code is making the codebase messier, say so clearly.
If the implementation missed an opportunity for a dramatic simplification, say that clearly too.

Good phrases:

- `this file is past 1k lines. let's decompose it and move the pieces to the module that owns them.`
- `this adds another special-case branch into an already busy flow. can we move this behind its own abstraction?`
- `this works, but it makes the surrounding code more spaghetti. let's keep the behavior and restructure the implementation.`
- `this feels like feature logic leaking into a shared path. can we isolate it?`
- `this abstraction seems unnecessary. can we just keep the direct flow?`
- `why does this need a cast / optional here? can we make the boundary more explicit instead?`
- `this looks like a bespoke helper for something we already have elsewhere. can we reuse the canonical one?`
- `i think there's a code-judo move here that makes this much simpler. can we reframe this so these branches disappear?`
- `this refactor moves complexity around, but doesn't really delete it. is there a way to make the model itself simpler?`

## Approval Bar

Do not approve merely because behavior seems correct.
The bar for approval is:

- no clear structural regression
- no obvious missed opportunity to make the implementation dramatically simpler when such a path is visible
- no unjustified file-size explosion
- no obvious spaghetti-growth from special-case branching
- no obviously hacky or magical abstraction that makes the code harder to reason about
- no unnecessary wrapper/cast/optionality churn obscuring the real design
- no clear architecture-boundary leak, avoidable canonical-helper duplication, or unjustified
  parallel implementation across independent consumers
- no missed opportunity for an obvious decomposition that would materially improve maintainability

Treat these as presumptive blockers unless the author can justify them clearly:

- the PR adds, anywhere in its diff, the shape its own deletions remove
- the PR preserves a lot of incidental complexity when there is a plausible code-judo move that would delete it
- a file in scope is over 1000 lines and was not decomposed
- the PR silences a linter or type checker anywhere outside generated output
- the PR adds ad-hoc branching that makes an existing flow more tangled
- the PR solves a local problem by scattering feature checks across shared code
- the PR adds an unnecessary abstraction, wrapper, or cast-heavy contract that makes the design more indirect
- the PR leaves a function that only reads one declared shape, or a family of them, outside that shape
- the PR carries code written after the review — for a tool, a red check, or a reviewer — that never went through the rubric
- the PR adds an abstraction that was never needed, or one whose guarantee is weaker than its name claims
- the PR adds a module holding one public symbol, or a second one-symbol module beside an existing one,
  without a demonstrated dependency boundary or entry-point requirement
- the PR adds a declaration whose members mirror one the repository already declares, or a
  module-level constant without its type
- the PR duplicates an existing helper, repeats a cross-consumer mechanism, or puts logic in the wrong
  layer when there is a clear canonical home

If those conditions are not met, leave explicit, actionable feedback and push for a cleaner decomposition.
