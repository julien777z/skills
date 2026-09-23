---
name: roblox-gameplay
description: Apply every time actively modifying a Roblox game, including mechanics, progression, rewards, controls, presentation, UI, and world content. Shape a fun, immediately understandable loop with frequent satisfying successes, rich readable feedback, meaningful progression, and useful companions when appropriate to the game's stage.
---

# Roblox gameplay and player enjoyment

Apply this skill whenever actively modifying a game. Preserve the authorized scope, genre, established identity, and current gameplay contract. Use it to improve the affected player experience; it does not require adding a new feature, economy, pet system, or chart research to every code change.

## Make success frequent and satisfying

Design for the user's requested **high-dopamine** experience: frequent moments of achievement, satisfying controls, and a clear desire to try the next action. Treat that phrase as a design goal for enjoyment, not a measured neurological claim. Put an understandable action and attainable first success early. Offer many quick opportunities for small wins within a larger goal, with meaningful choices, mastery, variety, discovery, or cooperation to sustain the loop.

Prefer generous, layered feedback when the player does something successfully. Combine an immediate visual response with a short sound, purposeful motion, and clear reward/progress UI. Make the result attributable to the player's action. A hit, successful defense, collection, solved step, defeated enemy, completed quest, and major milestone can each have a distinct scale of celebration. Small successes should happen often; reserve the strongest effect for larger achievements. Keep repeated rewards quick and allow the next action without waiting through long celebration sequences.

For example, a pet-assisted block game can let companions fire readable beams, break blocks in rapid succession, and send a burst of coin particles toward the player with a pickup sound and a matching counter change. The reusable lesson is the short action → visible success → reward → next opportunity loop, plus helpful companions. Do not transplant its blocks, coins, or pets into an unrelated game merely to copy the surface presentation.

Make feedback rich without obscuring targets, upcoming threats, card text, or the world. Layer a few well-chosen effects rather than adding indiscriminate particle spam. Bound concurrent particles/sounds, pool or clean up temporary visuals, and scale intensity for repeated events. Respect reduced motion, camera-shake settings, readable contrast, and audio balance. A quiet game can still have precise, rewarding feedback suited to its mood.

## Reward real progress and preserve player understanding

Show what was earned and why: a visible `+{XP}`, a collection count, a new ability, a completed objective, or another actual reward. Synchronize reward UI and effects with authoritative outcomes and prevent duplicates on retries, repeated clicks, or reconnects. A predicted hit animation must not claim an unconfirmed reward. Do not invent currency, misleading pickups, or progress that the game does not grant.

Tie near-term actions to clear medium-term goals and recognizable milestones. New powers, useful upgrades, newly accessible areas, personalization, and increased player skill can all make progress tangible. Vary tasks, pacing, encounters, and scenery while retaining a familiar core action. Avoid extending play only through repetitive waiting or arbitrary travel; preserve intentional anticipation, exploration, and tactical pauses where they make the genre enjoyable.

## Navigation and travel presentation

Keep the current goal easy to notice without hiding the action; favor a slim, persistent next-action strip near the top center when that fits the game's HUD. Briefly expand chapter details when the objective changes, then collapse them; let players reopen them by clicking or tapping. Keep the concrete next action and useful progress visible after collapse rather than hiding the reminder or leaving only a story title. Put physical route guidance in the world when it helps players connect the direction to the environment: use a translucent arrow with a clear head and tail, follow valid routes, and suppress it during conversations, encounters, and modal screens. Keep destination information stable when scenery streams out.

Travel choices should describe the action a click performs. Where unexplored worlds are meant to remain hidden, list only unlocked destinations; keep previously completed worlds available. Avoid redundant reassurance about ordinary expected behavior. Prefer a bounded world-space portal or vortex effect when travel belongs to the scene, keep status readable, respect reduced motion, and restore camera/input on failure.

## Variety, identity, and playing together

Give repeated play different decisions: tactical choices, complementary roles, discoveries, alternate approaches, or expressive customization that suits the game. Shared goals and visible contributions can reward cooperation before a large objective is complete. Support players who are learning or playing solo as well as groups. Comfortable controls and a world worth inhabiting matter alongside reward effects.

Treat design themes as hypotheses to test, not proof of what causes popularity. A tactical RPG, social roleplay game, and rapid collection game can be enjoyable for different reasons.

## Loading and arrival

