---
name: doctor-protocol
description: The audit-and-fix protocol every doctor skill runs on — scope resolution, a repository index doctors share, a mechanical pre-pass, a partitioned read-only audit under a reviewer cap, a resumable run ledger, a remediation plan shown and started at once, fixes by area on one pull request, one final review, deferral of leftovers, and the report skeleton. Read from a doctor skill that declares it; never invoked on its own.
short_description: 'Set the audit, fix, review, and reporting process used by every doctor skill.'
---

# Doctor Protocol

A doctor audits one class of repository hygiene across a whole repository and corrects what it
finds. This skill owns the run; each doctor owns only its domain.

## Dependencies
- `subagent-matrix`
- `review-proposal`
- `code-simplify`
- `acceptance-gate`
- `defer-scope`
- `pre-production`
- `execute-task`
- `edit-skill`
- `session-ledger`
- `council`

## Declare What The Doctor Owns

Read the applicable dependencies before beginning. Apply their approval, target-contract, compatibility, migration,
and encountered-issue policies within the invoking doctor's declared change boundary; they do not
expand that boundary, apart from a defect or vulnerability the run notices, which **Resolve The
Scope** puts inside every doctor's boundary.

A doctor declares this skill as a dependency, starts its run in its body with the instruction to
run `doctor-protocol`, and supplies:

1. an **inventory** — what it enumerates, where each item is discovered at runtime, and which
   paths it excludes and why;
2. **lenses** — each states its defect shape, the evidence that establishes it, the remedy, the
   checks that find every instance, what is left alone, and whether it is **whole-repository**,
   judged only across partitions, or judged within one file or area;
3. **mechanical commands** — the kinds of command whose output lists candidates for a lens, such
   as a linter, a type checker, a dead-code or dependency checker, a search or the doctor's own
   script, each found in the repository's configuration at runtime;
4. **measures** — one or more counts those commands produce, taken before the audit and after the
   fixes;
5. **dispositions** in order, declaring the permitted changes and evidence required for exceptions,
   and the calls its domain raises, which the doctor decides as **Gate And Show The Plan** says;
6. what its **cross-cutting reviewer compares** and what its **final reviewer challenges**;
7. **domain dependencies** — the skills whose policy it applies and never restates;
8. **report additions** — the rows it appends to the skeleton below.

A doctor may also state what dictates its partition cut, a reviewer cap lower than this
protocol's, a reviewer capability level, launches it adds beyond the table below with their counts
and caps, such as per-finding validation, and a late audit as **Implement In Waves** allows one.

A doctor runs one fixed workflow: it defines no effort levels, mode menus, or hidden switches,
and does not infer alternate execution from an effort word, flag, or implicit setting. Scope,
area, lens, and path selectors only bound the inventory, and the size of that scope alone selects
a route in **Launches**. Declare fixed dependency settings at the actual call in the doctor entrypoint body; they are not caller-selectable doctor options. Anything else a doctor states is
either this protocol restated, which is skill-to-skill duplication, or a rule the repository already owns.

## Launches

Every subagent is resolved through `subagent-matrix` and recorded as its **Dispatch** says, in the
run ledger. Reviewers run at the capability level the calling doctor selects, or standard when it
selects none, with any reviewer fallback the doctor specifies; workers run at standard.

| Launch | Small route | Whole route |
|---|---|---|
| Audit reviewers | 1, applying every lens | 1 per partition, at most 11, and 1 cross-cutting |
| Plan attackers | 0 | 0 when every remedy is one a lens states |
| Plan gate | 1 | 1 |
| Workers | 1 | 1 per group, as many at once as `subagent-matrix`'s **Dispatch** allows |
| Final reviewers | 1 | 2, or up to 5 when the diff is read in slices |
| Final gate | 1 | 1, or 1 per slice and 1 for the seams between slices, at most 5 |

- **The small route is 5 launches.** It applies when the caller's selection resolves to at most
  ten files holding at most 2,000 lines together. It takes no manifest, no cross-cutting reviewer
  and no plan attackers.
- **The whole route usually takes 15 launches** on a repository of four partitions and six groups:
  5 audit reviewers, 1 plan gate, 6 workers, 2 final reviewers and 1 final gate. On a diff read in
  slices the same run takes up to 22.
- **A run starts at most twelve audit reviewers.** A doctor may set a lower cap, never a higher
  one. Launches a doctor adds beyond the table follow the counts the doctor states and stand outside
  this cap.
- **What adds launches beyond the table:** one verifier for a partition whose reviewer returned
  findings unverified; `review-proposal`'s rounds when a whole-route plan holds a remedy the run
  designed;
  one Diff gate for a group later groups build on; a fresh gate for each flagged verdict, as
  `acceptance-gate`'s **Bounds** says; and one fix worker per final-review round after the first.

