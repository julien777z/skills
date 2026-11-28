---
description: Apply when building or changing shared surfaces, page layouts, spacing, or responsive behavior in React.
alwaysApply: false
paths:
- '**/*.ts'
- '**/*.tsx'
- '**/*.jsx'
---

# React Layout Conventions

## Shared Surfaces

- **Verify shared controls in the rendered surface at every supported responsive mode.** Check
  each visible control's purpose, count, accessibility and behavior, including the computed styles
  that make alternative controls mutually exclusive. A DOM assertion or a capture of one intended
  change does not establish that the surrounding controls work; inspect the whole changed surface
  before accepting it, and fix duplicated or incorrectly visible controls at their shared owner.

- **Find the established owner before building a repeated surface.** When the same page section,
  navigation element, menu, input, loading state or action appears elsewhere, move the established
  implementation into a generic shared primitive. A local component built on the shared primitive
  supplies content — its own data and copy — and picks a documented variant at the call site; it
  never fixes a variant under a second name, as the general React rule's **Components and Props** says, and never recreates
  structure, styling, fetching or interaction behavior. An interface
  that is correct in one consumer is the canonical starting point for the extraction, not a visual
  reference to copy.

- **One shared page section owns initial loading and the content it reveals.** Its single
  noninteractive skeleton stays visible until every request needed for the initially visible
  heading, counts, controls and content resolves; a consumer cannot add a second loader or reveal
  structural content afterward. A settled result includes populated content, an empty result, and
  an initial error. Keep that view, its controls, and its layout mounted while automatic refresh,
  revalidation, pagination, or a retry is pending; update it when the result actually changes,
  including the whole-page failure presentation below when the page's subject becomes unavailable. A request
  becoming pending again never makes a settled view an initial load, and absent data alone cannot
  distinguish a first load from a retry after failure. Present a required request's error through
  the failure owner below, retaining undismissed feedback during retries rather than alternating it
  with a skeleton or empty state. Background retries never redisplay the same dismissed failure or
  reopen its dismissed surface; present a materially changed failure as a new result through that
  owner. Background activity alone never replaces content, pulses the page,
  changes action labels, or disables unrelated controls; preserve automatic refresh instead of
  stopping it to hide flicker. These settled-view requirements apply to every data-dependent
  component, including one outside a shared page section.
  Validate each affected component through a cold load and repeated slow refreshes of populated, empty,
  and failed results, including recovery after an initial failure and dismissal followed by the same
  and a changed failure. The cold load changes directly from one complete skeleton to the settled
  section or the failure presentation below; later requests
  keep the settled structure and undismissed feedback visible while pending and apply only the new result.
- **Load available tabs, disclosures, and row actions with the page.** Start authorized display
  reads on page entry as soon as their prerequisites are met, including for inactive tabs and
  shared or inexpensive data needed by their row actions. Use the navigation rule below for
  costly per-row reads. Give initially visible data priority and defer reads that would compete
  with it until they can run without delaying it. Reuse the loaded results when
  the reader opens or switches sections. If the action opens another window or frame, deliver the
  loaded data to that destination; a warm cache in the opener alone does not count. Verify from
  page entry through opening the action. When there are tabs, start on a different tab; when
  there is a separate destination cache, start it empty.
- **A page states that something is missing only once its request has said so.** "Not found", an
  empty list or a "nothing here yet" state shows after the request answers with that result, such
  as a 404 or an empty page of results. Before the first request settles, the skeleton is all the
  reader sees; data not arrived yet is never read as data that does not exist. Afterward, the
  settled-view rule above governs background requests and retries.
- **A click that navigates shows the destination at once, finished where the data could be loaded
  ahead.** Load a destination's data before the click whenever the reader signals where they are
  going: a pointer resting on a row or link, keyboard focus on it, or a link in view whose
  destination is cheap to load. Where each destination costs several requests, as a detail page
  opened from a list does, load it on that signal for the one row in question, never for every row
  on screen. The skeleton is the fallback for data that has not arrived by the click: once a
  short pending delay of about 200 ms passes without the destination arriving, its frame and
  skeleton replace the current page, so a destination loaded ahead never flashes a skeleton and
  the old page never stays on screen past that delay while the next one's requests run. Each
  route segment that waits on data owns its own loading boundary, so the fallback shows wherever
  the navigation diverges, and the destination starts its independent requests together rather
  than one after another. Validate it by timing a click to content after resting on the row, and a
  cold click to the skeleton and to the content, against a deliberately slowed backend.

