---
name: code-review
description: Review a pull request or current changes with independent reviewer lenses, validated findings, and severity-rated results. Use when the user directly asks for a code review, or when `review-pass` or `incident` delegates to it; never on your own initiative.
short_description: 'Code review a pull request or the current working changes with independent reviewer lenses, validated findings, and severity-rated results.'
---

# Code Review

Provide a code review for the selected target.

`references/rubric.md` holds what the review judges by; this file holds how it is run.

For changed Python files, first run this skill's `scripts/paragraph_candidates.py` with the
reviewed files as arguments. It lists adjacent statement pairs where a completed guard meets
setup, one guard meets the next, a derived value meets its validation, or an operation meets the
next stage. Inspect every candidate in numbered source and report missing blank lines as Rules
findings even if the formatter accepts the file. Apply the same stage-boundary check by reading
source in other languages. The Rules receipt lists every candidate pair and its disposition,
including when another finding exists. A receipt without that list is incomplete and must be
rerun. Any pair described as separate stages without a blank line is a Rules finding, even at low
effort; it cannot remain only in the coverage receipt. The coordinator rejects and reruns a receipt
that names such a pair but omits it from the findings list.

The Rules receipt also lists every conditional choosing among a fixed set of string statuses,
including log-only values. Inline literals bypassing the language's named finite-state type are
findings. Use the representation required by the applicable language rule and preserve externally
fixed values in that type. A receipt without the conditional list is incomplete and must be rerun.

## Dependencies

- `subagent-selection` — return model capabilities for explicit reviewer dispatch.
- `code-simplify` — its `references/rubric.md` is the complete simplification rubric for that review lens.
- `pre-production` — supply the repository's target-contract and staging-data policy.
- `security-audit` — its `references/rubric.md` defines an exploitable finding, its precedents and its remedy, and its attack-class catalogue supplies the Security lens. The review borrows both and never the audit workflow.
- `acceptance-gate` — define the intent statement and gate the fixes the change did not itself
  introduce.
- `agent-lock` — protect local snapshot capture with the exact checkout key.

## Invocation

- Run this skill only when the user directly invokes it, or `review-pass` or `incident` delegates it. `review-pass` supplies high effort and fix mode; do not ask for standalone review options on that route.

```
/code-review [low|medium|high|xhigh|max|ultra] [fix] [comment] [<target>]
```

## Arguments

Arguments may appear in any order, and the `--` prefix on a mode is optional: `fix` and `--fix` mean the same thing, as do `comment` and `--comment`. `/code-review medium fix` is a valid invocation.

Read the tokens as follows:

- A token matching an effort level sets the effort.
- A token matching `fix` or `comment`, with or without a leading `--`, enables that mode.
- Any remaining token is the `<target>`. To review a ref whose name collides with a reserved word, pass it as a fuller ref such as `refs/heads/fix`.

**Ask for anything the invocation did not state, before doing anything else.** The invocation states two things independently, and each unstated one is a question:

- **Effort** — stated by an effort token. Otherwise ask which level to run.
- **Modes** — stated by the presence of any mode token, which turns the named modes on and leaves the unnamed ones off. When no mode token appears at all, ask which modes to enable.

So a bare `/code-review` asks both, `/code-review high` asks only about modes, `/code-review fix` asks only about effort, and `/code-review high fix` asks nothing and runs. A `<target>` never triggers a question; it has a defined fallback when absent.

When asking for effort, list every accepted value explicitly and describe its actual coverage and validation depth:

- `low` — Run one Rules and one Bugs lens with inline validation for a quick review of small, low-risk changes.
- `medium` — Run one Rules, one Bugs, and one Simplification lens, plus one Security lens, with inline validation.
- `high` — Run one Rules, two independent Bugs, and one Simplification lens, plus one Security lens, then have one standard validator try to refute every finding.
- `xhigh` — Run two independent Rules and Bugs lenses plus one Simplification lens and one Security lens, then use two standard validators per finding with majority rule.
- `max` — Run two Rules, three Bugs, two Simplification, and two Security lenses in one pass, then use three deep refuters per finding with majority rule.
- `ultra` — Repeat the `max` cohort until two consecutive rounds find nothing new, using the same three deep refuters per finding.

