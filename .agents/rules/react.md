---
alwaysApply: false
paths:
- '**/*.ts'
- '**/*.tsx'
- '**/*.jsx'
---

# React Conventions

## Components and Props

- **A module exports exactly one component**, with its props type at most, and is named for it. The
  helper components it needs stay in that file, unexported, so no other module can reach them. A
  module exporting two — a navigation shell that also exports a toggle and a menu — is two modules.
- **Components that belong together go in a folder named for their area, one file each**, published
  through the area's index as the TypeScript rules' **Area Imports** describe. A client component's
  `"use client"` directive goes on the first line of its own file.
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
  component libraries and pattern guides, are the hand-assembly this forbids. A call site fills slots;
  it never assembles the surface from parts or primitives, and structural behavior a caller needs
  becomes a prop or variant. Where a surface is hand-assembled or exports its parts, the fix names
  the one component that replaces it and lists each slot prop it takes.
- **Layout and type come from primitives, never from class strings.** A feature component arranges
  its content with the shared layout and text primitives — a row, a column, a grid, a box, a text, a
  heading — through their variants (`<Flex gap="sm" justify="between">`, `<Type size="sm"
  tone="muted">`), never a `className` spelling out flex, gap, padding, color or type size. A raw
  utility class is allowed only for positioning, animation, an override a third-party component
  needs, or a width on a layout primitive; a button keeps its own, as **Rendering and Events** says.
  A case the primitives cannot express becomes a new variant on the primitive
  that owns it, never a class string at the call site, so one spacing and type scale holds everywhere.

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

- **One shared page section owns initial loading and the content it reveals.** Keep its single
  noninteractive skeleton visible until every request needed for the initially visible heading,
  counts, controls and content resolves. Nested loaders do not reveal successive pieces of that
  page. Keep rendered content during background refresh and pagination, and show an explicit error
  when a required request fails. Move an established section into the shared owner and migrate its
  consumers rather than copying it into a sibling application.

- **A change to a shared mechanism is applied everywhere that mechanism appears, and on every
  sibling surface, in the same change.** A widget grid, a list row, a dialog shell, an edit-mode chrome, an empty state: when a
  design or a fix arrives for one page built on it, the other pages built on it are in scope too.
  Search for every surface that renders the same component or hook before editing, and every
  sibling surface — the variants of one document, the create and edit of one record, the same
  surface built for two audiences — whether or not it renders that component yet, since siblings
  share one structure; land the change on all of them together. A page left on the old shape is a
  defect, not a follow-up.
- **A surface that does for one audience what another already does for a second takes that
  sibling's component, placement, size and controls, differing only in the content each audience
  needs.** A first-run checklist, a status summary or a
  setup step shown to each role, plan or workspace kind is one surface: when one audience's version
  sits in the grid at half width with plain rows, the other's is not a full-width card with its own
  buttons. Read the existing sibling before building the new one, and build on it.
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
- **Name a surface for what it holds, never for the reader's role in it.** A reader knows which side
  of a transaction they are on, so "Payer Accounts", "Payout Methods" or "Your Seller Profile" labels
  them rather than the thing; the heading is "Bank Accounts", "Profile", whatever the surface holds.
  A heading is that name in a word or a short phrase — "Overview", "Contact details" — never a
  sentence or a phrase addressed to the reader, such as "What you can do here" or "Let's get you set
  up".
- **Never state what the reader takes for granted.** That data is encrypted, stored securely, kept
  private, or handled carefully is assumed of any product in this category; saying it out loud plants
  the doubt it was meant to settle. Mention a property only where the reader has to act on it or
  where it departs from what they would assume.
- **Keep implementation out of the interface.** Storage, masking, hashing, background jobs, retries
  and the names of internal states belong in the code. A description says what the field is for and
  what the reader should put in it, in the words they would use themselves.
- **Every section and every step of a flow carries a one-sentence description under its own heading,
  inside its surface** — two on a flow's first step, as **A flow starts at its first question**
  below allows — saying what the reader does there or what the section holds: "Choose how you hear
  about new activity", "The people who can see and edit this project". A heading alone, or a heading
  with only a badge beside it, is the defect. No sentence floats between the page's top bar and its
  first section: a page's name sits where the product puts page titles, and whatever a page-level
  sentence would say belongs to the section it describes.
- Say the one thing the reader needs and stop. On a field, prefer no description to a description
  that repeats the label, narrates the obvious, or hedges, and keep out of any label what the
  product already knows about the reader, such as their own name in a consent checkbox. Where a
  sentence is only there to cover the product, cut it. That includes a paragraph explaining the
  mechanics around an action, such as which party performs which step, and a note of a side effect
  nobody asked about, such as what happens to earlier versions.
- **A status reads from the viewer's side.** Name the state in terms of what that reader did or
  still has to do, and keep internal steps they take no part in behind a visual cue: a person who
  sent a form sees "Submitted", with the tone telling review apart from acceptance, while the
  reviewer sees "Pending review" and "Approved". One status maps to each audience's label in one
  place.

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

