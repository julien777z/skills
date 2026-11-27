# Interface Doctor Lenses

Each lens states the defect it flags, the evidence that establishes one, the checks that find every
instance, the remedy, and what is left alone. `SKILL.md`'s **Lenses** table says which lenses a
partition reviewer reports and which the cross-cutting reviewer owns, and its **Pre-Pass** and
**Walkthrough** produce the tables, search hits, captures and measurement rows the checks read. A
reviewer confirms or rejects each candidate those hold and enumerates nothing they already list.

The rubric is the rule each check cites, read whole at its section: a check names the defect and
where the rule states it, never the rule's wording. A word list below is a search key over the copy
table's text column; a hit is read in its slot and on its page before it is a finding.

Lenses, in order: Idle Text, Routes And Workarounds, Refusals, System Internals, Headings And
Descriptions, Two Names, Form Shape, Squeezed Or Hidden Content, Uneven Surfaces, Control
Placement, Messages And States, Drawn Two Ways.

## Idle Text

Text an end user reads that changes nothing they do or understand, against the **Copy** section of
`writing-conventions`' product-copy reference and the React copy and forms rule's **Interface Copy**.

Evidence: the copy-table row, and the neighboring rows of its surface that already say what it
says, or the absence of anything the reader does differently for having read it.

- every description, hint and helper row whose text restates the label, heading, control or value
  beside it: compare each with the other rows of the same component;
- every row matching `secure|securely|encrypted|private|safe|safely|carefully|protected`: a property
  the reader takes for granted, stated where they act on nothing;
- every row matching `free|no charge|at no cost|included`: a cost the reader is not paying;
- every row matching `logged|recorded|attributed|audited|responsible|make sure you|be careful`: a
  warning about the reader's own ordinary action;
- every paragraph under an action that explains its mechanics or a side effect nobody asked about:
  rows in a description slot longer than one sentence;
- every description that narrates the surface's own controls: `click|press|tap|below to|above to`
  and `select the .* button`;
- every label that holds what the product already knows about the reader, such as their own
  address in a confirmation label: interpolated values in label slots;
- every dialog whose commit button repeats its trigger and title: three equal rows across one
  dialog's trigger, title and commit.

Remedy: the line is deleted, or cut to the one thing the reader needs; a commit button takes the
shape the **Interface Copy** bullet on commit buttons gives. Left alone: a property stated where
the reader acts on it or where it departs from what they would assume; a description the copy rules
make mandatory on a section, step or dialog, which **Headings And Descriptions** judges; and legal
text.

## Routes And Workarounds

Text that sends the reader along a route where a link belongs, or tells them to work around the
product, against the product-copy reference's link bullet and **Interface Copy**'s workaround
bullet.

Evidence: the copy-table row, the place or control it refers to, and whether its slot can hold a
link.

- every row matching `go to|navigate to|head to|open .* (then|and)|under (the )?[A-Z]|>|→` or
  `in (the )?settings|from the .* (menu|tab|page)`: a route to follow;
- every plain-text message an API, tool, email or command writes that names another place with no
  absolute address;
- every toast that refers to another place, since a toast holds no link;
- every row that quotes a control's label that is itself an instruction, or links to the page it
  sits on;
- every row matching `refresh|reload|restart|sign out|log out|sign back in|clear (your )?cache` or
  `try another browser`: a workaround handed to the reader.

Remedy: the place's name becomes the link, or the absolute address in plain text; a toast's way
forward moves onto the page; text about a control on the same page names the control where the
reader sees it and the thing it acts on. A workaround is removed and the page does the work itself,
as that bullet says: where the page shows stale data, fetching the current data is the fix and the
message states only the condition. Left alone: a retry control the product itself offers, and a
link that already takes the reader there.

## Refusals

A refusal or failure message that passes a verdict, repeats what the reader entered, joins several
problems, or frames a pending step as a penalty, against the product-copy reference's refusal
bullet, **Interface Copy**'s bullets on status and on what is not yet possible, the general React rule's
**Rendering and Data**, and the React layout rule's bullets on one error per message.

Evidence: the row, the service or component that words it, and the action that produces it.

- every row in an error, banner or toast slot matching `you can'?t|you cannot|you are not` or
  `you don'?t have|not allowed|not permitted|invalid|illegal|forbidden|denied|failed to|unable to`:
  a verdict on the reader or the act, with no next step;
