---
globs:
- '**/*.ts'
- '**/*.tsx'
- '**/*.jsx'
alwaysApply: false
paths:
- '**/*.ts'
- '**/*.tsx'
- '**/*.jsx'
---

# React Conventions

## Components and Props

- One component per file (with co-located helpers)
- Named exports for components
- Default exports only for page components

- Destructure props in function signature
- Use optional chaining for optional props
- Provide sensible defaults
- Do not add one-off structural Tailwind overrides at component call sites. When a structural behavior is reusable, expose it through the component's props or variants; simple width utilities such as `w-full` are the narrow exception.

```typescript
function Card({ title, subtitle = "", className = "" }: CardProps) {
  // ...
}
```

## Reference Data

- **Reference data comes from a maintained package, never from a list typed into the repository.**
  Countries and their subdivisions, currencies, languages, time zones, dialling codes, bank and card
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

## Shared Surfaces

- **A change to a shared mechanism is applied everywhere that mechanism appears, in the same
  change.** A widget grid, a list row, a dialog shell, an edit-mode chrome, an empty state: when a
  design or a fix arrives for one page built on it, the other pages built on it are in scope too.
  Search for every surface that renders the same component or hook before editing, and land the
  change on all of them together. A page left on the old shape is a defect, not a follow-up.
- Never build a second copy of a mechanism beside the one the page already shares. Extend the
  existing component or hook with the new behavior, parameterized where the pages differ, and let
  every consumer pick it up. Two implementations of one mechanism drift the moment either is edited.
- Where a page genuinely cannot take the new shape, say which page and why in the pull request;
  silently leaving it behind is what turns a redesign into an inconsistency.

## Interface Copy

- **Write interface copy in American English**, in spelling and in vocabulary alike: a paper payment
  is a "check" rather than a "cheque", a colour is a "color", and a person "enrolls" rather than
  "enrols". A reader meeting the other spelling reads it as a mistake, and a product that uses both
  reads as two products.

- **Write labels, descriptions and hints for someone who already trusts the product.** Copy that
  warns the reader about their own ordinary action reads as suspicion. A person submitting a record on
  behalf of someone in their own workspace, who has already ticked the box that says they may, does
  not need to be told that the action is logged or attributed to them.
- **Never state what the reader takes for granted.** That data is encrypted, stored securely, kept
  private, or handled carefully is assumed of any product in this category; saying it out loud plants
  the doubt it was meant to settle. Mention a property only where the reader has to act on it or
  where it departs from what they would assume.
- **Keep implementation out of the interface.** Storage, masking, hashing, background jobs, retries
  and the names of internal states belong in the code. A description says what the field is for and
  what the reader should put in it, in the words they would use themselves.
- Say the one thing the reader needs and stop. Prefer no description to a description that repeats
  the label, narrates the obvious, or hedges. Where a sentence is only there to cover the product,
  cut it.

### Confirmation Dialogs

- **A dialog title names the action and is never a question.** "Archive record", "Delete role",
  "Discard draft": the title is what the reader is about to do, stated flatly, so it reads the same
  whether the dialog asks for confirmation or reports a result. "Archive record?" puts the
  question in the one place the reader cannot answer it.
- **The body is where the question is asked, and a confirmation body opens with "Are you sure you
  want to …".** After the question, one sentence on what follows — what the reader loses, what stops
  working, whether it can be undone — and nothing else.
- **The body never opens with the title again.** A title reading "Archive record" over a body
  reading "Archive Ann Lee? …" says the same words twice and spends the only line the reader
  actually reads on the one they have already read. Write the body as though the title is above it,
  because it is.
- Name the record in the title's noun, not the title's value: a dialog headed with one record's
  name is a different heading on every row, and the reader learns nothing from it that the row they
  clicked did not already tell them.
- **An action that cannot be undone is confirmed by typing, not by clicking.** Require the reader to
  type something that identifies what they are acting on — the record's own name — and keep the
  action unavailable until it matches. A button a reader can hit by reflex is not a confirmation.
- One component owns this shape, under **Shared Surfaces** above: dialogs hand-built from the same
  primitives are where these rules get broken one at a time.

## Layout And Spacing

- **Read the padding on every screen the change touches, at every width it is checked at.** Content
  clipped by a header, text against a card's edge, a control overlapping the thing below it, a gap
  that collapses at one breakpoint: each is invisible in the diff and obvious on the screen, and
  each reaches the reader because nobody looked.
- **Chrome positioned over content is the usual cause.** An absolutely positioned header, toolbar or
  footer takes no space, so whatever sits behind it is hidden with nothing in the markup to say so.
  Prefer giving that chrome its own row in a flex or grid column, where the browser reserves the
  space; reach for absolute positioning only where the overlap is the intent.
- A component that renders inside more than one shell — a widget in a canvas and on a page, a card
  in a list and alone — is checked in each one. Spacing that a parent supplies in one place and not
  the other is what a single screenshot cannot settle.

## State and Hooks

- Put reusable custom hooks in the repository's established hooks module.
- Prefix custom hooks with `use`, for example `useResources` or `useViewport`.
- Extract reusable logic into custom hooks

- Local state with `useState` for component-specific state
- Reuse the repository's established shared-state and server-state libraries instead of introducing parallel state layers.

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
- `not-found.tsx` - 404 page
- `_components/` - Page-specific components

- Use `Link` from `next/link` for navigation
- Use `useRouter` for programmatic navigation
- Use `redirect()` in Server Components

### Rendering and Data

Default is Server Component. Use `"use client"` only when needed:
- Event handlers (onClick, onChange, etc.)
- Browser-only APIs (localStorage, window)
- React hooks (useState, useEffect, useContext)
- Third-party client libraries

```typescript
// Server Component (default) - no directive needed
async function UserList() {
  const users = await fetchUsers(); // Direct DB/API access
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}

// Client Component - requires directive
"use client";

function SearchInput() {
  const [query, setQuery] = useState("");
  return <input value={query} onChange={e => setQuery(e.target.value)} />;
}
```

- **Server Components**: Fetch directly in the component
- **Client Components**: Reuse the repository's established client-side data layer and shared fetcher.
- **Mutations**: Reuse the mutation mechanism owned by that data layer.
- **Show the message the API sent.** Never key a table of your own copy off status codes for a first-party API: that is a second copy of its error vocabulary that nothing keeps in step, and it overrides the message the service chose. Wrong copy is fixed at the service that produced it.
- Keep one status-independent fallback for a response that carries no message at all, and reject a body that is a document rather than a message so a proxy's error page cannot reach the user as one.

### Metadata and Assets

Export metadata for SEO:

```typescript
export const metadata = {
  title: "Page Title",
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
