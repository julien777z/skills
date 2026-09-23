---
name: guidance-doctor
description: Audit the repository's agent guidance for what to cut, tighten, or add, against what a current model does unprompted and what the vendors' current authoring guidance says. The guidance is every rule, skill, agent definition, hook, settings file, and external-skill registry entry the repository keeps for its agents. Use to audit rules or skills for redundancy, staleness, contradiction, budget, or usefulness.
disable-model-invocation: true
---

# Guidance Doctor

Guidance written for yesterday's model is paid for on every turn by today's. This doctor finds the
sentences that no longer earn that cost, the ones that fight each other, the ones pointing at
things that are gone, and the ones the repository lacks.

## Dependencies

- `doctor-protocol` — own the run.
- `banned-terminology` — the wording findings.
- `edit-skill` — deliver the remediation; its pull request is left open for the user.

Also read the host's skill-authoring skill and skill diagnostics when the host has them, found by
their descriptions: a description optimiser, a trigger evaluation, a report of listing cost and
unused skills. They are measurements this doctor reads, never re-implements.

`references/vendor-guidance.md` holds the vendor and host tables and the dated summary of what the
vendors' authoring guidance said when last fetched. Read it before the inventory; the measurement
below refreshes it.

## Inventory

Every rule file: bytes, lines, bullets, whether it loads unconditionally or by path scope, and the
globs. Every skill: body lines and approximate tokens, description length and grammatical person,
frontmatter against the open specification, vendored (a registry entry) or owned, the
model-invocation flag, declared dependencies, the files that name it, and its bundled files with
sizes and how deep their references chain. Every agent definition, hook (where it is registered,
whether its command exists), settings file, and registry entry, one line each. A vendored skill is
inventoried and never edited; a finding on one lands on its registry entry.

Per host, what loads on every turn: the unconditional rules, the generated rules file, and the
skill listing.

Commit dates enter the inventory only when the clone is not shallow; otherwise they are unmeasured
with that reason. Age is never evidence on its own.

Measured once before fan-out:

1. The vendors' current authoring guidance. Fetch every URL in the references table; a cross-host
   redirect comes back to the caller rather than being followed, so record its target as a new row
   and fetch that; search for a successor when a page is gone. Rewrite the dated summary. Every
   reviewer reads the file. Offline, the cached summary is read and its date reported. A fetched
   number overrides a default below; a fetched recommendation that conflicts with a decision a rule
   records is a Contradictory finding for the user, never an automatic win.
2. Usage: the host's usage report where it has one, and the count of invocations per skill in the
   host's local transcripts over a stated window.
3. The byte, line, and token totals above.

## Lenses

Each check is reported file by file. Every threshold is a default the fetched guidance overrides.

### Budget

Guidance the reader pays for and does not use. Two tables. Per host, reported once whatever the
scope: the unconditional rules against the rules-file target; the generated rules file against the
host's cap, where a path-scoped rule still counts in full for a host that concatenates every rule
into one file, and a cap equal to the file's current size is a cap fitted to the content rather
than chosen; the skill listing against the host's budget. Per file: a skill body past the body
target; a description past the listing truncation; a reference past the table-of-contents
threshold without one; a reference chain deeper than one level. Evidence: the measurements.
Remedy: procedure moves from a rule to a skill, a rule scopes by path, a body splits into
references, text is cut.

### Restates The Model's Defaults

An instruction the model follows without being told. Two checks, both recorded for every sentence
judged: the sentence names no tool, number, path, glob, exception clause, or rejected alternative
("rather than", "instead of", "not X"); and its opposite is something no competent engineer would
do unprompted. Both hold: a finding. Only the second holds: a candidate for the whole-file trial in
Dispositions, never cut on its own. Third check: an instruction a configured linter or formatter
already enforces, or would with one rule switched on; the tool configuration is the evidence, and
the remedy is the cut plus that rule as the guard.

### Redundant

One statement with two homes: a rule in two files, a rule elaborating what a skill owns past a
terse bullet, a point made twice in one file, two skills whose bodies differ only by a noun. A
skill elaborating a rule is the convention, never a finding. Evidence: the
sentence pairs quoted. Remedy: one owner — a terse rule and the full skill — and the copies go; two
noun-different skills become one taking the kind as an argument, a user decision because it retires
an invocation name.

### Contradictory