- every refusal that interpolates the value the reader just entered or chose: template rows in
  error slots, in the interface and in the service that words them;
- every banner or notice matching `blocked|locked|denied|stay|until|restricted|suspended` about
  something the reader or someone else can still make possible;
- every message that joins problems: a list, a join over an error array, a summary banner above a
  form whose fields carry the same errors;
- every table of interface copy keyed by status code or error class for a first-party API, and
  every place the interface shows a message another reader's service wrote for an agent, an API
  client or a log;
- every expected refusal that reaches the reader as a generic failure: traced from the row to the
  handler that raises it;
- every status label worded from the product's side for the reader who sees it: one status with one
  label for every audience.

Remedy: a short, friendly request for the reader's next step, worded once at the service that
produces it, with the interface showing that message and writing its own words only from a reason
code; one message per problem, each on its field or in its own notification; a pending step worded
as who does what and what that enables. Left alone: a refusal the reader can do nothing about,
which may name the state plainly; a status label or badge, which names its state; the one
status-independent fallback for a response that carries no message; and a genuine server failure's
safe generic message.

## System Internals

Text an end user reads that speaks in the system's exact values or inner workings, and text only
the product's team reads that guesses a cause or assigns an errand, against the product-copy
reference's bullets on what the reader cares about and on team-only text, and **Interface Copy**'s
bullet on implementation.

Evidence: the row, its reader, and for an exact value whether the reader acts on it.

- every end-user row matching `error [0-9]{3}|status [0-9]{3}|code [A-Z0-9_]{3,}|exception|stack`,
  `timeout|rate limit|quota|queue|lock|retry|job|worker|cache|database|server|service` or
  `deploy|release|version|migration|maintenance|rollback`;
- every end-user row that interpolates a raw count, duration, size or timestamp in a sentence: read
  whether the reader chooses, pays or compares by it;
- every end-user row matching `almost|about|approximately|roughly|nearly` attached to a plain word;
- every end-user row holding an enum member, a snake-case or camel-case token, an identifier or an
  internal state name;
- every field description that says how a value is stored, masked, hashed or processed;
- every team-only row matching `probably|likely|may be|might be|seems|out of date|misconfigured` or
  `please (ask|contact|check|fix)|should be`: a guessed cause or an errand;
- every team-only row that uses the product's in-world word for a player, account or item where a
  plain term exists.

Remedy: plain words for what the reader cares about, with the exact value kept only where they act
on it and the cause moved to the log and to team-only text; a team-only message states the observed
condition and lists its values. Left alone: a price, a quantity the reader chooses, a figure they
compare; a proper name such as the product's currency; a version shown on a page whose subject is
versions; and text in logs.

## Headings And Descriptions

A heading, title, description, label or confirmation dialog out of the shape **Interface Copy** and
**Confirmation Dialogs** give it.

Evidence: the row and its slot, and for a truncated or missing line the capture of its surface.

- every heading or title row that is a sentence, a question or addressed to the reader: rows in a
  heading slot ending in `.`, `?` or `!`, holding a verb phrase, or matching
  `you|your|let'?s|welcome|here`;
- every heading or title cut short: an ellipsis in the text, a truncation or clamp utility on a
  heading from the source searches, and each heading the measurement rows list as clipped;
- every surface named for the reader's role rather than what it holds;
- every section, flow step and dialog with no one-sentence description under its heading, in every
  state it renders: component-use rows where the description prop is absent, and each shared dialog
  or section component whose description is optional;
- every sentence that sits between a page's top bar and its first section;
- every abbreviation a surface uses with no spelled-out first mention;
- every bare verb on a control among several things it could act on;
- every confirmation dialog: a title that is a question or a record's name, a body that does not
  ask the question, that repeats the title, or that runs past the question and one consequence, and
  typing-to-confirm on an action short of the most severe;
- every dialog built from primitives beside the component that owns the confirmation shape, which
  is also a candidate for **Drawn Two Ways**.

Remedy: the heading becomes a name in fewer words and its sentence moves to the line beneath it;
the missing description is written from what the reader does there, and the shared component makes
it mandatory; the confirmation takes the one component's shape. A heading or label that is correct
and merely plain keeps its words. Left alone: a marketing page's headline outside the application
shell, and a title whose length the product's layout already holds whole.

## Two Names

