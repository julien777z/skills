# Code Slop Doctor Lenses

Each lens states its defect shape, the checks that find every instance, the remedy, and what is left
alone.

## Pass-Through Layer

A layer, wrapper or alias that only hands the call on.

- every function, method, component or hook whose body is one call that receives the caller's own
  parameters, unchanged or renamed, or with fixed or defaulted values added, and adds no policy of
  its own — callers could make that call with what they already hold: count its callers. Rendering
  one other component is that call: a component passing on its props with some look or behavior
  props fixed or defaulted, and no content, data or state of its own, is a finding;
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
renders, as the React rules' **Components and Props** says, a chain collapses into one component
with variants, and a hook-only component becomes the hook its callers call. Left alone: a wrapper
that adds policy, which is only validation, error mapping, retries, authorization, caching or
translation at a provider boundary — a fixed or defaulted value, a hook call, a class or a renamed
prop is never policy; a function that names a domain operation by mapping a domain value onto the
call below it; one external name per field at a provider boundary; the explicit public-surface
re-export a language defines for a package, in a short list; a component that carries the
`"use client"` boundary for a Server Component call site, as the React rules' **Components and
Props** says; and a file the framework looks up by path.

## Speculative Abstraction

Structure built for cases that never arrived.

- every interface, Protocol or abstract base with one implementation, used by one consumer, and
  never substituted in a test through its declared seam;
- every base class with one subclass, every generic with one instantiation, every factory or
  registry with one product;
- every configuration field, option or prop no caller sets or every caller sets the same way;
- every context, provider or store read by one consumer, and every value threaded through layers
  that never read it.

The remedy is the concrete thing: the implementation in place of the interface, the subclass folded
into its base, the factory replaced by the constructor, the option replaced by its one value, the
store replaced by local state or a prop. Left alone: an interface the application declares as a
test seam and tests use; a plugin point a configuration file or an external consumer fills.

## Duplicate Implementation

One question answered twice.

- every data declaration whose field set matches another's, or is a subset carried by hand rather
  than derived; every empty subclass that only renames a model; every hand-written type that mirrors
  a generated contract type;
- every hand-written validation — a model validator, a manual check, a parse function — that the
  validation library's own tools express: a constrained or annotated type, a field validator, a
  reusable annotated alias, a type adapter, a computed field, a discriminated union;
- for every helper in scope, the same operation under another name, in another package or in
  another language — a formatter, a parser, a derivation, a guard, a client construction, a cache
  key;
- every pair of enums or literal unions with overlapping members and a bridge between them;
- the duplication detector's result from the measurement, read pair by pair rather than repeated.

The remedy is one owner, placed by `code-simplify`'s ownership analysis — the shared package every
consumer reads where more than one deployable needs it — with the copies and the bridge deleted and
generated types used directly or derived from. Left alone: a generated mirror; a demonstrated
dependency, domain or contract boundary; two contract models, which another doctor owns.

## Fragmented Use Case

One use case paying for many calls to operations the repository owns. The unit is the use case, not
the endpoint: read each row of the use-case table, never the list of operations alone.

- every use case calling several owned operations it always needs together — one page's load, one
  handler serving one request;
- every call made once per item — per row, per record, per identifier — inside a loop, a list render
  or a fan-out, where one operation could take the set;
- every chain of calls each waiting for the one before although none reads another's result;
- every owned operation whose callers all pass its result straight to another owned operation;
- static data the client can carry in its build — a published reference list, an owned enum and
  its labels — fetched at run time.

