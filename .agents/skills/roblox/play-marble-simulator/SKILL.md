---
name: play-marble-simulator
description: Play the public Roblox marble game Marble Elimination Ultimate (a marble race where the last marbles each level are eliminated) in the isolated Roblox runner, alone or in the same server as a Roblox player the user names, playing to win and collecting the game's coins, and sending screenshots as play goes on. Use when the user asks to play, join, follow or watch someone in that game, or to keep playing it until they say stop; and whenever a session playing it learns something new about joining, controls, levels, coins or strategy, which is added to this skill's playbook.
---

# Play Marble Simulator

## Dependencies

- `play-roblox-protocol`
- `roblox-studio`

Run `play-roblox-protocol` for every session; this skill supplies its game.

## The Game

Marble Elimination Ultimate: a lobby place that groups players into matches, each match a private
server no link can open, so the way into a named player's match is following them. Read
[the playbook](references/playbook.md#servers-and-joining) before the first join: it says how the
game moves players between servers and how to stay in the player's party.

## Objective

Survive every level of the match and finish each one as high as possible, ahead of the named player
and every other marble. The last marbles each level are eliminated, and the bar along the bottom
shows the finish order.

## Secondary Goals

Coins, which buy skins: collect the ones on the marble's line down a level where they cost it no
places, and claim every coin the game awards between levels and matches. The
[playbook](references/playbook.md#power-ups-and-coins) records how coins are earned and the
power-ups worth rolling through.

## Playing

Use the [playbook](references/playbook.md#controls)'s controls, strategy and pitfalls. Open the
People list only between levels or while eliminated, never mid-drop: an open menu costs the marble
its place.

## Captures And Report

Add to the protocol's lists: each level's result showing the finish order against the named player,
each power-up picked up or fired, each elimination, and each match result.

## Playbook

Learnings go into [the playbook](references/playbook.md) as the protocol's **Record What A Session
Learns** says, in the section for their kind: servers and joining, controls, power-ups and coins,
strategy, or pitfalls.
