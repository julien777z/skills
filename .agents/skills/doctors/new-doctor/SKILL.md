---
name: new-doctor
description: Create a doctor skill on the shared doctor-protocol for one class of repository hygiene. Takes the name of the doctor to add.
disable-model-invocation: true
---

# New Doctor

A doctor is a skill that audits one hygiene class on `doctor-protocol` and owns nothing the
protocol already does. Read the protocol first: it is the contract a new doctor is written against,
not a dependency this skill runs, so it is named here and not below.

## Dependencies

- `subagent-selection` — select the standard tier for doctor smoke reviewers.
- `get-doctors` — the doctors that already exist.
- `edit-skill` — deliver the new skill: its branch, its `code-simplify` pass, and its
  agent-configuration-only pull request, left open for the user.

## Workflow

1. **Name it** `<domain>-doctor`, the domain being the hygiene class in one word. Run
   `get-doctors`; a class an existing doctor covers becomes a lens on that doctor, not a new skill.
2. **Show the class is real.** From the current tree or the user's example, show the defect recurs
   and is mechanical enough to check on every run. A class a linter, type checker, or test already
   enforces gets no doctor; a lens over such a class verifies the enforcement still runs rather
   than re-implementing it.
3. **Write the five things** the protocol says a doctor owns, in this order after the title and a
   one-sentence lead: `## Dependencies` (`doctor-protocol` first, then the generic skills whose
   policy it applies, then any repository-specific skill referred to by role); `## Inventory`,
   naming any measurement the protocol takes once before fan-out; `## Lenses`, one `###` per lens
   stating the defect shape, the evidence that establishes it, and the remedy; `## Dispositions`,
   in order, naming which outcomes are the user's decision and what the cross-cutting reviewer
   compares; `## Report Additions`. A reviewer partition the domain dictates may take its own
   heading; nothing that restates a protocol section may.
4. **Keep it generic.** Discover layouts, tools, frameworks, and budgets at runtime. Never name the
   current repository's paths, packages, products, commands, or thresholds. State a default
   threshold as one the repository's configuration overrides. Refer to a repository-specific skill
   by role — "the repository's test-runner skill when the skill listing declares one, found by its
   description" — never by name.
5. **Write the frontmatter.** `name` equals the directory. The description's first sentence is the
   summary `get-doctors` quotes, so it stands alone; its last sentence says when to use the skill.
6. **Validate.** Grep the file for repository-specific names; confirm every dependency names an
   existing skill; confirm no heading restates a protocol section; run `get-doctors` and see the
   new doctor listed with the intended summary.
7. **Smoke-test it** as the section below states, and rewrite any lens a reviewer missed.
8. **Deliver** through `edit-skill`.

## Smoke Test The Doctor

A lens is only as good as what a reviewer reading it finds. Before delivery, prove each lens
against a violation a reviewer has not been told about.

- **Who reviews.** Invoke `subagent-selection` and use its **standard** tier for read-only
  reviewers, following its dispatch and unavailable-model policy. Record the resolved model
  each reviewer actually ran on.
- **What each reviewer gets.** The doctor's `SKILL.md`, the skills it depends on, one target tree,
  and the instruction to run the audit phase only: inventory the target, apply every lens, and
  return findings anchored to file and line, each naming the lens and the remedy. No plan, no
  gate, no edits, and never the expected findings.
- **Targets.** For each lens, first a real example: a place in the current repository where the
  shape exists today, found by the author and handed to the reviewer as a bounded scope. Where the
  repository has no live example, or the class is one the user described that has not happened
  yet, write a scratch tree outside the repository that plants exactly one violation per uncovered
  lens, beside one clean control tree that follows every convention and at least one near miss —
  a legitimate pattern that resembles a violation, such as a class-scoped fixture or a trivial
  predicate helper. Scratch trees are never committed.
- **Sealed expectations.** Before launching, write the expected findings for every target — lens,
  location, remedy — and keep them from the reviewers.
- **Pass.** Every planted or real violation is reported under the right lens with the remedy the
  doctor's dispositions state; the control produces no finding; the near miss is not flagged.
- **A miss or a false positive is a defect in the lens text, never in the reviewer.** Rewrite the
  lens's defect shape, evidence, or remedy, then re-run that target on a fresh reviewer; repeat
  until it passes. Never fix a miss by hinting the reviewer, and never narrow the target to what
  the reviewer already found.
- **Report** per doctor: the lenses exercised, real and invented targets, the model used, each miss
  and the rewrite it produced, and each false positive. A later edit to a lens re-runs its target.
