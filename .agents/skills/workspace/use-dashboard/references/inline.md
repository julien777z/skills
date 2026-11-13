# Inline display

How a harness that can show an HTML page inside the conversation shows a dashboard render.

## T3 Code

1. Run `html_preview` with the full page's absolute path to read the opening page's
   `contentHeight`; fix any console error or refusal it reports before showing the page.
2. Run `html_render` with the same path and a `title` naming the dashboard. Give it the preview's
   `contentHeight` for a dashboard with one page and no trees, and the tool's height limit for one
   with several pages or a tree, since the reader switches pages and expands entries in the frame.
3. Show every later render the same way, after its re-render, so the conversation holds the current
   page.
