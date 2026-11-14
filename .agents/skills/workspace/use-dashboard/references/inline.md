# Inline display

How a harness that can show an HTML page inside the conversation shows a dashboard render.

## T3 Code

1. Run `html_preview` with the full page's absolute path and fix any console error or refusal it
   reports before showing the page.
2. Run `html_render` with the same path, a `title` naming the dashboard, and `height` set to the
   largest value the tool accepts; the frame fits the page's content up to that height, and the
   reader can switch pages and open entries inside it.
3. Show every later render the same way, after its re-render, so the conversation holds the current
   page.