Keep each description to one or two sentences. Never summarize the effort values as a range such as `low`–`ultra` or replace the concrete descriptions with vague labels such as "quick," "thorough," or "broad."

Ask using the host's structured question tool when it has one and a plain chat question otherwise. Do not resolve a target, read a diff, or launch a reviewer until the answer arrives — guessing wrong means either a shallower review than wanted or unrequested edits and comments.

When the host cannot ask, as in a non-interactive or automated run, fall back to `medium` effort with both modes off and say that the fallback was used. Without fix mode this skill edits code only through the Pre-Push Gate's own fixes, committed alone as Step 1 says; without comment mode it never writes to GitHub beyond reads.

**Scope.** Anchor every finding as `references/rubric.md` — Scope directs, `OUTSIDE_DIFF` included.

## Agent assumptions

State these verbatim to every subagent launched:

- All tools are functional and will work without error. Do not test tools or make exploratory calls.
- Only call a tool when it is required to complete the task. Every tool call needs a clear purpose.
- Return findings as data. The final message is the return value, not a message to a human.

## Subagent selection

Invoke `subagent-selection` and choose its **standard** capability level for every reviewer,
validator, and refuter. The `fast`, `standard`, and `deep` labels elsewhere describe assignment
depth, not model capability levels: mechanical lookup, contextual review, and adversarial
investigation respectively.
Effort still determines the cohort and validation depth. Rating, deduplication, fix decisions,
and writing fixes stay with the orchestrator.

Use the dependency's explicit dispatch instructions. Record each launched reviewer's catalogue state,
exact dispatch identifier, assignment state and host receipt in the review evidence. If the standard capability
level is unavailable, report the limitation; do not silently substitute another tier, model version, or the
orchestrator's model. Every lens, validator and refuter this skill hands to a subagent is routed as
`subagent-selection`'s **Dispatch** section directs.

## Step 1 — Resolve the target

Make a todo list first.

When `<target>` is given — a PR number, PR URL, `owner/repo#N`, `owner/repo/pull/N`, a git ref range, or an immutable local `targetSnapshot` — review exactly that. Never substitute a different PR. An explicit target remains immutable for review; when authorized fix mode finds a defect, writes are limited to the verified writable checkout of that exact PR head branch or local snapshot route.
For an explicit local `targetSnapshot`, resolve its ledger entry and durable private artifact before any target derivation, context read, lens dispatch, or fix. Verify its route, repository, full identity, and digests, then materialize its cells in a fresh pristine task-owned checkout; a missing or invalid artifact is an incomplete retrieval, never permission to use the ambient checkout.

Otherwise work from the current branch. Detect the repository, the remote default branch, the current branch, the worktree state, and any open PR whose head branch is exactly the current branch.

What happens next turns on whether the branch already carries commits of its own — commits beyond the remote default branch — not on its name.

**When it carries none**, the work has nowhere to live yet. This covers the default branch, a detached HEAD, and a freshly created feature branch still level with the default branch. Give the work a home:

1. Separate the intended changes from unrelated worktree changes. If which changes are intended is ambiguous, stop and ask before staging anything.
2. When the current branch is the default branch or HEAD is detached, create a collision-free branch named for the change, following whatever branch-naming convention the repository already uses. When already on a non-default branch, keep it.
3. Stage only the intended changes, commit them with a concise message, and push with upstream tracking through `execute-task`'s **Pre-Push Gate**.

**When it already carries commits**, leave the worktree alone. Never stage and never commit — uncommitted work stays uncommitted and is reviewed in place. Push existing local-only commits with upstream tracking, through `execute-task`'s **Pre-Push Gate**, so the branch exists on the remote. The gate's own fixes are the one commit made here: stage only the gate's edits, commit them alone, and leave every uncommitted worktree change untouched.

Then open a **draft** PR against the remote default branch when no open PR already has this branch as its head. Committing the first change above is what makes this always possible: a branch reaches this point with at least one commit, so there is never a state where a review runs with no PR behind it. If there is genuinely nothing to review — no commits and no uncommitted changes — stop before any of this.

