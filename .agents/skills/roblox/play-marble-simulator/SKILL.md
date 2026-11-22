---
name: play-marble-simulator
description: Play the public Roblox marble game Marble Elimination Ultimate (a marble race where the last marbles each level are eliminated) in the isolated Roblox runner, alone or in the same server as a Roblox player the user names, playing to win and sending screenshots as play goes on. Use when the user asks to play, join, follow or watch someone in that game, or to keep playing it until they say stop; and whenever a session playing it learns something new about joining, controls, levels or strategy, which is added to this skill's playbook.
---

# Play Marble Simulator

## Dependencies

- `roblox-studio`
- `share-media`
- `subagent-matrix`
- `edit-skill`

## Setup

1. **Find the game and the player.** Look the game up by name through Roblox's search, since the
   user may misspell it, and resolve a named player to a user ID through Roblox's users API. Read
   the player's presence: it names the place and server they are in right now.
2. **Play in the isolated runner, never the user's desktop**: in a game VM's guest, as
   `roblox-studio`'s testing reference's **Play a published experience** section describes,
   adding the player app there as that reference says when it is missing. Check the signed-in
   account from a capture after launch; a sign-in page goes to the user as `roblox-studio`'s
   authentication section says. Never touch the runner's Studio editors.
3. **Delegate play to one worker** chosen under `subagent-matrix`, briefed with this skill, the
   player to join and the capture folder. The delegating agent forwards each capture as it lands,
   after reading it, as `share-media` says, and relays the worker's findings.

## Joining A Player

Read [the playbook](references/playbook.md#servers-and-joining) before the first join: the game
puts each match on a private server no link can open, so the route that works is following the
player, and the playbook says how the game moves players between servers.

- **Staying with the named player outranks finishing a match.** When a People-list check shows the
  player missing, leave and follow them again at once; a match they are not in is not played.
- A follow the game refuses is reported to the user with its capture, never replaced by joining a
  random server.
- Check the People list only between levels or while eliminated, never mid-drop: an open menu
  costs the marble its place.

## Playing

Play every level to finish first, with the controls, strategy and hazards the
[playbook](references/playbook.md#controls) records, and keep testing what the playbook marks
unconfirmed with a capture before and after.

- Never press the paid Donate button or anything that opens a Robux purchase; cancel any purchase
  prompt that appears. Coins the game awards are free to spend in-game.
- Keep playing match after match until the user says to stop, starting a new worker session when
  one ends and leaving the player in the game between them.
- **When the user says stop**, end play as `roblox-studio`'s **Play a published experience**
  section says.

## Captures

Capture each notable moment: the join with the People list showing the player, each level result
showing the finish order against the named player, each power-up picked up or fired, each
elimination, and each match result. Name captures in order with a short description, read each one
before keeping it, and drop blank or duplicate frames.

## Recording What A Session Learns

**Every verified learning goes into the playbook through `edit-skill` during the session that
found it**, the playing worker reporting each one and the delegating agent recording it: a new
control or a ruled-out one, a level's hazard and the line that beats it, a power-up's effect, a
change in how the game moves players between servers, a pitfall. Write it as the general fact, mark
anything seen once as unconfirmed, and replace an entry a later session disproves rather than
adding a second one beside it.

## Output

Report as the session runs and at its end:

- whether the agent is in the named player's server, with the People-list capture;
- each level's finish order against the named player, with its capture;
- the controls and strategy used, and what the session added to the playbook;
- anything that failed, and what the next session starts from.
