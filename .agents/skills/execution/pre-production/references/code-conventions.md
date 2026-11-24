# Code Conventions

What every line a change writes follows: code, configuration, manifests, documentation, comments,
commit messages and pull-request text. `SKILL.md` names this file at the point a change is written.

## Whose Standards Apply

- **The owner's standards govern the owner's repositories.** A repository is the owner's when it
  lives under their own account or an organization they run; any other, such as a project they
  open a pull request to, is someone else's. There a change carries what the request asks for and
  the defects it meets — a bug, a vulnerability, behavior that breaks for that project's users —
  written in that repository's own conventions. The style, structure, naming, testing, tooling, CI,
  runtime and documentation standards these rules and skills set, and this skill's incidental
  cleanup, are not applied there: an item only they would raise is left out, neither fixed nor
  recorded as deferred work in that repository, and named to the user in chat only when it bears on
  the request. The rules on how the agent acts hold in every repository: authorization, merging,
  posting, the publishing context, secrets and reporting.
- Every repository stands on its own. Never carry another repository's domain vocabulary into this
  one: its product name, its services, its table and column names, its record types, or the nouns
  its business speaks in. That holds for source, tests, fixtures, examples, and documentation
  alike, and it holds most strongly in a library, where every reader is a different consumer.
- Name implementation symbols, comments, docstrings, model descriptions, logs, technical
  documentation, and test examples for their behavior or domain. A product rename should require
  edits only at the sources of branding and documented integration or deployment contracts.
  Read the product name from its company or branding configuration when runtime text needs it,
  including metadata, accessibility labels, emails, and test expectations for that text. Keep
  literal names in their canonical sources, branded assets, company information and legal
  documents. Preserve existing package, protocol, database, and deployed resource identifiers
  when they are part of a compatibility contract.
- A library owns the vocabulary of the protocol or provider it wraps. That protocol's field names
  and naming conventions, such as how it spells an event type or a scope, are the library's own,
  never a consumer's domain vocabulary: a helper encoding such a convention belongs in the library
  even when one consumer prompted it, and the library's owned API gains it. This holds at the
  wrapper's layer; an application modeling the provider's data keeps its own field names, as this
  skill's **Adapting is not imitating** says.
- Identify environments by their full domain name throughout code, configuration, documentation,
  and user-facing labels, including enum and constant names. Code identifiers may encode the whole
  domain with separators, such as `garden.example` becoming `GARDEN_EXAMPLE`. Never drop the domain
  suffix, substitute a bare apex or product label, or append owner or organization aliases. Use
  the exact domain name for an environment's tailnet too. A name for anything else — a repository
  or service ID, a provider account, a project, a product, company or service name and its visual
  mark — keeps its own terminology, even when it shares an apex label with an environment.

## Code Layout

- In every language, use blank lines to separate setup, validation, transformations, side effects, and returns. Keep adjacent statements together only when they form one small operation; do not turn a function into an uninterrupted paragraph merely because a formatter permits it. Apply this to every line you write or edit, and elsewhere in a file you change within this skill's incidental size budget.
- Use current language syntax for simple operations. For one-off Python interpolation, use f-strings instead of string concatenation or `.format()`, and keep spacing in the final string rather than a fragment with a hidden leading space. Follow the Python rule for reusable structured templates.

```python
# Good: each phase is visible.
records = load_records()

if not records:
    return []

normalized = [normalize(record) for record in records]

save_records(normalized)

return normalized

# Bad: unrelated phases run together.
records = load_records()
if not records:
    return []
normalized = [normalize(record) for record in records]
save_records(normalized)
return normalized
```

- **A new file is the last resort.** Before creating one, find the existing file that already owns
  the concern, or an existing file a broader name would make its owner, and put the code there,
  renaming that file and updating every reference when the broader name is needed. Create a file
  only when neither exists, and name the candidates checked in the report. Code the change already
  wrote into a new file is moved the same way. Where another rule decides the kind of file, such as
  models in a models module, that rule picks the kind and this search runs within it; a file a rule
  or tool requires to stand alone — a component module, a migration revision, a page or workflow
  found by its path — is not this case.

