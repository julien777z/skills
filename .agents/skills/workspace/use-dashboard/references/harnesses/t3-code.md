# T3 Code

Delivery when the user reads the session in T3 Code, whichever agent runtime, such as Claude Code or
Codex, runs inside it: **in the conversation**, never beside another route; when that route is
unavailable or refuses the session, the skill's last route applies.

Run `html_preview` with the full page's absolute path and fix any console error or refusal it
reports. Then run `html_render` with the same path, a `title` naming the dashboard, and `height` set
to the largest value the tool accepts; the frame fits the page's content up to that height, and the
reader can switch pages and open entries inside it. Show every later render the same way, after its
re-render, so the conversation holds the current page.

A publishing tool the agent runtime brings into the session, such as Claude's Artifact tool, is used only
when the user asks for a published link.
