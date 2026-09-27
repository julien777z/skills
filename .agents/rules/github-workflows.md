---
description: Read when creating or editing GitHub Actions workflows, workflow scripts, or CI dependency installation. Keep workflow YAML concise and test workflows separate from release actions.
alwaysApply: false
paths:
- '.github/workflows/**/*'
- '.github/scripts/**/*'
- 'action.yml'
- 'action.yaml'
- '**/action.yml'
- '**/action.yaml'
---

# Github Workflows Rules

## Workflows

- Treat a request for CI tests as authorization for test workflows only. Inspect a workflow's jobs
  and triggers before dispatching it; a workflow that builds and publishes artifacts or deploys is
  a release action even if it also runs tests.

- Keep `run` steps declarative. Invoke checked-in scripts for control flow, validation, filesystem changes, or other implementation logic instead of embedding arbitrary shell or program code in workflow YAML; place those scripts under `.github/scripts/` and prefer Python.
- Do not hard-code runtime versions when a shared action, reusable workflow, or repository version file supplies them; omit `python-version` when shared Python automation provides it, and use `node-version-file: ".nvmrc"` for Node.js workflows.
- Do not add glue steps that only read versions or forward setup data. Pass repository-owned version files and inputs directly to the action that uses them whenever supported.
- Keep workflow files concise: merge related setup and dependency commands into one clearly named generic step when their execution order and conditions allow it. Do not split tool or package installation into separate steps merely by dependency.
- Environment configuration that tunes a tool — retry counts, timeouts, cache locations, path entries — belongs in the step that installs or runs that tool, not in a step of its own. A step whose whole body writes to `$GITHUB_ENV` is named for a concern rather than an action, and the reader has to look elsewhere to find out which later step it affects. Write those exports at the end of the owning step so the setting and its consumer stay together.
- Add an explanatory comment when an edge case requires an explicit version override.

## Dependency Installation

- Declare project dependencies used by workflows in the repository's dependency manifests and commit their lockfiles.
- Run project-level installation commands such as `poetry install` or `npm install` in workflows.
- Do not install individual project packages or embed their versions directly in workflow commands.
