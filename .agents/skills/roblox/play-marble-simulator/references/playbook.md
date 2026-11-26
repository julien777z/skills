# Marble Elimination Ultimate playbook

The `play-marble-simulator` skill's record of how the game works and how to win it. Every session
adds what it verifies, as `play-roblox-protocol`'s **Record What A Session Learns** says. Entries marked
*unconfirmed* were seen once and need a deliberate test.

## Servers And Joining

| Server | What it is | Can a link open it? |
|---|---|---|
| Lobby (the game's main place) | Waiting area with the leaderboards; groups players into the next match | Yes, by place, or a specific lobby server by its server ID |
| Match (a separate sub-place) | A private server running one match of many levels | No: a direct link fails with "You do not have permission to join this experience" (error 524) |

- **Joining the main place** lands in a random lobby, which moves you into a match within
  seconds. It reaches the named player only by chance.
- **Following the player works, even into a match in progress**, with the follow link
  `roblox-studio`'s runner reference's **Play a published experience** section gives. Joining
  mid-match counts the marble as eliminated ("Eliminated! Waiting for party."), so it watches until
  the match ends and then goes to the same lobby and the next match with the player.
- **Elimination moves you on unless you are in the player's party.** A marble eliminated alone goes
  to a new lobby and into a new match without the player. A marble in the player's match shows
  "Waiting for party" at every elimination and stays there; when the match ends the game moves both
  into the same lobby and then the same new match, with no further follow needed.
- Presence (`presence.roblox.com/v1/presence/users`) shows the player's current place and server
  ID; while they are in a match, the server ID is the match's.

## Controls

| Input | Effect | Status |
|---|---|---|
| none | The marble drops from the red arrow and falls on its own, but on water and open levels it hangs near the top while others finish | confirmed |
| hold W | Moves the marble down through water and open levels; alone it can still finish near the back | confirmed that it helps, not enough alone |
| hold W + tap Space | Finishes first or in the front group on most levels, though near last on a few | unconfirmed: Space not yet tested on its own |
| A / D | No visible effect: the marble's sideways drift did not follow the keys over 8 seconds | ruled out |
| Esc | Roblox menu with the People list, Leave and Respawn | confirmed |
| Tab | Shows no player list | confirmed |

- The yellow triangle marks your marble. The bar along the bottom fills with marbles in finish
  order from the left; the last marbles each level are eliminated.
- The match counter in the corner shows the level and total, such as `13/49`.

## Power-Ups And Coins

- Rows of item boxes across a level hand out a power-up to the marble that rolls through one. Its
  icon stacks at the right edge of the screen and it fires on its own; clicking the icon did
  nothing.
- **Black hole:** opens a vortex around your marble that pulls nearby marbles in and crushes the
  ones it swallows to a tiny size.
- **Bomb:** an explosion can go off in the power-up row or at the finish, scattering smoke and
  debris; who fires it and what it does to nearby marbles is not yet recorded.
- Other boxes seen: heart, drill, canister, fast-forward, magnet, weight, copy, spinner, sword
  and coin bag; their effects are not yet recorded.
- Yellow squares are coins ("Coins buy skins"). Every coin you earn, your friends in the server
  earn one too. No in-game shop has been found yet.

## Strategy

- A marble pinned against a side wall, or caught in a peg cluster near the top, falls to the back;
  levels with a side wall near the drop point are where the run is lost.
- **Funnel levels with a narrow exit** eliminate a marble left high in the funnel while the field
  drains through below.
- **Underwater levels** have finish lines at both top and bottom and slow every marble; a marble
  without input drifts and finishes last.
- **Spiky mine levels** place black spiked mines along the ramps; whether touching one costs the
  marble anything is not yet recorded.
- The pinball-table level is mostly luck: finishing places there vary from second to near last.
- The power-up row level is high risk: a marble can survive it on luck and still finish last.

## Pitfalls

- **The yellow button at the top right is the paid Donate button**; it opens a Robux purchase
  prompt.
- The green "+" button only opens Invite Friends.
