# Interface Doctor Pre-Pass

The mechanical commands run before any reviewer reads; read from **Pre-Pass** in `SKILL.md`. A bold section name below is a section of `SKILL.md` or of [the lens criteria](lenses.md).

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
- **Copy searches** — the word lists [the lens criteria](lenses.md) give per lens, run
  over the copy table's text column, never over all source.
- **Source searches** — the patterns below over component source: disclosures and accordions that
  start closed, truncation and clamping, fixed pixel widths, elements hidden by breakpoint, hidden
  scrollbars, raw spacing values, buttons stretched to their container, and autofill attributes.
  The patterns name React and Tailwind spellings and are swapped for the framework's own.
- **Walkthrough** — the rendered pages, captured and measured once, as **Walkthrough** in `SKILL.md` says.

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