## Resolve The Scope

Use an explicit domain, service, path, or other concrete selection supplied by the caller.
Otherwise audit the whole repository. A doctor run sets its own scope, so `pre-production`'s
incidental size budget does not apply. Before fan-out, take `defer-scope`'s **Reading A Scope** for
that scope, which returns its declined and canceled records with the reason each was declined and
what would reopen it. A finding one covers enters the ledger as declined and is skipped, never
presented again, unless what would reopen it has happened.

An explicit selection controls which inventory items are audited, not how little context may be
read. Trace each selected item across ownership boundaries far enough to establish its evidence.
Do not turn that trace into a proactive audit of unrelated items encountered along the way.

The doctor's dispositions also bound what may change, independently of which files may be read.
Enforce that boundary during dependency execution, planning, implementation, and final review.
A cleanup finding outside it follows the doctor's reporting disposition; neither recording nor a
refused deferral authorizes its implementation in this run.

**A defect or vulnerability the run notices is never outside the boundary.** Whatever its size, its
area, the lens that met it or the doctor running, a confirmed defect or exploitable vulnerability
joins the remediation plan as a required entry and is fixed in this run at its owner, as
`pre-production`'s **Scope Follows The Defect, Not The Request** says of a defect the work notices.
It is never reported in place of a fix, deferred or left for another doctor. What a doctor's
disposition may still exclude is cleanup that fixes no defect.

Discover the repository's actual languages, projects, ownership boundaries, runners, generators,
validation commands, and dependency graph at runtime. Do not assume a framework, directory layout,
tool, provider, or hosting system.

## Keep The Run Ledger

The run's records live in the working-files folder of the worktree the run works in,
`.agent_sources/doctor-runs/<doctor>/<scope key>/`, kept out of Git through the repository's local exclude
file. [Run records](references/run-records.md) gives each file's format: the manifest, the pre-pass
output, a read receipt and a findings file per partition, the ledger, the plan and a status per
stage.

- **The parent writes each stage's records when the stage ends**, and an entry's status when its
  fix lands, so nothing a later stage needs lives only in the parent's context.
- **A run that finds records for the same scope and base resumes.** It continues at the first
  stage not marked done, checks each entry marked fixed against the branch with that entry's own
  check, and audits again only a partition whose files changed, other than by the run's own
  commits, since the digest its manifest row holds, and any partition marked unread. Records for
  another base describe a tree that is gone and are replaced.
- **The ledger holds one entry per verified finding and per item retained with a reason**, in the
  reference's shape, with its disposition: fix, keep with the reason, a council ruling, a reserved
  user decision, declined by
  an earlier record, deferred with its record, or unresolved with the missing evidence. Each
  partition's check results, an empty result included, stay in its receipt.
- Do not infer an invariant from one observation: one passing run, one fixture, one file that
  happens to follow a convention. Enumerate the items before deciding what the convention is.

## Share The Index

Doctors run one after another on the same commit share one index of the repository, so each reads
what an earlier one built.

- **Where it lives.** `.agent_sources/doctor-index/<commit>/`, in the working-files folder of the
  worktree the run works in, beside the run records and kept out of Git the same way. The commit
  is the one its tables were built from. [Run records](references/run-records.md) gives its files.
- **What it holds.** The file inventory, the symbol table, the import table and the dependency
  list with each manifest's declarations, and each further table a doctor says it writes.
- **Who writes and reuses it.** The parent, before the mechanical pre-pass. It reads each table
  the doctor says it reads where the folder for the audited commit holds it, builds only the ones
  that are missing, and writes the tables the doctor says it writes. Reviewers and workers read
  the index and never write it. A doctor states which tables it reads and which it writes, and
  nothing else about the index.
- **When it is stale.** A table serves only the commit its folder names, and only for files with
  no uncommitted change. Once the head moves, by the run's own fix commits included, a table read
  again is rebuilt in the new head's folder, and the folders of commits no branch of the worktree
  points at are deleted.

## Measure Before Fan-Out

Before any reviewer launches, the parent runs three things once and saves each result in the run
folder. Every reviewer reads the same results and repeats none of them.

- **Baseline checks.** The checks the repository's CI runs on a pull request, as the GitHub rule's
  **Pre-Push Gate** finds them, run once on the base, so a failure that predates the run is known.
  They run once more on the final head under **Run Repository-Native Checks**, and in between only
  where a group's own files need one.
- **Mechanical pre-pass.** Each command the doctor declares runs in its read-only mode over the
  scope, and its output is saved as the candidate list for the lens it serves. A reviewer judges
  each candidate in its partition, confirming or rejecting it with a reason, and reads for what no
  command finds. A command uses the tool the repository configures for its job. A tool the
  repository does not declare but the machine already has may run read-only, with nothing
  installed, configured or committed. A tool neither has is recorded as not run, with the lens it
  would have served, and that lens falls back to the reviewers' reading; the run never installs a
  tool, adds one to a manifest or configures one unasked.
