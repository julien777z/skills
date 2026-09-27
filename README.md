# Skills

Skills and rules shared across my repositories. Their source lives in `.agents/`;
[Agent Sync](https://github.com/julien777z/agent-sync-action) prepares them for Claude, Codex,
and Cursor.

## Quick Start

Run `bash bootstrap/install.sh` from your main checkout. The installer links that checkout into
your Claude, Codex, and Cursor user directories. Pull `main` to update the installed guidance;
make edits in a separate branch or worktree.

For Claude cloud, add this to the start of your environment setup script:

```bash
set -e
install -d -o claude -g claude /home/claude/.local/share
if [ ! -d /home/claude/.local/share/agent-skills/.git ]; then
  runuser -u claude -- git clone https://github.com/julien777z/skills.git /home/claude/.local/share/agent-skills
fi
bash /home/claude/.local/share/agent-skills/bootstrap/cloud-install.sh
```

The cloud installer uses an attached checkout when available and the setup clone otherwise.

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

Follow a link for the skill's description and instructions. This index is generated from the skill
files.

<!-- skills:start -->

### User-Invoked

These run only when you ask for them by name, such as `/refactor`.

- [`assume-library-update`](.agents/skills/execution/assume-library-update/SKILL.md) · [`ci-watch`](.agents/skills/git/ci-watch/SKILL.md) · [`config-doctor`](.agents/skills/doctors/config-doctor/SKILL.md) · [`cr`](.agents/skills/git/cr/SKILL.md)
- [`defer-execution`](.agents/skills/deferrals/defer-execution/SKILL.md) · [`dependency-doctor`](.agents/skills/doctors/dependency-doctor/SKILL.md) · [`docs-doctor`](.agents/skills/doctors/docs-doctor/SKILL.md) · [`execute-defer-scope`](.agents/skills/deferrals/execute-defer-scope/SKILL.md)
- [`grade-plans`](.agents/skills/execution/grade-plans/SKILL.md) · [`guidance-doctor`](.agents/skills/doctors/guidance-doctor/SKILL.md) · [`hand-off`](.agents/skills/workspace/hand-off/SKILL.md) · [`incident`](.agents/skills/execution/incident/SKILL.md)
- [`legacy-doctor`](.agents/skills/doctors/legacy-doctor/SKILL.md) · [`manage-mcps`](.agents/skills/workspace/manage-mcps/SKILL.md) · [`migrations-doctor`](.agents/skills/doctors/migrations-doctor/SKILL.md) · [`new-doctor`](.agents/skills/doctors/new-doctor/SKILL.md)
- [`refactor`](.agents/skills/execution/refactor/SKILL.md) · [`schema-doctor`](.agents/skills/doctors/schema-doctor/SKILL.md) · [`skill-gauntlet`](.agents/skills/authoring/skill-gauntlet/SKILL.md) · [`study-games`](.agents/skills/roblox/study-games/SKILL.md)
- [`take-over-pr`](.agents/skills/git/take-over-pr/SKILL.md) · [`tests-doctor`](.agents/skills/doctors/tests-doctor/SKILL.md)

### Model-Invoked

An agent reaches for these on its own whenever the work calls for them.

- [`acceptance-gate`](.agents/skills/review/acceptance-gate/SKILL.md) · [`agent-browser`](.agents/skills/workspace/agent-browser/SKILL.md) · [`agent-lock`](.agents/skills/workspace/agent-lock/SKILL.md) · [`async-python-patterns`](.agents/skills/python/async-python-patterns/SKILL.md)
- [`awesome-design`](.agents/skills/web/awesome-design/SKILL.md) · [`banned-terminology`](.agents/skills/review/banned-terminology/SKILL.md) · [`build-types`](.agents/skills/web/build-types/SKILL.md) · [`clerk-nextjs-patterns`](.agents/skills/web/clerk-nextjs-patterns/SKILL.md)
- [`code-review`](.agents/skills/review/code-review/SKILL.md) · [`code-simplify`](.agents/skills/review/code-simplify/SKILL.md) · [`coordinate-repositories`](.agents/skills/workspace/coordinate-repositories/SKILL.md) · [`current-changes`](.agents/skills/git/current-changes/SKILL.md)
- [`database-migrations`](.agents/skills/python/database-migrations/SKILL.md) · [`defer-scope`](.agents/skills/deferrals/defer-scope/SKILL.md) · [`design-taste-frontend`](.agents/skills/web/design-taste-frontend/SKILL.md) · [`doctor-protocol`](.agents/skills/doctors/doctor-protocol/SKILL.md)
- [`edit-skill`](.agents/skills/authoring/edit-skill/SKILL.md) · [`execute-task`](.agents/skills/execution/execute-task/SKILL.md) · [`frontend-design`](.agents/skills/web/frontend-design/SKILL.md) · [`generic-push`](.agents/skills/git/generic-push/SKILL.md)
- [`get-doctors`](.agents/skills/doctors/get-doctors/SKILL.md) · [`i-have-adhd`](.agents/skills/execution/i-have-adhd/SKILL.md) · [`image-to-code`](.agents/skills/web/image-to-code/SKILL.md) · [`linear`](.agents/skills/workspace/linear/SKILL.md)
- [`list-prs`](.agents/skills/workspace/list-prs/SKILL.md) · [`list-repos`](.agents/skills/workspace/list-repos/SKILL.md) · [`list-rules`](.agents/skills/workspace/list-rules/SKILL.md) · [`list-skills`](.agents/skills/workspace/list-skills/SKILL.md)
- [`luau`](.agents/skills/roblox/luau/SKILL.md) · [`merge-conflict`](.agents/skills/git/merge-conflict/SKILL.md) · [`no-text-ai-slop`](.agents/skills/review/no-text-ai-slop/SKILL.md) · [`plan-change`](.agents/skills/execution/plan-change/SKILL.md)
- [`pre-production`](.agents/skills/execution/pre-production/SKILL.md) · [`prisma-client-api`](.agents/skills/web/prisma-client-api/SKILL.md) · [`propagate-skill`](.agents/skills/workspace/propagate-skill/SKILL.md) · [`python-anti-patterns`](.agents/skills/python/python-anti-patterns/SKILL.md)
- [`python-background-jobs`](.agents/skills/python/python-background-jobs/SKILL.md) · [`python-configuration`](.agents/skills/python/python-configuration/SKILL.md) · [`python-design-patterns`](.agents/skills/python/python-design-patterns/SKILL.md) · [`python-error-handling`](.agents/skills/python/python-error-handling/SKILL.md)
- [`python-performance-optimization`](.agents/skills/python/python-performance-optimization/SKILL.md) · [`python-project-structure`](.agents/skills/python/python-project-structure/SKILL.md) · [`python-resilience`](.agents/skills/python/python-resilience/SKILL.md) · [`python-resource-management`](.agents/skills/python/python-resource-management/SKILL.md)
- [`python-testing-patterns`](.agents/skills/python/python-testing-patterns/SKILL.md) · [`python-type-safety`](.agents/skills/python/python-type-safety/SKILL.md) · [`rebuild-git-history`](.agents/skills/git/rebuild-git-history/SKILL.md) · [`roblox-building`](.agents/skills/roblox/roblox-building/SKILL.md)
- [`roblox-gameplay`](.agents/skills/roblox/roblox-gameplay/SKILL.md) · [`roblox-react`](.agents/skills/roblox/roblox-react/SKILL.md) · [`roblox-studio`](.agents/skills/roblox/roblox-studio/SKILL.md) · [`run-site`](.agents/skills/workspace/run-site/SKILL.md)
- [`security-audit`](.agents/skills/review/security-audit/SKILL.md) · [`storyline`](.agents/skills/roblox/storyline/SKILL.md) · [`subagent-selection`](.agents/skills/execution/subagent-selection/SKILL.md) · [`tailwind-design-system`](.agents/skills/web/tailwind-design-system/SKILL.md)
- [`test-fixture`](.agents/skills/authoring/test-fixture/SKILL.md) · [`test-skill`](.agents/skills/authoring/test-skill/SKILL.md) · [`text-highlight`](.agents/skills/git/text-highlight/SKILL.md) · [`vercel-composition-patterns`](.agents/skills/web/vercel-composition-patterns/SKILL.md)
- [`vercel-react-best-practices`](.agents/skills/web/vercel-react-best-practices/SKILL.md) · [`vercel-react-view-transitions`](.agents/skills/web/vercel-react-view-transitions/SKILL.md) · [`web-design-guidelines`](.agents/skills/web/web-design-guidelines/SKILL.md)

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
