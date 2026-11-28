---
description: Apply when writing interface copy, confirmation dialogs, or forms in React.
alwaysApply: false
paths:
- '**/*.ts'
- '**/*.tsx'
- '**/*.jsx'
---

# React Interface Copy And Forms

## Interface Copy

- **Headings, labels, buttons, tabs and menu items share one capitalization across the product**,
  sentence case unless the product has settled on another: "Save draft", "Shared folders", "Reading
  list". A mix is the defect; a proper noun keeps its own capitals. Capitalization is the source
  string's: a type variant that renders text uppercase is styling, and the string stays written in
  the product's case.

- **Write labels, descriptions and hints for someone who already trusts the product.** Copy that
  warns the reader about their own ordinary action reads as suspicion. A person submitting a record on
  behalf of someone in their own workspace, who has already checked the box that says they may, does
  not need to be told that the action is logged or attributed to them.
- **Name a surface for what it holds, never for the reader's role in it.** A reader knows which role
  they hold, so "Organizer events", "Attendee tickets" or "Your speaker profile" labels them rather
  than the thing; the heading is "Events", "Tickets", "Profile", whatever the surface holds.
- **Every heading and title is a name in a word or a short phrase, never a sentence.** That holds
  for a page, a section, a card and a dialog, and for a state the page shows in place of its
  content, such as an empty state, an error or a refusal: "Overview", "Contact details", "No
  playlists yet", "Sync off". A sentence, such as "This folder is shared with you as read-only", or
  a phrase addressed to the reader, such as "What you can do here" or "Let's get you set up", goes
  in the line under the heading, which carries the explanation. A title too long for its place is
  given fewer words, never cut short with an ellipsis, whether by the text written into it or by
  styling that truncates it: a title the reader cannot finish names nothing.
- **Features offered side by side carry names no reader could mistake for each other.** Each name
  says what the feature holds or does in the reader's words, so a reader who has used neither picks
  the right one: "Collections" beside "Groups", or "Profiles" beside "Accounts", reads as two words
  for one thing. Read the names together, as the reader meets them, before settling either.
- **The interface writes its own text for a reason another reader's message carries.** A message a
  service writes for a different reader, such as an agent, an API client or a log, says what that
  reader needs: an agent's carries the URL it can follow. The service sends a reason code beside
  it, and the interface writes the words for its own reader and the page they are on, never
  showing the other reader's message.
- **Never write copy about the product's state that nobody has confirmed.** A page that says a
  feature is unavailable, coming soon or not yet supported, when nobody said so, misinforms the
  reader; the product's state is confirmed with the user before any copy states it.
- **Never state what the reader takes for granted.** That data is encrypted, stored securely, kept
  private, or handled carefully is assumed of any product in this category; saying it out loud plants
  the doubt it was meant to settle. Mention a property only where the reader has to act on it or
  where it departs from what they would assume.
- **Keep implementation out of the interface.** Storage, masking, hashing, background jobs, retries
  and the names of internal states belong in the code. A description says what the field is for and
  what the reader should put in it, in the words they would use themselves.
- **Copy never hands the reader a workaround for the implementation.** No message tells the reader
  to reload or refresh the page, sign out and back in, or clear their cache to get past what the
  product should have done itself. When an action reveals that the page shows stale data, such as a
  request refused because the item it targets has changed since the page loaded, the page fetches
  the current data itself — in the background, as a transition that keeps the settled view under
  the React layout rule's **Shared Surfaces** on screen with no skeleton and no full reload, an
  update that would move content applied in place without shifting the reader's position — and the
  message states only the condition, such as "This playlist was deleted."
- **Every section, every step of a flow and every dialog carries a one-sentence description under
  its own heading, inside its surface** — two on a flow's first step, as the React layout rule's
  **Layout And Spacing** allows for a flow's first question — saying what the reader does there, what the section holds, or why
  the dialog appeared, in terms of what the reader is trying to do: "Choose how you hear about new
  activity", "The people who can see and edit this project", "Sharing an album requires a verified
  email address first." It never narrates the surface's own controls, such as "Pressing Next opens…"
  or "Click below to…": the button's label already names its action. A heading alone, or a heading
  with only a badge beside it, is the defect, in every state the surface renders, a loading or
  failed one included. A shared dialog component makes its description a required prop, so a
  title-only dialog cannot be written. No sentence floats between the page's top bar and its first
  section: a page's name sits where the product puts page titles, and whatever a page-level sentence
  would say belongs to the section it describes.
- **Spell out an abbreviation the reader may not know the first time a surface uses it**, with the
  short form after it, such as "Service Level Agreement (SLA)"; later mentions on that surface use
  the short form alone.
- Say the one thing the reader needs and stop. On a field, prefer no description to a description
  that repeats the label, narrates the obvious, or hedges, and keep out of any label what the
  product already knows about the reader, such as their own email address in a confirmation label.
  Where a sentence is only there to cover the product, cut it. That includes a paragraph explaining
  the mechanics around an action, such as which party performs which step, and a note of a side
  effect nobody asked about, such as what happens to earlier versions.
