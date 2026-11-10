---
name: use-dashboard
description: Render a dashboard spec into the shared HTML dashboard page and deliver it to the user. Use as a dependency whenever a skill delivers a dashboard page built from its data, so those dashboards share one look and the caller writes data, never HTML.
short_description: 'Turn a dashboard spec into the shared HTML page and deliver it.'
---

# Use Dashboard

A caller describes its dashboard as a JSON spec; [scripts/render.py](scripts/render.py) validates it
and fills the page built from [app/](app/), a React app on Tailwind CSS and shadcn/ui laid out as a
standard shadcn site: a sticky top navbar with the dashboard's icon and title and a link to each
page, the open page's title and subtitle under it, a row of stat cards, and each section in its own
card. Every dashboard gets that layout without the caller writing any markup. The page is one
self-contained file; its web font loads from Google Fonts and falls back to system fonts, and a
diagram is drawn by Mermaid, loaded from jsDelivr, with its connections listed as text when Mermaid
cannot load. The page is dark unless the host's viewer is explicitly set to light
(`data-theme="light"` on the root element), and renders every value as text, so data never runs
as markup or script. The navbar keeps the title whole and the page links beside it: the page spans
up to 1920 px so a wide screen shows more links, the links scroll sideways with a visible scrollbar
when they still do not fit, and they fold into a menu only below 1024 px.

## Dependencies
- `pages:write-page`
- `use-browser`

## Spec

Top level: `title`, `topic`, `icon`, `updated_at` (ISO 8601) and `pages` are required. `title` is
the dashboard's name followed by "Dashboard", such as `Garden Dashboard`; `topic` names what this
render covers in a few words, such as `Bulk export`, and `subtitle` can say more. The navbar shows
`title` beside `icon`, then a link to each page, how long ago `updated_at` was and the `status`
badge, and each page opens with its own title. The page's own name, which a browser tab or a
published artifact shows, is "`title` - `topic`", such as "Garden Dashboard - Bulk export".
Every other field is optional, and an absent one leaves its part of the page out.

| Field | Shape |
| --- | --- |
| `subtitle` | One line under every page's title. |
| `status` | `{label, tone?}`: the badge at the right of the navbar. |
| `notice` | `{title, body, tone?}`: a banner with an icon for its tone under every page's title, for the one thing the reader must see first wherever they are. |
| `progress` | `{value: 0–1, label, detail?, segments?}`: a stat card twice as wide as the others, with the percentage, `detail` as its badge, and a bar. `segments` is `[{label, details?, tone?, weight?}]`, one block per unit of work in order, each as wide as its `weight`, a whole number of at least 1, relative to the others, a missing weight counting as 1, and its `label`, with each of `details` on a line under it, shown in a tooltip while the pointer rests on it; without `segments` the bar is a plain fill. |
| `metrics` | `[{label, value, detail?}]`: at most four stat cards beside the progress, `detail` under the figure. |
| `pages` | `[{title, icon, layout?, subtitle?, status?, progress?, locked?, sections}]`: one navbar link each, a page's `subtitle` replacing the dashboard's under its title, a page's `progress`, in the shape above, shown at its top, with `status` (`{label, tone?}`) shown as a dot in its tone after the page's name, and its label read out to screen readers, for the page's current state, such as something that needs the reader. A `locked` page sets `sections` to `[]` until it has content: its link shows a lock in place of its icon and cannot be opened. The first is always `Overview` with `icon` `overview`, and the progress and metrics show on it. `sections` render in order; with `layout` `columns`, the default, boards, tables, outlines, trees, tabs, diagrams and figures take the full row and the rest flow into columns, and with `rows` every section takes its own row. |
| `references` | `[{text, url?, details?}]`, each with exactly one of `url` and `details`: every whole-word occurrence of `text` in any page's text becomes a link to `url`, or opens `details`, one section, in a dialog, apart from the navbar, page titles, stat card figures, badges, progress segment tooltips and the first cell of a table row that opens a dialog, which stay plain. |

