---
name: interface-doctor
description: Find and fix what a product's interface gets wrong for its reader, in its text, its forms and its layout. It covers text that changes nothing the reader does, a route to follow where a link belongs, refusals that pass a verdict or repeat input, system internals and exact values shown to end users, headings and dialogs out of shape, one thing under two names, forms that hide or mishandle input, content squeezed, truncated or hidden at a width, surfaces stretched or unevenly spaced, controls outside the product's established positions, banners, toasts and failures in the wrong place, and one component, state or message drawn two ways across pages. Use to audit a whole site's or app's interface copy, forms, layout or consistency, or one of its apps, pages or lenses. Run only when the user asks for it.
short_description: 'Find and fix interface copy, form and layout defects across a product, and pages that draw one thing two ways.'
---

# Interface Doctor

An interface is judged by what its reader meets: the words on the page and the room each value
gets, at every width the product supports. This doctor reads the source for the first and the
rendered pages for the second, and corrects what serves the reader badly.

## Dependencies
- `doctor-protocol`
- `pre-production`
- `run-site`
- `share-media`
- `get-doctors`
- `council`

## Inventory

Run `doctor-protocol`.

Apply the general React rule, the React layout rule, the React copy and forms rule, `pre-production`'s
product-copy reference and the interface rules the repository's own project guidance holds. They
are the rubric; this doctor cites them and never restates them. Their examples are written in
React, and every lens applies to any web interface, read in its framework's terms.

Enumerate, found in the repository at runtime:

- every web app and every shared UI package the audited apps consume, with the app's router: its
  route files or route table, its layouts, and the roles, plans or workspace kinds its navigation
  serves;
- every piece of text an end user reads, wherever it is written: page and component source, message
  catalogs, the messages of an API or tool whose text reaches an end user, the constants and enums
  that hold such text, and email and notification templates;
- every piece of text only the product's own team reads: internal panels, operator and support
  tools, internal API messages;
- every form, dialog, multi-step flow, banner, notice, toast, empty state, loading state and failure
  presentation, each with the shared component that owns its shape, or `none`.

Excluded: generated code and message catalogs produced by a generator, corrected at their source;
vendored components and third-party widgets, another owner's; marketing pages outside the
application shell, for the layout lenses only; test files and fixtures, apart from fixture text that
restates a product message a lens changes, which moves with it; and legal text, whose wording is
its drafter's. An interface no browser renders, such as a native client, is audited by the copy and
form lenses from its source and takes no walkthrough.

**Shared index.** From the index `doctor-protocol`'s **Share The Index** keeps, this doctor reads
the file inventory, symbol table and import table. It writes the copy table, the page list and the component-use table described below.

### Pre-Pass

These are the mechanical steps `doctor-protocol` runs once before any reviewer reads. A hit is a
candidate a reviewer confirms or rejects, never a finding. A tool the repository does not configure
is handled as `doctor-protocol`'s **Measure Before Fan-Out** says.

- **Copy table** — a syntax-tree script kept in the run's working files lists every string an
  interface shows: element text, the string props of shared components (a title, label,
  description, placeholder, hint, accessible name), toast and notification calls, message-catalog
  entries, and server-side messages that reach an end user. Each row holds the text, its file and
  line, its slot — heading, button, tab, menu item, label, description, placeholder, status, banner,
  toast, error, empty state — and its reader: end user or the product's team.
- **Page list** — one row per page the router declares, for each role whose navigation offers it:
  the address, the page file, the layout it renders in, and whether it is a top-level destination,
  a nested page, a flow step or a state page. A dialog a page opens by one action is a row under
  that page.
- **Component-use table** — every shared component with the pages that render it, and every page or
  feature component that builds a dialog, banner, notice, toast, tooltip, empty state, skeleton,
  table row or save control from primitives where a shared component owns that shape.
- **Copy searches** — the word lists [the lens criteria](references/lenses.md) give per lens, run
  over the copy table's text column, never over all source.
- **Source searches** — the patterns below over component source: disclosures and accordions that
  start closed, truncation and clamping, fixed pixel widths, elements hidden by breakpoint, hidden
  scrollbars, raw spacing values, buttons stretched to their container, and autofill attributes.
  The patterns name React and Tailwind spellings and are swapped for the framework's own.
