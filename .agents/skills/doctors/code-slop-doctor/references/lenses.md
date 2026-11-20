# Code Slop Doctor Lenses

Each lens states what it flags, the checks that find every instance, the remedy, and what is left
alone. `SKILL.md`'s **Lenses** table says which lenses a partition reviewer reports and which the
cross-cutting reviewer owns. A check that names a pre-pass list reads the candidates `SKILL.md`'s
**Pre-Pass** produced: the reviewer confirms or rejects each one against the code and enumerates
nothing a list already holds.

Lenses, in order: Behavior Kept (the condition every rewrite meets), Pass-Through Layer,
Speculative Abstraction, Duplicate Implementation, Fragmented Use Case, Divergent Siblings,
Scattered Structure, Repeated Literal, Hand-Written Styling, Reads As Slop, Tolerated Past,
Migration Chain, Build And Root, Configuration Drift, Dependency Drift, Test Slop.

## Behavior Kept

**A lens that removes or rewrites executable code names a covering check before the edit.** The
check exercises the code and passes on the tree as it stands: an existing test, the type check
over the callers, or a build that compiles and loads the code. Where nothing reaches the code, the
worker writes the test first under `test-fixture`, in a repository that keeps tests; in one that
keeps none, the check is the type check or build together with a temporary, untracked run of the
code taken before and after. The same check runs after the edit, and the finding's proving check
records both results. A removal the lens proved unreachable — a symbol with no consumer, an arm no
writer produces — records that proof, the consumer count or the writers read, beside the check.

## Pass-Through Layer

A layer, wrapper or alias that only hands the call on.

- the pre-pass's one-call wrapper list: every function, method, component or hook whose body is
  one call that receives the caller's own parameters, unchanged or renamed, or with fixed or
  defaulted values added, and adds no policy of its own — callers could make that call with what
  they already hold. Rendering one other component is that call: a component passing on its props
  with some look or behavior props fixed or defaulted, and no content, data or state of its own, is
  a finding;
- every component that only runs a hook and renders nothing or its children;
- every chain of components each rendering the next with one more prop or value, counted end to end
  from the call site to the primitive at its end and reported as one finding with every link;
- every module layer — a service over a gateway, a lib under a route, a hook over one library call —
  whose members all forward to the next layer down;
- every barrel and re-export: count live imports through each path, tests separately; two live paths
  to one symbol, or a path whose only importers are tests, is a finding;
- every second name bound to one value, and every route, field or parameter accepted under two
  spellings.

The remedy is that callers call the target, the layer and alias go, and every importer moves in the
same change. A wrapper component's fixed values become a variant or prop on the component it
renders, as the general React rule's **Components and Props** says, a chain collapses into one component
with variants, and a hook-only component becomes the hook its callers call. Left alone: a wrapper
that adds policy, which is only validation, error mapping, retries, authorization, caching or
translation at a provider boundary — a fixed or defaulted value, a hook call, a class or a renamed
prop is never policy; a function that names a domain operation by mapping a domain value onto the
call below it; one external name per field at a provider boundary; the explicit public-surface
re-export a language defines for a package, in a short list; a component that carries the
`"use client"` boundary for a Server Component call site, as the general React rule's **Components and
Props** says; and a file the framework looks up by path.

## Speculative Abstraction

Structure built for cases that never arrived.

- the pre-pass's single-implementation list: every interface, Protocol or abstract base with one
  implementation, used by one consumer, and never substituted in a test through its declared seam;
- every base class with one subclass, every generic with one instantiation, every factory or
  registry with one product;
- every parameter, option, flag or prop no caller sets or every caller sets the same way;
- every context, provider or store read by one consumer, and every value threaded through layers
  that never read it.

The remedy is the concrete thing: the implementation in place of the interface, the subclass folded
into its base, the factory replaced by the constructor, the option replaced by its one value, the
store replaced by local state or a prop. Left alone: an interface the application declares as a
test seam and tests use; a plugin point a configuration file or an external consumer fills; and a
configuration field a deployment supplies, which **Configuration Drift** owns.

