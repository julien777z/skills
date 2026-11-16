# Claude Code

Delivery routes when the user reads the session in Claude Code, in the terminal, the desktop app or
on the web, in this order.

1. **An Artifact**, through the session's HTML artifact publishing tool and its current schema.
   Render with `--fragment` when the tool supplies the document skeleton, the full page otherwise,
   and publish it as a plain HTML page so the shared dashboard template remains the page the reader
   sees. Update the artifact the shared lookup in **Delivery** found for this dashboard, searching
   the tool's own listing for a subject that outlives the session; create one only when none
   exists. Follow the tool's icon, description and size requirements. Inspect its save receipt, read
   the saved content when supported, and check the rendered page and its controls when preview is
   available. Return its link and identify any rendering or interaction left unverified.
2. **The user's own browser**, when the artifact tool is absent or refuses the session, such as one
   signed in without a claude.ai account: open the full page through `use-browser`'s **Showing A
   Local Page**, and name the sign-in the refusal asked for in one line, so the user can enable a
   link for the next render.
