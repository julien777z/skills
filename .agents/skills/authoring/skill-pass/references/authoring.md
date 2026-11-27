# Authoring Agent Guidance

Contents: **Where Guidance Lives** (placement), **Harnesses**, **Rules**, **Skills** (package and
references, descriptions, dependencies, decisions, subagents, flows, output, routers), **Writing**
(wording, scope and size budgets), **Scripts**, **Validation**.

This reference holds how anything under `.agents`, and code outside it that sets up, configures
or fixes how agents run, is written, placed, served to harnesses and validated. The pass in
`SKILL.md` names the section each step applies, and the
[vendor rubric](vendor-rubric.md) beside this file holds what the model vendors' guidance adds.

## Where Guidance Lives

- **Guidance about anything under `.agents` lives in this reference**, however widely it holds: how
  a skill, rule, agent definition, hook, setting, reference or project guidance is written, where it
  goes, which harnesses it serves, how its generated mirrors are produced, and how a change to it is
  validated. So does guidance about code outside `.agents` that sets up, configures or fixes how
  agents run, such as workspace setup or machine provisioning. A rule, another skill or
  `.agents/global.md` keeps only what its own subject needs and leaves the rest here: a skill cites
  these sections by name, and a rule or `.agents/global.md` cites them by subject.
- **Guidance lives in skills and rules, never in a harness's memory.** A correction, preference,
  limit, exception or operating fact that tells agents how to work — such as a cap on workers, a
  repository that gets only minimal changes, or a machine whose processes may be ended — goes,
  as a guidance edit, into the skill, rule, project guidance or reference that owns it, so every
  harness and session reads the same copy; the global rules forbid writing a harness's memory. A
  memory found holding guidance is moved to its owner and deleted.
- **Agent configuration is read only by agents.** Skills, rules, agent definitions and the scripts
  they hold reach an agent session through its user-level install, or through a checkout that the
  local setup places for agent sessions. A repository's CI, build, tests, dependency manifests,
  lockfiles and product code never clone, install, copy, vendor or import any of it; the only
  automation that reads it is the workflow that syncs or validates the agent configuration itself,
  such as Agent Sync. A repository tool that agents run, such as a check helper built on a skill's
  client, loads that script only inside the agent's run. Its tests build the values the script
  would return and double it at the tool's own binding, so they pass in a checkout that holds no
  skills. Code that both agents and the repository's own automation need is a package of its own,
  never a skill.
- **A requirement goes in the skill that runs when it applies; a rule or `.agents/global.md` takes
  only what no skill can carry.** Before adding to `.agents/global.md` or a rule, name the skill
  that runs when the requirement applies.
  - A requirement about how a kind of work is done goes in the skill that runs when that work is
    done: executing a task in the skill that runs execution, merging in the skill that merges, test
    writing in the skill that runs for tests.
  - A rule file, `.agents/rules/*.md`, exists only for a subject no skill runs for: a language,
    framework or tool matched by file pattern, or a host such as GitHub whose rules span many
    skills. A requirement goes in one only when no skill runs where it applies, and it holds in any
    repository using that technology or host.
    A subject split across several rule files keeps one general file, named `general-<subject>.md`,
    for what applies to all work in it; each other file is named `<subject>-<topic>.md` and holds
    one topic, so the names show which file is the default and which load for a narrower task.
  - `.agents/global.md` holds only what must bind before any skill has loaded: which skills to
    start, who can authorize a merge, a deployment or a skill run, that only the user's words are
    approval, and how questions reach the user. A requirement goes there only when it must bind
    with no skill loaded. How agent configuration is written, placed, checked or made to serve each
    harness never goes there, however widely it must hold: it lives in this reference, which the
    work it governs loads.
  - Examples in `.agents/global.md` and a rule stay generic: invented names and
    placeholder shapes, never this repository's modules, helpers, packages, paths, or domain
    vocabulary, and never the product, tool, or platform whose incident prompted the change.
- **Skills cite rules; a rule never names a skill.** A rule file names no specific skill for any
  purpose: an exception, a permission, a citation of one of its sections, or a description of what
  it does. A rule holds in every repository and loads before any skill is chosen, so a skill it
  names may be absent, renamed or moved, and every exception listed there grows the rule by one
  case per skill. The rule states its requirement in full and words each exception and owner
  generically, such as "unless a skill in use authorizes it", "a skill that states it polls" or
  "the skill that runs a merge"; where it needs a term a skill defines, it states the criterion
  itself or names the subject, such as "the product-choice rule". A requirement that makes sense
  only inside one skill moves to that skill. The skill that departs from or relies on a rule cites
  the rule.
  - `.agents/global.md` keeps the same form, with one exception, because naming is its job there:
    its instructions on which skills always start. Anywhere else it cites an owner generically by
    its subject.
