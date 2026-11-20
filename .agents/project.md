# Shared Rules

Use these rules in any repository. Open a relevant file from your agent's user-level `rules/`
directory before working in its area. This repository keeps the source files in `.agents/rules/`.
The descriptions also cover work that file patterns alone cannot identify.

| Rule | Read it when… |
| --- | --- |
| `biome.md` | Formatting or linting TypeScript and TSX, or changing `biome.json`. |
| `fastapi.md` | Changing Python routes, dependencies, request handling, or responses. |
| `github.md` | Working with Actions, pull requests, commits, or repository documentation. |
| `http.md` | Designing or changing HTTP clients, provider calls, server API operations and policy, or response statuses. |
| `poetry.md` | Changing Python dependencies, project configuration, or test setup. |
| `pydantic.md` | Defining models and settings or changing validation and serialization. |
| `python.md` | Editing Python typing, imports, modules, constants, functions, control flow, or logging. |
| `python-boundaries.md` | Changing Python settings, client injection, model placement, caching, external API calls, or error handling. |
| `python-formatting.md` | Formatting Python code or writing its docstrings and comments. |
| `react.md` | Building components, hooks, rendering and events, or Next.js App Router surfaces. |
| `react-copy-and-forms.md` | Writing interface copy, confirmation dialogs, or forms in React. |
| `react-layout.md` | Building or changing shared surfaces, page layouts, spacing, or responsive behavior in React. |
| `sqlalchemy.md` | Defining tables or relationships, writing queries, or handling sessions. |
| `typescript.md` | Editing types, modules, imports, functions, or external-data boundaries. |

## Verification

- Do not add or maintain tests, test fixtures, test-support modules, test runners, or test CI in this repository, including for bootstrap and tooling code. Validate changes with source checks and temporary, untracked execution checks; do not commit those checks or introduce a replacement test suite.