The remedy is the operation shaped for its use case: one owned operation returning what that use
case always needs together, assembled server-side from the existing queries and concurrently where
they are independent; a batch operation taking the set in place of the per-item call; independent
calls that stay separate issued together rather than in turn; static data shipped with the client
through its package or generated contract; every caller moved, and each operation left with no
caller deleted with its client. A batch or merged operation authorizes each item and each returned
field as the operations it replaces did; where it cannot, those operations stay separate, as Left
alone says. The use case is timed before and after on the same stack, and a merge that makes it wait
longer for its first useful content is not the remedy. Two cases go to the user for approval, never
merged or left alone silently: an operation another use case also calls on its own, where the use
case may gain a merged operation while the other keeps its own; and a read only some runs of the use
case need, which a merged operation may still carry. Each request lets the user decide without
opening the code: the operations it would combine, by method and path or RPC name; the proposed
operation's method, path, parameters and response fields; every other caller of each of those
operations, found in the code by page, job or service, with what it reads and whether it already
shares the use case's read; what would become of each existing operation, kept for which caller or
deleted; the current counts and timings, and the call count the proposed operation would leave; and
the run's recommendation. The timings after are measured once the merge is approved and made. Left
alone: a call a later interaction makes — a tab opened, a page turned, a row expanded; reads under
different authorization or caching that one response cannot carry, and any set of items one
operation cannot authorize as the per-item calls did; a slow section kept apart so it does not hold
a fast one, with the timing showing it; and a third-party provider's operations, batched only where
the provider offers it.

## Divergent Siblings

Things of one kind built in different shapes.

- read each kind's slot table: a slot one deployable fills with a shared helper and another fills
  by hand, a slot filled differently in each, and a slot one fills and its siblings leave empty with
  no contract difference to explain it, are each a finding;
- sibling routes, pages and features: one data-fetching style, one folder layout, one way to
  submit, load and report errors per kind; a feature split across several places its siblings keep
  in one is a finding;
- copies of one module in two places that have drifted apart — providers, clients, configuration —
  compared line by line.

The remedy is one structure per kind: the shared shape lives in the shared package and each sibling
supplies only what differs, its name, port, servicers or routes. The slot's best existing
implementation becomes the shared one under `code-simplify`'s rubric **Standards**.
Left alone: a slot whose difference a contract requires, with the contract named.

## Scattered Structure

Code spread over more files and folders than its responsibilities need.

- every module with one or two small public symbols whose siblings would hold them;
- every module, whatever its count, that the `code-simplify` rubric's **A new module whose concern an existing module already owns**
  standard merges into an existing owner, or into one a broader name would make its owner;
- every UI area folder whose modules include **Pass-Through Layer**'s wrapper components or links
  of its chains;
- every pair of modules or folders answering the same question, and every concern split across
  several folders;
- every catch-all module mixing unrelated owners, and every `lib`/`utils`-style pair with no rule
  for what goes where;
- every file or folder whose name says something other than what it holds;
- every declaration list ordered by when its entries were added rather than by what they describe
  — the fields of a message or model, an enum's members, a configuration's keys — so one concept's
  entries sit apart, and every owned wire contract whose field numbers record that history.

The remedy is restructuring, done without hesitation: merge modules of similar scope into one,
collapse one-symbol modules into their owner, split a catch-all by owner, move code to where its
consumers expect it, rename files and folders for what they hold, and regroup each declaration list
by concept, renumbering an owned wire contract's fields to match — every importer, producer and
consumer updated and every generated target regenerated in the same change, no re-export left
behind. A UI area folder is merged down to the components that earn their place under the React
rules' **Components and Props**, each wrapper becoming a variant on its owner. Left alone: a module
boundary a framework prescribes, a package boundary a build or distribution artifact needs, and the
one-component-per-file split the React rules require for the components that remain — never for a
wrapper.

## Repeated Literal

One meaning spelled out many times.

- count every class-name or style string literal across the components in scope — extract each
  `className`, `class`, style-token or `cn(...)` argument string and tally identical values — and
  report every value that appears in three or more places with its count and locations, outside
  an app built on a shared UI library, whose class strings **Hand-Written Styling** owns and fixes
  as variants;
- every error-to-message conversion written inline beside a helper that does it; every port, host or
  URL declared in more than one place; every message template spelled out at more than one site;
  every list restating an enum's members;
- every constant restating a token the theme or framework declares — a breakpoint width, a color, a
  spacing step, a layer order — in script or in a second stylesheet.

The remedy is one owned definition — a component or style token, the existing helper, one
configuration source, the enum itself — and every site reading it; a restated theme token is read
from the theme, through one shared hook where script needs it.

## Hand-Written Styling

