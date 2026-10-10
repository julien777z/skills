---
name: doctor-protocol
description: The audit-and-fix protocol every doctor skill runs on — scope resolution, read-only reviewer fan-out, a parent-owned ledger, an acceptance-gated remediation plan, sole-editor implementation, final review, deferral of leftovers, and the report skeleton. Read from a doctor skill that declares it; never invoked on its own.
short_description: 'Set the audit, fix, review, and reporting process used by every doctor skill.'
---

# Doctor Protocol

A doctor audits one class of repository hygiene and corrects what it finds. This skill owns the
run; each doctor owns only its domain.

## Dependencies

- `subagent-selection` — route every read-only reviewer and final reviewer through a subagent of the
  running session.
- `execute-task` — present the validated remediation plan through its **Plan** and require explicit
  approval before editing, then implement it under its **Execution**.
- `code-simplify` — simplify each implementation batch and the complete result.
- `acceptance-gate` — judge the remediation plan before it is presented and the complete diff
  before it lands.
- `defer-scope` — record work consciously left undone; it runs the gate's admission question itself.
- `pre-production` — apply the encountered-issue and target-contract policy while implementing.
- `land-pr` — for a doctor that delivers in merged batches, the check gate, conflict resolution and
  verified squash merge of each batch pull request its run opens.

Read the applicable dependencies before beginning. Apply their approval, compatibility, migration,
and encountered-issue policies within the invoking doctor's declared change boundary; they do not
expand that boundary.

## Declare What The Doctor Owns

A doctor declares this skill as a dependency and supplies five things, and may name its delivery
cadence under **Deliver**:

1. an **inventory** — what it enumerates and where each item is discovered at runtime;
2. **lenses** — each a defect shape, the evidence that establishes it, and the remedy;
3. **dispositions** in order, declaring the permitted changes and evidence required for exceptions,
   and naming which outcomes are the user's decision;
4. **domain dependencies** — the skills whose policy it applies and never restates;
5. **report additions** — the rows it appends to the skeleton below.

Anything else a doctor states is either this protocol restated, which is skill-to-skill
duplication, or a rule the repository already owns.

## Resolve The Scope

Use an explicit domain, service, path, or other concrete selection supplied by the caller.
Otherwise audit the whole repository. Read the declined records for that scope through
`defer-scope` before fan-out, so a finding the user already declined arrives as a decision.

An explicit selection controls which inventory items are audited, not how little context may be
read. Trace each selected item across ownership boundaries far enough to establish its evidence.
Do not turn that trace into a proactive audit of unrelated items encountered along the way.

The doctor's dispositions also bound what may change, independently of which files may be read.
Enforce that boundary during dependency execution, planning, implementation, and final review.
General encountered-defect instructions do not authorize changes outside it. Follow the doctor's
reporting disposition for excluded findings; neither recording nor a refused deferral authorizes
their implementation in this run.

Discover the repository's actual languages, projects, ownership boundaries, runners, generators,
validation commands, and dependency graph at runtime. Do not assume a framework, directory layout,
tool, provider, or hosting system.

## Measure Before Fan-Out

The parent collects the baseline measurements a doctor's inventory declares — a timing, a tool's
report, a count, a replay — before audit reviewers launch, and every reviewer reads the same
results. This collection may require repeated samples to distinguish a finding from noise. Audit
reviewers do not duplicate the baseline collection; post-change measurements and independent final
re-measurement required by the doctor still run under the repository's execution constraints. A
measurement that cannot be taken is recorded as unmeasured with the reason.

## Delegate The Audit

Use multiple read-only subagents for every run. The parent remains the sole editor and owns the
unified ledger.

1. Launch at least two independent reviewers. Partition a multi-domain scope by coherent ownership
   boundaries discovered from the repository. For a narrow single-domain scope, give two reviewers
   independent passes over that domain rather than inventing arbitrary file slices.
2. Launch a cross-cutting reviewer to compare the partitions, trace items that cross boundaries,
   find what a single-slice reviewer cannot see, and challenge every proposed disposition whose
   evidence does not establish the full picture. The doctor names what its cross-cutting reviewer
   compares.
