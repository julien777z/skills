# Doctor Delivery

Contents: **Implement In Waves**, **Run Repository-Native Checks**, **Review The Result**, **Accept
The Complete Diff**, **Record What Stays Open**, **Deliver**, **Report**.

The stages a doctor run applies once its plan is shown, which `SKILL.md`'s **Gate And Show The Plan**
hands to this file.

## Implement In Waves

Once the plan is shown, workers implement it side by side while the parent keeps the ledger, the
plan's order, every judgment over the combined result and every check that needs a shared
resource.

- **A wave is the groups that can run at once:** groups whose files do not overlap and none of which
  needs what another group in flight produces. A group that reaches into other groups' files — a
  rename across the scope, a shared module, a lockfile, generated output, a migration, a guard the
  others rely on — runs alone, before every group that needs what it produces. Cut this way a run
  has few waves: the cross-area groups in order, then every area group together.
- **Each group gets one worker, within `subagent-matrix`'s cap on execution workers**; as one
  finishes, the next group in the wave starts.
- **The brief is `subagent-matrix`'s worker brief form with every field filled.** Its scope is the
  group's ledger entries, each with its fix and proving check; its files are the group's files; its
  checks are those proving checks and the checks covering those files; its branch is the run's.
  Two lines of the form are filled for a doctor run: every entry in the group is in scope whatever
  its size, since the size budget does not apply, and a defect the worker meets outside its files
  is handed up in its report, never edited, so two workers never edit one file.
- **The parent adds each handed-up defect to the ledger** as a required entry and gives it to the
  worker that owns its files, or to a later group.
- **A shared resource is never used by two workers at once** — a database, a port, a running stack.
  A check that needs one runs in the parent.
- **Fixes land as commits per area on the one pull request.** The parent reads each worker's
  reported head and check results at their source, as `execute-task`'s reported-outcomes reference
  says, and marks the group's entries fixed with their commits.
- **Nothing reads the diff per wave.** A worker runs its own checks and the reuse search its brief
  requires; no simplification pass, review or whole-diff gate runs per group or per wave. The one
  exception is a group later groups build on, which gets `acceptance-gate`'s Diff question over
  its own diff before they start, as `execute-task`'s **Ongoing Simplification** says of such a
  step.
- **A doctor may declare a late audit** for lenses whose items settle only once earlier entries
  land. It is one more audit and verification stage over the partitions those lenses cover, taken
  after the entries it waits on are pushed. Its reviewers count toward the run's cap, and its
  findings join the same ledger and plan under the same gate, shown as an amendment.

A decision discovered during implementation is settled as **Gate And Show The Plan** settles one and
added to the plan as an amendment; do not silently narrow the correction.

**The parent re-plans an entry that falls short**, as `SKILL.md`'s **Leave Nothing Open** says:
one whose proving check or measure still misses once its fix lands, a finding the work meets more
instances of than the plan holds, and a remedy the work shows to be wrong. It writes the new remedy
as an amendment, gates it as the plan was gated, shows it, and assigns it to the group that owns
its files or to a later wave. The plan in force is the latest amendment, never the plan as first
shown.

The plan is implemented to its last entry in one continuous run, into the branch in flight.
A finished wave is not a finished plan, and neither is a pushed commit or a green suite; start the
next wave in the same turn. A genuine gate holds only its dependent work.

## Run Repository-Native Checks

Once the last group lands, run on the final head, once: the pre-push checks the GitHub rule's
**Pre-Push Gate** defines, the baseline checks from **Measure Before Fan-Out**, and any further
repository-native check applicable to the changed files and their consumers: formatting, static
analysis, tests, builds, code generation, and contract checks. Report a check category that is not
configured rather than inventing one.

Then take every measure again and rerun the mechanical pre-pass. Each instance a measure of defect
candidates still counts is matched to a ledger entry that retains it: kept with a reason, declined,
held on a rule change's merge, or open for a reserved user decision or an external blocker as
`SKILL.md`'s **Leave Nothing Open** allows. An instance with no such entry, and an entry marked
fixed whose measure still misses its target, is a missed fix: it is re-planned as **Implement In
Waves** says and goes back out as a fix step, and the run moves to **Review The Result** only once
none remains. Inventory totals, such as files, symbols,
dependencies, documents and strings, and performance measures are compared before and after, never
reconciled item by item.

## Review The Result

The diff is reviewed once, at the end. Launch two independent read-only final reviewers:

- one verifies that every planned disposition was carried out completely, and applies
  `code-simplify`'s rubric to the diff in the same read, so no separate simplification pass runs;
- one tries to disprove the decisions, checks what was retained, and reviews unresolved evidence.
  The doctor names what this reviewer challenges.

On the small route one reviewer does both. Both check the delivered changes against the doctor's
boundary, which holds the fix for every defect or vulnerability the run noticed, and required
exception evidence, including changes introduced while incorporating the base branch or resolving
conflicts.