One thing called by two names, features offered side by side that a reader could mistake for each
other, and one slot's capitalization broken, against **Interface Copy**'s bullets on capitalization,
side-by-side names and status labels, and `change-scope`'s **Product Choices** on inconsistent
text. Whole repository: a name is wrong only beside the other name.

Evidence: both rows, their slots, and what each refers to in the code — the model, route or
component both names resolve to.

- group the copy table's noun phrases by the model, route, component or enum member they label; a
  group holding two names is a candidate, counted with every row of each name;
- every navigation item against the heading of the page it opens, and every button against the
  title of the dialog it opens;
- every pair of sibling navigation items, tabs or features whose names are near synonyms;
- every status with labels kept in more than one place, or one label shown to audiences that need
  different ones;
- every heading, label, button, tab and menu-item row whose capitalization differs from the form
  most rows of that slot use, and every source string written in a case its type variant then
  changes;
- every product page the interface's own text calls a screen, a view and a page in turn;
- every message that states the same condition in different words in two places.

Remedy: the name the product, its navigation and most rows already use wins, and every other row
moves to it in the same change, the fixture text that restates it included; a status maps to each
audience's label in one place. Where neither name is established, or two features need new names,
the choice between names is the run's decision, as `SKILL.md`'s **Dispositions** says. Left alone:
a proper noun's own capitals; an audience's own label for a status; and a variable or file name,
which is not interface text.

## Form Shape

A form that hides input it needs, picks the wrong control, or saves, confirms or fills in a way the
rules name a defect, against the product-copy reference's **Forms** and the React copy and forms
rule's **Forms**.

Evidence: the form's source — its fields, their controls and which are mandatory — and its capture
where one exists.

- every hit of the closed-disclosure search: a section, accordion or disclosure that starts closed
  and holds a field the form needs, or one that becomes needed during the flow and does not open;
- every field that picks one value from a defined list and renders a free-text input, and every
  domain field rendered by a second control beside the one that owns it;
- every submit, Next or Save that is enabled while a locally known prerequisite is unmet, and every
  error banner raised for incomplete input;
- every action shown disabled, with nothing to act on, beside actions that work;
- every form the product would refuse in full that is still shown;
- every page that edits saved values through buttons on the page, per section or in a footer that
  shows whether or not anything changed, and every save enabled with nothing changed;
- every form a person signs or certifies that is filled in from a profile or an earlier submission;
- every form for someone else's details, and every search or picker box, from the autofill search:
  the attributes set per field rather than once, or left for the browser to fill;
- every picker over consequential records that lists suggestions on focus, and every suggestion
  list that opens empty while loading;
- every form past a handful of fields with no titled sections, every section holding one input, and
  every qualifying control separated from the control it qualifies;
- every pair of fields with the same role at different widths or heights, and every form mixing
  direct controls with read-only values that each need an edit control;
- every second checkbox that confirms part of what the first confirmed;
- every placeholder matching `^0+$|^[*•.\-_x]+$|^(n/a|none)$`: zeros, dots or a mask in place of an
  example of the format;
- every setting edited on another surface that could be edited where its value is shown.

Remedy: the shape the rule states for that case, made at the shared form, field or save component
so sibling forms take it together. Left alone: a section that holds only optional input, which may
start closed; a form that creates a record or submits a flow step, which keeps its own footer; a
form in a dialog, which saves through the dialog's actions; a form for the reader's own details,
which keeps accurate autofill tokens; and a hard-coded option list, which is a code finding for the
doctor `get-doctors` lists for code slop.

## Squeezed Or Hidden Content

Content squeezed, truncated, wrapped, clipped or hidden where it should be given room, against the
React layout rule's **Layout And Spacing** bullets on sizing content for its values, padding and
chrome, scrolling frames and stacked rows, and `change-scope`'s **Product Choices** on making
content fit.

Evidence: the capture, its width and role, the region, the measurement row that lists the element,
and the source line that sets the width, clamp or breakpoint.

- every measurement row for a sideways-scrolling document, per width;
- every element the measurement rows list as clipped, ellipsized or clamped, and every hit of the
  truncation search that a capture shows cutting a value the reader needs;
- every table cell, button label, tab, card title or toolbar control the measurement rows list as
  wrapped past one line, and every column or card a capture shows narrowed until its values break
  word by word;
- every type size a breakpoint reduces to make content fit;
- every text the measurement rows list as present at the widest width and absent at a narrower one,
  and every hit of the hidden-by-breakpoint search, read against the task record for a decision by
  the user to hide it;
