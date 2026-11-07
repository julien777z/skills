# Code Simplify Rubric

The criteria the `code-simplify` pass applies. The skill's `SKILL.md` says how the pass runs; other
skills that borrow the rubric read this file.

## Scope

- **Judge the change and the code it must touch**: the diff, the consumers it has to update, and the
  existing code it should have reused. Read whole files and sibling modules to find owners and
  duplicates; reading a file does not make its unchanged code a target.
- **The intent wins.** Never recommend removing, narrowing or reshaping something the change's
  stated intent asks for, such as a cache, a retry or a guard the request names. Where it looks
  wrong, say so as a question beside the finding, never as the fix.
- **Outside the change:** a bug it meets is fixed when the fix is small (one focused fix in about two
  files or fewer) and deferred when larger. Non-bug cleanup outside the change is deferred, not
  fixed, unless the user has widened the task's scope, whose own limits then apply.
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
- an abstraction, interface or factory the change adds with a single implementation or caller, or
  one whose job something already in the project does (standards 1, 4 and 5);
- a file the change pushes past 1000 lines (standard 6);
- a lint or type suppression the change adds (standard 7).

Every other maintainability finding — placement, typing style, naming, module layout, a function
that could be a method, docstring length — is a `nit`. A bug a standard uncovers, such as a guard
that hides a real failure, keeps its bug severity.

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
   - **Reachability is judged where the change will land**: the branch it merges into and the open
     branches it ships with, in every repository the user controls. "Set outside this repository"
     leaves the question open until those are read.
2. **A new module whose concern an existing module already owns** merges into that owner, renamed
   first if its name is too narrow. A module holding one public symbol is the plainest case; several
   one-symbol modules of one shape are one module. Exempt: a shown dependency boundary, an entry
   point found by path, and a UI component module. Never move a data model into operational code to
   remove a small models module.
3. **A new declaration that names what the repository already declares** is a second copy. Search for
   a new enum, constant set, mapping or model by its members or keys, never by its name. When the two
   answer the same question, the new values become properties of the existing declaration.
4. **One mechanism, one implementation.** Before accepting a new helper, client or utility, search
   the whole repository for the same operation by what it does, not by its name. Two live
   implementations of one guard, check or transform is the defect, whichever came first; a different
   error type or input shape is drift, not a reason to keep both. Variants become parameters. A
   generic helper the change adds with one caller is either used at the other sites doing that job or
   folded back into its caller.
5. **No forwarding layers.** A function whose body is one call to another owned function, an
   interface or factory with one implementation, and the leftover a fresh extraction reduces to a
   forward are each deleted and their callers pointed at the real thing. An adapter stays only where
   a declared dependency boundary forbids either side from absorbing the mismatch.
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

## Five Greps

Run these over the diff's added lines before reading for anything else and list every hit. Each hit
takes its severity from **Severity**, so most are `nit`.

1. A subscript keyed by a model, class or `type(...)`, such as `LABELS[type(record)]`: the fact
   belongs on the key as an attribute or property, and the table goes.
2. A repository-wide fact — a contact address, legal or product name — as a loose string in one
   consumer: it moves to one typed model every consumer reads.
3. A router constructor with one handler registered on it: the handler moves to the router that
   owns its resource.
4. A data-holding class (`BaseModel`, dataclass, named tuple) declared outside a model-owned file or
   package. Only a settings class belongs in configuration.
5. A dict literal annotated with a `TypedDict`, or a bare dict passed where a signature names one:
   build it with the constructor.

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
rule is never a finding**, because the skill is the copy read when the task starts. Duplication
between two rules, two skills, or within one file stays a finding, and a skill and rule that
disagree are reconciled.
