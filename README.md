# Skills

Shared agent skills for every repository, in one place.

One canonical copy of each skill lives under `.agents/skills/`. [Agent
Sync](https://github.com/julien777z/agent-sync-action) mirrors them to Claude, Cursor and Codex,
vendors the third-party skills registered in `.agents/external_skills.json`, and `bootstrap/install.sh`
links the result into this machine's user-level roots — so every repository's session sees the same
skills.

## Quick Start

```bash
cd /home/user/skills && chmod +x bootstrap/install.sh && bootstrap/install.sh
```

Add that line to the environment's setup script after the repository is cloned. The script links
each skill into `~/.claude/skills`, `~/.codex/skills`, and `~/.cursor/skills` for whichever of those
roots already exist, and each agent definition into `~/.claude/agents` and `~/.cursor/agents`.
Re-running replaces the links and prunes the ones a removed skill left behind.

## Layout

| Path | Purpose |
|---|---|
| `.agents/skills/<name>/` | One skill: `SKILL.md`, with `references/`, `scripts/`, `assets/`, or `resources/` beside it. |
| `.agents/agents/` | Subagent definitions; the tier each runs on is stated by the skill that launches it. |
| `.agents/external_skills.json` | Third-party skills the workflow installs from [skills.sh](https://skills.sh/). |
| `.agents/.auto_generated/` | Provider mirrors the workflow generates on `main`; never edited by hand. |
| `AGENTS.md` | Repository instructions the workflow generates at the root; never edited by hand. |
| `bootstrap/install.sh` | Links the skills and agents into the user-level roots. |

## Skills

The two groups differ in who starts a skill: a user-invoked one carries
`disable-model-invocation: true` in its front matter and stays off the agent's tool surface until you
name it. Generated from each skill's front matter — edit the skill, not the table.

<!-- skills:start -->

### User-Invoked

These run only when you ask for them by name, such as `/refactor`.

| Skill | What it does |
|---|---|
| [`assume-library-update`](.agents/skills/assume-library-update/SKILL.md) | Write consuming code against a library change that is authored but not yet reachable, when the library is the user's own and this session cannot push to it. |
| [`ci-watch`](.agents/skills/ci-watch/SKILL.md) | Find and watch a GitHub pull request for review findings, investigate each finding, fix and push legitimate issues, and stop once checks are green and review threads are resolved. |
| [`config-doctor`](.agents/skills/config-doctor/SKILL.md) | Reconcile configuration names across every place they are declared, each deployment's own environment included, and remove settings nothing reads or nothing deployed sets. |
| [`defer-execution`](.agents/skills/defer-execution/SKILL.md) | Schedule an unrecorded scope of work on its own branch off the default branch rather than folding it into the change in flight, either after the originating pull request merges or immediately in a worktree. |
| [`dependency-doctor`](.agents/skills/dependency-doctor/SKILL.md) | Reconcile declared dependencies with what the code imports and the checks invoke, for every language the repository builds. |
| [`docs-doctor`](.agents/skills/docs-doctor/SKILL.md) | Find and fix documentation that no longer matches the code. |
| [`execute-defer-scope`](.agents/skills/execute-defer-scope/SKILL.md) | Evaluate and resolve recorded deferrals from Linear and the legacy repository ledger, using the current session or an explicit issue, key, path, pull request, or aggregate scope. |
| [`grade-plans`](.agents/skills/grade-plans/SKILL.md) | Compare, grade, rate, rank, or choose between two implementation plans written for the same goal or original agent prompt. |
| [`guidance-doctor`](.agents/skills/guidance-doctor/SKILL.md) | Audit the repository's agent guidance for what to cut, tighten, or add, against what a current model does unprompted and what the vendors' current authoring guidance says. |
| [`hand-off`](.agents/skills/hand-off/SKILL.md) | Wrap up the current session so its open pull requests can be taken to another session with nothing lost. |
| [`incident`](.agents/skills/incident/SKILL.md) | Restore a broken deployed service using a browser and the repository's deployment skill as needed, deploy and test a fix branch, and merge scoped fix pull requests after one Bugs and Simplification review round. |
| [`legacy-doctor`](.agents/skills/legacy-doctor/SKILL.md) | Find and remove code that tolerates a past the repository no longer has: fallbacks, compatibility branches, kept aliases, silent tolerance, and second implementations of one thing. |
| [`manage-mcps`](.agents/skills/manage-mcps/SKILL.md) | Audit, restore, reauthenticate, and align managed remote MCP connectors across Claude Desktop and Codex when the user directly invokes $manage-mcps, while preserving unknown connectors and permission overrides. |
| [`migrations-doctor`](.agents/skills/migrations-doctor/SKILL.md) | Audit and correct a repository's database migration chains, revisions, registries, and test scaffolding. |
| [`new-doctor`](.agents/skills/new-doctor/SKILL.md) | Create a doctor skill on the shared doctor-protocol for one class of repository hygiene. |
| [`refactor`](.agents/skills/refactor/SKILL.md) | Resolve and confirm a repository refactor scope, use multiple independent reviewers to plan structural improvements, then implement an approved plan. |
| [`schema-doctor`](.agents/skills/schema-doctor/SKILL.md) | Audit and correct unjustified nullability, model complexity, primary-key design, and index design across repository API contracts, serialized schemas, persisted schemas, and the field flows connecting them. |
| [`skill-gauntlet`](.agents/skills/skill-gauntlet/SKILL.md) | Audit installed agent skills across every visible scope, then autonomously benchmark, upgrade, retire, and install user-selected skills through isolated blind evaluations and a resumable local dashboard. |
| [`take-over-pr`](.agents/skills/take-over-pr/SKILL.md) | Make a pull request's branch the working checkout so its work continues in this session. |
| [`tests-doctor`](.agents/skills/tests-doctor/SKILL.md) | Audit and correct a test suite for consistency, redundancy, naming, runtime, coverage by test, and determinism, preferring fewer higher-quality tests. |

### Model-Invoked

An agent reaches for these on its own whenever the work calls for them.

| Skill | What it does |
|---|---|
| [`acceptance-gate`](.agents/skills/acceptance-gate/SKILL.md) | Judge an issue, a finding, a proposal, or a diff against the product's state, a change's stated intent, and the repository's quality rubric through a read-only subagent that answers one question with a specific verdict. |
| [`banned-terminology`](.agents/skills/banned-terminology/SKILL.md) | Owns the banned-terms list in resources/banned_words.json and enforces it. |
| [`code-review`](.agents/skills/code-review/SKILL.md) | Code review a pull request or the current working changes with independent reviewer lenses, validated findings, and severity-rated results. |
| [`code-simplify`](.agents/skills/code-simplify/SKILL.md) | Strictly review the branch's changes for reuse, simplification, abstraction quality, and maintainability, then fix the issues. |
| [`coordinate-repositories`](.agents/skills/coordinate-repositories/SKILL.md) | Coordinate one authorized task across a bounded collection of local repositories and caller-selected existing user-level installations while preserving unrelated work. |
| [`cr`](.agents/skills/cr/SKILL.md) | Triage and resolve the pull request's open review threads, run multi-subagent code-simplify across the complete pull request and related code, then run the high-effort fix review, repair failed checks, squash-merge, verify, and finalize the pull request. |
| [`current-changes`](.agents/skills/current-changes/SKILL.md) | Summarize what the current branch changes against the default branch as one paragraph and one sentence per material change, each linked to the code that makes it, with test changes folded into a single line. |
| [`defer-scope`](.agents/skills/defer-scope/SKILL.md) | Record deferred repository work in Linear, with the repository ledger and focused record pull request as an availability fallback; with no scope, read active Linear and legacy repository records. |
| [`doctor-protocol`](.agents/skills/doctor-protocol/SKILL.md) | The audit-and-fix protocol every doctor skill runs on — scope resolution, read-only reviewer fan-out, a parent-owned ledger, an acceptance-gated remediation plan, sole-editor implementation, final review, deferral of leftovers, and the report skeleton. |
| [`edit-skill`](.agents/skills/edit-skill/SKILL.md) | Add or edit a skill, rule, or agent file under `.agents`, implement the concrete issue that prompted it, and deliver it through simplification, the acceptance gate, the smoke test, and the user's approval of an example response before the pull request merges. |
| [`execute-task`](.agents/skills/execute-task/SKILL.md) | Always run this. Invoke once, before the first edit, at the start of every task that changes files — including one that only begins changing files because work turned up a defect — and keep it active until the task's report: it shapes every response, applies the repository's product constraints, fixes the bugs the work encounters rather than reporting them, simplifies as the change grows, gates the branch before it is pushed, and delivers each repository independently. |
| [`generic-push`](.agents/skills/generic-push/SKILL.md) | Keep repository publishing metadata generic and isolated. |
| [`get-doctors`](.agents/skills/get-doctors/SKILL.md) | List every doctor skill the skill listing declares with a one-line summary of what it audits. |
| [`linear`](.agents/skills/linear/SKILL.md) | Create, find, and update Linear issues through the available Linear integration with dynamic team, workflow, project, and label discovery. |
| [`list-prs`](.agents/skills/list-prs/SKILL.md) | List the pull request URLs for every currently open pull request changed during the entire current session, including drafts. |
| [`list-repos`](.agents/skills/list-repos/SKILL.md) | List the repository web URLs for every repository changed during the entire current session. |
| [`list-rules`](.agents/skills/list-rules/SKILL.md) | List and reconcile canonical rules across a bounded collection of local repositories. |
| [`merge-conflict`](.agents/skills/merge-conflict/SKILL.md) | Incorporate the base branch into a branch — a merge, a rebase, a pull, a branch update, or a conflict Git or the hosting service reports — by comparing what each side did and keeping the better answer, with the resolved result gated before it is pushed. |
| [`plan-change`](.agents/skills/plan-change/SKILL.md) | Present plans for explicit approval and carry approved plans to their last step. |
| [`pre-production`](.agents/skills/pre-production/SKILL.md) | Apply a pre-release repository's product constraints when planning, implementing, simplifying, or reviewing contracts, schemas, migrations, and stored data. |
| [`rebuild-git-history`](.agents/skills/rebuild-git-history/SKILL.md) | Rewrite a branch you own into one commit per material change, or drop one change from it, without losing content: the old head stays under a backup ref, the result is proven against it before anything moves, and the push is leased. |
| [`security-audit`](.agents/skills/security-audit/SKILL.md) | Security audit of a codebase — web apps, APIs, services, CLI tools, libraries, daemons, and more. |
| [`smoke-test`](.agents/skills/smoke-test/SKILL.md) | Prove a skill edit changes what a reader does: rebuild the miss that prompted it, run reviewers on the edited and the original text, and score both against stated criteria before the pull request merges. |
| [`test-fixture`](.agents/skills/test-fixture/SKILL.md) | Organize, add, or change pytest tests using canonical fixtures, factories, shared test utilities, concise cases, parametrization, honest doubles, and regression-proof validation. |

<!-- skills:end -->

## Repository-Provided Skills

A shared skill that needs something only one repository can supply names the role and finds the
skill through the skill listing; the repository's `project.md` says which local skill fills it.

| Role | What the repository provides |
|---|---|
| product constraints | `pre-production` is shared, so a repository supplies only the answers it leaves open: its product state, and what a requiredness change owes the rows already stored. |
| `run-tests` | Its test runner and browser walkthrough, under that exact name. |
| migrations | The skill that authors and validates its schema migrations. |
| finalization | The skill that runs before and after a merge: migration preflight, rollout. |
| deployment | The skill that operates its hosting provider. |
| deferral label | The issue-tracker label `defer-scope` records deferrals under. |

## Editing

Invoke `edit-skill`. It resolves whether the target is shared or repository-owned, edits the shared
one here on its own branch and pull request, and runs the source check, the simplification pass,
the acceptance gate, and the smoke test before the pull request merges.

## Local Development

```bash
bootstrap/install.sh                                            # link into this machine's roots
python3.12 .agents/skills/edit-skill/scripts/validate_sources.py # mirror with the pinned sync tool
```