- **A change to a shared mechanism is applied everywhere that mechanism appears, and on every
  sibling surface, in the same change.** A widget grid, a list row, a dialog shell, an edit-mode
  chrome, an empty state: when a fix arrives for one page built on it, the other pages built on it
  are in scope too. A correction the user makes to how one page looks or reads reaches other pages
  when the user makes it a rule or gives a reason that holds wherever the shape appears, and stays
  on that page otherwise.
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
- **A recurring interaction follows the product's established flow.** Before placing controls for
  selecting, changing or removing related items, inspect comparable screens for where the list,
  action and editing surface live. Keep the same division between viewing and editing unless the
  new task needs a different one; changing labels alone is not a reason to bury the interaction in
  an unrelated section or invent another control shape.
- Where a page genuinely cannot take the new shape, say which page and why in the pull request;
  silently leaving it behind is what turns a redesign into an inconsistency.

## Layout And Spacing

- **Text inside an application surface stays within the product's heading scale.** A section,
  card, panel or step title takes the size its component owns, under the general React rule's **Components and
  Props**; a display-size headline, a hero line or marketing lettering inside an application surface
  outranks the page it sits on and reads as an advertisement. Display type belongs to marketing
  pages outside the application shell.
- **Read the padding on every screen the change touches, at every width it is checked at.** Content
  clipped by a header, text against a card's edge, a control overlapping the thing below it, a gap
  that collapses at one breakpoint: each is invisible in the diff and obvious on the screen, and
  each reaches the reader because nobody looked. Compare neighboring banners and sections as well:
  their content insets and the gaps between them must follow the same shared spacing scale. Fix
  inconsistent padding or gaps in the owning component rather than adding page-specific overrides.
- **Chrome positioned over content is the usual cause.** An absolutely positioned header, toolbar or
  footer takes no space, so whatever sits behind it is hidden with nothing in the markup to say so.
  Prefer giving that chrome its own row in a flex or grid column, where the browser reserves the
  space; reach for absolute positioning only where the overlap is the intent.
  Sticky headings must leave the content beneath them readable at every scroll position.
- **Align paired comparison values by field.** Place each editable value on the same row as the
  corresponding read-only value where they appear side by side.
- **A page takes the content frame of its kind, and every page of that kind takes the same one.**
  The product's page layout has few frames, each set once in a layout component — commonly a
  centered column for a page the reader passes through to finish one task and then leaves, such as a
  step of a multi-step flow, a standalone form outside the navigation or a confirmation, and the
  full-width frame for a page reached from the navigation, whatever it holds. A page never sets its
  own width, centering or outer padding. Two pages of one kind whose content starts at different
  distances from the navigation read as two products.
- **A surface is as tall as its content, never taller.** A card, panel, section or widget showing a
  large empty area — below its content, or between the content and the control that acts on it —
  reads as unfinished. Content flows from the top; artificial filler never pushes a control to the
  bottom of a stretched container or the far edge of an otherwise empty row or footer. Surfaces the
  established layout already pairs in a row split its width evenly, unless
  one is a main area beside a narrow side rail. They end on the same line, and they get there by
  balancing what they hold — cutting a
  line that earns no place, moving a control, re-pairing the surfaces — never by stretching the
  shorter one; where content cannot be balanced, the shorter keeps its own height. An empty state is
  sized like any other content. Content that can outgrow its surface scrolls inside a
  maximum height, so the surface stays as tall as its content until it reaches the cap. A height set
  from outside the content belongs only to a surface whose content fills the space it is given — a
  chart, a map, media — to one the reader sized, or to a section deliberately sized to the viewport.
- **Size interactive content for its values, relationships and task, not a fixed fraction of the
  page.** Keep a page section's structural frame, heading, description and dividers at the width its
  page layout assigns. Bound simple control groups inside that frame so short values and their
  actions stay together; give structured content the room its columns and relationships need.
  Content that cannot get that room at some width never gets it by squeezing values until they
  wrap, truncate or shrink; which of it to remove or hide below that width is the user's choice,
  since it changes what information the product shows, unless a skill in use settles it. Compact controls do not require a narrow
  container, and a wide container does not require stretched controls. Use the product's
  established layout and control sizes, preserving comparable widths under the React copy and forms rule's **Forms**, rather than
  shrinking the section or creating a new peer-section row.