- **A skill is found by its frontmatter description, so every subject a skill owns is named in that
  description.** No rule file, `.agents/global.md` or index table lists which skill owns which
  subject: a list kept beside the descriptions goes stale and repeats what they already say. A
  change that moves a subject into a skill, or adds one to it, widens that skill's description by
  a clause naming the subject as **Descriptions** says, including a subject its sections govern in
  a task that does not otherwise run the skill.
- `.agents/project.md` is the home for repository-specific guidance: the rules and conventions an
  agent follows there, such as which base classes and helpers to use and its generated sections.
- **Guidance never keeps a copy of how a repository's tooling behaves today.** Commands, flags,
  ports, test accounts, deployment targets and file layouts are read from the code, configuration
  and help output that own them, and from the README a person reads. A copy in guidance reads to the
  next agent as a contract to preserve, so it holds the tooling back from changing and goes stale
  when it does. Guidance states what an agent must or must not do by what it achieves, such as
  starting a test run from an empty database, never by the command, port or account that does it
  today; a repository keeps no `.agents/references/` folder.
- A rule that cannot be stated without naming something this repository owns belongs in
  `.agents/project.md`. Move it there rather than rewording it into something generic but untrue.
- **A new rule file is only ever a guidance correction**, written for a subject no skill runs
  for, as the placement bullet above says. A system an agent built, such as a booking
  service's flows, is documented in its code and README, never in guidance; repository guidance
  that says to add a rule per system is itself corrected.
- **Shared or repository-owned.** Generic skills live in one shared skills repository and reach
  every session through a user-level skill root; repository-specific skills, every rule, and
  repository-specific agents live in the repository they describe. Inspect a skill's content and
  dependencies to decide ownership, never its name, including for an existing skill: a user-level
  symlink shows where it is installed, not where it belongs, and a generically named skill can
  depend on one repository's contract. A new or existing skill goes to the skills
  repository only when it reads generically without losing required behavior. If making it
  generic would remove or misstate guidance it needs to give, put it in the repository it
  describes under `.agents/skills/`, at any depth; move a misplaced existing skill there.
  **Guidance whose correctness depends on a current repository's product, resources, topology, contracts, configuration, or relationships is project guidance.** It belongs in that repository's `.agents/project.md` or a repository-specific skill, regardless of the subject that exposed the gap. A shared skill may teach the classification procedure, but never carry a current repository's facts or boundaries.
  An agent definition that a shared skill runs on goes with that skill; every other agent, and
  every rule, is repository-owned.
- **Hooks belong in the repository that owns their behavior.** Keep their implementation and
  source registration under that repository's `.agents/`: repository-managed hooks go in
  `.agents/hooks/`, and hooks shipped with a skill stay in its package. A hook shared across
  repositories belongs in the shared skills repository; a hook that depends on one repository's
  behavior belongs there. Installed copies and native registrations consume that source.
- **A skill that reads generically belongs to every repository, so write it that way and put it in the skills repository.** Repository paths, product names, and domain nouns turn a reusable workflow into one repository's copy of it; keep them out unless the skill's correctness depends on that local contract, and where a skill genuinely needs one local fact — a command, an identity, a host, a package, a fixture — read it from the repository's tooling, configuration and README, as the tooling bullet above says, or from a setting, rather than baking it in. Live file paths and copied application code go stale when files move or refactors land; use generic placeholders such as `services/<name>/...`, short pattern descriptions, or minimal invented examples instead. Where a shared skill needs a repository-specific collaborator — a migrations skill, a finalization skill, a deployment skill, a deferral label — it names the role and finds the skill by its description in the skill listing, and the repository's `project.md` **Repository Skills** table says which local skill fills the role.
- **What a skill builds on in the repository it runs in is looked up there, never written into the
  skill.** A structure the skill reads — how skills or files are grouped, which folders exist, which
  skill a workflow starts from, what a page or section is called — comes from the repository when it
  has one, and the skill says what the agent does when it has none: choose the best fit itself,
  guided by a few examples in the skill of what such a choice looks like. A list of one repository's
  categories, page names or skill names written into a shared skill makes it that repository's copy;
  shared skills still name the shared skills they depend on.
