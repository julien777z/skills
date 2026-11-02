---
description: Apply when writing, creating, or editing agent guidance — skills, rules, agent definitions, and project guidance.
alwaysApply: false
paths:
- '.agents/**'
- '**/SKILL.md'
---

# Agent Guidance Rules

## Where Guidance Lives

- `.agents/global.md` states guidance that holds in every repository, and every `.agents/rules/*.md`
  file guidance that holds in any repository using its technology. Keep their examples generic —
  invented names and placeholder shapes, never this repository's modules, helpers, packages, paths,
  or domain vocabulary, and never the product, tool, or platform whose incident prompted the change.
- `.agents/project.md` is the home for repository-specific guidance: its base classes, helpers,
  packages, layout, documentation structure, inventories, and generated sections.
- Repository facts only some work needs — a local stack, test accounts, deployment targets, a
  migration layout — go in `.agents/references/<name>.md`, named for their content and read on
  demand, and `.agents/project.md` points to each file in one line.
- A rule that cannot be stated without naming something this repository owns belongs in
  `.agents/project.md`. Move it there rather than rewording it into something generic but untrue.
- **Shared or repository-owned.** Generic skills live in one shared skills repository and reach
  every session through a user-level skill root; repository-specific skills, every rule, and
  repository-specific agents live in the repository they describe. Inspect a skill's content and
  dependencies to decide ownership, including for an existing skill: a user-level symlink shows
  where it is installed, not where it belongs. A new or existing skill goes to the skills
  repository only when it reads generically without losing required behavior. If making it
  generic would remove or misstate guidance it needs to give, put it in the repository it
  describes under `.agents/skills/`, at any depth; move a misplaced existing skill there.
  **Guidance whose correctness depends on a current repository's product, resources, topology, contracts, configuration, or relationships is project guidance.** It belongs in that repository's `.agents/project.md` or a repository-specific skill, regardless of the subject that exposed the gap. A shared skill may teach the classification procedure, but never carry a current repository's facts or boundaries.
  An agent definition that a shared skill runs on goes with that skill; every other agent, and
  every rule, is repository-owned.
- **A skill that reads generically belongs to every repository, so write it that way and put it in the skills repository.** Repository paths, product names, and domain nouns turn a reusable workflow into one repository's copy of it; keep them out unless the skill's correctness depends on that local contract, and where a skill genuinely needs one local fact, take it from the repository's project guidance or a setting rather than baking it in. Where a shared skill needs a repository-specific collaborator — a migrations skill, a finalization skill, a deployment skill, a deferral label — it names the role and finds the skill by its description in the skill listing, and the repository's `project.md` **Repository Skills** table says which local skill fills the role.
- **Generic ownership is determined by what the skill must do, not its name.** A generically named skill can depend on one repository's contract; keep that skill in the repository and its facts in project guidance. Language, platform, framework, and workflow skills that truly apply across products remain shared and read repository commands, identities, hosts, packages, and fixtures from project guidance rather than embedding them.
- **A file's name and description bound what it owns.** Before choosing a skill or rule, state
  the condition its name and description set — a release stage, a technology, a mode, a kind of
  task — and ask whether the guidance would still be true where that condition does not hold. If
  it would, that file is too narrow, however close its neighbouring section: the guidance goes to
  the file whose scope matches its own, and a global rule takes what holds everywhere. Neither
  running on every task nor already holding a related rule, such as one on required fields when
  the guidance is about required settings, makes a narrower file the owner.
- Paths inside a repository's `.agents`:
  - `agent` -> `.agents/agents/<name>.md`
  - `rule` -> `.agents/rules/<name>.md`
  - `skill` -> `.agents/skills/<name>/SKILL.md`, or `.agents/skills/<folder>/<name>/SKILL.md`
    where the repository sorts its skills into folders; the folders group the source and never
    change the name a skill installs under.
  - repository facts only some skills need -> `.agents/references/<name>.md`, as the references
    bullet above places them; Agent Sync neither mirrors nor validates them.

