---
name: use-dashboard
description: Render a dashboard spec into the shared HTML dashboard page and deliver it to the user. Use as a dependency whenever a skill delivers a dashboard page built from its data, so those dashboards share one look and the caller writes data, never HTML.
short_description: 'Turn a dashboard spec into the shared HTML page and deliver it.'
---

# Use Dashboard

A caller describes its dashboard as a JSON spec; [scripts/render.py](scripts/render.py) validates it
and fills the page built from [app/](app/), a React app on Tailwind CSS and shadcn/ui laid out
as a standard shadcn site: a sticky top navbar with the title and a link to each page, the open
page's title and subtitle under it, a row of stat cards, and each section in its own card. Every dashboard gets that layout without the
caller writing any markup. The page is one self-contained file; its web font loads from Google
Fonts and falls back to system fonts, and a diagram is drawn by Mermaid, loaded from jsDelivr, with
its connections listed as text when Mermaid cannot load. The page is dark unless the host's viewer
is explicitly set to light (`data-theme="light"` on the root element), folds the page links into a
menu on a phone, and renders every value as text, so data never runs as markup or script.

## Spec

Top level: `title`, `updated_at` (ISO 8601) and `pages` are required. The navbar shows `title`,
how long ago `updated_at` was and the `status` badge, and each page opens with its own title; the page's own
name, which a browser tab or a published link shows, is always `Dashboard - <title>`. Every other
field is optional, and an absent one leaves its part of the page out.

| Field | Shape |
| --- | --- |
| `subtitle` | One line under every page's title. |
| `status` | `{label, tone?}`: the badge at the right of the navbar. |
| `progress` | `{value: 0–1, label, detail?, segments?}`: a stat card twice as wide as the others, with the percentage, `detail` as its badge, and a bar. `segments` is `[{label, tone?, weight?}]`, one block per unit of work in order, each as wide as its `weight`, a whole number of at least 1, relative to the others, a missing weight counting as 1; without `segments` the bar is a plain fill. |
| `metrics` | `[{label, value, detail?}]`: at most four stat cards beside the progress, `detail` under the figure. |
| `pages` | `[{title, icon?, layout?, sections}]`: one navbar link each, the progress and metrics showing on the first. `icon` is one of `overview`, `list`, `chart`, `diagram`, `document`, `shield`, `people`, `data`, `settings`, `alert`, `check` or `calendar`; without it the first page shows `overview` and the rest `document`. `sections` render in order; with `layout` `columns`, the default, callouts, boards, tables, outlines and diagrams take the full row and the rest flow into columns, and with `rows` every section takes its own row. |
| `references` | `[{text, url}]`: every whole-word occurrence of `text` in the page's own text becomes a link to `url`. |

`tone` is `good`, `warning`, `critical`, `accent` or `done`, as **Making A Dashboard** defines
them; omit it for neutral. Section types:

| `type` | Fields | Item fields |
| --- | --- | --- |
| `board` | `title`, `columns: [{title, tone?, page_size?, items}]` | `title`, `detail?`, `meta?`, `tag?`, `url?` |
| `questions` | `title`, `items`, `page_size?` | `question`, `status` (`open`, `answered`), `context?`, `options?`, `recommendation?`, `answer?`, `meta?` |
| `links` | `title`, `items`, `page_size?` | `label`, `url`, `detail?`, `status?`, `tone?`, `state?`: a pull request's `open`, `draft`, `merged` or `closed`, drawn with GitHub's icon for it in place of the arrow |
| `table` | `title`, `columns`, `rows` | each row a list of strings, one per column |
| `notes` | `title`, `items` | each item a string |
| `changes` | `title`, `items`, `page_size?` | `name`, `change` (`added`, `changed`, `removed`), `detail?`: a named part with its change as a colored badge |
| `outline` | `title`, `groups: [{title, items}]` | `title`, `detail`, `tone?`, `tag?`, `meta?`: a headline that opens to its detail, with `tag` as a badge in the item's tone and `meta` as small text such as a source; a group of one or two items shows them open |
| `callout` | `title`, `body`, `tone?` | — : a banner across the page with an icon for its tone, for the one thing the reader must see first |
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

