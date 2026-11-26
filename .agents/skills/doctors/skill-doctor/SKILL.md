---
name: skill-doctor
description: 'Audit all agent guidance — every rule, skill, agent definition, hook, settings file and external-skill registry entry — for what to cut, tighten, fix or add. It first refreshes its record of the vendors'' skill and prompting guidance online, then reads every file against the repository''s own authoring criteria, what a current model does unprompted and that record, and finds prohibitions, absolutes and cautions the vendor rubric would reword, merge or cut, conflicting instructions, stale citations, misplaced or duplicated requirements, descriptions that fail as the index, rules broader or more literal than their case, size budgets, undeclared dependencies, and flows that spend more subagents, rounds or gates than the work needs. Use for a skill doctor, rule doctor or guidance doctor run, or to audit, deep-review or clean up skills, rules or how skills run. Run only when the user asks for it.'
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
- `council`

## Inventory

Run `doctor-protocol`. The criteria are `skill-pass`'s: every reviewer reads that skill and its
authoring reference whole, and a lens below cites the section it applies rather than restating it.
Apply `banned-terminology` to wording findings and deliver remediation through `edit-skill`, leaving
its pull request open for the user.

The doctor runs no skill-test round across the guidance it audits, and a run that changes nothing
runs none.

Also read the host's skill-authoring skill and skill diagnostics when the host has them, found by
their descriptions: a description optimizer, a trigger evaluation, a report of listing cost and
unused skills. They are measurements this doctor reads, never re-implements.

`references/vendor-guidance.md` is the record of the vendors' skill and prompting guidance: the
pages, the files a harness bundles, the host table, a dated summary and the quotes it rests on.
The pre-pass's first step refreshes it, so the audit never runs against a record nobody checked.

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

**Shared index.** From the index `doctor-protocol`'s **Share The Index** keeps, this doctor reads
the file inventory. It writes the guidance inventory above, the dependency graph between skills and
the citation table.

### Pre-Pass

These are the mechanical steps `doctor-protocol` runs once before any reviewer reads, so no reviewer
spends a read on what a step already lists. A step whose tool the repository does not configure is
handled as `doctor-protocol`'s **Measure Before Fan-Out** says, and a step whose source cannot be
reached is recorded as not run the same way.

1. The vendor record, before anything else is measured or read.
   - Fetch every page in the record's **Pages** table, and search each vendor's documentation for
     newer guidance written for the current model family, of these kinds: the skill
     best-practices page, the coding agent's skills and memory pages, the general prompting page
     and the page for each current model, the vendor's own skill-writing skill, and its
     engineering posts on skills and context. Read the prompt audit and the other files the record
     lists under **Bundled Files** when the running harness has them.
   - Record each page as the record's opening says: URL, title, the date the page shows, the fetch
     date, how much was read, and each quote the summary relies on. A cross-host redirect comes
     back to the caller rather than being followed, so its target becomes a new row and is
     fetched; a page that is gone gets a search for its successor. A row that could not be reached
     is marked so and keeps its earlier date. A quote is copied from what was read; when a quote
     cannot be found, the line that needed it is dropped.
   - Keep the record as it stood in the run folder, rewrite the dated summary, and list what
     changed between the two for the report.
   - With no network, say so in the ledger and the report and audit against the record as it
     stands, giving its dates.
   - A fetched number overrides a default below. A fetched recommendation that conflicts with a
     decision the repository's guidance records, such as one `skill-pass`'s **Where The Sources
     Disagree** lists, is a Contradictory finding the run settles, through `council` where its
     checks cannot, never an automatic win. A fetched
     page that makes a check in `skill-pass`'s vendor rubric wrong or incomplete is a Stale
     finding on that rubric.
   - Every reviewer reads the refreshed record.
2. `skill-pass`'s **Source Check**, over the whole canonical tree. Every report it prints enters
   the ledger as a finding under the lens that owns its shape, **Stale** for a link, section or
   rule file that does not resolve and **Dependencies** for an undeclared name or a cycle.
3. Near-duplicate statements. A script kept in the run's working files splits every canonical
   file under `.agents` into bullets and sentences, normalizes each — case, markup and punctuation
   removed — and compares their word shingles across every file, printing each pair whose overlap
   passes a threshold the run states, 0.6 of five-word shingles by default, with both locations.
   The pairs are **Redundant**'s candidates.
4. Prohibition and emphasis wording, per owned file: the `wording` command `skill-pass`'s **Source
   Check** documents. Its rows, ranked by prohibiting units per 100 units and by how few of those
   units hold a reason, are **Vendor Rubric**'s candidates and counts, and its list of
   descriptions past a length limit goes to **Budget**.
5. The other countable wording shapes, per file: headings with one bullet, bullets past the length
   `skill-pass`'s **Writing** allows, each description's grammatical person, and hits for each
   term `banned-terminology` lists. They are **Wrong Altitude**'s counts.