- **A file's name and description bound what it owns, and so do a reference's file name and a
  section's heading inside the skill chosen.** Before choosing a skill, rule, reference or section,
  state the condition its name and description set — a release stage, a technology, a mode, a kind of
  task — and ask whether the guidance would still be true where that condition does not hold. If
  it would, that file is too narrow, however close its neighboring section: the guidance goes to
  the file whose subject matches its own. Scope is judged by subject, never reach: guidance that
  holds in every repository still goes to the skill or rule owning its subject, as the first bullet
  places guidance about `.agents` content, and `.agents/global.md` takes only what the placement
  bullet above leaves it. Use existing mentions and dependencies to find readers. Assign
  ownership by the file's responsibility and when the guidance must apply. Move existing text
  and update its readers when correcting its placement is in scope. When that relocation would
  expand the request, explain the mismatch and ask whether to include it. Continue the work
  already authorized.
- Paths inside a repository's `.agents`:
  - `agent` -> `.agents/agents/<name>.md`
  - `rule` -> `.agents/rules/<name>.md`
  - `tool` -> `.agents/tools/<name>`, a helper script agents run, found by listing the folder
  - `skill` -> `.agents/skills/<name>/SKILL.md`, or `.agents/skills/<folder>/<name>/SKILL.md`
    where the repository sorts its skills into folders; the folders group the source and never
    change the name a skill installs under.

## Harnesses

- **Everything under `.agents` works in every harness that loads it**, from one provider-neutral
  implementation and one canonical source for skills, rules, and agent prompts. So does code outside
  `.agents` that sets up, configures or fixes how agents run, such as workspace setup or machine
  provisioning that installs skills or hooks: it builds on that provider-neutral source and the
  generator each harness's files come from, never on the files of the harness the session happens to
  use. That covers what the harness runs or reads, not only prose: a hook script and the matcher
  that selects it, a skill's script, a setting, an instruction naming a tool, and how each harness
  discovers and installs the guidance. Each depends on a harness contract — its tool names, the
  payload a hook receives and the output it answers with, its settings keys — so read every loading
  harness's contract and handle each, such as a hook that reads one harness's edited file path and
  another's patch. Only a capability a single harness alone has, such as a tool no other harness
  offers, stays that harness's, confined to a scoped compatibility section or a file only that
  harness loads. Verify each path in every harness that loads the guidance or that the change sets
  up, such as running a hook against each harness's payload. A harness left unserved is a defect,
  fixed now where `pre-production`'s **Scope Follows The Defect, Not The Request** places it,
  never as new behavior.
- Keep reusable skill names, instructions, scripts, and interfaces model-agnostic. Name a client or
  model only in a scoped compatibility section where its behavior genuinely differs. A skill states
  the facts an agent gathers about its own session — its transcript, its task list, its subagents
  and their records — and leaves finding them to the agent in whichever harness runs it; outside
  such a compatibility section, a script or instruction that finds those session facts through one
  harness's files, environment variables or record layout is a defect, never a convenience.
- Never stage generated provider output manually. Only the repository's Agent Sync workflow may
  generate and commit provider mirrors.

## Rules

- For a scoped rule, declare its file patterns once as `paths` in canonical frontmatter.
  Do not duplicate them as `globs`; Agent Sync writes each provider's required scope key.
  Use `alwaysApply: true` only when the rule belongs in every session.
- **Every rule file carries a frontmatter `description`**: one sentence that says when to read it,
  in the words a task arrives in. A rule listed without one shows its file name alone, which tells a
  reader of the rule index nothing about work its file patterns cannot identify.
- **Files that load together are read as one document.** Before adding or changing a ruling or an
  example, read what every file that loads alongside the edited one says on the same point:
  `.agents/global.md` always, every rule sharing one of a scoped rule's `paths` patterns, and for a
  skill its own references, its declared dependencies and the rules matching the files it works on.
  A ruling that differs names the file it narrows and the case it covers, and an example obeys
  every one of those files, since a reader copies an example before it reads the text elsewhere
  that forbids it.
- Before adding a requirement to a shared rule, test it against a repository, skill or file without the feature that prompted it; a requirement true only for the skill that prompted it goes in that skill. If it prescribes the current repository's documentation sections, inventory, or generation workflow, put it in `.agents/project.md`; keep the shared rule limited to guidance that still makes sense elsewhere.

## Skills

### Package And References

- **Skill shape.** `SKILL.md` holds how the skill runs: its trigger, its dependencies, its
  workflow, its output, its guardrails. What a reader *applies* rather than *follows* lives in
  `references/<topic>.md` beside it, named for what it holds — a rubric, a checklist, a catalog,
  a protocol — and `SKILL.md` names the file at the point the workflow reads it. A skill with two
  routes through it (two modes, two kinds of target, two hosts) keeps the shared workflow in
  `SKILL.md` and gives each route its own reference, so the file a reader loads first stays within
  the size budget under **Writing**. References may explain the technical steps for a route selected by the
  entry point. They do not select the top-level workflow, hide a decision gate, declare a dependency,
  or invoke another skill. Scripts the skill runs go under `scripts/`; supporting files may live
  under `assets/`, `resources/`, or another directory named for their role. Keep only files the skill
  needs.
