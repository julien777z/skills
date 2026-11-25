# Skill Doctor Lenses

Contents: Budget, Restates The Model's Defaults, Redundant, Contradictory, Stale, Misplaced, Wrong
Altitude, Scope Calibration, Vendor Rubric, Authoring Sections, Dependencies, Unreachable,
Description Spends Its Budget On Nothing, Flow, Installed Copies, Missing.

The checks each lens of `SKILL.md`'s **Lenses** section runs, reported file by file as that section says.

## Budget

Guidance the reader pays for and does not use. Two tables. Per host, reported once whatever the
scope: the unconditional rules against the rules-file target; the generated rules file against the
host's cap, where a path-scoped rule still counts in full for a host that concatenates every rule
into one file, and a cap equal to the file's current size is a cap fitted to the content rather
than chosen; the skill listing against the host's budget. Per file: a file past the size budget
`skill-pass`'s **Writing** sets for how it loads — a file loaded in every session, a skill's
entry point or a path-scoped rule — with a skill entry point's approximate tokens reported beside
its lines and the rules that load together for one file type reported as a total; a description
past the specification's limit or the listing truncation; a reference past the table-of-contents
threshold without one; a reference chain deeper than one
level. Evidence: the measurements. Remedy: what the file states twice is merged, text moves to the
reference or file that owns it, a rule scopes by path, text is cut.

## Restates The Model's Defaults

An instruction the model follows without being told. Two checks, both recorded for every sentence
judged: the sentence names no tool, number, path, glob, exception clause, or rejected alternative
("rather than", "instead of", "not X"); and its opposite is something no competent engineer would
do unprompted. Both hold: a finding, whose cut meets the passage trial in Dispositions. Only the
second holds: a candidate for that trial, never cut on its own. Third check: an instruction a configured linter or formatter
already enforces, or would with one rule switched on; the tool configuration is the evidence, and
the remedy is the cut plus that rule as the guard.

## Redundant

One statement with two homes: a requirement in two rule files, in a rule and in the skill that runs
when it applies, twice in one file, in a caller and a skill it always invokes, two skills whose
bodies differ only by a noun, and each shape `skill-pass`'s **Prose Duplication** lists. A skill
restating an ambient rule at its point of use is judged as `skill-pass`'s **Writing** allows.
The pre-pass's near-duplicate pairs are the candidates, each confirmed or rejected by reading both
passages; a pair that words one requirement too differently for the script to match is still
reported when a reviewer meets it. Evidence: the sentence pairs quoted. Remedy: one owner, chosen as `skill-pass`'s **Where Guidance
Lives** places a requirement, and the copies go; two noun-different skills become one taking the
kind as an argument, and the report names each invocation name that retires.

## Contradictory

One reachable case given two answers, found by applying `skill-pass`'s **Conflict Check** and its
conflict criteria decision by decision across every file that loads together, never by matching
sentences: two files that disagree; a paraphrase that narrows, widens or reclassifies the decision
its owner states; an earlier clause or escape a later correct instruction leaves standing; an
example a co-loaded file forbids; a description that disagrees with a frontmatter flag; an absolute
whose exception is stated only elsewhere. A disagreement between path-scoped rules with disjoint
globs is a finding only for a host that loads both, and its remedy there is scoping. Evidence: the
decision, both passages, the case that reaches both, and which hosts co-load them. Remedy: one
coherent decision at its owner and a citation where the copy stood; where intent is unclear, `council` picks the reading and the
report names both.

## Stale

A reference to something gone: a tool, path, command, flag, model, product, or URL that no longer
exists or redirects; a cited `**Section**` its skill or rule no longer holds, and a section cited by
a step number, as `skill-pass`'s **Writing** says of citations; a dependency naming a skill that
does not exist; a hook registered whose command is missing; a registry entry with no directory
after the last scheduled sync, with that run's log; time-sensitive text, and text that says what
changed rather than what holds. Evidence: the source check's output, the tree, the manifests, the
sync log. Remedy: fix the reference, or cut what it anchored.

## Misplaced

A requirement in a file that `skill-pass`'s **Where Guidance Lives** does not make its owner:
`.agents/global.md` holding what need not bind before a skill loads; a rule file holding what a
skill runs for; a skill holding what its name and description do not bound; shared guidance
carrying one repository's facts, or a copy of how its tooling behaves today; guidance held in a
harness's memory. And a rule file or `.agents/global.md` that names an individual skill, outside
the one place that section allows, or that keeps an index of which skill owns which subject.
Evidence: the sentence, the condition its file's name and description set, and the skill that runs
when the requirement applies. Remedy: move it to that owner, word the rule's opening generically,
and let the departing skill state its own departure.

