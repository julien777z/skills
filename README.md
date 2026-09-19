# Skills

Shared agent skills for every repository, in one place.

## Features

- One canonical copy of each generic skill under `.agents/skills/`, mirrored to Claude, Cursor, and
  Codex by [Agent Sync](https://github.com/julien777z/agent-sync-action).
- The subagent definitions those skills run on, under `.agents/agents/`.
- Third-party skills registered in `.agents/external_skills.json` and vendored by the same workflow.
- `bootstrap/install.sh` links everything into the user-level roots a machine has, so every
  repository's session sees the same skills.

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
| `.claude/`, `.cursor/`, `.codex/`, `AGENTS.md` | Provider mirrors the workflow generates on `main`; never edited by hand. |
| `bootstrap/install.sh` | Links the skills and agents into the user-level roots. |

## Repository-Provided Skills

A shared skill that needs something only one repository can supply names the role and finds the
skill through the skill listing; the repository's `project.md` says which local skill fills it.

| Role | What the repository provides |
|---|---|
| `pre-production` | Its product state and target-contract policy, under that exact name. |
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