- **A skill's main idea stays in `SKILL.md`, near the top,** whatever its form, even where Skill
  shape would send it to a reference: the part a reader opens the skill to see, such as the
  mapping, principle or contract its name promises. A skill is read by people as well as agents,
  and a person scanning it sees only its body, so an idea moved to a reference is one they never
  find; the vendor rubric's placement of the most important instructions near the top gives the
  agent's side of the same reason. A reference holds what only some routes, modes or readers need.
- **A skill keeps as few references as its routes need.** Each one earns its own file because some
  route or reader skips it; a subject an existing reference's name already covers, by the
  name-bounds test above, goes there, a rename to a broader name that truly covers both is the
  other way in, and a new file is added only for a subject no name covers. The right skill never
  makes a reference or section named for another subject the place for text. A name joining two subjects, such as `x-and-y`, signals two files' worth or a
  broader name not yet found. Whenever a pass covers a skill, judge its references as a set:
  - merge references on one subject, or always read together;
  - move into `SKILL.md` a short one every run follows, or one holding the main idea above, when
    the body has room under its budget;
  - delete one nothing links to, or whose content the body or another reference already states.
- Never add `agents/openai.yaml` to a repository skill, and remove one found in a canonical
  package. Repository skills contain `SKILL.md` and only supporting files required by the skill;
  provider UI metadata stays outside repositories and is never propagated.
- Critical decisions and when to load a reference are visible in `SKILL.md`. A reader following the
  entry point reaches all guidance needed for the selected route before acting.
- Each reference has a descriptive subject, a resolved link, and a clear role within its owning
  skill. User-facing explanations identify it as that skill's reference and describe its purpose;
  a bare filename must not sound like an unexplained skill, mode, or prerequisite.
- References carry supporting criteria and technical procedures. Moving text into one is not a fix for
  overly specific guidance, duplication, unsupported claims, or an unclear ownership boundary.

### Descriptions

The front-matter `description` is read on every turn, for every skill, to decide
whether this one fires. It has two jobs. The first is to state **when** — the situations that
should reach it, in the words a task actually arrives in. The second is to carry any rule that must
bind before the body is read, since a reader often acts on the description first. What the skill
does belongs there only so far as a reader needs it to recognize those situations; the body says
the rest.

So the slash command normally earns no space. It is the skill's own name, the listing normally shows
it, and a reader deciding whether to invoke has it in hand — `Invoke as /code-slop-doctor to deslop
a repository` spends its opening clause telling the reader something they used to get here. Keep the
trigger and drop the command: `Use to deslop a whole repository or one of its areas, lenses or paths.`
The same goes for a phrase naming the skill, `Use this skill to`, and a restatement of the skill's
title.

An opaque short alias is the exception. When a user can send only that alias and it does not itself
identify the task, name its literal slash form in the description with the action it triggers. That
gives the dispatcher a match without replacing the natural-language trigger; “Use when a user enters
`/qx` to reconcile an inventory” identifies both.

Where an invocation carries an argument the trigger depends on, the argument is the thing worth
naming — a target, a scope, a mode — not the command that precedes it.

Judge a description by substitution: read it without knowing which skill it belongs to. If it still
says which situations fire the skill, it works. If the remainder names no situation, it was never a
trigger.

A description is written in the third person and stays within 1,024 characters, the limit the open
skill specification sets and a vendor's upload refuses past. Its main use comes first, because a
host's listing truncates a long description at its own cap and drops whole descriptions when the
listing passes its budget. It names kinds of situation, never a list of near-synonymous phrases
that grows by one with each missed trigger. A rule it carries because the rule must bind before
the body is read takes one clause; procedure stays in the body.

**A skill that runs only at the user's request says so in its description, never by hiding itself.**
A frontmatter flag that keeps a skill out of the agent's skill listing, such as
`disable-model-invocation`, hides every route and tool inside it: an agent cannot load it when the
user asks for it in words, cannot follow another skill that names it, and never finds a script it
holds when other work needs one. Keep every skill listed and end its description with the exact
sentence "Run only when the user asks for it.", which is how readers and tools recognize the
restriction. Gate a single user-only workflow inside an otherwise usable skill in its body.

### Dependencies

