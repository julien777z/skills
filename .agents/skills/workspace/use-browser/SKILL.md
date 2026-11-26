---
name: use-browser
description: Show the user a page the agent made, such as a dashboard or report, in their browser, reloading its tab in the task group; or operate the user's browser to open websites, fill forms, click, take screenshots, extract data, test web apps, QA and bug hunts, sign in, or automate Electron apps and Slack. Use whenever a task opens, shows, reloads or controls a browser page, before selecting a browser or binding a task tab, and when a browser or app surface reports an inventory or availability error.
short_description: 'Show a local page in the user''s browser, or operate a browser.'
---

# Use Browser

Show a page or operate the user's existing browser through the harness.

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

- Use the harness's browser control to connect to the user's existing browser and the relevant
  profile. This applies to public pages, local previews, debugging, and verification alike.
- Do not launch or attach to a separate Chrome test or debug browser, a headless session, or a
  temporary browser profile. Apply this to browser tools, commands, helper scripts and delegated work.
- If the harness cannot connect to the required browser or profile, report the blocked browser
  step and continue any work that can be verified independently.

## Selecting And Binding A Tab

Bind a tab in the selected browser before reading, navigating or interacting.

- Inventory browser metadata and select the user's existing browser and the relevant profile. An
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