- **A dialog's commit button never repeats the label its trigger and title already carry.** The
  reader pressed "Add song" to open the dialog and read "Add song" as its title; a third "Add song"
  on the button says nothing new. The commit names the act in the fewest words: "Save" for a form
  that adds or changes something, the bare verb for a confirmation — "Delete" under "Delete
  playlist". When that verb is also the word the product's dialogs use to dismiss, such as "Cancel",
  the commit adds what it acts on — "Cancel booking" — so one word never means both doing the
  act and backing out of it.
- **A bare verb labels a control only where what it acts on is plain from what surrounds it**, as
  under a dialog's title. A control among several things it could act on names its object: "Shuffle
  queue" beside a player's search field and volume, never "Shuffle".
- **A list filter takes tabs only for a few top-level groups that fit one row on a phone**, such as
  all, mine and shared; a filter with more options, or one likely to gain them, such as a
  status, is a select in the filter bar. A row of many tabs wraps or scrolls on a phone and takes
  the room the next filter needs, while a select holds any number of options in one control. A
  filter select's options carry no counts; a count beside a filter option belongs only on a tab.
- **A status reads from the viewer's side.** Name the state in terms of what that reader did or
  still has to do, and keep internal steps they take no part in behind a visual cue: a person who
  sent a form sees "Submitted", with the tone telling review apart from acceptance, while the
  reviewer sees "Pending review" and "Approved". One status maps to each audience's label in one
  place.
- **A banner or notice about something not yet possible says what will make it possible, never
  that it is held back.** Its sentence names who has to do what and what that enables — "This
  member must confirm their email to enable exports" — rather than "Exports stay blocked until they
  confirm", which reads as a penalty. Words such as blocked, locked, denied, stay or until frame a
  pending step as a punishment; keep them for a refusal the reader can do nothing about. A status
  label or badge is not such a sentence: it names the state plainly, as the status bullet above
  says. A notice only the product's own team reads states the observed condition and the values it
  concerns instead, with no guessed cause and no request of anyone, since its reader is the one who
  investigates.

### Confirmation Dialogs

- **A dialog title names the action and is never a question.** "Archive record", "Delete role",
  "Discard draft": the title is what the reader is about to do, stated flatly, so it reads the same
  whether the dialog asks for confirmation or reports a result. "Archive record?" puts the
  question in the one place the reader cannot answer it.
- **The body is where the question is asked, and a confirmation body opens with "Are you sure you
  want to …".** After the question, one sentence on what follows — what the reader loses, what stops
  working, whether it can be undone — and nothing else. On a confirmation, this body is the
  dialog's description, and the question with its one consequence sentence stands in for the
  one-sentence limit.
- **The body never opens with the title again.** A title reading "Archive record" over a body
  reading "Archive Ann Lee? …" says the same words twice and spends the only line the reader
  actually reads on the one they have already read. Write the body as though the title is above it,
  because it is.
- Name the record in the title's noun, not the title's value: a dialog headed with one record's
  name is a different heading on every row, and the reader learns nothing from it that the row they
  clicked did not already tell them.
- **Typing to confirm is reserved for the most severe actions**, such as deleting an account or a
  whole workspace, where everything the reader holds goes at once. There the reader types something
  that identifies what they are acting on and the action stays unavailable until it matches. Every
  other action, including one that cannot be undone — deleting a record, removing a saved address,
  sending a message — is confirmed by the dialog's button alone.
  A phrase demanded for routine actions slows every one of them and is soon typed by reflex.
- One component owns this shape, under the React layout rule's **Shared Surfaces**: dialogs hand-built from the same
  primitives are where these rules get broken one at a time.

## Forms

- **Choose each field's control from the values it accepts before laying out the form.** A field
  that selects one value from a defined list uses the shared dropdown or combobox, never a free-text
  input. Reuse the existing domain control and its complete option source wherever that field
  appears; country and state fields do not become text inputs in a generic field renderer.
- **Check locally known prerequisites before opening a dialog.** An unmet prerequisite keeps the
  dialog closed unless the dialog is a necessary entry point. When the dialog stays closed,
  disable the entry action if the reason is visible. Otherwise, keep it clickable and show the
  actionable reason in the page's shared error banner on click. A necessary dialog opens and
  shows the reason in its shared banner with its final action disabled until the prerequisite is
  met. Ordinary incomplete fields and selections keep the action disabled without an error banner.
- **Leave an unavailable action out when another action beside it is available.** An action with
  nothing to act on shows disabled only when no other action in its menu, toolbar or group is
  available, or when the plan bullet in the React layout rule's **Layout And Spacing** locks a paid
  control. Except for the entry action above, keep an action disabled beside available actions
  while its prerequisite can still be met: incomplete forms or steps, unchanged values, and actions
  already running.