- **Walkthrough** — the rendered pages, captured and measured once, as the next section says.

```sh
rg -n 'defaultOpen=\{false\}|defaultExpanded=\{false\}|defaultCollapsed|collapsed=\{true\}' -g '*.{tsx,jsx}'
rg -n 'truncate|line-clamp-|text-ellipsis|whitespace-nowrap|textOverflow' -g '*.{tsx,jsx,css}'
rg -n '\b(w|min-w|max-w|h)-\[[0-9.]+(px|rem)\]|width: ?[0-9]+px' -g '*.{tsx,jsx,css}'
rg -n '\b(max-)?(sm|md|lg|xl):hidden|\bhidden (sm|md|lg|xl):' -g '*.{tsx,jsx}'
rg -n 'scrollbar-none|scrollbar-hide|scrollbar-width: ?none|::-webkit-scrollbar' -g '*.{tsx,jsx,css}'
rg -n '\b(p|m|gap|space)[xytrbl]?-\[[^\]]+\]|(padding|margin|gap): ?[0-9]' -g '*.{tsx,jsx,css}'
rg -n '<Button[^>]*(w-full|fullWidth|block)' -g '*.{tsx,jsx}'
rg -n 'autoComplete=|autocomplete=' -g '*.{tsx,jsx}'
```

### Walkthrough

Layout shows only on the rendered page, so the pre-pass renders each page once and every reviewer
reads those captures; no reviewer, lens or worker renders a page again. The request for this audit
is the direct request for browser work that `run-site`'s **Principles** names, so the walkthrough
applies in a local and a cloud execution environment alike.

- **The parent runs it as one scripted loop and starts no subagent for it.** It brings the stack up
  as `run-site`'s **Start and verify the stack** says, serving the local production build, reaches
  each state through the repository's scenario command where it has one, as **Scenarios** says, and
  signs in as each role in the page list as **Sign in** says.
- **Rows.** Every row of the page list, each in its loaded default state. A page that renders one
  component for many records is one row, opened on the first record the test data offers. An empty,
  failed or locked state is a row only where a scenario reaches it; otherwise its lenses are judged
  from source. The walk opens pages and dialogs and submits nothing.
- **Widths.** Each page row is captured full-page at every width `run-site`'s **Widths and
  full-page captures** names for a change to layout, the phone width included where the page is
  reachable on one. A dialog row is captured at the smallest desktop width and the phone width.
- **Bound.** One capture per row per width per role, and at most 120 rows a run unless the
  repository's project guidance sets another number. Past the bound, rows are taken in this order —
  top-level destinations, flow steps, nested pages, dialogs — and the rest are recorded unwalked.
- **Measurement rows.** At each capture the loop evaluates one read-only script in the page and
  saves what it lists: whether the document scrolls sideways; each element whose text is clipped,
  ellipsized or clamped; each button label and table cell wrapped past one line; each text present
  at the widest width and not visible at this one; each frame whose content overflows with no
  visible scrollbar; each button as wide as its container; each heading's computed size; the
  distance from the navigation to where the page's content starts; each section's padding and the
  gaps between sections; and the banners, notices and toasts showing, by tone.
- **Records.** Captures go in the worktree's captures folder, in a folder named for the run; the
  measurement rows go beside the pre-pass output; and the pre-pass index lists, per row, each
  capture's path, width, role and measurement file. A reviewer reads each capture of its partition
  whole, region by region, as `share-media`'s **What reaches the user, and when** says, before it
  reads the measurement rows, which narrow nothing.
- **A stack that will not start is repaired at its owner**, as `run-site` says, and the walk then
  runs. Where sign-in cannot complete or the repository holds no app a browser renders, the walk is
  recorded as not run with the reason, the checks that read captures are reported as not run, and
  the lenses fall to what source shows.
- **The second walk** is the pre-pass rerun `doctor-protocol`'s **Run Repository-Native Checks**
  takes on the final head: the same rows, widths and roles, saved beside the first, so each row has
  a before and an after.

### Measures