Loading must feel intentional and safe. Keep the player's character out of Workspace throughout loading and pre-game presentation; do not let a hidden avatar fall, die, respawn, take damage, or trigger gameplay behind the screen. Prevent automatic spawning before initialization can yield, and handle any character already created. Spawn or restore the character only when its destination and gameplay are ready. Preserve server authority and clean up interrupted loads, retries, and departures.

Where a suitable map is available, prefer a slow, deliberate camera orbit around an authored scenic focus while loading. Keep the camera independent of the character and respect reduced motion with a still view. An empty routing place should use a polished opaque backdrop rather than expose empty space or load an entire world solely for decoration. Keep status and recovery controls readable; do not invent progress or delay entry to prolong an animation.

In the focused loading check, observe arrival through the handoff to gameplay, including a slow or failed load where relevant. Confirm no avatar is in Workspace during loading, no death or falling appears, and camera/input ownership returns correctly. Reuse that evidence during delivery instead of adding another walkthrough.

## NPCs and readable, animated characters

Every walking NPC or monster needs a visible walking animation that matches its movement, starts and stops with travel, and turns smoothly. Moving a rigid model along a path is not sufficient. Give flying or floating creatures deliberate locomotion appropriate to their anatomy, such as flapping, tentacle movement, or hovering. Preserve authored silhouettes and use rigged or intentionally articulated assets; verify actual visible motion in Play rather than assuming a running animation track proves it works.

Ground each walking or standing NPC against the actual authored surface using its rig and foot geometry, rather than a guessed root-height offset. Verify both feet from a low side view after appearance changes and through idle animation; neither floating nor feet sunk into paths is acceptable. Hovering must be an intentional creature design with appropriate motion.

Give stationary NPCs visible, restrained idle animation: breathing, a small weight shift, or an occasional glance suited to their character. Standing still must not look frozen. Reuse the rig's animation owner, vary poses where appropriate, keep feet planted, and clean up on streaming or despawn.

For face-to-face conversations, guide the player to a clear spot in front of the NPC using actual walking and walking animation before framing the dialogue. Use the NPC's facing or a named conversation anchor, validate the approach and final proximity on the server, and avoid walking through obstacles or other characters. Bound the approach, cancel it on death, departure, or interruption, and restore controls if it fails. Do not snap the player across the scene or frame a conversation from behind either speaker.

NPCs and monsters need readable overhead names during exploration as well as encounters. Add optional level, health, or interaction information only when it helps the player. Bound viewing distance, avoid labels through walls and dense overlaps, and clean up labels and animation ownership on despawn, streaming, and encounter transitions.

Share monster definitions and a common creation/lifecycle path. Definitions own health, spell loadouts, appearance, and locomotion; map populations instantiate those definitions rather than duplicating behavior scripts. Monster spells should use the same validation, targeting, costs, effects, and resolution rules as player spells, while a separate server-authorized loadout keeps creature-only abilities out of player collections. Test both legal monster choices and rejection of player attempts to cast their spells.

## Useful pets and companions

Pets can add attachment, personalization, collection goals, and visible assistance. Prefer companions with understandable helpful behavior—gathering, combat support, utility, or another meaningful role—over a decorative checklist feature. Show their contribution with readable actions and feedback, give them character, and keep them from blocking controls, navigation, performance, or the player's own sense of agency.

Fit companions to the genre, progression, and production stage. A popular feature is not automatically appropriate for every game.

## Validate fun at the affected scale

Play the affected loop through ordinary controls. Observe how quickly a beginner understands the next action, whether success is visible/audible, whether rewards agree with real state, and whether another attempt feels inviting. Check feedback at normal player pace and during rapid repeated successes, including overlap, audio buildup, cleanup, and performance. Keep stronger milestones distinct from routine hits.

Apply [roblox-react](../roblox-react/SKILL.md) for UI clarity and its scheduled repeated-click checks, [roblox-building](../roblox-building/SKILL.md) for coherent, interesting worlds, [luau](../luau/SKILL.md) for authority and cleanup, and [roblox-studio](../roblox-studio/SKILL.md) for non-interfering Play tests. Static checks cannot establish enjoyment; short playtests cannot prove long-term retention.

## Learn from evidence

Use [study-games](../study-games/SKILL.md) only when the user explicitly invokes research. Its main agent synthesizes independent game notes into this skill. Keep permanent, transferable themes in this skill. Archive dated studies, ranks, per-game observations, sources, and limits under [references/chart-studies/](references/chart-studies/), distinguish passive inspection from actual play, and label hypotheses about popularity. Adopt transferable principles that fit the current game, not a list of copied trending features. Update canonical `.agents` sources only and leave mirrors to Agent Sync.
