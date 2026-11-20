---
name: use-browser
description: Show the user a page the agent made, such as a dashboard or report, in their browser, reloading the tab already opened for it; or operate a browser — the user's own, or one the agent runs with the agent-browser CLI — to open websites, fill forms, click, take screenshots, extract data, test web apps, QA and bug hunts, sign in, or automate Electron apps and Slack. Use whenever a task opens, shows, reloads or controls a browser page.
short_description: 'Show a local page in the user''s browser, or operate a browser.'
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*)
---

# Use Browser

Two jobs. **Showing a local page** puts a file the agent made in front of the user. **Operating a
browser** has the agent work in one, the user's or its own.

## Showing A Local Page

For an HTML file the agent wrote, such as a rendered dashboard, that the user should look at. This
route needs the user's browser on the machine that holds the file, since a `file://` address
resolves there; when it is not, such as a cloud session, this route does not apply.

1. **Find the tab already showing it.** The task's record of this page, kept wherever the caller
   keeps task state, holds the tab it was opened in and the file it shows. A tab still showing that
   file is the one to use.
2. **Reload, never reopen.** A page that refreshes itself when its file changes needs nothing
   once it is open. For any other page, when that tab exists and the harness has a tool that
   controls the user's browser, navigate it to the file's address again, which reloads it. Bring it
   to the front only when the user asked to see the change.
3. **Otherwise open it once.** Open `file://<absolute path>` in a new tab with the tool that controls
   the user's browser, selecting the browser as **Selecting And Binding A Tab** says,
   and record the tab and the file. When there is no such tool, or it cannot open a `file://`
   address, open the file with the system opener — `open <path>` on macOS, `xdg-open <path>` on
   Linux, `start "" <path>` on Windows — and record that it is open. Never open it again after a
   later change unless the user asks; a page that does not refresh itself and that this route
   cannot reload gets one line saying it changed and needs a reload.

## Operating A Browser

For the agent's own work in a browser: visiting sites, filling forms, clicking, screenshots,
extracting data, testing and QA, signing in, Electron desktop apps and Slack.

- **Pick the browser by what the work needs.** Use the harness's tool for the user's browser when
  the work needs the user's accounts, sessions or open tabs. Use the `agent-browser` CLI when the
  agent needs a browser of its own, such as for a walkthrough, screenshots or QA. Either way,
  choose and bind to one tab as **Selecting And Binding A Tab** says.
- The `agent-browser` CLI drives Chrome or Chromium over the DevTools protocol with
  accessibility-tree snapshots and `@eN` element references. Install it with
  `npm i -g agent-browser && agent-browser install`.
- Before its first command, load its guide from the CLI, which matches the installed version:
  `agent-browser skills get core`, adding `--full` for the command reference. Load a specialized
  guide when the target is not a web page, such as `electron`, `slack` or `dogfood` for exploratory
  testing; `agent-browser skills list` names them all.
- Its observability dashboard runs on port 4848, also reachable through a forwarded address such as
  `https://dashboard.agent-browser.localhost`; stay on that origin, which proxies the sessions.

## Selecting And Binding A Tab

Whichever browser the work uses, every read, navigation and interaction goes through one tab
selected and bound this way.

- Before reading page content, navigating or interacting, inventory the browser metadata the tool
  exposes and select the surface most relevant to the task. Preserve every browser, profile, window
  or tab constraint the user set, and ask about a concrete conflict or one the tool cannot verify or
  honor rather than silently choosing another account or surface. Within those constraints, prefer
  the exact task page, then a related page in the correct account and work context, rather than the
  active or default surface. A shared domain or title alone does not establish task relevance. An
  explicit task reference or metadata that identifies a candidate can make it eligible for narrow
  account or work-context confirmation when no unsaved-work or other-agent conflict is known; do not
  inspect a speculative candidate only to resolve ambiguity. Inspect an eligible candidate only as
  needed to verify it, leaving unrelated pages untouched.
- Reuse the most relevant suitable existing tab when doing so preserves unsaved work and does not
  interfere with another agent's use. Claim or coordinate exclusive control before acting; an
  inventory match alone grants neither ownership nor authority for a new action. If no suitable
  tab can be reused safely, create a task-owned tab in the most relevant available parent surface
  when the tool can select one, in the background when supported. Otherwise use its supported
  browser or tab route without asserting unavailable parent context. Create a window only when the
  tool supports it and none suitable exists.
- Retain the selected tab's handle or stable ID together with every available parent-surface ID and
  explicit user constraint, and bind subsequent actions to it. With tools that act on a selected
  tab, explicitly select that ID and verify it before each action batch and after reconnecting or
  switching tabs, and verify that the control itself targets the stable tab independently of the
  foreground selection. A matching URL, active tab, browser profile or session label is not evidence
  of control, and an application handle that follows the active tab or window does not preserve the
  binding. When the binding is lost or the bound tab closes, refresh the inventory and repeat the
  selection and reuse above within the retained constraints and coordination requirements before
  binding again; a replacement is a task-owned tab a supported tab control creates, never a window.
  If the control cannot reach the required page, hold only that operation and continue independent
  work. Never fall back to inspecting or operating the browser's current tab.
- Treat an inventory or availability error as scoped to the surface it names. A native-app lock or
  failure does not block browser automation, and a browser failure does not block terminal or API
  work. Before reporting a task blocked by a surface warning, inspect the requested surface
  directly and retry its normal recovery path.
