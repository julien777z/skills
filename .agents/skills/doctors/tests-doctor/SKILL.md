---
name: tests-doctor
description: Audit and correct existing tests for contract value, redundancy, weak assertions, naming, suite layout against siblings and source, runtime, third-party rate limits, coverage by test, doubles of repository-owned code, construction and data placed outside their owners, determinism, and suite configuration such as skips, warnings and time limits, posting one cost comment on each pull request it opens. Use to review, clean up, speed up, de-duplicate, or find gaps in tests across a repository. Run only when the user asks for it.
short_description: 'Audit tests for contract value, redundant proof, weak assertions, runtime, provider rate limits, and determinism.'
---

# Tests Doctor

Bring every suite to the shape its siblings share, repair or remove tests that prove nothing, name
them as labels, run them within budget, and cover each contract in every classification that can
reach it.

Repair the existing tests and their necessary configuration through existing runner targets, and
apply `test-fixture`'s validation boundary to diagnostic experiments.

## Dependencies
- `doctor-protocol`
- `pre-production`
- `test-fixture`
- `council`

## Inventory

Run `doctor-protocol`.

Also read the repository's test-runner skill when the skill listing declares one, found by its
description rather than assumed by name. Its locking, service, and pacing rules hold for every run
this doctor makes and are never restated here.

A skill's regression scenarios, the scenario folders in its top-level `<skill>/tests/` folder, are
guidance, never test code: they are out of this doctor's inventory.

Discover at runtime: source roots and test roots; the classifications the runner distinguishes; each suite,
the ownership boundary it belongs to, and the source it mirrors; where each suite keeps fixtures,
factories, helpers, and shared cases; markers, skip and xfail marks, and commented-out tests; the
runner's targets and the CI jobs that run tests; every double — each `patch`, `patch.object`, and
`monkeypatch.setattr` target and each `Mock`, `AsyncMock`, and `MagicMock` construction — with the
owner of its target, whether the real implementation crosses a process boundary, and the seam the
application declares for that dependency when one exists; each third party a suite calls for real,
with the calls one run makes to it per account and per destination; and any tighter suite budget
the repository configures, such as a documented target, with runner and CI timeouts recorded as
hang bounds rather than budgets.

**Shared index.** From the index `doctor-protocol`'s **Share The Index** keeps, this doctor reads
the file inventory, symbol and import tables and dependency list. It writes the test-to-source map,
the collected test list, the fixture and doubles tables, the duplication detector's pairs over test
trees, and each suite's timing and coverage.

### Pre-Pass

These are the mechanical commands `doctor-protocol` runs once before any reviewer reads, serialized
as the runner requires, each listing candidates for the lenses that read it. A tool the repository
does not configure is handled as `doctor-protocol`'s **Measure Before Fan-Out** says. The commands
below are pytest's, and a suite on another runner uses that runner's equivalent.

- **Collected tests** — every test the runner collects per target, and every test directory no
  target reaches.
- **Timing** — every runner target through the runner's own per-test and per-fixture duration
  reporting, with baseline pass and fail state and suite wall times. Rank cases and fixtures only
  where existing reporting attributes their costs; missing attribution is recorded as unmeasured,
  not filled by a new maintained diagnostic system. A suite that cannot run locally uses its
  existing CI timing when available.
- **Coverage by test** — line coverage per suite with the test that covers each line, where the
  runner's coverage plugin records it.
- **Fixtures** — every fixture the runner knows against the references to it, listing those no
  test requests, and every fixture definition by module.
- **Doubles** — a syntax-tree script kept in the run's working files that lists every patch target
  and mock construction with the module that owns the target.
- **Skips** — every skip mark, xfail mark, conditional skip and commented-out test.
- **Repeated blocks** — the repository's cross-file duplication detector over every test tree, at
  the tool's default similarity.
- **Symbols only tests consume** — every module-level symbol in an application package with its
  consumers classified by root, from the symbol table or a dead-code detector run with and without
  the test roots; and every import from a test root into an executable, from the import table.
- **Test-to-source map** — one row per test module with the source module or package it resolves
  to, as **Align Structure With Siblings And Source** lays the table out.

```sh
pytest --collect-only -q
pytest --durations=0 --durations-min=0
pytest --cov --cov-context=test
pytest --fixtures -q
rg -n 'pytest\.mark\.(skip|skipif|xfail)|pytest\.skip\(|pytest\.importorskip|^\s*#\s*(async )?def test_'
rg -n '@pytest\.fixture' -g 'test_*.py' -g 'conftest.py'
vulture <source roots> --min-confidence 80
```