- **The repository does one thing one way.** Before writing anything of a kind it already holds —
  a router, a client, a helper, a test, a fixture, a configuration entry, the way it raises and
  reports errors — read how the existing instances are written and follow that shape. A new pattern
  beside the old one reads as bespoke however good it is, and a reviewer meeting it has to learn two
  ways to do the same thing. **A better shape is proposed, never swept in.** Where a different shape
  would serve better — more standard, simpler, less code — the change keeps the existing shape and
  the conversion goes to the user as a proposal: the shape, why it is better, every instance it
  would convert and the size of that change, with a recommendation. It is built only once the user
  approves it and at the scope they approve, as its own work rather than under this skill's size
  budget, and never left half done; a sweep built unasked costs its whole size again when the
  user rejects it. An existing shape a standing rule names a defect is not followed; it is repaired
  on every instance as this skill's **Scope Follows The Defect, Not The Request** says. Only a difference a
  contract the instance serves requires stays, with that contract named in the report.

- A bootstrap or setup folder holds its entrypoint and, when needed, its configuration file at
  its root. Supporting scripts, modules, and data files go in its `resources/` folder; configuration
  stays beside the entrypoint rather than among those helpers.

- Executable scripts and command entrypoints are consumers, never reusable data or helper owners.
  Application code, test setup, and other commands must import shared behavior from its existing
  application, utility, test-support, or bootstrap-resource owner, not from an executable module.
  Move reusable definitions and all their consumers to that owner; keep command orchestration in
  the entrypoint. A test may import a command to exercise that command itself, but not to obtain
  unrelated setup or sample data. Classify the module by its role, not merely its directory name.

- **Every prompt an application gives a model is its own Markdown file in its prompts folder, which
  code loads and fills, never text in code**: a template, MCP server instructions, an agent definition it loads.

## Configuration

- **A configuration value is required unless it has a safe default or its owner documents a
  supported absence.**
  Configuration is every value a deployment, environment or operator supplies: an environment
  variable, a settings field, a secret, a key in a config file or deployment manifest, a workflow
  input. A value the code needs takes a default only when that default is safe, meaning a
  production deployment running on it gets the full behavior the value exists for; otherwise it has
  no default, and loading configuration without it fails at startup or deploy, naming the value. A
  deployment that forgot it then stops, rather than running without what it provides.
- **None of these makes absence a supported mode**: the value is new; local runs, tests or a
  development environment have no use for it, or already behave correctly without it; credentials
  for it are not yet available; a mock value exists. Those setups set the value in their own
  configuration, such as the example environment file, the test settings or the local stack, with a
  synthetic value where the real one is a secret.
- **A supported absence is a contract its owner documents**, such as ambient credentials a platform
  provides, and the configuration owner declares and enforces it. No consumer checks whether a value
  is set, and no code path falls back to weaker behavior when one is unset: a webhook check that
  passes every request when its verification key is missing, or a rate limit that switches off
  without its store address, is the defect even where the declaration reads as required.
- The technology rules say how each settings owner declares a required value.

## Logging

- **Error messages and tracebacks are never censored, in any environment.** A failure is debugged
  from its log, so a record reporting one keeps the exception's type and message, its notes and its
  whole traceback, and a warning or error keeps the values it was given. A disclosure policy conceals
  only typed secrets and credentials, such as a key or a URL's password and query string. It never
  replaces a failure's text with a placeholder, renders an exception as its type or its message
  alone, leaves a provider's error response out of the record, or redacts a warning or error
  wholesale because it might hold personal data. Records that report no failure may still withhold
  personal data.

- An agent's authorized access to a credential is not credential exposure. Seeing a credential in a
  prompt, private configuration, tool input or output, or the agent's own execution history never
  establishes compromise and never warrants revocation by itself. Treat a credential as exposed
  only when evidence shows that it reached an unauthorized recipient, a public surface, or a
  compromised destination. Preserve secret-safe handling; do not surface values unnecessarily.

## Versions

- Reference external code and automation by a maintained version tag when available, or by a
  maintained branch while developing or when no release tag exists. Do not pin dependency manifests,
  shared checkouts, or workflow references to commit hashes. Lockfiles and release records may retain
  the exact resolved commit for reproducibility and provenance.

