---
name: use-dashboard
description: Render a dashboard spec into the shared HTML dashboard page and deliver it to the user. Use as a dependency whenever a skill delivers a dashboard page built from its data, so those dashboards share one look and the caller writes data, never HTML. Also owns every correction to a dashboard that would hold for any dashboard, such as how it looks, reads, counts or responds.
short_description: 'Turn a dashboard spec into the shared HTML page and deliver it.'
---

# Use Dashboard

A caller describes its dashboard as a JSON spec; [scripts/render.py](scripts/render.py) validates it
and fills the page built from [app/](app/), a React app on Tailwind CSS and stock shadcn/ui
components: a slim sticky navbar of page links, then the dashboard's title, the subtitle and when
it was updated, a row of metric cards, and each section in its own card, all on a near-black
neutral surface. Every dashboard gets that layout
without the caller writing any markup. The page is one self-contained file with its web font bundled
in, and a diagram is drawn by Mermaid, loaded from jsDelivr, with its connections listed as text
when Mermaid cannot load. The page is dark unless the host's viewer is explicitly set to light
(`data-theme="light"` on the root element), and renders every value as text, so data never runs as
markup or script. A dialog opens just below the entry, row or node that opened it, at most 640 px
tall, or less when the frame or window it opens in is shorter, with its contents scrolling; apart
from that cap, nothing on the page is sized by the viewport's height, so it shows whole in a frame
that a harness sizes to its content. Content runs left-aligned up to 72rem wide; the navbar's links
scroll sideways with a visible scrollbar when they do not fit, and below 1024 px they fold into a
menu, with the open page's name beside its button.

**A correction to one dashboard that would hold for any dashboard belongs here**, never in the
skill that built it: how a figure is written, what a chart shows on hover, what is clickable, which
colors mean what, how text reads. The calling skill takes only what concerns its own data, such as
which pages it has, what it counts and what its observations cover. When a correction does both,
split it between the two.

## Dependencies
- `pages:write-page`
- `use-browser`

## Spec

Top level: `title`, `topic`, `icon`, `updated_at` (ISO 8601) and `pages` are required. `title` is
the dashboard's name followed by "Dashboard", such as `Garden Dashboard`; `topic` names what this
render covers in a few words, such as `Bulk export`, and `subtitle` can say more. The navbar shows
a link to each page and the `status` badge; every page opens with `title`
as its heading, then its subtitle and how long ago `updated_at` was. The phone-width page menu shows
`title` beside `icon` and each page's icon beside its name. The page's own name, which a browser tab or a
published artifact shows, is "`title` - `topic`", such as "Garden Dashboard - Bulk export".
Every other field is optional, and an absent one leaves its part of the page out.

| Field | Shape |
| --- | --- |
| `subtitle` | One line under the dashboard's title on the first page only; every other page shows its own `subtitle` or none. |
| `status` | `{label, tone?}`: the badge at the right of the navbar. While any question is `open`, the renderer shows `Waiting on you` in the `warning` tone there and as the `Proposals` page's `status`, and a spec that sets either then is refused. |
| `notice` | `{title, body, tone?}`: a banner with an icon for its tone under every page's heading, for the one thing the reader must see first wherever they are. |
| `progress` | `{value: 0–1, label, detail?, segments?}`: a stat card twice as wide as the others, with the percentage, `detail` as its badge, and a bar. `segments` is `[{label, details?, tone?, weight?}]`, one block per unit of work in order, each as wide as its `weight`, a whole number of at least 1, relative to the others, a missing weight counting as 1, and its `label`, with each of `details` on a line under it, shown in a tooltip while the pointer rests on it; without `segments` the bar is a plain fill. |
| `metrics` | `[{label, value, detail?}]`: at most four stat cards beside the progress, `detail` under the figure. |
| `pages` | `[{title, icon, layout?, subtitle?, status?, progress?, locked?, sections}]`: one navbar link each, a page's `subtitle` under the heading, on the first page in place of the dashboard's, a page's `progress`, in the shape above, shown at its top, with `status` (`{label, tone?}`) shown as a dot in its tone after the page's name, and its label read out to screen readers, for the page's current state, such as something that needs the reader. A `locked` page sets `sections` to `[]` until it has content: its link shows a lock and cannot be opened. The first is always `Overview` with `icon` `overview`, and the progress and metrics show on it. A page titled `Proposals` always has `icon` `proposals` and comes directly after `Overview`, and it is the only page that holds `questions` sections, in tabs and dialogs as well. `sections` render in order; with `layout` `columns`, the default, boards, tables, outlines, trees, tabs, diagrams, figures and timelines take the full row and the rest flow into columns, and with `rows` every section takes its own row. |
| `references` | `[{text, url?, details?}]`, each with exactly one of `url` and `details`: every whole-word occurrence of `text` in any page's text becomes a link to `url`, or opens `details`, one section, in a dialog, apart from the navbar, the page heading, stat card figures, badges, progress segment tooltips and the first cell of a table row that opens a dialog, which stay plain. |