Styling written by hand where a shared component owns it. The aim is the app the React rules'
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
the library, the classes a primitive is made of and the allowances the React rules' **Components and
Props** grants there.

## Reads As Slop

Code a reviewer recognizes as generated: correct, and still a shape no careful author writes. The
test is the slop question `acceptance-gate`'s diff review asks first, with the shapes it lists as
examples rather than the limit: each reason an experienced reviewer would give is a finding with its
remedy, whether or not a check below or another lens names it. A shape another lens owns is fixed
under that lens, and an exemption in this skill or a rule that would keep a shape the reviewer calls
slop is named in the finding and does not keep it. Apply the test to each package whole as well as
file by file — its file count, its exported names, the depth of its component chains — since a
reviewer calls a package slop from its shape before opening any file. Every check below makes the
test concrete.

- **Tangled control flow** — nesting deeper than the repository's lint configuration allows,
  three levels by default; nested loops that a lookup map, a set or one pass replaces; an if/else
  ladder that a table, a match or early returns flatten; a boolean parameter that switches a
  function between two behaviors.
- **Narrating comments and docs** — a comment restating the line below it; a comment justifying a
  choice whose reason lives in code the repository controls; a comment narrating what a branch,
  guard or invariant does or protects against; a docstring listing the parameters, return or raised
  types the signature already declares, or running past the line the repository's language rules
  require; a JSDoc block on a prop, field, type or component; a comment on an external quirk
  running past two lines; banner or section-divider comments; a comment explaining what a better
  name would show.
- **Ceremony** — a temporary assigned and returned on the next line; a branch returning `True` or
  `False` to restate its own condition; comparing to `True`, `False` or `None` with `==`; a
  hand-written loop that a comprehension, builtin or standard-library call already does; a helper
  re-implementing the standard library.
- **Defensive noise** — a try/except around code that cannot raise what it catches; catch, log and
  re-raise repeated at each layer.
- **Placeholder and confusing names** — `data`, `result`, `temp`, `info`, `helper`, `manager` or
  `handler` naming something specific; `_new`, `_v2`, `_final` or `_fixed` suffixes; a name saying
  how rather than what; a name a reader cannot map to what it renders or holds; two exported names
  for one need, and one name on two exports.
- **Padding** — a function past the length the repository's configuration sets, about sixty lines by
  default, doing several separable phases; log lines restating the step the code just took; emoji or
  exclamation in comments and logs.

The remedy is the plain shape a careful author writes: flatten, look up, return early, inline,
delete the comment and let the code or a better name carry it, cut a docstring to the line the
language rules require and delete it only where they require none, cut a quirk comment to the
external behavior in one or two lines, split the function at its phases. A rewrite of executable
code keeps its behavior exactly, and the repository's tests prove it before and after; executable
code no test covers gets one first. A comment stating a behavior the code must keep is replaced by a
test that fails when that behavior regresses, never deleted on its own. Left alone: a nested loop
over small fixed sets; a comment of one or two lines recording behavior outside the repository — a
third-party or protocol quirk — that the code cannot show; a log line reporting an outcome, status,
progress or failure an operator reads; a long function whose phases share state a split would have
to pass around.

## Tolerated Past

Code that tolerates a past the repository no longer has. Trace each finding to the contract,
producer, caller or check that proves the tolerated past is gone; without that proof it is not a
finding.

- **Default over contract** — every `or` with a literal, nullish fallback, lookup with a default,
  attribute read with a default or probe on the repository's own type, optional chain on a value
  typed present, total map indexed with a fallback, and coercion of a value the same module writes
  in one shape: the declaration of the value read; a declaration that supplies it makes the
  fallback a finding.
- **Dual path** — every branch on input format or encoding, defensive import or version branch;
  every configuration field selecting a former behavior; every backend selected by environment;
  every value reachable under several names; every wire message with two fields for one concept and
  every reserved or deprecated wire field: the producers and readers on both sides, and whether any
  still reaches the old side.
- **Silent tolerance** — every catch that returns a default, passes or logs and continues; every
  suppression comment and type-ignore, read against the measurement with it removed; every rule
  switched off in tool configuration with zero instances of what it reports; every pipeline step
  whose failure is ignored; every filter that narrows a check to changed lines.