- **Refer to a skill, and to anything inside it, by the skill's name, never by path.** the `code-simplify` skill's rubric reference is right; a relative path into another skill's directory is wrong, because the directories move between repositories and user-level roots and the name is the only stable handle.
- Declare every invoked skill by canonical skill name in a near-top `## Dependencies` section of
  the owning `SKILL.md`. Each entry is only `- ` followed by the backtick-quoted skill name: no
  description, role, arguments, or surrounding workflow prose. That section lists skills only,
  never tools, plugins, scripts, references, assets, executables, or filesystem paths.
- A dependency's frontmatter owns its purpose and discovery conditions. If a caller needs to
  explain when that dependency applies, correct the dependency's description instead of keeping
  another description in the caller. Put invocation-specific effort, scope, inputs, order, and
  conditions at the actual call in the caller's workflow body.
- Keep dependency direction acyclic. A coordinator invokes lower-level operations; an operation
  returns results, required follow-up work, and unresolved decisions to its caller instead of
  invoking the coordinator or importing its workflow sections as policy. Put shared policy at an
  existing lower-level owner. Select independently applicable companion skills from their own
  frontmatter at the task boundary rather than making peers invoke each other.
- **A skill refers only to the skills it depends on, and declares every one it refers to.**
  Referring to a skill anywhere in its package — frontmatter, body, references, an example or an
  explanation — is an edge from it to that skill, so it is declared and points the way the flow
  runs. A description that identifies a skill is the same reference as its name: "a review pass
  calls it", "the task's ledger processing" or "the Studio skill" is that skill named in other
  words. A skill never refers to a skill that runs it: not its caller, not a coordinator it returns
  to, not a workflow it serves. A collaborator it invokes, reads or hands work to and finds at run time
  by its role, through the skill listing or a declared dependency that reads it, as the bullet on a
  repository-specific collaborator says, is named by that role, never as a particular skill. A role its caller fills is still
  a caller reference. It may state what its invocation supplies in terms any caller could meet, such
  as "an invocation that names a delta reviews that delta". It states its own behavior and what it
  returns, and the caller's text says how the caller uses it. Peers that never invoke each other
  name neither; each is found from its own description. Resolve a reverse or cyclic edge at its
  owner by moving the policy to the caller or to a lower-level skill both depend on, never with
  flags, copied policy, a call hidden in a reference, or a name dropped while the policy read stays.
  A `/name` command the skill tells the user they can run is not a reference: the user runs it, the
  skill does not, so it is no dependency and no cycle. The command form is for that alone.
  This skill's source check refuses a dependency cycle and an undeclared skill it finds named in a
  package's Markdown, skipping the packages `external_resources.json` refreshes from upstream. It
  matches name forms only, so a description, a `/name` command and a declared edge back toward a
  caller pass it, and passing it never meets this bullet.
- **A skill restricted to user invocation is never an automatic dependency.** A directly
  user-invoked workflow may delegate such an action only when its contract explicitly authorizes
  that action and bounds its targets, and the restricted action's own entry point recognizes
  that delegation. Declare it in the workflow's dependencies. This authority lasts only for that
  invocation; discovery, an ordinary task, a prior run, or an automatic caller supplies none.
  Otherwise move any shared steps into a model-invokable skill both may depend on rather than
  bypassing the restriction. Naming a user-only skill or suggesting the user invoke it is not
  delegation or authorization.
- Invoke dependent skills only from the owning `SKILL.md`. References and other supporting files are passive and must not invoke skills or identify dependencies through relative paths to another `SKILL.md`.

### Decisions

- **A skill sends a decision to the user only when it is the user's**: a product, scope, security, disclosure or authorization choice, as
  `pre-production`'s **Product Choices** defines one, or a step only the user can take. Every other contested
  call a workflow's own checks cannot settle — a disputed finding, a flag that survives its
  repairs, a stuck review, the disposition of a change that keeps failing — goes to `council` in
  **Ask** mode, and its ruling, by majority unless the skill sets a stricter threshold, is followed and named in the skill's result. A skill whose
  workflow does this declares `council`. A ruling never accepts a confirmed defect, an exploitable
  vulnerability or a failing required check.
- **A stop for the user that guidance could settle is a defect in that guidance.** A workflow
  pauses for the user only at a decision the bullet above makes theirs. An approval step reached
  with no open decision, a question a standing rule already answers and a confirmation of work the
  user has authorized each cost a wait and return nothing, so the text that causes one is changed
  to state the answer.

### Subagents

