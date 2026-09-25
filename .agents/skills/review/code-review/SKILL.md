---
name: code-review
description: Code review a pull request or the current working changes with independent reviewer lenses, validated findings, and severity-rated results. Establishes a branch and a draft pull request when none exists yet. Accepts an effort level, an optional fix mode that applies the smallest complete correction for each confirmed finding, and an optional comment mode that posts inline review comments, each written with or without a leading double dash. Asks for whichever of effort or modes the invocation did not state. Reports in chat and never posts or fixes unless the matching mode is requested. Use when asked to review a PR or review current changes.
---

# Code Review

Provide a code review for the selected target.

`references/rubric.md` holds what the review judges by; this file holds how it is run.

## Dependencies

- `subagent-selection` — return model tiers for explicit reviewer dispatch.
- `code-simplify` — its `references/rubric.md` is the complete simplification rubric for that review lens.
- `pre-production` — supply the repository's target-contract and staging-data policy.
- A repository-local `security-audit`, when present — its `references/rubric.md` defines an exploitable finding and its remedy, and its attack-class catalogue supplies that lens. The review borrows both and never the audit workflow.
- `acceptance-gate` — define the intent statement and gate the fixes the change did not itself
  introduce.

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

- `low` — Run one Bugs lens with inline validation for a quick review of small, low-risk changes.
- `medium` — Run one Bugs and one Simplification lens, plus one Security lens when the reviewed repository provides its own `security-audit` skill, with inline validation.
- `high` — Run two independent Bugs lenses, one Simplification lens, and one repository-local Security lens when available, then have one standard validator try to refute every finding.
- `xhigh` — Run two independent Bugs lenses, one Simplification lens, and one repository-local Security lens when available, then use two standard validators per finding with majority rule.
- `max` — Run three Bugs, two Simplification, and two repository-local Security lenses when available in one pass, then use three deep refuters per finding with majority rule.
- `ultra` — Repeat the `max` cohort until two consecutive rounds find nothing new, using the same three deep refuters per finding.

Keep each description to one or two sentences. Never summarize the effort values as a range such as `low`–`ultra` or replace the concrete descriptions with vague labels such as "quick," "thorough," or "broad."

Ask using the host's structured question tool when it has one and a plain chat question otherwise. Do not resolve a target, read a diff, or launch a reviewer until the answer arrives — guessing wrong means either a shallower review than wanted or unrequested edits and comments.

When the host cannot ask, as in a non-interactive or automated run, fall back to `medium` effort with both modes off and say that the fallback was used. Without fix mode this skill never edits code; without comment mode it never writes to GitHub beyond reads.

**Scope.** Anchor every finding as `references/rubric.md` — Scope directs, `OUTSIDE_DIFF` included.

## Agent assumptions

State these verbatim to every subagent launched:

- All tools are functional and will work without error. Do not test tools or make exploratory calls.
- Only call a tool when it is required to complete the task. Every tool call needs a clear purpose.
- Return findings as data. The final message is the return value, not a message to a human.

## Subagent selection

Invoke `subagent-selection` and choose its **standard** tier for every reviewer, validator, and
refuter. The `fast`, `standard`, and `deep` labels elsewhere describe assignment depth, not separate
model tiers: mechanical lookup, contextual review, and adversarial investigation respectively.
Effort still determines the cohort and validation depth. Rating, deduplication, fix decisions,
and writing fixes stay with the orchestrator.

Use the dependency's explicit dispatch instructions. If standard is unavailable, report the
limitation; do not silently substitute cheap or the orchestrator's model. When the host cannot
launch subagents, use this skill's existing inline/degraded procedure and disclose missing
independent coverage.

## Step 1 — Resolve the target

Make a todo list first.

When `<target>` is given — a PR number, PR URL, `owner/repo#N`, `owner/repo/pull/N`, or a git ref range — review exactly that and mutate nothing. Never substitute a different PR.

Otherwise work from the current branch. Detect the repository, the remote default branch, the current branch, the worktree state, and any open PR whose head branch is exactly the current branch.

What happens next turns on whether the branch already carries commits of its own — commits beyond the remote default branch — not on its name.

**When it carries none**, the work has nowhere to live yet. This covers the default branch, a detached HEAD, and a freshly created feature branch still level with the default branch. Give the work a home:

