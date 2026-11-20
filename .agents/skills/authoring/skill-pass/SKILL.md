---
name: skill-pass
description: 'How agent guidance under `.agents` is written, placed and checked — the criteria and the source check for a skill, rule, agent definition, hook, setting, reference or project guidance. Read when writing, editing, reviewing or auditing guidance, for where a requirement lives among the global rules, a rule file and a skill; frontmatter descriptions; skill dependencies and their declaration; conflicting instructions; citations that must resolve; size budgets; harness support; subagent counts; output sections; routers; prose duplication; validating guidance; and how a reviewer or gate of a guidance diff is briefed. It starts no subagents.'
short_description: 'Apply the writing, placement, conflict and source checks to agent guidance.'
---

# Skill Pass

The criteria guidance is held to, and the one mechanical check beside them. Whoever writes, edits,
reviews or audits guidance reads this skill and applies it in process: it starts no subagents, opens
no pull request and delivers nothing. An invocation names what it covers — a delta, a set of files
or the whole canonical tree — and the pass runs over that.

## Dependencies
- `pre-production`
- `council`
- `i-have-adhd`
- `code-simplify`

## The Pass

Run the steps in order over what the invocation names. The
[authoring reference](references/authoring.md) holds the criteria steps 2 and 4 to 7 apply, and the
[conflict criteria](references/conflicting-instructions.md) hold step 3's.

1. **Source check.** Run it as **Source Check** says and fix or record every report before reading
   further, so no read is spent on what a script finds.
2. **Writing.** Hold each instruction and example to the authoring reference's **Writing**, and to
   each other section the file's kind and content fall under: **Rules** for a rule file;
   **Package And References**, **Decisions**, **Subagents**, **Output** and **Routers** for a skill;
   **Scripts** for a helper script; and **Harnesses** for anything a harness runs or reads.
3. **Conflicts.** Apply **Conflict Check**.
4. **Placement.** Test each requirement against the authoring reference's **Where Guidance Lives**:
   name the skill that runs when the requirement applies before accepting it in a rule file or
   `.agents/global.md`, check what the owning file's name and description bound, and confirm no rule
   file or `.agents/global.md` names an individual skill outside the one place that reference
   allows.
5. **Description as the index.** For every subject a skill owns, confirm a clause of its frontmatter
   description names it, and judge the description as the authoring reference's **Descriptions**
   says. An index of owners kept in a rule file, `.agents/global.md` or a table is a finding.
6. **Budgets.** Count the lines of every `SKILL.md` and rule file covered against the size budget
   **Writing** sets, and judge each launch of subagents against **Subagents**: a stated usual
   count, what it grows with, and a cap.
7. **Dependencies.** Apply **Dependency Audit**.

A skill-test round is not part of the pass. Exercising guidance against tasks belongs to the
delivery of changed guidance, covers only what that delivery changed, and is never run across
standing guidance because a pass read it.

## Source Check

Run `scripts/validate_sources.py check`, resolved from this skill's directory, from the root of the
repository being checked, with that repository's own interpreter or any interpreter meeting the
sync tool's version. It covers the whole canonical tree whatever the pass covers, imported skills
included, so a clean changed file does not make a failing tree pass.

- **What it refuses.** It installs the sync tool at the revision the repository's workflow pins and
  mirrors the canonical tree into a scratch copy, so what its mirror refuses is exactly what the
  workflow would; a frontmatter description holding a colon followed by a space is the usual
  report, and quoting the value is the fix. It refuses a skill named in a package's Markdown
  without being declared, and a cycle among declared dependencies. It refuses a relative link whose
  file or anchor is missing, a section cited as a skill's or a rule's `**Section**` that the cited
  skill's entry point and references, or the cited rule, do not hold, and a rule file named that
  does not exist.
- **What it leaves to reading.** It matches name forms only, so a skill identified by a
  description, a declared edge that points back toward a caller, a cited path outside a link, a
  script, a command, a flag and what a command prints all pass it. For each file the pass covers,
  check by reading and searching that every one of those resolves, as **Writing** requires, that no
  ruling or example disagrees with a file that loads beside it, and that the file is within its
  budget.
- Generated mirrors are left to Agent Sync and are never read or repaired by this check.

## Conflict Check

Validate every instruction and example the pass covers for conflicts. Search the canonical rules
and skills by the instruction's subject, its required action and the opposite disposition, never by
its words. Read the complete skill or rule and its supporting files, every file that loads alongside
it, and the relevant sections of other skills, rules, callers and dependencies, then apply the
[conflict criteria](references/conflicting-instructions.md), which also name the authoring
reference's bullets each instruction is held to.

Resolve competing instructions at their owners rather than adding a reminder beside them. Where a
new instruction conflicts with standing guidance nobody asked to change, the new instruction is
fitted to the standing one. Record the searches, the sources read and each resolution, or the
evidence for a clean result. A later wording change is checked again: an earlier clean result does
not cover a new edit.

## Dependency Audit

For each skill the pass covers, read its complete package and its affected callers, every file a
folded or incorporated change brings in included. List every skill each one refers to, by name or by
a description that identifies it, and compare the list with the owning entry point's
`## Dependencies`. Resolve every reverse, peer, missing, stale or path-based reference, and any
user-only dependency lacking explicit bounded delegation, as the authoring reference's
**Dependencies** says, and check a dependency change as its **Validation** section says. Check
references separately for hidden invocations and cross-skill filesystem links. **Source Check**
matches name forms only, so a passing check never replaces this audit.

## Prose Duplication

Prose duplicates as readily as code, and no mechanical check catches it. Read every file the pass covers whole, a one-line rule edit as much as a new skill,
for these shapes:

- guidance duplicated between peer rules or skills, a caller and a skill it always invokes
  included, or between two files of one skill;
- a section grown around a second subject;
- a heading named for a category with one member;
- a rubric left inline that the authoring reference's skill shape sends to a reference;
- a single bullet added to a file that does not own its subject, the duplication least likely to be
  looked at twice.

## Reviewer Brief

A reviewer or gate judging guidance is handed this skill and reads the authoring reference whole,
since nothing loads it for a reader of `.agents` files. Its brief asks:

- whether the guidance holds at the breadth the authoring reference's **Writing** asks for, and no
  broader: a rule written for one symptom is a finding, and so is a requirement its case never
  needed, a neighboring subject swept in, or an absolute applied past the cases its reason covers;
- whether every mechanism it adds earns its place;
- whether generic guidance names a tool, surface or workaround its contract does not depend on,
  which is a finding.

For a diff written to answer a request, the brief also carries the request's intent, the real case
behind it, and the incident's vocabulary — the product, its record and page nouns, the labels the
request quoted — so an example carrying any of it is a finding, and the incident's route must not
narrow the durable decision boundary. For standing guidance read with no request, the reviewer
judges breadth from the text itself and its neighbors.

## Output

Return findings in this shape, one block per finding, or the single line `Skill pass: clean` with
the scope it covered:

```markdown
Skill pass: <scope covered>

- <path>:<line> — <step of the pass> — <what the text says, and the criterion it misses, cited as the authoring reference's **Section** or the conflict criteria>
  Remedy: <the change at the owning file>
```