6. Usage: the host's usage report where it has one, and the count of invocations per skill in the
   host's local transcripts over a stated window.
7. The byte, line, and token totals above.

### Measures

The counts `doctor-protocol` takes before the audit and again after the fixes: bytes, lines and
approximate tokens per file and loaded per turn for each host; source-check reports; near-duplicate
pairs; the `wording` command's total row and per-file rows; each other countable wording shape;
files past the size budget for how they load; descriptions past a length limit; and, per skill that starts subagents, its usual structural count.

## Lenses

Each check is reported file by file. A threshold the vendors publish is a default the fetched
guidance overrides; a threshold `skill-pass` sets is the repository's recorded decision.
**Reviewers** says which lenses are judged inside one partition and which need the whole tree.
Every finding is recorded in `doctor-protocol`'s finding shape: its fix quotes the sentence that
goes or the text that replaces it and names the owner a moved requirement lands in, and its
proving check is the pre-pass step or source check that listed it, or the passages a reader
compares.

**A registered external skill's text is its upstream's, and no lens raises a finding on it.** A
skill the external-resources registry, `.agents/external_resources.json`, lists is vendored: its
frontmatter, description, body and bundled files are read only for what the repository's own files
need from them, such as whether one names, depends on or duplicates it. What a lens would report
inside that text — a flag that hides it from the listing or a description with no trigger under
Unreachable, a description's length or wording under Budget and the two description lenses, a
sentence under Restates, Wrong Altitude, Scope Calibration, Vendor Rubric or Authoring Sections,
a skill name under Dependencies — is listed once in the report as upstream, with the registry
entry and the
upstream repository, and is never a finding, a remedy or an edit. A finding lands on the registry
entry only when it is about the entry itself: one with no directory, one whose skill duplicates
an owned skill, or a whole-entry cut under **Dispositions**.

### Budget

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

### Restates The Model's Defaults

An instruction the model follows without being told. Two checks, both recorded for every sentence
judged: the sentence names no tool, number, path, glob, exception clause, or rejected alternative
("rather than", "instead of", "not X"); and its opposite is something no competent engineer would
do unprompted. Both hold: a finding, whose cut meets the passage trial in Dispositions. Only the
second holds: a candidate for that trial, never cut on its own. Third check: an instruction a configured linter or formatter
already enforces, or would with one rule switched on; the tool configuration is the evidence, and
the remedy is the cut plus that rule as the guard.

### Redundant

One statement with two homes: a requirement in two rule files, in a rule and in the skill that runs
when it applies, twice in one file, in a caller and a skill it always invokes, two skills whose
bodies differ only by a noun, and each shape `skill-pass`'s **Prose Duplication** lists. A skill
restating an ambient rule at its point of use is judged as `skill-pass`'s **Writing** allows.
The pre-pass's near-duplicate pairs are the candidates, each confirmed or rejected by reading both
passages; a pair that words one requirement too differently for the script to match is still
reported when a reviewer meets it. Evidence: the sentence pairs quoted. Remedy: one owner, chosen as `skill-pass`'s **Where Guidance
Lives** places a requirement, and the copies go; two noun-different skills become one taking the
kind as an argument, and the report names each invocation name that retires.

### Contradictory

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

Text at the wrong height for the reader, in two groups. The countable shapes come from the
pre-pass and no reviewer recounts them: capital emphasis and bold-led prohibitions from the
`wording` rows, a heading with one bullet, a bullet carrying an appended exception past the length
`skill-pass`'s **Writing** allows, banned terms, and a description in the first or second person,
or addressed to the reader as an instruction, where the host's guidance wants the third person —
reported once as a convention when every description shares it, never as a finding per file. The
judgment shapes are what a reviewer reads for: hedges, brittle step-by-step logic where a heuristic
would do, vagueness where a decision was needed, a menu of options where one default belongs, and
incident narrative or evidence that belongs in a project or verification record. Evidence: the
pre-pass's counts per file, reported and never thresholded, and for a judgment shape the passage
quoted with what its reader cannot decide from it. Remedy: rewrite at the altitude the guidance
describes, explaining the why.

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
the intended reach, `council` picks the reading and the report names both.

### Vendor Rubric

A prohibition, an absolute, a caution or an example that `skill-pass`'s vendor rubric would write
another way. This lens applies that rubric in depth to every owned skill, rule and agent
definition; the rubric holds each check's principle, violation, better form and firmness, and
nothing here restates them. It owns the checks no other lens does: goal and reason over a
prohibition, absolutes, approval rules that name their actions, incident patches, named defaults,
examples, instructions about thinking and tools, and text written for older models. A rubric check
whose shape another lens owns is reported there and judged against the rubric's text: sizes under
Budget, a restated default under Restates, emphasis and steps under Wrong Altitude, descriptions
under the two description lenses, subagent text under Flow.

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
trace the work and are never its aim: no passage is reworded to move a number. They do show what
was judged: each prohibiting unit the rerun still counts is a passage with a recorded keep verdict
and its reason, and one with none was never judged, so it is judged and given its verdict in this
run, never left for a later one.

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

