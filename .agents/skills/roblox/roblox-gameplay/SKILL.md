---
name: roblox-gameplay
description: Apply every time actively modifying a Roblox game, including mechanics, progression, rewards, controls, presentation, UI, and world content. Shape a fun, immediately understandable loop with frequent satisfying successes, rich readable feedback, meaningful progression suited to the game.
short_description: 'Apply every time actively modifying a Roblox game, including mechanics, progression, rewards, controls, presentation, UI, and world content.'
---

# Roblox gameplay and player enjoyment

## Dependencies

- `roblox-react`
- `roblox-worldbuilding`
- `luau`

## Make success clear and satisfying

Apply this skill whenever actively modifying a game. Preserve the authorized scope, genre, established identity, and core loop; redesign what does not make sense as **Judge the game as a player meets it** says. Use it to improve the affected player experience; it does not require adding a new feature, economy, or pet system to every code change.

Fit the rhythm of success to the requested genre, audience, and mood. Establish an understandable first action and a visible result early, then connect smaller achievements to meaningful longer goals. Fast rewards suit some games; quieter discovery, mastery, or social play can be equally intentional. Do not infer a fixed reward cadence or neurological effect from chart popularity.

Make successful actions legible through appropriately scaled visual, audio, motion, and progress feedback. Attribute the result to the player's action without obscuring targets, text, or threats. Bound concurrent effects, clean them up, and respect motion, camera-shake, contrast, and audio preferences. Keep frequent feedback short enough that the next action remains available.

Where an action's quality can vary, tell the player how well it went, not only whether it worked: a short worded verdict, a grade or a medal for quality, attributed to the action that earned it. When an action fails, show why at the moment it fails, such as who or what caused it, which value fell short, or how close the attempt came, and, where the game allows another attempt, keep the way back to it clear and short. A failure the player can only work out by repeating it teaches slowly.

## First session

Put the first action before everything a new player does not yet need. Update notes, rules, daily rewards, events and offers wait until after the first success, or until the player opens them; a join that queues several panels before control delays the loop it is meant to introduce. When the game has an earn-and-spend economy and the work shapes its onboarding, carry the guidance through one whole cycle: the core action, its payout, and a first purchase or upgrade within reach of that payout. When the game guides a new player, lead that guidance all the way to the place the loop first pays, switched on by default for a new player, rather than stopping at the first menu step or hiding it behind an opt-in control. A new player stalls in the gap between the last guided step and the first earning spot, so check that the cue stays visible there, including when other players crowd the route.

Introduce each world mechanic before the player meets it unexplained: a health pickup, a gate, a board or an ingredient gets a short line from a character or a one-time hint the first time it is in reach. Dialogue and objective text name a character, place or threat only once the player can place it: from meeting it, from what the story has already shown or told them, or from the line itself.

Where the end of the guided chain, or of a unit such as a round, a stage, a level or a published creation, leaves the next step unclear, hand off to it: a short card or line naming the next goals or choices, such as continue, try the real mode, or return to the hub, or a cue the world or existing controls already give. A newly unlocked tool or area belongs in that handoff. The end of guidance should never read as silence.

## Judge the game as a player meets it

Every result is judged in the game as a player would meet it, whether you built it or a worker did: from a capture or a playtest, not from the brief, the code or a report. Ask of each thing in view whether it makes sense in this world, not only whether it is broken: an object reads as what it is meant to be, a room's furnishings fit its purpose, a character holds what it holds, a creature belongs in its area's level band, a label sits where it can be read, a rule agrees with the game's other rules. Something that reads wrong is fixed, whoever made it and whenever, even when no brief, check or request mentioned it.

**Something new on the screen is judged as a player meets it before it is built.** A marker, label, number, outline, arrow or overlay added to make something readable is first pictured in the scene where it would appear, such as an edited copy of a capture or a runtime toggle, at play distance, in a busy moment and beside everything else on screen. It is weighed against simpler routes the world already offers: the thing itself responding when the player points at or picks it, by lighting up, turning or lifting; a sound; a camera move; or a cue the existing HUD gives. Build the route that makes the moment clear with the least added to the screen. An addition that labels what the player could act on directly is the weaker option, such as a floating tag over each door naming the room behind it, where the room's light and furnishings seen through the doorway already say what it is.

