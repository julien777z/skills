# Game brief

The `roblox-studio` skill's input contract for building a new game from an approved idea. A game
brief is one JSON file of product facts: what the game is, who it is for, what players do and
what it must and must not include. It holds no implementation: no scripts, services, data models,
instance names or technical architecture. Those are the builder's decisions.

## Fields

Every field is required unless marked optional. Text fields are plain sentences a designer would
write; lists hold at least one entry.

| Field | Holds |
| --- | --- |
| `brief_version` | `1` |
| `title` | The working title. |
| `logline` | One sentence on what the game is. |
| `genre` | `{primary, secondary?}`: the Roblox genre closest to the game, and any second genre whose rhythm it borrows. |
| `audience` | `{ages, players, devices, session_minutes}`: the age range, who they are and how they play (solo, friends, strangers), the devices to support, and a typical session length. |
| `tone` | The mood the game keeps, and what it never becomes. |
| `player_fantasy` | Who the player gets to be. |
| `core_loop` | `[{step, detail}]`: what players do, in order, until the loop repeats. |
| `modes` | Optional. `[{name, detail, when}]`: rounds, events or modes beside the core loop, and when they happen. |
| `story` | Optional. `{premise, player_role, characters: [{name, role}], arc: [{chapter, goal}], ending}`; omitted when the game has no story. |
| `world` | `{setting, areas: [{name, purpose, landmark}], look}`: where the game happens, its areas in the order players reach them, and its visual direction. |
| `first_session` | `[step]`: what a new player sees and does from spawn until play becomes their own. |
| `progression` | `{short_term, medium_term, long_term, collection?}`: goals at each horizon, and any collection or index. |
| `social` | `{party_size, interaction, solo}`: how players play together, what they can and cannot do to each other, and how solo play works. |
| `monetization` | `{model, offers, rules}`: what the first release sells, and the rules paid content follows. |
| `accessibility` | `[requirement]`. |
| `saving` | `[rule]`: what a player keeps between sessions and what happens when a save or load fails. |
| `scope` | `{first_release, later, excluded}`: what the first playable release contains, what comes after it, and what the game never includes. |
| `success_signals` | `[signal]`: observable outcomes that show the game works for its audience. |
| `competitors` | `[{name, url, overlap, difference}]`: games a player of this one would otherwise play, what each shares with it and how this game differs. |
| `open_questions` | `[question]`: product choices the approval left open, or `[]`. |
| `evidence` | Optional. `[{claim, source}]`: what supports the design, such as a study's patterns. |

## Building from a brief

Read the whole brief before planning. Its product facts are the approved scope: build what
`scope.first_release` names, follow `tone`, `audience`, `social`, `monetization` and
`accessibility` as requirements, and apply the gameplay, interface and world guidance the
skill's dependencies hold to each part. `scope.later` and `scope.excluded` are not built.
Every implementation choice is the builder's. An `open_questions` entry, or a product fact the
first release needs that the brief leaves unstated, is a product choice: put it to the user
rather than deciding it.