## Duplicate Implementation

One question answered twice.

- every implementation-only data declaration — one that crosses no serialized or stored boundary —
  whose field set matches another's, or is a subset carried by hand rather than derived; every
  hand-written type that mirrors a generated contract type;
- every hand-written validation — a model validator, a manual check, a parse function — that the
  validation library's own tools express: a constrained or annotated type, a field validator, a
  reusable annotated alias, a type adapter, a computed field, a discriminated union;
- the symbol index read whole: the same operation under another name, in another package or in
  another language — a formatter, a parser, a derivation, a guard, a client construction, a cache
  key — matched by signature and first docstring line, then confirmed by reading both bodies;
- every pair of enums or literal unions with overlapping members and a bridge between them, and
  every declaration `code-simplify`'s **A new declaration that names what the repository already
  declares** standard calls a second copy, searched by members and keys;
- the pre-pass's duplication-detector pairs, read pair by pair rather than repeated.

The remedy is one owner, placed by `code-simplify`'s ownership analysis — the shared package every
consumer reads where more than one deployable needs it — with the copies and the bridge deleted and
generated types used directly or derived from. Left alone: a generated mirror; a demonstrated
dependency, domain or contract boundary; two contract models, and copied blocks inside test trees,
each of which another doctor owns.

## Fragmented Use Case

One use case paying for many calls to operations the repository owns, or for work nothing bounds.
The unit is the use case, not the endpoint: read each candidate row of the use-case table, never
the list of operations alone.

- every use case calling several owned operations it always needs together — one page's load, one
  handler serving one request;
- every call made once per item — per row, per record, per identifier — inside a loop, a list render
  or a fan-out, where one operation could take the set;
- every chain of calls each waiting for the one before although none reads another's result;
- every owned operation whose callers all pass its result straight to another owned operation;
- static data the client can carry in its build — a published reference list, an owned enum and
  its labels — fetched at run time;
- every list read that returns a collection with no bound, and every producer-side helper that
  drains every page for its caller, as `pre-production`'s **Slow, unbounded or fragile work is a
  defect too** and the FastAPI rules' **Pagination** say.

The remedy is the operation shaped for its use case: one owned operation returning what that use
case always needs together, assembled server-side from the existing queries and concurrently where
they are independent; a batch operation taking the set in place of the per-item call; independent
calls that stay separate issued together rather than in turn; static data shipped with the client
through its package or generated contract; a bounded, paginated read in place of the unbounded one,
with the fetch-all helper deleted and each consumer that needs every page looping at its own call
site; every caller moved, and each operation left with no caller deleted with its client. A batch
or merged operation authorizes each item and each returned field as the operations it replaces did;
where it cannot, those operations stay separate, as Left alone says. The use case is timed before
and after on the same stack, and a merge that makes it wait longer for its first useful content is
not the remedy. Two cases go to the user for approval, never merged or left alone silently: an
operation another use case also calls on its own, where the use case may gain a merged operation
while the other keeps its own; and a read only some runs of the use case need, which a merged
operation may still carry. Each request lets the user decide without opening the code: the
operations it would combine, by method and path or RPC name; the proposed operation's method, path,
parameters and response fields; every other caller of each of those operations, found in the code
by page, job or service, with what it reads and whether it already shares the use case's read; what
would become of each existing operation, kept for which caller or deleted; the current counts and
timings, and the call count the proposed operation would leave; and the run's recommendation. The
timings after are measured once the merge is approved and made. Left alone: a call a later
interaction makes — a tab opened, a page turned, a row expanded; reads under different
authorization or caching that one response cannot carry, and any set of items one operation cannot
authorize as the per-item calls did; a slow section kept apart so it does not hold a fast one, with
the timing showing it; a third-party provider's operations, batched only where the provider offers
it; and the one complete read of its own collection the FastAPI rules' **Pagination** allows a
domain service.

