# Code Simplify Rubric

The criteria the `code-simplify` pass applies. The skill's `SKILL.md` says how the pass runs; other
skills that borrow the rubric read this file.

Contents: **Scope**, **Severity**, **Reuse And Removal**, **Standards**, **Five Greps**, **Trace
Changed Flows**, **Remedies**, **Guidance Prose**.

## Scope

- **Judge the change and the code it must touch**: the diff, the consumers it has to update, and the
  existing code it should have reused. Read whole files and sibling modules to find owners and
  duplicates; reading a file does not make its unchanged code a target.
- **The intent wins.** Never recommend removing, narrowing or reshaping something the change's
  stated intent asks for, such as a cache, a retry or a guard the request names. Where it looks
  wrong, say so as a question beside the finding, never as the fix.
- **The change is the pull request's whole diff against its merge base**, whatever scope a pass or
  slice reviews: a finding in lines or files the pull request wrote is inside it, in an earlier
  commit, another slice or a file it moved, copied or recreated at a new path alike. Check a
  finding's place against the pull request's file list, never the reviewed delta or a move's label.
- **Outside the change:** a bug it meets is always fixed, where
  `scope-of-change`'s **Scope Follows The Defect, Not The Request** places it. Non-bug cleanup outside
  the change follows that skill's size budget for admission, placement and deferral.
- **Contracts.** Preserve what a consumer outside the user's control observes: public routes and
  their shapes, durable identifiers, persisted and wire formats. A contract whose every consumer the
  user controls may change, with every consumer updated in the same change, in any repository, never
  behind a pass-through or compatibility shim.
- **Tests are not a contract.** A finding is never declined because a test patches or imports the
  symbol; the tests move with the code.
- **Code written after the review is reviewed too.** An edit made to quiet a checker, turn a check
  green or answer a reviewer meets this rubric before it is pushed.

## Severity

Findings use this scale:

| Severity | Meaning |
| --- | --- |
| `blocker` | The intended case is wrong. |
| `should` | A real bug callers will hit, an unsafe input, or one of the maintainability findings below. |
| `nit` | Everything else. |

A maintainability finding is never `blocker`. It is at most `should`, and only when it is one of:

- a second copy of a helper or mechanism the repository already owns (standards 3 and 4);
- an added file doing work an existing file owns when the split serves no distinct boundary
  (standard 2);
- a fixed value wrapped in a callable for a repository-owned interface (standard 5);
- new code beside an existing helper or mechanism that would have done the job with one more
  parameter, condition or case (standard 4);
- an abstraction, interface or factory the change adds with a single implementation or caller, or
  one whose job something already in the project does (standards 1, 4 and 5);
- a parameter, option, prop, flag or branch the change adds for a condition no caller produces, or
  that every caller sets the same way (standard 1);
- a file the change pushes past 1000 lines (standard 6);
- a lint or type suppression the change adds (standard 7).

Every other maintainability finding — placement, typing style, naming, module layout, a function
that could be a method, docstring length — is a `nit`. A bug a standard uncovers, such as a guard
that hides a real failure, keeps its bug severity.

## Reuse And Removal

Every addition gets one receipt line, written in the task record before the edit and checked at
review against an independent search:

```text
<what it does> · searched: <terms, by effect and key operation> · found: <owner and path, or none> · <reuse | extend: <the parameter or condition added> | new: <why no owner fits>>
```

- **Search** the repository and its shared packages by what the addition does and by its key
  operation, never by the name it would be given or by filename; a read of the sibling modules
  alone cannot find the owner another package holds.
- **Reuse** calls the owner as it stands.
- **Extend** adds the one parameter, condition or case an owner lacks to do the job; a second
  helper beside that owner is standard 4's finding.
- **New** names what each candidate found cannot do; with none found, the search terms are the
  evidence. A receipt that names no search is no receipt.

