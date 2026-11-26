---
name: doctor-protocol
description: The audit-and-fix protocol every doctor skill runs on — scope resolution, a repository index doctors share, a mechanical pre-pass, a partitioned read-only audit under a reviewer cap, a resumable run ledger, a remediation plan shown and started at once, fixes by area on one pull request, re-planning mid-run so every finding is fixed in the run and only user decisions and external blockers stay open, one final review, behavioral verification once every fix is in, and the report skeleton. Read from a doctor skill that declares it; never invoked on its own.
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
   and the calls its domain raises, each named as the run's to decide or reserved to the user, as
   **Gate And Show The Plan** says;
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
| Audit reviewers | 1, applying every lens | 1 per partition, at most 11 at once, and 1 cross-cutting |
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
- **At most twelve audit reviewers run at once**, and a partition past that starts as one returns,
  as **Delegate The Audit** says. A doctor may set a lower cap, never a higher one. Launches a
  doctor adds beyond the table follow the counts the doctor states and stand outside this cap.
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

## Leave Nothing Open

The owner invokes a doctor for a complete pass over its class, so the run fixes every finding
inside its boundary before it reports.

- **A finding is fixed once its proving check passes and each measure it counts toward reaches its
  target**, such as a file brought within its size budget. A landed commit whose check or measure
  still misses leaves the entry open.
- **The plan changes mid-run when the work outgrows it.** A remedy that falls short of its
  finding's measure, more instances of a finding than the plan counted, and a remedy the work shows
  to be wrong are each re-planned and carried out in this run, as the delivery reference's
  **Implement In Waves** says. No plan foresees every case, so the parent judges the new remedy
  from what the finding's measure needs, such as moving text to the file that owns it where
  rewording cannot bring a file within its budget.
- **Unplanned, older than the run and too large are not dispositions.** A finding the plan missed
  joins it, one that predates the run is fixed like any other, and size only sequences an entry
  late, as **Gate And Show The Plan** says.
- **A round limit ends an approach, never a finding.** Where a review or gate loop reaches its
  limit on an in-boundary entry, the disposition picks the approach the entry is then fixed by;
  reverting the fix or accepting it with the finding recorded would leave it open.
- **Only two kinds of item stay open:** a decision reserved to the user, asked as **Gate And Show
  The Plan** says, and a genuine external blocker the run cannot remove, such as access it lacks or
  a release another owner holds. Each is recorded as the delivery reference's **Record What Stays
  Open** says, the blocker with what removes it.

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
  user decision, declined by an earlier record, unresolved while the run gathers the missing
  evidence, or deferred with its record for an item **Leave Nothing Open** lets stay open. Each
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
  **Pre-Push Gate** finds them, run once on the base, so the run knows which failures predate it;
  each is a defect it fixes, as **Resolve The Scope** says.
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
   than the cap allows at once, audit the ones with the most pre-pass candidates first and start
   the next as each reviewer returns, so this run reads every partition. Each reviewer gets its
   partition's paths, the complete lens catalog, the pre-pass candidates in its partition and the
   measures. It reads every file of its partition whole and runs each lens check by check,
   reporting each check's result, an empty result included: a check whose result is not reported
   was not run. An instance of a whole-repository lens is returned as a candidate for the
   cross-cutting reviewer, never chased across partitions.
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
   within the cap, until it is read whole; only a path the run cannot open stays marked unread,
   named in the report with what would let it be read.

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
- **Each entry is checked against the doctor's change boundary.** An entry whose remedy needs
  exception evidence the ledger lacks gets a step that gathers it, such as a measurement or a
  trial, and takes the disposition that evidence supports; a shown plan cannot supply that
  evidence, and only evidence the run cannot obtain leaves the entry open, as **Leave Nothing
  Open** says.
- **The plan takes one gate.** When every entry's fix is the remedy its lens states, put the plan
  to `acceptance-gate`'s Proposal question directly, and no attacker starts. When some entries
  carry a remedy the run designed, or alternatives the run chose between, invoke `review-proposal`
  with those entries as the proposal and the rest of the plan as its evidence; its Proposal
  verdict is the plan's one gate. On the small route the plan always goes to the Proposal question
  directly. Preserve objections and their dispositions through either route.
- **The doctor decides, and every decision is in the report.** The owner invokes a doctor to have
  its class corrected, and a run that stops for approvals returns a plan where a fix was wanted. So
  the run decides and makes every change its findings call for, including a rewording of correct
  guidance text and a rewording across the tree, apart from the reserved entries below; a call its
  own checks cannot settle goes to `council` in **Ask** mode, and the ruling is followed. Each
  decision goes in the plan file and the report with its reason, and the report says which
  decisions the run made and which went to the user.
  - **Reserved to the user's own words**: a merge, deployment, publication or release, a security,
    disclosure or authorization choice, such as who may see a record, and a product or scope
    choice a remedy makes, as `pre-production`'s **Product Choices** defines one — removing or
    hiding content or a feature, a remedy whose visible effect is large, a new surface, and a
    rewording of correct text already in a product. A rewording of guidance text is not a product
    choice, and a routine presentation detail stays the run's. Fixing a vulnerability so the
    product enforces the access it already intends is not one, and the run makes that fix. Ask the
    reserved entries together through the global rules' question procedure, each as options with
    each consequence and a recommendation, and for a visible choice with its captures and the old
    and new text in a message the user sees first; only the entries that depend on an answer wait
    for it.
  - **A departure from a rule rides the rule change.** Where the run judges a shape a rule
    prescribes or exempts worse than the departure, as `pre-production`'s **Trade-Offs Are
    Surfaced, Never Enforced** asks of a rule, the rule change goes on the run's
    agent-configuration pull request, and the code keeps the rule's form until that change merges,
    since code that departs from a rule still in force reads as a defect to the next run. The
    dependent source entry is recorded as held on that pull request's merge, which is the user's.
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

Once the plan is shown, read [the delivery reference](references/delivery.md) for the waves,
checks, review, acceptance, deferral, delivery and report.

## Guard Recurrences

A shape a lens finds more than once is a shape the next change will add again. Where the repository
already keeps structural tests or lint configuration, pair the fix with a guard: a test that fails
on the shape, a lint rule, a generator template corrected at its source. A doctor that only cleans
up what it finds runs forever; a guard is what lets a lens retire. A guard asserts the convention,
never the absence of a retired implementation.