## Divergent Siblings

Things of one kind built in different shapes.

- read each kind's slot table: a slot one deployable fills with a shared helper and another fills
  by hand, a slot filled differently in each, and a slot one fills and its siblings leave empty with
  no contract difference to explain it, are each a finding;
- sibling routes, pages and features: one data-fetching style, one folder layout, one way to
  submit, load and report errors per kind; a feature split across several places its siblings keep
  in one is a finding;
- every kind the repository builds more than once — routers, clients, helpers, configuration
  entries, the way an error is raised and reported — listed with the shape each instance takes: an
  instance built unlike the majority, with no contract requiring the difference, is the finding
  `code-simplify`'s **One thing one way** standard names;
- every service's responses and every client's error handling read against the `http.md` rule: a
  status outside the set that rule allows, a table mapping a provider's statuses onto messages of
  the repository's own, and a timeout or retry override on an official SDK with no stated reason;
- copies of one module in two places that have drifted apart — providers, clients, configuration —
  compared line by line.

The remedy is one structure per kind: the shared shape lives in the shared package and each sibling
supplies only what differs, its name, port, servicers or routes. The slot's best existing
implementation becomes the shared one under `code-simplify`'s rubric **Standards**; the minority
instance of a kind takes the shape the majority already has, and a shape better than every existing
one goes to the user as `pre-production`'s **The repository does one thing one way** says.
Left alone: a slot or instance whose difference a contract requires, with the contract named.

## Scattered Structure

Code spread over more files and folders than its responsibilities need, or held in the wrong kind
of file.

- every module with one or two small public symbols whose siblings would hold them;
- every module, whatever its count, that the `code-simplify` rubric's **A new module whose concern an existing module already owns**
  standard merges into an existing owner, or into one a broader name would make its owner;
- every pair of modules or folders answering the same question, and every concern split across
  several folders;
- every catch-all module mixing unrelated owners, and every `lib`/`utils`-style pair with no rule
  for what goes where;
- every file or folder whose name says something other than what it holds;
- the module table's files past the size `code-simplify`'s **Files over 1000 lines** standard sets;
- each of `code-simplify`'s **Five Greps**, run over every tree in the area rather than a diff's
  added lines, every hit listed;
- the import graph's edges into an executable: every application module, test-support module or
  command that imports from a script or command entrypoint, and every import that runs against the
  layering the repository's language rules set;
- every prompt an application gives a model that is held as text in code — a template, a server's
  instructions, an agent definition — found by reading each model-client call's arguments back to
  where their text is declared, as `pre-production`'s **Code Layout** conventions place it;
- every declaration list ordered by when its entries were added rather than by what they describe
  — the fields of a message or model, an enum's members, a configuration's keys — so one concept's
  entries sit apart, and every owned wire contract whose field numbers record that history.

The remedy is restructuring, done without hesitation: merge modules of similar scope into one,
collapse one-symbol modules into their owner, split a catch-all by owner and an oversized file into
the modules that own its concepts, move code to where its consumers expect it, move a helper out of
an executable to its application, utility or test-support owner with every consumer, move each
prompt into its own file in the application's prompts folder, which the code loads and fills,
rename files and folders for what they hold, and regroup each declaration list by concept,
renumbering an owned wire contract's fields to match — every importer, producer and consumer
updated and every generated target regenerated in the same change, no re-export left behind. A UI
area folder is judged by these checks once **Pass-Through Layer**'s wrappers in it have become
variants on their owners. Left alone: a module boundary a framework prescribes, a package boundary
a build or distribution artifact needs, the one-component-per-file split the general React rule requires
for the components that remain, a test importing a command to exercise that command, and a wrapper
component, which **Pass-Through Layer** owns.

## Repeated Literal

One meaning spelled out many times, or a literal that belongs to one machine.