1. Separate the intended changes from unrelated worktree changes. If which changes are intended is ambiguous, stop and ask before staging anything.
2. When the current branch is the default branch or HEAD is detached, create a collision-free branch named for the change, following whatever branch-naming convention the repository already uses. When already on a non-default branch, keep it.
3. Stage only the intended changes, commit them with a concise message, and push with upstream tracking.

**When it already carries commits**, leave the worktree alone. Never stage and never commit — uncommitted work stays uncommitted and is reviewed in place. Push existing local-only commits with upstream tracking so the branch exists on the remote.

Then open a **draft** PR against the remote default branch when no open PR already has this branch as its head. Committing the first change above is what makes this always possible: a branch reaches this point with at least one commit, so there is never a state where a review runs with no PR behind it. If there is genuinely nothing to review — no commits and no uncommitted changes — stop before any of this.

The review target is the complete `merge-base(default, HEAD)..HEAD` diff plus any uncommitted intended changes — every commit on the branch, not only the latest push. If that is empty, stop and report there is nothing to review. Record the PR number, base branch, head branch, and full head SHA, or the ref range.

Classify whether the target is non-runtime before choosing validation. A target is non-runtime when its complete diff does not change executable source, package or dependency definitions, tests, runtime configuration, CI workflows, generated runtime artifacts, or another contract that changes executed behavior. This is semantic rather than path-based: agent instructions, documentation, policies, static metadata, and non-executable configuration can live anywhere. Validate a non-runtime target with the checks appropriate to its artifacts, exact contents, and `git diff --check`; do not run application tests or query or wait for CI.

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

Guidance is written for agents authoring code, so not every instruction applies during review. Identify the guidance that applies to each changed file from its front matter, scope, or always-apply status and provide it as context to the selected lenses and to fix mode.

Rule and skill files are review criteria, never review targets. Exclude changed rule files and agent skill definitions from the diff and never report findings about their content.

Summarize the changed files and produce the intent statement as `acceptance-gate` defines it, unless the caller supplied one. Give every reviewer the target's title, description, and change summary so they understand author intent.

## Step 3 — Run reviewer lenses

| Lens | Capability | What it does |
|---|---|---|
| **Bugs** | deep | Find correctness, data-loss, security and authz, performance, and user-facing behavior defects, each with a concrete trigger |
| **Simplification** | deep | Run the `code-simplify` skill as its rubric over the scope — redundancy, a module named or placed wrong, a file past a healthy size, a value modelled one way here and another way in a sibling |
| **Security** | deep | When the reviewed repository defines its own `security-audit` skill, apply that skill's rubric and attack-class catalogue over the changed lines — injection, authentication and authorization defeats, sensitive data reaching a log or response, unsafe deserialization, secrets in source |

Discover Security only under the reviewed repository's `.agents/skills/` tree. An installed shared
skill or a skill from another repository does not qualify. Omit Security without failure when the
reviewed repository has no local `security-audit` skill, and name the omission in the report.

Effort selects the cohort and the validation depth:

| Effort | Bugs | Simplification | Security, if local | Validation |
|---|---|---|---|---|
| `low` | 1 | – | – | Inline |
| `medium` | 1 | 1 | 1 | Inline |
| `high` | 2 | 1 | 1 | One **standard** validator per finding |
| `xhigh` | 2 | 1 | 1 | Two **standard** validators per finding, majority rules |
| `max` | 3 | 2 | 2 | Three **deep** refuters per finding, majority rules |
| `ultra` | 3 | 2 | 2 | Three **deep** refuters per finding, majority rules |

At `low` and `medium` the lenses may run inline in a single pass, and depth on the riskiest changed files beats exhaustive coverage of trivial ones. From `high` upward, launch one distinct subagent per lens in parallel; capacity limits force batching, never omission and never an undeclared local skim. When the host has no subagent dispatch, run the lenses sequentially and report that degraded mode.

`ultra` runs the `max` cohort repeatedly, stopping only after two consecutive rounds surface no new confirmed finding. Every other level runs its cohort once.

**A lens that keeps coming back clean retires.** Whenever the cohort runs more than once in the same logical review — `ultra`'s own loop, and every fix-triggered re-review of the same pull request or ref range — track each lens's consecutive clean rounds across the follow-up invocations. A lens that has returned no confirmed finding for **two consecutive rounds** is excluded from every later round of that logical review, and its last coverage receipt stands as its result. Count a round as clean for a lens only when it completed: a lens that errored, timed out, or reported partial coverage has not earned a clean round, and its counter holds rather than advancing.