3. Give every reviewer the complete lens catalogue. Require findings anchored to concrete
   declarations, files, and lines. A lens that lists its checks is run check by check, and each
   check's result is reported, an empty result included: a check whose result is not reported was
   not run. Reviewers edit nothing.
4. The parent verifies the evidence in the current tree, reconciles duplicates and disagreements,
   rejects unsupported churn, and records every item's disposition.

## Keep The Ledger

Maintain one working ledger for the complete audit. For every inventoried item record its
canonical declaration, the evidence gathered, its disposition under each lens — fix, keep with the
reason, unresolved with the missing evidence, left for the next run because a check rediscovers it,
or a user decision — and any unresolved edge. A finding an earlier run's declined record covers
enters as retained by that decision, with its reconsideration criterion checked, never as a finding
to present again.

Do not infer an invariant from one observation: one passing run, one fixture, one file that happens
to follow a convention. Enumerate the items before deciding what the convention is.

Keep the ledger outside the repository unless the caller explicitly requests a durable artifact.

## State The Intent

Build the intent statement from the lens catalogue and the user's approved remediation plan,
following `acceptance-gate`'s intent contract. Preserve approved dispositions through implementation
and check their completion against the change history and final diff.

## Gate And Present The Plan

If no justified correction remains, report the completed coverage and stop.

Otherwise write a decision-complete remediation plan and put it to `acceptance-gate`'s proposal
question as one item. A flag names the entries to rewrite, and the rewritten plan goes to a fresh
gate under `acceptance-gate`'s **Bounds**; a flag that section sends to the user is reported in the
plan as it directs, never silently dropped.

Check each entry against the doctor's change boundary before presenting it. Exclude entries whose
required exception evidence is absent; approval of a generated plan cannot supply that evidence.

**The plan schedules order, never branches.** Every entry lands in the branch the run is driving for
its kind — agent configuration or source, the one split the GitHub rule's **Branches and Pull
Requests** makes — whatever lens found it and however unrelated two entries look. A plan that gives
a group "its own branch" has split one approved instruction into several deliveries, and the ones
after the first are what get dropped: the run reports the branch it opened, the user reads that as
the work, and the rest survives only in a chat log. Say which entries go first and why the order
matters; never say where they go.

That holds for a group large enough to deserve its own review, too. Size is an argument for
sequencing it late and describing it clearly in the pull request, not for a second branch. Beyond
that split, only the user asking to hold work apart puts an entry anywhere else. A doctor that
delivers in merged batches names each checkpoint in its plan — the groups it closes and why the
batch is substantial enough to merge on its own — so the user approves the checkpoints with the
plan.

Then present it through `execute-task`'s **Plan**. The audit and its ledger are read-only; neither authorizes an edit. A
user decision a disposition produces — a test to cut, a flag whose removal changes behavior — is
presented as options with each consequence and a recommendation.

## Guard Recurrences

A shape a lens finds more than once is a shape the next change will add again. Where the repository
already keeps structural tests or lint configuration, pair the fix with a guard: a test that fails
on the shape, a lint rule, a generator template corrected at its source. A doctor that only cleans
up what it finds runs forever; a guard is what lets a lens retire. A guard asserts the convention,
never the absence of a retired implementation.

## Implement As Sole Editor

After explicit plan approval, the parent implements the complete approved plan and is the only
editor. Apply `code-simplify` after each meaningful implementation batch and across the final
result. Return to `execute-task`'s **Plan** for a newly discovered decision that changes the approved outcome;
do not silently narrow the correction.

The plan is implemented to its last entry in one continuous run, into the branch in flight.
A finished group is not a finished plan, and neither is a pushed commit or a green suite; go into
the next group in the same turn. `execute-task` owns what may and may not stop that run.

Do not add source comments that narrate the change, its previous shape, or why something was added,
removed, merged, or tightened. Make the result express the current state; tests validate that
behavior.

## Run Repository-Native Checks