An `icon` is one of `overview`, `proposals`, `progress`, `board`, `checklist`, `list`, `chart`, `activity`,
`compare`, `diagram`, `document`, `guide`, `legal`, `shield`, `people`, `data`, `package`, `release`,
`pull-request`, `settings`, `alert`, `check` or `calendar`. The dashboard's icon and each page's icon
all differ, so no glyph appears twice in the page menu.

`tone` is `good`, `warning`, `critical`, `accent` or `next`, as **Making A Dashboard** defines
them; omit it for neutral. `links` is `[{kind, label, url, state?}]`: pills under the item that open its sources,
each led by its `kind` — `doc`, `code`, `diff`, `spec`, `config`, `test`, `page` or `data`, shown as
Doc, Code, Diff, Spec, Config, Test, Page or Data — and labeled briefly, such as
`terms-of-service.md L324` or `export.py L40–L58`. A `pull-request` link is the pull-request pill
instead: GitHub's icon and color for its `state`, `open` (green), `draft` (gray), `merged` (purple)
or `closed` (red), and its label alone, such as `garden-api#42`, with no kind shown; `state` is
required on it and refused on every other kind. `at` is an ISO 8601
timestamp the page shows in the viewer's own timezone on a 12-hour clock, such as `9:05 PM`, with the
date when it is not today. Every section takes an optional `description`, one sentence shown under
its title, and `counted`, which shows how many items a `table`, `notes`, `links` or `changes`
section holds beside its title. Set it only on a list whose length changes as the work does, such as
the session's pull requests or the findings still open; a fixed list, such as a legend or the steps
of a process, carries no count. Section types:

