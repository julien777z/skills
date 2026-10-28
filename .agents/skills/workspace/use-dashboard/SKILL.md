---
name: use-dashboard
description: Render a dashboard spec into the shared HTML dashboard page and deliver it to the user. Use as a dependency whenever a skill delivers a dashboard page built from its data, so those dashboards share one look and the caller writes data, never HTML.
short_description: 'Turn a dashboard spec into the shared HTML page and deliver it.'
---

# Use Dashboard

A caller describes its dashboard as a JSON spec; [scripts/render.py](scripts/render.py) validates it
and fills [assets/dashboard.html](assets/dashboard.html), with
[assets/diagram.js](assets/diagram.js) inlined, into one page with no build step; its web font loads
from Google Fonts and falls back to system fonts, and a diagram is drawn by Mermaid, loaded from
jsDelivr, with its connections listed as text when Mermaid cannot load. The page is dark unless the
host's viewer is explicitly set to light, lays out wide on a desktop and stacks on a phone, and
renders every value as text, so data never runs as markup or script.

## Spec

Top level: `title`, `updated_at` (ISO 8601) and `pages` are required. The page heading shows
`title`; the page's own name, which a browser tab or a published link shows, is always
`Dashboard - <title>`. Every other field is optional, and an absent one leaves its part of the page
out.

| Field | Shape |
| --- | --- |
| `subtitle` | One line under the title. |
| `status` | `{label, tone?}`: the pill beside the title. |
| `progress` | `{value: 0–1, label, detail?, segments?}`: the large percentage and its bar. `segments` is `[{label, tone?, weight?}]`, one block per unit of work in order, each as wide as its `weight`, a whole number of at least 1, relative to the others, a missing weight counting as 1; without `segments` the bar is a plain fill. |
| `metrics` | `[{label, value, detail?}]`: up to four figures beside the progress. |
| `pages` | `[{title, layout?, sections}]`: with more than one, a tab bar switches between them, and the progress and metrics show on the first. `sections` render in order; with `layout` `columns`, the default, boards, tables and diagrams take the full row and the rest flow into columns, and with `rows` every section takes its own row. |
| `references` | `[{text, url}]`: every whole-word occurrence of `text` in the page's own text becomes a link to `url`. |

`tone` is `good`, `warning`, `critical`, `accent` or `done`, a purple for finished work; omit it
for neutral. Section types:

| `type` | Fields | Item fields |
| --- | --- | --- |
| `board` | `title`, `columns: [{title, tone?, page_size?, items}]` | `title`, `detail?`, `meta?`, `tag?`, `url?` |
| `questions` | `title`, `items`, `page_size?` | `question`, `status` (`open`, `answered`), `context?`, `options?`, `recommendation?`, `answer?`, `meta?` |
| `links` | `title`, `items`, `page_size?` | `label`, `url`, `detail?`, `status?`, `tone?`, `state?`: a pull request's `open`, `draft`, `merged` or `closed`, drawn with GitHub's icon for it in place of the arrow |
| `table` | `title`, `columns`, `rows` | each row a list of strings, one per column |
| `notes` | `title`, `items` | each item a string |
| `changes` | `title`, `items`, `page_size?` | `name`, `change` (`added`, `changed`, `removed`), `detail?`: a named part with its change as a colored badge |
| `outline` | `title`, `groups: [{title, items}]` | `title`, `detail`, `tone?`: a headline that opens to its detail; a group of one or two items shows them open |
| `diagram` | `title`, `nodes`, `edges`, `prs?`, `steps?` | node: `id`, `label`, `detail?`, `pr?`, `change?`; edge: `from`, `to`, `label?`, `step?`, `change?`; pr: `ref`, `url`; each step a string |

A diagram draws each node as a box inside a frame titled with the `ref` its `pr` names, and each
edge as an arrow numbered with its `step`; the numbered `steps` are listed beside or under it.
`change` is `added`, `changed` or `removed` and colors the box or arrow; omit it for an unchanged
part. Every `pr`, `from` and `to` names a listed `ref` or node `id`, and every `step` a position in
`steps`.

A board column, `questions`, `links` or `changes` section with more entries than its `page_size`,
a whole number of at least 1, shows that many at a time, with Previous and Next.

Every text field is a non-empty string; unknown fields are refused, so a typo fails the render
instead of vanishing from the page. `ref`s, node `id`s and reference `text`s are each unique; every
list in the spec holds at least one entry, apart from a board column's cards, so a list with nothing
to show is left out, and so is the entry that requires it. A URL renders as a link only when it is
`http` or `https`.

```json
{
  "title": "Search rewrite",
  "updated_at": "2026-01-05T14:20:00+00:00",
  "status": {"label": "On track", "tone": "good"},
  "progress": {
    "value": 0.5,
    "label": "Overall progress",
    "segments": [{"label": "Index", "tone": "good"}, {"label": "Query"}]
  },
  "metrics": [{"label": "Time remaining", "value": "~20 min"}],
  "pages": [
    {"title": "Progress", "sections": [{"type": "notes", "title": "Notes", "items": ["Index format settled."]}]}
  ]
}
```

## Render

1. Write the spec to a JSON file in private task storage, outside every repository checkout, and
   choose a page path the delivery route below can read, such as the host's scratch directory when
   its publishing tool reads only there.
2. Run `python3 -B scripts/render.py --input <spec.json> --output <page.html>`, resolving `scripts/`
   from this skill's directory; `-B` keeps the run from writing bytecode into the skill. Add
   `--fragment` when the host wraps the page in its own document, as the publishing route below
   says. The script prints the written path, or names the first field
   that does not match the spec and exits non-zero; fix the spec and run it again.
3. Keep the output path stable for one dashboard, so each render replaces the last.

Change a delivered dashboard only by re-rendering its whole spec, never by editing the page's
HTML, which skips the renderer's validation; change the page itself only in this skill's assets.

## Delivery

Use the first route the host offers, and use the same one for every update of one dashboard.

1. **A tool that publishes an HTML page to a link** — Claude's Artifact tool, for example. Render
   with `--fragment`, publish that file as a plain page, never through a page type the host offers
   for dashboards, so every dashboard keeps this template, and give the user the link. Republish
   later renders to that same page so the link stays the one the user already has; record the link
   where the caller keeps task state. Follow the tool's own instructions for its icon and
   description.
2. **A tool that sends a file to the user.** Send the full page.
3. **Neither** — Codex, for example. Give the absolute path to the full page and the command that
   opens it on the user's machine, such as `open <path>` on macOS or `xdg-open <path>` on Linux.

## Guardrails

- A spec carries what the user may see: never a credential, token or secret.
