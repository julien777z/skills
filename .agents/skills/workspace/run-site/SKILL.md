---
name: run-site
description: Bring an application stack up and repair startup blockers. Guidance-required browser walkthroughs apply only in cloud execution environments; explicit user requests for browser work apply in either environment. Use when a change needs applicable browser verification, when a page is behind sign-in, when services are not running, when a bootstrap or environment problem blocks local work, or when asked to show that the app works.
short_description: 'Start an application stack and perform browser verification where applicable.'
---

# Run Site

Start and verify the stack within the requested scope. When browser verification applies under
**Principles**, its deliverable includes screenshots and a recording showing signed-in functionality.

## Dependencies

- `agent-browser` — the browser automation CLI this skill drives.
- `execute-task` — what happens to a defect a walkthrough finds, under its **Encountered Issues**.
- `proton-pass` — a sign-in password the repository provides no source for.

## Principles

- Select browser verification applicability before starting its stack, browser or sign-in
  prerequisites. Guidance-required walkthroughs and rendered UI inspections apply only when the
  agent executes in a cloud environment. Classify the agent's execution environment, not the
  application's address: a cloud agent checking a service on localhost still follows the cloud
  requirement. In a local execution environment, mark this verification not applicable; do not
  recreate it under another validation label or hold completion for its prerequisites. Browser
  work the user explicitly requests, including debugging or verification, applies in either
  environment. Stack startup and non-browser validation required by the task still apply.
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
| Frontend only | Serve the site; when browser verification applies, drive the UI as far as it goes without a live API |
| Both | Start and verify both; when browser verification applies, perform the full walkthrough below |

Never assume the other repository exists, and never fail because it does not. Name whatever did not
run, and why, beside the result.

## Start and verify the stack

Read each present repository's startup and schema-provisioning commands, services, ports, health
probes, log locations, and recovery facts from its project guidance, opening every
`.agents/references/` file its `project.md` points to: such facts usually live there rather than in
`project.md` itself.
Start the backend first when both are present. Run the owning startup command with the authorized
environment and inspect actual readiness. Reuse healthy dependencies; repair the startup owner rather
than relying on an unrecorded workaround. Never conclude the stack is out of reach by reasoning about
what it probably needs: run the startup command and let it fail first.

If Docker is required, inspect its current state and use the host's supported startup procedure; a
restored snapshot restores files, not a running daemon. Check ownership before touching existing
services; a running container does not prove another test is active. Keep secrets out of logs and
preserve configured ports.

| Symptom | Likely cause | Fix at the owner |
|---|---|---|
| Every authenticated request returns 401 | A checked-in placeholder shadowed the real value from the session environment | Make the environment win over the dotenv layers; read the running process's environment to confirm |
| A service starts but every query fails | The database has no schemas | Run schema provisioning before launch and read its output for the failing service |
| A module is missing at import though the manifest names it | It is declared where the package manager does not install it | Declare it in the manifest's install list, re-lock, and install; never patch the environment by hand |
| A setup command reports missing settings before doing anything | It imports something that builds the application config at import time | Import only what build tooling needs, and keep a test guarding it |
| A `run`-style script reports command not found | Its entry point is registered only by an install that has not run since | Invoke bootstrap commands as modules so they need no registration |
| A dependency service refuses connections | It is not in the started set | Start it through the launcher's service selection |
| The browser reaches loopback but no external host | The egress relay accepts only HTTPS CONNECT tunnels | Bypass the proxy for loopback in the browser configuration |
| The browser fails with a connection reset where `curl` succeeds | An inspecting proxy resets the browser's TLS 1.3 handshake | Cap the browser's TLS version in its configuration; never read this as no browser egress |
| Signed in, but mutations no-op and the console reports a cookie failure | The page is not a secure context, so `crypto.subtle` is undefined | Serve and browse on `localhost`, not a wildcard bind address |
| A click reports success and no request follows | The ref resolved but the event never reached the handler | Click the element through `eval` and confirm the request in the service log |

## Prove it works in a browser

### When a walkthrough is owed

After selecting browser verification applicability under **Principles**, perform the following
walkthrough only when it applies. Passing tests, type checks, and a clean build do not replace an
applicable walkthrough. A change that can alter what the app does — new or reordered UI, layout or
spacing, a component's props or state, a hook, a route, a redirect, middleware, an auth round trip, or the shape
of a request — is walked end to end before it is reported done, however few lines it took; the
walkthrough follows the push rather than holding it, as `execute-task`'s **Pre-Push Gate** says. An
edit that provably cannot reach behavior — rewording text already rendered in its existing slot, a
comment, prose in Markdown — is verified by reading it and by finding the new text in the build
output and the old text nowhere in the tree. Judge by what the edit touches, not how small it looks:
moving text into a shared constant stays a copy change only while every call site keeps its slot. Where a component has no surface in the running app,
say so and name what only a harness rendered.

### Sign in

Use the repository's normal sign-in flow and the test identity, tenant, fixtures, provider modes,
and persistence checks its project guidance names. Use those facts exactly and reuse
what exists: never invent a test identity or turn a provider fixture into a generic workflow. **Never work around the sign-in wall**: a
preview route, a stubbed page, a component mounted where it does not ship, or a widened public-route
matcher proves the component renders and nothing about the screen a user reaches. If sign-in
genuinely cannot complete, report the walkthrough as not done. Drive the browser automation's own
profile; never read the user's saved passwords, cookies, local storage, or session files.