### Measures

The counts `doctor-protocol` takes before the audit and again after the fixes: per suite, wall time
against its budget, the sum of test call durations, tests collected, and line coverage; across the
test trees, duplication-detector pairs, skips and xfails, doubles of repository-owned code, unused
fixtures, test modules mirroring no source, and names a naming check reports; and per provider,
account and destination, real calls per run.

**A source line covered before a fold, merge or cut and uncovered after it is a dropped fact.** The
second coverage run is compared with the first line by line, and the run restores what proved each
such line, or names the removed disproportionate case that accounts for it.

The budget is the suite budget `test-fixture`'s **Time Budgets** set, and within it no test, parametrized family
or module is disproportionate under `test-fixture`'s cost question.

**The budget binds the run.** A suite measured over it is worked until it is under, by the
dispositions below, and the run is not finished while one stands: the number was known before the
run began, so reporting the breach, recording it or carrying it into the plan as an observation
spends the measurement on nothing. Where the work genuinely cannot land in this run, the run puts
that to `council` in **Ask** mode with the number and the cause, follows its ruling and names it in
the report; a breach stands only on that ruling.

**Read setup against assertion before reading any single case.** Where existing reporting supplies
per-test call durations, compare their sum with suite wall time. A large difference identifies cost
outside test bodies, not a particular fixture. Use existing setup and fixture attribution to
investigate repeated client, organization, persisted-aggregate or authenticated-session creation.
Report available totals and mark missing attribution unmeasured under `test-fixture`'s procedure.

## Lenses

Read [the lens criteria](references/lenses.md) before building the inventory: each lens named here
and in this skill's other sections is a section of that reference, stating what the lens flags, the
checks that find every instance, what is left alone, and its remedy where **Findings** below does
not already give it. Its lenses apply `test-fixture`'s sections named in the lens criteria (**Test
Value And Retention**, **Literal Sweep**, **Prefer Parametrized Cases**, **Boundary Representations
And Decision Matrices**, **Naming Checks**, **Auditing Existing Doubles**, **Factory Contents**, and
its suites reference).

| Lens | Flags | Reach |
| --- | --- | --- |
| **Align Structure With Siblings And Source** | A suite laid out unlike its siblings or its source, and application symbols only tests consume. | Whole repository. |
| **Audit Test Value And Repair Weak Proof** | A test that proves nothing, proves it weakly, or repeats a literal or a case its owner declares. | Partition. |
| **Find Repeated Blocks With A Detector** | A block copied between test modules. | Whole repository. |
| **Name Cases As Labels** | A test, fixture, factory or helper name that is not a label. | Partition. |
| **Bring Every Suite Under Budget** | A suite over its budget, a disproportionate case, and what makes a test flaky. | Partition, by suite. |
| **Stay Inside Third-Party Limits** | A run that draws a limit refusal from a third party. | Partition; each provider's calls are summed across the repository. |
| **Map Coverage By Test** | A journey, boundary crossing or pure function with no test in the classification that should reach it. | Whole repository. |
| **Make Doubles Honest** | A double of repository-owned code, or one placed off the declared seam. | Partition; the doubles table is compared across suites. |
| **Keep Construction Out Of Test Modules** | Model construction, factories and mirrored types outside their shared owner. | Partition. |
| **Keep Test Data In The Repository's Domain** | A suite speaking a domain its source does not own. | Partition. |
| **Hold Suite Configuration To Its Rules** | Runner and job configuration off the suite rules: skips, warnings, markers, environment values, time limits. | Whole repository. |

Every finding is recorded in `doctor-protocol`'s finding shape. Its fix names the owner each block,
fixture or case moves to and what is deleted; its proving check is the affected suite re-run green,
with the timing or coverage measure re-taken where the finding concerns one.

## Reviewers

Reviewers are capped as `doctor-protocol`'s **Launches** sets. The
suite family dictates the partition cut: each application, service, and package suite, and each
cross-boundary group such as end-to-end, migration, script, or front-end, is a partition of its own
or is split inside itself, never merged with another family. The lens catalog a reviewer is given is
the lens criteria reference together with the **Lenses** table.