The counts `doctor-protocol` takes before the audit and again after the fixes: copy-table rows by
reader and slot; hits per copy search and per source search; pages and dialogs in the page list,
walked and unwalked; captures taken; measurement-row instances per check and per width; pages
whose document scrolls sideways, per width; shapes a page builds by hand where a shared component
owns them; and, from the cross-cutting reviewer's tables, things carrying two names and components
drawn two ways. Each count that a fix lens owns reads zero when the run is finished, apart from the
instances a ledger entry retains.

## Lenses

Read [the lens criteria](references/lenses.md) before building the inventory: each lens named here
is a section of that reference, stating the defect shape, the evidence that establishes it, the
checks that find every instance, the remedy, and what is left alone so a reviewer does not go
hunting.

| Lens | Flags | Read from | Reach |
| --- | --- | --- | --- |
| **Idle Text** | Text that changes nothing the reader does or understands. | Copy table | Partition |
| **Routes And Workarounds** | A route to follow where a link belongs, or an instruction that works around the product. | Copy table | Partition |
| **Refusals** | A refusal or failure message that passes a verdict, repeats input, joins several problems or reads as a penalty. | Copy table and the service that words the message | Partition |
| **System Internals** | Exact values, causes and internal names shown to an end user, or team-only text that guesses a cause. | Copy table | Partition |
| **Headings And Descriptions** | A heading, title, description, button label or confirmation dialog out of the shape the copy rules give it. | Copy table, confirmed on captures | Partition |
| **Two Names** | One thing called by two names, two features a reader could mistake, or one capitalization broken. | Copy table across apps | Whole repository |
| **Form Shape** | A form that hides input it needs, picks the wrong control, or saves, confirms or fills in a way the form rules name a defect. | Source searches and source, confirmed on captures | Partition |
| **Squeezed Or Hidden Content** | Content squeezed, truncated, wrapped, clipped or hidden where it should be given room. | Captures and measurement rows, traced to source | Partition |
| **Uneven Surfaces** | Spacing, type scale, frames and heights that differ from the product's own scale or stretch past their content. | Captures and measurement rows, traced to source | Partition; frames and scale are compared across the repository |
| **Control Placement** | A control outside the product's established position, doubled, mislabeled by position, or not reading as what it is. | Captures and source | Partition |
| **Messages And States** | A banner, notice, toast, failure, loading state or state page in the wrong place, weight or tone, or a page that should not exist. | Captures and source | Partition |
| **Drawn Two Ways** | One component, state, message or sibling surface drawn differently on different pages. | Component-use table, measurement rows and captures across pages | Whole repository |

Every finding is recorded in `doctor-protocol`'s finding shape. Its location is the source line that
owns the defect, the shared component where one owns the shape. For a finding read from source its
evidence is the quoted text or code with its copy-table slot. For one read from a capture its
evidence names the capture, its width and role, the region, and the measurement row where one lists
it, beside the source line that produces it. Its proving check is the search or table check
returning nothing for that row, or, for a rendered finding, that row's capture and measurement
reading clean on the second walk, which the parent takes because it needs the running stack.

## Reviewers

Reviewers are capped as `doctor-protocol`'s **Launches** sets; this doctor sets no lower cap, and
the walkthrough and the decision captures under **Dispositions** are the parent's work. The page dictates the partition cut. A partition is one app area: its page files, the components
only those pages render, and their captures. A shared UI package is a partition of its own, audited
with the component-use table rather than captures. Beside the protocol's size bound a partition
holds at most fifteen walked rows, since its reviewer reads every one of their captures.

The cross-cutting reviewer owns **Two Names** and **Drawn Two Ways** and the whole-repository half
of **Uneven Surfaces**, working from the copy table, the component-use table and every measurement
row, and opens a capture or source only to confirm a candidate. It compares the names one thing
carries across apps, roles and messages; one slot's capitalization across the product; one message
worded differently in two places; the content-start distance, heading sizes and section padding of
every page of one kind; each shared shape against the pages that build it by hand; and each surface
serving one audience against its sibling serving another.

