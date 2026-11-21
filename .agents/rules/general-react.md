---
description: Apply when building components, hooks, rendering and events, or Next.js App Router surfaces.
alwaysApply: false
paths:
- '**/*.ts'
- '**/*.tsx'
- '**/*.jsx'
---

# General React Conventions

## Components and Props

- **A module exports exactly one component**, with its props type at most, and is named for it. The
  helper components it needs stay in that file, unexported, so no other module can reach them. A
  module exporting two — a navigation shell that also exports a toggle and a menu — is two modules.
- **Components that belong together go in a folder named for their area, one file each**, published
  through the area's index as the TypeScript rules' **Area Imports** describe. The folder holds
  components that each earn their place under the next bullet; it never shelters one that is
  another's variant or a hook's wrapper. A client component's `"use client"` directive goes on the
  first line of its own file.
- **A shared UI library is primitives and the fuller components built from them, and a difference in
  look or behavior is a prop or variant on its owner, never another component.** A primitive is one
  layout, type, surface or control with variants — a stack, a text, a panel, a button — taking
  children but no named slots and opening no portal. A fuller component — a page, a section, a
  dialog, a list, a form — composes primitives and takes slots, as the structure bullet below says.
  A component that renders one other component with some of its look or behavior props fixed or
  defaulted, and adds no content, data or state of its own, is that owner's variant: a
  `DangerNotice` rendering `<Notice tone="danger" dismissible={false}>` is `tone="danger"` on
  `Notice`. One that only runs a hook and renders nothing or its children is that hook, called where
  it is needed, unless it carries the `"use client"` boundary for a Server Component call site. A
  chain of components each adding one prop or value is one component with variants, counted from the
  call site to the primitive at its end. A variant shares its owner's structure; a branch that
  renders a different tree is a second component behind a prop, and becomes that component.
- Named exports for components
- Default exports only for page components

- Destructure props in function signature
- Use optional chaining for optional props
- Provide sensible defaults

```typescript
function Card({ title, action, footer, children, variant = "default" }: CardProps) {
  // ...
}
```

- **A component owns its structure; a call site supplies content.** A surface made of parts — a
  card with a title, an action, a body and a footer — is one exported component that takes them as
  slots (`action={...}`, `footer={...}`, `children`) and owns their spacing, alignment, dividers and
  type sizes through its variants, so each kind of text — a name, a figure, a label — has one size
  across the product. A slot takes the element itself — `action={<Button>…</Button>}`, never
  `actionLabel` and `actionHref` — so each caller keeps its own content without the component
  growing a prop per field. Its parts — a header, a body, a title, an item — are unexported helpers
  in its file: exported compound parts (`Panel`, `PanelHeader`, `PanelBody`), however common in
  component libraries and pattern guides, a third-party skill's compound examples included, are the
  hand-assembly this forbids.
  A call site fills slots; it never assembles the surface from parts or primitives, and structural
  behavior a caller needs becomes a prop or variant. Where a surface is hand-assembled or exports
  its parts, the fix names the one component that replaces it and lists each slot prop it takes.
- **Layout and type come from primitives, never from class strings.** A feature component arranges
  its content with the shared layout and text primitives — a row, a column, a grid, a box, a text, a
  heading — through their variants (`<Flex gap="sm" justify="between">`, `<Type size="sm"
  tone="muted">`), never a `className` spelling out flex, gap, padding, color or type size. A raw
  utility class is allowed only for positioning, animation, an override a third-party component
  needs, or a width on a layout primitive; a button keeps its own, as **Rendering and Events** says.
  A case the primitives cannot express becomes a new variant on the primitive
  that owns it, never a class string at the call site, so one spacing and type scale holds everywhere.
  These allowances belong to the code that builds the UI; an app built on a shared UI library takes
  none of them, as the next bullet says.
- **An app built on a shared UI library writes no styling of its own.** No `className`, no
  class-merging call such as `cn(`, no class string kept in a constant or a style module, no style
  rule or styled component of its own — its stylesheet only loads the library's — and no inline
  `style` except a value read from saved data, such as a column width the reader dragged and saved.
  Each page is a tree of the library's components configured by their props and variants, so every
  page looks standard: a page reads
  `<Section title="Favorites" description="…"><Stack gap="md">…</Stack></Section>`, never a `div`
  spelling out the section's padding and border. A case the library cannot express becomes a prop or
  variant on the shared component that owns it, never a local wrapper, and no shared component takes
  a `className` prop that would let a caller reach around its variants.