**A diff past 2,500 changed lines or 60 changed files is read in slices by area.** The first
reviewer's read is split into at most four slices of neighboring groups, one reviewer per slice,
each given its slice's diff, the entries it covers and the list of files the other slices change.
The second reviewer stays one, working from the ledger and opening the diff where a decision
points.

Validate their findings, fix every confirmed in-scope issue, rerun affected checks, and review
again only the changed code and the findings still open, with one reviewer, until no confirmed
issue remains or a genuine external blocker or user decision prevents completion, within the
review-round limit `acceptance-gate`'s **Bounds** sets; a change that has used those rounds gets
the disposition that limit carries.

## Accept The Complete Diff

Once review is clean, put the complete diff to `acceptance-gate`'s final-acceptance question
against the intent statement. A diff read in slices is put slice by slice, the same slices, each
gate given its slice's diff as content with the intent statement and the list of files the other
slices change, and every slice must be accepted. One more gate then reads the seams between
slices, as `acceptance-gate`'s final-acceptance question allows: each place one slice's change
calls, imports or shares a contract with a file another slice changes. Answer every flag under `acceptance-gate`'s **Bounds**, pushing each fix as its own
increment through the GitHub rule's **Pre-Push Gate**.

When acceptance passes, record a `review` entry with `session-ledger` for each pull request: the
repository, the pull request, the accepted head, its tree and the scope `whole`, with the
requirements checked and the base revision of the governing guidance where the diff changes agent
configuration. A later review asked for the whole pull request then measures only what changed
after that head.

## Record What Stays Open

The run leaves open only what `SKILL.md`'s **Leave Nothing Open** allows, and nothing it leaves
lives only in chat, the plan or the report.

- **A confirmed defect or vulnerability is fixed in this run**, whatever its size or area, as
  **Resolve The Scope** says, and is never deferred.
- **Each item that stays open is recorded through `defer-scope`** once it is known to stay: a
  reserved decision the user has not answered when the run ends, and an external blocker, with
  what removes it. Cleanup that fixes no defect found outside the doctor's boundary is recorded the
  same way, subject to its reporting disposition. A refused admission means the work is done in
  this run, unless the refusal names close, which is recorded canceled with its reason and
  reconsideration criterion.
- **A decision the user declined is recorded the same way**, so a later run reads it under
  **Resolve The Scope** and skips the finding.
- **A path no reviewer read is not a finding.** This run reads it as `SKILL.md`'s **Delegate The
  Audit** says; one the run cannot open stays marked unread in the manifest and is named in the
  report with the count and what would let it be read.

## Deliver

Keep each repository's run on its draft pull request for the user's review: no doctor pull request
is merged or set to auto-merge by the run, whatever standing merge exception would otherwise cover
it, because the merge is where the owner reads the decisions the run made on its own. A later
explicit user instruction naming the target may authorize merge. A run that changes both agent configuration and source carries each on its own pull
request, except guidance the GitHub rule puts on the source pull request it depends on, and each
kind stays on one pull request however many fixes the run makes. Complete
every planned entry continuously; checkpoints sequence work on those drafts and never wait for a
merge. The one exception is a source entry held on a rule change's merge under **Gate And Show The
Plan**: the run completes its independent work and reports that entry as held. Run **Run
Repository-Native Checks**, **Review The Result**, and **Accept The Complete Diff** over the completed work before reporting it for the user's review. Confirm that every planned
disposition landed.

**A run's guidance fixes are reviewed once.** Where the run changed agent configuration, **Review
The Result** and **Accept The Complete Diff** are that change's delivery review and acceptance,
their reviewers and gate briefed as `edit-skill`'s **Guidance Delivery** asks of a guidance diff's
readers. Hand that route the accepted head as already reviewed: it adds the source check and one
skill-test round for the guidance the fixes changed, and starts no second review or acceptance.

## Report

The final report names:

- the resolved scope, the route taken, and the inventory counts;
- each draft pull request the run opened and what it carries;
- coverage: partitions and paths read whole, and every path no reviewer read, with the reason;
- each measure before and after, side by side, and each pre-pass tool that was not run;
- per area and per lens, the counts by disposition;
- each retained item and the distinction or reason that retains it;
- each recorded deferral and each declined record that skipped a finding, by its record;
- the launches the run made against the counts in **Launches**, final-review results, and every
  gate verdict with what it named;
- the baseline and final check results and any category not configured;
- every decision the run made, each council ruling, and each reserved decision with the user's
  answer or as still open;
- each source entry held on a rule change's merge, with that pull request;
- each item still open as **Record What Stays Open** records it: the reserved decision as asked,
  or the external blocker with what removes it; nothing else is reported as open.

Per-entry detail, each applied correction with its evidence and commit, goes in a file sent with
the report once the run holds more than five entries. Each doctor appends its own rows.
