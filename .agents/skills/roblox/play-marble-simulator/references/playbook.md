# Marble Elimination Ultimate playbook

The `play-marble-simulator` skill's record of how the game works and how to win it. Every session
adds what it verifies, as that skill's **Recording What A Session Learns** says. Entries marked
*unconfirmed* were seen once and need a deliberate test.

## Servers And Joining

| Server | What it is | Can a link open it? |
|---|---|---|
| Lobby (the game's main place) | Waiting area with the leaderboards; groups players into the next match | Yes, by place, or a specific lobby server by its server ID |
| Match (a separate sub-place) | A private server running one match of many levels | No: a direct link fails with "You do not have permission to join this experience" (error 524) |

- **Joining the main place** lands in a random lobby, which moves you into a match within
  seconds. It reaches the named player only by chance.
- **Following the player works, even into a match in progress**: in the player app run
  `open "roblox://experiences/start?userId=<their user ID>"`. Joining mid-match counts the marble
  as eliminated ("Eliminated! Waiting for party."), so it watches until the match ends and then
  goes to the same lobby and the next match with the player.
- **Elimination moves you on unless you are in the player's party.** Eliminated alone, the game
  sent the marble to a new lobby and into a new match without the player. Once the marble was in
  the player's match, every elimination showed "Waiting for party" and kept it there, and when the
  match ended the game moved both into the same lobby and then the same new match, with no
  further follow needed.
- **The player log in the runner records every move**: each join and teleport names its place and
  server ID, so it shows which server the marble is in and why it changed. On macOS it is the
  newest `*Player*.log` in the account's Roblox logs folder.
- Presence (`presence.roblox.com/v1/presence/users`) shows the player's current place and server
  ID; while they are in a match, the server ID is the match's.

## Controls

| Input | Effect | Status |
|---|---|---|
| none | The marble drops from the red arrow and falls on its own, but on water and open levels it hangs near the top while others finish | confirmed |
| hold W | Moves the marble down through water and open levels; alone it still finished near the back on several levels | confirmed that it helps, not enough alone |
| hold W + tap Space | Finished first or in the front group on most levels across two matches, though near last on a few | unconfirmed: Space not yet tested on its own |
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

- Hold W through the whole drop and tap Space; W alone was not enough to stay in the front group.
- A marble pinned against a side wall, or caught in a peg cluster near the top, falls to the back;
  levels with a side wall near the drop point are where the run is lost.
- **Funnel levels with a narrow exit** eliminate a marble left high in the funnel while the field
  drains through below.
- **Underwater levels** have finish lines at both top and bottom and slow every marble; a marble
  without input drifts and finishes last.
- **Spiky mine levels** place black spiked mines along the ramps; whether touching one costs the
  marble anything is not yet recorded.
- The pinball-table level is mostly luck: finishes there ranged from second to near last.
- Opening any menu during a level cost the marble its place and, once, the match.
- The power-up row level is high risk: a marble that survived on luck there finished last.

## Pitfalls

- **The yellow button at the top right is a paid Donate button** that opens a Robux purchase
  prompt. Cancel the prompt; never confirm it.
- The green "+" button only opens Invite Friends.
- A macOS "Software Update Available" banner in a runner guest covers the top-right corner of
  captures; it does not affect play.
