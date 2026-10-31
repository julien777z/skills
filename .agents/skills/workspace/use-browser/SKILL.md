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
2. **Reload, never reopen.** When that tab exists and the harness has a tool that controls the
   user's browser, navigate it to the file's address again, which reloads it; a `file://` page does
   not refresh itself when the file changes. Bring it to the front only when the user asked to see
   the change.
3. **Otherwise open it once.** Open `file://<absolute path>` in a new tab with the tool that controls
   the user's browser, selecting the browser as the global rules' **Tools and environments** say,
   and record the tab and the file. When there is no such tool, or it cannot open a `file://`
   address, open the file with the system opener — `open <path>` on macOS, `xdg-open <path>` on
   Linux, `start "" <path>` on Windows — and record that it is open. That tab cannot be reloaded
   from here, so after a later change say in one line that the page changed and needs a reload,
   rather than opening it again.

## Operating A Browser

For the agent's own work in a browser: visiting sites, filling forms, clicking, screenshots,
extracting data, testing and QA, signing in, Electron desktop apps and Slack.

- **Pick the browser by what the work needs.** Use the harness's tool for the user's browser when
  the work needs the user's accounts, sessions or open tabs. Use the `agent-browser` CLI when the
  agent needs a browser of its own, such as for a walkthrough, screenshots or QA. Either way,
  choose and bind to one tab as the global rules' **Tools and environments** say.
- The `agent-browser` CLI drives Chrome or Chromium over the DevTools protocol with
  accessibility-tree snapshots and `@eN` element references. Install it with
  `npm i -g agent-browser && agent-browser install`.
- Before its first command, load its guide from the CLI, which matches the installed version:
  `agent-browser skills get core`, adding `--full` for the command reference. Load a specialized
  guide when the target is not a web page, such as `electron`, `slack` or `dogfood` for exploratory
  testing; `agent-browser skills list` names them all.
- Its observability dashboard runs on port 4848, also reachable through a forwarded address such as
  `https://dashboard.agent-browser.localhost`; stay on that origin, which proxies the sessions.