- **Dead branch and dead entry** — every union member no caller passes and the arm handling it;
  every narrowing arm the module's own writer makes unreachable; every enum member nothing
  produces; every key a label map or switch holds that its producer does not carry; every build,
  trace, ignore or external-package entry in tool configuration naming a path or dependency that
  is gone; every exported type, helper or constant with no consumer, and the client it served.

The remedy is the current path alone: read the contract, raise the violation, fix the shape at its
source, delete the suppression and let the check's verdict gate again, delete the branch, the
widened type and the test that only exercised it. Left alone: a genuinely optional third-party
field; failover between live providers; a non-temporal second strategy; a catch that compensates
and re-raises; a cancellation carve-out; a pattern the repository's rules prescribe by name; a
member a stored row or a third-party producer can still supply; a branch a caller outside the
audited scope still reaches; a guard on a data-fetching library's loading slot; a component
primitive that works controlled or uncontrolled; a name a framework prescribes; and migration
bodies and backfills, where reading two stored formats is the job rather than a survival.

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
- **Parity** — replay from empty matches the current models; a model change without a revision, a
  revision changing what no model declares, and a historical revision importing a current model are
  each a finding.
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
grown long is collapsed into one baseline revision.

## Build And Root

Build, CI and root files carrying more than they need.

- every container file differing from a sibling only in a name, port or path: compare them line by
  line;
- every workflow job repeating another's setup steps, and every workflow pair that has drifted
  apart;
- every script with no caller and no documented use, and every pair of scripts doing one job;
- every root or tool configuration file no tool in use reads, every package script for an app that
  does not exist, every second deploy path beside the live one, and template residue for tools the
  repository does not use;
- every value — a port, a version, an image name — declared in more places than the tools need.

The remedy is one parameterized file, a shared composite action or reusable workflow, one script,
one source for each value, and deletion of what nothing reads. Left alone: a difference a
deployment target requires, with the target named.

## Configuration Drift

A configuration name that the matrix shows out of step:

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
- **Bypassed** — an environment read in application code outside the typed model.

The remedy: a missing value declared wherever its siblings are, with a placeholder in test and
example locations and no real value committed anywhere; an orphaned or unused name deleted with
every vestige — the example line, the manifest entry, the test placeholder, the doc sentence; a
mismatch reconciled toward the typed model's declaration, a per-environment override stating its
reason; one declaration the processes needing it share, on the shared base or on a model scoped to
the capability that the processes without it never load, and a subclass that deliberately narrows
the shared declaration saying so on the field rather than restating it; a bypassed read routed
through the typed model; and, where the repository can derive an example file or test block from the
models, that derivation proposed as the guard.

## Dependency Drift

Declared dependencies out of step with what the code imports and the checks invoke.

- every package no first-party module imports and no check invokes, including an audit tool never
  wired into a check;
- every import satisfied only transitively;
- one package pinned with different floors or ranges across manifests, or a shared floor below a
  sibling's;
- a lockfile older than its manifest, a lock entry the manifest no longer declares, or two
  lockfiles resolving overlapping sets from different floors;
- two libraries declared for one job, or a package the platform, framework or runtime provides.

The remedy: the unused declaration removed with its lock entries; an audit tool wired into an
existing check or removed; an undeclared import declared in the project that imports it; one range
chosen from actual usage, stated where it changes behavior; a lockfile regenerated only through the
package manager's own command; one library for one job, the one the rest of the repository uses.

## Test Slop

Tests that cost reading time and prove nothing, found after the code has settled.

- run `test-fixture`'s **Test Value And Retention**, **Naming Checks** and **Auditing Existing
  Doubles** over every test the earlier phases touched and every test module mirroring code they
  changed;
- every test that only exercised a layer, alias or branch the earlier phases removed;
- every test package with no tests, and every test module mirroring no source.

The remedy is `test-fixture`'s dispositions: repair, fold into the keeper, or delete with its
evidence, with coverage of a removed layer's behavior kept at the real boundary. Timing, suite
budgets, cross-suite layout and coverage maps belong to another doctor and are named, not run.
