---
name: roblox-game-overview
description: Build a dashboard that explains a Roblox game to someone who has not played it — what it is, its rules, how its quests, levels, rounds or areas connect, with pictures staged in the game itself — and audits its content for consistency. Use when asked for an overview, explainer, map or audit of a Roblox game; with no game named it covers the game the current repository and session work on, otherwise the game the request names. Run only when the user asks for it.
short_description: 'Explain and audit a Roblox game in a dashboard with pictures staged in the game.'
---

# Roblox Game Overview

A reader's map of one Roblox game, built from the game's own source and shown through
`use-dashboard`: what the game is and how it plays, pages chosen for its genre, pictures of each
part staged in the game, and a page auditing whether its content agrees with itself. The game's
source is the authority; a design document is compared with it, never read in its place.

## Dependencies
- `use-dashboard`
- `roblox-studio`
- `subagent-matrix`
- `use-browser`

## Choose The Game

- **With no argument**, the game is the one the session works on: the current repository's checkout
  and the branch the session uses, with the project guidance and game skill that repository holds.
- **With an argument**, it names the game, a repository or a branch; read that one. A request
  naming only part of a game, such as one world, still gets the Overview and How to play pages and
  the audit for that part.
- Read the game from a fresh worktree of the chosen branch, at its fetched head, and leave the game
  unchanged: nothing this skill does is committed to the game or saved into its places.

## Run Order

The page reaches the reader before any picture is staged, and every later step updates that same
page:

1. **Read the game** and write the spec: text, dialogs, diagrams, tables and the audit, all rebuilt
   from the source on every run, since they are cheap and must match the head read.
2. **Render and deliver at once**, with every picture the picture manifest still accepts already in
   place and the rest left out, as **Render And Deliver** says.
3. **Stage the pictures still owed**, batch by batch, as **Pictures** says, re-rendering into the
   same page as each batch lands.
4. **Review the page after its last render**: open it in a browser through `use-browser`, read
   every page and at least one dialog of each kind whole, fix what reads wrong, and after that
   re-render read again each page the fix changed. A read before the last render covers nothing.

## Read The Game As Data

1. **Load the content the way the game does.** Where the repository runs its modules outside the
   engine, such as a standalone test runner with its own module loader, load the content modules
   through it from a script outside the checkout, giving the engine's value types (vectors, frames,
   colors) small stand-ins and generating any network or build output those modules require first.
   Dump the loaded tables to JSON: quests, side quests, story staging, maps and areas, points,
   encounters and creatures, collections, shops and items, spells or abilities, progression. Where
   the content cannot be loaded, read the definition files directly.
2. **Use the game's own lookups** for anything it derives — which area a position falls in, where a
   character stands at a given progress, which map an encounter is fought on — by calling them on
   the loaded modules rather than reimplementing them. Their answer is the one a player sees.
3. **Resolve places per map.** A combined place can hold every map, and a lookup built for one map
   then answers for another: a point on a map with no named areas falls back to the other map's
   town. Resolve each point against its own map's areas, and where that map names none, against
   the landmarks it does have, such as the nearest named room or gate.
4. **Read the game's design documents and its game skill** for summaries, cast notes and intended
   behavior, and note each place they disagree with the source for the audit.

## Pages

Every overview has these pages, in this order, then the genre's pages from the router below, then
Consistency:

- **Overview**: a headline picture, what the game is in a few plain sentences, the core loop as a
  `diagram` with numbered steps, a `table` of its worlds or modes, and at most four stat cards; a
  count beyond four goes in a card's detail line, such as creatures beside characters.
- **How to play**: the rules as a stacked `outline`, a `figures` section of drawn rule pictures,
  the controls as a `table` for keyboard and touch, then progression and the economy: levels,
  currencies, shops, inventory, daily and weekly activities.
- **Consistency**, last: a `table` of every check with how many items it covered and its result,
  each row opening that check's findings; a findings `outline` grouped by check, each finding
  naming its quest, round or stage so the name opens its dialog, with a source link at the commit
  read; and a short `notes` section on how the content was read. Set the page's `status` in the
  warning tone while findings exist. Report findings; never fix the game from this skill.

## Genre Router

Tell the genre from how the game is played: its main loop, what the player spends most time doing
and how the source organizes its content. Read each file that matches; a game spanning several
genres, such as a story game with minigame events, reads each.