An `icon` is one of `overview`, `progress`, `board`, `checklist`, `list`, `chart`, `activity`,
`compare`, `diagram`, `document`, `guide`, `legal`, `shield`, `people`, `data`, `package`, `release`,
`pull-request`, `settings`, `alert`, `check` or `calendar`. The dashboard's icon and each page's icon
all differ, so no glyph appears twice in the navbar.

`tone` is `good`, `warning`, `critical`, `accent` or `done`, as **Making A Dashboard** defines
them; omit it for neutral. `links` is `[{kind, label, url}]`: pills under the item that open its sources,
each led by its `kind` — `doc`, `code`, `diff`, `spec`, `pull-request`, `config`, `test`, `page` or
`data`, shown as Doc, Code, Diff, Spec, PR, Config, Test, Page or Data — and labelled briefly, such as
`terms-of-service.md L324` or `export.py L40–L58`. `at` is an ISO 8601
timestamp the page shows in the viewer's own timezone on a 12-hour clock, such as `9:05 PM`, with the
date when it is not today. Every section takes an optional `description`, one sentence shown under
its title, and `counted`, which shows how many items a `table`, `notes`, `links` or `changes`
section holds beside its title. Set it only on a list whose length changes as the work does, such as
the session's pull requests or the findings still open; a fixed list, such as a legend or the steps
of a process, carries no count. Section types:

| `type` | Fields | Item fields |
| --- | --- | --- |
| `board` | `title`, `columns: [{title, tone?, page_size?, items}]` | `title`, `detail?`, `meta?`, `tag?`, `url?`, `at?`, `links?`: `tag`, `meta` and `at` share one line of small text, in that order |
| `questions` | `title`, `items`, `page_size?`, `group_label?` | `question`, `status` (`open`, `answered`), `context?`, `options?`, `recommendation?`, `answer?`, `meta?`, `at?`, `group?` |
| `links` | `title`, `items`, `page_size?`, `group_label?` | `label`, `url`, `detail?`, `status?`, `tone?`, `state?`, `group?`: `state` is a pull request's `open`, `draft`, `merged` or `closed`, drawn with GitHub's icon for it in place of the arrow |
| `table` | `title`, `columns`, `rows`, `details?` | each row a list of strings, one per column; `details`, one section per row, makes each row open a dialog holding that section, with its title and description as the dialog's |
| `notes` | `title`, `items` | each item a string |
| `changes` | `title`, `items`, `page_size?`, `group_label?` | `name`, `change` (`added`, `changed`, `removed`), `detail?`, `links?`, `group?`: a named part with its change as a colored badge |
| `outline` | `title`, `groups: [{title, items}]`, `expanded?` (every item starts open when true), `stacked?` (groups run in one column, each across the full width, for groups read in order), `collapsible?` (false shows every item in full with no toggle, its `title` as a muted label beside its `detail`, for a short write-up of facts read top to bottom) | `title`, `detail`, `tone?`, `tag?`, `meta?`, `links?`, `points?`: a headline that opens to its detail, with `points` as a bulleted list under it, with `tag` as a badge in the item's tone (neutral without one) and `meta` as small text; without `expanded`, a group of one or two items shows them open |
| `tree` | `title`, `items`, `open_depth?` (levels open on load, 1 by default) | `label`, `detail?`, `figure?`, `meta?`, `tone?`, `children?`, `details?`: nested entries, each with children opening and closing from a chevron, `figure` a short count in a neutral badge right after its label, `meta` beside it, and `details`, one section, opening in a dialog from the entry's label; for a whole made of parts made of parts |
| `tabs` | `title`, `tabs: [{label, sections}]` | each tab a `label` and the `sections` it shows: a bar of tab labels, read with the arrow keys as well as the pointer, over the selected tab's sections, which render inside this card in order; a tab whose `sections` is `[]` is left off the bar, and with one tab left no bar shows, only its sections; for one subject split into kinds the reader looks at one at a time |
| `figures` | `title`, `items` | `image`, `alt`, `caption?`: `image` a base64 data URI of an SVG, PNG, JPEG, WebP or GIF image, shown at the card's width, two side by side on a wide page, with `alt` read out in its place and `caption` under it; for what the reader needs to see rather than read, such as a map, a mock-up or a screenshot |
| `diagram` | `title`, `nodes`, `edges`, `prs?`, `steps?`, `legend?` (`[{tone, label}]`, a line in each tone beside what it means) | node: `id`, `label`, `detail?`, `pr?`, `change?`, `tone?`, `details?`, `target?`; edge: `from`, `to`, `label?`, `step?`, `change?`, `tone?`, `details?`; pr: `ref`, `url`; each step a string |

