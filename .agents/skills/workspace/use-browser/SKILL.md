---
name: use-browser
description: Show the user a page the agent made, such as a dashboard or report, in their own browser, reusing and reloading the tab it already opened; or drive a browser for the agent's own work with the agent-browser CLI, such as opening a website, filling a form, clicking, taking screenshots, scraping, testing a web app, QA and bug hunts, signing in, or automating Electron apps and Slack. Use whenever a task opens, shows, reloads or controls a browser page.
short_description: 'Show a local page in the user''s browser, or drive a browser for the agent.'
---

# Use Browser

Two jobs share a browser and differ in whose it is. **Showing a local page** puts a file the agent
made in front of the user, in the user's own browser. **Controlling a browser** drives one for the
agent's own work.

## Showing A Local Page

For an HTML file the agent wrote, such as a rendered dashboard, that the user should look at.

1. **Find the tab already showing it.** The task's record of this page, kept wherever the caller
   keeps task state, holds the tab it was opened in and the file it shows. A tab still showing that
   file is the one to use.
2. **Reload, never reopen.** When that tab exists and the harness has a tool that controls the
   user's browser, navigate it to the file's URL again, which reloads it; a `file://` page does not
   refresh itself when the file changes. Bring it to the front only when the user asked to see the
   change.
3. **Otherwise open it once.** Open `file://<absolute path>` in a new tab with the tool that controls
   the user's browser, selecting the browser as the global rules' **Tools and environments** say,
   and record the tab and the file. With no such tool, but the user's own machine running the
   session, open it with the system opener — `open <path>` on macOS, `xdg-open <path>` on Linux,
   `start "" <path>` on Windows — and record that it is open. That tab cannot be reloaded from
   here, so after a later change say in one line that the page changed and needs a reload, rather
   than opening it again.
4. **When the user's browser is out of reach**, such as a cloud session, this route does not apply;
   the caller falls back to sending the file.

## Controlling A Browser

For the agent's own browser work: visiting sites, filling forms, clicking, screenshots, extracting
data, testing and QA, signing in, Electron desktop apps and Slack.

- Choose the browser and bind to one tab as the global rules' **Tools and environments** say,
  whichever tool drives it.
- The `agent-browser` CLI drives Chrome or Chromium over the DevTools protocol with
  accessibility-tree snapshots and `@eN` element references. Install it with
  `npm i -g agent-browser && agent-browser install`.
- Before the first command, load its guide from the CLI, which matches the installed version:
  `agent-browser skills get core`, adding `--full` for the command reference. Load a specialized
  guide when the target is not a web page: `electron`, `slack`, `dogfood` for exploratory testing,
  `derive-client` to record traffic and derive an API client, `vercel-sandbox`,
  `protected-vercel-deployments` and `agentcore`; `agent-browser skills list` names them all.
- Its observability dashboard runs on port 4848, also reachable through a forwarded address such as
  `https://dashboard.agent-browser.localhost`; stay on that origin, which proxies the sessions.