Making the game read right is the agent's call: redesign an asset, a room, a placement, a balance value or a mechanic that does not make sense, including content built before the current task, and report each change with its captures, naming new behavior as new. This is the global product-choice boundary's game-design exception. Only a change to the game's core loop or genre, to anything players pay for, to security, disclosure or authorization, or to something the user decided goes to the user first.

## Reward real progress and preserve player understanding

Show what was earned and why using the game's actual rewards and progress states. Synchronize reward UI and effects with authoritative outcomes and prevent duplicates on retries, repeated clicks, or reconnects. A predicted hit animation must not claim an unconfirmed reward. Do not invent currency, misleading pickups, or progress that the game does not grant.

Tie near-term actions to clear medium-term goals and recognizable milestones. New powers, useful upgrades, newly accessible areas, personalization, and increased player skill can all make progress tangible. Vary tasks, pacing, encounters, and scenery while retaining a familiar core action. Avoid extending play only through repetitive waiting or arbitrary travel; preserve intentional anticipation, exploration, and tactical pauses where they make the genre enjoyable. Pace a leveled game through level design rather than level requirements on encounters: an encounter never refuses to start because of the player's level. Place each area's creatures and each fight in the level band a player naturally has when the game first sends them there, never above it, and let the curve and the amount of content set how long a world lasts; a check that fails when an area's creatures start above its arrival level keeps that true as content grows.

Show locked content where the player will use it, together with what unlocks it: a silhouetted collection entry, a padlocked slot, a grayed move labeled with the level or mastery that opens it, a mode showing the wins it needs, or a gate that states its requirement as a number the player can read from the approach. The condition shown must be the one the game actually checks. Content the progression contract keeps secret can stay hidden or appear as an unnamed slot.

Where the game allows it, let what the player did stay visible in the world: ground they cleared, a structure that grows as they invest in it, NPCs that react to what they chose, their name on what they own. The world then shows progress without a meter. Drive these changes from authoritative state, bound them, and keep them consistent on rejoin and streaming.

## Navigation and travel presentation

Make the current objective and next useful action easy to find without covering play. Use a HUD cue, in-world guidance, or another presentation suited to the game. Keep route cues attached to traversable paths, and suppress them when they would obstruct conversations, encounters, or modal screens. Preserve destination information through streaming and restore camera/input after failed transitions.

Travel choices should describe their actual destination and action. Reveal locked or unexplored destinations according to the game's progression contract, and preserve access the player has earned. Keep transition effects readable, bounded, and compatible with reduced motion.

## Variety, identity, and playing together

Give repeated play different decisions: tactical choices, complementary roles, discoveries, alternate approaches, or expressive customization that suits the game. Shared goals and visible contributions can reward cooperation before a large objective is complete. Support players who are learning or playing solo as well as groups. Where players can attack, block or take from each other, protect a newcomer's first attempts: a clearly bounded spawn area that really is safe, a short opening in which combat is off, or a protected moment after death. Comfortable controls and a world worth inhabiting matter alongside reward effects.

Treat design themes as hypotheses to test, not proof of what causes popularity. A tactical RPG, social roleplay game, and rapid collection game can be enjoyable for different reasons.

## Loading and arrival

Loading must feel intentional and safe. When the game suppresses its character during loading or pre-game presentation, prevent an unseen avatar from falling, dying, taking damage, or triggering gameplay behind the screen. Spawn or restore the character only when its destination and gameplay are ready. Preserve server authority and clean up interrupted loads, retries, and departures.

Walking through a door into an interior of the same place is entering a room, not travel: keep it seamless when the room is already there, use a quick fade through black, under a second, only when a teleport or camera cut needs hiding, and show a loading screen only when the room is still streaming in after a short wait. Choose a loading view suited to the available scene, with a still reduced-motion option. Do not expose empty routing space or load an entire world solely for decoration. Keep status and recovery controls readable; do not invent progress or delay entry to prolong an animation.

In the focused loading check, observe arrival through the handoff to gameplay, including a slow or failed load where relevant. Confirm the intended avatar state during loading, that no hidden gameplay or falling occurs, and that camera/input ownership returns correctly. Reuse that evidence during delivery instead of adding another walkthrough.

## NPCs and readable, animated characters

