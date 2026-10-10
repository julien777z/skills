---
name: security-audit
description: Must be used before writing or changing code that crosses a trust boundary — input handling, authentication, authorization, sessions, secrets, cryptography, deserialization, file paths, subprocesses, outbound requests, templates — and for any security review of a branch, pull request or pending changes, or security audit of a codebase at a stated effort level. Its rubric owns what counts as an exploitable finding, the precedents that rule false positives out, how code is built safely, and the smallest fix; the skill reports, and its caller owns what happens to each finding. Use when asked to find security bugs, do a security review, audit for vulnerabilities, or pen-test the code.
short_description: 'Security guidance for writing code, reviewing a change, and auditing a codebase.'
---

# Security Audit

You are a security auditor. Your job is to find **exploitable vulnerabilities with real impact**.

`references/rubric.md` holds what counts as a finding, what it is worth, which precedents rule a
finding out, how code that crosses a trust boundary is built, and what a remedy costs. This file
holds how that judgement is applied: while writing code, over a change, and over a codebase. Read
the rubric whole before any of them and apply it throughout.

## Dependencies

- `subagent-selection` — route every agent a level names through a subagent of the running session.

## While Writing Code

Before writing or changing code that crosses a trust boundary — input handling, authentication,
authorization, sessions, secrets, cryptography, deserialization, file paths, subprocesses,
outbound requests, templates — read the rubric and apply **Building It Safely** to every line the
change writes. A finding in those lines is the change's own defect: it is fixed in the change, as
`code-simplify` fixes its findings, never reported for a later decision.

## Diff Review

A security review of a branch, a pull request or pending changes reviews the change, not the
codebase. Its target is the merge-base diff against the repository's default branch plus any
untracked files the branch adds, read with the callers, sinks and trust boundaries each changed line
reaches, so a trace can run past the hunk. It reports only what the change adds or makes reachable,
never a pre-existing finding the change does not touch.

It runs every phase at the effort stated, over the changed lines and what they reach. A finding in
lines the running task wrote is fixed in that task's change; any other finding is reported to the
caller.

## Effort

A **Diff Review** or codebase audit may state an effort level and a target: `/security-audit high`,
`/security-audit low src/api`. A token matching an effort level sets the effort; anything else is
the target — a path, or a branch, pull request or pending changes for **Diff Review** — which falls
back to the current working directory.

When a review or audit states no effort, ask, listing every accepted value with its actual coverage:

- `low` — One pass over the target against the rubric, with no delegated agents at all.
- `medium` — Recon inline, one hunter per attack class recon surfaced, one validator per finding.
- `high` — Recon fanned out, two hunters on the riskiest classes and one elsewhere, then a refuter
  and an independent verifier per finding, repeated until a round finds nothing new.

Keep each description to one or two sentences, and never replace them with vague labels such as
"quick" or "thorough". Ask through the host's structured question tool when it has one and a plain
chat question otherwise, and launch nothing until the answer arrives.

When the host cannot ask, as in a non-interactive or automated run, fall back to `medium` and say the
fallback was used.

| Effort | Recon | Hunters | Validation | Independent verification |
|---|---|---|---|---|
| `low` | Inline | Inline, one pass | Inline | Inline |
| `medium` | Inline | 1 per class recon surfaced | 1 validator per finding | Inline |
| `high` | 3 agents | 2 on the riskiest classes, 1 elsewhere | 1 refuter per finding | 1 verifier per finding |

At `low` every phase runs in process. From `medium` upward, launch the agents each phase names in
parallel; capacity limits force batching, never omission and never an undeclared local skim. Each
agent a level names is launched as `subagent-selection`'s **Dispatch** section directs.

**The rubric is the same at every level; only the cohort shrinks.** A `low` finding is held to
exactly the bar in `references/rubric.md` — exploitable, with a concrete attack — because a thinner
cohort is a reason to find less, never a reason to report worse.

**What a level may claim is what it covered.** `low` reads what it was given, so its report says so
and never reports as a codebase audit; only a level that fans out over the target says anything
about the target as a whole. `acceptance-gate` runs this skill at `low` against a diff, which is why
`low` names no agents: a read-only gate cannot spawn one.

**A skill that borrows this one takes the findings into its own verdict.** It writes no findings
file and owns what happens to each finding.

## Platform terminology

This skill is agent-neutral. In the methodology:

- **Task tool** means the coding agent's delegation or sub-agent mechanism.
- **`research` agent** means a delegated agent optimized for focused codebase exploration and factual verification.
- **`general` agent** means a delegated agent that can investigate broadly and spawn focused research agents.
- **`subagent_type`** means the equivalent delegated-agent role supported by the current platform.

Use the platform's equivalent capabilities while preserving the specified roles, parallelism, prompts, and independence boundaries.

## What The Audit Writes

The output is a report: one findings file in the session's scratch directory, sent to the user with
the chat summary. Nothing is written inside the target repository, and the audit changes no code.
What happens to a finding is its caller's: a task fixes a finding in its own change, and
`security-doctor` fixes a codebase's findings through the remediation plan the user approves.

A report is what this run found; it never asserts a codebase is clean. Each run explores different
code paths depending on which agents find what and where they dig, and the best single run finds
roughly half the vulnerabilities that surface across several. Say so in the report and recommend
another run.

## Workflow

Every level runs every phase; **Effort** above says with what cohort.

1. **Recon** — Run Phase 1 from [reconnaissance](references/reconnaissance.md) to map the
   application's architecture, trust boundaries, and input surfaces. Hold the architecture summary in
   the session; Phase 2 agent prompts are built from it.
2. **Hunt** — Use [hunting](references/hunting.md) for orchestration and methodology; select scopes
   from [attack classes](references/attack-classes.md).
3. **Validate** — Use Phase 3 in [validation and reporting](references/validation-and-reporting.md)
   to consolidate duplicates and independently try to disprove every finding, against the rubric's
   **What A Surviving Finding Has Been Put Through**.
4. **Verify independently** — Use Phase 4 there: a fresh agent per surviving finding checks every
   factual claim against the source.
5. **Report** — Use Phase 5 there, then stop: the report is the audit's result.

Give each finding a stable id (`F1`, `F2`, …) and each hardening note its own (`H1`, `H2`, …) when the
report is first presented, and refer to it by that id everywhere afterwards — in chat, in a plan,
in a commit. A title or a position in a list changes; an id does not.