## Rules

- For a scoped rule, declare its file patterns once as `paths` in canonical frontmatter.
  Do not duplicate them as `globs`; Agent Sync writes each provider's required scope key.
  Use `alwaysApply: true` only when the rule belongs in every session.
- Before adding a requirement to a shared rule, test it against a repository without the feature that prompted it. If it prescribes the current repository's documentation sections, inventory, or generation workflow, put it in `.agents/project.md`; keep the shared rule limited to guidance that still makes sense elsewhere.

## Skills

### Package And References

- **Skill shape.** `SKILL.md` holds how the skill runs: its trigger, its dependencies, its
  workflow, its output, its guardrails. What a reader *applies* rather than *follows* lives in
  `references/<topic>.md` beside it, named for what it holds — a rubric, a checklist, a catalogue,
  a protocol — and `SKILL.md` names the file at the point the workflow reads it. A skill with two
  routes through it (two modes, two kinds of target, two hosts) keeps the shared workflow in
  `SKILL.md` and gives each route its own reference, so the file a reader loads first stays short
  enough to be read whole. References may explain the technical steps for a route selected by the
  entry point. They do not select the top-level workflow, hide a decision gate, declare a dependency,
  or invoke another skill. Scripts the skill runs go under `scripts/`; supporting files may live
  under `assets/`, `resources/`, or another directory named for their role. Keep only files the skill
  needs.
- Never add `agents/openai.yaml` to a repository skill. Repository skills contain `SKILL.md` and
  only supporting files required by the skill; provider UI metadata stays outside repositories
  and is never propagated.
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
does belongs there only so far as a reader needs it to recognise those situations; the body says
the rest.

So the slash command normally earns no space. It is the skill's own name, the listing normally shows
it, and a reader deciding whether to invoke has it in hand — `Invoke as /code-slop-doctor to deslop
a repository` spends its opening clause telling the reader something they used to get here. Keep the
trigger and drop the command: `Use to deslop a repository or one of its phases, lenses or paths.`
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

### Dependencies

- **Refer to a skill, and to anything inside it, by the skill's name, never by path.** `the `code-simplify` skill's rubric reference` is right; a relative path into another skill's directory is wrong, because the directories move between repositories and user-level roots and the name is the only stable handle.
- Declare every invoked skill by canonical skill name in a near-top `## Dependencies` section of the owning `SKILL.md`. That section lists skills only, never tools, plugins, scripts, references, assets, executables, or filesystem paths.
- **A skill restricted to user invocation is never an automatic dependency.** A directly
  user-invoked workflow may delegate such an action only when its contract explicitly authorizes
  that action and bounds its targets, and the restricted action's own entry point recognizes
  that delegation. Declare it in the workflow's dependencies. This authority lasts only for that
  invocation; discovery, an ordinary task, a prior run, or an automatic caller supplies none.
  Otherwise move any shared steps into a model-invokable skill both may depend on rather than
  bypassing the restriction. Naming a user-only skill or suggesting the user invoke it is not
  delegation or authorization.
- Invoke dependent skills only from the owning `SKILL.md`. References and other supporting files are passive and must not invoke skills or identify dependencies through relative paths to another `SKILL.md`.

### Output

Prefer an `## Output` section holding a hard-coded format whenever two correct runs
should return the same shape, whether a user reads the result or another agent or workflow consumes
it. Choose the format the consumer needs: YAML or JSON for structured state, Markdown for a report,
or a fixed sentence for a verdict. Define its fields or headings, order, and empty case in one
template; record-specific facts belong inside that structure rather than a section per kind of
thing returned. Keep procedure in the workflow and the output contract in Output.

Output is the last section unless Guardrails is present, in which case Output immediately precedes
it. Guardrails is always the final section; no workflow, report or reference section follows it.

