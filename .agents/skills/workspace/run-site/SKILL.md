---
name: run-site
description: Bring a local application stack up, repair startup blockers, and prove the running site works by driving a real browser through sign-in and core functionality with screenshots. Use when services are not running, when a bootstrap or environment problem blocks local work, or when asked to show that the app works.
---

# Run Site

The deliverable is evidence: a reader should finish with screenshots and a recording showing a
signed-in dashboard doing real work, not a claim that it started.

## Dependencies

- `agent-browser` — the browser automation CLI this skill drives.

## Principles

- Setup is agent-agnostic. Any agent must be able to run it, so never hard-code an absolute path,
  a home directory, a machine-specific port, or an assumption about which agent is running.
  Resolve the repository root from the script's own location and read every other path from there.
- When something is not running, fix the owning startup/bootstrap implementation rather
  than working around it with one-off commands in the session. A fix that lives only in a
  transcript is not a fix.
- Values injected into the agent's session (runtime credentials and proxy variables) are not present
  when the environment's own bootstrap runs. Anything depending on them must stay re-runnable and
  must let the live environment win over checked-in defaults.
- **Every command the setup path runs must work from a bare shell** — a fresh clone, no prior
  install, no environment loaded, nothing already running. Setup cannot depend on the state it
  exists to create. Concretely: a bootstrap command must not need a console entry point that only
  a prior install registers, and must not import anything that reads the application's runtime
  settings, because those settings are the thing being configured. Resolve the environment inside
  the command instead of requiring the caller to have exported it.
- **When you find one of these, fix it — do not report it as a caveat.** "Run this other thing
  first" is the defect, not the workaround. A setup step with a documented precondition is a setup
  step that will fail for whoever does not read the document.

## Work out which repositories are present

The stack spans a backend and a frontend that live in separate repositories, and either may be
absent. Detect what is checked out — from this repository's root and its sibling directories —
and scale the work to match:

| Present | What to do |
|---|---|
| Backend only | Start the services, verify the health endpoints and `/docs`, exercise the API directly |
| Frontend only | Serve the site and drive the UI as far as it goes without a live API |
| Both | The full walkthrough below, browser included |

Never assume the other repository exists, and never fail because it does not.

## Start and verify the stack

Read the operational profile named by project rules for the startup and schema-provisioning commands, configured services, ports, health probes, log locations, and concrete recovery steps. Run the owning startup command with the authorized environment and inspect actual readiness. Reuse healthy dependencies; repair the startup owner rather than relying on an unrecorded workaround.

If Docker is required, inspect its current state and use the host's supported startup procedure. Check ownership before touching existing services; a running container does not prove another test is active. Diagnose missing schemas, environment precedence, dependency declarations, and missing services at their owner. Keep secrets out of logs and preserve configured ports.

## Prove it works in a browser

Use the local production build when verifying production behavior. Follow the project's normal sign-in and approved reusable test identity/tenant; never invent an authentication bypass. Snapshot after navigation. Operate the actual affected controls, perform a meaningful workflow, and read the resulting state back through the documented API or persistence boundary. Capture screenshots and a recording of that flow, not just the initial page.

Distinguish tool success from application success: verify the intended event and request occurred, then inspect its result. A startup health response alone does not establish signed-in rendering or behavior. Repair observed failures before reporting the walkthrough complete.

## Domain-specific walkthroughs

Read the repository operational profile for approved fixtures, identities, provider modes, and persistence checks. Use those facts exactly; do not invent test identities or turn a provider fixture into a generic workflow.