## Reviewers

**Lenses are grouped onto reviewers, never one reviewer per lens or per file.** Every reviewer
reads the whole **Lenses** section; the grouping says who reports which checks.

- Reviewers are capped as `doctor-protocol`'s **Launches** sets; this doctor sets no lower cap. The
  repository's skill categories dictate the partition cut: a skill's whole package stays in one
  partition, a category is split only between packages, and the rule files and every other non-skill
  file form partitions of their own.
- A partition reviewer reports the lenses judged within a file or package: the per-file Budget
  table, Restates, Stale, Wrong Altitude, Scope Calibration, Vendor Rubric, Authoring Sections,
  Dependencies, the
  two description lenses, and the launch records Flow needs for each skill in its slice.
- The cross-cutting reviewer reports the whole-repository lenses, what is visible only across files,
  working from the pre-pass output and the dependency graph: Redundant, Contradictory, Misplaced,
  Unreachable, Missing, Installed Copies, the Flow checks that span a caller and the skills it
  runs, and the unconditional set judged as one document against the per-host budget.
- The final reviewers and the final acceptance gate are briefed with `skill-pass`'s **Reviewer
  Brief**. The adversarial one takes each proposed cut and tries to name a task the sentence would
  have prevented a mistake on, takes each rewrite and looks for a requirement, condition or
  exception the original held that it lost, takes each retained instruction and tries to show the
  model does it unprompted, and takes each Flow remedy and tries to name a defect the removed launch
  would have caught.

## Dispositions

- **Cutting a whole rule file, skill, or registry entry is the run's decision**, made on four
  things, each named in the report: the files that name it; the usage measurement over a stated window, or unmeasured with
  the reason; the sentences that survive the Restates and Redundant lenses, which are what it
  uniquely says; and, when any survive, the result of a bounded task run at `subagent-matrix`'s
  standard capability level without the file, judged against the file's own stated outcomes. **A
  cut is made only on a repeatable result**: the task runs twice without the file, a third time
  when the two disagree, and a single run that did well without it recommends nothing. Every
  candidate file is tried in the run, the ones with the fewest surviving sentences first, so none
  is left for a later run. No surviving sentence is the ground to cut; surviving sentences
  with no usage is the ground to fix the trigger first. Age, size, and a
  reference count on their own never cut a file.
- **A passage is cut for restating the model only on a repeatable result**, through the trial
  `skill-pass`'s **Cutting A Passage** sets out, with its level, repeats and bound.
- **A rewording is ordinary work however many files it reaches.** Because a rewording across the
  tree changes how the guidance reads everywhere, the report shows the `wording` counts for the
  tree and for the ten highest-ranked files, the number of passages under each verdict, and three
  to five representative rewrites, original beside rewrite, drawn from a file loaded in every
  session, a rule and a skill entry point.
- **Cutting a firm rule the user stated, or making it less firm, takes the repeatable trial result**
  above and a `council` ruling, since the rule records the owner's own judgment; the report shows
  the passage, the new text and the trial's runs. A rewording that keeps what the rule requires and
  how firmly is ordinary work.
- A Flow remedy that removes a review, gate or round, or changes who decides, is the run's decision,
  put to `council` when the remedy is contested and reported with the structural count before and
  after; one that batches, caps or stops a rerun of unchanged input is ordinary work.
- A rule that must be deterministic becomes a hook, and the rule stays for hosts without hooks.
- A wording change within a file that removes no requirement is ordinary work, unlike a
  contradiction, whose disposition the Contradictory lens already states.
- Each mechanical check gets a guard in `skill-pass`'s source check or a hook, never a committed
  test, as its **Scripts** says: a check that fails when the generated rules file reaches its cap,
  when a registry entry has no directory, when two rule files share a byte-identical bullet.

## Report Additions

- per file, bytes and lines before and after; per host, the loaded-per-turn total against its
  budget;
- each cut with its evidence;
- per skill whose flow changed, the usual structural subagent count before and after;
- what changed in the vendor record since the last run: rows added, pages gone, redirected or not
  reached, figures and summary lines that changed, quotes no longer found, and each rubric check
  the change bears on; or that the network was unavailable, with the record's dates;
- each URL fetched, with its date and any redirect;
- the `wording` total row before and after, the files whose counts changed most, and the passages
  kept, reworded, merged and cut, each kept one with its reason;
- each passage trial with its runs and outcome, and each untried candidate;
- each whole-file cut made or kept, its trial runs and its outcome;
- each installed copy reported;
- what the lenses met inside registered external skills, listed as upstream;
- each hook, description clause, or guard added;
- the reviewers started, by role, and the skill-test round run for the changed guidance or the
  reason none ran.
