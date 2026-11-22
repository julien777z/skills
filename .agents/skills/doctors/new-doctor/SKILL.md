---
name: new-doctor
description: Create a doctor skill on the shared doctor-protocol for one class of repository hygiene. Takes the name of the doctor to add. Run only when the user asks for it.
short_description: 'Create a doctor skill on the shared doctor-protocol for one class of repository hygiene.'
---

# New Doctor

A doctor is a skill that audits one hygiene class on `doctor-protocol` and owns nothing the
protocol already does. Read the protocol first to apply its authoring contract; creating a doctor
does not start a doctor audit.

## Dependencies
- `doctor-protocol`
- `get-doctors`
- `edit-skill`
- `execute-task`

## Workflow

1. **Name it** `<domain>-doctor`, the domain being the hygiene class in one word. Run
   `get-doctors`; a class an existing doctor covers becomes a lens on that doctor, not a new skill.
2. **Show the class is real.** From the current tree or the user's example, show the defect recurs
   and is mechanical enough to check on every run. A class a linter, type checker, or test already
   enforces gets no doctor; a lens over such a class verifies the enforcement still runs rather
   than re-implementing it.
3. **Write what the protocol says a doctor owns**, in this order after the title and a
   one-sentence lead:
   - `## Dependencies`: `doctor-protocol` first, then the generic skills whose policy it applies,
     then any repository-specific skill referred to by role.
   - `## Inventory`, opening with the instruction to run `doctor-protocol`. It names what is
     enumerated and what is excluded; the mechanical commands whose output lists candidates, by
     kind and found in the repository's configuration at runtime; and the before-and-after
     measures, each a count one of those commands produces. A **Shared index.** paragraph names
     what the doctor reads from the index `doctor-protocol`'s **Share The Index** keeps and the
     tables it writes there, in one or two sentences.
   - `## Lenses`, one `###` per lens, each stating six things: the defect shape; the evidence that
     establishes it; the remedy; the checks that find every instance, never only the first one
     noticed; what is left alone, so a reviewer does not go hunting; and whether the lens is
     whole-repository, judged only across partitions, or judged within one file or area.
   - `## Reviewers`: one opening sentence citing the cap `doctor-protocol`'s **Launches** sets, a
     lower cap only where the domain needs one, and what dictates the partition cut, then what the
     cross-cutting reviewer compares and what the final reviewer challenges.
   - `## Dispositions`, in order, naming the calls this domain raises, each decided by the run as
     `doctor-protocol`'s **Gate And Show The Plan** says.
   - `## Report Additions`.

   A decision a dependency already settles — breaking an owned contract, what stored data owes,
   what stays reserved to the user — is cited by its section in Dispositions, never restated
   or reclassified. Nothing that restates a protocol section takes a heading or a paragraph,
   launch counts included. Declare no delivery cadence: the protocol's **Deliver** leaves the run's
   pull requests draft for the user.
4. **Keep it generic.** Discover layouts, tools, frameworks, and budgets at runtime. Never name the
   current repository's paths, packages, products, commands, or thresholds. State a default
   threshold as one the repository's configuration overrides. Refer to a repository-specific skill
   by role — "the repository's test-runner skill when the skill listing declares one, found by its
   description" — never by name.
5. **Write the frontmatter.** `name` equals the directory. The description's first sentence is the
   summary `get-doctors` quotes, so it stands alone; its last sentence says when to use the skill.
6. **Validate.** Grep the file for repository-specific names; confirm every dependency names an
   existing skill; check the entrypoint against `doctor-protocol`'s **Declare What The Doctor Owns**;
   confirm no heading restates a protocol section; run `get-doctors` and see the new doctor listed
   with the intended summary.
7. **Prepare its skill test** as the section below states.
8. **Deliver** through `edit-skill`, whose one skill-test round is the doctor's test, and rewrite
   any lens a reader missed. The GitHub rule's **Merge Authorization** holds a pull request that
   adds a doctor for the user's review; the report hands the user its link.

## Skill Test The Doctor

A lens is only as good as what a reviewer reading it finds, so each lens is proved against a
violation its reader has not been told about. The doctor is tested once: this section says what
the skill-test round of `edit-skill`'s **Guidance Delivery** is given, and starts no round of its
own.

- **Scenarios.** One per lens, and one for the clean control tree. Each reader gets the doctor's
  `SKILL.md`, the skills it depends on, one target tree, and the instruction to run the audit
  phase only: inventory the target, apply every lens, and return findings anchored to file and
  line, each naming the lens and the remedy. No plan, no gate, no edits, and never the expected
  findings.
- **Who writes and judges.** The round's scenario writer, never the doctor's author, picks or
  builds the targets and writes the sealed expectations below, and the round's grader judges each
  reader's findings against them.
- **Targets.** For each lens, first a real example: a place in the current repository where the
  shape exists today, handed to the reader as a bounded scope. Where the
  repository has no live example, or the class is one the user described that has not happened
  yet, write a scratch tree outside the repository that plants exactly one violation per uncovered
  lens. The clean control tree follows every convention and holds at least one near miss —
  a legitimate pattern that resembles a violation, such as a class-scoped fixture or a trivial
  predicate helper. Scratch trees are never committed.
- **Sealed expectations.** Before the readers start, the expected findings for every target —
  lens, location, remedy — are written and kept from them.
- **Pass.** Every planted or real violation is reported under the right lens with the remedy the
  doctor's dispositions state; the control produces no finding; the near miss is not flagged.
- **A miss or a false positive is a defect in the lens text, never in the reader.** Rewrite the
  lens's defect shape, evidence, checks, or remedy, and the round reruns that scenario on a fresh
  reader, within the limit of 3 review rounds per change that `execute-task`'s review-rounds
  reference sets; a lens that fails its third round gets that reference's disposition. Never fix
  a miss by hinting the reader, and never narrow the target to what the reader already found.
- **Launches.** The round's own: its scenario writer, one reader per scenario, the control
  readers it requires for a new skill, and its grader, so the count grows only with the lenses.
- **Report** per doctor: the lenses exercised, real and invented targets, the model used, each miss
  and the rewrite it produced, and each false positive. A later edit to a lens re-runs its
  scenario.
