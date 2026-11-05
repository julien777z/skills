# Spaces publishing

Publish the rendered dashboard as an executable visualization in a text Page. Use the existing
dashboard's Page when one is recorded. For a new dashboard, honor a named Page or Space; with no
destination, create a private Page. Keep the dashboard itself in this skill's shared template.

1. Read the active Page tool schemas. Render with `--fragment --compress` and measure the output's
   UTF-8 byte size against the visualization tool's current limit. Compression preserves the
   renderer's page and requires the viewer's `DecompressionStream` API. If the output still exceeds
   the limit, report that concrete publishing failure and continue its repair; do not silently send
   a file or claim publication.
2. Create the Page only when the shared delivery lookup found none to update. Read the selected
   Page and its guidance before inserting a visualization.
3. Pass the rendered HTML to `create_page_visualization`, with `base_sequence` when the read
   provides it. To update, use `replace_block` with the existing visualization's observed block ID
   and hash, preserving the Page and its other content.
4. Inspect the edit receipt and read the Page back. If an error returns an uploaded visualization,
   reconcile that file and the Page before retrying; an uncertain save is read back first. Do not
   create another Page or visualization to escape an uncertain result.
5. Verify the saved visualization reference and inspect the rendered dashboard when browser preview
   is available. Check page navigation and the controls the spec includes. Return the Page link,
   distinguishing saved content from any rendering or interaction that could not be verified.