- count every class-name or style string literal across the components in scope — extract each
  `className`, `class`, style-token or `cn(...)` argument string and tally identical values — and
  report every value that appears in three or more places with its count and locations, outside
  an app built on a shared UI library, whose class strings **Hand-Written Styling** owns and fixes
  as variants;
- every error-to-message conversion written inline beside a helper that does it; every port, host or
  URL declared in more than one place; every message template spelled out at more than one site;
  every list restating an enum's members;
- every constant restating a token the theme or framework declares — a breakpoint width, a color, a
  spacing step, a layer order — in script or in a second stylesheet;
- the pre-pass's one-machine path list in source, configuration and fixtures, every environment
  named in code without its full domain, and every sample value shaped like a real identifier from
  another system, as `pre-production`'s **Examples And Paths** and **Whose Standards Apply** say.

The remedy is one owned definition — a component or style token, the existing helper, one
configuration source, the enum itself — and every site reading it; a restated theme token is read
from the theme, through one shared hook where script needs it; a one-machine path becomes a path
from the repository root or a configured location, an environment takes its full domain name, and a
sample value becomes a plainly synthetic one. Left alone: a trivial single-use literal; a literal a
protocol or provider defines for every caller; and the same values in prose, which another doctor
owns.

## Hand-Written Styling

Styling written by hand where a shared component owns it. The aim is the app the general React rule's
**Components and Props** describes: every page a tree of common components configured by props and
variants, so every page looks standard and the app holds no styling of its own:

```tsx
<Page title="Recipes" actions={<Button>New recipe</Button>}>
  <Section title="Favorites" description="The recipes you cook most often.">
    <Stack gap="md">
      <Row justify="between">
        <Text>Lemon tart</Text>
        <Badge tone="neutral">40 min</Badge>
      </Row>
    </Stack>
  </Section>
</Page>
```

- in every app built on a shared UI library: every `className`, class-merging call such as `cn(`,
  class string held in a constant or style module, style rule or styled component of the app's own
  beyond the stylesheet line that loads the library's, and inline `style` whose values are not read
  from saved data — counted per app;
- inside the shared library: every layout, spacing, color or type size written as raw classes in a
  component where a primitive expresses it, and every shared component taking a `className` prop.

The remedy is the owner's existing prop or variant at the call site, and where none expresses the
case, a new prop or variant on the shared component that owns it — never a local wrapper, class
constant or style module in the app; inside the library, the primitive in place of the raw classes,
and each `className` prop removed with its callers moved onto variants. A finished run brings every
app's count to zero: a use left standing is an open finding, never a disposition. Left alone: an
inline style whose values come from saved data, such as a column width the reader dragged; inside
the library, the classes a primitive is made of and the allowances the general React rule's **Components and
Props** grants there.

## Reads As Slop

Code a reviewer recognizes as generated: correct, and still a shape no careful author writes. The
six checks below are the lens. A finding outside them is admitted only when the reviewer names the
concrete shape — the lines, and what a careful author would have written in their place — and what
it costs a reader, such as a second place to look or a branch to hold in mind; "reads as generated"
names neither and is no finding. A package is also read whole, since a reviewer calls one slop from
its shape before opening any file, and each such finding states its measure: the file count against
the responsibilities held, the exported names against the names consumed, the depth of a component
chain. A shape another lens owns is fixed under that lens. **A shape a rule or a declared
dependency prescribes or exempts is kept**: where the reviewer still judges it slop, the report
proposes the rule change to the user and the code stays as the rule has it.

- **Tangled control flow** — the pre-pass's complexity findings: nesting deeper than the
  repository's lint configuration allows, three levels by default; nested loops that a lookup map,
  a set or one pass replaces; an if/else ladder that a table, a match or early returns flatten; a
  boolean parameter that switches a function between two behaviors.
