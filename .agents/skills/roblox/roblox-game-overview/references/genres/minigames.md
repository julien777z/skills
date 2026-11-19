# Minigame Collections

The `roblox-game-overview` skill's pages for a game made of short rounds the server picks between,
such as a party game that rotates through races, memory rounds and last-one-standing arenas.

## Pages

- **Minigames.** A `tree` grouped the way the game rotates them — by round type, map or player
  count — with one entry per minigame whose name opens its dialog. The dialog holds the round staged
  in the game (players mid-round in its arena, captured from the round's own camera), then its facts:
  the goal in one sentence, how a round starts and ends, its time limit and player range, how points
  or eliminations are scored, its settings and their values, the map it runs on, and what it awards.
  A `diagram` in the same dialog draws the round's flow from its phases in the source: lobby,
  countdown, play, sudden death, results.
- **Rotation.** How the server chooses the next round — weights, cooldowns, player-count limits —
  as a `table` per minigame, and a `diagram` of the round cycle from lobby to results and back.
- **Maps.** A `tree` of each arena with its picture, the minigames that use it and its spawn and
  hazard counts.
- **Rewards and progression.** What a round pays, what the currency buys and any level or pass
  track, on How to play.

## Consistency

- Every minigame the rotation names exists, and every one that exists can be chosen at some player
  count.
- Each round's instructions match its settings: a stated time limit, score target or team size
  equals the value the round runs with.
- Every map a minigame names exists and has the spawns and objects the minigame looks up.
- Rewards name items and currencies the game defines.