- **Responsive layout is the primitive's own CSS.** A primitive changes layout with the room it is
  given through the styling system's container variants, or its responsive variants where the
  viewport decides (`@md:` and `md:` in Tailwind), and a variant value says what it renders at every
  width — never a `cols={3}` whose classes collapse to one column at a breakpoint the caller cannot
  see, as a third-party design-system skill's grid example may. Script that must know the width
  reads the theme's breakpoint through one shared hook; a number restating a breakpoint, color or
  spacing step the theme declares is a second copy of that token.

## Reference Data

- **Reference data comes from a maintained package, never from a list typed into the repository.**
  Countries and their subdivisions, currencies, languages, time zones, dialing codes, bank and card
  networks, MIME types: each is a published standard somebody else already tracks, revises when it
  changes, and ships with types. Reach for the popular, well-maintained package first, and treat
  adding the dependency as the cheaper option, because it is.
- **A short hard-coded list is the failure mode, and it never reads like one.** Eight countries in a
  select looks like a sensible starting point and is in fact a silent limit on who can use the
  screen: the reader whose country is missing cannot finish the form, and nothing reports it. The
  same list then gets copied into the next form that needs it.
- Where a list genuinely has no package — a set this product defines, such as its own plans or
  statuses — it is declared once, in one module, with every consumer importing it. Two copies of one
  list is the defect, whatever the list is of.
- Judge a package on how widely it is used and how recently it was maintained, not on how small it
  is. Weigh the bytes it adds where the data is large and say in the pull request what it costs, but
  never trade completeness away to avoid the download.
- **Completeness is what the dependency buys, so use all of it.** Importing the package and then
  filtering it down to the handful of entries that seemed likely is the hard-coded list again, one
  layer along.

## State and Hooks

- **A custom hook lives in its package's hooks area** — `hooks/`, or the repository's established
  hooks module — never inside a component or feature module, and a shared package exports it only
  once a consumer outside the package calls it.
- Prefix custom hooks with `use`, for example `useResources` or `useViewport`.
- Extract reusable logic into custom hooks

- Local state with `useState` for component-specific state
- Reuse the repository's established shared-state and server-state libraries instead of introducing parallel state layers; in a Next.js App Router repository, server data follows **Rendering and Data** below and takes no client data layer.

- Use `useRef` for DOM access and mutable values
- Don't overuse refs for state that should cause re-renders

- Minimize useEffect usage - prefer derived state
- Always include dependencies
- Clean up subscriptions and timers

- Use `memo()` for expensive pure components
- Use `useMemo` for expensive computations
- Use `useCallback` for stable function references
- Don't over-memoize - profile first

## Rendering and Events

- Prefix with `handle`: `handleClick`, `handleSubmit`
- Use `useCallback` for handlers passed to memoized children
- **Every textual hyperlink has a visible, non-layout-shifting hover effect.** Its resting style
  already signals navigation; hovering changes its color or underline treatment with sufficient
  contrast. The shared link primitive owns that treatment where one exists; otherwise, use the
  product's link tokens consistently across tables, cards, and inline text.
- **Text on a clickable card, row or label stays selectable, and selecting it never activates the
  control.** A drag, double-click or triple-click that selects text leaves the checkbox or option as
  it was; only a plain click toggles it. Disabling selection to avoid the accidental toggle is the
  defect. The shared label component owns this, so every card and row built on it behaves the same.
- **A labeled button in a form, beside a field, or in a form's row of actions reads as a button at
  rest**: a filled surface, or a boundary with at least 3:1 contrast against what it sits on, plus
  a hover state. One that reads as text or a faint outline beside an input is the defect. A control
  may read as text only inside running text — a sentence, a hint, a field's description — where it
  takes the button component's link-style variant when it acts and is a link when it navigates.
  The call site picks a variant that reads as a button; a variant is restyled product-wide only
  where every use of it stands as such an action, and never with a class at one call site, as
  **Components and Props** says of every primitive.
- **A button is as wide as its label and padding, wherever it sits and at any viewport width.** One
  stretched to its row or container — a full-width class, a flex or grid child left to grow, a block
  display — reads as a bar rather than an action and is the defect. The button component keeps its
  own width in any parent, so no call site sets one, and buttons in a group each keep their own
  width; where they sit is the React layout rule's **Layout And Spacing** to say. This holds over general advice to make
  components full width on small screens.