Keep a password out of argv and the transcript: put it in an environment variable for the one
command that fills the field, build the script that fills the field, and pipe it to the browser
command through stdin. The password comes from what the repository provides — the file project
guidance names, or the helper its tooling uses to set or generate a test identity's password, run
first when the identity has none yet — and through `proton-pass` only for an account the
repository provides no source for, such as a deployed or third-party one. Set the value through the native setter and dispatch a bubbling `input` event so a
framework-controlled input registers it:

```bash
# Account with no repository source: SIGN_IN_PASSWORD="$(PROTON_PASS_AGENT_REASON="<why>" pass-cli item view \
#   --vault-name "<vault>" --item-title "<title>" --field password)"
SIGN_IN_PASSWORD="$(cat <password-file>)" python3 - <<'EOF' | agent-browser --session <name> eval --stdin
import json, os
secret = os.environ["SIGN_IN_PASSWORD"]
js = ("const el=document.querySelector('input[type=\"password\"]');"
      "Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(el,%s);"
      "el.dispatchEvent(new Event('input',{bubbles:true}));'ok'") % json.dumps(secret)
print(js)
EOF
```

### Drive the change

- Drive the **local** production build the startup command serves, never a dev server and never the
  deployed domain: prefetching, caching, and middleware behave differently under a dev server, and a
  deployed site proves nothing about this checkout. Snapshot after every navigation; refs do not
  survive it.
- **Operate the control the change touched, not the page that holds it**, with real input events on
  every screen that mounts it, then read the state it was meant to leave — where the element landed,
  what the field holds, whether the list closed up — and reload where it persists something. A drag
  is several moves, not one jump:

  ```bash
  agent-browser --session <name> mouse move <x> <y>
  agent-browser --session <name> mouse down
  agent-browser --session <name> mouse move <x2> <y2>
  agent-browser --session <name> mouse up
  ```

- A library doing the work is a reason to exercise it, never an exemption: the arguments handed to it
  and the state handed back belong to the change.
- Distinguish tool success from application success: confirm the intended request happened, then read
  its result back through the documented API or the database rows it created. A health response
  proves the process is up, never signed-in rendering or behavior.
- Read the whole changed screen against the repository's interface rules while it is on screen:
  judge the headings, labels and hints as rendered, whether related controls belong together, and
  whether controls with comparable roles have a consistent shape, spacing and recovery from errors.
  Open a comparable existing flow for each recurring interaction the change adds or moves,
  including how related items are selected,
  changed and removed; compare the placement and editing path as well as the result. A violation is
  a defect the walkthrough found.
- The browser daemon starts a fresh profile each time, so `state save` a signed-in session that must
  survive a restart.

### Widths and full-page captures

Walk every changed screen at several widths — at least 1280, 1536 and 2000 pixels, plus a phone width
when the screen is reachable on one — and on each confirm the document does not scroll sideways and
everything the change touched is visible and usable. **Capture the full page, always.** A capture
taken while the window is shorter than the page draws fixed chrome such as a sidebar only as tall as
the window, leaving an empty band that reads as a layout bug, so size the viewport to the page's full
height before each capture — the larger of the document's and its scrolling container's scroll
height — and restore it before interacting again:

```bash
for width in 1280 1536 2000; do
  agent-browser --session <name> set viewport "$width" 900
  agent-browser --session <name> eval "document.documentElement.scrollWidth <= innerWidth"
  height=$(agent-browser --session <name> eval \
    "Math.max(document.documentElement.scrollHeight, document.querySelector('<scroll-container>')?.scrollHeight ?? 0)")
  agent-browser --session <name> set viewport "$width" "$height"
  agent-browser --session <name> screenshot --full <path>-"$width".png
  agent-browser --session <name> set viewport "$width" 900
done
```

### Without the API changes it relies on

A frontend change that reads a new route, field, or value deploys independently of the API, so walk
every page it touches again against an API without those changes — the deployed API, or those
requests made to fail. A failing request can surface anything, so read the whole page against the
intended behavior: each failing section shows its own explicit error, the rest stays usable, and the
page settles after its first load with nothing refetching, reloading, or navigating on its own. Watch
the network panel for the whole wait. A refetch loop, a blank page, a section shown as empty rather
than failed, an action enabled on data that never arrived, or a mode derived from a missing response
is a defect in the change.

### Defects

Anything the run shows that the product should not do — an error the run did not ask for (a
failed request, an empty section, an error boundary, an unwritten redirect, a console error) or
wrong behaviour on screen (a value shown altered or lost, data in the wrong place, a broken
layout) — is a defect the walkthrough found, and `execute-task`'s **Encountered Issues** decides
what happens to it. Diagnose it to its cause through the service log, the network response, and the
rendering code, fix it, and re-run the step. The one exception is the failure you induced on the
run above; say which kind each capture shows, since the two look identical.

### Evidence

Record the flow until the feature is exercised to its end — the form submitted and its result read
back, the item seen in its list, the setting confirmed after a reload. Start recording before signing
in: starting a recording opens a fresh browser context, so a session signed in before it is gone.
The recorder writes WebM, which some viewers cannot play; send the MP4:

```bash
agent-browser --session <name> record start <path>.webm
agent-browser --session <name> record stop
ffmpeg -y -i <path>.webm -c:v libx264 -pix_fmt yuv420p -movflags +faststart -an <path>.mp4
```

Send the recording and a still of the view the change touched, unasked, plus a still per width, the
page with its requests failing, and each defect with the fix that resolved it — as the run produces
them, as the User-Facing Output rule requires. Captures left on disk are a walkthrough the reader
never saw. The report names the widths checked, whether the run without the API changes was done,
and what the screens were read against.