- every frame whose content overflows with no scrollbar showing before the reader touches it, and
  every hit of the hidden-scrollbar search;
- every region a capture shows covered by a header, toolbar, footer or sticky heading;
- every stacked table row on the phone-width capture whose values sit at the right edge away from
  their labels;
- every hit of the fixed-width search on a container whose content a capture shows cut or crowded.

Remedy: a remedy that keeps every value readable, of the kinds **Product Choices** lists, made in
the component that owns the layout and at the width the defect shows; chrome that covers content
gets its own row; the scroll container is styled once in its shared component. Which content to
remove or hide where it cannot get its room is the run's decision, as `SKILL.md`'s
**Dispositions** says. Left alone: content the user decided to hide at a width; an element hidden
because another element shows the same value at that width, such as a navigation bar folded into
its menu at phone and tablet widths; and a title too long for its place, which **Headings And
Descriptions** shortens in words.

## Uneven Surfaces

Spacing, type scale, frames and heights that depart from the product's own scale or stretch past
their content, against **Layout And Spacing**'s bullets on the heading scale, padding, the content
frame, surface height, dialog width and paired values, and the general React rule's **Rendering and
Events** on button width.

Evidence: the capture and region, the measurement rows compared — this page's against the pages of
its kind — and the source line that sets the value.

- every heading whose computed size is off the product's heading scale for its component, and every
  display-size line inside the application shell;
- every section whose padding, or gap to its neighbor, differs from the value most sections of that
  component show, and every hit of the raw-spacing search that produces it;
- every page whose content starts at a different distance from the navigation than the pages of its
  kind, and every page file that sets its own width, centering or outer padding;
- every card, panel, section or widget a capture shows with a large empty area below its content or
  between its content and its control, and every surface stretched to match a taller neighbor;
- every dialog a capture shows with an empty band beside its content;
- every button the measurement rows list as wide as its container, and every hit of the
  stretched-button search;
- every side-by-side comparison whose editable and read-only values sit on different rows;
- every component rendered in more than one shell whose spacing differs between them.

Remedy: the value on the product's scale, set in the component that owns it, with page-level
overrides removed; a page takes its kind's frame from the layout component; a surface is as tall as
its content; a dialog takes the smallest step of the dialog scale that holds its content. Left
alone: a surface whose content fills the space it is given, such as a chart, a map or media; a
surface the reader sized; a main area beside a narrow side rail; and how the spacing is spelled in
source, which belongs to the doctor `get-doctors` lists for code slop.

## Control Placement

A control outside the product's established position, doubled, labeled by something other than
its place in a flow, or not reading as what it is, against **Layout And Spacing**'s bullets on
actions, rows, menus, dialogs and flow footers, **Shared Surfaces**' bullet on recurring
interactions, **Interface Copy**'s bullet on list filters, and **Rendering and Events**.

Evidence: the capture and region, the comparable page that shows the established position, and the
source that places the control.

- every page action in the header bar, the top navigation or above the page's banners, and every
  page that renders its own toolbar above the layout's order;
- every section or item action moved into a detached row away from what it acts on;
- every list or table row with an edit, view or pencil control beside a row that already opens its
  record, and every row whose actions are inline buttons rather than items of its one menu;
- every destructive item not last in its menu, and every grave action sitting beside one it could
  be mistaken for;
- every pair of controls in one page's content that open the same destination or perform the same
  action;
- every cancel or clear control outside a field for what leaving the field already does;
- every row of actions spread to opposite edges, or placed against the position its surface gives
  it, and every dialog that only points to one next step and still shows a cancel;
- every multi-step flow footer whose labels name the step's content, whose Back sits beside the
  forward action, or whose forward action performs the step's work or advances on its own;
- every menu button that folds the navigation at a desktop width, and every primary navigation
  whose settings group or account item is out of the order the rule gives;
- every list filter drawn as tabs past a few top-level groups, and every count beside a select's
  option;
- every textual link with no hover change, every labeled button in a form that reads as text at
  rest, every clickable card or row whose text cannot be selected, and every button whose pending
  state changes its width or label.

Remedy: the control moves to the position the rule and the comparable pages establish, made in the
layout or shared component that owns that order; a doubled control leaves the one where the reader
looks for it. Left alone: a control that is the row's content, such as a role picker or a switch; a
remove control on an entry being edited in a form; a clear control inside a search field; and the
app's own navigation, which is not counted against a page's controls.

