---
name: use-dashboard
description: Render a dashboard spec into the shared HTML dashboard page and deliver it to the user, a preview, sample or test render of the page included. Use as a dependency whenever a skill delivers a dashboard page built from its data, so the caller writes data, never HTML.
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
as markup or script. Apart from a dialog's height cap, nothing on the page is sized by the
viewport's height, so it shows whole in a frame that a harness sizes to its content.

## Dependencies
- `use-browser`

## Spec

Write the spec as the [spec reference](references/spec.md) describes.

## Making A Dashboard

Dashboards look alike because they are built alike:

- **Overview first, then one page per subject.** Every dashboard opens on `Overview`, the page
  that tells the reader where things stand: the `progress` and `metrics` stat cards, then sections
  that summarize, such as counts per subject
  or one line per theme naming the page that holds it. Overview repeats no item another page lists,
  apart from a summary row that opens an item's full write-up, or a link to it; each later page
  goes deeper on one subject and is named for it.
- **A page serves a stage of the reader's work.** When a request asks for
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
- **Detail opens in place.** A tree entry's parts are its `children`, opened from its chevron,
  never a dialog; a dialog through `details` holds what is not a part of the entry, such as a
  write-up about it, a table or a diagram.
- **A pill is for a state the reader scans for.** A status, a mark such as Matches or Out of date,
  or a pull request's state takes a pill — in a tree, the entry's `status` — never words trailing
  the entry in `meta`; a short label that tells otherwise alike entries apart takes a tree entry's
  `tag`. A longer label saying what kind of thing an item is or which group it belongs to, such as
  its plan or its type, is plain text. A pill
  earns its place by telling items apart: statuses that differ from item to item are worth a pill on
  every one, while a pill reading the same on most items has stopped meaning anything.
- **A figure is a real quantity in a unit the reader knows.** A duration is clock time. A total over
  work that ran in parallel counts overlapping time once, so no total is longer than the clock time
  it spans. A figure never carries a label for how it was computed.
- **Text says what it means where it stands.** A line never sends the reader elsewhere to make
  sense of it, such as "at step 2" or "see above": it says what happens then, such as "after the
  batch is frozen". A numbered title keeps its number; the text about it never leans on one.
- **A label names only what it marks.** A segment, tag, group or row label never restates the
  dashboard's `topic` or the heading above it: the reader already has both, so a progress segment
  is labeled with its step, such as "Offer rules", never "Plot waitlist: Offer rules", and an outline
  group is headed with the area it covers, never with the task's name.
- **Labels and headings are written in sentence case and shown as written.** The dashboard's
  `title` and the preview `topic` `Synthetic Preview` are names, in title case.
- **Tone means the same everywhere.** `good` is fine, matches or finished, `warning` needs the
  reader's look or action, `critical` is wrong or blocking, `accent` is in progress or
  informational, and `done`, a purple, is finished work that must read apart from what is merely
  fine, such as a merged pull request beside open ones. Leave it out for neutral, since a tone on an item that needs no attention dilutes every other tone.
- **Blue text is a link.** A reader clicks blue text, so only links take it, and a tone colors a
  dot, border, line or bar, never text. A figure, number or label meant to stand out sits in a
  neutral badge rather than taking a color or the weight its neighboring names already use.
- **Text shows the current state and earns its line.** A `description`, subtitle or note says what
  is true now and only what the title and the contents do not, such as which entries a count covers
  or that a figure lacks records for part of its range. A sentence that restates the title,
  describes the section's form, such as "as a list" or "newest first", narrates its controls,
  narrates how the dashboard was built, such as what it leaves out or an instruction it follows, or
  adds a caveat that changes nothing the reader does, such as who will make the final version of
  what it shows, is left out: data that is not there shows its absence by itself.
- **A pull request is named with its repository.** Every label, table cell, title and reference
  names a pull request as `repository#number`, such as `garden-api#42`, never `#number` alone.
- **Sources are links.** Anything a reader can check, such as a file and line,
  a diff, a pull request, a document's section or a page of a site, goes in `links` with a URL that
  opens it at that exact place: a permalink to the line or range at the commit that was read, or the
  pull request's diff for that file. A path or line number written into a title, `detail` or `meta` is not a
  source the reader can open, and a branch, commit, pull request or file a sentence names takes a
  `references` entry so the mention itself is a link.
- **Times are timestamps.** A moment goes in `at` as a timestamp, never as a clock time written into
  text, so every reader sees it in their own timezone.
- **Text is plain.** Titles say what is true in a few words, in the words a reader scans for, such
  as "Opening hours" rather than "When you can visit us"; `detail` explains in a sentence or two
  that reads without the source.

## Previews

For a preview, sample or test render, read the [previews reference](references/previews.md) before inventing the scenario.

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
   (`$XDG_CACHE_HOME/use-dashboard`, or `~/.cache/use-dashboard`), which needs the Node.js version the app's dependencies support,
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
to write those types and type-check and lint the app. A change to the spec's enums or shapes
updates the [spec reference](references/spec.md) in the same change, since that reference is a copy callers read.

## Delivery

A dashboard is rendered and delivered only when the user asks for it, by invoking the skill that
builds it or in words, on an update schedule that skill states itself, or when a workflow the task
runs states a step that shows one. Finished work, a merge, a changed record or an earlier one-time
request to update it never re-renders one on its own.

Every render the user is shown goes out through this section, including a preview, a sample, or a
test of a change to the page.
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
