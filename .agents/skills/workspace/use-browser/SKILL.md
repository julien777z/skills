---
name: use-browser
description: Show the user a page the agent made, such as a dashboard or report, in their browser, or select and operate a browser for websites, forms, screenshots, testing, sign-in and other tasks. Use whenever a task opens, shows, reloads or controls a browser page, before selecting a browser or binding a task tab, and when a browser or app surface reports an inventory or availability error.
short_description: 'Show a local page in the user''s browser, or operate a browser.'
---

# Use Browser

Select a browser for each operation. Honor a browser explicitly named for that operation; if it
lacks the required account session, use its supported sign-in route or report the step blocked.
Otherwise, use the user's browser to show them a page and follow **Operating A Browser** for other
work. A browser named for an inspection does not carry over to a separate preview request.

## Showing A Local Page

For a local page the user should look at, including a served page or an HTML file the agent wrote,
such as a rendered dashboard. A `file://` preview needs the selected browser on the machine that holds
the file; when it is not, such as a cloud session, serve the page to that browser instead.

Open the page in a task tab in the selected browser, bound as below. If a task tab already shows it, reload that
tab. Bring the preview to the front only when the user asks to see it. If the selected browser
cannot load the file, use a local URL served to that browser or report the preview blocker.

## Operating A Browser

In Codex, when the user names Chrome or the task selects their existing Chrome session, use the
bundled Browser plugin's Chrome backend. An `@Chrome` mention selects that backend. Follow
the plugin's setup and Chrome troubleshooting for the selected profile.

If the backend stays unavailable after supported recovery, report the plugin blocker and continue
independent work. Never enable or request Chrome remote debugging, attach a debugger or automation
CLI to Chrome, launch a debug browser, or substitute another browser or backend for that operation.

For operations without an explicit browser, select in this order:
- For a task needing the user's account session, use the harness to connect to the user's existing
  browser and relevant profile.
- Otherwise, for local development and verification, use an isolated `agent-browser` session or an
  isolated browser supplied by the harness. Create a task-owned session without inherited browser
  attachment, profile or saved-state settings. Do not attach to the user's existing browser or
  profile, or fall back to it if neither route is available; report the blocked step and continue
  independent work.
- For other browser work, including a user-reported issue at a non-local URL, use the harness to
  connect to the user's existing browser and relevant profile.

Showing a page to the user follows **Showing A Local Page**; an agent's own inspection of that page
follows the selection above.

## Selecting And Binding A Tab

Bind a tab in the selected browser before reading, navigating or interacting. For an isolated
browser, use its supported tab controls and keep the task's work in its own tab or session. For the
user's browser, follow the steps below.

Treat an inventory or availability error as scoped to the surface it names. A native-app lock or
failure does not block browser automation, and a browser failure does not block terminal or API
work. Before reporting a task blocked by a surface warning, inspect the requested surface directly
and retry its normal recovery path.

- Inventory browser metadata and select the user's existing browser and relevant profile. Leave
  unrelated tabs and groups alone.
- For the bundled Chrome backend, name the session and open a task-owned tab through the plugin.
  If the user explicitly tags an existing tab, follow the plugin's tab-claiming procedure.
- For other routes, create a dedicated task tab group and open task-owned tabs in it, in the
  background when supported.
- Bind each action and observation to the intended tab's stable ID. Verify the binding after
  reconnecting or switching. If tab creation, claiming or binding fails, follow recovery for
  the selected route or report the blocker.