The review target is the complete `merge-base(default, HEAD)..HEAD` diff plus any uncommitted intended changes — every commit on the branch, not only the latest push. If that is empty, stop and report there is nothing to review. Record the PR number, base branch, head branch, and full head SHA, or the ref range. Before dispatching any lens or validator, resolve an explicit pull request's remote head and base as authoritative and materialize that exact commit in a read-only checkout or immutable remote tree; an unrelated local checkout does not block that review. In fix mode, also resolve and verify a task-owned, clean writable checkout of that PR head and branch before applying corrections; its branch, HEAD, tree, and tracked remote must equal the resolved PR, and create one when none qualifies. Then freeze an immutable `targetSnapshot` containing its route, merge base and candidate head/tree. A PR snapshot also records its resolved base ref and exact base SHA. An explicit-PR snapshot contains only that resolved remote material. Before freezing a local-diff snapshot, acquire `agent-lock` for `checkout:<absolute-path>`, record and
check its receipt, resolve the intended-entry selection at the patch-partition and hunk level and stop for user resolution whenever it is ambiguous. In particular, stop if a selected hunk shares an index, modified-worktree, or untracked-worktree cell with unrelated content; unrelated dirty work is excluded. Classify every selected cell under the repository's secret policy before retaining bytes: never serialize or dispatch secret-bearing bytes in ledger evidence; exclude an unneeded secret cell or hold until an authorized secret-safe review input exists outside the ledger. The local artifact is task-private durable evidence owned through `session-ledger`: serialize the complete eligible target-patch partitions and each selected path's relative path, status, and separate `HEAD`, `index`, and `worktree` cells; every cell records presence, mode, bytes when present, and content digest. Retain the intended-selection, layered-manifest, and artifact digests; write and read back the artifact in private evidence storage; and record its absolute locator and full identity in the task ledger, then release the capture receipt with `--resource-idle`. Every post-acquire ambiguity, hold, failure, cancellation, or other exit confirms the checkout is untouched and releases its owned receipt with `--resource-idle`. Rehydrate only into a fresh pristine task-owned checkout, verify retained cells and expected absence of untracked residue, and remove residue before every local review or re-gate. Pass its identifier and exact material to every worker; receipts, test results, validation verdicts, and later attestations derive from it, never from a mutable working tree.

In every review round, give each dispatched reviewer and validator the merge-base SHA, current head
SHA, complete pull-request diff, and complete changed-file list. When a previous reviewed head
exists, also give the diff from that head to the current head so recent fixes receive focused
attention. That incremental diff supplements the full pull-request target; never substitute the
latest commit or fix diff for it. The one exception is a delta `review-pass` delegates: that delta is
the review target, and the complete pull-request diff is the context its reviewers read. Keep that
complete context distinct from each lens's analysis slice: the exact changed hunks, files, and
operations it evaluates, plus every supporting input whose semantics it uses. A reviewer may read
context without adding it to its analysis slice, but material it evaluates, uses as evidence, or
relies on for a conclusion belongs in that slice. Record both manifests so a later pass can retain a
receipt only when its actual analysis remains valid.

Classify whether the target is non-runtime before choosing validation. A target is non-runtime when its complete diff does not change executable source, package or dependency definitions, tests, runtime configuration, CI workflows, generated runtime artifacts, or another contract that changes executed behavior. This is semantic rather than path-based: agent instructions, documentation, policies, static metadata, and non-executable configuration can live anywhere. Validate a non-runtime target with the checks appropriate to its artifacts, exact contents, and `git diff --check`; do not run application tests or query or wait for CI.

When a runtime change names an external provider resource or permission — a tag, OAuth scope, credential identifier, repository, application, or network target — treat the provider object as a reviewed input. Read the live object using the least-privilege authorized surface and compare its resolved identity, owner and grants with the intent statement. Permission to mutate a resource does not establish that it is the intended resource. Trace selectors and configuration through to the actual account, application, datastore or recipient; a label, alias, package location or successful access check does not prove that binding. Source-only consistency, a previous successful run, and a green static check do not establish that contract. A reviewer may mark the change clean only after this verification passes. If verification is blocked, record the concrete blocker and leave the review incomplete.