## Wrong Altitude

Text at the wrong height for the reader, in two groups. The countable shapes come from the
pre-pass and no reviewer recounts them: capital emphasis and bold-led prohibitions from the
`wording` rows, a heading with one bullet, a bullet carrying an appended exception past the length
`skill-pass`'s **Writing** allows, banned terms, and a description in the first or second person
(the third person and the imperative both pass; "I", "we", "you" or "your" is the finding), reported once as a convention when every description shares it,
never as a finding per file. The
judgment shapes are what a reviewer reads for: hedges, brittle step-by-step logic where a heuristic
would do, vagueness where a decision was needed, a menu of options where one default belongs, and
incident narrative or evidence that belongs in a project or verification record. Evidence: the
pre-pass's counts per file, reported and never thresholded, and for a judgment shape the passage
quoted with what its reader cannot decide from it. Remedy: rewrite at the altitude the guidance
describes, explaining the why.

## Scope Calibration

A rule broader, narrower or more literal than the case it serves, judged from its own text and its
neighbors, since the request that prompted it is not in the file:

- an absolute whose stated reason covers fewer cases than its words do;
- a rule a neighboring section or a co-loaded file carves an exception out of more than once;
- a rule that names a mechanism — a threshold, tool, surface or step — where its reason names an
  outcome, so obeying the words can miss the outcome;
- a rule written for one symptom that is silent on the next member of its class, or whose example
  is its only reachable case;
- an example carrying an incident's own vocabulary;
- a direction for one task, session or state of a product's contents encoded as lasting guidance.

Evidence: the sentence, its stated reason, and one invented case of a different kind from the
rule's own example where following the words gives a result the reason does not want, or the
passages that carve the exceptions. Remedy: state the outcome and the cases the reason covers, as
`skill-pass`'s **Writing** asks; where the text gives no reason and its neighbors do not settle
the intended reach, `council` picks the reading and the report names both.

## Vendor Rubric

A prohibition, an absolute, a caution or an example that `skill-pass`'s vendor rubric would write
another way. This lens applies that rubric in depth to every owned skill, rule and agent
definition; the rubric holds each check's principle, violation, better form and firmness, and
nothing here restates them. It owns the checks no other lens does: goal and reason over a
prohibition, absolutes, approval rules that name their actions, incident patches, named defaults,
examples, instructions about thinking and tools, and text written for older models. A rubric check
whose shape another lens owns is reported there and judged against the rubric's text: sizes under
Budget, a restated default under Restates, emphasis and steps under Wrong Altitude, descriptions
under **Description Spends Its Budget On Nothing** and the description check of **Unreachable**,
subagent text under Flow.

A reviewer reads each file in its partition whole. The `wording` rows say which files to expect
most from, never which passages fail. It judges every prohibition and absolute in the file as
`skill-pass`'s **How A Passage Is Judged** says, whatever the passage is about:

- **keep**, recording why: a fact specific to this repository, or a failure the repository's
  correction record shows agents still making;
- **reword**, as the goal and its reason or as the action to take, with the substance kept;
- **merge**, several passages into the reason they share, at its owner;
- **cut**, with the evidence `skill-pass`'s **Cutting A Passage** asks for.

Evidence: the passage quoted with its location, the rubric check it misses and the verdict.
Remedy: in the protocol's finding shape, one finding per passage. Its specific fix is the
rewritten text in full, ready to replace the passage, and for a merge the owner it lands in and
each passage that goes. Its proving check is the `wording` command rerun on the file and a read of
the rewrite beside the original that accounts for every requirement, condition and exception as
kept or named as cut. A kept passage is no finding; kept passages are counted per file with their
reasons. Checks that find every instance: the `wording` rows and the whole-file read. Left alone:
a registered external skill, text inside a fenced template or output format, and a list of named
defaults the rubric keeps. Judged within one file; a merge across files is confirmed by the
cross-cutting reviewer.

The measure is the `wording` command's rows before and after: prohibiting units, how many hold a
reason, the counts of each absolute, capital emphasis and descriptions past a limit. The counts
trace the work and are never its aim: no passage is reworded to move a number.

## Authoring Sections

