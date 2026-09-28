# Skills Repository

This repository holds shared skills, rules, and agent definitions for Claude, Codex, and Cursor.
`.agents/` is the source; Agent Sync prepares provider files from it after pushes to `main`.

## Working rules

- Edit the canonical file under `.agents/`. Leave `AGENTS.md` and `.agents/.auto_generated/` to
  Agent Sync. Use `edit-skill` when changing a skill, rule, or agent definition.
- Keep reusable guidance independent of any one consuming repository. Put facts about this
  repository, including its layout and installer, in this file.
- Declare a scoped rule's file patterns once under `paths`; do not repeat them under `globs`.
  Agent Sync links Claude to the canonical rule and writes Cursor's `globs` format.
- Keep `alwaysApply: true` for guidance every session needs. A topic rule's description should
  say when to read it, including tasks its file patterns cannot capture.
- Run `python3.12 .agents/skills/authoring/edit-skill/scripts/validate_sources.py` to check sources
  against the Agent Sync version used by the workflow. Run
  `python3 .github/scripts/render_readme_skills.py --check` after changing skill metadata.

## Project docs

This file covers repository-wide conventions. The rules below hold the detailed guidance for a
particular technology or task. Read the relevant rule before changing that area.

| Rule | Read it when… |
| --- | --- |
| [Biome](/.agents/rules/biome.md) | Formatting or linting TypeScript and TSX, or changing `biome.json`. |
| [FastAPI](/.agents/rules/fastapi.md) | Changing Python routes, dependencies, request handling, or responses. |
| [GitHub](/.agents/rules/github.md) | Working with Actions, pull requests, commits, or repository documentation. |
| [HTTP](/.agents/rules/http.md) | Adding or changing Python HTTP clients or provider calls. |
| [Poetry](/.agents/rules/poetry.md) | Changing Python dependencies, project configuration, or test setup. |
| [Pydantic](/.agents/rules/pydantic.md) | Defining models and settings or changing validation and serialization. |
| [Python](/.agents/rules/python.md) | Editing Python typing, modules, control flow, errors, logging, or style. |
| [React](/.agents/rules/react.md) | Building components, hooks, layouts, or Next.js App Router surfaces. |
| [SQLAlchemy](/.agents/rules/sqlalchemy.md) | Defining tables or relationships, writing queries, or handling sessions. |
| [Testing](/.agents/rules/testing.md) | Writing or moving tests, fixtures, assertions, or test configuration. |
| [TypeScript](/.agents/rules/typescript.md) | Editing types, modules, imports, functions, or external-data boundaries. |

## Layout and installation

| Path | Purpose |
| --- | --- |
| `.agents/global.md` | Instructions installed for every session. |
| `.agents/project.md` | Conventions for this repository, included in generated `AGENTS.md`. |
| `.agents/rules/` | Canonical topic rules linked or mirrored for providers. |
| `.agents/skills/` and `.agents/agents/` | Skills and agent definitions. |
| `.agents/.auto_generated/` | Provider outputs created by Agent Sync. |
| `bootstrap/install.sh` | Links guidance from the main checkout into user-level roots. |

Run `bash bootstrap/install.sh` from the main checkout to refresh installed links. The README
lists the available skills and explains local and Claude cloud setup.
