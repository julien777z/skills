---
name: skill-doctor
description: 'Audit all agent guidance — every rule, skill, agent definition, hook, settings file and external-skill registry entry — for what to cut, tighten, fix or add. It reads every file against the repository''s own authoring criteria, what a current model does unprompted and the vendors'' current authoring guidance, and finds conflicting instructions, stale citations, misplaced or duplicated requirements, descriptions that fail as the index, rules broader or more literal than their case, size budgets, undeclared dependencies, and flows that spend more subagents, rounds or gates than the work needs. Use for a skill doctor, rule doctor or guidance doctor run, or to audit, deep-review or clean up skills, rules or how skills run. Run only when the user asks for it.'
short_description: 'Audit rules, skills and their flows for what to cut, fix, or add.'
---

# Skill Doctor

Guidance written for yesterday's model is paid for on every turn by today's. This doctor finds the
sentences that no longer earn that cost, the ones that fight each other, the ones pointing at
things that are gone, the flows that start more agents than their purpose needs, and what the
repository lacks. "Skill" here stands for all guidance: rules, skills, agent definitions, hooks,
settings and registry entries.

## Dependencies
- `doctor-protocol`
- `skill-pass`
- `guidance-flow`
- `banned-terminology`
- `edit-skill`
- `subagent-matrix`

## Inventory

Run `doctor-protocol`. The criteria are `skill-pass`'s: every reviewer reads that skill and its
authoring reference whole, and a lens below cites the section it applies rather than restating it.
Apply `banned-terminology` to wording findings and deliver remediation through `edit-skill`, leaving
its pull request open for the user.

**The run's fixes are reviewed once and tested once.** The protocol's final review and final
acceptance are their delivery review, as `doctor-protocol`'s **Deliver** says, so `edit-skill`'s
**Guidance Delivery** adds only the source check and one skill-test round, for the guidance the
fixes change. The doctor runs no skill-test round across the guidance it audits, and a run that
changes nothing runs none.

Also read the host's skill-authoring skill and skill diagnostics when the host has them, found by
their descriptions: a description optimizer, a trigger evaluation, a report of listing cost and
unused skills. They are measurements this doctor reads, never re-implements.

`references/vendor-guidance.md` holds the vendor and host tables and the dated summary of what the
vendors' authoring guidance said when last fetched. Read it before the inventory; the measurement
below refreshes it.

Every rule file, `.agents/global.md` and the project guidance included: bytes, lines, bullets,
whether it loads unconditionally or by path scope, the globs, and every skill it names. Every
skill: body lines and approximate tokens, description length and grammatical person, frontmatter
against the open specification, vendored (a registry entry) or owned, the description's user-only
gate and any flag that hides the skill from the listing, declared dependencies, the files that name
it, its bundled files with sizes and how deep their references chain, and each launch of subagents
its text describes. Every agent definition, hook (where it is registered, whether its command
exists), settings file, and registry entry, one line each. A vendored skill is inventoried and
read as **Lenses** says of a registered external skill.

Every installed copy of a skill, in each project, user, system, plugin and provider root the host
loads skills from: its path, the target a link resolves to, its scope, and a digest of its
content. A candidate on disk that no configured root or listing names is recorded as unknown, never
as installed, and precedence between roots is recorded only where the host states it.

Per host, what loads on every turn: the unconditional rules, the generated rules file, and the
skill listing.

Commit dates enter the inventory only when the clone is not shallow; otherwise they are unmeasured
with that reason. Age is never evidence on its own.

Measured once before fan-out:

1. `skill-pass`'s **Source Check**, over the whole canonical tree. Every report it prints enters
   the ledger as a finding under the lens that owns its shape, **Stale** for a link, section or
   rule file that does not resolve and **Dependencies** for an undeclared name or a cycle, and
   every reviewer reads the output, so no reviewer spends a read on what the script finds.
2. The vendors' current authoring guidance. Fetch every URL in the references table; a cross-host
   redirect comes back to the caller rather than being followed, so record its target as a new row
   and fetch that; search for a successor when a page is gone. Rewrite the dated summary. Every
   reviewer reads the file. Offline, the cached summary is read and its date reported. A fetched
   number overrides a default below; a fetched recommendation that conflicts with a decision the
   repository's guidance records is a Contradictory finding for the user, never an automatic win.