- **Measures.** The doctor's declared measures and any other baseline its inventory declares, such
  as a timing or a replay. A collection may need repeated samples to tell a finding from noise. A
  measure that cannot be taken is recorded as unmeasured with the reason.

## Delegate The Audit

Reviewers are read-only subagents and edit nothing. On the small route one reviewer reads every
file in the scope whole, applies every lens, and returns its findings and read receipt; the rest
of this section is the whole route.

1. **Write the partition manifest before any reviewer starts.** Every in-scope path sits in exactly
   one partition, and every path the inventory excludes is listed with its reason. A partition is
   one area of the repository — a package, service, app or directory found at runtime, or what the
   doctor says dictates its cut — holding at most 5,000 lines or 60 files, whichever comes first,
   which is what one reviewer reads whole. Split a larger area at its next boundary down, then by
   directory order; a single file past the bound is a partition of its own. Merge small neighbors
   up to the bound.
2. **Launch one reviewer per partition, within the cap.** When the manifest holds more partitions
   than the cap allows, audit the ones with the most pre-pass candidates first and mark the rest
   unread; a resumed run audits them. Each reviewer gets its partition's paths, the complete lens
   catalog, the pre-pass candidates in its partition and the measures. It reads every file of its
   partition whole and runs each lens check by check, reporting each check's result, an empty
   result included: a check whose result is not reported was not run. An instance of a
   whole-repository lens is returned as a candidate for the cross-cutting reviewer, never chased
   across partitions.
3. **Launch one fresh cross-cutting reviewer** once the partition reviewers have returned their
   final results. It is handed the manifest, the doctor's
   whole-repository lenses, the pre-pass output, and every partition's findings and receipt. It
   finds what no single partition shows, such as duplicates and divergent siblings in different
   partitions and items that cross boundaries, compares what the doctor names, and challenges every
   proposed disposition whose evidence does not establish the full picture. It opens source only to
   confirm a candidate.
4. **Every finding takes the one shape the reference gives:** location, lens, quoted evidence, the
   specific fix, reach, severity, confidence and the check that proves the fix.
5. **Findings are verified by partition, never all in the parent's context.** As its last step,
   each reviewer opens every finding's location again at the audited head, confirms the quote and
   runs the proving check where that is read-only. A partition whose reviewer returned findings
   unverified gets one verifier. A candidate subject to validation the doctor adds passes it
   first. A finding without evidence, or whose quote the file does
   not hold, is dropped and counted.
6. **The parent reconciles from the returned records.** It merges duplicates, settles
   disagreements, rejects unsupported churn and records each entry's disposition in the ledger,
   reading source only to settle a disagreement.
7. **Coverage is checked against the manifest.** The parent compares each read receipt with its
   partition by command. A path missing from a receipt goes back to that reviewer, or to another
   within the cap; a path no reviewer read whole stays marked unread and is named in the report.

## State The Intent

Build the intent statement from the lens catalog, the plan as shown, the decisions the run made with
any council ruling, and the user's answer to any reserved decision, following `acceptance-gate`'s
**The Intent Statement**. Preserve the plan's dispositions
through implementation and check their completion against the change history and final diff.

## Gate And Show The Plan

If no justified correction remains, report the completed coverage and stop.

Otherwise write a decision-complete remediation plan from the ledger.

- **Entries are grouped by area, never by lens.** A group is the files that change together: one
  area of the repository, with every lens's entries for those files. The plan names each group's
  files, what it waits on and the wave it runs in, as **Implement In Waves** sets out.
- **Each entry is checked against the doctor's change boundary.** An entry whose required exception
  evidence is absent leaves the plan, stays in the ledger as unresolved naming that evidence, and
  follows **Defer Leftovers**; a shown plan cannot supply that evidence.
- **The plan takes one gate.** When every entry's fix is the remedy its lens states, put the plan
  to `acceptance-gate`'s Proposal question directly, and no attacker starts. When some entries
  carry a remedy the run designed, or alternatives the run chose between, invoke `review-proposal`
  with those entries as the proposal and the rest of the plan as its evidence; its Proposal
  verdict is the plan's one gate. On the small route the plan always goes to the Proposal question
  directly. Preserve objections and their dispositions through either route.
- **The doctor decides, and every decision is in the report.** The owner invokes a doctor to have
  its class corrected, and a run that stops for approvals returns a plan where a fix was wanted. So
  the run decides and makes every change its findings call for, including removing a feature, a
  product or scope choice a remedy makes, a rewording of correct text and a rewording across the
  tree; a call its own checks cannot settle goes to `council` in **Ask** mode, and the ruling is
  followed. Each decision goes in the plan file and the report with its reason.
  - **Reserved to the user's own words**: a merge, deployment, publication or release, and a
    security, disclosure or authorization choice, such as who may see a record. Fixing a
    vulnerability so the product enforces the access it already intends is not one, and the run
    makes that fix. Ask the reserved entries together through the global rules' question
    procedure, each as options with each consequence and a recommendation; only the entries that
    depend on an answer wait for it.