- **Narrating comments and docs** — a comment restating the line below it; a comment justifying a
  choice whose reason lives in code the repository controls; a comment narrating what a branch,
  guard or invariant does or protects against; a comment or docstring recounting what the code
  used to do, against `pre-production`'s **Documentation** conventions; a second comment on
  behavior another party owns; a docstring listing the parameters, return or raised types the
  signature already declares, or running past the line the repository's language rules require; a
  JSDoc block on a prop, field, type or component; a comment on an external quirk running past two
  lines; banner or section-divider comments; a comment explaining what a better name would show.
- **Ceremony** — the pre-pass's lint findings for it: a temporary assigned and returned on the next
  line; a branch returning `True` or `False` to restate its own condition; comparing to `True`,
  `False` or `None` with `==`; a hand-written loop that a comprehension, builtin or
  standard-library call already does; a helper re-implementing the standard library; statements of
  different phases run together with no blank line between them, against `pre-production`'s **Code
  Layout** conventions.
- **Defensive noise** — a try/except around code that cannot raise what it catches; catch, log and
  re-raise repeated at each layer.
- **Names that do not say their subject** — every name, read against `pre-production`'s **Naming
  And Language** conventions: a verb with no object; `data`, `result`, `temp`, `info`, `helper`,
  `manager` or `handler` naming something specific; `_new`, `_v2`, `_final` or `_fixed` suffixes; a
  name saying how rather than what; a word right only in another field, or one thing called by two
  words; a name a reader cannot map to what it renders or holds; two exported names for one need,
  and one name on two exports; the pre-pass's hits for each term `banned-terminology` lists; and
  spelling or vocabulary that is not American English.
- **Padding** — a function past the length the repository's configuration sets, about sixty lines by
  default, doing several separable phases; log lines restating the step the code just took; emoji or
  exclamation in comments and logs.

The remedy is the plain shape a careful author writes: flatten, look up, return early, inline,
delete the comment and let the code or a better name carry it, cut a docstring to the line the
language rules require and delete it only where they require none, cut a quirk comment to the
external behavior in one or two lines, rename to the word that says the subject — every name built
on a banned term for that meaning, as `banned-terminology` renames them — and split the function at
its phases. A comment stating a behavior the code must keep is replaced by a test that fails when
that behavior regresses, never deleted on its own. Each lint rule that reported is proposed as the
guard `doctor-protocol`'s **Guard Recurrences** asks for. Left alone: a nested loop over small
fixed sets; a comment of one or two lines recording behavior outside the repository — a third-party
or protocol quirk — that the code cannot show; a log line reporting an outcome, status, progress or
failure an operator reads; a long function whose phases share state a split would have to pass
around; a name a framework, protocol or provider defines; and a name on an owned contract, whose
rename is the contract break `banned-terminology` describes.

## Tolerated Past

Code that tolerates a past the repository no longer has, or silences what would report it. Trace
each finding to the contract, producer, caller or check that proves the tolerated past is gone;
without that proof it is not a finding.

- **Default over contract** — every `or` with a literal, nullish fallback, lookup with a default,
  attribute read with a default or probe on the repository's own type, optional chain on a value
  typed present, total map indexed with a fallback, and coercion of a value the same module writes
  in one shape: the declaration of the value read; a declaration that supplies it makes the
  fallback a finding.
- **Dual path** — every branch on input format or encoding, defensive import or version branch;
  every configuration field selecting a former behavior; every backend selected by environment;
  every wire message with two fields for one concept and every reserved or deprecated wire field:
  the producers and readers on both sides, and whether any still reaches the old side.
- **Silent tolerance** — every catch that returns a default, passes or logs and continues; the
  pre-pass's suppression list, every suppression comment and type-ignore read against the
  measurement with it removed, and every escape hatch that does a suppression's job, an annotation
  of `Any`, a cast that only quiets the checker, arguments passed through unnamed, as the
  general Python rule and the TypeScript rules' **Suppressions** name them; every rule switched off in
  tool configuration with zero instances of what it reports; every pipeline step whose failure is
  ignored; every filter that narrows a check to changed lines.
