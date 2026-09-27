---
description: Read when using a browser or native app, repairing a local environment, or validating a live deployment.
alwaysApply: false
---

# Workspace Operations Rules

## Computer-Use Surface Failures

- Treat an inventory or availability error as scoped to the surface it names. A native-app lock or failure does not block browser automation, and a browser failure does not block terminal or API work.
- Before reporting a task blocked by a surface warning, inspect the requested surface directly and retry its normal recovery path. For a browser, refresh the tab inventory and reopen an authenticated task tab when the prior agent-owned tab has closed.
- Prefer an isolated agent-owned browser tab. When the user explicitly directs use of an existing
  browser tab or window for the current task, that instruction overrides the isolation preference;
  use only the authorized surface and leave every other user-owned surface untouched.
- Report a block only when the requested surface itself cannot complete the next required action and safe alternatives have been exhausted.

## Local Environments

- **Local stack resources are disposable, and repairing them is part of the work, never a question for the user.** Local databases and their migration state, Redis, Docker containers, volumes, networks, images and the daemon itself can be repaired, reset, dropped or recreated whenever the task needs them working. A database stuck on a revision a branch has since regenerated, a stale cache, a wedged container: fix it and carry on. The one limit is a resource another run is actively using, such as a test runner holding the stack's lock. Wait for it or use a separate resource; never stop it. Deployed and shared remote environments are not local; the next section governs them.

## Live Deployment Validation

- Treat create, update, and delete requests against a live deployment as data mutations, not health
  checks. Run them only against a target that the repository explicitly designates for mutation
  testing; when no such target exists, live smoke testing is read-only.
- When the same artifact and materially equivalent configuration run in several environments, one
  successful write test on the designated mutation target plus read-only health and routing checks
  on the others validates the shared path. Never create persistent synthetic records in a stable or
  shared staging environment merely to smoke-test a deployment.
