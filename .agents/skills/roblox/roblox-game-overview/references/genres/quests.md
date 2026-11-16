# Quest and Story Games

The `roblox-game-overview` skill's pages for a game played through quests: a main story told in
beats, side quests given by characters, places to travel between and creatures or rivals to beat —
such as a lighthouse adventure whose keeper sends the player along the coast after a lost lens.

## Pages

- **Story.** A `tree` of chapter, then quest, then step: a quest entry carries its kind as a tag
  (talk, duel, collect, use), its experience as a figure, its district as meta and a status pill
  where the audit found something; its children are what the quest asks, such as each piece to
  collect with the district it lies in, or the foe a duel fields and the companion each further
  player brings. A `diagram` named for the story map draws every quest in order, each side quest
  from the quest or side quest that unlocks it, and each dungeon or area from the step that opens it,
  toned and given a legend for side quests and places. A setups-and-payoffs `outline` follows when
  the story's design document lists them, with design ids replaced by the quests' names.
- **Each quest's dialog**, opened from its name anywhere on the page, holds in one section:
  - the quest staged in the game;
  - what happens, from the story document's summary where one exists, and the quest's own text;
  - who gives it and who is on stage while it is current, read from the staging that places
    characters for that progress;
  - where it happens, as world, district and place, from the game's own area lookup;
  - what it asks and what it rewards, including the spells or items it teaches or gives;
  - what unlocks it and what it unlocks;
  - the audit's findings for it;
  - a source link to the quest's definition;
  - a small `diagram` of the quest between the one before and the one after, with every side quest,
    spell or place it unlocks; each node is named for its quest, so it opens that quest's dialog.
- **Worlds.** A `tree` of world, then district, then place: rooms, shops and dungeons behind doors,
  landmarks the story uses, and lore spots with their text. A district's dialog
  holds its view from above and lists the characters standing there, the quests and side quests met
  there and the creatures that roam there; a place's dialog holds its interior and, for a shop, its
  stock, for a dungeon its rooms, weekly reward and chest.
- **Side quests.** A `tree` by district, then chain, then step. The chain's dialog carries its
  picture, giver, unlock, steps, final reward and what it opens; each step's dialog carries the same
  facts as a main quest's, with its own picture where one was staged for it.
- **Characters.** A `tree` by district, each name opening a dialog with a portrait, role, look and
  voice from the cast list, where they stand, how many places the story moves them to, any shop
  they keep, and the quests they give or appear in.
- **Creatures.** A `tree` of roaming species, rare variants and unique foes, each with its rank or
  tier as a tag and its health as a figure; its dialog holds its picture in a fight, where it
  fights, its levels, each move it uses with damage, target and accuracy, any signature move, and
  what a win pays.

## Consistency

| Check | What it compares |
| --- | --- |
| Places | Every quest and step's target resolves to a point, encounter, collection or interaction; the area that target falls in matches any place word in the quest's objective and text. |
| Givers | Every side quest's giver is a speaking character with a point, present when the chain is offered, standing in the district the chain belongs to. |
| Gates | Unlocks name real quests and chains with no cycle; each door or area opens on the step that sends the player in, or on a prerequisite before it; staged fights and quest targets name each other. |
| Rewards | Every item, spell and currency a quest, chain, shop, level or collection gives is defined. |
| Reachable | Every chain unlocks from a quest the story reaches, every step's conversation exists and every collection piece is placed. |
| Order | The story document lists the same beats as the game, in order, with the same kind, target and reward; every staging window opens before it closes; the document's totals match the quests. |

A place word is matched against the set of areas it can name, such as a district word against the
district and the rooms inside it; a text that names several places passes when any of them holds
the target. Read every flagged quest's text and the character's lines before calling it a finding:
a word can name the route rather than the destination. A finding's detail quotes the text, states
where the game puts the target in the area names a player sees, and adds what makes it matter, such
as a dialogue line repeating the claim or a district of the same name elsewhere.