- **Every subagent a skill starts is usage the user pays for, so guidance starts as few as its
  purpose needs.** Before writing or changing text that launches subagents — a writer, reader,
  reviewer, grader, gate, worker or council member — state in that text how many it starts in a
  usual run and in each round, and what that count grows with. Prefer one agent serving a batch over
  one per item, a fresh agent only where independence requires one, and a rerun only of what a
  change touched; a count that grows with items, findings or files names its cap. Text that tells a
  reader to delegate says what the delegation buys — independent work run side by side, a reviewer
  who has not seen the author's reasoning, or bulky output kept out of the caller's context — and
  when the work is done directly instead, such as a read of one file; a second agent given the
  same task returns no better answer than the first. An edit that
  raises a workflow's usual subagent count says so, with its reason, in its pull request
  description, and a review of the edit judges that count as part of the change.

### Flows

A flow is what a skill's text makes agents do from a request to its result: the steps, launches,
reviews, gates, rounds and stops. Guidance that defines one is held to these, beside **Subagents**
and **Decisions**.

- **A delivery is sized to its change.** Text that sets the reviews, gates, rounds and tests a
  change passes branches on the size or kind of change, so a one-sentence correction does not pay
  what a new workflow pays, and no change takes far longer to deliver than it warrants.
- **Nothing is read or run twice for one answer.** Each of these is a finding in the text that
  causes it: one diff or document read by several agents for criteria that overlap, in one skill
  or across a caller and the skills it runs; a gate, review or round that reruns everything where
  only a delta changed; a step repeated on a head, diff or input unchanged since it last ran.
- **A flow that writes code or guidance searches for an existing owner or implementation before
  it writes**, and records what it searched and found, so a reviewer checks the search instead of
  trusting that one happened.
- **Every route to a flow's done, report or merge state passes an independent review of the
  change.** A branch that shortens the delivery for a class of change names the review that still
  covers that class.

### Output

Prefer an `## Output` section holding a hard-coded format whenever two correct runs
should return the same shape, whether a user reads the result or another agent or workflow consumes
it. Choose the format the consumer needs: YAML or JSON for structured state, Markdown for a report,
or a fixed sentence for a verdict. Define its fields or headings, order, and empty case in one
template; record-specific facts belong inside that structure rather than a section per kind of
thing returned. Keep procedure in the workflow and the output contract in Output.

Output is the last section unless Guardrails is present, in which case Output immediately precedes
it.

For user-facing responses, the template names the facts the response carries and puts per-item
detail past five items in a file sent with the response; a word limit it sets binds only while `i-have-adhd` is active. A skill whose result is
edits, a merge, a deployment, or a running system carries the report line its delivery step owes,
not a forced template for the execution result. Decide from what the skill returns, and leave out
a template where correct results genuinely vary in shape.

### Routers

- **A skill whose guidance differs by one attribute of the task routes to a reference per value.**
  The attribute is something the task in hand has one value of, such as a platform, a provider or a
  framework. Guidance true for only some values goes to a folder named for the attribute in the
  plural, `references/<attributes>/<value>.md` such as `references/platforms/ios.md`, so a reader
  loads only the variant that applies and a rule meant for one value is never applied to all.
  Guidance true for every value stays in `SKILL.md`, and guidance repeated across variant files
  moves up to it, narrowed to name the values it covers when it does not hold for all.
- Add the router with the first variant file: a `## <Attribute> Router` section in `SKILL.md` that
  says how to tell the task's value, a table of each value and its linked file, and what a reader
  does when no file matches (follow `SKILL.md` alone) or the task spans several values (read each).
  A new variant file adds its row in the same change; a file no row links is unreachable.
- A variant specializes `SKILL.md` and never contradicts it. Where a variant needs the opposite,
  narrow the shared statement to name that exception.
- Use no router when the variants differ in workflow rather than content, which is two routes as the
  skill-shape bullet says, or when a few lines in `SKILL.md` cover every value.

## Writing

- A skill may restate an ambient rule when it helps the reader act at the point of use; this does
  not license a second copy of a decision boundary owned by a skill that necessarily runs.
- If target file does not exist, create it with a concise structure matching existing style.
- Group frontmatter fields by subject. Put a field that summarizes, qualifies, or overrides
  another immediately after the field it relates to, unless the format requires another order.
  Place new body guidance under the broadest existing subject section that fits.
- A heading names the subject a reader looks under — Comments, Commits, Workflows — never the
  requirement it holds. Add a section only when no existing one covers the subject, and name it
  for the whole subject: a heading that states one rule invites the next rule on that subject
  into a heading of its own. A restriction on one subject goes under that subject's heading;
  `## Guardrails`, always the last section when present, holds only constraints that span the
  file's subjects.