The cross-cutting reviewer works from the test-to-source map, the collected test list, the
detector's pairs, the coverage by test and the doubles table in the pre-pass output, and owns the
whole-repository lenses: layout, coverage, suite configuration and the duplicates across suites of
one classification, because those are visible only across slices. It compares the doubles table
across suites, since a seam one suite uses and its sibling patches around is visible only there,
and sums each provider's per-run calls per account and per destination across slices, since a
shared account's total is visible only there.

The final reviewer challenges the result this way: it re-times every suite the run cut or reduced against the reported
numbers, re-checks each merged parametrization and folded assertion against the coverage
comparison for a fact that was dropped, confirms each retained skip or xfail still has a live
condition, and challenges every coverage gap the run left open.

## Dispositions

### Change Boundary

This doctor changes tests, test-only support, and test execution configuration. Classify an edit
by its purpose and runtime consumers, not its directory: a shared bootstrap or configuration edit
that changes application execution is an application change. Reading source to understand a test
does not authorize changing it.

**A suite's architecture is inside that boundary, whole.** How tests isolate from one another, how
state is seeded, shared and cleared, what scope the expensive fixtures hold, and how the application's
own sessions are bound during a test are test execution configuration, and rewriting them across an
entire suite is this doctor's ordinary work. The purpose of the run is a suite in good working
condition, and the slop that keeps one out of it is usually structural — a cleanup contract that
rebuilds the same world per test, a fixture every module reaches for at the wrong scope — so a run
that fixes every symptom and leaves the structure has not done the job.

A fixture kept under its existing name costs its callers nothing however many there are, and a rewrite that changes
the isolation model is verified the same way as any other edit here: the affected suites re-run
green, and the durations are re-taken against the same workload.

Application changes qualify only for the performance exception below, removal of a proven dead
test-only seam or of an application symbol whose only consumers are the tests that exercise it,
or repair of a product defect or vulnerability the run notices, one a baseline failing test
exposes included. For a seam,
inspect non-test callers and history, move coverage to its real owner boundary, then remove the
unused export, flag, wrapper, injection hook, or dead path without a compatibility alias. A test
failing at this run's baseline measurement is this doctor's own finding: a run the user invoked to
repair tests is the one exception to `pre-production`'s **Encountered Issues** baseline exclusion,
which records and leaves a test already failing on the default branch that other work meets. For a
baseline failure, reproduce the product defect, fix it at its owner in a separate commit, and show
the same harness failing with the fix absent and passing with it present. Do not weaken, skip, or
delete tests to conceal a defect. Other structural changes to the application remain outside this
doctor's boundary and are reported with evidence; any other confirmed product defect or
vulnerability the run notices is fixed at its owner in this run, as `doctor-protocol`'s **Resolve
The Scope** says.

### Application Performance Exception

Before proposing an application change, establish all three conditions:

1. A repository-native suite exceeds its wall-time budget.
2. Profiling or repeated measurements attribute the overrun to an application path. First address
   test-side causes such as fixture setup, repeated startup, excessive data, and timing sleeps.
3. The focused application fix is necessary to bring that suite within budget, alone or alongside
   identified test fixes. An isolated 10 ms saving qualifies only when its measured cumulative cost
   satisfies these conditions; a faster microbenchmark or a suite already within budget does not.

Record the workload, baseline, budget, bottleneck evidence, expected suite-level improvement, and
correctness guarantees before adding a distinct performance entry to the remediation plan. Missing
measurements and differences within measurement noise leave the exception unproven. A shown plan does not substitute for this evidence.

After implementation, repeat the same suite workload, verify its budget outcome and correctness,
and report the before/after evidence. The improvement must exceed measurement noise. Preserve every
coverage guarantee unique within its classification; never cut tests solely to achieve a timing
target, apart from removing a disproportionate case as **Bring Every Suite Under Budget** says. A missed budget or unverified improvement remains unresolved rather than being reported as a successful performance fix.

Reviewers check every application performance change against this exception at proposal and final
review, including changes introduced during conflict resolution. Temporary application mutations used to
prove tests may bypass the performance exception only while running the proof; restore every one
before delivery and verify that none enters the delivered diff.

### Findings

- A slow suite, in order: widen the scope of the fixtures that dominate it, so an expensive world is
  built once for the tests that share it rather than per test; fold the cases whose runtime is out of
  proportion to what they prove into a case of the same classification already paying that setup,
  or make them cheaper where they stand; fix the remaining test-side causes; admit a focused
  application fix only through the performance exception; remove a disproportionate case that cannot
  be made cheap; parallelize independent work where the runner and shared resources allow, never
  across a shared database or lock and never in a way `test-fixture`'s **Test Cost** lists as absorbing a slow
  test. Re-time after implementation against the
  same workload. A suite still over budget is unfinished work, not a line in the report: carry on
  with the next disposition; when the remaining choice is between dispositions, put it to `council`
  in **Ask** mode and follow its ruling.
