# Skills

Shared agent skills, agents, and reusable rules for every repository, in one place.

One canonical copy of each skill lives under `.agents/skills/`. [Agent
Sync](https://github.com/julien777z/agent-sync-action) mirrors them to Claude, Cursor and Codex,
vendors the third-party skills and reference collections registered under `.agents/`, and
`bootstrap/install.sh` links the result into user-level agent roots.

## Quick Start

For a local installation, run `bash bootstrap/install.sh` from the main checkout. User-level
links point directly into that checkout; pull `main` there after a merge to update installed
guidance. Edit skills on a separate branch or worktree. For Claude cloud, put
this at the start of the environment setup script, before project-specific setup commands:

```bash
set -e
install -d -o claude -g claude /home/claude/.local/share
if [ ! -d /home/claude/.local/share/agent-skills/.git ]; then
  runuser -u claude -- git clone https://github.com/julien777z/skills.git /home/claude/.local/share/agent-skills
fi
bash /home/claude/.local/share/agent-skills/bootstrap/install.sh
```

For Codex cloud, create an environment for the repository with this setup script:

```bash
set -e
mkdir -p "$HOME/.codex" "$HOME/.local/share"
if [ ! -d "$HOME/.local/share/agent-skills/.git" ]; then
  git clone https://github.com/julien777z/skills.git "$HOME/.local/share/agent-skills"
fi
bash "$HOME/.local/share/agent-skills/bootstrap/install.sh"
```

Use `bash "$HOME/.local/share/agent-skills/bootstrap/install.sh"` as the Codex cloud maintenance
script so a resumed container refreshes the installation. Each installer invocation fetches the
cloud setup clone's current branch once and fast-forwards it. It then selects a single attached
Skills checkout when one is available and links the result into existing agent roots. In Claude
cloud it also searches Claude's session checkout and links the root home used by the runtime. The
installer exits on update, conflict, or installation failure.

The local installer links skills, reference collections, reusable rules, and applicable agent definitions into existing
Claude, Codex, and Cursor user roots. Codex's global `AGENTS.md` links to the same canonical
`global.md` rule used by the other harnesses. Repository-specific rules stay in each repository's
`project.md`. Re-running refreshes owned links and prunes obsolete ones; real content or foreign
links at an installed path are reported before any links change.

## Layout

| Path | Purpose |
|---|---|
| `.agents/skills/<category>/<name>/` | One skill: `SKILL.md`, with `references/`, `scripts/`, `assets/`, or `resources/` beside it. The categories sort the skills and reach no provider — each one still installs as `<name>`, so a name is unique across the whole tree. |
| `.agents/agents/` | Subagent definitions; the tier each runs on is stated by the skill that launches it. |
| `.agents/rules/` | Reconciled reusable rules; technology-specific rules retain their file scopes. |
| `.agents/external_resources.json` | Third-party skills and reference directories vendored by the workflow. |
| `.agents/resources/<name>/` | Vendored reference files, linked into each supported user-level root under `resources/<name>/`. |
| `.agents/.auto_generated/` | Provider mirrors the workflow generates on `main`; never edited by hand. |
| `AGENTS.md` | Repository instructions the workflow generates at the root; never edited by hand. |
| `bootstrap/install.sh` | Refreshes a cloud setup clone when used there, then links skills, resources, agents, and rules into user-level roots. |

## Skills

The two groups differ in who starts a skill: a user-invoked one carries
`disable-model-invocation: true` in its front matter and stays off the agent's tool surface until you
name it. Generated from each skill's front matter — edit the skill, not the table.

<!-- skills:start -->

### User-Invoked

These run only when you ask for them by name, such as `/refactor`.

- [`assume-library-update`](.agents/skills/execution/assume-library-update/SKILL.md) — Write consuming code for a change in one of your libraries before the library update is available.
- [`ci-watch`](.agents/skills/git/ci-watch/SKILL.md) — Watch a pull request, resolve review findings, and check that CI passes.
- [`code-review`](.agents/skills/review/code-review/SKILL.md) — Code review a pull request or the current working changes with independent reviewer lenses, validated findings, and severity-rated results.
- [`code-slop-doctor`](.agents/skills/doctors/code-slop-doctor/SKILL.md) — Remove unneeded layers, abstractions, duplicates, divergent structure and legacy paths across a repository.
- [`config-doctor`](.agents/skills/doctors/config-doctor/SKILL.md) — Find configuration names that disagree across code and deployments, or are no longer used.
- [`continue-handoff`](.agents/skills/workspace/continue-handoff/SKILL.md) — Pick up work another session handed off.
- [`defer-execution`](.agents/skills/deferrals/defer-execution/SKILL.md) — Schedule separate work on its own branch, either now or after the current pull request merges.
- [`dependency-doctor`](.agents/skills/doctors/dependency-doctor/SKILL.md) — Reconcile declared dependencies with what the code imports and the checks invoke, for every language the repository builds.
- [`docs-doctor`](.agents/skills/doctors/docs-doctor/SKILL.md) — Find and fix documentation that no longer matches the code.
- [`execute-defer-scope`](.agents/skills/deferrals/execute-defer-scope/SKILL.md) — Review and resolve recorded deferred work for a chosen issue, path, or pull request.
- [`grade-plans`](.agents/skills/execution/grade-plans/SKILL.md) — Compare, grade, rate, rank, or choose between two implementation plans written for the same goal or original agent prompt.
- [`guidance-doctor`](.agents/skills/doctors/guidance-doctor/SKILL.md) — Review agent guidance for instructions to cut, clarify, or add.
- [`handoff`](.agents/skills/workspace/handoff/SKILL.md) — Move the current session's work to another session with nothing lost and nothing left for the user to do.
- [`incident`](.agents/skills/execution/incident/SKILL.md) — Restore a broken deployed service, test the fix, and merge the scoped repair.
- [`manage-mcps`](.agents/skills/workspace/manage-mcps/SKILL.md) — Audit and repair managed MCP connectors across Claude Desktop and Codex.
- [`merge-pr`](.agents/skills/git/merge-pr/SKILL.md) — Merge finished pull requests after acceptance and CI, then CR what merged.
- [`new-doctor`](.agents/skills/doctors/new-doctor/SKILL.md) — Create a doctor skill on the shared doctor-protocol for one class of repository hygiene.
- [`placeholder-data`](.agents/skills/workspace/placeholder-data/SKILL.md) — Turn a pasted API payload into the same shape with obviously fake values.
- [`refactor`](.agents/skills/execution/refactor/SKILL.md) — Plan and carry out a repository refactor with independent structural review.
- [`schema-doctor`](.agents/skills/doctors/schema-doctor/SKILL.md) — Check models and schemas for unnecessary nulls, complexity, keys, and indexes.
- [`security-doctor`](.agents/skills/doctors/security-doctor/SKILL.md) — Find and fix the exploitable vulnerabilities in a codebase, each proven by a concrete attack.
- [`skill-gauntlet`](.agents/skills/authoring/skill-gauntlet/SKILL.md) — Audit installed agent skills and test which ones to improve, retire, or install.
- [`study-games`](.agents/skills/roblox/study-games/SKILL.md) — Explicit user-invoked research of Roblox charts for the requested audience and region.
- [`tests-doctor`](.agents/skills/doctors/tests-doctor/SKILL.md) — Audit tests for contract value, redundant proof, weak assertions, runtime, provider rate limits, and determinism.

### Model-Invoked

An agent reaches for these on its own whenever the work calls for them.

- [`acceptance-gate`](.agents/skills/review/acceptance-gate/SKILL.md) — Have an independent reviewer decide whether a proposed change fits the task and the repository.
- [`agent-browser`](.agents/skills/workspace/agent-browser/SKILL.md) — Browser automation CLI for AI agents.
- [`agent-lock`](.agents/skills/workspace/agent-lock/SKILL.md) — Coordinate exclusive use of a shared resource between agents using an exact string key.
- [`async-python-patterns`](.agents/skills/python/async-python-patterns/SKILL.md) — Master Python asyncio, concurrent programming, and async/await patterns for high-performance applications.
- [`banned-terminology`](.agents/skills/review/banned-terminology/SKILL.md) — Owns the banned-terms list in resources/banned_words.json and enforces it.
- [`build-types`](.agents/skills/web/build-types/SKILL.md) — Regenerate generated API types from an OpenAPI document, using a local API checkout when it is present and the deployed API otherwise.
- [`clerk-nextjs-patterns`](.agents/skills/web/clerk-nextjs-patterns/SKILL.md) — Advanced Next.js patterns - middleware, Server Actions, caching with Clerk.
- [`code-simplify`](.agents/skills/review/code-simplify/SKILL.md) — Strictly review the branch's changes for reuse, simplification, abstraction quality, and maintainability, then fix the issues.
- [`coordinate-repositories`](.agents/skills/workspace/coordinate-repositories/SKILL.md) — Carry one task across selected repositories and user-level installations.
- [`cr`](.agents/skills/git/cr/SKILL.md) — Run the full review-and-fix workflow for a pull request when a user enters `/cr`, asks to run CR, or says "CR".
- [`current-changes`](.agents/skills/git/current-changes/SKILL.md) — Summarize the branch's changes against the default branch with links to the code.
- [`database-migrations`](.agents/skills/python/database-migrations/SKILL.md) — Guide for authoring, rebasing, and troubleshooting Alembic database migrations, including how to avoid and fix branched migration graphs.
- [`defer-scope`](.agents/skills/deferrals/defer-scope/SKILL.md) — Record unfinished work in the repository it affects, or read its active records.
- [`design-taste-frontend`](.agents/skills/web/design-taste-frontend/SKILL.md) — Anti-slop frontend skill for landing pages, portfolios, and redesigns.
- [`doctor-protocol`](.agents/skills/doctors/doctor-protocol/SKILL.md) — Set the audit, fix, review, and reporting process used by every doctor skill.
- [`edit-skill`](.agents/skills/authoring/edit-skill/SKILL.md) — Edit a skill, rule, or agent file and fix the guidance gap that prompted the change.
- [`execute-task`](.agents/skills/execution/execute-task/SKILL.md) — Plan the change for approval, then apply repository guidance, fix issues found along the way, and deliver a reviewable pull request.
- [`frontend-design`](.agents/skills/web/frontend-design/SKILL.md) — Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one.
- [`generic-push`](.agents/skills/git/generic-push/SKILL.md) — Keep repository publishing metadata generic and isolated.
- [`get-doctors`](.agents/skills/doctors/get-doctors/SKILL.md) — List every doctor skill the skill listing declares with a one-line summary of what it audits.
- [`i-have-adhd`](.agents/skills/execution/i-have-adhd/SKILL.md) — Apply before the first user-facing response without waiting for an invocation, and stay active until the reader explicitly stops it.
- [`image-to-code`](.agents/skills/web/image-to-code/SKILL.md) — Elite website image-to-code skill for Codex.
- [`impeccable`](.agents/skills/web/impeccable/SKILL.md) — Use when the user wants to design, redesign, shape, critique, audit, polish, clarify, distill, harden, optimize, adapt, animate, colorize, extract, or otherwise improve a frontend interface.
- [`land-pr`](.agents/skills/git/land-pr/SKILL.md) — Ready a pull request, gate its exact head, and merge it when authorized.
- [`linear`](.agents/skills/workspace/linear/SKILL.md) — Create, find, and update Linear issues through the available Linear integration with dynamic team, workflow, project, and label discovery.
- [`list-prs`](.agents/skills/workspace/list-prs/SKILL.md) — List the ongoing task’s open PRs.
- [`list-repos`](.agents/skills/workspace/list-repos/SKILL.md) — List the repository web URLs for every repository changed during the entire current session.
- [`list-rules`](.agents/skills/workspace/list-rules/SKILL.md) — List and reconcile canonical rules across a bounded collection of local repositories.
- [`list-skills`](.agents/skills/workspace/list-skills/SKILL.md) — List and reconcile canonical skills across a bounded collection of local repositories.
- [`luau`](.agents/skills/roblox/luau/SKILL.md) — Apply Roblox Luau conventions when reading or changing game code and tooling.
- [`merge-conflict`](.agents/skills/git/merge-conflict/SKILL.md) — Bring the base branch into a work branch, resolve conflicts, and validate the result.
- [`no-text-ai-slop`](.agents/skills/review/no-text-ai-slop/SKILL.md) — Edit drafts into sharper, more human writing while preserving the writer's personal voice, or detect AI-slop patterns without rewriting.
- [`pre-production`](.agents/skills/execution/pre-production/SKILL.md) — Apply target-contract constraints to implementation and review tasks.
- [`prisma-client-api`](.agents/skills/web/prisma-client-api/SKILL.md) — Prisma Client API reference covering model queries, filters, operators, and client methods.
- [`propagate-skill`](.agents/skills/workspace/propagate-skill/SKILL.md) — Reconcile skills across the user's repository collection.
- [`proton-pass`](.agents/skills/workspace/proton-pass/SKILL.md) — Retrieve credentials from Proton Pass with pass-cli.
- [`python-anti-patterns`](.agents/skills/python/python-anti-patterns/SKILL.md) — Use this skill when reviewing Python code for common anti-patterns to avoid.
- [`python-background-jobs`](.agents/skills/python/python-background-jobs/SKILL.md) — Python background job patterns including task queues, workers, and event-driven architecture.
- [`python-configuration`](.agents/skills/python/python-configuration/SKILL.md) — Python configuration management via environment variables and typed settings.
- [`python-design-patterns`](.agents/skills/python/python-design-patterns/SKILL.md) — Python design patterns including KISS, Separation of Concerns, Single Responsibility, and composition over inheritance.
- [`python-error-handling`](.agents/skills/python/python-error-handling/SKILL.md) — Python error handling patterns including input validation, exception hierarchies, and partial failure handling.
- [`python-performance-optimization`](.agents/skills/python/python-performance-optimization/SKILL.md) — Profile and optimize Python code using cProfile, memory profilers, and performance best practices.
- [`python-project-structure`](.agents/skills/python/python-project-structure/SKILL.md) — Python project organization, module architecture, and public API design.
- [`python-resilience`](.agents/skills/python/python-resilience/SKILL.md) — Python resilience patterns including automatic retries, exponential backoff, timeouts, and fault-tolerant decorators.
- [`python-resource-management`](.agents/skills/python/python-resource-management/SKILL.md) — Python resource management with context managers, cleanup patterns, and streaming.
- [`python-testing-patterns`](.agents/skills/python/python-testing-patterns/SKILL.md) — Implement comprehensive testing strategies with pytest, fixtures, mocking, and test-driven development.
- [`python-type-safety`](.agents/skills/python/python-type-safety/SKILL.md) — Python type safety with type hints, generics, protocols, and strict type checking.
- [`reconcile-skills`](.agents/skills/workspace/reconcile-skills/SKILL.md) — Refresh installed shared skills and rules from their source checkout.
- [`rewrite-git-history`](.agents/skills/git/rewrite-git-history/SKILL.md) — Rework your branch into focused commits while preserving and checking its content.
- [`roblox-building`](.agents/skills/roblox/roblox-building/SKILL.md) — Build and improve Roblox worlds, terrain, structures, props, and assets.
- [`roblox-gameplay`](.agents/skills/roblox/roblox-gameplay/SKILL.md) — Apply every time actively modifying a Roblox game, including mechanics, progression, rewards, controls, presentation, UI, and world content.
- [`roblox-react`](.agents/skills/roblox/roblox-react/SKILL.md) — Design and change React-rendered Roblox interfaces, including HUDs and menus.
- [`roblox-studio`](.agents/skills/roblox/roblox-studio/SKILL.md) — Create, polish, and playtest Roblox games in Studio.
- [`run-site`](.agents/skills/workspace/run-site/SKILL.md) — Start an application stack and perform browser verification where applicable.
- [`security-audit`](.agents/skills/review/security-audit/SKILL.md) — Security guidance for writing code, reviewing a change, and auditing a codebase.
- [`session-ledger`](.agents/skills/workspace/session-ledger/SKILL.md) — Keep verified task artifacts in one private task file.
- [`storyline`](.agents/skills/roblox/storyline/SKILL.md) — Create or improve a coherent game story with playable beats and a satisfying ending.
- [`subagent-selection`](.agents/skills/execution/subagent-selection/SKILL.md) — Select a model tier for live verification chats or subagent delegation.
- [`tailscale-config`](.agents/skills/workspace/tailscale-config/SKILL.md) — Reconcile Tailscale authority and every affected execution consumer.
- [`tailwind-design-system`](.agents/skills/web/tailwind-design-system/SKILL.md) — Build scalable design systems with Tailwind CSS v4, design tokens, component libraries, and responsive patterns.
- [`test-fixture`](.agents/skills/authoring/test-fixture/SKILL.md) — Check test data and fixtures before changing tests or running tests after a fixture change.
- [`test-skill`](.agents/skills/authoring/test-skill/SKILL.md) — Compare edited and original skill guidance against the same scenario.
- [`text-highlight`](.agents/skills/git/text-highlight/SKILL.md) — Show code changes in small diff-shaped excerpts that are easy to locate.
- [`vercel-composition-patterns`](.agents/skills/web/vercel-composition-patterns/SKILL.md) — React composition patterns that scale.
- [`vercel-react-best-practices`](.agents/skills/web/vercel-react-best-practices/SKILL.md) — React and Next.js performance optimization guidelines from Vercel Engineering.
- [`vercel-react-view-transitions`](.agents/skills/web/vercel-react-view-transitions/SKILL.md) — Guide for implementing smooth, native-feeling animations using React's View Transition API (`<ViewTransition>` component, `addTransitionType`, and CSS view transition pseudo-elements).
- [`web-design-guidelines`](.agents/skills/web/web-design-guidelines/SKILL.md) — Review UI code for Web Interface Guidelines compliance.

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
python3.12 .agents/skills/authoring/edit-skill/scripts/validate_sources.py # mirror with the pinned sync tool
```