- **Text inside an application surface stays within the product's heading scale.** A section,
  card, panel or step title takes the size its component owns, under **Components and Props**
  above; a display-size headline, a hero line or marketing lettering inside an application surface
  outranks the page it sits on and reads as an advertisement. Display type belongs to marketing
  pages outside the application shell.
- **Read the padding on every screen the change touches, at every width it is checked at.** Content
  clipped by a header, text against a card's edge, a control overlapping the thing below it, a gap
  that collapses at one breakpoint: each is invisible in the diff and obvious on the screen, and
  each reaches the reader because nobody looked.
- **Chrome positioned over content is the usual cause.** An absolutely positioned header, toolbar or
  footer takes no space, so whatever sits behind it is hidden with nothing in the markup to say so.
  Prefer giving that chrome its own row in a flex or grid column, where the browser reserves the
  space; reach for absolute positioning only where the overlap is the intent.
- **A surface is as tall as its content, never taller.** A card, panel, section or widget showing a
  large empty area — below its content, or between the content and the control that acts on it —
  reads as unfinished. Content flows from the top and each control sits directly after what it acts
  on, never pushed to the bottom of a stretched container by a fill or a space-between, or to the
  far edge of an otherwise empty row or footer. Surfaces sharing a row split its width evenly,
  unless one is a main area beside a narrow side rail. They end on the same line, and they get there by balancing what they hold — cutting a
  line that earns no place, moving a control, re-pairing the surfaces — never by stretching the
  shorter one; where content cannot be balanced, the shorter keeps its own height. An empty state is
  sized like any other content. Content that can outgrow its surface scrolls inside a
  maximum height, so the surface stays as tall as its content until it reaches the cap. A height set
  from outside the content belongs only to a surface whose content fills the space it is given — a
  chart, a map, media — to one the reader sized, or to a section deliberately sized to the viewport.
- **A frame that scrolls shows its scrollbar whenever its content overflows** — a box of legal
  text, a dialog body, a list or a table inside a maximum height — on every platform and before the
  reader touches it, so cut-off text reads as more to scroll rather than as text that ends. A hidden
  or hover-only scrollbar on such a frame is the defect, including the overlay scrollbar a platform
  hides until scrolling, which the shared scroll component replaces with one it always renders. The
  scroll container is styled once, in that component or the product's base styles, never per call
  site. This holds over general advice to hide scrollbars for a cleaner look.
- **Navigation decides who reaches a page, and the decision that hides a page also refuses to serve
  it.** An address the viewer's role, workspace, plan or permissions never offer them redirects to
  the viewer's home. A screen or empty state telling the viewer the page belongs to somebody else —
  "this page is for …", "switch to … to use it", "you don't have access" — is dead code wherever it
  sits, in a page, a layout or a gate: the check becomes the redirect and the screen is deleted,
  never restyled, moved into a shared message component, or kept because a task lists it among the
  states to restyle.
- **A multi-step flow the reader has finished — a verification, a setup, an onboarding — leaves the
  navigation, and its address redirects to the viewer's home.** A finished flow whose outcome is
  final shows no banner where the reader lands, a toast at most; one whose submission waits on
  someone else's decision — a review, an approval — lands the reader on the product as usual, with
  the banner the banner bullet below describes until the decision lands. A status page standing in
  the flow's place, at its own address or any other, is the defect. A page that a flow finished
  outside the product returns the reader to — a hosted checkout's return address, a provider's
  signing or verification redirect — is that flow's last step and stays.
- **Inside a page, offer only what applies to the reader.** A choice, a document, a field or a
  status row the reader can never use — the other region's version of a document, the other account
  type's settings — is left out, decided by the same rule that decides which one applies, never
  listed beside it. What is left out is the item, never the step or section holding it: a step or
  section stays for every reader who still has something in it to answer, and goes only when
  nothing in it is left. A field whose value the context already fixes — the country on a form only
  one country files, the currency of an account that holds one — is not asked: the value is set, and
  shown as text where the reader should know it.
- **A page's content offers one control per destination or action** — a button, a link, a menu item,
  an icon or a clickable row; the app's own navigation is not counted against it. Two that open the
  same form or page — a checklist step's button or linked label beside a quick link, a row that
  opens its record beside that row's own "View" link, a header action repeated in the section below
  it — read as two different actions and crowd the page. Keep the one control where the reader
  looks for it; elsewhere, text naming the same destination stays plain text, and a control that
  carries nothing else is removed.
- **A flow starts at its first question.** A step that only introduces the product, lists what it
  offers or explains what comes next asks the reader for nothing and is removed. The context a
  first-time reader needs to answer that question — what they are creating and what it holds —
  stays, as one or two plain sentences in the first step's description; removing the step never
  removes the explanation. A flow left with one step is a single page, with no stepper. This holds
  over general onboarding advice to open with a welcome screen or a concept tour.
