---
name: roblox-gameplay
description: Apply every time actively modifying a Roblox game, including mechanics, progression, rewards, controls, presentation, UI, and world content. Shape a fun, immediately understandable loop with frequent satisfying successes, rich readable feedback, meaningful progression suited to the game.
short_description: 'Apply every time actively modifying a Roblox game, including mechanics, progression, rewards, controls, presentation, UI, and world content.'
---

# Roblox gameplay and player enjoyment

## Dependencies

- `roblox-react` — apply for React-rendered UI.
- `roblox-building` — apply for maps and world content.
- `luau` — apply when reading or changing Luau.
- `roblox-studio` — apply for Studio playtests.

Apply this skill whenever actively modifying a game. Preserve the authorized scope, genre, established identity, and current gameplay contract. Use it to improve the affected player experience; it does not require adding a new feature, economy, pet system, or chart research to every code change.

## Make success clear and satisfying

Fit the rhythm of success to the requested genre, audience, and mood. Establish an understandable first action and a visible result early, then connect smaller achievements to meaningful longer goals. Fast rewards suit some games; quieter discovery, mastery, or social play can be equally intentional. Do not infer a fixed reward cadence or neurological effect from chart popularity.

Make successful actions legible through appropriately scaled visual, audio, motion, and progress feedback. Attribute the result to the player's action without obscuring targets, text, or threats. Bound concurrent effects, clean them up, and respect motion, camera-shake, contrast, and audio preferences. Keep frequent feedback short enough that the next action remains available.

## Reward real progress and preserve player understanding

Show what was earned and why using the game's actual rewards and progress states. Synchronize reward UI and effects with authoritative outcomes and prevent duplicates on retries, repeated clicks, or reconnects. A predicted hit animation must not claim an unconfirmed reward. Do not invent currency, misleading pickups, or progress that the game does not grant.

Tie near-term actions to clear medium-term goals and recognizable milestones. New powers, useful upgrades, newly accessible areas, personalization, and increased player skill can all make progress tangible. Vary tasks, pacing, encounters, and scenery while retaining a familiar core action. Avoid extending play only through repetitive waiting or arbitrary travel; preserve intentional anticipation, exploration, and tactical pauses where they make the genre enjoyable.

## Navigation and travel presentation

Make the current objective and next useful action easy to find without covering play. Use a HUD cue, in-world guidance, or another presentation suited to the game. Keep route cues attached to traversable paths, and suppress them when they would obstruct conversations, encounters, or modal screens. Preserve destination information through streaming and restore camera/input after failed transitions.

Travel choices should describe their actual destination and action. Reveal locked or unexplored destinations according to the game's progression contract, and preserve access the player has earned. Keep transition effects readable, bounded, and compatible with reduced motion.

## Variety, identity, and playing together

Give repeated play different decisions: tactical choices, complementary roles, discoveries, alternate approaches, or expressive customization that suits the game. Shared goals and visible contributions can reward cooperation before a large objective is complete. Support players who are learning or playing solo as well as groups. Comfortable controls and a world worth inhabiting matter alongside reward effects.

Treat design themes as hypotheses to test, not proof of what causes popularity. A tactical RPG, social roleplay game, and rapid collection game can be enjoyable for different reasons.

## Loading and arrival

Loading must feel intentional and safe. When the game suppresses its character during loading or pre-game presentation, prevent an unseen avatar from falling, dying, taking damage, or triggering gameplay behind the screen. Spawn or restore the character only when its destination and gameplay are ready. Preserve server authority and clean up interrupted loads, retries, and departures.

Choose a loading view suited to the available scene, with a still reduced-motion option. Do not expose empty routing space or load an entire world solely for decoration. Keep status and recovery controls readable; do not invent progress or delay entry to prolong an animation.

In the focused loading check, observe arrival through the handoff to gameplay, including a slow or failed load where relevant. Confirm the intended avatar state during loading, that no hidden gameplay or falling occurs, and that camera/input ownership returns correctly. Reuse that evidence during delivery instead of adding another walkthrough.

## NPCs and readable, animated characters

A walking NPC or creature needs visible locomotion that matches its movement, starts and stops with travel, and turns smoothly. Moving a rigid model along a path is not sufficient. Give flying or floating creatures deliberate locomotion appropriate to their anatomy, such as flapping, tentacle movement, or hovering. Preserve authored silhouettes and use rigged or intentionally articulated assets; verify actual visible motion in Play rather than assuming a running animation track proves it works.

Ground each walking or standing NPC against the actual authored surface using its rig and foot geometry, rather than a guessed root-height offset. Verify both feet from a low side view after appearance changes and through idle animation; neither floating nor feet sunk into paths is acceptable. Hovering must be an intentional creature design with appropriate motion.

Give stationary NPCs visible, restrained idle animation: breathing, a small weight shift, or an occasional glance suited to their character. Standing still must not look frozen. Reuse the rig's animation owner, vary poses where appropriate, keep feet planted, and clean up on streaming or despawn.

For face-to-face conversations, guide the player to a clear spot in front of the NPC using actual walking and walking animation before framing the dialogue. Use the NPC's facing or a named conversation anchor, validate the approach and final proximity on the server, and avoid walking through obstacles or other characters. Bound the approach, cancel it on death, departure, or interruption, and restore controls if it fails. Do not snap the player across the scene or frame a conversation from behind either speaker.

When the game uses overhead names or indicators, keep them readable during the interactions they serve. Add level, health, or interaction information only when it helps the player. Bound viewing distance, avoid labels through walls and dense overlaps, and clean up labels and animation ownership on despawn, streaming, and encounter transitions.

When a game has repeated creature types, share their definitions and lifecycle. Keep appearance, locomotion, statistics, and abilities in one owned contract rather than duplicating behavior per map. Creature-only abilities use the game's authoritative validation and must not become player actions through an unchecked client request.

## Companions when the game calls for them

When companions fit the game, give them understandable useful behavior and a clear role rather than adding them as a checklist feature. Show their contribution with readable actions and feedback, give them character, and keep them from blocking controls, navigation, performance, or the player's own sense of agency.

Fit companions to the genre, progression, and production stage. A popular feature is not automatically appropriate for every game.

## Validate fun at the affected scale

Play the affected loop through ordinary controls. Observe how quickly a beginner understands the next action, whether success is visible/audible, whether rewards agree with real state, and whether another attempt feels inviting. Check feedback at normal player pace and during rapid repeated successes, including overlap, audio buildup, cleanup, and performance. Keep stronger milestones distinct from routine hits.

When the work involves React-rendered UI, apply `roblox-react` for clarity and its scheduled repeated-click checks. Apply `roblox-building` for coherent, interesting worlds, `luau` for authority and cleanup, and `roblox-studio` for non-interfering Play tests. Static checks cannot establish enjoyment; short playtests cannot prove long-term retention.

## Learn from evidence

Do not invoke `study-games` during ordinary gameplay work; it runs only when the user directly requests that research. Keep transferable design principles here and dated observations in the invoking project's verification evidence. Distinguish passive inspection from actual play, label popularity hypotheses, and apply only ideas that fit the current game. Update canonical `.agents` sources only and leave mirrors to Agent Sync.