- A third-party limit finding clears the refusal by the order in **Stay Inside Third-Party
  Limits**, and is verified by the per-run count, per account and per destination, fitting the
  provider's documented limit with room for the runs that overlap it, and by running the affected
  suite twice back to back with neither drawing a refusal.
- A redundant test merges into the survivor of its own classification, and the merge keeps every
  assertion nobody else in that classification makes; only a case disproportionate under
  `test-fixture`'s cost question is removed with its assertion, as **Bring Every Suite Under
  Budget** says.
- A test-only production seam with no non-test caller is removed after its contract has a keeper;
  a baseline test exposing a product defect is repaired at the owner with failing control and
  passing candidate proof.
- A name any naming check reports — a leading article, more than eight words, a numeric status
  code, a restated class noun — is renamed to a label within `test-fixture`'s word budget; the
  condition the name lost moves into the docstring, and a rename that would leave fewer than two
  words takes a hand-chosen label rather than the mechanical residue.
- A layout finding moves to the pattern `test-fixture`'s ownership rules select; an even split
  between equally valid patterns is settled as `test-fixture` settles a layout tie.
- A coverage gap is closed by the test that proves it, and a misplaced test moves between suites.
  Every added or rewritten test follows `test-fixture`'s validation through existing tools.
- A construction finding moves the construction to the suite's shared home and reads identities
  from the canonical fixtures. A factory-content finding deletes the override or the provider, or
  folds the repeated shape into one generator taking the value that varied; the model's default and
  the plain attribute already say the same thing.
- A test utility found in application code moves to the shared test-utilities owner with every
  consumer, in the same change. An application symbol tests only exercise as their subject is
  deleted with those tests, never moved.
- A suite-configuration finding takes the setting the cited section of `test-fixture`'s suites
  reference states; a skip or xfail that is a finding is repaired and unskipped, or deleted with
  its deletion evidence.
- A foreign-domain finding rewrites the data in the mirrored source's own nouns where it has them
  and in neutral placeholders where it is a library with none; a fixture that introduced the noun
  is the finding, fixed once for every test it serves.
- A doubles finding runs the real code; one that needs the database follows the coverage
  disposition above and is counted there; a fault the real path cannot produce keeps its double at
  the declared seam, with the fault named in the ledger.

## Declared Outcome: The Slowest Tests Are Posted

**This run posts one cost comment on each of its pull requests.** Include available suite wall times
against the budget and rank up to ten tests and ten fixtures where existing reporting attributes
their costs. Mark unavailable attribution unmeasured under `test-fixture`'s procedure. It is a declared
outcome of the skill, so
invoking the skill authorizes that comment under the comment rules, and it is posted whether the run
brought every suite under budget or not.

The comment exists because a duration needs one place a later run can read. The diff cannot show a
number and a report in chat is gone by the next session; one comment, updated in place, gives the
next run its baseline and shows anyone deciding what to cut where the time goes.

Post it once per pull request, updating the same comment when a later push changes the numbers
rather than adding a second; the draft pull request carries the final ranking against the baseline.
Give it measured durations and unmeasured dispositions, without narration of the repairs the body and diff already carry.

## Report Additions

- per suite: wall time before and after against the budget, and unmeasured suites with the reason;
- per suite: available test call totals against wall time, with unattributed costs marked unmeasured;
- each case folded or made cheaper for disproportionate runtime, with what it proved and where that
  now lives;
- per suite: tests removed, parametrized, renamed, moved, and added;
- skip and xfail marks resolved, and each suite-configuration section's result;
- each source line the coverage comparison showed dropped, and what restored it;
- each application symbol only tests consumed, moved as a test utility or deleted as dead code;
- per suite, foreign domain nouns removed and the fixtures that carried them;
- the coverage map by test, with gaps closed and gaps recorded;
- per provider, account and destination: real calls per run before and after, and the refusals
  the baseline drew;
- determinism corrections; per suite, doubles of repository-owned code removed, moved to the suite
  with the real boundary, or retained with the fault they inject; and declared seams no test used
  before the run;
- each cut and the deletion evidence that justified it.