A confirmed finding from a lens resets its counter to zero, so a lens that goes quiet and then catches something on a later round starts earning its way out again from scratch. Refuted findings do not reset it — only findings that survive Step 4. Invalidating a retired lens's receipt reactivates that lens and resets its counter to zero before the next cohort; retirement never outlives the material or inputs its receipt covered.

Name the retired lenses and their round counts in the report, so a reader can tell a lens that found nothing twice from one that never ran. Persist the counters with the logical review's receipts. A new target or an invocation unrelated to the active fix loop starts every lens at zero; a follow-up invocation required by fixes to the same target does not.

The **Security** lens does not carry its own rubric: when the reviewed repository has a local
`security-audit` skill, give it that skill's complete core principles and attack-class catalogue
for the current target, so the two stay one source of truth. Borrow the *rubric*, not the
*workflow* — do not run the audit skill's own phases, write its findings files or report artifacts,
or apply its remediation-approval gate. This lens applies the local rubric to the review scope and
returns ordinary review findings.

The **Simplification** lens does not carry its own rubric: dispatch it to the `code-simplify` agent, whose `references/rubric.md` is the complete rubric, so the two stay one source of truth rather than two drifting copies. Give it the same target, and one instruction this skill adds — `code-simplify` resolves a scope to the diff *plus* whole files *plus* sibling modules, and it should keep reading all three, but every finding it returns must still anchor to a line this target added or removed. Reading a sibling is how it sees that a new module is misnamed, sits in a package that does not own it, or models a value the codebase already models another way; unrelated sibling debt is not this review's finding. However, related behavior left behind by a newly introduced or promoted owner is an incomplete ownership move: anchor the finding to the new boundary, and include the unchanged implementations and consumers needed to complete it.

When the target introduces a new abstraction, helper, client, lifecycle, model, or utility, require the Simplification receipt to list its repository-wide reuse searches and the canonical candidates inspected, each related implementation's disposition, and verification that consolidation or replacement actually reached every affected consumer. An inventory alone is not a clean receipt. Apply the same requirement whenever a target adds or changes a search, filter, query, or lookup path, even when it adds no named abstraction: search the owning domain and every existing surface for the same subject, then compare the complete behavior and use the canonical path. Reject and rerun an otherwise clean receipt that omits this evidence.

Duplicated lenses run independently and must not see each other's output; redundancy is the point.

From `high` upward, each reviewer returns a coverage receipt with its lens, the reviewed head SHA, the reviewed changed-file list, the exact rule and rubric inputs it used, its completion status, and a flat list of findings. Each finding carries path, line, anchor (`RIGHT` for added or current changed lines, `LEFT` for removed or base changed lines, or `OUTSIDE_DIFF` for an exact current line with no faithful diff anchor), a concrete trigger, and its reasoning.

For `ultra`, deduplicate each round against every finding seen so far, not only against confirmed ones, or rejected findings resurface every round and the loop never converges.

If the user gives a new task while reviewers are running, compare the complete reviewed inputs: the target diff and every rule, rubric, dependency, generated contract, configuration, workflow, and document whose semantics a lens used. A changed target diff invalidates every receipt that covered the changed material. A changed supporting input invalidates each lens whose analysis depends on it, even when no source file changed. Interrupt and rerun only the invalidated lenses after the new task completes; retain receipts whose target material and inputs are byte-identical.

Do not classify validity by file extension or category. A lock file can change executed code, a workflow can change the gate, a rule can create a new violation, and a skill can change a lens rubric. Conversely, an unrelated edit outside the target and its reviewed inputs does not invalidate anything. Record the compared inputs and the receipt decision so a resumed review can prove why coverage still stands.

## Step 4 — Validate findings

Deduplicate findings describing the same underlying issue, then validate each one against the diff as `references/rubric.md` — Validation directs: validators are told to refute, every finding resolves to CONFIRMED or refuted, the rubric lists what is dropped outright, and the one undecidable case — intent that exists nowhere in the repository — goes to the user in the shape step 8 uses for an ambiguous fix.

## Step 5 — Rate and rank

Assign severity and a category slug as `references/rubric.md` — Severity And Categories defines them.

Rank most severe first and report at most 32 findings.

## Step 6 — Re-gate before reporting