A diagram draws each node as a box inside a frame titled with the `ref` its `pr` names, and each
edge as an arrow numbered with its `step`; the numbered `steps` are listed beside or under it.
`change` is `added`, `changed` or `removed` and colors the box or arrow; omit it for an unchanged
part. The diagram shows its own legend, a colored line beside each change it uses, so `legend`
never repeats them. A node's or edge's `tone` colors its border or arrow instead, for a state the
reader follows, such as the step under discussion; `legend` says what each tone means. A node or edge with
`details`, one section, opens it in a dialog when it is clicked. A node's `target` names another
section on the same page, outside tabs, by its title: clicking the node scrolls smoothly to it, and its label
stays plain text rather than a link. Every `pr`, `from` and `to` names a listed `ref` or node `id`, and every `step` a position in
`steps`.

A board column, `questions`, `links` or `changes` section with more entries than its `page_size`,
a whole number of at least 1, shows that many at a time, with Previous and Next.

A `questions`, `links` or `changes` item's `group` names what it belongs to, such as a pull
request's repository as `owner/repo`; when one item sets it, every item and the section's
`group_label`, the name of what the groups are, such as `Repository`, are set too. The section
shows its items group by group, in the order each group first appears, with each group's name above
its items. With two or more groups it also shows a select labelled `group_label`, offering All and
each group; choosing a group shows only its items, without the group names above them, and the
count, the questions' summary and the pages follow what is shown.

Every text field is a non-empty string; unknown fields are refused, so a typo fails the render
instead of vanishing from the page. `ref`s, node `id`s and reference `text`s are each unique; every
list in the spec holds at least one entry, apart from a board column's cards, a locked page's `sections` and a tab's `sections`, so a list with nothing
to show is left out, and so is the entry that requires it; a `tabs` section holds at least one tab
with sections, and its tab labels are unique. A URL renders as a link only when it is
`http` or `https`.

```json
{
  "title": "Garden Dashboard",
  "topic": "Search rewrite",
  "icon": "progress",
  "updated_at": "2026-01-05T14:20:00+00:00",
  "progress": {
    "value": 0.5,
    "label": "Overall progress",
    "segments": [{"label": "Index", "tone": "good"}, {"label": "Query"}]
  },
  "metrics": [{"label": "Time remaining", "value": "~20 min"}],
  "pages": [
    {
      "title": "Overview",
      "icon": "overview",
      "sections": [{"type": "notes", "title": "Notes", "items": ["Index format settled."]}]
    }
  ]
}
```

## Making A Dashboard

Dashboards look alike because they are built alike:

- **Overview first, then one page per subject.** Every dashboard opens on `Overview`, the page
  that tells the reader where things stand: the `progress` and `metrics` stat cards, then sections
  that summarize, such as counts per subject
  or one line per theme naming the page that holds it. Overview repeats no item another page lists,
  apart from a summary row that opens an item's full write-up, or a link to it; each later page
  goes deeper on one subject and is named for it.
- **A page serves a stage of the reader's work, never one narrow artifact.** When a request asks for
  a page about one thing, such as the order parcels leave the warehouse in, find the stage that
  thing belongs to, such as dispatching the week's orders, and build the page for that stage, with
  the requested thing as one section among what the reader needs there. Name the page for the stage.
- **Pages run in the order the reader's work does.** After Overview, pages that help the reader
  understand the work come together, followed by pages for acting on it, such as dispatching the
  week's orders, which come last; a page never sits between two pages of another kind.