3. Usage: the host's usage report where it has one, and the count of invocations per skill in the
   host's local transcripts over a stated window.
4. The byte, line, and token totals above.

## Lenses

Each check is reported file by file. A threshold the vendors publish is a default the fetched
guidance overrides; a threshold `skill-pass` sets is the repository's recorded decision.

**A registered external skill's text is its upstream's, and no lens raises a finding on it.** A
skill the external-resources registry, `.agents/external_resources.json`, lists is vendored: its
frontmatter, description, body and bundled files are read only for what the repository's own files
need from them, such as whether one names, depends on or duplicates it. What a lens would report
inside that text — a flag that hides it from the listing or a description with no trigger under
Unreachable, a description's length or wording under Budget and the two description lenses, a
sentence under Restates, Wrong Altitude, Scope Calibration or Authoring Sections, a skill name
under Dependencies — is listed once in the report as upstream, with the registry entry and the
upstream repository, and is never a finding, a remedy or an edit. A finding lands on the registry
entry only when it is about the entry itself: one with no directory, one whose skill duplicates
an owned skill, or a whole-entry cut under **Dispositions**.

### Budget

Guidance the reader pays for and does not use. Two tables. Per host, reported once whatever the
scope: the unconditional rules against the rules-file target; the generated rules file against the
host's cap, where a path-scoped rule still counts in full for a host that concatenates every rule
into one file, and a cap equal to the file's current size is a cap fitted to the content rather
than chosen; the skill listing against the host's budget. Per file: a `SKILL.md` or a rule file
past the size budget `skill-pass`'s **Writing** sets for a file read whole, which binds rule files
and skills alike, a vendor's smaller target for an always-loaded file being reported as a
measurement and never as a finding per file; a description past the listing truncation; a
reference past the table-of-contents threshold without one; a reference chain deeper than one
level. Evidence: the measurements. Remedy: what the file states twice is merged, text moves to the
reference or file that owns it, a rule scopes by path, text is cut.

### Restates The Model's Defaults

An instruction the model follows without being told. Two checks, both recorded for every sentence
judged: the sentence names no tool, number, path, glob, exception clause, or rejected alternative
("rather than", "instead of", "not X"); and its opposite is something no competent engineer would
do unprompted. Both hold: a finding. Only the second holds: a candidate for the whole-file trial in
Dispositions, never cut on its own. Third check: an instruction a configured linter or formatter
already enforces, or would with one rule switched on; the tool configuration is the evidence, and
the remedy is the cut plus that rule as the guard.

### Redundant

One statement with two homes: a requirement in two rule files, in a rule and in the skill that runs
when it applies, twice in one file, in a caller and a skill it always invokes, two skills whose
bodies differ only by a noun, and each shape `skill-pass`'s **Prose Duplication** lists. A skill
restating an ambient rule at its point of use is judged as `skill-pass`'s **Writing** allows.
Evidence: the sentence pairs quoted. Remedy: one owner, chosen as `skill-pass`'s **Where Guidance
Lives** places a requirement, and the copies go; two noun-different skills become one taking the
kind as an argument, a user decision because it retires an invocation name.

### Contradictory

One reachable case given two answers, found by applying `skill-pass`'s **Conflict Check** and its
conflict criteria decision by decision across every file that loads together, never by matching
sentences: two files that disagree; a paraphrase that narrows, widens or reclassifies the decision
its owner states; an earlier clause or escape a later correct instruction leaves standing; an
example a co-loaded file forbids; a description that disagrees with a frontmatter flag; an absolute
whose exception is stated only elsewhere. A disagreement between path-scoped rules with disjoint
globs is a finding only for a host that loads both, and its remedy there is scoping. Evidence: the
decision, both passages, the case that reaches both, and which hosts co-load them. Remedy: one
coherent decision at its owner and a citation where the copy stood; unclear intent is a user
decision naming both readings.

### Stale

A reference to something gone: a tool, path, command, flag, model, product, or URL that no longer
exists or redirects; a cited `**Section**` its skill or rule no longer holds, and a section cited by
a step number, as `skill-pass`'s **Writing** says of citations; a dependency naming a skill that
does not exist; a hook registered whose command is missing; a registry entry with no directory
after the last scheduled sync, with that run's log; time-sensitive text, and text that says what
changed rather than what holds. Evidence: the source check's output, the tree, the manifests, the
sync log. Remedy: fix the reference, or cut what it anchored.