- **Censored failure** — every record of a failure that drops the exception's message, notes or
  traceback, renders it as its type alone, replaces it with a placeholder, leaves out a provider's
  error response, or redacts a warning or error wholesale, against `pre-production`'s **Logging**
  conventions: read every logging call inside a handler or beside a raise, and every redaction
  filter with what it matches.
- **Deprecated usage** — every warning the pre-pass's install, build and suite logs printed, and
  every call, setting, default or dependency its owner has deprecated, as `pre-production`'s
  **Deprecated usage and printed warnings are defects** says.
- **Dead branch and dead entry** — every union member no caller passes and the arm handling it;
  every narrowing arm the module's own writer makes unreachable, and every guard for a state no
  writer can produce, read as `code-simplify`'s **A guard for a state no writer can produce is dead
  code** reads one; every enum member nothing produces; every key a label map or switch holds that
  its producer does not carry; every build, trace, ignore or external-package entry in tool
  configuration naming a path or dependency that is gone; and the pre-pass's dead-code list
  confirmed against the symbol index: every exported type, helper or constant with no consumer
  outside tests, and the client it served.

The remedy is the current path alone: read the contract, raise the violation, fix the shape at its
source, delete the suppression and let the check's verdict gate again, type the value the escape
hatch hid, log the failure whole with only typed secrets concealed, move to the supported
replacement or turn on the default its owner says is coming, delete the branch, the guard with its
message, the widened type and the test that only exercised it, and delete a symbol only tests
consume together with those tests, as the `python-boundaries.md` rule says of dead code. Left
alone: a genuinely optional third-party field; failover between live providers; a non-temporal
second strategy; a catch that compensates and re-raises; a cancellation carve-out; a pattern the
repository's rules prescribe by name; a member a stored row or a third-party producer can still
supply; a branch a caller outside the audited scope still reaches; a check after a lock, a
transaction start or an `await`, where the value can change in that window; a guard on a
data-fetching library's loading slot; a component primitive that works controlled or uncontrolled;
a name a framework prescribes; a symbol tests call as support, which another doctor moves to test
utilities; one value under two names, which **Pass-Through Layer** owns; a record that reports no
failure and withholds personal data; the one narrow warning ignore `test-fixture`'s **Test
Configuration** allows for a third-party package's own defect; and migration bodies and backfills,
where reading two stored formats is the job rather than a survival.

## Migration Chain

A chain, its registries and its tooling, held to one shape and no more machinery than the job.

- **Graph and references** — one head per chain on a linear path; every parent resolves; no merge
  revision joining a fork; file name, identifier and header agree; no placeholder identifier or
  fabricated timestamp; every registry names real revisions in chain order, with no boundary claimed
  twice.
- **Uniformity** — one header style and a generator template that emits it; no generator residue;
  no per-revision copy of a value a manifest carries; one idiom per operation through the shared
  helpers; a revision name describing the schema change.
- **Downgrade** — every upgrade step reversed in the right order; an empty downgrade only where the
  policy mechanism records the loss with recovery material; a downgrade a fraction of its upgrade's
  size is read.
- **Survivorship** — every revision meets the migration skill's **Authoring Rules** for a
  destructive operation's policy entry and a data-reading migration's preparation hook, and its
  **What A Change Owes The Rows It Breaks** and **Stored-Format Transitions**; verify and reverse
  hooks that resolve to unconditional success verify nothing; an exactness check the tests already
  enforce is verified to run, never re-implemented.
- **Parity** — the pre-pass's replay and drift result: replay from empty matches the current
  models; a model change without a revision, a revision changing what no model declares, and a
  historical revision importing a current model are each a finding.
- **Placement** — revision code, backfill packages and temporary tables where the migration skill's
  **Migration Support Packages** and **Temporary Backfill Tables** place them; a value list a
  revision repeats is read from the migration package's own declaration where one holds it, and a
  historical revision never imports a current application model to get it.
- **Environment and CI** — per-chain environment modules differ only in the service they name; no
  hand-maintained path filter or table beside the manifest that derives it; every documented
  migration command exists.
