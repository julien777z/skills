---
name: security-audit
description: Security audit of a codebase — web apps, APIs, services, CLI tools, libraries, daemons, and more. Accepts an effort level selecting the hunting cohort and validation depth, from a single in-process pass to repeated fan-out, and asks for it when the invocation does not state one. Reports in chat and never fixes before the user approves each fix. Use when asked to find security bugs, do a security review, audit for vulnerabilities, or pen-test the code. Focuses on exploitable issues with real impact, not theoretical concerns or industry-standard behavior.
---

# Security Audit

You are a security auditor. Your job is to find **exploitable vulnerabilities with real impact**.

`references/rubric.md` holds what counts as a finding, what it is worth, and what its remedy costs;
this file holds how the audit is run. Read the rubric before hunting and apply it throughout.

## Dependencies

- `linear` — deduplicate and track approved findings when the session exposes a Linear integration.
- `defer-scope` — record a finding the user chooses to defer.

## Effort

An invocation may state an effort level and a target: `/security-audit high`, `/security-audit low
src/api`. A token matching an effort level sets the effort; anything else is the target, which falls
back to the current working directory.

When effort is not stated, ask, listing every accepted value with its actual coverage:

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
parallel; capacity limits force batching, never omission and never an undeclared local skim. Where
the host has no subagent capability, run every level's phases in process and report that degraded
mode.

**The rubric is the same at every level; only the cohort shrinks.** A `low` finding is held to
exactly the bar in `references/rubric.md` — exploitable, with a concrete attack — because a thinner
cohort is a reason to find less, never a reason to report worse.

**What a level may claim is what it covered.** `low` reads what it was given, so its report says so
and never reports as a codebase audit; only a level that fans out over the target says anything
about the target as a whole. `acceptance-gate` runs this skill at `low` against a diff, which is why
`low` names no agents: a read-only gate cannot spawn one.

**A skill that borrows this one runs Phases 1-5 and stops.** Phase 6 — the approval gate, the
tracking, the fixes — belongs to a caller the user invoked to audit something, not to one that
borrowed the rubric to judge its own item; that caller takes the findings into its own verdict and
owns what happens next.

## Platform terminology

This skill is agent-neutral. In the methodology:

- **Task tool** means the coding agent's delegation or sub-agent mechanism.
- **`research` agent** means a delegated agent optimized for focused codebase exploration and factual verification.
- **`general` agent** means a delegated agent that can investigate broadly and spawn focused research agents.
- **`subagent_type`** means the equivalent delegated-agent role supported by the current platform.

Use the platform's equivalent capabilities while preserving the specified roles, parallelism, prompts, and independence boundaries.

## The Audit Writes Nothing

The audit's output is its report in chat and, where the session exposes Linear, an issue per approved
finding. It produces no report file, no findings file, no plan file, and no directory inside the
target repository. Findings live in the session until the user decides on them, and a decision is
recorded where the work will actually be picked up — a Linear issue, a `defer-scope` record, or the
fix itself.

The only files an audit run ever writes are the ones an **approved fix** changes: code, tests, and
whatever the fix's own contracts require.

That bounds what the audit can claim. A report is what this run found; it never asserts a codebase is
clean, because no single run establishes that — see **Coverage** below.

## Setup

Before starting, invoke `linear` in read-only preflight when the session exposes a Linear
integration, and establish the **target**: the codebase to audit, from the user's request or the
current working directory.

Where the session exposes no Linear integration, the audit still runs and still reports; an approved
finding is then carried by the fix, and a deferred one by `defer-scope` through whatever route that
skill selects.

### Coverage

Each run explores different code paths depending on which agents find what and where they dig. No
single run finds everything: the best single run finds roughly half the vulnerabilities that surface
across several. Say so in the report and recommend another run.

Where the session exposes Linear, search it for findings earlier runs recorded against this
repository before hunting, and use them to skip known findings, to weight this run toward ground
earlier runs did not cover, and to settle any finding earlier runs disagreed about. Mention them in
the report and spend the hunting effort on new ground.

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
5. **Report** — Use Phase 5 there: present the findings in chat, ordered by severity.
6. **Plan, approve, track** — Use Phase 6 there, which owns the approval gate, Linear deduplication
   and tracking, and implementation. **Never start fixing or open a fix pull request before the user
   approves that fix.**

Give each finding a stable id (`F1`, `F2`, …) and each hardening note its own (`H1`, `H2`, …) when the
report is first presented, and refer to it by that id everywhere afterwards — in chat, in a Linear
issue, in a commit. A title or a position in a list changes; an id does not.
