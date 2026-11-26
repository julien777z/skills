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

Open the page in the task group selected below. If a task tab already shows it, reload that
tab. Bring the preview to the front only when the user asks to see it. If the selected browser
cannot load the file, use a local URL served to that browser or report the preview blocker.

## Operating A Browser

For the agent's own work in a browser: visiting sites, filling forms, clicking, screenshots,
extracting data, testing and QA, signing in, Electron desktop apps and Slack.

- **The agent's own headless browser is the default**, for public pages, local stacks, walkthroughs,
  screenshots, QA, sign-in to a test account and every other browser step, by the agent and by
  every worker, script or skill it runs. Drive it with the `agent-browser` CLI, which runs Chrome or
  Chromium headless over the DevTools protocol with accessibility-tree snapshots and `@eN` element
  references. Install it with `npm i -g agent-browser && agent-browser install`, and before its
  first command load its guide from the CLI, which matches the installed version:
  `agent-browser skills get core`, adding `--full` for the command reference.
- **The harness's browser control or an MCP browser is used only when the user asks for it, or
  gives a specific URL to inspect or debug in their own browser.** Then connect to their existing
  browser and the relevant profile, as **Selecting And Binding A Tab** says.
- If the headless browser cannot run, report the blocked browser step with its error and continue
  any work that can be verified independently. Never move to the user's browser or a harness
  preview, or ask the user to show or keep a window open, unless they asked for that route.

## Selecting And Binding A Tab

Bind a tab in the selected browser before reading, navigating or interacting.

- In the agent's headless browser, run one named session per task (`--session <name>`), record
  its name, and keep every action of the task in it.
- In the user's browser, inventory browser metadata and select the user's existing browser and the relevant profile. An
  open user tab can identify the URL and profile, but leave that tab and the user's groups alone.
- Create a dedicated tab group for the task through the browser harness. Open task-owned tabs in
  that group, in the background when supported. Keep navigation, debugging, screenshots, sign-in,
  and verification in those tabs. Work with one tab when it suffices.
- Record the group and each tab's stable IDs. Bind each action and observation to the intended
  task tab, verifying the binding after reconnecting or switching. Keep the task group when
  replacing a closed tab. If the harness cannot create or bind a grouped tab, use its supported
  recovery or report the browser step as blocked.
- Treat an inventory or availability error as scoped to the surface it names. A native-app lock or
  failure does not block browser automation, and a browser failure does not block terminal or API
  work. Before reporting a task blocked by a surface warning, inspect the requested surface
  directly and retry its normal recovery path.
