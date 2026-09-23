# Skills

Shared agent skills for every repository, in one place.

One canonical copy of each skill lives under `.agents/skills/`. [Agent
Sync](https://github.com/julien777z/agent-sync-action) mirrors them to Claude, Cursor and Codex,
vendors the third-party skills registered in `.agents/external_skills.json`, and `bootstrap/install.sh`
links the result into this machine's user-level roots — so every repository's session sees the same
skills.

## Quick Start

For a local checkout, run `bash bootstrap/install.sh` from that checkout. For Claude cloud, put
this at the start of the environment setup script, before project-specific setup commands:

```bash
set -e
install -d -o claude -g claude /home/claude/.local/share
if [ ! -d /home/claude/.local/share/agent-skills/.git ]; then
  runuser -u claude -- git clone https://github.com/julien777z/skills.git /home/claude/.local/share/agent-skills
fi
bash /home/claude/.local/share/agent-skills/bootstrap/cloud-install.sh
```

The cloud installer uses an attached skills checkout when one is present and the setup clone
otherwise. It links skills for `/home/claude` and the root home used by the current cloud runtime,
and exits on clone,
update, or installation failure. Cloud environment image caching can skip setup on later sessions;
the previously installed skills remain available then.

The local installer links each skill into `~/.claude/skills`, `~/.codex/skills`, and
`~/.cursor/skills` for whichever of those
roots already exist, and each agent definition into `~/.claude/agents` and `~/.cursor/agents`.
Re-running refreshes owned links and prunes the ones a removed skill left behind. A real directory
or foreign link at a skill name is reported before any links change so its contents can be
reconciled safely.

## Layout

| Path | Purpose |
|---|---|
| `.agents/skills/<folder>/<name>/` | One skill: `SKILL.md`, with `references/`, `scripts/`, `assets/`, or `resources/` beside it. The folders sort the skills and reach no provider — each one still installs as `<name>`, so a name is unique across the whole tree. |
| `.agents/agents/` | Subagent definitions; the tier each runs on is stated by the skill that launches it. |
| `.agents/external_skills.json` | Third-party skills the workflow installs from [skills.sh](https://skills.sh/). |
| `.agents/.auto_generated/` | Provider mirrors the workflow generates on `main`; never edited by hand. |
| `AGENTS.md` | Repository instructions the workflow generates at the root; never edited by hand. |
| `bootstrap/install.sh` | Links the skills and agents into the user-level roots. |
| `bootstrap/cloud-install.sh` | Selects the attached or cached checkout and installs it for Claude cloud's user. |

## Skills

The two groups differ in who starts a skill: a user-invoked one carries
`disable-model-invocation: true` in its front matter and stays off the agent's tool surface until you
name it. Generated from each skill's front matter — edit the skill, not the table.

<!-- skills:start -->

### User-Invoked

These run only when you ask for them by name, such as `/refactor`.

| Skill | What it does |
|---|---|
| [`assume-library-update`](.agents/skills/execution/assume-library-update/SKILL.md) | Write consuming code against a library change that is authored but not yet reachable, when the library is the user's own and this session cannot push to it. |
| [`ci-watch`](.agents/skills/git/ci-watch/SKILL.md) | Find and watch a GitHub pull request for review findings, investigate each finding, fix and push legitimate issues, and stop once checks are green and review threads are resolved. |
| [`config-doctor`](.agents/skills/doctors/config-doctor/SKILL.md) | Reconcile configuration names across every place they are declared, each deployment's own environment included, and remove settings nothing reads or nothing deployed sets. |
| [`cr`](.agents/skills/git/cr/SKILL.md) | Triage and resolve the pull request's open review threads, run multi-subagent code-simplify across the complete pull request and related code, then run the high-effort fix review, repair failed checks, squash-merge, verify, and finalize the pull request. |
| [`defer-execution`](.agents/skills/deferrals/defer-execution/SKILL.md) | Schedule an unrecorded scope of work on its own branch off the default branch rather than folding it into the change in flight, either after the originating pull request merges or immediately in a worktree. |
| [`dependency-doctor`](.agents/skills/doctors/dependency-doctor/SKILL.md) | Reconcile declared dependencies with what the code imports and the checks invoke, for every language the repository builds. |
| [`docs-doctor`](.agents/skills/doctors/docs-doctor/SKILL.md) | Find and fix documentation that no longer matches the code. |
| [`execute-defer-scope`](.agents/skills/deferrals/execute-defer-scope/SKILL.md) | Evaluate and resolve recorded deferrals from Linear and the legacy repository ledger, using the current session or an explicit issue, key, path, pull request, or aggregate scope. |
| [`grade-plans`](.agents/skills/execution/grade-plans/SKILL.md) | Compare, grade, rate, rank, or choose between two implementation plans written for the same goal or original agent prompt. |
| [`guidance-doctor`](.agents/skills/doctors/guidance-doctor/SKILL.md) | Audit the repository's agent guidance for what to cut, tighten, or add, against what a current model does unprompted and what the vendors' current authoring guidance says. |
| [`hand-off`](.agents/skills/workspace/hand-off/SKILL.md) | Wrap up the current session so its open pull requests can be taken to another session with nothing lost. |
| [`incident`](.agents/skills/execution/incident/SKILL.md) | Restore a broken deployed service using a browser and the repository's deployment skill as needed, deploy and test a fix branch, and merge scoped fix pull requests after one Bugs and Simplification review round. |
| [`legacy-doctor`](.agents/skills/doctors/legacy-doctor/SKILL.md) | Find and remove code that tolerates a past the repository no longer has: fallbacks, compatibility branches, kept aliases, silent tolerance, and second implementations of one thing. |
| [`legal-review`](.agents/skills/review/legal-review/SKILL.md) | Review the Terms of Service and Privacy Policy against the law that applies to the company today and against what the site actually does: six parallel legal lenses, a code-versus-document check, an adversarial pass that tries to refute every finding, ranked findings with suggested language, a recommendation for every open question, and only the strictly necessary fixes gated through acceptance-gate and proposed through plan-change. |
| [`manage-mcps`](.agents/skills/workspace/manage-mcps/SKILL.md) | Audit, restore, reauthenticate, and align managed remote MCP connectors across Claude Desktop and Codex, preserving unknown connectors and permission overrides. |
| [`migrations-doctor`](.agents/skills/doctors/migrations-doctor/SKILL.md) | Audit and correct a repository's database migration chains, revisions, registries, and test scaffolding. |
| [`new-doctor`](.agents/skills/doctors/new-doctor/SKILL.md) | Create a doctor skill on the shared doctor-protocol for one class of repository hygiene. |
| [`refactor`](.agents/skills/execution/refactor/SKILL.md) | Resolve and confirm a repository refactor scope, use multiple independent reviewers to plan structural improvements, then implement an approved plan. |
| [`schema-doctor`](.agents/skills/doctors/schema-doctor/SKILL.md) | Audit and correct unjustified nullability, model complexity, primary-key design, and index design across repository API contracts, serialized schemas, persisted schemas, and the field flows connecting them. |
| [`skill-gauntlet`](.agents/skills/authoring/skill-gauntlet/SKILL.md) | Audit installed agent skills across every visible scope, then autonomously benchmark, upgrade, retire, and install user-selected skills through isolated blind evaluations and a resumable local dashboard. |
| [`take-over-pr`](.agents/skills/git/take-over-pr/SKILL.md) | Make a pull request's branch the working checkout so its work continues in this session. |
| [`tests-doctor`](.agents/skills/doctors/tests-doctor/SKILL.md) | Audit and correct a test suite for consistency, redundancy, naming, runtime, coverage by test, and determinism, preferring fewer higher-quality tests. |

### Model-Invoked

An agent reaches for these on its own whenever the work calls for them.

| Skill | What it does |
|---|---|
| [`acceptance-gate`](.agents/skills/review/acceptance-gate/SKILL.md) | Judge an issue, a finding, a proposal, or a diff against the product's state, a change's stated intent, and the repository's quality rubric through a read-only subagent that answers one question with a specific verdict. |
| [`agent-browser`](.agents/skills/workspace/agent-browser/SKILL.md) | Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. |
| [`agent-lock`](.agents/skills/workspace/agent-lock/SKILL.md) | Coordinate exclusive use of a shared resource between agents using an exact string key. |
| [`async-python-patterns`](.agents/skills/python/async-python-patterns/SKILL.md) | Master Python asyncio, concurrent programming, and async/await patterns for high-performance applications. |
| [`banned-terminology`](.agents/skills/review/banned-terminology/SKILL.md) | Owns the banned-terms list in resources/banned_words.json and enforces it. |
| [`build-types`](.agents/skills/web/build-types/SKILL.md) | Regenerate generated API types from an OpenAPI document, using a local API checkout when it is present and the deployed API otherwise. |
| [`clerk-nextjs-patterns`](.agents/skills/web/clerk-nextjs-patterns/SKILL.md) | Advanced Next.js patterns - middleware, Server Actions, caching with Clerk. |
| [`code-review`](.agents/skills/review/code-review/SKILL.md) | Code review a pull request or the current working changes with independent reviewer lenses, validated findings, and severity-rated results. |
| [`code-simplify`](.agents/skills/review/code-simplify/SKILL.md) | Strictly review the branch's changes for reuse, simplification, abstraction quality, and maintainability, then fix the issues. |
| [`coordinate-repositories`](.agents/skills/workspace/coordinate-repositories/SKILL.md) | Coordinate one authorized task across a bounded collection of local repositories and caller-selected existing user-level installations while preserving unrelated work. |
| [`current-changes`](.agents/skills/git/current-changes/SKILL.md) | Summarize what the current branch changes against the default branch as one paragraph and one sentence per material change, each linked to the code that makes it, with test changes folded into a single line. |
| [`database-migrations`](.agents/skills/python/database-migrations/SKILL.md) | Guide for authoring, rebasing, and troubleshooting Alembic database migrations, including how to avoid and fix branched migration graphs. |
| [`defer-scope`](.agents/skills/deferrals/defer-scope/SKILL.md) | Record deferred repository work in Linear, with the repository ledger and focused record pull request as an availability fallback; with no scope, read active Linear and legacy repository records. |
| [`design-taste-frontend`](.agents/skills/web/design-taste-frontend/SKILL.md) | Anti-slop frontend skill for landing pages, portfolios, and redesigns. |
| [`doctor-protocol`](.agents/skills/doctors/doctor-protocol/SKILL.md) | The audit-and-fix protocol every doctor skill runs on — scope resolution, read-only reviewer fan-out, a parent-owned ledger, an acceptance-gated remediation plan, sole-editor implementation, final review, deferral of leftovers, and the report skeleton. |
| [`edit-skill`](.agents/skills/authoring/edit-skill/SKILL.md) | Add or edit a skill, rule, or agent file under `.agents`, implement the concrete issue that prompted it, and deliver it through simplification, the acceptance gate, the smoke test, and the user's approval of an example response before the pull request merges. |
| [`execute-task`](.agents/skills/execution/execute-task/SKILL.md) | Always run this. Invoke once, before the first edit, at the start of every task that changes files — including one that only begins changing files because work turned up a defect — and keep it active until the task's report: it shapes every response, applies the repository's product constraints, fixes the bugs the work encounters rather than reporting them, simplifies as the change grows, gates the branch before it is pushed, and delivers each repository independently. |
| [`frontend-design`](.agents/skills/web/frontend-design/SKILL.md) | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. |
| [`generic-push`](.agents/skills/git/generic-push/SKILL.md) | Keep repository publishing metadata generic and isolated. |
| [`get-doctors`](.agents/skills/doctors/get-doctors/SKILL.md) | List every doctor skill the skill listing declares with a one-line summary of what it audits. |
| [`i-have-adhd`](.agents/skills/execution/i-have-adhd/SKILL.md) | Shape output for a reader with ADHD: lead with the next action, number multi-step work, restate state across turns, suppress tangents, give specific time estimates, make wins visible. |
| [`linear`](.agents/skills/workspace/linear/SKILL.md) | Create, find, and update Linear issues through the available Linear integration with dynamic team, workflow, project, and label discovery. |
| [`list-prs`](.agents/skills/workspace/list-prs/SKILL.md) | List the pull request URLs for every currently open pull request changed during the entire current session, including drafts. |
| [`list-repos`](.agents/skills/workspace/list-repos/SKILL.md) | List the repository web URLs for every repository changed during the entire current session. |
| [`list-rules`](.agents/skills/workspace/list-rules/SKILL.md) | List and reconcile canonical rules across a bounded collection of local repositories. |
| [`list-skills`](.agents/skills/workspace/list-skills/SKILL.md) | List and reconcile canonical skills across a bounded collection of local repositories. |
| [`luau`](.agents/skills/roblox/luau/SKILL.md) | Apply whenever Roblox Luau source is opened, read, reviewed, created, or modified, including scripts, modules, builders, tests, network contracts, and tooling configuration. |
| [`merge-conflict`](.agents/skills/git/merge-conflict/SKILL.md) | Incorporate the base branch into a branch — a merge, a rebase, a pull, a branch update, or a conflict Git or the hosting service reports — by comparing what each side did and keeping the better answer, with the resolved result gated before it is pushed. |
| [`no-ai-slop`](.agents/skills/review/no-ai-slop/SKILL.md) | Edit drafts into sharper, more human writing while preserving the writer's personal voice, or detect AI-slop patterns without rewriting. |
| [`plan-change`](.agents/skills/execution/plan-change/SKILL.md) | Present plans for explicit approval and carry approved plans to their last step. |
| [`pre-production`](.agents/skills/execution/pre-production/SKILL.md) | Apply a pre-release repository's product constraints when planning, implementing, simplifying, or reviewing contracts, schemas, migrations, and stored data. |
| [`prisma-client-api`](.agents/skills/web/prisma-client-api/SKILL.md) | Prisma Client API reference covering model queries, filters, operators, and client methods. |
| [`propagate-skill`](.agents/skills/workspace/propagate-skill/SKILL.md) | Reconcile skills across the user's repository collection. |
| [`python-anti-patterns`](.agents/skills/python/python-anti-patterns/SKILL.md) | Use this skill when reviewing Python code for common anti-patterns to avoid. |
| [`python-background-jobs`](.agents/skills/python/python-background-jobs/SKILL.md) | Python background job patterns including task queues, workers, and event-driven architecture. |
| [`python-configuration`](.agents/skills/python/python-configuration/SKILL.md) | Python configuration management via environment variables and typed settings. |
| [`python-design-patterns`](.agents/skills/python/python-design-patterns/SKILL.md) | Python design patterns including KISS, Separation of Concerns, Single Responsibility, and composition over inheritance. |
| [`python-error-handling`](.agents/skills/python/python-error-handling/SKILL.md) | Python error handling patterns including input validation, exception hierarchies, and partial failure handling. |
| [`python-performance-optimization`](.agents/skills/python/python-performance-optimization/SKILL.md) | Profile and optimize Python code using cProfile, memory profilers, and performance best practices. |
| [`python-project-structure`](.agents/skills/python/python-project-structure/SKILL.md) | Python project organization, module architecture, and public API design. |
| [`python-resilience`](.agents/skills/python/python-resilience/SKILL.md) | Python resilience patterns including automatic retries, exponential backoff, timeouts, and fault-tolerant decorators. |
| [`python-resource-management`](.agents/skills/python/python-resource-management/SKILL.md) | Python resource management with context managers, cleanup patterns, and streaming. |
| [`python-testing-patterns`](.agents/skills/python/python-testing-patterns/SKILL.md) | Implement comprehensive testing strategies with pytest, fixtures, mocking, and test-driven development. |
| [`python-type-safety`](.agents/skills/python/python-type-safety/SKILL.md) | Python type safety with type hints, generics, protocols, and strict type checking. |
| [`rebuild-git-history`](.agents/skills/git/rebuild-git-history/SKILL.md) | Rewrite a branch you own into one commit per material change, or drop one change from it, without losing content: the old head stays under a backup ref, the result is proven against it before anything moves, and the push is leased. |
| [`roblox-building`](.agents/skills/roblox/roblox-building/SKILL.md) | Apply when planning, inspecting, creating, modifying, importing, optimizing, or playtesting Roblox maps, worlds, terrain, buildings, props, environmental meshes, or Blender assets. |
| [`roblox-gameplay`](.agents/skills/roblox/roblox-gameplay/SKILL.md) | Apply every time actively modifying a Roblox game, including mechanics, progression, rewards, controls, presentation, UI, and world content. |
| [`roblox-react`](.agents/skills/roblox/roblox-react/SKILL.md) | Apply whenever Roblox UI is opened, inspected, designed, created, modified, or playtested, especially React Luau components, hooks, HUDs, menus, modals, tutorials, cards, and viewport previews. |
| [`roblox-studio`](.agents/skills/roblox/roblox-studio/SKILL.md) | Create, update, polish, and playtest Roblox games in Roblox Studio, including detailed maps, character presentation, Blender assets, background MCP playtests, and verified place delivery. |
| [`run-site`](.agents/skills/workspace/run-site/SKILL.md) | Bring a local application stack up, repair startup blockers, and prove the running site works by driving a real browser through sign-in and core functionality with screenshots. |
| [`security-audit`](.agents/skills/review/security-audit/SKILL.md) | Security audit of a codebase — web apps, APIs, services, CLI tools, libraries, daemons, and more. |
| [`smoke-test`](.agents/skills/authoring/smoke-test/SKILL.md) | Prove a skill edit changes what a reader does: rebuild the miss that prompted it, run reviewers on the edited and the original text, and score both against stated criteria before the pull request merges. |
| [`storyline`](.agents/skills/roblox/storyline/SKILL.md) | Create, audit, or extend a game's substantial, coherent storyline with independent narrative proposals, motivated characters, playable story beats, a connected story web, and a satisfying ending. |
| [`study-games`](.agents/skills/roblox/study-games/SKILL.md) | Explicit user-invoked research of the current Roblox desktop US charts. |
| [`subagent-selection`](.agents/skills/execution/subagent-selection/SKILL.md) | Apply whenever selecting or launching sub-agents, whether directly for a task or through another skill. |
| [`tailwind-design-system`](.agents/skills/web/tailwind-design-system/SKILL.md) | Build scalable design systems with Tailwind CSS v4, design tokens, component libraries, and responsive patterns. |
| [`test-fixture`](.agents/skills/authoring/test-fixture/SKILL.md) | Must be used before creating, moving, renaming, editing, reviewing, or generating any test, fixture, factory, test data, test support, or test configuration in any language, and before executing tests after such a change. |
| [`text-highlight`](.agents/skills/git/text-highlight/SKILL.md) | Show changes as diff-shaped code blocks a reader can locate at a glance: an edited line marked + in the form it now takes, a line dropped with nothing in its place marked -, a few unchanged lines around each change, and ... |
| [`vercel-composition-patterns`](.agents/skills/web/vercel-composition-patterns/SKILL.md) | React composition patterns that scale. Use when refactoring components with boolean prop proliferation, building flexible component libraries, or designing reusable APIs. |
| [`vercel-react-best-practices`](.agents/skills/web/vercel-react-best-practices/SKILL.md) | React and Next.js performance optimization guidelines from Vercel Engineering. |
| [`vercel-react-view-transitions`](.agents/skills/web/vercel-react-view-transitions/SKILL.md) | Guide for implementing smooth, native-feeling animations using React's View Transition API (`<ViewTransition>` component, `addTransitionType`, and CSS view transition pseudo-elements). |
| [`web-design-guidelines`](.agents/skills/web/web-design-guidelines/SKILL.md) | Review UI code for Web Interface Guidelines compliance. |

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
