# Conflicting instructions

These criteria apply to the entire skill package: its entry point, references, scripts, templates,
and examples. A supporting file is part of the skill, not an exemption from its ownership or scope.

- Compare instructions by the decisions they govern, not matching words or file proximity. For each
  changed decision, identify its applicable scope, required action, permission, refusal, exception
  and stopping condition across the relevant guidance, including unchanged instructions in the
  edited skill or rule and its supporting files.
- A conflict exists when the same reachable case requires incompatible actions, or one instruction
  allows a stop or omission another requires the reader to continue past. Check earlier clauses and
  examples as well as the changed wording; a later correct instruction does not remove an earlier
  escape. Distinct scopes and explicit delegations are compatible only when a reader can select the
  applicable route before taking either action.
- Read a new skill or section decision by decision, not as one instruction: list each decision it
  makes — who decides, act or ask, keep or remove, stop or continue — and read beside it the section
  of the dependency or rule that owns that decision. A paraphrase that narrows, widens or
  reclassifies the owner's decision is a conflict even when no sentence negates the owner; replace
  it with a citation of the owner's section.
- **The check covers examples as well as statements, and every file that loads alongside the
  edited one.** `edit-skill`'s authoring reference lists those files under **Rules**; an example
  one of them forbids is a conflict, since a reader copies an example before reading the text
  elsewhere that forbids it.
- **A changed instruction that breaks one of the authoring reference's own bullets conflicts with
  standing guidance.** Hold each change to its **Where Guidance Lives** placement bullet and to its
  **Writing** bullets on a correction that restructures the bullet it lands in, an absolute that
  carries its scope and exception, guidance that states what holds, and citations that resolve.
- **A rule file or `.agents/global.md` that names an individual skill to carve an exception, grant
  a permission or describe that skill conflicts with standing guidance**, as the authoring
  reference's **Where Guidance Lives** says. The rule states its requirement and the generic
  opening, such as "unless an invoked skill authorizes it". Read the departing skill's own text
  as well: it states its departure and cites the rule, and a departure stated on neither side, or
  only in the rule, leaves one case with two answers.
- **A subject a skill owns that its frontmatter description does not name is unreachable, and
  counts as a defect.** For every subject a change moves into a skill or adds to one, read that
  skill's description and confirm a clause names the subject; an index of owners in a rule file,
  `.agents/global.md` or a table is the same defect, as the authoring reference's **Where Guidance
  Lives** says, since the description is the only route to a skill.
- **Guidance arriving from another branch is checked like an edit.** A merge or rebase that brings
  the base into a guidance branch, a pull that updates a checkout holding pending guidance edits, and
  a pull request folded into another each put two sets of changes together that were only ever
  checked apart. Git reports a conflict only where both touched the same lines; two edits to
  different files can still give one case two answers, cite a section the other side renamed or
  moved, restate a rule the other side changed at its owner, or name a skill the other side removed.
  After the incoming changes land, list the decisions each side changed, apply these criteria to
  every decision both sides touch and to every citation of a file, section or skill either side
  moved, renamed or removed, and run the source check on the combined tree before the next push.
- Keep one coherent decision at its owner. Remove obsolete competing language, narrow a clause that
  applies too broadly, or make route selection explicit; preserve requirements for cases outside the
  correction. A passing package or source validator does not establish semantic consistency.