- **A button whose action is running is disabled, marked busy (`aria-busy`), and shows a spinner in
  place of its label at the same width**, so it cannot be pressed twice and nothing beside it moves.
  The label stays in the layout, transparent, holding the width and remaining the accessible name,
  with the spinner overlaid and hidden from assistive technology. The button component owns this
  behind one pending prop; there is no second label prop for the pending state ("Saving…").
  Pending covers only the time the reader waits on the product — preparing a window, saving a
  result. Once a dialog, window or connection flow the button opened is showing, the reader is
  acting rather than waiting, so the button stops spinning, and it spins again only for the work
  that follows when that flow returns.
- **Pressing a send action again moments later shows the same success as the first press.** A
  button that emails, notifies or reminds someone stays enabled once its request finishes, and the
  server sends nothing twice, as the HTTP rule's idempotent message operations say; a countdown, a
  "please wait" refusal or a disabled resend window in its place is the defect.

- Use ternary for simple conditions
- Use early return for complex conditions
- Avoid `&&` with numbers (renders 0)

```typescript
// Good
{count > 0 ? <Badge count={count} /> : null}

// Bad - renders "0" when count is 0
{count && <Badge count={count} />}
```

- Always provide stable `key` prop
- Don't use array index as key (unless list is static)
- Extract list items to separate components when complex

## Next.js App Router

Apply this section only when the repository uses the Next.js App Router.

### Project Structure and Routing

- `page.tsx` - Route pages
- `layout.tsx` - Shared layouts
- `loading.tsx` - Loading UI
- `error.tsx` - Error boundary
- `not-found.tsx` - 404 page, at the app root only; the root layout carries no navigation, so a
  missing page renders outside it, as the full-page message the React layout rule's page-layout bullet keeps for it
- `_components/` - Page-specific components

- Use `Link` from `next/link` for navigation
- Use `useRouter` for programmatic navigation
- Use `redirect()` in Server Components

### Rendering and Data

```typescript
// user-list.tsx - Server Component, no directive
export async function UserList() {
  const users = await fetchUsers(); // Direct DB/API access
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

```typescript
// search-input.tsx - Client Component, directive on the first line
"use client";

export function SearchInput() {
  const [query, setQuery] = useState("");
  return <input value={query} onChange={e => setQuery(e.target.value)} />;
}
```

- **Render on the server.** A page, and every section of it that shows data, is an async Server Component that loads its data and renders it. A Client Component (`"use client"`) exists only for what the browser has to own — event handlers and input, state and effect hooks, browser-only APIs, a dialog, drag-and-drop, a third-party client widget — takes its data as props, and never fetches it.
- **Writes are Server Actions**, and Server Actions authenticate their caller and authorize what they read or change. A write re-renders the page when it finishes. A client-side data layer for reads — SWR, React Query, a fetching hook, a fallback cache seeded from the server — is the shape this replaces, not a companion to it, and a status that has to update live refreshes the server render on an interval instead of fetching on the client. A read that depends on input an open control holds in its own state — a city search as the reader types, a preview of the choices in a dialog — is a read-only Server Action that control calls, never a route handler it fetches; input that belongs in the address, such as a list's filters, stays search params the page renders from.
- **The address carries only state that differs from the page's default.** The first page, an empty search, and the default filter, tab or sort stay out of every link, redirect and router push, so a URL never reads `?page=1` or `?search=`. The helper that builds the address drops a default value itself, so no caller has to remember to.
- **Expected refusals carry a specific, human-readable message the reader can act on**, worded as
  a short, friendly request for the reader's next step that never repeats back what they entered.
  Trace generic copy for a known validation or business refusal to its service and fix that error contract there, rather than inventing replacement client copy. Expected
  refusals must not escape as internal server errors. Genuine 500 responses may keep a safe,
  generic message; diagnose and repair an unexpected 500 encountered during normal operation
  rather than accepting the failure feedback as a finished result. Clearly label failures deliberately
  induced to verify failure presentation so they cannot be mistaken for normal-flow defects.
- **Show the message the API sent.** Never key a table of your own copy off status codes for a first-party API: that is a second copy of its error vocabulary that nothing keeps in step, and it overrides the message the service chose. Wrong copy is fixed at the service that produced it.
- Keep one status-independent fallback for a response that carries no message at all, and reject a body that is a document rather than a message so a proxy's error page cannot reach the user as one.

### Metadata and Assets

Export metadata for SEO:

```typescript
export const metadata = {
  title: "Page title",
  description: "Page description",
};
```

Follow the repository's established image component and optimization policy consistently:

```typescript
<Image src="/logo.png" alt="Logo" width={100} height={50} />
```

### Environment

- `NEXT_PUBLIC_*` - exposed to client
- Other variables - server-only
- Never expose secrets with `NEXT_PUBLIC_` prefix
