# Spaces publishing

Publish the rendered dashboard as an executable visualization in a text Page. Use the existing
dashboard's Page when one is recorded. For a new dashboard, honor a named Page or Space; with no
destination, create a private Page. Keep the dashboard itself in this skill's shared template.

1. Read the active Page tool schemas. Render with `--fragment --compress` and measure the output's
   UTF-8 byte size against the visualization tool's current limit. Compression preserves the
   renderer's page and requires the viewer's `DecompressionStream` API.
2. Create the Page only when the shared delivery lookup found none to update. Read the selected
   Page and its guidance before inserting a visualization.
3. When the HTML fits the visualization tool's limit, pass it to `create_page_visualization`, with
   `base_sequence` when the read provides it. To update, use `replace_block` with the existing
   visualization's observed block ID and hash, preserving the Page and its other content.
   When it exceeds that limit but fits the current `write_page_reference` upload limit, upload the
   rendered HTML file to the selected Page. Confirm `file_access_confirmed` in the receipt and
   compare its byte size and SHA-256 with the rendered file before inserting it. From the returned
   `library-file:<file-id>` or `project-file:<file-id>` reference, use its exact opaque file ID unchanged in
   a standalone `![Title](visualize:<file-id>)` block. Read the Page again and use `edit_page` with
   fresh sequence and block guards to insert or replace that block. If access is unconfirmed or the
   upload outcome is unknown, inspect Files or Library before another upload. If the file exceeds
   the upload limit too, report the publishing failure and continue its repair without trimming data.
4. Inspect the edit receipt and read the Page back. If an error returns an uploaded visualization,
   reconcile that file and the Page before retrying; an uncertain save is read back first. Do not
   create another Page or visualization to escape an uncertain result.
5. Verify the saved visualization reference and, where `read_page_reference` supports its size,
   compare the saved file's byte size and SHA-256 with the rendered file. Inspect the rendered
   dashboard when browser preview is available, checking page navigation and the controls the spec
   includes. Return the Page link, distinguishing saved content from any digest, rendering or
   interaction that could not be verified; reading HTML source does not establish that it rendered.
