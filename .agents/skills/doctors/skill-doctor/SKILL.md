---
name: skill-doctor
description: 'Audit all agent guidance — every rule, skill, agent definition, hook, settings file and external-skill registry entry — for what to cut, tighten, fix or add. It first refreshes its record of the vendors'' skill and prompting guidance online, then reads every file against the repository''s own authoring criteria, what a current model does unprompted and that record, and finds prohibitions, absolutes and cautions the vendor rubric would reword, merge or cut, conflicting instructions, stale citations, misplaced or duplicated requirements, descriptions that fail as the index, rules broader or more literal than their case, size budgets, undeclared dependencies, installed copies that shadow the canonical skills, and flows that spend more subagents, rounds or gates than the work needs. Use to audit, deep-review or clean up skills, rules or how skills run. Run only when the user asks for it.'
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
Unreachable, a description's length or wording under Budget and **Description Spends Its Budget On
Nothing**, a sentence under Restates, Wrong Altitude, Scope Calibration, Vendor Rubric or Authoring
Sections, a skill name under Dependencies — is listed once in the report as upstream, with the
registry entry and the upstream repository, and is never a finding, a remedy or an edit. A finding lands on the registry
entry only when it is about the entry itself: one with no directory, one whose skill duplicates
an owned skill, or a whole-entry cut under **Dispositions**.

Read [the lens catalog](references/lenses.md) whole before the pre-pass reads: each lens named
under **Reviewers** is a section of it, stating its defect shape, evidence, remedy and what is left
alone. Lenses, in order: Budget, Restates The Model's Defaults, Redundant, Contradictory, Stale,
Misplaced, Wrong Altitude, Scope Calibration, Vendor Rubric, Authoring Sections, Dependencies,
Unreachable, Description Spends Its Budget On Nothing, Flow, Installed Copies, Missing.

## Reviewers

**Lenses are grouped onto reviewers, never one reviewer per lens or per file.** Every reviewer
reads the whole **Lenses** section and the lens catalog it points to; the grouping says who
reports which checks.

- Reviewers are capped as `doctor-protocol`'s **Launches** sets. The
  repository's skill categories dictate the partition cut: a skill's whole package stays in one
  partition, a category is split only between packages, and the rule files and every other non-skill
  file form partitions of their own.
- A partition reviewer reports the lenses judged within a file or package: the per-file Budget
  table, Restates, Stale, Wrong Altitude, Scope Calibration, Vendor Rubric, Authoring Sections,
  Dependencies, **Description Spends Its Budget On Nothing**, the description check of
  **Unreachable** (a subject the skill owns that no clause of its description names) for each skill
  in its slice, and the launch records Flow needs for each skill in its slice.
- The cross-cutting reviewer reports the whole-repository lenses, what is visible only across files,
  working from the pre-pass output and the dependency graph: Redundant, Contradictory, Misplaced,
  Unreachable's other checks, Missing, Installed Copies, the Flow checks that span a caller and the skills it
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
- **A passage is cut for restating the model only on a repeatable result**, as `skill-pass`'s
  **Cutting A Passage** sets out, at its capability level and within its bound; an untried
  candidate is reported and stays as written or is reworded.
- **A rewording that removes no requirement is ordinary work however many files it reaches**,
  unlike a contradiction, whose disposition the **Contradictory** lens states. Because a rewording
  across the tree changes how the guidance reads everywhere, the report shows the `wording` counts
  for the tree and for the ten highest-ranked files, the number of passages under each verdict, and
  three to five representative rewrites, original beside rewrite, drawn from a file loaded in every
  session, a rule and a skill entry point.
- **Cutting a firm rule the user stated, or making it less firm, takes the repeatable trial result**
  above and a `council` ruling, since the rule records the owner's own judgment; the report shows
  the passage, the new text and the trial's runs. A rewording that keeps what the rule requires and
  how firmly is ordinary work.
- A Flow remedy that removes a review, gate or round, or changes who decides, is the run's decision,
  put to `council` when the remedy is contested and reported with the structural count before and
  after; one that batches, caps or stops a rerun of unchanged input is ordinary work.
- A rule that must be deterministic becomes a hook, and the rule stays for hosts without hooks.
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