| Genre | Reference |
| --- | --- |
| Quests and story: a main story, side quests, characters, areas | [quests](references/genres/quests.md) |
| Minigame collections: short rounds the server rotates | [minigames](references/genres/minigames.md) |
| Tycoons and simulators: an earn-buy-unlock loop, often with rebirths | [tycoons and simulators](references/genres/tycoons-and-simulators.md) |
| Obbies: stages and checkpoints | [obbies](references/genres/obbies.md) |
| Shooters and arena games: matches, maps and loadouts | [shooters](references/genres/shooters.md) |

When no file matches, build the pages from the same questions: what are the game's units of play,
what is each made of, where does each happen, who or what is met there, and what connects them.

## Dialogs And Text

- **Each thing the reader can click is defined once.** Put every named entity a page mentions —
  quest, side quest, character, creature, district, minigame — in the dashboard's `references`
  with its dialog, so every whole-word mention of its name on any page opens it and its picture is
  embedded once. An entity whose name another shares, such as two creatures called the same, gets
  its dialog inline on its tree entry instead, with a label telling them apart.
- **A dialog holds one section, so wrap its parts in a `tabs` section with a single tab**: the
  picture as `figures`, the facts as a non-collapsible `outline` whose group is named for what the
  entity is, and a small `diagram` of its neighbors. Inside a dialog its own name does not link;
  every other name does, so the neighbor diagram's nodes open the neighbors' dialogs. Leave the
  dialog's own node untoned: a toned node's thicker border clips its label.
- **A picture appears once on the page.** Where two dialogs would show the same capture, such as a
  boss's dialog and the quest that fights it, keep it in one and name the other in a facts row,
  which links to it.
- **Generated text is checked as text.** Sentences built from templates go wrong in the joins: an
  article chosen before the name it precedes ("a" before a vowel), a count beside a fixed plural
  ("1 other places"), a prefix doubled when the name already starts with it ("The The …"), and
  British spellings from the builder. Pick the article and plural from the value, and before
  rendering scan every string the spec holds for those joins; text quoted verbatim from the game
  keeps its own spelling.

## Pictures

A picture shows what each part is about: the quest's real characters with its props at its real
place, the round's arena mid-play, the stage from its checkpoint. The staging, capture, framing check
and reuse procedure is the [picture reference](references/pictures.md); read it before staging.

- **Reuse what is still true.** A manifest beside the spec fingerprints what produced each picture.
  A later run keeps every picture whose fingerprint is unchanged and recaptures only the changed,
  new and rejected ones; a picture the reader or the agent rejects is marked so in the manifest, and
  is recaptured whatever its fingerprint says.
- **Stage in the game.** In the game's isolated Studio runner, holding one of its editors as
  `roblox-studio` says, on a built copy of the place that is never saved, with the game's own
  progress route placing each scene's characters and props.
- **Frame the subject, not the avatar.** Check each view's framing before capturing it and reframe
  it in the same lease, as the reference says.
- **Draw what no scene shows** — a rule, a resource curve, a layout — as a clean SVG in the game's
  palette.
- **Size**: compress each capture to a JPEG about 900 px wide and 60 to 90 KB, and keep the rendered
  page well under `use-dashboard`'s size limit.
- When the captures run long, hand them to a worker under `subagent-matrix` with the scene file, the
  manifest, the runner lock procedure and the output folder; the page is delivered meanwhile.

## Render And Deliver

Render through `use-dashboard` with the spec, the page, the pictures and the manifest in the folder
`use-dashboard`'s **Render** gives a dashboard that outlives the session, one page path per dashboard so every re-render updates the page the reader already
has. Deliver through `use-dashboard`'s **Delivery** and its harness router. The dashboard's subject
outlives the session, so its title is the game's name with "Dashboard" and its topic is
"Game overview", and an update goes to the page already delivered under them. The page is finished
only once **Run Order**'s review has read it.

## Output

```markdown
**<Game> overview** — <link to the delivered page>

- Pages: <page names in order>
- Pictures: <n> reused, <n> recaptured (<n> changed, <n> new, <n> rejected), <n> drawn; not captured: <ids and reasons, or "none">
- Audit: <n> checks over <n> items; <n> findings
  - <quest or part>: <finding in one line>
- Source read: <repository>@<commit>
```

## Guardrails

- Never save, publish or commit the game's places or source from this skill.
- Stop only processes this skill started in the runner, and leave it idle when each lease ends.