A file that misses the section of `skill-pass`'s authoring reference its kind falls under, checked
section by section: **Harnesses**, for a hook, script, setting or instruction that serves one
harness's contract outside a scoped compatibility section; **Rules**, for a rule file's frontmatter
and scope; **Package And References**, for a skill's shape; **Decisions**, for a decision sent to
the user that is not the user's; **Output**, for a skill whose correct runs should share a shape
and that fixes none; **Routers**, for guidance that differs by one attribute of the task and is not
routed. Evidence: the passage and the bullet it misses. Remedy: the one that bullet states.

## Dependencies

A skill reference `skill-pass`'s **Dependency Audit** resolves: a skill named or identified by a
description without being declared; a declared edge that points back toward a caller, or a cycle;
a reference by path; a reference file that invokes a skill; a user-only skill used as an automatic
dependency. Evidence: the source check's output for name forms, and for the rest the passage and
the entry point's `## Dependencies`. Remedy: the one that section's criteria state.

## Unreachable

Nothing leads in: a skill no file names whose description carries no trigger; a subject a skill
owns that no clause of its description names, as `skill-pass`'s **Descriptions** and its conflict
criteria require; a variant file no router row links; a hook on disk not registered; a skill the
usage measurement shows never invoked; and an owned skill hidden from the listing by a frontmatter flag,
which that **Descriptions** section counts as a defect whatever the skill's invocation name.
Evidence: the reference counts, the description beside the skill's section headings, and usage.
Remedy: add the clause, remove the flag and state the user-only gate in the description, or a
whole-file cut under Dispositions.

## Description Spends Its Budget On Nothing

Every description is read on every turn, for every skill, so a clause that neither helps decide
whether this skill fires nor carries a rule that must bind before the body is read is paid for
constantly and returns nothing. The shapes are those `skill-pass`'s **Descriptions** names.

Score each by the substitution test `skill-pass`'s **Descriptions** states; where the remainder names
no situation and no file names the skill either, it is a finding under **Unreachable** as well.

Evidence: the description, quoted, with the clause that earns nothing marked and its length. Remedy:
cut the marked clause, keeping the trigger, every subject the skill owns, any argument it depends
on — a target, a scope, a mode — and any rule that must bind before the body is read. Retain a
literal slash alias that is too opaque to identify the task by itself, because it is then part of
the trigger rather than duplicate naming.

## Flow

A workflow that spends more agents, rounds or gates than its purpose needs, or lets a change
through with too little. The doctor reads the text and never runs a workflow it audits. For every
skill that starts subagents, record each launch as `guidance-flow`'s **Map it** defines a
structural count — owner, role, how many per round, what the count grows with, its cap, its rounds,
what a later round reruns, and the scope each agent reads — with the lines that state it. The
checks, judged against `skill-pass`'s **Subagents**:

- a launch whose count or rounds have no stated cap;
- a launch per scenario, per grader, per finding, per file or per item where one agent could take
  the batch and no independence requirement is stated;
- one diff or text read by several agents, in one skill or across a caller and the skills it runs,
  for criteria that overlap;
- a gate, review or round that reruns everything where only a delta changed;
- a step repeated on a head, diff or input that has not changed since it last ran;
- a delivery with no branch on the size or kind of change, so a one-sentence correction starts the
  reviewers, gates and rounds a new workflow does;
- a workflow that writes code or guidance with no earlier step that searches for an existing owner
  or implementation to reuse;
- a route to a workflow's report, merge or done state that passes no independent review or gate of
  the change.

Evidence: the launch records and the passages, with the usual structural count for one run before
and after the remedy; never a measured time or cost. Remedy: one agent per batch, a fresh agent
only where independence requires one, a rerun only of what a change touched, a named cap, the
duplicated read kept by the skill that owns the criterion, the missing search or review step added
at its owner.

## Installed Copies

An installed skill that is not the canonical one: a copy in a root the host loads that is not a
link to the canonical package and whose digest differs from it, which shadows the canonical skill
wherever that root takes precedence; the same name installed from two sources; two installed names
with identical content. Evidence: the inventory's paths, link targets and digests. Remedy: a copy
the repository's installer owns is refreshed through that installer; any other is reported for the
user with its path, never edited or deleted by this run.

## Missing

What the fetched guidance or the tree calls for and the repository lacks: a stack present in the
tree with no path-scoped rule and no skill that runs for it, a rule that must hold every turn and
that the usage measurement shows the user re-invoking mid-session (a hook), a description without
negative triggers where the host asks for them, a rule file with no frontmatter description.
Evidence: the tree and the summary. Remedy: add the rule, hook or description clause. A trigger
kept in a rules file and a committed evaluation are never the remedy: a skill is found by its
description, and `skill-pass`'s **Scripts** keeps tests of skills out of the tree.