- **Tests** — lifecycle wiring only in the shared test setup; fixtures and helpers where the
  migration skill's **Where A Revision's Test Scaffolding Lives** puts them; a revision-to-test
  pairing rule the repository states holds; a migration-test deferral record pointing at a path that
  no longer exists is reported to `defer-scope`.
- **History** — the migration skill's **Applied Is What Makes History** decides whether a revision
  is corrected in place or by stacking; a create-then-rename across unapplied revisions collapses; a
  merge-of-main revision carrying unrelated operations is split or rebaselined; a hand edit to a
  generated revision is stated in the change.
- **Tooling** — each piece of repository tooling around the migration library is weighed against
  what the library already does and what its extension points can do: a rewriter, renderer or
  post-processing pass is a finding when it restates the library's own output, or when the library's
  generation hooks — a render hook, a revision-directive hook, a custom template — can emit the same
  result as the revision is written. Read those hooks' documentation and the repository's current
  use of them before keeping the pass. A runner that wraps the library's command with nothing added
  is a finding too.

The remedy is the one shape: re-pointed parents, regenerated headers and the shared helper in place
of per-revision idioms, each only where **Applied Is What Makes History** allows editing that
revision; the missing policy, hook or downgrade added; code moved to its owner, tooling the library
makes redundant deleted with its callers switched to the library, and the repository's migration
skill followed for every correction. Where project guidance says no environment keeps data, a chain
grown long is collapsed into one baseline revision. Left alone: an applied revision's body, which
is corrected only by stacking; and the schema the chain produces — its nullability, keys and
indexes — which another doctor owns.

## Build And Root

Build, CI and root files carrying more than they need, or built against the workflow rules.

- every container file differing from a sibling only in a name, port or path: compare them line by
  line;
- every workflow job repeating another's setup steps, and every workflow pair that has drifted
  apart;
- every script with no caller and no documented use, and every pair of scripts doing one job;
- every root or tool configuration file no tool in use reads, every package script for an app that
  does not exist, every second deploy path beside the live one, and template residue for tools the
  repository does not use;
- every value — a port, a version, an image name — declared in more places than the tools need;
- every workflow and action read against the `github-workflows` rule, bullet by bullet, each
  bullet's result reported: a pull-request test job that runs on a draft, a `run` step holding
  control flow or program code, a job name built from an expression, a runtime version written in
  the workflow where a version file supplies it, a required input that carries a default or a step
  skipped when it is empty, a Boolean input named for something other than what it enables, an
  owned package placed by a toggle, a step that only forwards a value, a step whose whole body
  exports environment, and a job under an environment that picks a secret or variable by a
  per-stage name;
- every workflow that installs a project package outside the manifest, against the `github-workflows`
  rule's **Dependency Installation**.

The remedy is one parameterized file, a shared composite action or reusable workflow, one script,
one source for each value, deletion of what nothing reads, and for a workflow finding the shape
the cited bullet states, with a checked-in script under the repository's workflow-scripts folder
where a step held logic. Left alone: a difference a deployment target requires, with the target
named; an external action's own input contract; and a suite job's time limit and a test run's
environment values, which another doctor owns.

## Configuration Drift

A configuration name that the matrix shows out of step, or that its code treats as optional when
the deployment needs it:

- **Missing** — a field a settings model declares that an environment booting that model does not
  supply, test environment included, or a default its reader refuses while no deployment sets it;
- **Orphaned** — a name an example file, manifest or environment block supplies that no model
  declares and no reader reads;
- **Mismatched** — one name with different types, defaults, placeholder styles or required-ness
  across locations, or an override present in one sibling environment and absent from another that
  boots the same model;
- **Misdeclared** — one name declared on several models with the same type and default, or a name
  a process receives and reads that no model it owns declares;
- **Unused** — a field with no reader, or one whose default is absence that no deployment sets while
  its reader branches on it; tests are not readers, and a test block or local example file is not a
  setter;