Before deciding whether to create, split or rename a file, read the closest existing files and
their callers; a rename runs this check again.
Treat similar names or overlapping responsibilities as a warning to check those files first.
Record which existing file can own the addition and whether its current name describes the
combined responsibility. When its name covers only part of the resulting work, rename it for the
shared responsibility and update its callers. Handle any further consolidation under **Scope**.
Create a separate file only when the receipt names the distinct responsibility or boundary it
serves, such as a UI component, dependency boundary, or framework-required path. What the code
does decides it, never who calls it: admin-only, internal or one page's use is no boundary, so
`invoices.py` takes the staff listing it serves rather than a `staff_invoices.py` beside it. A file
past a length limit is first refactored shorter, then has one whole responsibility moved to an
existing owner, broadened and renamed if needed, and only as a last resort becomes a folder named
for the same responsibility, holding modules named for what each holds, such as `invoices/` with
`pricing.py` and `delivery.py`; a caller- or variant-named sibling file is never the answer. Files
a framework or the repository's layout requires, such as routes, migrations or one test class per
file, keep that layout. Report the candidates and why the file stands alone. Search within the
file kind the repository requires, such as a model module for a model declaration.

A workaround, or a design that changes a shared operation, guard, contract, subsystem, runtime
boundary or independent consumer, also writes all three fields below, in the task record or
verdict, before deciding. Each field asks only for the facts the change has:

- **Source.** For each existing piece the design calls or composes, cite its implementation and
  state what it does and where it fails. Where it checks a caller, name the accepted caller role or
  authorization guard and the object scope separately; where it selects fields, list its exact
  field or mask entries and what omission does; where it writes, state the commit boundary. If no
  candidate exists, name the search. Flag a material missing fact and state the strongest
  supported design.
- **Smallest change.** Name the concrete sequence or composition using existing primitives and
  what code goes away. If a new mechanism is required, name the invariant the smaller design
  breaks. For a guard around broad work, compare narrowing the callee with guarding it.
- **Proof.** Name an observable case for the intended result, and an unchanged resource where
  collateral work matters. Where the effect depends on stored state or a transaction, seed the
  prior state, check dependent results, and cover commit and rollback.

## Standards

1. **Should this exist at all?** Before asking whether new code duplicates something, ask what breaks
   if it is deleted. If nothing a platform, framework or dependency was not already doing, the
   finding is to delete it, however tidy it is.
   - State what it guarantees, not what its name claims: an in-process limit on a replicated
     service, or a check another path reaches around, protects less than it advertises.
   - **A guard for a state no writer can produce is dead code.** Read every writer of the value it
     tests and of what its path reads next. When they already exclude the state, or an earlier check
     on the path refuses the same inputs, delete the guard with its message and its tests. A check
     after a lock, a transaction start or an `await` is not a duplicate when the value can change in
     that window.
   - Where a writer can produce the state, the check is real and belongs on every sibling path that
     answers the same question.
   - **A parameter, option, prop, flag or branch for a condition nothing uses is dead code too.**
     Read every caller of what the change adds or widens. One that no caller sets, or that every
     caller sets the same way, is deleted with its branch and its one value inlined; "a later
     caller may need it" keeps nothing.
   - **Reachability is judged where the change will land**: the branch it merges into and the open
     branches it ships with, in every repository the user controls. "Set outside this repository"
     leaves the question open until those are read.
2. **A new module whose concern an existing module already owns** belongs there. Verify the
   placement receipt for each added file against its actual siblings under **Reuse And Removal**.
   A file holding one public symbol is a cue to check for a shared responsibility.
3. **A new declaration that names what the repository already declares** is a second copy. Search for
   a new enum, constant set, mapping or model by its members or keys, never by its name. When the two
   answer the same question, the new values become properties of the existing declaration.
4. **One mechanism, one implementation.** Before accepting a new helper, client or utility, search
   the whole repository for the same operation by what it does, not by its name. Two live
   implementations of one guard, check or transform is the defect, whichever came first; a different
   error type or input shape is drift, not a reason to keep both. Variants become parameters: new
   code beside an owner that needed one more condition or parameter is folded into that owner. A
   generic helper the change adds with one caller is either used at the other sites doing that job or
   folded back into its caller.
5. **No forwarding layers.** A function whose body is one call to another owned function, an
   interface or factory with one implementation, and the leftover a fresh extraction reduces to a
   forward are each deleted and their callers pointed at the real thing. An adapter stays only where
   a declared dependency boundary forbids either side from absorbing the mismatch.
   Treat a side-effect-free callable that ignores its input and returns a fixed value the same
   way. Use the data directly through the existing enum, constant or mapping. If an interface
   the repository owns requires a callable for fixed data, let it accept the value directly.
   A callable required by an external contract stays at that boundary.
6. **Files over 1000 lines.** A file the change pushes past 1000 lines is decomposed into the modules
   that own its concepts. One already over the line is outside the change and follows **Scope**.
