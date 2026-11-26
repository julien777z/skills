---
name: use-browser
description: Show the user a page the agent made, such as a dashboard or report, in their browser, reloading its tab in the task group; or operate a browser — by default a headless one the agent runs itself, and the harness's or an MCP browser only when the user asks for it or gives a specific URL to inspect or debug — to open websites, fill forms, click, take screenshots, extract data, test web apps, QA and bug hunts, sign in, or automate Electron apps and Slack. Use whenever a task opens, shows, reloads or controls a browser page, before selecting a browser or binding a task tab, and when a browser or app surface reports an inventory or availability error.
short_description: 'Show a local page in the user''s browser, or operate a browser.'
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*)
---

# Use Browser

Show a page in the user's browser, or operate a browser: by default a headless one the agent runs.

## Showing A Local Page

For an HTML file the agent wrote, such as a rendered dashboard, that the user should look at. This
route needs the user's browser on the machine that holds the file, since a `file://` address
resolves there; when it is not, such as a cloud session, this route does not apply.

Open the page in a task group in the user's browser, selected and bound as **Selecting And Binding
A Tab** says for the user's browser. If a task tab already shows it, reload that tab. Bring the
preview to the front only when the user asks to see it. If that browser cannot load the file, use
a local URL served to it or report the preview blocker.

## Operating A Browser

For the agent's own work in a browser: visiting sites, filling forms, clicking, screenshots,
extracting data, testing and QA, signing in, Electron desktop apps and Slack.

- **The agent's own headless browser is the default**, for public pages, local stacks, walkthroughs,
  screenshots, recordings, QA, sign-in to a test account and every other browser step, by the agent
  and by every worker, script or skill it runs. Drive it with the `agent-browser` CLI, which runs
  Chrome or Chromium headless over the DevTools protocol; `snapshot` lists the page's accessibility
  tree with references that later commands take as `@e1`, `@e2` and so on. Install it with
  `npm i -g agent-browser && agent-browser install`, and before its first command load its guide
  from the CLI, which matches the installed version: `agent-browser skills get core`, adding
  `--full` for the command reference. The headless route takes nothing from the user's browser:
  `--auto-connect`, `--profile` naming one of the user's browser profiles, and `connect` or `--cdp`
  aimed at a browser the user runs are the user's-browser route below.
- **Electron desktop apps and Slack**: the agent launches the app itself where it opens no window
  on the user's desktop, such as an isolated runner or a virtual display, with a DevTools port on
  127.0.0.1 (`--remote-debugging-port=<port>`) and a test profile and test data where the app takes
  them, and attaches the CLI with `agent-browser connect <port>`, as `agent-browser skills get
  electron` describes. Where no such place exists, the step is blocked as below. Launching it on
  the user's desktop, or attaching to an instance they already run, such as their signed-in Slack,
  is the user's-browser route and needs their request.
- **The harness's browser control or an MCP browser is used only when the user asks for it, or
  gives a specific URL to inspect or debug.** Then connect to their existing browser and the
  relevant profile, as **Selecting And Binding A Tab** says for the user's browser.
- If the headless browser cannot run, report the blocked browser step with its error and continue
  any work that can be verified independently. Never move to the user's browser or a harness
  preview, or ask the user to show or keep a window open, unless they asked for that route.

## Selecting And Binding A Tab

Bind the task's browser before reading, navigating or interacting.

In the agent's headless browser:

- Run one named session per task (`--session <name>`), record its name, and keep every action of
  the task in it. A restarted session keeps its name but loses its pages and sign-in, so after
  reconnecting or restarting browser control, read `agent-browser --session <name> get url` and a
  `snapshot` before the next action, then sign in again and return to the page when they were lost.

In the user's browser:

- Inventory browser metadata and select the user's existing browser and the relevant profile. An
  open user tab can identify the URL and profile, but leave that tab and the user's groups alone.
- Create a dedicated tab group for the task through the browser harness. Open task-owned tabs in
  that group, in the background when supported. Keep navigation, debugging, screenshots, sign-in,
  and verification in those tabs. Work with one tab when it suffices.
- Record the group and each tab's stable IDs. Bind each action and observation to the intended
  task tab, verifying the binding after reconnecting or switching. Keep the task group when
  replacing a closed tab. If the harness cannot create or bind a grouped tab, use its supported
  recovery or report the browser step as blocked.

In either browser:

- Treat an inventory or availability error as scoped to the surface it names. A native-app lock or
  failure does not block browser automation, and a browser failure does not block terminal or API
  work. Before reporting a task blocked by a surface warning, inspect the requested surface
  directly and retry its normal recovery path.