- **Icons say what each thing is.** Give the dashboard the icon that best names its subject, such as
  `chart` for sales figures or `legal` for legal documents, and each page the icon for what
  it holds, such as `board` for a board of work or `diagram` for a diagram.
- **Pick the section by the reader's question.** Where is each item? `board`. What needs my answer?
  `questions`. Where do I click? `links`. What does each part say, in a sentence I can open?
  `outline`. What was added or removed? `changes`. Values across the same columns? `table`. Short
  remarks? `notes`. How do the parts connect? `diagram`. What is this made of, part by part? `tree`.
  One subject in several kinds, read one kind at a time? `tabs`. What does it look like? `figures`.
- **A pill is for a state the reader scans for.** A status, a mark such as Matches or Out of date,
  or a pull request's state takes a pill; a label that only says what kind of thing an item is or
  which group it belongs to, such as its plan or its type, is plain text. When most items on a page
  would carry a pill, the pill has stopped meaning anything.
- **Text says what it means where it stands.** A line never sends the reader elsewhere to make
  sense of it, such as "at step 2" or "see above": it says what happens then, such as "after the
  batch is frozen". A numbered title keeps its number; the text about it never leans on one.
- **A label names only what it marks.** A segment, tag, group or row label never restates the
  dashboard's `topic` or the heading above it: the reader already has both, so a progress segment
  is labelled with its step, such as "Offer rules", never "Plot waitlist: Offer rules", and an outline
  group is headed with the area it covers, never with the task's name.
- **Labels and headings are written in sentence case and shown as written.** The dashboard's
  `title` and the preview `topic` `Synthetic Preview` are names, in title case.
- **Tone means the same everywhere.** `good` is fine, matches or finished, `warning` needs the
  reader's look or action, `critical` is wrong or blocking, `accent` is in progress or
  informational, and `done`, a purple, is finished work that must read apart from what is merely
  fine, such as a merged pull request beside open ones. Leave it out for neutral; never tone an item only to decorate it.
- **Blue text is a link.** A reader clicks blue text, so only links take it, and a tone colors a
  dot, border, line or bar, never text. A figure, number or label meant to stand out sits in a
  neutral badge rather than taking a color or the weight its neighbouring names already use.
- **Every section says what it holds.** Give each one a `description`: one sentence on what the
  reader finds or does there, never a narration of its controls.
- **Sources are links, never paths in text.** Anything a reader can check, such as a file and line,
  a diff, a pull request, a document's section or a page of a site, goes in `links` with a URL that
  opens it at that exact place: a permalink to the line or range at the commit that was read, or the
  pull request's diff for that file. A path or line number written into `detail` or `meta` is not a
  source the reader can open, and a branch, commit, pull request or file a sentence names takes a
  `references` entry so the mention itself is a link.
- **Times are timestamps.** A moment goes in `at` as a timestamp, never as a clock time written into
  text, so every reader sees it in their own timezone.
- **Text is plain.** Titles say what is true in a few words; `detail` explains in a sentence or two
  that reads without the source. A file, section or line is named by its `links` pill, never in the
  title, `detail` or `meta`.

## Previews

A preview, sample or test render — showing a caller's layout, a page someone asked for before real
data exists, or a change to the app — runs on one made-up scenario, never on real data.

- **Invent the scenario first**: a fictional product, its repositories, people, pull request numbers,
  environments, settings and dates, then a task that fits them, such as a community garden adding
  a waitlist for its plots. Its domain shares nothing with the user's own projects: not their
  product's kind, its vocabulary, its providers or the problems it solves, so nothing in the preview
  reads as their work.
- **Every value comes from that scenario**: titles, references, links, diffs, checks, questions and
  notes. No real repository, pull request, person, task, setting or address appears, and links point
  at `example.com`.
- **Every page the caller's skill defines is there**, filled, even when the change being previewed
  touches one: a reader judges a page by where it sits among the others, and a preview showing one
  page reads as a dashboard that has only that one.
- **The pages agree with one another**: the same pull requests, counts and names recur on every page,
  and each section fills its slot as the caller's skill describes, so the preview shows what a real
  run of that skill would produce.