- **Place actions by what they affect, beside the content they act on.** A page's own actions —
  create, import, a toggle into a mode such as reorder or bulk edit, and the strip that mode shows
  while it is on — sit directly above the content they act on, below the page's banners and its
  load-failure area. Never put them in the header bar, the top navigation, or anywhere else above
  the banners, where they are far from what they change and easy to miss. The page layout owns that
  order — banners, failures, actions, content — so no page renders its own toolbar above it. An
  action on one section or item stays with that section or item. Do not move a contextual action
  into a detached row merely to satisfy a width or proximity rule. At narrower widths, wrap or stack
  related content and controls while preserving readable values, visible context, accessible labels
  and a clear association with their actions.
- **A table row stacked on a narrow screen reads from the left.** Each value sits left-aligned
  under its column's label; only the row's "⋯" menu takes the right edge. A value pushed to the
  right edge reads as detached from its label and sends the eye zigzagging across the card.
- **A frame that scrolls shows its scrollbar whenever its content overflows** — a box of legal
  text, a dialog body, a list or a table inside a maximum height — on every platform and before the
  reader touches it, so cut-off text reads as more to scroll rather than as text that ends. A hidden
  or hover-only scrollbar on such a frame is the defect, including the overlay scrollbar a platform
  hides until scrolling, which the shared scroll component replaces with one it always renders. The
  scroll container is styled once, in that component or the product's base styles, never per call
  site. This holds over general advice to hide scrollbars for a cleaner look.
- **Navigation decides who reaches a page, and the decision that hides a page also refuses to serve
  it.** An address the viewer's role, workspace, plan or permissions never offer them redirects to
  the viewer's home. A feature a higher plan includes is offered, locked, as the plan bullet below
  says, never redirected. A screen or empty state telling the viewer the page belongs to somebody
  else — "this page is for …", "switch to … to use it", "you don't have access" — is dead code
  wherever it sits, in a page, a layout or a gate: the check becomes the redirect and the screen is
  deleted, never restyled, moved into a shared message component, or kept because a task lists it
  among the states to restyle.
- **A menu button that collapses the navigation, such as a hamburger, is for phone and tablet
  widths only.** On a desktop the navigation stays in its bar: when its destinations outgrow the
  row, the bar first uses the full width of the page frame, then the row scrolls sideways. Folding
  them into a menu on a desktop is the defect.
- **Settings is the last group in the primary navigation, and the reader's own account is the last
  item within it.** The work the product exists for comes first; settings about the shared
  workspace come before settings about the reader themselves.
- **A multi-step flow the reader has finished — a verification, a setup, an onboarding — leaves the
  navigation, and its address redirects to the viewer's home.** A finished flow whose outcome is
  final shows no banner where the reader lands, a toast at most; one whose submission waits on
  someone else's decision — a review, an approval — lands the reader on the product as usual, with
  the banner the banner bullet below describes until the decision lands. A status page standing in
  the flow's place, at its own address or any other, is the defect. A page that a flow finished
  outside the product returns the reader to — the address an external service sends the reader back
  to once its own step is done — is that flow's last step and stays.
- **Inside a page, offer only what applies to the reader.** A choice, a document, a field or a
  status row the reader can never use — the other region's version of a document, the other account
  type's settings — is left out, decided by the same rule that decides which one applies, never
  listed beside it. What is left out is the item, never the step or section holding it: a step or
  section stays for every reader who still has something in it to answer, and goes only when nothing
  in it is left. A field whose value the context already fixes — the language of a course taught in
  only one, the venue of an event held in only one — is not asked: the value is set, and shown as
  text where the reader should know it.
- **A feature the reader's plan does not include is shown working, with its paid controls locked,
  never described by a notice.** The reader can start one, open it and see every option the paid
  plan adds, rendered as on that plan but disabled, and do what costs nothing, such as naming it and
  saving one with its defaults; the server refuses anything past that. Once the reader holds what
  their plan allows, the create action stays in place, disabled, with a hint on hover and focus that
  names the plan which creates more and links to the plans page, in the tooltip the next bullet
  describes. One notice in that surface names what upgrading unlocks, as the controls the reader
  can see, beside the upgrade action. A sentence saying the plan lacks the feature, or that the
  reader gets a default named by an internal term, shows nothing they would gain.