The final reviewer that tries to disprove the decisions challenges: each text kept as correct, for
being wrong after all, and each text changed, for being correct text the run only liked less; each
fix that made content fit, for having squeezed, shrunk, truncated or hidden it instead; each
row whose second capture differs from its first with no ledger entry naming that page, which is
reach the plan did not show; each retained truncation, fixed width and hidden element; and each
finding rejected because a rule's example differed from the case in front of it.

## Dispositions

Apply `pre-production` to every correction.

1. **Change boundary.** This doctor changes interface text wherever it is written, component and
   page source, the shared components that own a shape, and the variants and props a fix adds to
   them. It adds no feature, page or flow.
2. **What a rule file names a defect is fixed on every page that has it**, as `pre-production`'s
   **Scope Follows The Defect, Not The Request** says of such a shape and its **Product Choices**
   says of such text. The fix is the remedy the rule states, made at the shared component that owns
   the shape, with every page that builds its own copy moved onto it.
3. **Wrong or inconsistent text is corrected**: a label that states something untrue, one thing
   under two names, a message that does not match what happens, and every text a lens flags. Wrong
   copy for a refusal a service words is fixed at that service, as the general React rule's **Rendering and
   Data** says, with the interface showing what the service sends.
4. **Making content fit is a fix, decided and made at whatever width the defect shows**, by a
   remedy that keeps every value readable, as `pre-production`'s **Product Choices** says of
   content and its space. Squeezing, truncating, shrinking and narrowing are never the remedy.
5. **A routine presentation detail is decided and stated in the report**, as **Product Choices**
   says of one, and a detail the user already decided on a page is followed.
6. **These calls are the run's too**, decided as `doctor-protocol`'s **Gate And Show The Plan**
   decides one, by what serves the reader, through `council` where the run's checks cannot settle
   it, and made in this run:
   - **Removing or hiding content.** Where content cannot get the room its values need at some
     width, which column, field or item goes or is hidden there.
   - **A remedy the run designed whose visible effect is large**: one no rule states, that changes
     the layout, controls or flow on many pages or that a returning reader would notice. The report
     lists every page it changed.
   - **Rewording text that is correct but could read better.**
   - **Which of two names, or of two drawings of one shape, wins** where neither is established,
     most used or the one a rule states.
   - **More than two legitimate non-error banners on one surface**, and **product state no one has
     confirmed**, where copy says a feature is unavailable or coming: the run settles which banners
     stay and what the copy says from what the code and product show.
   - **A departure from a rule that would serve the reader better**: the run proposes the departure
     as the rule change, as `doctor-protocol`'s **Gate And Show The Plan** says.
7. **How a decision is shown.** A decision about layout, controls or hidden content is reported
   with before-and-after captures of a few representative pages where the change shows, never every
   page, the before from the first walk, at the widths where they differ, sent as `share-media`
   says. A wording decision shows the old and new text as text, beside one capture of where it
   sits.
8. **A defect the walk meets that no lens names** — a failed request, an error boundary, a value
   shown wrong — is fixed in this run, as `doctor-protocol`'s **Resolve The Scope** says.
9. **A recurring shape's guard** is the shared component made unable to take it — a description
   prop made mandatory, a width or class prop removed — or a lint rule against the spelling, where
   the repository keeps lint configuration.
10. **A cleanup finding another doctor owns is not fixed here**: a class string or style an app
    writes by hand, a wrapper component, a component's file layout, documentation. The report names
    it with that doctor, found through `get-doctors`. This doctor fixes what the reader sees and
    leaves how the styling is written to its owner.

## Report Additions

- the page list: rows walked and unwalked per app and role, the widths captured, and whether each
  walk ran;
- per lens: copy-table rows and captures judged, findings, and fixes, by app;
- each page a fix visibly changed, as a before-and-after pair at each width where its captures
  differ, directly under that page's line, sent as `share-media` says;
- each text changed, with its old and new wording and its slot, in the detail file;
- each shape moved onto a shared component, with the pages moved and the variant or prop added;
- each routine presentation detail decided, with its reason;
- each decision the run made, with the pages it changed, the file of each capture shown for it
  named inside that entry, never only as a count or a list kept elsewhere, and any council ruling;
- each rule departure made, with its rule change;
- each finding another doctor owns, named with that doctor.
