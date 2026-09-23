# Asset and avatar standards

Apply these standards to the game's genre and the requested change. They are not instructions to give every game fantasy scenery, quests, or custom avatars.

For Blender and environmental assets, apply [roblox-building](../../roblox-building/SKILL.md). Its [import reference](../../roblox-building/references/blender-assets.md) owns the reusable pipeline.

## Avatars and animation

Only override the player's avatar when the product calls for it. Otherwise preserve the existing character behavior and appearance.

For an override, start with an appropriate Roblox body package/HumanoidDescription and compatible catalog hats/accessories. Use a coherent silhouette and controlled proportions; fit original Blender details to that body. Do not compensate for poor fitting with giant blocky shells. Do not assume permission to purchase an accessory or spend Robux.

- Verify the rig type, attachments, body scale, collisions, mass, face, accessories, and normal locomotion. NPCs can use compatible rigs with deliberate variations.
- Inspect the bounds of off-world preview rigs. `Humanoid:AddAccessory()` may leave an accessory at its original position outside Workspace, causing viewport fitting to shrink the whole character. Align matching attachments and create/verify the accessory weld before fitting the camera. Prebake validated templates when it avoids runtime asset loading and keeps previews consistent with equipped characters.
- Preserve recognizable facial/skin appearance where compatible. A catalog face product ID is not necessarily an image content ID: inspect the loaded asset's actual Decal/Texture instead of assigning the product ID directly as a texture. Never execute scripts from an imported face/accessory model.
- Current R15 assets may use AnimationConstraint-based joints rather than only Motor6D. Inspect the actual rig before writing procedural poses. Measure visible joint motion; a non-erroring animation call is insufficient evidence.
- Layer procedural motion in appropriate animation/simulation phases so the default animator does not overwrite it immediately. Restore poses and clean connections after completion or character replacement.
- Procedural idle/cast/hit/victory or other game-specific motion is an option when suitable. Do not describe those as uploaded animation clips. If uploaded clips are required, publish them under the correct owner and verify their IDs/permissions in the live experience.
- Enemy action, impact, and defeat presentation should be readable and timed to the authoritative events. Client presentation completion must never decide whether server gameplay can proceed.

## Character collision and motion pitfalls

Roblox Humanoids may re-enable torso collisions after spawning even if every NPC part was set noncollidable in the editor; disabling `EvaluateStateMachine` did not solve the observed case. An explicit NPC collision group with the player group's collision disabled kept an anchored dialogue character from blocking movement. Apply it to runtime and serialized NPCs, and verify by walking past them.

Anchoring a player and setting `WalkSpeed=0` do not necessarily stop the running animation or clear the last movement input. For a gameplay mode that needs a stationary character, clear movement/velocity, suspend the normal Animate script where appropriate, stop conflicting tracks, and explicitly own the resting joint transforms for that mode. Restore the original Animate state on exit. Current rigs may use AnimationConstraint; transforms are normally overwritten between PreAnimation and PreSimulation. Preserve intentional action animations, verify observer clients, and verify real walking resumes when the mode ends. A normal-input regression confirmed these behaviors; root anchoring alone was not a sufficient assertion. See the official [Animator](https://create.roblox.com/docs/reference/engine/classes/Animator) and [AnimationConstraint](https://create.roblox.com/docs/reference/engine/classes/AnimationConstraint) APIs.
