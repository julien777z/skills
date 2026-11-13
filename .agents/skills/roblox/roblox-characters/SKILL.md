---
name: roblox-characters
description: Apply whenever a Roblox character is planned, created, modified, imported, placed, animated, or playtested — NPCs, enemies and other creatures, pets and companions, and the player's avatar — including avatar overrides, accessories and faces, rigs, skinning and bones, idle, procedural and action animation, locomotion, NPC conversations, overhead names, and character collision. Require visible motion that matches movement, grounded and purposeful placement, readable presentation, and motion verified in Play.
short_description: 'Make Roblox NPCs, creatures, and avatars look, move, and present convincingly.'
---

# Roblox characters

## Dependencies

- `luau`
- `roblox-worldbuilding`

## Characters a player meets

Apply this skill to every character a player sees: NPCs, enemies and other creatures, pets and companions, and the player's own avatar. Preserve authored silhouettes and the game's established characters. Override the player's avatar only when the product calls for it, because it was requested or the game requires it; otherwise preserve the existing character behavior and appearance.

Model and import a character's mesh through `roblox-worldbuilding`'s Blender pipeline, apply `luau` when reading or changing character code, and return imports, uploads, editor operations and Play sessions to the caller. Read [rigs, avatars and animation](references/rigs-and-animation.md), this skill's reference for rig-level work, before building or overriding an avatar, fitting accessories or a face, writing procedural poses or action presentation, rigging a creature for import, or changing character collision or a mode that holds a character still.

## Locomotion

A walking NPC or creature needs visible locomotion that matches its movement, starts and stops with travel, and turns smoothly. Moving a rigid model along a path is not sufficient. Give flying or floating creatures deliberate locomotion appropriate to their anatomy, such as flapping, tentacle movement, or hovering. Use rigged or intentionally articulated assets.

## Placement and idle

Stand each NPC where its role puts it, on or beside the path a player arrives by or at its own place such as a doorway, stall, bench or garden, never alone in open ground, and face it toward the route the player approaches from, so the player meets its front and its prompt on that side. Ground each walking or standing NPC against the actual authored surface using its rig and foot geometry, rather than a guessed root-height offset. Verify both feet from a low side view after appearance changes and through idle animation; neither floating nor feet sunk into paths is acceptable, unless hovering is the creature's intentional design with the motion **Locomotion** describes.

Give stationary NPCs visible, restrained idle animation: breathing, a small weight shift, or an occasional glance suited to their character. Standing still must not look frozen. Reuse the rig's animation owner, vary poses where appropriate, and keep feet planted. A prop a character carries, such as an umbrella, a book or a lantern, reads as held: pose the arm so the forearm comes forward and place the prop just in front of the palm, resting on it or hanging over the forearm, so it moves with the hand through idle and gestures. A prop passing through the middle of a blocky hand or floating beside a straight arm fails; verify it from the front and side in Play.

## Conversations and staged appearances

For face-to-face conversations, guide the player to a clear spot in front of the NPC using actual walking and walking animation before framing the dialogue. Use the NPC's facing or a named conversation anchor, validate the approach and final proximity on the server, and avoid walking through obstacles or other characters. Bound the approach, cancel it on death, departure, or interruption, and restore controls if it fails. Do not snap the player across the scene or frame a conversation from behind either speaker. A conversation opens with a line from the character the player spoke to, and the camera holds one framing while the same speaker talks, moving only when the speaker changes. A character who appears only for a scene, such as an antagonist's entrance, arrives for it and leaves visibly when it ends, carries no prompt the player can walk up to, and returns only when a later scene stages it.

## Overhead names

When the game uses overhead names or indicators, keep them readable during the interactions they serve. Add level, health, or interaction information only when it helps the player. Hide overhead names while a conversation shows its speaker's name. Bound viewing distance and avoid labels through walls and dense overlaps.

## Shared creature definitions

When a game has repeated creature types, share their definitions and lifecycle. Keep appearance, locomotion, statistics, and abilities in one owned contract rather than duplicating behavior per map. Creature-only abilities use the game's authoritative validation and must not become player actions through an unchecked client request.

## Lifecycle and verification

Give each character's animation tracks, procedural connections and overhead labels one owner. Restore poses and clean them up after completion, despawn, streaming, encounter transitions and character replacement.

Judge motion from what Play shows. A running animation track, a non-erroring animation call or a successful `Bone.Transform` assignment is not evidence that anything moved: measure visible joint motion and limb deformation. Verify in Play the rig type, proportions and body scale, attachments, accessories, face, collisions, mass, normal locomotion and action animations.
