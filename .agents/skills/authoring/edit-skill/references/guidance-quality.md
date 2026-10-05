# Guidance quality

These criteria apply to the entire skill package: its entry point, references, scripts, templates,
and examples. A supporting file is part of the skill, not an exemption from its ownership or scope.

## Reusable scope

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
- A concrete platform constraint belongs only when it changes the procedure. State its applicable
  boundary and source; keep observed symptoms separate from proven causes and avoid inferring a
  universal rule from one run. Configuration supplies environment-specific values.
- An example earns space only when it explains a non-obvious distinction. It must not make the rule
  depend on recognizing that exact example; check that another member of the same class is covered.

## Entry point and references

- Critical decisions and when to load a reference are visible in `SKILL.md`. A reader following the
  entry point reaches all guidance needed for the selected route before acting.
- Each reference has a descriptive subject, a resolved link, and a clear role within its owning
  skill. User-facing explanations identify it as that skill's reference and describe its purpose;
  a bare filename must not sound like an unexplained skill, mode, or prerequisite.
- References carry supporting criteria and technical procedures. Moving text into one is not a fix for
  overly specific guidance, duplication, unsupported claims, or an unclear ownership boundary.

## Shape, description, and output

**Skill shape.** `SKILL.md` holds how the skill runs: its trigger, its dependencies, its
workflow, its output, its guardrails. What a reader *applies* rather than *follows* lives in
`references/<topic>.md` beside it, named for what it holds — a rubric, a checklist, a catalogue,
a protocol — and `SKILL.md` names the file at the point the workflow reads it. A skill with two
routes through it (two modes, two kinds of target, two hosts) keeps the shared workflow in
`SKILL.md` and gives each route its own reference, so the file a reader loads first stays short
enough to be read whole. References may explain the technical steps for a route selected by the
entry point. They do not select the top-level workflow, hide a decision gate, declare a dependency,
or invoke another skill. Scripts the skill runs go under `scripts/`; supporting files may live
under `assets/`, `resources/`, or another directory named for their role. Keep only files the skill
needs. Provider metadata such as `agents/openai.yaml` stays outside repositories and is never
propagated.

**Description.** The front-matter `description` is read on every turn, for every skill, to decide
whether this one fires. It has two jobs. The first is to state **when** — the situations that
should reach it, in the words a task actually arrives in. The second is to carry any rule that must
bind before the body is read, since a reader often acts on the description first. What the skill
does belongs there only so far as a reader needs it to recognise those situations; the body says
the rest.

So the slash command earns no space. It is the skill's own name, the listing already shows it, and
a reader deciding whether to invoke has it in hand — `Invoke as /refactor to refactor a
repository` spends its opening clause telling the reader something they used to get here. Keep the
trigger and drop the command: `Use to refactor a repository, change request, branch, path, symbol,
or concern.` The same goes for a phrase naming the skill, `Use this skill to`, and a restatement of
the skill's title.

Where an invocation carries an argument the trigger depends on, the argument is the thing worth
naming — a target, a scope, a mode — not the command that precedes it.

Judge a description by substitution: read it without knowing which skill it belongs to. If it still
says which situations fire the skill, it works. If the remainder names no situation, it was never a
trigger.

**Output.** Prefer an `## Output` section holding a hard-coded format whenever two correct runs
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