- **Every hover or focus hint uses the product's one tooltip, never a second popup built for one
  case.** A hint holding a link is that tooltip made reachable by pointer and keyboard: the reader
  can move into it and tab to the link.
- **A page's content offers one control per destination or action** — a button, a link, a menu item,
  an icon or a clickable row; the app's own navigation is not counted against it. Two that open the
  same form or page — a checklist step's button or linked label beside a quick link, a page action
  repeated inside the section below it — read as two different actions and crowd the page. Keep the
  one control where the reader looks for it; elsewhere, text naming the same destination stays plain
  text, and a control that carries nothing else is removed.
- **A row that opens its record is itself the control.** Clicking anywhere on a list or table row,
  or pressing Enter on it, opens or edits the record it shows; a pencil, "Edit" or "View" button
  beside it makes the reader find a second target for the one destination and is left out. Other
  controls in the row, such as the row's menu or a role picker, keep their own action without
  opening the row.
- **A row's actions go in one "⋯" menu at the row's end, not as buttons inline in the row.** Delete,
  archive, set as default, download and the like are menu items, with a destructive item last; a
  row of icon or text buttons competes with the row's content and differs from row to row. A
  control that is the row's content, such as a role picker or an on/off switch, stays in the row,
  and so does a remove control on an entry being edited in a form, such as one line of a list the
  reader is still writing.
- **An action graver than its neighbors is set apart from any action it could be mistaken for.**
  In a menu it goes last, below a divider; in a group of buttons it stands apart from the rest. Two
  destructive actions listed together, such as removing a member beside deleting the workspace, are
  one slip of the pointer apart, and the slip costs far more in one direction; sharing a red tone
  does nothing to tell them apart.
- **A field gets no button beside it for what editing it or leaving it already does.** An edit in
  place shows its save alone: Escape or moving away cancels it and keeps the saved value. A "×"
  button outside the field to cancel or clear it is a second control for the same thing, easy to
  mistake for a delete, and is left out; a clear "×" inside a search field, as part of the field, is
  the expected shape.
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
- **A record created from a short form is created in a dialog.** Its list's create button opens a
  dialog holding the form, such as a folder's name and icon; the list page never keeps the form open
  above its content, and the record gets no create page of its own. A create page is for a record
  whose form is a document the reader builds, such as a report with its sections.
- **A dialog is as wide as its content needs and no wider.** Take the smallest width on the
  product's dialog scale that holds its widest field or control group at its natural size, such as
  a row of icon choices; an empty band beside the content reads as unfinished and pushes the
  actions away from what they act on. When even the smallest step leaves a band, the scale gains a
  smaller step rather than the dialog a width of its own. Content that already spans the dialog,
  such as a grid of many options, keeps the width that lets the reader scan it, however much room
  each cell has to spare.
- **A dialog holds one form.** When the reader chooses between several forms or documents, the
  choice is made on the trigger before the dialog opens — a menu listing each option with a
  one-line description — never as tabs or a switcher inside it. A field the form itself submits,
  such as a type selector, is part of that form and stays inside.
- **A row of actions that follows content sits together, never spread to opposite edges.** On a
  page, such as a full-page form, a card or the choices under a prompt, the row starts where the
  content starts, at the bottom-left, with the primary action last. In a modal, a dialog or a
  confirmation, the row sits at the bottom-right, the primary action rightmost and cancel
  immediately to its left, where readers of modals look for them. A dialog that only points the
  reader to one next step shows that action alone. Its "×" already closes it, and a cancel beside
  the step the product wants taken invites the reader away from it. A dialog that collects input,
  takes a purchase or confirms an action keeps its cancel. Center actions only under centered
  content, such as an empty state. The next bullet governs multi-step footers. A control beside a
  heading, in a toolbar, at a table row's end or in a floating save panel follows that layout.
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
- **"Next" only moves on; it never performs the step's work.** A step whose requirement is an action
  — linking an account, connecting a calendar, uploading a file — offers that
  action as its own button in the step's content, and "Next" stays disabled until the requirement
  is met. A forward control that opens a dialog, starts a connection or makes a change before it
  advances leaves the reader unable to tell moving on from acting, and a step that advances on its
  own once the action finishes takes the reader somewhere they did not ask to go.