- **Every project the owner runs or consumes runs the newest stable language runtime, base image
  and dependency releases it works with.** A change made for that move — one the user asks for, or
  the upgrade pull request a warning leads to, as this skill's **Scope Follows The Defect, Not The
  Request** places it — moves what the project actually runs onto them: its version file,
  container images, CI and lockfile, with whatever code changes the new releases need, including in
  an owned package that only widened its range to let a consumer move. Neither of these is that
  move: a CI leg kept on the old release beside the new one, or a dependency held below its newest
  release. A change that touches a manifest or lockfile for another purpose, such as adding one
  dependency, takes that dependency's newest stable release and moves nothing else. Hold one back only
  where an install or test shows the newer release failing on the project's runtime, such as
  another dependency pinning it, and name that failure in a comment beside the constraint; a
  migration the newer release needs is part of the move, not a reason to hold. Widening a
  supported range to admit a newer release is fine, since an owned project's range serves the
  owner's own projects. Raise its minimum once keeping the lower release no longer makes sense,
  such as when the formatter or the code would stay on the older release's syntax. A library
  published for consumers outside the owner's projects keeps the range its language rule sets.

## Naming And Language

- **Name things with the everyday word a reader expects.** The reader is this codebase's: a name
  says what its product, its users and its existing code call the thing, never a word that is right
  only in another field, such as a botanical Latin name for a plant in a garden shop's catalog.
  Where the domain or a provider has a term this codebase's readers use, use it. A parcel the
  carrier reports as delivered is `delivered`, never `parcel_arrived`, because an unusual synonym
  makes every reader translate it back. This covers identifiers, fields, messages, documentation and
  test names in every language.
- **Everything an agent writes is in American English, in spelling and vocabulary alike**: code and
  its identifiers, comments, documentation, guidance, records, commit messages, pull-request text,
  product copy, generated content and every reply the user reads. It writes `color`, `behavior`,
  `center`, `catalog`, `canceled` and `organize`, and a "cell phone" rather than a "mobile". A
  reader meeting the other form reads it as a mistake, and a product using both reads as two
  products. Two kinds of text keep their own form: a quotation reproduced verbatim from its source,
  such as an on-screen message, and a name a language, framework, protocol or provider defines, such
  as an HTML attribute.
- **A name says what it is about, so a reader never opens the body to learn what it acts on or
  holds.** That holds for every name: a function, Boolean, field, event, constant, class, module,
  file or package. A name built on a verb names the verb's object: `job.writes_files`,
  `assert_may_book_rooms`, never `writes(job)` or `assert_may_book`, whose reader asks "writes
  what?", "book what?". A receiver or argument supplies the subject only when it is the very thing
  the name is about: `loan.is_overdue` and `is_deliverable(message)` need nothing more, but a check
  on whether a member may change a club's bookings takes the club and is about its bookings, so it is
  `may_change_bookings(member, club)`, never `may_change(member, club)`. A generic noun says what it
  holds unless its receiver already does: `shipment.status` is the shipment's own state, but the
  state of its customs check is `customs_status`; a parsed recipe in a local variable is `recipe`,
  never `result` or `data`; a constant is `MAX_GUESTS_PER_TABLE`, never `LIMIT`; and a module of
  date helpers is `dates.py`, never `helpers.py` or `misc.py`. The one generic container name is
  the category package a language rule assigns, such as `utils/`, whose topic-named modules carry
  what it holds. A name a framework or protocol defines keeps its own spelling.
- Name things for the shape being exercised, not for whichever caller happened to prompt the work.
  A test needing a table with a secret column names it for that — a record with a secret — rather
  than borrowing the one real table the change was made for.

## Examples And Paths

- **An example the user gives is never reproduced.** A value the user quotes or shows to illustrate
  a case — a name, an address, an amount, an identifier, a message, a record read from their data, a
  capture or a log — appears in nothing the agent writes, such as source, tests, fixtures, comments,
  documentation, guidance, records, commit messages, branch names, pull-request and issue text,
  posts, worker briefs, and the reports and questions the user reads. Each place uses a newly
  invented, plainly synthetic value that keeps only the trait the case turns on, such as a hyphen, a
  long value or an accented letter: a reported plant code `FERN-EXAMPLE-0042` becomes
  `PLANT-SAMPLE-0001`, and a reported total of `$9,876.54` becomes `$1,000.50`.
  Outside the bullets below, it is swapped at the **first retelling** later work copies from: the
  plan, ledger entry or brief. A value derived from it, such as its digits reordered, is the user's.
  - A quote of the user's words that holds such a value — an intent statement, a recorded answer, a
    handoff, a dashboard — keeps the rest of their words exactly and names the value by its kind in
    brackets, such as `[the reported plant code]`.
  - A value naming the record or account the work operates on, or one the code must match, appears
    only where the work acts on it — a query, a command, a brief that sends a worker to it, the code
    or configuration that matches it — and tests, comments, descriptions and other committed,
    posted or published text use an invented one.
  - Two kinds of value are not examples and keep their exact text: fixed text the product shows
    every reader that the user asks to add or reword, such as a label, never a value shown from a
    record; and a literal a protocol or provider defines for every caller, such as a status value.
  - Every other sample value is synthetic too, never shaped like another system's real identifier.