When the target is a PR, check eligibility and stop when any of these hold:

- The PR is closed or merged.
- The PR does not need review, such as an automated dependency bump or a change that is trivially correct.
- Comment mode is on and this skill already posted a review for the current head.

Draft status is never a reason to skip — this skill opens drafts by design. The already-reviewed gate applies only to comment mode, because its purpose is avoiding duplicate posts. A chat-only invocation always reports the current review result, even when a similar comment already exists on the PR.

Use the host's pull-request tools when available, with `gh` as a fallback. Do not use web fetch for GitHub data. GitHub reads are always allowed.

## Step 2 — Build review context

Discover repository guidance from whichever of these exist, scoping each file to its own directory subtree so a nested file governs only its descendants:

- `.agents/rules/**`
- `AGENTS.md`, at the root and in any changed directory
- `CLAUDE.md`, at the root and in any changed directory
- `.cursor/rules/**`
- `.github/copilot-instructions.md`

When a repository publishes a canonical source and generated per-tool mirrors of the same rules, read the canonical source only. Reading both double-counts every rule.

Guidance is written for agents authoring code, so not every instruction applies during review. Identify the guidance that applies to each changed file from its front matter, scope, or always-apply status. Give the Rules lens the applicable rules and provide them as context to the other lenses and to fix mode.

Rule and skill files are review criteria unless the selected target changes canonical definitions.
In that case, review those changed files as non-runtime content against their owning guidance. Exclude
rules and skill definitions outside the selected target, and do not report unrelated guidance.

Summarize the changed files and produce the intent statement as `acceptance-gate` defines it, unless the caller supplied one. Reconcile it with the user's instructions, accepted decisions and repository guidance independently of the implementation and pull-request description; neither an author's claim nor tests agreeing with the code approve a different contract. Before assigning lenses, resolve the affected-repository map required by `code-simplify`'s **Trace Changed Flows**. Give every reviewer and validator that map and the complete intent statement, including its owned-boundary receipt, alongside the target's title, description and change summary. Missing intent or binding evidence is incomplete review context, never permission to infer the intended design from the diff.

## Step 3 — Run reviewer lenses

| Lens | Capability | What it does |
|---|---|---|
| **Rules** | standard | Check every applicable rule against the changed lines and produce a ledger of rule → files checked → violation or clean |
| **Bugs** | deep | Find correctness, data-loss, security and authz, performance, and user-facing behavior defects, each with a concrete trigger |
| **Simplification** | deep | Run the `code-simplify` skill as its rubric over the scope — redundancy, a module named or placed wrong, a file past a healthy size, a value modelled one way here and another way in a sibling |
| **Security** | deep | Apply `security-audit`'s rubric and attack-class catalogue over the changed lines — injection, authentication and authorization defeats, sensitive data reaching a log or response, unsafe deserialization, secrets in source |

Effort selects the cohort and the validation depth:

| Effort | Rules | Bugs | Simplification | Security | Validation |
|---|---|---|---|---|---|
| `low` | 1 | 1 | – | – | Inline |
| `medium` | 1 | 1 | 1 | 1 | Inline |
| `high` | 1 | 2 | 1 | 1 | One **standard** validator per finding |
| `xhigh` | 2 | 2 | 1 | 1 | Two **standard** validators per finding, majority rules |
| `max` | 2 | 3 | 2 | 2 | Three **deep** refuters per finding, majority rules |
| `ultra` | 2 | 3 | 2 | 2 | Three **deep** refuters per finding, majority rules |

At `low` and `medium` the lenses may run inline in a single pass, and depth on the riskiest changed files beats exhaustive coverage of trivial ones. From `high` upward, launch one distinct subagent per lens in parallel; capacity limits force batching, never omission and never an undeclared local skim.

`ultra` runs the `max` cohort repeatedly, stopping only after two consecutive rounds surface no new confirmed finding. Every other level runs its cohort once.