7. **No new suppressions.** A `type: ignore`, `pyright: ignore`, `noqa`, lint disable, widened
   `except`, new ignore-list entry, lowered threshold, hand-written stub or a cast that only quiets a
   tool is a finding, in the author's edits and the pass's own. Fix what the tool reports about owned
   code. A report about a third-party package's own types is answered once in the tool's
   configuration for every package, never in code. Generated files are exempt.
8. **One thing one way.** Does the change build something in a second shape beside how the
   repository already builds it — a bare string where an enum exists, a helper, test or configuration
   entry written unlike its siblings — where no contract requires the difference? The remedy is the
   existing shape. A better shape is proposed to the user, never built beside the first; an existing
   shape a standing rule names a defect is repaired, not followed.
9. **Deletions read first.** An addition that takes the shape the same diff removes elsewhere — a
   restated list, a second mechanism, a reintroduced flag — is a finding.
10. **Configuration is required unless it has a safe default or its owner documents an absence.** A
   settings field, environment variable, secret, config key or workflow input the change adds or
   reads as optional, with a default that is not safe or a branch that skips or weakens its work
   when it is unset, is a `should` finding under `engineering-conventions`' **Configuration** convention: a
   deployment that misses it runs without what it provides. Local runs or tests lacking the value
   are not such a documented absence. The remedy makes it required and deletes the absence branch.

## Five Greps

Run these over the diff's added lines before reading for anything else and list every hit, since a
fix written after review takes these shapes most easily. Each hit takes its severity from
**Severity**, so most are `nit`. A report with no hit for any of the five says so in those words.

1. **A reader reaching through a table keyed by a model, class or type for a fact about the key** —
   the pattern `[A-Z_]+\[` followed by a model, record, class, `type(` or `cls` expression, such as
   `LABELS[type(record)]` or `FORM_TYPES[model].label`. Each hit counts whether or not the diff added
   the table: the value belongs on the key as a class attribute or property, every reader moves onto
   it, and the table goes.
2. **A repository-wide fact held as a loose string** — an email or street address, a legal entity
   or product name in a string literal outside one typed model in the package every consumer reads:
   it moves onto that model.
3. **A container declared for one member** — a router constructor, such as `APIRouter(`, in an
   added line, with a count of the handlers registered on that router in the resulting tree. One
   handler is a hit whether or not the diff added the router: the handler moves onto the router that
   already owns its resource, at a path under that resource, and the router and its module go. A
   prefix ending in a verb or an operation is the same hit read from the URL.
4. **A data-holding class declared outside model ownership** — every added `BaseModel`, dataclass,
   named tuple or equivalent record declared outside a `models.py` file or `models/` package. It
   moves to a concept-specific model module. Only a settings class, such as a Pydantic
   `BaseSettings`, is configuration and belongs in `config.py` or `config/`; registries, manifests,
   policies, provider payloads and response schemas remain models. A model never moves into
   operational code merely to remove a one-symbol declarative module.
5. **A typed parameter built as a dict** — an annotation on a dict literal, such as
   `name: SomeTypedDict = {` or `params: sdk.params.X = {`, or a bare dict passed where an SDK or
   repository signature names a `TypedDict`, at any nesting level. Each hit is rewritten as the
   constructor call, such as `sdk.params.X(...)`, with tests asserting the same way.

## Trace Changed Flows

For a changed operation, follow its path through construction, mutation, persistence and reporting
far enough to name the existing operation that could own the same work, and any intermediate field
or return value no live consumer reads, which is deleted. Name the **affected-repository map** in
one line: the repositories that may share the operation, contract or a parallel implementation, and
what was done with each (consolidated, updated as a consumer, or excluded with the concrete
difference). A map listing only the current repository states the search that found no other.

## Remedies

- Prefer deleting a layer, a branch or an abstraction over rearranging it.
- A remedy follows the language and layout rules for the file it writes; check it before
  proposing it.
- A remedy that undoes one an earlier review prescribed for the same code names that remedy and the
  evidence it was wrong.

## Guidance Prose

The rubric applies to `.agents` rules and skills too, with one exception: **a skill restating a
rule is never a finding**, because the skill is the copy read when the task starts, apart from a
repository's own skill restating a shared skill or rule. Duplication
between two rules, two skills, two files of one skill, or within one file stays a finding, and a
skill and rule that disagree are reconciled.
