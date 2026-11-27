---
name: use-browser
description: Show the user a page the agent made, such as a dashboard or report, in their browser, reloading its tab in the task group; or operate the user's browser to open websites, fill forms, click, take screenshots, extract data, test web apps, QA and bug hunts, sign in, or automate Electron apps and Slack. Use whenever a task opens, shows, reloads or controls a browser page, before selecting a browser or binding a task tab, and when a browser or app surface reports an inventory or availability error.
short_description: 'Show a local page in the user''s browser, or operate a browser.'
---

# Use Browser

Select a browser for the task, then show the page or operate it through its supported controls.

## Showing A Local Page

For an HTML file the agent wrote, such as a rendered dashboard, that the user should look at. This
route needs the user's browser on the machine that holds the file, since a `file://` address
resolves there; when it is not, such as a cloud session, this route does not apply.

Open the page in the task group selected below. If a task tab already shows it, reload that
tab. Bring the preview to the front only when the user asks to see it. If the selected browser
cannot load the file, use a local URL served to that browser or report the preview blocker.

## Operating A Browser

For visits, forms, screenshots, testing, sign-in and other browser work, select by purpose:

- For local development and verification, use `agent-browser` or an isolated browser supplied by
  the harness. Do not fall back to the user's personal browser if neither is available; report the
  blocked browser step and continue independent work.
- For a user-reported issue at a non-local URL, sign-in, account work, or another task that uses
  the user's session, use the harness to connect to the user's existing browser and relevant profile.
- Honor an explicitly requested browser. Showing a page to the user follows **Showing A Local Page**;
  an agent's own inspection of that page follows the local verification route above.

## Selecting And Binding A Tab

Bind a tab in the selected browser before reading, navigating or interacting. For an isolated
browser, use its supported tab controls and keep the task's work in its own tab or session. For the
user's browser, follow the steps below.

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