- **Nothing committed to a repository or posted to its host holds a path that only one machine
  has.** Source, configuration, guidance, documentation, fixtures, captured tool output, commit
  messages, pull-request text and comments never name a home directory, a temporary or scratch
  directory, the place a checkout sits, or a drive letter, such as
  `/home/<name>/work/garden/tools/build.py` or `D:\exports\stock.csv`. A file in the repository is
  named by its path from the repository root; a location that differs between machines is read from
  configuration or an environment variable; captured output is trimmed to repository-relative paths
  before it is committed or posted; and a file outside the repository is named for what it is and
  how a reader obtains it, such as "the CSV the stock report's Export button downloads".

## Documentation

- **Every document holds only what its reader needs for its purpose.** A README, project guidance, a
  skill, a rule, a design document, a pull request description, a code comment: each has one reader
  and one job, and content goes to the document whose reader acts on it: an operator's runbook in a
  README, an incident timeline in a skill, and a design specification in a code comment are each
  content in the wrong document. A change adds to a document only what alters that document's
  reader's work; being nearby, or already covering the area, is no reason.
- Documentation, code comments and docstrings describe current behavior only; Git history is the
  record of what changed. Never describe what a symbol used to do, what was removed, renamed, or
  deprecated, and never write migration tables, upgrade notes, or "formerly", "replaces", or "kept
  for backwards compatibility" notes.
- **Behavior another party owns is explained once**, beside the value or line where the code first
  handles it. Every other place that reuses that value or works around the same behavior restates
  nothing: a second comment, a docstring, or a comment in another file. A comment above a timeout
  saying a library sets none, and another at the override that applies it, are one comment too many.

## Repository Text

- Write repository artifact text for its reader: describe behavior, configuration, contracts and
  validation, without narrating the task that produced it. This includes action and workflow
  metadata, configuration descriptions, code comments, documentation, commit messages and
  pull-request text. Do not add attribution to user requests, approvals or agent compliance, such
  as “as requested” or “per your instructions”; apply the instruction to the result itself.
  Record an exchange only when the user explicitly asks to document that exchange, in a document
  whose purpose is that record.
- **A description of an input, output, option, setting or field tells a person what the value is,
  in a plain sentence**, such as "Commit the changes are compared against". It never restates the
  flag or variable the value becomes, such as `--base-sha`, stands a bare value grammar such as
  `a | b` in place of words, or lists which operation, command or caller uses it, such as
  `(generate only)`: the code already shows how the value is passed and who reads it, and a list of
  users goes stale with the next change to the code. Where a value is one of a fixed set, the
  sentence says what each one does.
- Use conventional commit messages when applicable and keep commits atomic and focused.
- Name what a branch, commit or pull request changes by its category of change, in generic nouns
  such as page, request or button. A branch takes the repository's required prefix and a slug of
  that description. Leave branch names and pull-request metadata that automation owns unchanged.
- Keep pull requests focused and give them descriptive titles and descriptions: a title stays short,
  and a body may run long with bullets and validation notes. Request appropriate reviewers when the
  repository workflow requires them.
- **A pull-request description is written from what is already known, never by re-reading the
  history.** The agent that did or coordinated the work writes it from its own record of the
  change, the existing description, `git log --oneline` subjects and `git diff --stat` against the
  base. It opens a commit or a file only to settle one line those leave unclear, and never walks
  commits one by one; a worker asked to write one is handed that change list in its brief.
- A pull-request description covers the changes in that pull request and nothing else. Leave out
  alternatives considered and rejected, work deferred to a later change, and the reasoning behind
  not doing something.