**A lens that keeps coming back clean retires.** Whenever the cohort runs more than once in the same logical review — `ultra`'s own loop, and every fix-triggered re-review of the same pull request or ref range — track each lens's consecutive clean rounds across the follow-up invocations. A lens that has returned no confirmed finding for **two consecutive rounds** is excluded from every later round of that logical review, and its last coverage receipt stands as its result. Count a round as clean for a lens only when it completed: a lens that errored, timed out, or reported partial coverage has not earned a clean round, and its counter holds rather than advancing.

A confirmed finding from a lens resets its counter to zero, so a lens that goes quiet and then catches something on a later round starts earning its way out again from scratch. Refuted findings do not reset it — only findings that survive Step 4. Invalidating a retired lens's receipt reactivates that lens and resets its counter to zero before the next cohort; retirement never outlives the material or inputs its receipt covered.

Name the retired lenses and their round counts in the report, so a reader can tell a lens that found nothing twice from one that never ran. Persist the counters with the logical review's receipts. A new target or an invocation unrelated to the active fix loop starts every lens at zero; a follow-up invocation required by fixes to the same target does not.

The **Security** lens does not carry its own rubric: give it `security-audit`'s complete rubric and
attack-class catalogue for the current target, so the two stay one source of truth. Borrow the
*rubric*, not the *workflow* — do not run the audit skill's own phases or write its findings file.
This lens applies the rubric to the review scope and returns ordinary review findings.

The **Simplification** lens does not carry its own rubric: dispatch it to the `code-simplify` agent, whose `references/rubric.md` is the complete rubric, so the two stay one source of truth rather than two drifting copies. Give it the same target and its affected-repository map, then one instruction this skill adds — `code-simplify` resolves a scope to the diff *plus* whole files *plus* sibling modules, and it should keep reading all three, but every finding it returns must still anchor to a line this target added or removed. Reading a sibling is how it sees that a new module is misnamed, sits in a package that does not own it, or models a value the codebase already models another way; unrelated sibling debt is not this review's finding. However, related behavior left behind by a newly introduced or promoted owner is an incomplete ownership move: anchor the finding to the new boundary, and include the unchanged implementations and consumers needed to complete it.

Require the Simplification receipt to satisfy the `code-simplify` rubric’s **Trace Changed Flows** for each changed operation, including its affected-repository map and one disposition per candidate. Reject and rerun an otherwise clean receipt that omits that evidence, leaves a related implementation outside its claimed owner, or assumes the reviewed repository is the complete system; an inventory alone is incomplete.

When the target introduces a public concept, require the Simplification receipt to compare its
interface and owner with existing public concepts serving the same purpose, and to say whether it
belongs as a variant under an existing concept or needs an independent contract. A clean receipt
without that assessment is incomplete; reject and rerun it even when the new implementation itself
has no duplicate code.
For a variant, require the receipt to propose the resulting single public registry, command, and
package owner where those surfaces apply, and to name the consumers that must move. A receipt that
only proposes sharing low-level helpers while keeping parallel public surfaces is incomplete.

When a cohort calls for more than one reviewer of a lens, assign each a distinct concern within
the complete target. One Bugs reviewer can trace changed behavior through callers while another
follows failure and recovery paths through consumers. Each still reads the context needed to catch
a cross-boundary defect, and reviewers do not see one another's output. A second reviewer asked the
same undifferentiated question adds no coverage receipt.

Require each Rules receipt to include its complete rule ledger. A clean Rules receipt without the applicable rules, checked files, and disposition for each rule is incomplete and must be rerun.
For a changed ownership, lifecycle or scope boundary, assign a Bugs reviewer to compare the
owned-boundary receipt with the actual selectors, configuration, permissions and affected tests.
Its coverage receipt names the evidence for each constraint and the counterexample it checked;
tests mirroring an incorrect configuration do not establish the intended boundary. Reject a clean
receipt that omits this comparison or substitutes the author's design claim for an accepted user
requirement.
Every lens and validator whose conclusion might be retained records the reviewed head and merge-base
identities, a target-diff identity covering intended committed, staged, unstaged, and untracked
content, an analysis-slice manifest, and a supporting-input manifest. Each slice and input entry
carries an immutable locator and canonical content identity or digest, so a later pass can compare
the actual bytes it reviewed even when the target contained uncommitted changes.

