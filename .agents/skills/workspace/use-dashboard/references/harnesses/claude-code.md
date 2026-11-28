# Claude Code

Delivery when the user reads the session in Claude Code, in the terminal, the desktop app or on the
web: **an Artifact**, through the session's HTML artifact publishing tool and its current schema.
Render with `--fragment` when the tool supplies the document skeleton, the full page otherwise, and
publish it as a plain HTML page so the shared dashboard template remains the page the reader sees.
Update the artifact the shared lookup in **Delivery** found for this dashboard; create one only when
none exists. Follow the tool's icon, description and size requirements. Inspect its save receipt,
read the saved content when supported, and check the rendered page and its controls in the browser
`use-browser` selects, on the full page rendered locally, never on the published link, which only
the user's signed-in account opens. Return its link and identify any rendering or interaction left unverified.

When the artifact tool is absent or refuses the session, such as one signed in without a claude.ai
account, the skill's browser route follows, and the reply names the sign-in the refusal asked for in
one line, so the user can enable a link for the next render.
