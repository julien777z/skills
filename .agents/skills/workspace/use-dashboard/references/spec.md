# Dashboard Spec

Contents: the top-level fields, the `icon` and `tone` values, the section types, diagrams, grouping,
validation, and a full example.

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
| `status` | `{label, tone?}`: the badge at the right of the navbar. While any question is `open`, the renderer shows `Waiting on you` in the `warning` tone there and as the `Proposals` page's `status`, and a spec that sets either then is refused. |
| `notice` | `{title, body, tone?}`: a banner with an icon for its tone under every page's title, for the one thing the reader must see first wherever they are. |
| `progress` | `{value: 0–1, label, detail?, segments?}`: a stat card twice as wide as the others, with the percentage, `detail` as its badge, and a bar. `segments` is `[{label, details?, tone?, weight?}]`, one block per unit of work in order, each as wide as its `weight`, a whole number of at least 1, relative to the others, a missing weight counting as 1, and its `label`, with each of `details` on a line under it, shown in a tooltip while the pointer rests on it; without `segments` the bar is a plain fill. |
| `metrics` | `[{label, value, detail?}]`: at most four stat cards beside the progress, `detail` under the figure. |
| `pages` | `[{title, icon, layout?, subtitle?, status?, progress?, locked?, sections}]`: one navbar link each, a page's `subtitle` replacing the dashboard's under its title, a page's `progress`, in the shape above, shown at its top, with `status` (`{label, tone?}`) shown as a dot in its tone after the page's name, and its label read out to screen readers, for the page's current state, such as something that needs the reader. A `locked` page sets `sections` to `[]` until it has content: its link shows a lock in place of its icon and cannot be opened. The first is always `Overview` with `icon` `overview`, and the progress and metrics show on it. A page titled `Proposals` always has `icon` `proposals` and comes directly after `Overview`, and it is the only page that holds `questions` sections, in tabs and dialogs as well. `sections` render in order; with `layout` `columns`, the default, boards, tables, outlines, trees, tabs, diagrams and figures take the full row and the rest flow into columns, and with `rows` every section takes its own row. |
| `references` | `[{text, url?, details?}]`, each with exactly one of `url` and `details`: every whole-word occurrence of `text` in any page's text becomes a link to `url`, or opens `details`, one section, in a dialog, apart from the navbar, page titles, stat card figures, badges, progress segment tooltips and the first cell of a table row that opens a dialog, which stay plain. |

An `icon` is one of `overview`, `proposals`, `progress`, `board`, `checklist`, `list`, `chart`, `activity`,
`compare`, `diagram`, `document`, `guide`, `legal`, `shield`, `people`, `data`, `package`, `release`,
`pull-request`, `settings`, `alert`, `check` or `calendar`. The dashboard's icon and each page's icon
all differ, so no glyph appears twice in the navbar.

`tone` is `good`, `warning`, `critical`, `accent` or `done`, as `SKILL.md`'s **Making A Dashboard**
defines them; omit it for neutral. `links` is `[{kind, label, url, state?}]`: pills under the item that open its sources,
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
| `board` | `title`, `columns: [{title, tone?, page_size?, items}]` | `title`, `detail?`, `status?`, `meta?`, `tag?`, `url?`, `at?`, `links?`: `status` (`{label, tone?}`) the card's state as a pill in its tone; `tag`, `meta` and `at` share one line of small text, in that order |
| `questions` | `title`, `items`, `page_size?`, `group_label?` | `question`, `status` (`open`, `answered`), `context?`, `options?`, `recommendation?`, `answer?`, `meta?`, `at?`, `group?` |
| `links` | `title`, `items`, `page_size?`, `group_label?` | `label`, `url`, `detail?`, `status?`, `tone?`, `state?`, `group?`: `state` is a pull request's `open`, `draft`, `merged` or `closed`, drawn with the pull-request pill's icon and color for it in place of the arrow; an item with a `state` is labeled with the pull request's `repository#number` alone, such as `garden-api#42`, what it does in a few words in `detail` |
| `table` | `title`, `columns`, `rows`, `details?` | each row a list of strings, one per column; `details`, one section per row, makes each row open a dialog holding that section, with its title and description as the dialog's |
| `notes` | `title`, `items` | each item a string |
| `changes` | `title`, `items`, `page_size?`, `group_label?` | `name`, `change` (`added`, `changed`, `removed`), `detail?`, `current?`, `proposed?`, `links?`, `group?`: a named part with its change as a colored badge; `current` and `proposed` say what the part does on each side of the change, each on its own line under the name behind a bold Current or Proposed label, the proposed line after the current one and after `detail`, which holds anything else; an added part sets only `proposed` and a removed part only `current` |
| `outline` | `title`, `groups: [{title, items}]`, `expanded?` (every item starts open when true), `stacked?` (groups run in one column, each across the full width, for groups read in order), `collapsible?` (false shows every item in full with no toggle, its `title` as a muted label beside its `detail`, for a short write-up of facts read top to bottom) | `title`, `detail?`, `current?`, `proposed?`, `tone?`, `tag?`, `meta?`, `links?`, `points?`, with at least one of `detail`, `current` and `proposed`: a headline that opens to its detail, then `current` and `proposed` as a `changes` item shows them, with `points` as a bulleted list under them, with `tag` as a badge in the item's tone (neutral without one) and `meta` as small text; without `expanded`, a group of one or two items shows them open |
| `tree` | `title`, `items`, `open_depth?` (levels open on load, 1 by default) | `label`, `detail?`, `tag?`, `figure?`, `status?`, `meta?`, `tone?`, `children?`, `details?`: nested entries, each with children opening and closing from a chevron, `tag` a short label that tells otherwise alike entries apart, such as the warehouse each parcel left from, in a neutral pill beside its label, `figure` a short quantity, such as a count or a duration, in a neutral badge after that, `status` (`{label, tone?}`) the entry's state as a pill in its tone after the figure, its tone also coloring the entry's dot when the entry sets no `tone`, `meta` beside them, and `details`, one section, opening in a dialog from the entry's label, which then shows as a link with an open icon; for a whole made of parts made of parts |
| `tabs` | `title`, `tabs: [{label, sections}]` | each tab a `label` and the `sections` it shows: a bar of tab labels, read with the arrow keys as well as the pointer, over the selected tab's sections, which render inside this card in order; a tab whose `sections` is `[]` is left off the bar, and with one tab left no bar shows, only its sections; for one subject split into kinds the reader looks at one at a time |
| `figures` | `title`, `items`, `stacked?` (one figure per row, each followed by its caption, for pictures read in order) | `image`, `alt`, `caption?`: `image` a base64 data URI of an SVG, PNG, JPEG, WebP or GIF image, a single figure taking the card's width and several two side by side on a wide page, or one per row at a readable width with `stacked`, with `alt` read out in its place and `caption` under it; for what the reader needs to see rather than read, such as a map, a mock-up or a screenshot |
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
its items. With two or more groups it also shows a select labeled `group_label`, offering All and
each group; choosing a group shows only its items, without the group names above them, and the
count, the questions' summary and the pages follow what is shown.

Every text field is a non-empty string; unknown fields are refused, so a typo fails the render
instead of vanishing from the page. `ref`s, node `id`s and reference `text`s are each unique; every
list in the spec holds at least one entry, apart from a board column's cards, a locked page's `sections` and a tab's `sections`, so a list with nothing
to show is left out, and so is the entry that requires it; a `tabs` section holds at least one tab
with sections, and its tab labels are unique. A URL renders as a link only when it is
`http` or `https`. A spec carries what the user may see, which excludes any credential, token or
secret.

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