From `high` upward, each reviewer returns a coverage receipt with its lens and assigned concern, the reviewed head SHA,
the complete changed-file list it received as context, its analysis-slice and supporting-input
manifests, the exact rule and rubric inputs it used, its completion status, and a flat list of
findings. Each finding carries path, line, anchor (`RIGHT` for added or current changed lines,
`LEFT` for removed or base changed lines, or `OUTSIDE_DIFF` for an exact current line with no
faithful diff anchor), a concrete trigger, and its reasoning.

For `ultra`, deduplicate each round against every finding seen so far, not only against confirmed ones, or rejected findings resurface every round and the loop never converges.

If the user gives a new task while reviewers are running, rebuild the complete context inventory,
then compare each receipt's analysis slice and every rule, rubric, dependency, generated contract,
configuration, workflow, and document input whose semantics that lens used. A changed target diff
invalidates a receipt only when it intersects that lens's analysis slice. A changed supporting input
invalidates each lens whose analysis depends on it, even when no source file changed. A changed
complete-context manifest alone does not invalidate a receipt, but a receipt cannot call material
context-only when it evaluated, used as evidence, or relied on it. Interrupt and rerun only the
invalidated lenses after the new task completes; retain only receipts with byte-identical analysis
slices and supporting inputs. Build a coverage map keyed by every required lens and concern over the
current target snapshot before reporting clean: each applicable lens's slices must cover its target
material, and high review keeps a frozen concern-by-operation matrix for distinct Bugs concerns.
Every applicable concern covers each new operation or records an explicit non-applicability disposition.
Dispatch each missing applicable lens and concern only for material the map leaves uncovered; never carry a receipt forward as a
substitute for coverage of a newly added hunk, file, or operation.

Do not classify validity by file extension or category. A lock file can change executed code, a workflow can change the gate, a rule can create a new violation, and a skill can change a lens rubric. Conversely, an unrelated edit outside the target and its reviewed inputs does not invalidate anything. Record the compared inputs and the receipt decision so a resumed review can prove why coverage still stands.

## Step 4 — Validate findings

Deduplicate findings describing the same underlying issue, then validate each one against the diff as `references/rubric.md` — Validation directs: validators are told to refute, every finding resolves to CONFIRMED or refuted, the rubric lists what is dropped outright, and the one undecidable case — intent absent from the supplied instructions, accepted decisions and repository guidance — goes to the user in the shape step 8 uses for an ambiguous fix.

Require each validator to state the complete resolved target it inspected: the full pull-request range
for PR targets, immutable range for ref targets, or snapshot identity with complete target-diff and
entry identities for local targets; on a later round, also state the incremental range it checked for
the latest fixes. Its retainable receipt carries the same target-diff
identity and analysis-slice and supporting-input manifests, keyed to the findings it refuted or
confirmed. Reject a validation based only on the latest commit, even if the finding sits in that
commit; rerun it against the complete target Step 1 resolves before using its verdict.

## Step 5 — Rate and rank

Assign severity and a category slug as `references/rubric.md` — Severity And Categories defines them.

Rank most severe first and report at most 32 findings.

## Step 6 — Re-gate before reporting

For PR and ref targets, re-fetch the target head and rebuild the complete reviewed-input inventory,
including the resolved base ref, base SHA, and merge base recorded in the active snapshot.
For a local snapshot, reload its ledger-recorded durable private artifact and rehydrate it into a
fresh pristine task-owned checkout before verifying its full identity in the task-owned checkout — route, repository, merge base, candidate head/tree,
target-patch digest, intended-selection, layered entry manifest, and artifact digest — then persist,
read back, and compare a replacement local snapshot. If any identity differs from the baseline, freeze
a replacement `targetSnapshot`. When target material changed, invalidate only
results whose analysis slices intersect changed material; supporting-input-only changes invalidate
all dependent lens and validator receipts. Rebuild coverage and retirement state from retained
attested receipts plus fresh work against the replacement. Retain an earlier-head receipt only after
recording a continuity attestation that identifies its source
receipt and original head, the current head and target-diff identity, recomputed slice/input
identities, and proof that no changed material intersects the slice and every supporting input is
identical. A changed context manifest alone is retained only when the attestation proves the changed
material was not analyzed or relied on. Missing, incomparable, or changed identities require a
rerun. Rebuild the coverage map against the re-gated snapshot and dispatch the applicable fresh
lens for every uncovered target entry before reporting clean. Report the head and inputs actually
reviewed. Never report findings gathered against one target or rubric as though they apply to
another. For a PR target, repeat the Step 1 eligibility check.