## Messages And States

A banner, notice, toast, failure, loading state or state page in the wrong place, weight or tone,
and a page or step that should not exist, against **Shared Surfaces**' bullets on loading and
missing content and **Layout And Spacing**'s bullets on banners, toasts, failures, tone, navigation,
plan limits, flows and state pages.

Evidence: the capture where a scenario reaches the state, otherwise the source that renders it, and
the request or condition that triggers it.

- every boxed banner that carries information the reader need not act on, every slim notice that
  carries something they must act on, and every banner or stored dismissal for a success state;
- every surface a capture or source shows holding more than two non-error banners: each traced to
  the state that produces it;
- every account or workspace banner rendered on a page nested below a top-level destination;
- every failed or refused user action reported through a page banner, a dialog banner or a modal,
  and every second notification stack;
- every resource-load failure rendered inside a card, row, field, footer or feature section rather
  than the page's shared error area, and every toast or field message standing in for one;
- every failure presented twice, and every whole-page error message used where part of the page
  still works;
- every state of the whole page's subject repeated by its sections;
- every toast that repeats what the page or dialog already shows, reports an outcome that did not
  happen, or fires on a step of a flow;
- every use of the destructive tone on a state that blocks or warns without being an error or a
  destructive action;
- every empty or not-found state that can render before its request answers, every second loader
  inside a section that owns its loading, and every loaded view replaced by a skeleton on refresh;
- every page, layout or gate that renders a notice that the page is for somebody else, and every
  status page standing in a finished flow's place;
- every flow step that asks the reader for nothing, every flow step rendered as a dialog, every
  short-form record with a create page of its own, and every dialog holding more than one form;
- every state page outside the product's page layout, and every paid feature described by a notice
  rather than shown with its paid controls locked;
- every hover or focus hint drawn by a popup other than the product's one tooltip.

Remedy: the presentation the rule gives that condition, through the shared owner of banners,
failures and notifications; a page that should not exist becomes the redirect and is deleted with
whatever stored its state. More than two legitimate non-error banners is the run's decision, as
`SKILL.md`'s **Dispositions** says. Left alone: the page for an address that does not exist, which
keeps its full-page message; a return page a flow outside the product lands on; an error banner
beside a status banner; and the behavior behind a state — refetching, caching, redirect logic —
beyond what the reader sees, which is fixed only where the walk shows it failing.

## Drawn Two Ways

One component, state, message or sibling surface drawn differently on different pages, against
**Shared Surfaces**' bullets on the established owner, sibling surfaces and shared mechanisms, and
the general React rule's **Components and Props**. Whole repository: each drawing looks right alone.

Evidence: both instances — captures or source lines — the shared component that owns the shape or
the instance most pages use, and the list of every page on each drawing.

- every row of the component-use table where a page or feature builds a dialog, banner, notice,
  toast, tooltip, empty state, skeleton, table row, save control, form section or page frame by
  hand while a shared component owns that shape;
- every shared shape with two owners: two dialog shells, two empty states, two notification
  systems, two tooltips, two save controls;
- every surface that does for one audience, plan or workspace kind what a sibling does for another:
  compare the two for component, placement, size and controls;
- the create and the edit of one record, and the variants of one document, compared field by field
  and section by section;
- every recurring interaction — selecting, changing or removing related items — compared across
  the pages that offer it for where the list, action and editing surface sit;
- every state of one kind — empty, loading, failed, locked — compared across pages from captures
  where the walk reached it and source where it did not;
- every page of one kind compared by its measurement rows for content start, heading size and
  section padding;
- every redesigned shape some pages still carry in its old form.

Remedy: one owner. The shared component, or the instance that is right, becomes the shared
primitive; every page that draws its own moves onto it in the same change and its copy is deleted,
each difference a page still needs becoming a documented variant. A move that gives a page the look
the rest of the product already has is a fix, as `change-scope`'s **Scope Follows The Defect, Not
The Request** says; where the two drawings are evenly used and neither is the rule's, which one
wins is the run's decision, as `SKILL.md`'s **Dispositions** says. Left alone: a difference the
content each audience needs explains; a page whose look the task record shows the user decided; a
variant the shared component documents; and the wrapper components and class strings that build a
drawing, which the doctor `get-doctors` lists for code slop owns.