Two statements the reader cannot both follow: two files that disagree, a rule and a skill that
disagree, a description that disagrees with a frontmatter flag, a rule that bans what another
prescribes. A disagreement between path-scoped rules with disjoint globs is a finding only for a
host that loads both, and its remedy there is scoping. Evidence: both sentences and which hosts
co-load them. Remedy: one wins under current intent; unclear intent is a user decision naming both
readings.

### Stale

An outward reference to something gone: a tool, path, command, model, product, or URL that no
longer exists or redirects; a dependency naming a skill that does not exist; a hook registered
whose command is missing; a registry entry with no directory after the last scheduled sync, with
that run's log; time-sensitive text. Evidence: the tree, the manifests, the sync log. Remedy: fix
the reference, or cut what it anchored.

### Wrong Altitude

Text at the wrong height for the reader: emphasis on a share of bullets above the guidance's
example, hedges, brittle step-by-step logic where a heuristic would do, vagueness where a decision
was needed, a menu of options where one default belongs, a heading with one bullet, banned terms,
and a description in the first or second person, or addressed to the reader as an instruction,
where the host's guidance wants the third person — reported once as a convention when every
description shares it, never as a finding per file. Evidence: counts per file, reported and never
thresholded. Remedy: rewrite at the altitude the guidance describes, explaining the why.

### Unreachable

Nothing leads in: a skill no file names whose description carries no trigger, a hook on disk not
registered, a skill the usage measurement shows never invoked. A flagged skill is reachable by its
invocation name and, for a doctor, through the doctor listing; the flag alone is never the finding.
Evidence: the reference counts and usage. Remedy: fix the trigger, or a whole-file cut under
Dispositions.

### Description Spends Its Budget On Nothing

Every description is read on every turn, for every skill, so a clause that does not help decide
whether this skill fires is paid for constantly and returns nothing. The shapes: the slash command
or invocation name, which the listing already carries and the reader deciding already has; a
paraphrase of the skill's own title; `Use this skill to`; and what the skill does elaborated past
the point a reader needs to recognise the situation.

Score each by the substitution test `edit-skill` — **Description** states; where the remainder names
no situation and no file names the skill either, it is a finding under **Unreachable** as well.

Evidence: the description, quoted, with the clause that earns nothing marked and its length. Remedy:
rewrite to the trigger, keeping any argument the trigger depends on — a target, a scope, a mode —
and dropping the command that precedes it.

### Missing

What the fetched guidance or the tree calls for and the repository lacks: a stack present in the
tree with no path-scoped rule, a rule that must hold every turn and that the usage measurement shows
the user re-invoking mid-session (a hook), a skill the rules file never points at where the host's
guidance wants a trigger there, a description without negative triggers where the host asks for
them, a skill with no evaluations. Evidence: the tree and the summary. Remedy: add the rule, hook,
trigger, or evaluation.

## Dispositions

- A vendored skill is never edited; its registry entry is.
- Cutting a whole rule file, skill, or registry entry is a user decision, presented with four
  things: the files that name it; the usage measurement over a stated window, or unmeasured with
  the reason; the sentences that survive the Restates and Redundant lenses, which are what it
  uniquely says; and, when any survive, the result of one bounded task run on the weaker model
  without the file, judged against the file's own stated outcomes. No surviving sentence is the
  recommendation to cut; surviving sentences with no usage is the recommendation to fix the trigger
  first. Age, size, and a reference count on their own never cut a file.
- A rule that must be deterministic becomes a hook, and the rule stays for hosts without hooks.
- A wording cut within a file is ordinary work, unlike a contradiction, whose disposition the
  Contradictory lens already states.
- Each mechanical check gets a guard where the repository keeps structural tests: a test that fails
  when the generated rules file reaches its cap, when a registry entry has no directory, when two
  rule files share a byte-identical bullet.

The cross-cutting reviewer reads every file for redundancy and contradiction, which are visible only
across files, and judges the unconditional set as one document against the budget. The final
adversarial reviewer takes each proposed cut and tries to name a task the sentence would have
prevented a mistake on, and takes each retained instruction and tries to show the model does it
unprompted.

## Report Additions

- per file, bytes and lines before and after; per host, the loaded-per-turn total against its
  budget;
- each cut with its evidence;
- each URL fetched, with its date and any redirect;
- each whole-file cut proposed and its outcome;
- each hook, trigger, or guard added.