## Making A Dashboard

Dashboards look alike because they are built alike:

- **First page, the answer.** Open on the page that tells the reader where things stand: the
  `progress` and `metrics` stat cards, then a `callout` when one thing needs them now, then the
  detail. Later pages go deeper on one subject each, named for it and given a fitting `icon`.
- **Pick the section by the reader's question.** Where is each item? `board`. What needs my answer?
  `questions`. Where do I click? `links`. What does each part say, in a sentence I can open?
  `outline`. What was added or removed? `changes`. Values across the same columns? `table`. Short
  remarks? `notes`. How do the parts connect? `diagram`.
- **Tone means the same everywhere.** `good` is fine or matches, `warning` needs the reader's look
  or action, `critical` is wrong or blocking, `accent` is in progress or informational, and `done`,
  a purple, is finished work. Leave it out for neutral; never tone an item only to decorate it.
- **Text is plain.** Titles say what is true in a few words; `detail` explains in a sentence or two
  that reads without the source. Name a file, section or line in `meta`, never in the title.

## Render

1. Write the spec to a JSON file in private task storage, outside every repository checkout, and
   choose a page path the delivery route below can read, such as the host's scratch directory when
   its publishing tool reads only there.
2. Run `python3 -B scripts/render.py --input <spec.json> --output <page.html>`, resolving `scripts/`
   from this skill's directory; `-B` keeps the run from writing bytecode into the skill. Add
   `--fragment` when the host wraps the page in its own document, as the publishing route below
   says. The script prints the written path, or names the first field
   that does not match the spec and exits non-zero; fix the spec and run it again.
   The first render after the app changes builds it with npm into the user cache directory
   (`$XDG_CACHE_HOME/use-dashboard`, or `~/.cache/use-dashboard`), which needs Node.js 20 or newer,
   npm and access to the npm registry, and takes up to a minute; later renders reuse that build. A
   failed build exits non-zero with npm's output.
3. Keep one output path per dashboard, so each render replaces the last and republishes to the same
   page.

Change a delivered dashboard only by re-rendering its whole spec, never by editing the page's
HTML, which skips the renderer's validation. Change the page itself only in `app/`: its shadcn
components live in `app/src/components/ui/` and are added with the shadcn CLI. The spec is declared
once, in `scripts/render.py`, which writes the app's TypeScript types from it into the build. Run
`npm ci` once and then `npm run check` in `app/` to write those types and type-check and lint the
app.

## Delivery

Every render the user is shown goes out through this section, including a preview, a sample, or a
test of a change to the page: a screenshot of a render is a capture of the page, never its delivery.
Use the first route the host offers, and the same one for every update of one dashboard.

1. **A tool that publishes an HTML page to a link**, such as Claude's Artifact tool, whenever the
   host offers one. Render with `--fragment` and publish that file as a plain page, never through a
   page type the host offers for dashboards, so every dashboard keeps this template. Follow the
   tool's own instructions for its icon and description, and give the user the link.
   - **One artifact per dashboard.** Before publishing, look for the link already published for
     this dashboard's purpose, in the caller's task state or earlier in the session. When there is
     one, republish to it: the same file path within the session, or the link itself from another
     one. A dashboard that changes its look, its data, or both is still the same dashboard; only a
     dashboard with a different purpose gets a new artifact.
   - Record each new link where the caller keeps task state, so the next render finds it.
2. **A tool that sends a file to the user.** Send the full page.
3. **Neither** — Codex, for example. Give the absolute path to the full page and the command that
   opens it on the user's machine, such as `open <path>` on macOS or `xdg-open <path>` on Linux.

## Guardrails

- A spec carries what the user may see: never a credential, token or secret.