- **Every step of a multi-step flow renders as a page, in the flow's own chrome, never as a
  dialog.** A dialog is for one action taken from inside a page, however long its form —
  submitting a form outside any flow, submitting on someone's behalf, a quick edit — and one form
  serves the page and the dialog alike, inside each shell.
- **A dialog holds one form.** When the reader chooses between several forms or documents, the
  choice is made on the trigger before the dialog opens — a menu listing each option with a
  one-line description — never as tabs or a switcher inside it. A field the form itself submits,
  such as a type selector, is part of that form and stays inside.
- **A multi-step flow's footer puts "Back", on every step that has one, at its start and the
  forward action at its end, apart; a footer holding only the forward action places it at the start,
  as no control sits alone at the far edge of an empty footer. It labels them by position, never by
  the step's content:** "Next" on every step before the last
  and "Submit" on the last, so the control that goes back never sits beside the one that commits.
  "Save address", "Continue", "Save and continue" or "Create profile" make each step's control look
  like a different action, and the step's heading already says what it holds. This holds for every
  page system that moves through steps — an onboarding, a setup, a verification, a wizard, a form
  split across pages — whether or not each step saves as it advances, and over general advice to
  name a button for its action.
- **Every page renders in the product's page layout, including a page that reports a state** — a
  confirmation, such as the return page a flow finished outside the product lands on, or an expired
  link — with its content in sections, each headed and described as **Interface Copy** says. A
  section carries what the reader needs next — the record the state concerns, its status, the action
  that moves on, in that section's footer. A confirmation also thanks the reader, marks the success,
  and says what they now have and what happens next — never a neutral status panel, nor a
  placeholder for something the reader does not have yet such as "appears here". A label and a
  button centred in an otherwise empty page is the defect, and so is a small card left under chrome
  that no longer applies, such as tabs or a form header. A notice that the page is for somebody
  else, and a status page standing in a finished flow's place, are deleted as the bullets above say.
- **A banner appears only when the reader has something to do, something is wrong, or something
  they submitted is waiting on a decision** — terms to accept, a verification to finish, a load
  that failed, a blocking state to resolve, a submission under review, worded from the reader's
  side as **Interface Copy**'s status bullet says. A success or
  completed state shows none, and a toast at most when the reader's own action just caused it. A
  dismissible "approved" or "done" banner, and whatever stores its dismissal, is the defect: delete
  both.
- **A failure beside working content is a dismissible banner above that content.** It never
  replaces a surface's own heading or description, which keep saying what the surface is while the
  banner says what went wrong.
- A component that renders inside more than one shell — a widget in a canvas and on a page, a card
  in a list and alone — is checked in each one. Spacing that a parent supplies in one place and not
  the other is what a single screenshot cannot settle.

## Forms

- **Disable an action while locally known prerequisites are unmet.** Missing selections or incomplete
  required fields are normal editing state, not an error banner. Show errors for failures after a
  valid action or for failed data requests.

- **A form a person signs, certifies or attests to starts empty.** Nothing is seeded from a profile
  or an earlier submission, because the signer vouches for what they entered.
- **A form longer than a handful of fields is grouped into titled sections,** each holding the
  fields that answer one question; sibling forms share one section layout, under **Shared
  Surfaces** above.
- **Related short fields sit side by side wherever the width allows,** wrapping only when it does
  not.
- **One act gets one confirmation.** A single checkbox, worded as the whole statement the reader is
  making, stands for it; a second box restating part of the first asks twice.
- **Long fixed text a reader must accept — a certification, terms, a disclosure — is set in smaller
  muted type** and scrolls inside a maximum height as Layout And Spacing describes.
- **A placeholder shows a realistic example of the value's format,** such as `555-0100` or
  `2030-01-31`, never zeros, dots or a mask that reads as an existing value hidden from the reader.

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
- **A labelled button in a form, beside a field, or in a form's row of actions reads as a button at
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
  width; where they sit is **Layout And Spacing**'s to say. This holds over general advice to make
  components full width on small screens.
- **A button whose action is running is disabled, marked busy (`aria-busy`), and shows a spinner in
  place of its label at the same width**, so it cannot be pressed twice and nothing beside it moves.
  The label stays in the layout, transparent, holding the width and remaining the accessible name,
  with the spinner overlaid and hidden from assistive technology. The button component owns this
  behind one pending prop; there is no second label prop for the pending state ("Saving…").

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
  missing page renders outside it, still in the product's page layout, with a section linking home
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
- **Writes are Server Actions** that authenticate their caller and re-render the page when they finish. A client-side data layer for reads — SWR, React Query, a fetching hook, a fallback cache seeded from the server — is the shape this replaces, not a companion to it, and a status that has to update live refreshes the server render on an interval instead of fetching on the client.
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