Before reporting a clean result at `high` or above, verify that every required lens and concern key has either a complete distinct receipt for the replacement snapshot or a complete earlier-head receipt with a continuity attestation bound to it. Reject missing, failed, duplicate, incomplete, or stale keys and rerun only those lenses. A review without complete coverage must never report `No findings.`

## Step 7 — Report

When the host exposes a structured findings tool, report through it, passing the effort level, and do not also print the findings as prose. Where its schema offers a verdict meaning unverified, leave that value unused — nothing surviving step 4 has one. Prose carries no qualifier either: no "possibly", no "may", no request that the reader go check.

Otherwise report in chat as `## Output` shapes it.

## Step 8 — Fix mode

Only in fix mode. Every reported finding is CONFIRMED, because step 4 refutes everything else.

Fix mode is bound by `references/rubric.md` — Fix Mode and A Fix Inherits The Intent: every CONFIRMED finding gets fixed, severity ranks the work and never selects it, a round is not finished while confirmed findings remain, a test seam never softens a fix, and a fix takes the remedy the change itself would take rather than the shape the change is removing.

Apply `pre-production` to compatibility and stored-data decisions. When its required-data policy
calls for a schema migration, invoke the repository's migration skill, when the skill listing declares
one, for the implementation and validation.

Work findings in severity order:

1. Apply the minimal correct fix. Do not refactor beyond the finding's blast radius.
2. Follow the repository's own rules in the fix itself.
3. When the minimal fix does not resolve the finding, fix its cause. A defect whose root lies outside the diff is still this review's to fix, and a rule the code knowingly breaks is resolved by correcting one of them, not by recording the contradiction. Where two rules genuinely conflict, make the governing rule state the real contract rather than leaving code that violates it.
4. Escalate only a decision that is genuinely the user's: a change to intended product behavior, or a choice between defensible designs that neither the diff nor the guidance settles. Designs that differ only in how the code is built — where shared behavior lives, which repository owns a helper, which mechanism replaces parallel copies — are ranked by `pre-production` and `code-simplify`: apply the one that leaves the fewest mechanisms and report the choice. A reviewer or validator calling a finding an open decision, or a question for the user, is a claim this step classifies, never the classification. Ask the specific question through the host's question tool and act on the answer. An unanswered question is one of only three routes to reporting a CONFIRMED finding unfixed, and the report must say what was asked.
5. Size keeps a confirmed finding out of this round only under the size bar in `references/rubric.md` — Fix Mode; a confirmed defect is fixed here whatever its size. A scope the bar admits is recorded through the repository's deferral mechanism so it outlives the review, and the record is named in the report: a finding described only in the report is not deferred, it is dropped. That mechanism's admission gate decides whether the scope may be recorded at all; a refusal naming fix or do means the finding is fixed here, and one naming close is recorded cancelled with its reason and reconsideration criterion.

**Each fix is committed as its own increment. A working-pull-request fix is pushed and its `execute-task` **Pre-Push Gate** verdict is its gate; a local-snapshot fix freezes a replacement local snapshot and continues its local validation and review loop without pushing.** A pre-existing defect, an `OUTSIDE_DIFF` anchor, a defect the diff inherits, and anything this round considered deferring are the fixes most likely to take the shape the change is removing, because nothing about them was the change's purpose, and the gate reads each against the intent statement. Resolve each flag under `acceptance-gate`'s **Bounds**, retaining the finding and intent through each changed increment and fresh review. A repeated flag is neither a deferral justification nor permission to leave flagged code standing.

Preserve the requested behavior and any unrelated worktree changes. Re-review the fixed lines to confirm each correction holds, then re-report with an outcome per finding: `fixed`, `skipped`, or `no_change_needed`.