| `type` | Fields | Item fields |
| --- | --- | --- |
| `board` | `title`, `columns: [{title, tone?, page_size?, items}]` | `title`, `detail?`, `status?`, `meta?`, `tag?`, `url?`, `at?`, `links?`: `status` (`{label, tone?}`) a pill in its tone for what the card's column does not already say, such as Blocked; `tag`, `meta` and `at` share one line of small text, in that order |
| `questions` | `title`, `items`, `page_size?`, `group_label?` | `question`, `status` (`open`, `answered`), `context?`, `options?`, `recommendation?`, `answer?`, `meta?`, `at?`, `group?` |
| `links` | `title`, `items`, `page_size?`, `group_label?` | `label`, `url`, `detail?`, `status?`, `tone?`, `state?`, `group?`: `state` is a pull request's `open`, `draft`, `merged` or `closed`, drawn with the pull-request pill's icon and color for it in place of the arrow; an item with a `state` is labeled with the pull request's `repository#number` alone, such as `garden-api#42`, what it does in a few words in `detail` |
| `table` | `title`, `columns`, `rows`, `details?` | each row a list of strings, one per column, a column whose cells are all short, such as names, kept on one line; `details`, one section per row, makes each row open a dialog holding that section, with its title and description as the dialog's |
| `notes` | `title`, `items` | each item a string |
| `changes` | `title`, `items`, `page_size?`, `group_label?` | `name`, `change` (`added`, `changed`, `removed`), `detail?`, `current?`, `proposed?`, `links?`, `group?`: a named part with its change as a colored badge; `current` and `proposed` say what the part does on each side of the change, each on its own line under the name behind a bold Current or Proposed label, the proposed line after the current one and after `detail`, which holds anything else; an added part sets only `proposed` and a removed part only `current` |
| `outline` | `title`, `groups: [{title, items}]`, `expanded?` (every item starts open when true), `stacked?` (groups run in one column, each across the full width, for groups read in order), `collapsible?` (false shows every item in full with no toggle, its `title` as a muted label beside its `detail`, for a short write-up of facts read top to bottom) | `title`, `detail?`, `current?`, `proposed?`, `tone?`, `tag?`, `meta?`, `links?`, `points?`, with at least one of `detail`, `current` and `proposed`: a headline that opens to its detail, then `current` and `proposed` as a `changes` item shows them, with `points` as a bulleted list under them, with `tone` as the item's dot, `tag` as a neutral badge and `meta` as small text; without `expanded`, a group of one or two items shows them open |
| `tree` | `title`, `items`, `open_depth?` (levels open on load, 1 by default) | `label`, `detail?`, `tag?`, `figure?`, `status?`, `meta?`, `tone?`, `children?`, `details?`: nested entries, each with children opening and closing from a chevron, `tag` a short label that tells otherwise alike entries apart, such as the warehouse each parcel left from, in an outline badge beside its label, `status` (`{label, tone?}`) a pill in its tone after the tag, `figure` a short quantity, such as a count or a duration, in muted right-aligned tabular figures at the end of the row, so every entry's figure lines up with its siblings', `meta` as muted text just before the figure, wrapping within half the row, or under the entry's detail on a phone, siblings' dots and labels lined up whether or not each has children, `tone` alone coloring the entry's dot, whatever `status` holds: without it a leaf's dot is neutral and an entry with children shows none, and `details`, one section, opening in a dialog from the entry's label, which then shows as a link with an open icon; for a whole made of parts made of parts |
| `tabs` | `title`, `tabs: [{label, sections}]` | each tab a `label` and the `sections` it shows: a bar of tab labels, read with the arrow keys as well as the pointer, over the selected tab's sections, which render inside this card in order; a tab whose `sections` is `[]` is left off the bar, and with one tab left no bar shows, only its sections; for one subject split into kinds the reader looks at one at a time |
| `figures` | `title`, `items`, `stacked?` (one figure per row, each followed by its caption, for pictures read in order) | `image`, `alt`, `caption?`: `image` a base64 data URI of an SVG, PNG, JPEG, WebP or GIF image, a single figure taking the card's width and several two side by side on a wide page, or one per row at a readable width with `stacked`, with `alt` read out in its place and `caption` under it; for what the reader needs to see rather than read, such as a map, a mock-up or a screenshot |
| `timeline` | `title`, `lanes: [{label, tag?, tone?, details?, bars}]`, `gaps?: [{start, end, label}]` | bar: `start`, `end`, `tone?`, `label?`, both times ISO 8601 with their UTC offset and `end` no earlier than `start`: a Gantt chart of when work ran in clock time, one row per lane with its label, its `tag` as an outline badge and a dot in its `tone` as a tree leaf's, and each bar placed on one time axis across the card in its `tone`, or neutral without one, the axis ticked in the viewer's local time with the date where the span crosses days; a `gap` is a hatched band across every lane with its label above, such as a pause while a provider throttled requests, drawn as a short break of fixed width whatever its length, so a long pause never squeezes the work around it, with its length in its label; idle time between bars stays empty; resting the pointer on a bar shows its lane, label, start, end and duration; a lane with `details`, one section, opens it in a dialog from its label; lane labels are unique and each lane holds at least one bar; on a narrow screen the chart scrolls sideways inside its card |
| `chart` | `title`, `kind` (`pie`, `bar`), `items`, `total?` | `label`, `value`, `figure`, `detail?`, `tone?`, `details?`: `value` a number of at least 0 that sizes the item's slice or bar, at least one above 0; `figure` the value as the reader reads it, such as `3h 20 min`, shown beside the label with, in a pie, its share of the whole; `detail` a line under it; `tone` colors an item whose meaning is that tone's, such as a late shipment in `warning`; `details`, one section, opens in a dialog when the item's label or its pie slice is clicked; a bar itself is not clickable, since its label beside it already opens the same dialog, for what lies behind that amount, such as the agents or runs it sums. Every untoned item in a pie takes the next series color, distinct hues that are never a gray, taking those close to a tone the chart uses last, and every untoned bar one color, so only a tone stands out. Pointing at an item, or walking a pie's ring with the arrow keys, dims the rest. A pie's slice shows its label, figure and share in a popup, and its label and share in the ring's middle, so a reader reads it off the ring without matching colors; a bar, whose label and figure sit beside it, has no popup. A pie is a ring with `total` in its middle and a legend beside it; bars run one per item scaled to the largest; labels are unique |
| `diagram` | `title`, `nodes`, `edges`, `prs?`, `steps?`, `legend?` (`[{tone, label}]`, a line in each tone beside what it means) | node: `id`, `label`, `detail?`, `pr?`, `change?`, `tone?`, `details?`, `target?`; edge: `from`, `to`, `label?`, `step?`, `change?`, `tone?`, `details?`; pr: `ref`, `url`; each step a string; a drawing is centered in its card when it fits and otherwise scrolls sideways from its left edge, where the flow starts; a download button at the card's top right, shown once the drawing is drawn, saves it as a PNG at twice its full size, scaled down only past the largest canvas a browser draws, named for the dashboard, the page and the section, with the page's fonts, label styles and background baked in |

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
its items. With two or more groups it also shows a select labeled `group_label`, offering All and
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
    },
    {
      "title": "Proposals",
      "icon": "proposals",
      "sections": [
        {
          "type": "questions",
          "title": "Decisions",
          "items": [{"question": "Rank exact title matches first?", "status": "open"}]
        }
      ]
    },
    {
      "title": "Changes",
      "icon": "pull-request",
      "sections": [
        {
          "type": "changes",
          "title": "Changes",
          "items": [
            {
              "name": "Query parser",
              "change": "added",
              "links": [
                {
                  "kind": "pull-request",
                  "label": "garden-api#42",
                  "url": "https://example.com/garden-api/pull/42",
                  "state": "open"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## Making A Dashboard

Dashboards look alike because they are built alike:

- **The page is stock shadcn components on the neutral theme.** The navbar is text links with no
  icons or title, the open one in the foreground over an underline, never a filled background. A
  card is the background's color with a thin border, never a fill, gradient or shadow of its own; a
  section is one such `Card` with its plain title and description in its header and its count a
  muted `Badge` beside the title, and everything inside it flat: no bordered or rounded box within
  a section, its items rows split by thin dividers and a board's columns plain columns. Type and
  spacing are compact, as the app sets them. A diagram's nodes are square boxes with a thin border,
  a name and a small muted detail line. A table is a frameless `Table`, a pill an outline `Badge`
  whose tone shows only as a dot or icon inside it, apart from the pull-request pill, and tabs,
  dialogs, collapsibles, tooltips, separators and the phone-width page menu are `Tabs`, `Dialog`,
  `Collapsible`, `Tooltip`, `Separator` and `Sheet`.
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
- **A page that needs the reader says so in the navbar.** A page other than Proposals holding something the
  reader must act on, such as a review waiting on them, sets its `status` in the `warning` tone, so
  its link carries the yellow dot; a page with nothing for the reader carries none.
- **Pages run in the order the reader's work does.** After Overview and Proposals, pages that help the reader
  understand the work come together, followed by pages for acting on it, such as dispatching the
  week's orders, which come last; a page never sits between two pages of another kind.
- **Icons say what each thing is.** Give the dashboard the icon that best names its subject, such as
  `chart` for sales figures or `legal` for legal documents, and each page the icon for what
  it holds, such as `board` for a board of work or `diagram` for a diagram.
- **Pick the section by the reader's question.** Where is each item? `board`. What needs my answer?
  `questions`. Where do I click? `links`. What does each part say, in a sentence I can open?
  `outline`. What was added or removed? `changes`. Values across the same columns? `table`. Short
  remarks? `notes`. How do the parts connect? `diagram`. What is this made of, part by part — an order and its parcels, a folder and its files? `tree`,
  never a flat table whose rows name their parent.
  One subject in several kinds, read one kind at a time? `tabs`. What does it look like? `figures`.
  When did each piece of work run, and what ran in parallel? `timeline`.
  How is a whole split, or how do amounts compare? `chart`, never a table of numbers the reader has
  to compare by eye; a pie holds the parts of one whole, at most eight, and bars compare the rest.
- **Detail opens in place.** A tree entry's parts are its `children`, opened from its chevron,
  never a dialog; a dialog through `details` holds what is not a part of the entry, such as a
  write-up about it, a table or a diagram.
- **A pill is for a state the reader scans for that nothing else on the entry shows.** A status,
  a mark such as Matches or Out of date, or a pull request's state where no state icon is drawn
  takes a pill — in a tree, the entry's `status` — never words trailing the entry in `meta`; a
  short label that tells otherwise alike entries apart takes a tree entry's `tag`. A longer label
  saying what kind of thing an item is or which group it belongs to, such as its plan or its type,
  is plain text. A pill earns its place by telling items apart: one reading the same on most items
  has stopped meaning anything, and one that only restates the entry's dot, its board column or
  its pull request's state icon, such as Done, Active, Up next or Open, is left out, unless the
  dashboard's own skill keeps one at the user's word. One that tells
  the reader what to look at, such as a Damaged or Held at customs mark, stays, in the `warning` or
  `critical` tone its meaning carries.
- **A piece of work's dot shows where it stands.** A tree entry that stands for work, such as a
  step, a delivery run or a group of them, takes the `tone` of its state — `good` done, `accent`
  active, `critical` blocked, `next` not started — whatever pill it carries, so a delivered parcel
  marked Damaged still has a green dot; a group's state comes from its members, active while any
  runs, blocked while one waits and done once all are finished. Every other tree keeps its tones
  as **Tone means the same everywhere** defines them.
- **Figures line up.** A quantity siblings are compared by, such as a tree entry's `figure`, sits
  right-aligned at the end of its row, never in a badge like a tag, so the reader reads them down a
  column.
- **The dashboard's subtitle shows once**, under the heading on the first page; every other page shows its
  own `subtitle` or none.
- **A figure is a real quantity in a unit the reader knows.** A duration is clock time. Every
  elapsed or estimated time a spec carries, in text as in figures, reads in its two largest units,
  starting from the largest that is not zero, so `2d 7h`, `5h 42 min` and `12 min`, never `55h` or
  `2d 7h 12 min`; a one-letter unit sits against its number and a longer one follows a space. A
  total over work that ran in parallel counts overlapping time once, so no total is longer than the
  clock time it spans. A figure summed over parallel work instead is agent time: its chart's
  `description` says so, and it sets no `total`. A pie's parts never overlap, so its shares add up
  to its whole. A figure never carries a label for how it was computed.
- **Text says what it means where it stands.** A line never sends the reader elsewhere to make
  sense of it, such as "at step 2" or "see above": it says what happens then, such as "after the
  batch is frozen". A numbered title keeps its number; the text about it never leans on one.
- **A label names only what it marks.** A segment, tag, group or row label never restates the
  dashboard's `topic`, the heading above it, or what a pill, tag or figure on the same entry shows:
  the reader already has them, so a progress segment is labeled with its step, such as "Offer
  rules", never "Plot waitlist: Offer rules", an outline group is headed with the area it covers,
  never with the task's name, and an entry tagged with its model is labeled with its role, such as
  "Copy editor", never "Copy editor (Corvid 2.4)".
- **A model is named exactly.** Wherever a dashboard names a model, such as the one an agent ran
  on, it gives the model and its version as the provider names it, such as Corvid 2.4, never the
  family alone, such as Corvid, the raw ID, such as `corvid-2-4`, or the alias a launch passed: read the model the run used
  from its own records, such as the model ID in its transcript, and name one the records do not
  show as unknown rather than guess it from the alias.
- **Labels and headings are written in sentence case and shown as written.** The dashboard's
  `title` and the preview `topic` `Synthetic Preview` are names, in title case.
- **Tone means the same everywhere.** `good`, green, is fine, matches or finished: Done,
  Approved, Passed. `warning` needs the reader's look or action, `critical` is wrong or blocking,
  `accent`, a blue, is running now or informational, such as Running, and `next`, a purple, is up
  next or still to do. A status takes the tone its meaning carries on every dashboard, never a
  color picked for one page. Leave it out for neutral; never tone an item only to decorate it.
- **Assistive tech reads only the page's words.** No element, the page root and navbar included,
  takes style or script text into its accessible name.
- **Blue text is a link.** A reader clicks blue text, so only links take it, and a tone colors a
  dot, border, line or bar, never text. A figure, number or label meant to stand out sits in a
  neutral badge, and a quantity in muted tabular figures, rather than taking a color or the weight its
  neighboring names already use.
- **Text shows the current state and earns its line.** A `description`, subtitle or note says what
  is true now and only what the title and the contents do not, such as which entries a count covers
  or that a figure lacks records for part of its range. A sentence that restates the title,
  describes the section's form, such as "as a list" or "newest first", narrates its controls,
  narrates how the dashboard was built, such as what it leaves out or an instruction it follows, or
  adds a caveat that changes nothing the reader does, such as who will make the final version of
  what it shows, is left out: data that is not there shows its absence by itself.
- **A pull request is named with its repository.** Every label, table cell, title and reference
  names a pull request as `repository#number`, such as `garden-api#42`, never `#number` alone.
- **Sources are links, never paths in text.** Anything a reader can check, such as a file and line,
  a diff, a pull request, a document's section or a page of a site, goes in `links` with a URL that
  opens it at that exact place: a permalink to the line or range at the commit that was read, or the
  pull request's diff for that file. A path or line number written into `detail` or `meta` is not a
  source the reader can open, and a branch, commit, pull request or file a sentence names takes a
  `references` entry so the mention itself is a link.
- **Times are timestamps.** A moment goes in `at` as a timestamp, never as a clock time written into
  text, so every reader sees it in their own timezone.
- **Text is plain.** Titles say what is true in a few words, in the words a reader scans for, such
  as "Opening hours" rather than "When you can visit us"; `detail` explains in a sentence or two
  that reads without the source. Every title, label, caption and description is plain statement,
  never flourish. A file, section or line is named by its `links` pill, never in the
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

1. Write the spec and the page to the task's working-files folder, `.agent_sources/` at the
   root of the task's worktree. A dashboard of a subject that outlives the session keeps its
   spec, its page and anything a later render reuses in a folder of its own under the user's state
   directory (`$XDG_STATE_HOME`, by default `~/.local/state`) instead. Copy the page to the host's
   scratch directory only when the delivery route reads from there alone.
2. Run `python3 -B scripts/render.py --input <spec.json> --output <page.html>`, resolving `scripts/`
   from this skill's directory; `-B` keeps the run from writing bytecode into the skill. Add
   `--fragment` and `--compress` when the harness's delivery route says to. The script prints the written path, or names the first
   field that does not match the spec and exits non-zero; fix the spec and run it again.
   The first render after the app changes builds it with npm into the user cache directory
   (`$XDG_CACHE_HOME/use-dashboard`, or `~/.cache/use-dashboard`), which needs Node.js 20 or newer,
   npm and access to the npm registry, and takes up to a minute; later renders reuse that build. A
   failed build exits non-zero with npm's output.
3. Keep one output path per dashboard, so each render replaces the last and updates the same
   published page or browser tab. A full page also writes `<page>.update.js` beside itself; an
   open local copy checks it every few seconds and shows a new render's data in place, on the same
   page and scroll position, with no reload; only a render from a changed app reloads it.
4. **Look the page over before it reaches the user.** The agent that delivers the dashboard, never a
   subagent, views the rendered page itself, every page and the entries and dialogs that carry its
   content, and judges it as the user will: does each page make sense, is every color, pill and
   label the standard one for what it marks, are names exact and readable, is every elapsed or
   estimated time in the text, as in the figures, written in its two largest units, and does
   anything look wrong, repeated, raw or confusing, such as an internal identifier or file path as a
   label, a name given in both a label and its tag, or a figure that contradicts another. These
   rules list what is already known; the look-over uses judgment for everything else. Fix what it
   finds in the spec or in the caller's data, re-render, and look again. The look-over renders to a
   working copy in the task's working-files folder, never to the delivered output path, whose open
   copy updates in place; only a page with nothing left to fix is rendered to that path.

Change a delivered dashboard only by re-rendering its whole spec, never by editing the page's HTML,
which skips the renderer's validation. Everything the reader can click, a table row or tree entry
that opens a dialog included, shows the pointer cursor. Change the page itself only in `app/`. A new
part of the page uses a stock shadcn component, added with the shadcn CLI (`npx shadcn@latest add
<component>` in `app/`) into `app/src/components/ui/` and kept as the CLI wrote it; custom markup or
CSS is written only for what no shadcn component covers, and goes once a stock component covers it.
The spec is declared once, in `scripts/` (its enums in `models.py`, its shapes in `render.py`), and
`render.py` writes the app's TypeScript types from it into the build. Run `npm ci` once and then
`npm run check` in `app/` to write those types and type-check and lint the app.

## Delivery

A dashboard is rendered and delivered only when the user asks for it, by invoking the skill that
builds it or in words, on an update schedule that skill states itself, or when a workflow the task
runs states a step that shows one. Finished work, a merge, a changed record or an earlier one-time
request to update it never re-renders one on its own.

Every render the user is shown goes out through this section, including a preview, a sample, or a
test of a change to the page: a screenshot of a render is a capture of the page, never its delivery.
Deliver through the routes the **Harness Router** below selects for the harness this session runs
in, in their order, and through the same route for every update of one dashboard within that
harness. A local file or a screenshot does not replace a publishing route the harness's file names.
A dashboard an earlier session delivered through a route this harness does not offer, such as a
published link a session in another harness made, is delivered here through this harness's route,
never held for that route or put to the user as a step; the report says in one line that the earlier
link stays at its last version.

- **One published page per dashboard.** Before publishing, look for the link already published for
  this dashboard's purpose, and publish the update to it when there is one. A dashboard that changes
  its look, its data, or both is still the same dashboard; only a dashboard with a different purpose
  gets a new page. Where that search looks depends on what the dashboard shows, which the caller
  states:
  - **Session work**, such as work in hand this session or a preview, looks only in the caller's
    task state and earlier in this session. A new session publishes a new page and never updates one
    another session published.
  - **A subject that outlives the session**, such as a repository's structure, also looks among the
    user's published pages for one with the same title and topic, through the publishing tool's own
    listing. Before publishing to a page found that way, read it through the tool to confirm this
    session can update it and to build on its current version; when it cannot, publish a new page
    and say why.
- Record each new link or opened local page where the caller keeps task state, so the next render
  finds it.

## Harness Router

The harness is the app the user reads this conversation in, as the session's own description of its
environment names it. Settle it before calling any delivery tool. A host app can run another
harness's agent inside it, as T3 Code runs Claude Code and Codex sessions; the app the user reads
in decides, never the agent runtime or which tools the session happens to list. A session has one
harness, so one file applies.

| Harness | Delivery routes |
| --- | --- |
| T3 Code | [references/harnesses/t3-code.md](references/harnesses/t3-code.md) |
| Claude Code, in the terminal, the desktop app or on the web | [references/harnesses/claude-code.md](references/harnesses/claude-code.md) |
| Codex | [references/harnesses/codex.md](references/harnesses/codex.md) |

**The user's own browser is every harness's last route**: open the full page through `use-browser`'s
**Showing A Local Page**, which refreshes it on every later render. A harness takes it only when
the routes its file lists are unavailable or refuse the session, never beside a route that showed
the page, and a harness no row names takes it alone. Where that route does not apply, send the full
page with a tool that sends a file to the user, or, with none, give its absolute path.

## Guardrails

- A spec carries what the user may see: never a credential, token or secret.
