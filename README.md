# Skills

I keep the skills and rules I use across projects here. [Agent Sync](https://github.com/julien777z/agent-sync-action)
turns the files in `.agents/` into guidance for Claude, Codex, and Cursor.

## Quick Start

Run `bash bootstrap/install.sh` from your main checkout to link these skills into Claude, Codex,
and Cursor. Pull `main` when you want the latest version. Make edits in a separate branch or
worktree.

For Claude cloud, add this to the start of your environment setup script:

```bash
set -e
install -d -o claude -g claude /home/claude/.local/share
if [ ! -d /home/claude/.local/share/agent-skills/.git ]; then
  runuser -u claude -- git clone https://github.com/julien777z/skills.git /home/claude/.local/share/agent-skills
fi
bash /home/claude/.local/share/agent-skills/bootstrap/cloud-install.sh
```

If the environment already has this checkout attached, the cloud installer uses it. Otherwise,
it uses the clone from setup.

## Layout

| Path | Purpose |
|---|---|
| `.agents/skills/` | Skills, grouped by topic. Each skill has a `SKILL.md`. |
| `.agents/rules/` | Shared rules. Scoped rules declare `paths`; Agent Sync writes each provider's format. |
| `.agents/agents/` | Agent definitions. |
| `.agents/project.md` and `.agents/global.md` | Repository and global instructions. |
| `.agents/external_skills.json` | Third-party skills installed from [skills.sh](https://skills.sh/). |
| `.agents/.auto_generated/` and `AGENTS.md` | Generated after pushes to `main`. Edit `.agents/` instead. |

## Skills

Browse the skills below, or open one for its full instructions. This list comes from the skill files.

<!-- skills:start -->

### User-Invoked

These run only when you ask for them by name, such as `/refactor`.

- [`assume-library-update`](.agents/skills/execution/assume-library-update/SKILL.md) — Write consuming code for a change in one of your libraries before the library update is available.
- [`ci-watch`](.agents/skills/git/ci-watch/SKILL.md) — Watch a pull request, resolve review findings, and check that CI passes.
- [`config-doctor`](.agents/skills/doctors/config-doctor/SKILL.md) — Find configuration names that disagree across code and deployments, or are no longer used.
- [`cr`](.agents/skills/git/cr/SKILL.md) — Resolve a pull request's review threads and checks, then merge and verify it.
- [`defer-execution`](.agents/skills/deferrals/defer-execution/SKILL.md) — Schedule separate work on its own branch, either now or after the current pull request merges.
- [`dependency-doctor`](.agents/skills/doctors/dependency-doctor/SKILL.md) — Reconcile declared dependencies with what the code imports and the checks invoke, for every language the repository builds.
- [`docs-doctor`](.agents/skills/doctors/docs-doctor/SKILL.md) — Find and fix documentation that no longer matches the code.
- [`execute-defer-scope`](.agents/skills/deferrals/execute-defer-scope/SKILL.md) — Review and resolve recorded deferred work for a chosen issue, path, or pull request.
- [`grade-plans`](.agents/skills/execution/grade-plans/SKILL.md) — Compare, grade, rate, rank, or choose between two implementation plans written for the same goal or original agent prompt.
- [`guidance-doctor`](.agents/skills/doctors/guidance-doctor/SKILL.md) — Review agent guidance for instructions to cut, clarify, or add.
- [`hand-off`](.agents/skills/workspace/hand-off/SKILL.md) — Wrap up the current session so its open pull requests can be taken to another session with nothing lost.
- [`incident`](.agents/skills/execution/incident/SKILL.md) — Restore a broken deployed service, test the fix, and merge the scoped repair.
- [`legacy-doctor`](.agents/skills/doctors/legacy-doctor/SKILL.md) — Remove fallbacks, aliases, and duplicate paths left over from an old contract.
- [`manage-mcps`](.agents/skills/workspace/manage-mcps/SKILL.md) — Audit and repair managed MCP connectors across Claude Desktop and Codex.
- [`migrations-doctor`](.agents/skills/doctors/migrations-doctor/SKILL.md) — Audit and correct a repository's database migration chains, revisions, registries, and test scaffolding.
- [`new-doctor`](.agents/skills/doctors/new-doctor/SKILL.md) — Create a doctor skill on the shared doctor-protocol for one class of repository hygiene.
- [`refactor`](.agents/skills/execution/refactor/SKILL.md) — Plan and carry out a repository refactor with independent structural review.
- [`schema-doctor`](.agents/skills/doctors/schema-doctor/SKILL.md) — Check models and schemas for unnecessary nulls, complexity, keys, and indexes.
- [`skill-gauntlet`](.agents/skills/authoring/skill-gauntlet/SKILL.md) — Audit installed agent skills and test which ones to improve, retire, or install.
- [`study-games`](.agents/skills/roblox/study-games/SKILL.md) — Explicit user-invoked research of Roblox charts for the requested audience and region.
- [`take-over-pr`](.agents/skills/git/take-over-pr/SKILL.md) — Make a pull request's branch the working checkout so its work continues in this session.
- [`tests-doctor`](.agents/skills/doctors/tests-doctor/SKILL.md) — Audit and correct existing tests for contract value, redundancy, weak assertions, naming, runtime, coverage by test, and determinism.

### Model-Invoked

An agent reaches for these on its own whenever the work calls for them.

- [`acceptance-gate`](.agents/skills/review/acceptance-gate/SKILL.md) — Have an independent reviewer decide whether a proposed change fits the task and the repository.
- [`agent-browser`](.agents/skills/workspace/agent-browser/SKILL.md) — Browser automation CLI for AI agents.
- [`agent-lock`](.agents/skills/workspace/agent-lock/SKILL.md) — Coordinate exclusive use of a shared resource between agents using an exact string key.
- [`async-python-patterns`](.agents/skills/python/async-python-patterns/SKILL.md) — Master Python asyncio, concurrent programming, and async/await patterns for high-performance applications.
- [`awesome-design`](.agents/skills/web/awesome-design/SKILL.md) — Curated collection of DESIGN.md files from real websites.
- [`banned-terminology`](.agents/skills/review/banned-terminology/SKILL.md) — Owns the banned-terms list in resources/banned_words.json and enforces it.
- [`build-types`](.agents/skills/web/build-types/SKILL.md) — Regenerate generated API types from an OpenAPI document, using a local API checkout when it is present and the deployed API otherwise.
- [`clerk-nextjs-patterns`](.agents/skills/web/clerk-nextjs-patterns/SKILL.md) — Advanced Next.js patterns - middleware, Server Actions, caching with Clerk.
- [`code-review`](.agents/skills/review/code-review/SKILL.md) — Code review a pull request or the current working changes with independent reviewer lenses, validated findings, and severity-rated results.
- [`code-simplify`](.agents/skills/review/code-simplify/SKILL.md) — Strictly review the branch's changes for reuse, simplification, abstraction quality, and maintainability, then fix the issues.
- [`coordinate-repositories`](.agents/skills/workspace/coordinate-repositories/SKILL.md) — Carry one task across selected repositories and user-level installations.
- [`current-changes`](.agents/skills/git/current-changes/SKILL.md) — Summarize the branch's changes against the default branch with links to the code.
- [`database-migrations`](.agents/skills/python/database-migrations/SKILL.md) — Guide for authoring, rebasing, and troubleshooting Alembic database migrations, including how to avoid and fix branched migration graphs.
- [`defer-scope`](.agents/skills/deferrals/defer-scope/SKILL.md) — Record unfinished work in the repository it affects, or read its active records.
- [`design-taste-frontend`](.agents/skills/web/design-taste-frontend/SKILL.md) — Anti-slop frontend skill for landing pages, portfolios, and redesigns.
- [`doctor-protocol`](.agents/skills/doctors/doctor-protocol/SKILL.md) — Set the audit, fix, review, and reporting process used by every doctor skill.
- [`edit-skill`](.agents/skills/authoring/edit-skill/SKILL.md) — Edit a skill, rule, or agent file and fix the guidance gap that prompted the change.
- [`execute-task`](.agents/skills/execution/execute-task/SKILL.md) — Apply repository guidance, fix issues found along the way, validate the diff, and deliver the change.
- [`frontend-design`](.agents/skills/web/frontend-design/SKILL.md) — Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one.
- [`generic-push`](.agents/skills/git/generic-push/SKILL.md) — Keep repository publishing metadata generic and isolated.
- [`get-doctors`](.agents/skills/doctors/get-doctors/SKILL.md) — List every doctor skill the skill listing declares with a one-line summary of what it audits.
- [`i-have-adhd`](.agents/skills/execution/i-have-adhd/SKILL.md) — Make responses easier to scan, with the next action first and tangents removed.
- [`image-to-code`](.agents/skills/web/image-to-code/SKILL.md) — Elite website image-to-code skill for Codex.
- [`linear`](.agents/skills/workspace/linear/SKILL.md) — Create, find, and update Linear issues through the available Linear integration with dynamic team, workflow, project, and label discovery.
- [`list-prs`](.agents/skills/workspace/list-prs/SKILL.md) — List the pull request URLs for every currently open pull request changed during the entire current session, including drafts.
- [`list-repos`](.agents/skills/workspace/list-repos/SKILL.md) — List the repository web URLs for every repository changed during the entire current session.
- [`list-rules`](.agents/skills/workspace/list-rules/SKILL.md) — List and reconcile canonical rules across a bounded collection of local repositories.
- [`list-skills`](.agents/skills/workspace/list-skills/SKILL.md) — List and reconcile canonical skills across a bounded collection of local repositories.
- [`luau`](.agents/skills/roblox/luau/SKILL.md) — Apply Roblox Luau conventions when reading or changing game code and tooling.
- [`merge-conflict`](.agents/skills/git/merge-conflict/SKILL.md) — Bring the base branch into a work branch, resolve conflicts, and validate the result.
- [`merge-pr`](.agents/skills/git/merge-pr/SKILL.md) — Validate and merge an authorized pull request at its reviewed head.
- [`no-text-ai-slop`](.agents/skills/review/no-text-ai-slop/SKILL.md) — Edit drafts into sharper, more human writing while preserving the writer's personal voice, or detect AI-slop patterns without rewriting.
- [`plan-change`](.agents/skills/execution/plan-change/SKILL.md) — Present plans for explicit approval and carry approved plans to their last step.
- [`pre-production`](.agents/skills/execution/pre-production/SKILL.md) — Apply a pre-release repository's product constraints to contracts, schemas, and stored data.
- [`prisma-client-api`](.agents/skills/web/prisma-client-api/SKILL.md) — Prisma Client API reference covering model queries, filters, operators, and client methods.
- [`propagate-skill`](.agents/skills/workspace/propagate-skill/SKILL.md) — Reconcile skills across the user's repository collection.
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
- [`rebuild-git-history`](.agents/skills/git/rebuild-git-history/SKILL.md) — Rework your branch into focused commits while preserving and checking its content.
- [`roblox-building`](.agents/skills/roblox/roblox-building/SKILL.md) — Build and improve Roblox worlds, terrain, structures, props, and assets.
- [`roblox-gameplay`](.agents/skills/roblox/roblox-gameplay/SKILL.md) — Apply every time actively modifying a Roblox game, including mechanics, progression, rewards, controls, presentation, UI, and world content.
- [`roblox-react`](.agents/skills/roblox/roblox-react/SKILL.md) — Design and change React-rendered Roblox interfaces, including HUDs and menus.
- [`roblox-studio`](.agents/skills/roblox/roblox-studio/SKILL.md) — Create, polish, and playtest Roblox games in Studio.
- [`run-site`](.agents/skills/workspace/run-site/SKILL.md) — Start a local app, repair startup failures, and test its core flow in a browser.
- [`security-audit`](.agents/skills/review/security-audit/SKILL.md) — Security audit of a codebase — web apps, APIs, services, CLI tools, libraries, daemons, and more.
- [`storyline`](.agents/skills/roblox/storyline/SKILL.md) — Create or improve a coherent game story with playable beats and a satisfying ending.
- [`subagent-selection`](.agents/skills/execution/subagent-selection/SKILL.md) — Apply whenever selecting or launching sub-agents, whether directly for a task or through another skill.
- [`tailwind-design-system`](.agents/skills/web/tailwind-design-system/SKILL.md) — Build scalable design systems with Tailwind CSS v4, design tokens, component libraries, and responsive patterns.
- [`test-fixture`](.agents/skills/authoring/test-fixture/SKILL.md) — Check test data and fixtures before changing tests or running tests after a fixture change.
- [`test-skill`](.agents/skills/authoring/test-skill/SKILL.md) — Compare edited and original skill guidance against the same scenario.
- [`text-highlight`](.agents/skills/git/text-highlight/SKILL.md) — Show code changes in small diff-shaped excerpts that are easy to locate.
- [`vercel-composition-patterns`](.agents/skills/web/vercel-composition-patterns/SKILL.md) — React composition patterns that scale.
- [`vercel-react-best-practices`](.agents/skills/web/vercel-react-best-practices/SKILL.md) — React and Next.js performance optimization guidelines from Vercel Engineering.
- [`vercel-react-view-transitions`](.agents/skills/web/vercel-react-view-transitions/SKILL.md) — Build smooth React animations with the View Transition API.
- [`web-design-guidelines`](.agents/skills/web/web-design-guidelines/SKILL.md) — Review UI code for Web Interface Guidelines compliance.

<!-- skills:end -->

## Repository Skills

Shared skills can call repository-specific skills for tests, migrations, deployment, and other
local work. Each repository lists those roles in its `.agents/project.md`.

## Editing

Use [`edit-skill`](.agents/skills/authoring/edit-skill/SKILL.md) to change canonical guidance.
Agent Sync updates provider files after changes reach `main`.

## Local Development

```bash
bootstrap/install.sh
python3.12 .agents/skills/authoring/edit-skill/scripts/validate_sources.py
```