- Its `topic` is `Synthetic Preview`, so the page is named such as "Garden Dashboard - Synthetic
  Preview", and the `subtitle` says what made-up task it shows.

## Render

1. Write the spec to a JSON file in private task storage, outside every repository checkout, and
   choose a page path the delivery route below can read, such as the host's scratch directory when
   its publishing tool reads only there.
2. Run `python3 -B scripts/render.py --input <spec.json> --output <page.html>`, resolving `scripts/`
   from this skill's directory; `-B` keeps the run from writing bytecode into the skill. Add
   `--fragment` and `--compress` when **Delivery** says to. The script prints the written path, or names the first
   field that does not match the spec and exits non-zero; fix the spec and run it again.
   The first render after the app changes builds it with npm into the user cache directory
   (`$XDG_CACHE_HOME/use-dashboard`, or `~/.cache/use-dashboard`), which needs Node.js 20 or newer,
   npm and access to the npm registry, and takes up to a minute; later renders reuse that build. A
   failed build exits non-zero with npm's output.
3. Keep one output path per dashboard, so each render replaces the last and updates the same
   published page or browser tab. A full page also writes `<page>.update.js` beside itself; an
   open local copy checks it every few seconds and shows a new render's data in place, on the same
   page and scroll position, with no reload; only a render from a changed app reloads it.

Change a delivered dashboard only by re-rendering its whole spec, never by editing the page's
HTML, which skips the renderer's validation. Everything the reader can click, a table row or tree
entry that opens a dialog included, shows the pointer cursor. Change the page itself only in `app/`: its shadcn
components live in `app/src/components/ui/` and are added with the shadcn CLI. The spec is declared
once, in `scripts/` (its enums in `models.py`, its shapes in `render.py`), and `render.py` writes the
app's TypeScript types from it into the build. Run `npm ci` once and then `npm run check` in `app/`
to write those types and type-check and lint the app.

## Delivery

A dashboard is rendered and delivered only when the user asks for it, by invoking the skill that
builds it or in words, or on an update schedule that skill states itself. Finished work, a merge, a
changed record or an earlier one-time request to update it never re-renders one on its own.

Every render the user is shown goes out through this section, including a preview, a sample, or a
test of a change to the page: a screenshot of a render is a capture of the page, never its delivery.
Use the first route the session offers, and the same one for every update of one dashboard.

1. **A publishing tool**, whenever the harness offers one. In Codex with Pages tools, apply
   `pages:write-page` and follow the [Spaces publishing reference](references/spaces.md). In Claude,
   follow the [Artifacts publishing reference](references/artifacts.md). Both publish this renderer's
   interactive page and return its link. A local file or a screenshot does not replace publication
   when the session offers the publishing route. For another publisher, use its current instructions
   and render with `--fragment` when it supplies the document skeleton, the full page otherwise.
   - **One published page per dashboard.** Before publishing, look for the link already published
     for this dashboard's purpose, and publish the update to it when there is one. A dashboard that
     changes its look, its data, or both is still the same dashboard; only a dashboard with a
     different purpose gets a new page. Where that search looks depends on what the dashboard
     shows, which the caller states:
     - **Session work**, such as work in hand this session or a preview, looks only in the caller's
       task state and earlier in this session. A new session publishes a new page and never updates
       one another session published.
     - **A subject that outlives the session**, such as a repository's structure, also looks among
       the user's published pages for one with the same title and topic, through the tool's own
       listing. Before publishing to a page found that way, read it through the tool to confirm this
       session can update it and to build on its current version; when it cannot, publish a new
       page and say why.
   - Record each new link where the caller keeps task state, so the next render finds it.
2. **The user's own browser, through `use-browser`**, when no such tool exists and its **Showing A
   Local Page** route applies, with the full page; the page refreshes itself on every later render.
3. **Otherwise**, send the full page with a tool that sends a file to the user, or, with none, give
   its absolute path.

## Guardrails

- A spec carries what the user may see: never a credential, token or secret.