Before staging, rerun the Rules lens over the fix diff with the same rule inventory. Resolve every
violation and repeat until its ledger is clean. A remedy a validator proposed carries no authority
of its own; check it the same way as any other edit. Where a fix cannot satisfy both the finding
and a rule, correct the governing rule rather than shipping code that violates it.

After fixing, rescan the affected ownership area and its consumers for the same class of finding,
then apply the target classification from Step 1. For a non-runtime target, validate only the checks appropriate to its artifacts, exact contents, and `git diff --check`; do not run application tests or query or wait for CI. Otherwise, record which local services were already running before local validation. Never stop, restart, reconfigure, or claim ownership of a pre-existing service: another agent or user may be using it. When relevant validation requires local services and any were already running, do not run a competing service-managed test locally. A working-pull-request fix uses CI only at its exact pushed head; when no safe native command is available, CI is its fallback and its draft state records the local-validation limit until `merge-gate`. An unpushed local snapshot runs an isolated native check only when it can do so without disturbing external state; otherwise it records the concrete local-validation limit and remains gated or requires an authorized working-pull-request route. It never uses CI for an unpushed snapshot.

Stage only the fix edits — never sweep in unrelated uncommitted work that Step 1 deliberately left alone — and commit in the verified writable checkout selected for the target, never on the default branch. Push only when that target has a working pull request; a local-snapshot fix creates a replacement local snapshot and remains unpushed unless an authorized working-pull-request route is established. A full re-review is a later phase of the same authorized logical fix review, not a new action-skill invocation: carry forward its receipts and lens-retirement counters, invalidate them against the new reviewed inputs, and rerun the required cohort.

## Step 9 — Comment mode

Only in comment mode. Post one inline comment per unique issue with a faithful changed-line anchor, never duplicates. Collect `OUTSIDE_DIFF` findings in one top-level review comment with permanent blob links to their exact current lines; never attach them to unrelated diff lines.

Each comment states the issue briefly and cites its source; a rule finding must link the rule file. Include a committable suggestion block only when committing it fixes the issue entirely — never for fixes spanning 6 or more lines, multiple locations, or needing follow-up.

Link code with a full SHA, in exactly this shape or the Markdown preview will not render:

```
https://github.com/owner/repo/blob/c21d3c10bc8e898b7ac1a2d745bdc9bc4e423afe/package.json#L10-L15
```

The SHA must be literal; a command substitution such as `$(git rev-parse HEAD)` renders as text. The repo must match the reviewed repo, a `#` must follow the file name, the range is `L<start>-L<end>`, and at least one line of context belongs on each side of the cited line.

Keep the comment brief and free of emoji.

## Output

The chat report takes this shape and nothing else:

```markdown
## Code review

- [High] Short imperative title — path/to/file.py:42 (correctness, CONFIRMED)
  Concrete trigger, impact, and the expected correction. → Fixed | → Not fixed: <reason>

Findings: <count by severity>. Fixed: <count>. Deferred: <count, each with its record>.
Lenses: <completed lens names>. Head: <reviewed SHA>. Rules: <ledger summary>.
```

The chat list carries the five most severe findings. Whenever more than five remain, one file in
the session's scratch directory holds every finding in the same shape and is sent with the report.
The outcome arrow appears only in fix mode. If nothing remains, the list is the single line
`No findings.` and the closing lines stay. When a lens, validator or refuter was reported as not
run under `subagent-selection`'s **Dispatch** section, add one line naming it.

## Constraints

- Outside fix mode, the only permitted mutations — besides the findings file in the session's scratch directory, never in the repository — are creating a branch, committing when the branch carries no commits of its own, committing the **Pre-Push Gate**'s own fixes alone, pushing, and opening a draft PR. Never commit the worktree of a branch that already carries commits.
- Do not fix findings unless fix mode is on.
- Do not post to GitHub unless comment mode is on.
- Do not build, typecheck, or run tests during the review pass. The fix pass runs tests after applying corrections; the review pass never does.
- Do not resolve or create GitHub review threads.
- Do not mark a head as already reviewed outside the comment-mode gate; each invocation reviews the current complete target Step 1 resolves.