For user-facing responses, the template names the facts the response carries and puts per-item
detail past five items in a file sent with the response, as the global rule **User-Facing Output**
requires; a word limit it sets binds only while `i-have-adhd` is active. A skill whose result is
edits, a merge, a deployment, or a running system carries the report line its delivery step owes,
not a forced template for the execution result. Decide from what the skill returns, and leave out
a template where correct results genuinely vary in shape.

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
- Express each independent requirement once, as one concise statement or bullet, without padding. Merge overlapping or synonymous guidance without losing distinct criteria or exceptions.
- Normalize the touched file's nearby structure when needed: combine narrow sections, remove redundant wording, and order foundational guidance before specialized concerns.
- **Prefer the broad statement, and let the request's shape be its example.** A request
  arrives as one symptom, and the rule it needs names the class that symptom belongs to; the
  symptom's shape stays as one illustration of it. In shared guidance that illustration never
  carries the incident's own vocabulary — the labels, headings, records, screens or values of
  the product that prompted it, however ordinary they read: a label lifted from the screen
  under review is that screen's copy. Retell it with invented nouns from an unrelated domain, as
  **Where Guidance Lives** requires, and replace any such noun already in the
  section the edit touches. Asked for `Final` on string constants, write `Final` for
  every module-level constant; asked for a walkthrough rule because a page reloaded in a
  loop once a back-end change was absent, write that the run is judged against intended
  behaviour because an API error surfaces as any unintended behaviour, and name the loop
  only as one instance. A rule written for the symptom is silent on the next one, and the
  next one is what it will be read for. A named field, file, section, document kind, tool,
  or step, including the place a request says to put the fix, is an example of its class and
  a candidate home under `edit-skill`'s owner search, never the limit of the rule, unless the
  contract requires its exact identity. Broaden to the class the user plainly meant, never to a
  neighbouring subject. Wording handed over — rule text in the request or in a delegating agent's
  brief — remains input, not the spec: draft against the invariant and alternate routes
  `edit-skill`'s failure-class diagnosis classified, then apply that decision to every instruction
  in the file that does the same work.
  One section rewritten while a neighbour still does the narrow thing is the draft only half
  done, and it is rewritten until the neighbour changes too. An agent delegating an edit
  passes the class and the evidence, not finished rule text for one case.
- Describe reusable roles, boundaries, and decision criteria generically even in
  repository-focused guidance when the pattern is not repository-specific. Keep concrete
  repository names only when correctness depends on that local contract.
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
- When the user asks to add guidance from another repository, treat that repository as source material: encode transferable requirements in the owning skills and refer to those skills by name. Before delivery, audit the edited package for the source repository's name, links, paths, commands, versions, and configuration; never hard-code or cite that repository in a skill.
- Separate temporary task, session, and pull-request directions from lasting guidance before
  writing. Apply the former to the current work only; never encode them as canonical rules or
  skills.
- Keep reusable skill names, instructions, scripts, and interfaces model-agnostic.
  Name a client or model only in a scoped compatibility section where its behavior genuinely
  differs. A skill states the facts an agent gathers about its own session — its transcript, its
  task list, its subagents and their records — and leaves finding them to the agent in whichever
  harness runs it; outside such a compatibility section, a script or instruction that finds those
  session facts through one harness's files, environment variables or record layout is a
  defect, never a convenience.
- Do not embed product-specific file paths or copy current application code into reusable skills; those go stale when files move or refactors land. Prefer generic placeholders (for example `services/<name>/...`), short pattern descriptions, or minimal invented examples that are not tied to live paths or current line-level code.

## Scripts

- Write new or substantially rewritten skill helper scripts in Python by default. Use another language when the execution platform requires it, such as browser JavaScript, and state that constraint. Keep executable helpers inside the owning skill's `scripts/` directory, resolve supporting files relative to the skill package, and take private endpoints, credentials, and environment-specific values from private configuration rather than committed source.
- Do not add committed tests for skills or their helper scripts, inside or outside the skill directory. Keep any needed execution checks temporary and untracked.