Run the pre-push checks `execute-task`'s **Pre-Push Gate** defines, then any further
repository-native check applicable to the changed files and their consumers: formatting, static
analysis, tests, builds, code generation, and contract checks. Report a check category that is not
configured rather than inventing one.

## Review The Result

Launch at least two independent read-only final reviewers:

- one verifies that every approved disposition was carried out completely;
- one tries to disprove the decisions, checks what was retained, and reviews unresolved evidence.
  The doctor names what this reviewer challenges.

Both reviewers check the delivered changes against the doctor's boundary and required exception
evidence, including changes introduced while incorporating the base branch or resolving conflicts.

Validate their findings, fix every confirmed in-scope issue, rerun affected checks, and repeat the
relevant review until no confirmed issue remains or a genuine external blocker or user decision
prevents completion.

## Accept The Complete Diff

Once review is clean, put the complete diff to `acceptance-gate`'s final-acceptance question
against the intent statement. Fix every flag under `acceptance-gate`'s **Bounds** and push each fix
as its own increment, whose `execute-task` **Pre-Push Gate** verdict is the fresh gate.

## Defer Leftovers

A run's own leftover findings are not deferred: the next run rediscovers them, so the report names
them and nothing is written. A confirmed defect within the doctor's change boundary is fixed in this run,
whatever its size, rather than left for a later one. What goes through `defer-scope`, at the
moment the decision is made, is a decision the user declined — recorded so the next run carries it
rather than presenting the finding again — and anything found outside the run's lenses that no
check rediscovers, subject to the doctor's reporting disposition and change boundary. Any other
refused admission means in-boundary work is done in this run, unless the refusal names close,
which is recorded cancelled with its reason and reconsideration criterion. A finding
stated only in chat, the plan, or the report is not recorded.

## Deliver

The result goes out on the repository's delivery path in the cadence the doctor names; a doctor
that names none uses the first. A run that changes both agent configuration and source carries each
on its own pull request in that cadence.

- **One pull request, left open.** Merging is the user's decision, agent configuration included,
  because a doctor's edit may need more testing than one run.
- **Merged batches.** The run merges its pull request at each checkpoint and carries the rest of the
  plan on a fresh one, until the plan's last entry lands. Declaring this cadence authorizes those
  merges under the GitHub rules.
  - A batch ends at a checkpoint the approved plan names, never partway through an entry and never
    with a fix separated from the guard that holds it.
  - Before merging, the batch passes **Run Repository-Native Checks**, **Review The Result**, and
    **Accept The Complete Diff** on its own diff, gated against the run's full intent statement kept
    current with the batches already merged; the batch's entries say only what this diff must
    complete. It then merges through `land-pr`, which polls its checks to a terminal state. Between
    polls the next group is committed and pushed, each step through `execute-task`'s **Pre-Push
    Gate**, to the next batch's branch, stacked on the batch's branch as the GitHub rule's
    **Branches and Pull Requests** allows; nothing more is pushed to the batch's branch.
  - Required approvals and branch protection are never bypassed. When they are all a batch waits
    on, the batch extends through the next checkpoint the plan names, re-passes these gates on the
    grown head, and re-requests the required review.
  - After the merge, fetch the default branch, retarget the next batch's branch onto it (reusing
    the run's branch name where the environment fixes one), open its pull request as a draft, and
    continue. A merged batch is never the finished run.
  - The last batch's review also confirms that every approved disposition, across all batches,
    landed.

## Report

The final report names:

- the resolved scope and the inventory counts;
- each pull request the run opened, what it carried, and whether it merged;
- per-lens counts by disposition, including items that were already correct and needed no change;
- each applied correction and the evidence for it;
- each retained item and the distinction or reason that retains it;
- each unresolved item and the evidence that was unavailable or contradictory;
- each leftover finding a check will rediscover, named but not recorded;
- each recorded deferral, by its record;
- reviewer coverage, final-review results, and every gate verdict with what it named;
- the checks run and any category not configured;
- remaining external blockers or user decisions.

Each doctor appends its own rows.