- **Every page renders in the product's page layout, including a page that reports a state** — a
  confirmation, such as the return page a flow finished outside the product lands on, or an expired
  link — with its content in sections, each headed and described as the React copy and forms rule's **Interface Copy** says. A
  section carries what the reader needs next — the record the state concerns, its status, the action
  that moves on, in that section's footer. A confirmation also thanks the reader, marks the success,
  and says what they now have and what happens next — never a neutral status panel, nor a
  placeholder for something the reader does not have yet such as "appears here". It ends on one
  action, which returns the reader to the page they left to start the flow, or to their home when
  that is unknown. A label and a button centered in an otherwise empty page is the defect, and so is
  a small card left under chrome that no longer applies, such as tabs or a form header. The page for
  an address that does not exist is the exception: a full-page message centered in the screen,
  outside the navigation, with one action home. A notice that the page is for somebody else, and a
  status page standing in a finished flow's place, are deleted as the bullets above say.
- **A boxed banner appears only when the reader has something to do, something is wrong, or
  something they submitted is waiting on a decision** — terms to accept, a verification to finish,
  a load that failed, a blocking state to resolve, a submission under review, worded from the
  reader's side as the status bullet of the React copy and forms rule's **Interface Copy** says. **General information the reader need
  not act on takes the slim notice instead**: one line, a soft tint, no border or shadow — how many
  projects the reader's plan includes, a note on how a feature behaves. Weight follows whether the
  reader must act, never how important the message feels: information in a boxed banner, a
  bordered callout or a card reads as a demand, and a state the reader must act on in a slim notice
  is missed. A success or completed state shows neither, and a toast at most when the reader's own
  action just caused it. A dismissible "approved" or "done" banner, and whatever stores its
  dismissal, is the defect: delete both.
- **A toast reports a result of the reader's action that the page does not already show, or the
  completion of a flow** — a record saved, an invitation sent, a file exported. An action that
  changed nothing the reader can see closes without one: a request already recorded, a step only
  someone else can take, a save with nothing changed, a dialog's Continue after the dialog has said
  what happens next. Apart from the flow-completion toast below, a toast never repeats text the
  dialog or page already shows, and one that claims an outcome which did not happen, such as a
  notification nobody sent, is the worse defect. A step of a multi-step flow shows none when the
  reader moves on, since reaching the next step is the feedback; the action that completes the flow
  shows one, worded as its completion, even where the page it lands on says the same in a banner,
  which the reader may not see at once. A form's save stays disabled until something in it differs
  from what was loaded, so a save with nothing changed cannot be made.
- **A banner about the account or workspace, rather than the page, shows only on top-level pages**
  — the home page and each destination the primary navigation lists — never on a page nested below
  one, such as a record's detail, edit or create page or a step of a flow. Storage nearly full, a
  renewal coming due, a note about the plan: the reader meets them where they arrive, and a
  nested page keeps its space for the task in hand. The page's level in the navigation decides it,
  in one place, so a new nested page leaves the banner out without being listed. A banner that
  explains why the page's own actions are refused — a read-only or suspended workspace on a page
  whose writes it blocks — concerns that page and shows wherever the refusal applies, as the
  whole-subject state bullet below says.
- **At most two non-error banners appear on the whole rendered surface, including its shell and
  sections; error banners are the exception.** Error banners may coexist visibly with those status or action
  banners and with other independent error banners. For simultaneous non-error conditions, trace each
  to its state owner, writers and prerequisites. If they cannot legitimately coexist, fix the state
  or transition that produced them; a display selector does not repair it. If more than two legitimate
  non-error conditions require banners, surface the product or flow conflict and the concrete alternatives
  that would resolve it for the user's decision, unless a skill in use settles it. Preserve established banner
  rendering while that decision waits; combining messages, changing presentation, prioritizing,
  capping, hiding or dismissing an unresolved condition is not a repair. Continue independent
  authorized work. Verify an approved state or flow remedy at its producing transitions and on the
  whole resulting surface.