- **A form the product would refuse in full is never shown.** When every choice it offers would be
  refused, because the feature is off or nothing asked for is allowed, the page shows in its place
  why, and the way forward for this reader, with one action to leave. The server refuses that
  submission too, so the state cannot be reached by posting around the page.

- **A page or form that edits saved values saves through one floating save panel fixed to the bottom
  of the viewport, never through buttons on the page** — a settings page, a profile, a record's edit
  page alike. The panel is out of view until a field differs from its saved value; then it animates
  up from below the viewport's bottom edge to rest a little above it, holding a cancel action that
  restores the saved values and a save action. It floats over the page and never takes room in it,
  so nothing beneath it, a page footer included, moves when it rises. It stays in view as the reader
  scrolls while changes are unsaved, and slides away once they are saved or canceled. A reader who
  unchecks one topic on a newsletter preferences page sees it rise, and checking the topic again sends
  it away. A save or reset button per section, a row of them at the end of the page or form, and a
  footer that sticks to the bottom of the page whether or not anything changed are the defect. A
  form that creates a record or submits a flow step is not editing saved values and keeps its own
  footer, and a form inside a dialog saves through the dialog's own actions; the panel belongs to a
  page the reader scrolls. One shared component owns the panel, under the React layout rule's **Shared Surfaces**.
- **A form a person signs, certifies or attests to starts empty.** Nothing is seeded from a profile
  or an earlier submission, because the signer vouches for what they entered.
- **A form where the signed-in person enters someone else's details turns browser autofill off on
  every field, selects included** — a record made on another person's behalf, a person they add to a
  team, an organization or other record they name — so the browser never fills the reader's own
  name, address, email or saved organization into a record that is not the reader. One boundary
  around the form sets it for every control inside, including those a shared field component
  renders, never a token per field that the next added field forgets. "Off" means what the browser
  and the common password managers actually honor, which a bare `autocomplete="off"` is not for
  name, email and address fields. A search or picker box offers nothing the browser saved — neither
  saved details nor values typed into other fields — wherever it appears, since it never holds
  anyone's details: Chrome stops typed history only for exactly `off`, and fills nothing in a field
  it reads as a search term, so such a box takes `off` with a `search` name. The shared input and
  combobox components own those attributes. A form for the person's own details keeps accurate
  autocomplete tokens on each field.
- **A search box that picks a consequential record — a person, an account, a project — shows no
  suggestions and makes no request until the reader types.** A list on focus invites a pick by
  proximity rather than intent, and offers records the reader never asked to see. A picker over a
  low-stakes vocabulary, such as tags, may suggest on focus. The shared search component makes each
  caller declare which kind it picks rather than defaulting to either.
- **A suggestion list opens only once it has something to show:** its results, or its empty
  message once the search has finished. While the results for the typed text are still loading,
  the list stays closed and the field shows the loading state; an empty frame that grows when the
  results land reads as a broken list.
- **A form longer than a handful of fields is grouped into titled sections,** each holding the
  fields that answer one question; sibling forms share one section layout, under the React layout rule's **Shared
  Surfaces**. A section is never one per input: a control that only qualifies another — how
  picked items combine, the unit of an amount, the end of a range — sits in that control's section,
  directly under it, and the section's one description covers both.
- **Group fields by the question the reader answers, not by how short their values are.** Fields
  answered together sit side by side wherever the width allows, wrapping when it does not; independent
  decisions keep separate rows even when both controls are short.
- **A small setting that can be edited independently is edited where its value is shown.** Put the
  control beside its label or current value where space allows, sized for its values; stack it when
  narrow space or long labels need it, preserving readable values and the accessible label
  association. Opening another surface solely to change that one setting adds a step without a new
  decision. Keep a separate editing flow when coupled fields, detailed validation or sensitive-action
  confirmation require it, and retain the product's save and cancel behavior.
- **Comparable controls use comparable dimensions.** Inputs with the same role in a form take the same
  width or grid span; let the value format or available space justify a difference. A content-sized
  control beside a fixed-width peer reads as a different kind of choice even when both collect the
  same kind of answer. Choose the editing mode for the form, not independently for each field:
  a form ready for input uses direct controls throughout, rather than mixing them with read-only
  values that each need an Edit button. Equivalent editable fields use the same inline row layout
  and control height, including fields enabled by a selection. Preserve masking for sensitive values
  in that layout.
- **One act gets one confirmation.** A single checkbox, worded as the whole statement the reader is
  making, stands for it; a second box restating part of the first asks twice.
- **Long fixed text a reader must accept — a certification, terms, a disclosure — is set in smaller
  muted type** and scrolls inside a maximum height as the React layout rule's **Layout And Spacing** describes.
- **A placeholder shows a realistic example of the value's format,** such as `555-0100` or
  `2030-01-31`, never zeros, dots or a mask that reads as an existing value hidden from the reader.