- **The gated plan is shown, and its work starts in the same turn.** The user reads one line per
  area with its entry counts, the order, what waits on a decision and any path no reviewer read;
  the entries themselves go in the plan file sent with it, as the reference says. The message
  carries no approval question, and the user can interrupt at any point.
- **A plan shown this way is never called approved.** The run ledger, the plan record kept with
  `session-ledger`, every brief and the report say it was shown, with no open decision or with the
  ones open then, and when. Showing it starts implementation and verification only; a merge still
  waits for what **Deliver** names.

**The plan schedules order, never branches.** Every entry lands in the branch the run is driving for
its kind — agent configuration or source, the one split the GitHub rule's **Branches and Pull
Requests** makes — whatever lens found it, however unrelated two entries look and however many
there are. A plan that gives a group its own branch has split one instruction into several
deliveries, and the ones after the first are what get dropped. Size is a reason to sequence a
group late and describe it clearly in the pull request, never a reason for a second branch; beyond
that split, only the user asking to hold work apart puts an entry anywhere else. The plan may name
checkpoints that group related entries on the same draft pull request.

## Guard Recurrences

A shape a lens finds more than once is a shape the next change will add again. Where the repository
already keeps structural tests or lint configuration, pair the fix with a guard: a test that fails
on the shape, a lint rule, a generator template corrected at its source. A doctor that only cleans
up what it finds runs forever; a guard is what lets a lens retire. A guard asserts the convention,
never the absence of a retired implementation.

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

The plan is implemented to its last entry in one continuous run, into the branch in flight.
A finished wave is not a finished plan, and neither is a pushed commit or a green suite; start the
next wave in the same turn. A genuine gate holds only its dependent work.

Do not add source comments that narrate the change, its previous shape, or why something was added,
removed, merged, or tightened. Make the result express the current state; tests validate that
behavior.

## Run Repository-Native Checks

Once the last group lands, run on the final head, once: the pre-push checks the GitHub rule's
**Pre-Push Gate** defines, the baseline checks from **Measure Before Fan-Out**, and any further
repository-native check applicable to the changed files and their consumers: formatting, static
analysis, tests, builds, code generation, and contract checks. Report a check category that is not
configured rather than inventing one.

Then take every measure again and rerun the mechanical pre-pass. Each instance a measure still
counts is matched to a ledger entry that retains it: kept with a reason, declined, deferred or
waiting on a reserved user decision. An instance with no such entry is a missed fix and goes back out as a
fix step.

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
issue remains or a genuine external blocker or user decision prevents completion, within the limit
of 3 review rounds per change that `execute-task`'s review-rounds reference sets; a change that
fails its third round gets that reference's disposition.

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

## Defer Leftovers

Nothing the run leaves unfixed lives only in chat, the plan or the report.

- **A confirmed defect or vulnerability is fixed in this run**, whatever its size or area, as
  **Resolve The Scope** says, and is never deferred.
- **Cleanup the run cannot finish is recorded through `defer-scope`** at the moment that is
  decided: an entry left unresolved for missing evidence or an external blocker, a decision the
  user has not answered when the run ends, and cleanup that fixes no defect found outside the
  doctor's boundary, subject to its reporting disposition. A refused admission means in-boundary
  work is done in this run, unless the refusal names close, which is recorded canceled with its
  reason and reconsideration criterion.
- **A decision the user declined is recorded the same way**, so a later run reads it under
  **Resolve The Scope** and skips the finding.
- **A path no reviewer read is not a finding.** It stays marked unread in the manifest and is
  named in the report with the count.

## Deliver

Keep each repository's run on its draft pull request for the user's review: no doctor pull request
is merged or set to auto-merge by the run, whatever standing merge exception would otherwise cover
it, because the merge is where the owner reads the decisions the run made on its own. A later
explicit user instruction naming the target may authorize merge. A run that changes both agent configuration and source carries each on its own pull
request, except guidance the GitHub rule puts on the source pull request it depends on, and each
kind stays on one pull request however many fixes the run makes. Complete
every planned entry continuously; checkpoints sequence work on those drafts and never wait for a
merge. Run **Run Repository-Native Checks**, **Review The Result**, and **Accept The Complete Diff**
over the completed work before reporting it for the user's review. Confirm that every planned
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
- remaining external blockers.

Per-entry detail, each applied correction with its evidence and commit, goes in a file sent with
the report once the run holds more than five entries. Each doctor appends its own rows.