- **A refused or failed user action reports its reason beside what the reader is acting on, or
  through the existing bottom notification system.** A refusal that concerns what the reader
  entered or chose in a field or control — a choice the field cannot take, an amount over its limit
  — is that field's or control's inline error, in the page or dialog where they acted, and clears
  when they change it. Every other failed or refused save, submission, download or requested
  action, including one refused because of the account's or record's state or one taken from a
  status or error notice, reports its human-readable reason through the shared notification owner. Never add a page or dialog error
  banner or an error modal for a user-action failure, or create another notification stack.
  Locally known prerequisites checked before an action starts follow the React copy and forms
  rule's **Forms**.
  Classify the operation by its intent, not its status code, HTTP method or whether a button started
  it: loading or retrying the data a surface needs follows the resource-load rule below. Preserve
  entered values, the original notice and its state and remedy, and independent resource errors;
  the report neither clears nor replaces them. Release pending protection when the action
  settles and restore native retry controls according to their prerequisites. Keep the API's safe
  human reason, with the established generic fallback only when no safe reason is available.
- **One message carries one error.** A banner, an inline error and a notification each state a
  single problem; several problems are never joined into one string, list or summary in one
  surface. A field or control shows at most one inline error at a time — the first, when one action
  leaves it with several — while other fields each show their own. A form whose submission fails
  on several fields reports each on its field, never in one combined banner, and independent
  failures that each need a banner or notification get one each. A remedy that shows two problems
  by joining their messages is the same defect.
- **Present each failure once.** A terminal error message replaces content only when the whole
  page's subject is unavailable, not when one request or part of a usable page fails. This full-page
  exception owns the specific human-readable reason and recovery action, keeps usable navigation,
  and shows no banner repeating the same failure or second generic failure heading. Show the
  recovery actions that apply and omit controls that require the unavailable subject. Keep its
  purpose heading short; render the explanation and recovery instruction as normal body text, not
  as a large or bold heading containing the whole error message. Unrelated usable content stays
  available; its presence makes a partial resource failure use the shared error-banner route below
  instead.
  Independent action failures report as the user-action bullet above says.
- **Resource and data load failures on otherwise usable surfaces keep a persistent native error
  banner with retry, using the standard shared component's frame and error visual tone.** On a page,
  each failed resource appears in a dismissible banner in the page's shared error area at the top,
  outside its structural content. No feature-local or embedded partial surface renders error text, a banner or a
  terminal-error placeholder. Moving a native shared banner outside a panel while keeping it inside
  that feature's section, row or grid cell still violates this placement rule. Route every partial
  failure through the page's shared failure owner, preserve
  unrelated usable content, and identify the failed content and recovery action in that banner.
  Never substitute field error messages, a toast or an unframed row, or put the banner in a card,
  table row, field, footer, submit row or floating save panel. A dialog's data-load failure uses the
  native shared banner at the top of the dialog, above its fields, rather than moving it to the page
  behind the dialog. A dialog that only exists to say what an action needs first never opens on data
  it could not load: the load failure reports as a page resource failure, in the page's shared error
  banner, worded as an error rather than as the dialog's usual explanation. The banner
  never replaces the surface's own heading or description, which keep saying
  what the surface is while the banner says what went wrong.
  When a load failure appears or changes, keep entered values and reveal its banner through the
  existing shared failure owner if it is outside the visible scroll area, including inside a dialog. Do not
  scroll on ordinary edits or unrelated status changes. Verify the reader can see the explanation
  and recovery controls in the actual viewport; DOM presence or an alert role alone is not proof.
- **A state of the whole page's subject shows once, as a persistent banner at the top of the page.**
  An account, workspace or project that is suspended, archived or read-only is not a failure of any
  one section: no section repeats the state itself, and each shows what it still can. An actual
  failed data load still shows its standard error banner alongside the persistent state banner.
  A refused action reports as the user-action bullet above says, without replacing that state. A
  library card that has lapsed keeps its status banner when a loan request fails; the refusal
  appears as a notification.
- **Red is for errors and destructive actions, never required verification or another blocking status.**
  Red, or whatever tone the product reserves for destructive and
  failed states, marks only a failure, a refusal the product reports, or a destructive action: one
  that removes or discards what the reader cannot get back. A decision the reader makes on someone
  else's submission, such as rejecting or declining it, is not destructive; it takes the neutral
  tone and sits beside its counterpart, as reject directly under approve. A state that blocks or
  warns without being an error — something the reader must resolve, a hold, a limit reached — takes
  the warning tone, and a neutral status the neutral one, on a badge, a banner or a text color
  alike: an order waiting on a missing delivery address is a warning, not an error.
- A component that renders inside more than one shell — a widget in a canvas and on a page, a card
  in a list and alone — is checked in each one. Spacing that a parent supplies in one place and not
  the other is what a single screenshot cannot settle.