A walking NPC or creature needs visible locomotion that matches its movement, starts and stops with travel, and turns smoothly. Moving a rigid model along a path is not sufficient. Give flying or floating creatures deliberate locomotion appropriate to their anatomy, such as flapping, tentacle movement, or hovering. Preserve authored silhouettes and use rigged or intentionally articulated assets; verify actual visible motion in Play rather than assuming a running animation track proves it works. Anything that moves in view, such as a walker, an indicator following a target or a guide line, reads smooth on every client every frame: a position the server steps on a timer or replicates at network rate is drawn as jumps, so the client draws each mover along its path every frame from what the server decides, through one movement mechanism every mover of that kind shares.

Stand each NPC where its role puts it, on or beside the path a player arrives by or at its own place such as a doorway, stall, bench or garden, never alone in open ground, and face it toward the route the player approaches from, so the player meets its front and its prompt on that side. Ground each walking or standing NPC against the actual authored surface using its rig and foot geometry, rather than a guessed root-height offset. Verify both feet from a low side view after appearance changes and through idle animation; neither floating nor feet sunk into paths is acceptable. Hovering must be an intentional creature design with appropriate motion.

Give stationary NPCs visible, restrained idle animation: breathing, a small weight shift, or an occasional glance suited to their character. Standing still must not look frozen. Reuse the rig's animation owner, vary poses where appropriate, keep feet planted, and clean up on streaming or despawn. A prop a character carries, such as an umbrella, a book or a lantern, reads as held: pose the arm so the forearm comes forward and place the prop just in front of the palm, resting on it or hanging over the forearm, so it moves with the hand through idle and gestures. A prop passing through the middle of a blocky hand or floating beside a straight arm fails; verify it from the front and side in Play.

For face-to-face conversations, guide the player to a clear spot in front of the NPC using actual walking and walking animation before framing the dialogue. Use the NPC's facing or a named conversation anchor, validate the approach and final proximity on the server, and avoid walking through obstacles or other characters. Bound the approach, cancel it on death, departure, or interruption, and restore controls if it fails. Do not snap the player across the scene or frame a conversation from behind either speaker. A conversation opens with a line from the character the player spoke to, and the camera holds one framing while the same speaker talks, moving only when the speaker changes. A character who appears only for a scene, such as an antagonist's entrance, arrives for it and leaves visibly when it ends, carries no prompt the player can walk up to, and returns only when a later scene stages it.

When the game uses overhead names or indicators, keep them readable during the interactions they serve. Add level, health, or interaction information only when it helps the player. Hide overhead names while a conversation shows its speaker's name. Bound viewing distance, avoid labels through walls and dense overlaps, and clean up labels and animation ownership on despawn, streaming, and encounter transitions.

When a game has repeated creature types, share their definitions and lifecycle. Keep appearance, locomotion, statistics, and abilities in one owned contract rather than duplicating behavior per map. Creature-only abilities use the game's authoritative validation and must not become player actions through an unchecked client request.

## Companions when the game calls for them

When companions fit the game, give them understandable useful behavior and a clear role rather than adding them as a checklist feature. Show their contribution with readable actions and feedback, give them character, and keep them from blocking controls, navigation, performance, or the player's own sense of agency.

Fit companions to the genre, progression, and production stage. A popular feature is not automatically appropriate for every game.

## Paid offers

When a game sells items, a paid action never looks like free progression or help. Give paid controls their own shape and a price label, not only a color or a small badge. Keep them off the routes and controls that guidance sends a new player through. A help, hint or "+" button either does what its label promises for free or shows its cost before it is pressed.

## Validate fun at the affected scale

Play the affected loop through ordinary controls. Observe how quickly a beginner understands the next action, whether success is visible/audible, whether rewards agree with real state, and whether another attempt feels inviting. Check feedback at normal player pace and during rapid repeated successes, including overlap, audio buildup, cleanup, and performance. Keep stronger milestones distinct from routine hits.

When the work involves React-rendered UI, apply `roblox-react` for clarity and its scheduled repeated-click checks. Apply `roblox-worldbuilding` for maps and world content and `luau` when reading or changing Luau, including authority and cleanup. Return non-interfering Play tests to the caller. Static checks cannot establish enjoyment; short playtests cannot prove long-term retention.

## Learn from evidence

Keep only transferable design principles here; dated observations stay in the records that hold them. Distinguish passive inspection from actual play, label popularity hypotheses, and apply only ideas that fit the current game. Update canonical `.agents` sources only and leave mirrors to Agent Sync.