Re-fetch the target head and rebuild the complete reviewed-input inventory. If either differs from the baseline, apply the invalidation rule from Step 3: discard and rerun every receipt whose target material or supporting inputs changed, and retain only receipts proven byte-identical in both respects. Report the head and inputs actually reviewed. Never report findings gathered against one target or rubric as though they apply to another. For a PR target, repeat the Step 1 eligibility check.

Before reporting a clean result at `high` or above, verify that every launched lens returned a complete, distinct receipt for the baseline head. Reject missing, failed, duplicate, incomplete, or stale receipts and rerun those lenses. A review without complete coverage must never report `No findings.`

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
4. Escalate only a decision that is genuinely the user's: a change to intended product behavior, or a choice between defensible designs that the diff does not settle. Ask the specific question through the host's question tool and act on the answer. An unanswered question is one of only three routes to reporting a CONFIRMED finding unfixed, and the report must say what was asked.
5. Size keeps a confirmed finding out of this round only under the size bar in `references/rubric.md` — Fix Mode; a confirmed defect is fixed here whatever its size. A scope the bar admits is recorded through the repository's deferral mechanism so it outlives the review, and the record is named in the report: a finding described only in the report is not deferred, it is dropped. That mechanism's admission gate decides whether the scope may be recorded at all; a refusal naming fix or do means the finding is fixed here, and one naming close is recorded cancelled with its reason and reconsideration criterion.

**A fix for a finding the change did not introduce goes to `acceptance-gate` before it is committed.** A pre-existing defect, an `OUTSIDE_DIFF` anchor, a defect the diff inherits, and anything this round considered deferring are the fixes most likely to take the shape the change is removing, because nothing about them was the change's purpose. Put each round's fixes of that kind to the gate's diff question as one diff, against the intent statement. A flag is reworked once; a second flag reverts that fix and records it through the deferral mechanism with both flags as its reason, unless the pull request is confined to agent configuration, where `acceptance-gate`'s **Bounds** leave the disposition with this run. The change's own findings get no per-fix gate.

Preserve the requested behavior and any unrelated worktree changes. Re-review the fixed lines to confirm each correction holds, then re-report with an outcome per finding: `fixed`, `skipped`, or `no_change_needed`.

Before staging, check the fix diff against applicable repository guidance and resolve any violation.
A remedy a validator proposed carries no authority of its own; check it the same way as any other
edit. Where a fix cannot satisfy both the finding and a rule, correct the governing rule rather
than shipping code that violates it.

After fixing, apply the target classification from Step 1. For a non-runtime target, validate only the checks appropriate to its artifacts, exact contents, and `git diff --check`; do not run application tests or query or wait for CI. Otherwise, run the relevant tests and report their actual output. Before any local validation, record which local services were already running. Never stop, restart, reconfigure, or claim ownership of a pre-existing service: another agent or user may be using it. When relevant validation requires local services and any were already running, do not run a competing service-managed test locally; push the fix, use the pull request's CI checks as the authoritative validation, and wait through the host's event mechanism until those checks reach a terminal result. If no required service was already running and the repository's normal test command can run without disturbing external state, run it; otherwise use CI and state the local-validation limit.

Stage only the fix edits — never sweep in unrelated uncommitted work that Step 1 deliberately left alone — and commit on the current feature branch with a conventional commit message, never on the default branch. When the target is a PR, push so its diff stays authoritative. A full re-review is a later phase of the same authorized logical fix review, not a new action-skill invocation: carry forward its receipts and lens-retirement counters, invalidate them against the new reviewed inputs, and rerun the required cohort.

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
Lenses: <completed lens names and Security omitted when unavailable>. Head: <reviewed SHA>.
```

The outcome arrow appears only in fix mode. If nothing remains, the list is the single line
`No findings.` and the two closing lines stay. In degraded mode, add one line stating that no
subagent dispatch was available.

## Constraints

- Outside fix mode, the only permitted mutations are creating a branch, committing when the branch carries no commits of its own, pushing, and opening a draft PR. Never commit the worktree of a branch that already carries commits.
- Do not fix findings unless fix mode is on.
- Do not post to GitHub unless comment mode is on.
- Do not build, typecheck, or run tests during the review pass. The fix pass runs tests after applying corrections; the review pass never does.
- Do not resolve or create GitHub review threads.
- Do not mark a head as already reviewed outside the comment-mode gate; each invocation reviews the current complete diff.