- **A section, subsection or bullet, added, moved or reordered, goes where its reader needs it,
  never beside the text it most resembles.** Read the file's existing order first. Guidance every
  reader of the file needs comes before guidance only some cases need, and each part follows the
  parts whose terms it uses. In a style guide, a section on footnotes, which only some documents
  use, follows the sections on headings and paragraphs that every document uses, even though
  footnotes extend paragraphs. In a skill, sections come in the order a run needs them: the first
  decision before the procedure, and the common path before its edge cases.
- Express each independent requirement once, as one concise statement or bullet, without padding. Merge overlapping or synonymous guidance without losing distinct criteria or exceptions.
- **A file's size budget follows how it loads.** A change that pushes a file past its budget, or
  grows one already past it, makes its room in the same change by merging what the file states
  twice or moving text to the reference or file that owns it.
  - **A file loaded in every session has a budget of 200 lines**, the figure a vendor publishes
    for one: `.agents/global.md`, a rule with `alwaysApply: true`, and any other file a host loads
    before a task is known. Every line there takes attention on every task, and adherence to the
    whole file falls as it grows. The generated rules file a host concatenates is measured against
    that host's own cap.
  - **A skill's `SKILL.md` has a budget of 500 lines**, the skill-body target hosts publish, with
    about 5,000 tokens as the figure an audit measures beside it, since a file written one
    paragraph per line passes a line count while costing several times the tokens.
  - **A path-scoped rule has a budget of 500 lines.** It loads only with the files its patterns
    match, and the vendors publish no figure for one, so the repository holds it to the budget of
    the other file a reader takes whole. Rules whose patterns match the same file load together,
    and an audit reports their total.
  - **A reference has no line budget.** One past 100 lines opens with a contents list, and
    `SKILL.md` says when to read it.
  - **A budget is a ceiling, not a target.** A file under it is still too long when its length is out
    of proportion to what it does: cut every sentence whose removal leaves a reader's actions
    unchanged, however far under budget the file sits, judging a cut as the vendor rubric's
    **Cutting A Passage** says.
- **A correction restructures the bullet it lands in, never appends to it.** A bullet that already
  carries an exception, or runs past about twelve lines, takes no further clause: state its rule in
  one sentence and move each condition and exception into a sub-bullet or a bullet of its own, so
  the main rule stays findable. Several narrow cases that share a reason are replaced by that
  reason, stated once.
- **An absolute carries its scope, its exception and its reason in the same bullet, or is written
  as the action to take.** Text that says never, always or only is applied exactly as written,
  including to a step the user approved, so it names the case it covers, and any passage elsewhere
  that requires the opposite in some case is named there as the exception. Where the reader should
  stay responsible for a step, the bullet says what to do before it, such as checking that a
  backup exists before dropping a table, in place of forbidding the step.
- **A requirement states the result wanted and its reason; a prohibition is kept where it does
  work a positive statement cannot.** The vendor rubric's **How A Passage Is Judged** says which
  prohibitions those are, and a new one is written to pass it.
- **Guidance states what holds now, in plain weight.** It never says what changed, as in "now",
  "no longer", "legacy" or a past-tense account of a run, and it marks importance with a reason,
  never with capitals or with words such as "critical" and "do not skip". A bold lead names a
  bullet's subject so the bullet can be found and cited; it is a label, and a file whose bullets
  mostly open with a bold prohibition has spent it as emphasis.
- **Everything guidance cites resolves where it says.** A cited `**Section**`, a path, a script, a
  command, a flag and what a command prints each exist under that name in the file or tool named.
  Cite a section by its name, never by a step number, which moves with the next edit, and resolve a
  skill's own script from the skill's directory, never from a repository path.