- **Weakened** — a value the code needs that is declared optional, or with a default on which a
  production deployment would not get the full behavior the value exists for; and a reader that
  skips, switches off or weakens its work when the value is unset. This shape is judged from the
  declaration and the reader alone, whatever the deployment columns show, as `pre-production`'s
  **Configuration** conventions and `code-simplify`'s **Configuration is required unless it has a
  safe default or its owner documents an absence** say;
- **Bypassed** — the pre-pass's environment reads in application code outside the typed model.

The remedy: a missing value declared wherever its siblings are, with a placeholder in test and
example locations and no real value committed anywhere; an orphaned or unused name deleted with
every vestige — the example line, the manifest entry, the test placeholder, the doc sentence; a
mismatch reconciled toward the typed model's declaration, a per-environment override stating its
reason; one declaration the processes needing it share, on the shared base or on a model scoped to
the capability that the processes without it never load, and a subclass that deliberately narrows
the shared declaration saying so on the field rather than restating it; a weakened value declared
required, its absence branch deleted, and a synthetic value set in the test and example locations
that had none; a bypassed read routed through the typed model; and, where the repository can derive
an example file or test block from the models, that derivation proposed as the guard. Left alone: a
default that is safe; an absence the value's owner documents as supported, with that contract named
in the ledger; and a control that skips itself when its setting is unset where an attacker gains by
it, which is a vulnerability fixed in this run as `doctor-protocol`'s **Resolve The Scope** says.

## Dependency Drift

Declared dependencies out of step with what the code imports and the checks invoke, or behind what
their owners have released.

- the pre-pass's dependency-checker list: every package no first-party module imports and no check
  invokes, including an audit tool never wired into a check, and every import satisfied only
  transitively;
- one package pinned with different floors or ranges across manifests, or a shared floor below a
  sibling's;
- a lockfile older than its manifest, a lock entry the manifest no longer declares, or two
  lockfiles resolving overlapping sets from different floors;
- two libraries declared for one job, or a package the platform, framework or runtime provides;
- the pre-pass's outdated list: every dependency held below its newest stable release, every
  language runtime in a version file, CI leg or container below the newest stable one the project
  works with, and every container base image behind its newest stable tag, as `pre-production`'s
  **Versions** conventions say;
- the pre-pass's package-audit list: every declared package with a published advisory a release
  fixes;
- the pre-pass's commit-hash pins: a manifest, shared checkout or workflow reference pinned to a
  commit where a maintained tag or branch exists.

The remedy: the unused declaration removed with its lock entries; an audit tool wired into an
existing check or removed; an undeclared import declared in the project that imports it; one range
chosen from actual usage, stated where it changes behavior; a lockfile regenerated only through the
package manager's own command; one library for one job, the one the rest of the repository uses;
the runtime, base image and each outdated or advised package moved to its newest stable release in
the version file, container files, CI and lockfile together, with the code changes the release
needs; and a commit-hash pin replaced by the maintained tag, or the maintained branch where no tag
exists. Left alone: a package held back where an install or test shows the newer release failing on
the project's runtime, with that failure named in a comment beside the constraint; a lockfile's own
resolved commits; and the supported range of a library published for consumers outside the owner's
projects.

## Test Slop

Tests that cost reading time and prove nothing, audited with the code and fixed after it.

- run `test-fixture`'s **Test Value And Retention**, **Naming Checks** and **Auditing Existing
  Doubles** over every test module mirroring code a finding in another lens changes;
- every test that only exercises a layer, alias, branch or symbol another lens's finding removes;
- every test package with no tests, and every test module mirroring no source.

The remedy is `test-fixture`'s dispositions: repair, fold into the keeper, or delete with its
evidence, with coverage of a removed layer's behavior kept at the real boundary. Left alone: every
other test — timing, suite budgets, cross-suite layout, copied blocks between test modules, suite
configuration and coverage maps belong to another doctor and are named, not run.