### Misplaced

A requirement in a file that `skill-pass`'s **Where Guidance Lives** does not make its owner:
`.agents/global.md` holding what need not bind before a skill loads; a rule file holding what a
skill runs for; a skill holding what its name and description do not bound; shared guidance
carrying one repository's facts, or a copy of how its tooling behaves today; guidance held in a
harness's memory. And a rule file or `.agents/global.md` that names an individual skill, outside
the one place that section allows, or that keeps an index of which skill owns which subject.
Evidence: the sentence, the condition its file's name and description set, and the skill that runs
when the requirement applies. Remedy: move it to that owner, word the rule's opening generically,
and let the departing skill state its own departure.

### Wrong Altitude

Text at the wrong height for the reader: emphasis on a share of bullets above the guidance's
example, hedges, brittle step-by-step logic where a heuristic would do, vagueness where a decision
was needed, a menu of options where one default belongs, a heading with one bullet, a bullet
carrying an appended exception past the length `skill-pass`'s **Writing** allows, banned terms,
incident narrative or evidence that belongs in a project or verification record, and a description
in the first or second person, or addressed to the reader as an instruction, where the host's
guidance wants the third person — reported once as a convention when every description shares it,
never as a finding per file. Evidence: counts per file, reported and never thresholded. Remedy:
rewrite at the altitude the guidance describes, explaining the why.

### Scope Calibration

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
the intended reach, a user decision naming both readings.

### Authoring Sections

A file that misses the section of `skill-pass`'s authoring reference its kind falls under, checked
section by section: **Harnesses**, for a hook, script, setting or instruction that serves one
harness's contract outside a scoped compatibility section; **Rules**, for a rule file's frontmatter
and scope; **Package And References**, for a skill's shape; **Decisions**, for a decision sent to
the user that is not the user's; **Output**, for a skill whose correct runs should share a shape
and that fixes none; **Routers**, for guidance that differs by one attribute of the task and is not
routed. Evidence: the passage and the bullet it misses. Remedy: the one that bullet states.

### Dependencies

A skill reference `skill-pass`'s **Dependency Audit** resolves: a skill named or identified by a
description without being declared; a declared edge that points back toward a caller, or a cycle;
a reference by path; a reference file that invokes a skill; a user-only skill used as an automatic
dependency. Evidence: the source check's output for name forms, and for the rest the passage and
the entry point's `## Dependencies`. Remedy: the one that section's criteria state.

### Unreachable

Nothing leads in: a skill no file names whose description carries no trigger; a subject a skill
owns that no clause of its description names, as `skill-pass`'s **Descriptions** and its conflict
criteria require; a variant file no router row links; a hook on disk not registered; a skill the
usage measurement shows never invoked; and an owned skill hidden from the listing by a frontmatter flag,
which that **Descriptions** section counts as a defect whatever the skill's invocation name.
Evidence: the reference counts, the description beside the skill's section headings, and usage.
Remedy: add the clause, remove the flag and state the user-only gate in the description, or a
whole-file cut under Dispositions.

### Description Spends Its Budget On Nothing

Every description is read on every turn, for every skill, so a clause that neither helps decide
whether this skill fires nor carries a rule that must bind before the body is read is paid for
constantly and returns nothing. The shapes: a slash command or invocation name that already identifies
the task, because the listing carries it and the reader deciding already has it; a paraphrase of the skill's own title;
`Use this skill to`; and what the skill does elaborated past the point a reader needs to recognize
the situation.

Score each by the substitution test `skill-pass`'s **Descriptions** states; where the remainder names
no situation and no file names the skill either, it is a finding under **Unreachable** as well.

Evidence: the description, quoted, with the clause that earns nothing marked and its length. Remedy:
cut the marked clause, keeping the trigger, every subject the skill owns, any argument it depends
on — a target, a scope, a mode — and any rule that must bind before the body is read. Retain a
literal slash alias that is too opaque to identify the task by itself, because it is then part of
the trigger rather than duplicate naming.

### Flow

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

### Installed Copies