- Normalize the touched file's nearby structure when needed: combine narrow sections and remove redundant wording.
- **State the class the user plainly meant, no narrower and no broader; the request's shape is
  its example.** A request arrives as one symptom, and the rule it needs names the class that
  symptom belongs to, with the symptom's shape kept as one illustration of it.
  - **No narrower.** A rule written for the symptom is silent on the next one, and the next one is
    what it will be read for. Asked for `Final` on string constants, write `Final` for every
    module-level constant; asked for a walkthrough rule because a page reloaded in a loop once a
    back-end change was absent, write that the run is judged against intended behavior because an
    API error surfaces as any unintended behavior, and name the loop only as one instance. A named
    field, file, section, document kind, tool, or step, including the place a request says to put
    the fix, is an example of its class and a candidate home for the edit's owner search, never
    the limit of the rule, unless the contract requires its exact identity.
  - **No broader.** The class ends where the user's words stop being about it. Name the nearest
    case outside it, the one a broader reading would change, and confirm the draft leaves it as it
    was: the `Final` rule reaches every module-level constant and stops before a function's local
    names, which nobody raised. A neighboring subject, a requirement the case never needed, and a
    change the user would not expect from their own words stay out of the draft and are put to
    the user.
  - **Every instruction that does the same work, and none that does other work.** Apply the
    decision to each instruction in the file that does the same work: one section rewritten while
    a neighbor still does the narrow thing is the draft half done.
  - **Handed wording is input, not the spec.** Rule text in the request or in a delegating agent's
    brief is drafted again against the invariant and alternate routes the edit's failure-class
    diagnosis supplies. An agent delegating an edit passes the class, its outer edge and the
    evidence, not finished rule text for one case.
  - **The illustration never carries the incident's own vocabulary** in shared guidance — the
    labels, headings, records, screens or values of the product that prompted it, however ordinary
    they read: a label lifted from the screen under review is that screen's copy. Retell it with
    invented nouns from an unrelated domain, as **Where Guidance Lives** requires, and replace any
    such noun already in the section the edit touches.
- Describe reusable roles, boundaries, and decision criteria generically even in
  repository-focused guidance when the pattern is not repository-specific.
- Guidance states a transferable decision or procedure. Incident dates, machine inventories,
  project identities, test outcomes, and recovery diaries belong in project records or verification
  evidence. Renaming a product or moving its anecdote to a reference does not make it generic.
- Generalization preserves operational knowledge: applicability, prerequisites, action order,
  success checks, and relevant recovery or stopping conditions. Stable commands and API names are
  useful detail; replace environment-specific values with configuration or placeholders. “Inspect
  and retry” is not a substitute for a known procedure. Evidence records keep the incident;
  the skill or its linked owner keeps the reusable lesson.
  Linking an API reference preserves syntax, but the procedure must still say which operation or
  options apply and how to check the result.
- When generalizing or shortening guidance, account for each useful instruction removed: retain
  it as a reusable procedure, link its owning guidance, or establish why it no longer applies.
  Check that the next reader can still perform the action and recognize success; removing the
  incident details must not remove the lesson. Apply the preservation criteria above.
- A concrete platform constraint belongs only when it changes the procedure. State its applicable
  boundary and source; keep observed symptoms separate from proven causes and avoid inferring a
  universal rule from one run. Configuration supplies environment-specific values.
- An example earns space only when it explains a non-obvious distinction. It must not make the rule
  depend on recognizing that exact example; check that another member of the same class is covered.
  A reader copies an example's length, tone and structure, so a rule that needs one takes two of
  different kinds over one, and none of them is the incident that prompted the rule.
- When the user asks to add guidance from another repository, treat that repository as source material: encode transferable requirements in the owning skills and refer to those skills by name. Before delivery, audit the edited package for the source repository's name, links, paths, commands, versions, and configuration; never hard-code or cite that repository in a skill.
- Separate temporary task, session, and pull-request directions from lasting guidance before
  writing. Apply the former to the current work only; never encode them as canonical rules or
  skills. A direction about what the product holds now, such as which recipes a cookbook includes,
  what each plan costs or which accounts get a discount, is one of them even when the user gives a
  reason: it changes the product's data, and guidance keeps describing how the product works, since
  its contents will change as it grows.

## Scripts

- Write new or substantially rewritten skill helper scripts in Python by default. Use another language when the execution platform requires it, such as browser JavaScript, and state that constraint. Keep executable helpers inside the owning skill's `scripts/` directory, resolve supporting files relative to the skill package, and take private endpoints, credentials, and environment-specific values from private configuration rather than committed source.
- Do not add committed tests for skills or their helper scripts, inside or outside the skill directory. Keep any needed execution checks temporary and untracked.

## Validation

- A pull request confined to canonical agent configuration and generated provider mirrors contains
  no application or package behavior change. Validate the Markdown, the synchronization contract,
  and the checks a changed skill script or hook owns, such as its type check, a test render or the
  per-harness verification **Harnesses** requires; do not run application suites or gate the pull
  request on them.
- Keep CI change-detection paths scoped to application, package, dependency, test, or runtime files
  so an agent-configuration-only pull request selects no application test job.
- The exemption applies to the complete pull request, not individual files. If a pull request also
  changes application code, package source, dependencies, tests, runtime configuration, or CI
  behavior, run its normal validation.
- For a dependency change, inspect the declared graph and the actual invocation and policy-read
  paths together. Check names-only entries, target discovery descriptions, body call arguments,
  undeclared invocations, and cycles. A names-only manifest or an acyclic declared graph alone
  does not establish that the workflow is acyclic or that its required work remains reachable.