An installed skill that is not the canonical one: a copy in a root the host loads that is not a
link to the canonical package and whose digest differs from it, which shadows the canonical skill
wherever that root takes precedence; the same name installed from two sources; two installed names
with identical content. Evidence: the inventory's paths, link targets and digests. Remedy: a copy
the repository's installer owns is refreshed through that installer; any other is reported for the
user with its path, never edited or deleted by this run.

### Missing

What the fetched guidance or the tree calls for and the repository lacks: a stack present in the
tree with no path-scoped rule and no skill that runs for it, a rule that must hold every turn and
that the usage measurement shows the user re-invoking mid-session (a hook), a description without
negative triggers where the host asks for them, a rule file with no frontmatter description.
Evidence: the tree and the summary. Remedy: add the rule, hook or description clause. A trigger
kept in a rules file and a committed evaluation are never the remedy: a skill is found by its
description, and `skill-pass`'s **Scripts** keeps tests of skills out of the tree.

## Dispositions

- Cutting a whole rule file, skill, or registry entry is a user decision, presented with four
  things: the files that name it; the usage measurement over a stated window, or unmeasured with
  the reason; the sentences that survive the Restates and Redundant lenses, which are what it
  uniquely says; and, when any survive, the result of a bounded task run at `subagent-matrix`'s
  cheap capability level without the file, judged against the file's own stated outcomes. **A cut
  is recommended only on a repeatable result**: the task runs twice without the file, a third time
  when the two disagree, and a single run that did well without it recommends nothing. At most five
  files are tried in a run, the ones with the fewest surviving sentences first, and the rest are
  reported as untried candidates. No surviving sentence is the recommendation to cut; surviving
  sentences with no usage is the recommendation to fix the trigger first. Age, size, and a
  reference count on their own never cut a file.
- A Flow remedy that removes a review, gate or round, or changes who decides, is a user decision
  presented with the structural count before and after; one that batches, caps or stops a rerun of
  unchanged input is ordinary work.
- A rule that must be deterministic becomes a hook, and the rule stays for hosts without hooks.
- A wording cut within a file is ordinary work, unlike a contradiction, whose disposition the
  Contradictory lens already states.
- Each mechanical check gets a guard where the repository keeps structural tests: a test that fails
  when the generated rules file reaches its cap, when a registry entry has no directory, when two
  rule files share a byte-identical bullet.

**Lenses are grouped onto reviewers, never one reviewer per lens or per file.** Every reviewer
reads the whole catalog; the grouping says who reports which checks.

- A whole-tree run starts at most five audit reviewers: up to four partition reviewers, the tree
  split by the repository's skill categories into slices of similar size with the rule files and
  every other non-skill file in one slice, and one cross-cutting reviewer. A scoped run, one
  category, skill or path, starts three: two independent passes over the scope and the
  cross-cutting reviewer.
- A partition reviewer reports the lenses judged within a file or package: the per-file Budget
  table, Restates, Stale, Wrong Altitude, Scope Calibration, Authoring Sections, Dependencies, the
  two description lenses, and the launch records Flow needs for each skill in its slice.
- The cross-cutting reviewer reports what is visible only across files: Redundant, Contradictory,
  Misplaced, Unreachable, Missing, Installed Copies, the Flow checks that span a caller and the
  skills it runs, and the unconditional set judged as one document against the per-host budget.
- Final review starts the protocol's two reviewers per round. Both, and the final acceptance gate,
  are briefed with `skill-pass`'s **Reviewer Brief**. The adversarial one takes each proposed cut and tries to name a task the sentence
  would have prevented a mistake on, takes each retained instruction and tries to show the model
  does it unprompted, and takes each Flow remedy and tries to name a defect the removed launch
  would have caught.

## Report Additions

- per file, bytes and lines before and after; per host, the loaded-per-turn total against its
  budget;
- the source check's result before and after;
- each cut with its evidence;
- per skill whose flow changed, the usual structural subagent count before and after;
- each URL fetched, with its date and any redirect;
- each whole-file cut proposed, its trial runs and its outcome, and each untried candidate;
- each installed copy reported;
- what the lenses met inside registered external skills, listed as upstream;
- each hook, description clause, or guard added;
- the reviewers started, by role, and the skill-test round run for the changed guidance or the
  reason none ran.
