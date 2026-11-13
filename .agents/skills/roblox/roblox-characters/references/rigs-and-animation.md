# Rigs, avatars and animation

The `roblox-characters` skill's reference for avatar overrides, rig and accessory fitting, procedural motion, imported creature rigs, and character collision. Apply these standards to the game's genre and the requested change. They do not prescribe a genre, quest structure, or custom avatar.

## Avatar overrides

For an override, start with an appropriate Roblox body package/HumanoidDescription and compatible catalog hats/accessories. Use a coherent silhouette and controlled proportions; fit original Blender details to that body. Do not compensate for poor fitting with giant blocky shells. Do not assume permission to purchase an accessory or spend Robux. NPCs can use compatible rigs with deliberate variations.

- Inspect the bounds of off-world preview rigs. `Humanoid:AddAccessory()` may leave an accessory at its original position outside Workspace, causing viewport fitting to shrink the whole character. Align matching attachments and create/verify the accessory weld before fitting the camera. Prebake validated templates when it avoids runtime asset loading and keeps previews consistent with equipped characters.
- Preserve recognizable facial/skin appearance where compatible. A catalog face product ID is not necessarily an image content ID: inspect the loaded asset's actual Decal/Texture instead of assigning the product ID directly as a texture. Never execute scripts from an imported face/accessory model.

## Procedural motion

- Current R15 assets may use AnimationConstraint-based joints rather than only Motor6D. Inspect the actual rig before writing procedural poses. Joint transforms are normally overwritten between PreAnimation and PreSimulation, so layer procedural motion in the animation/simulation phase where the default animator does not overwrite it immediately. See the official [Animator](https://create.roblox.com/docs/reference/engine/classes/Animator) and [AnimationConstraint](https://create.roblox.com/docs/reference/engine/classes/AnimationConstraint) APIs.
- Procedural idle/action/impact/victory or other game-specific motion is an option when suitable. Do not describe those as uploaded animation clips. If uploaded clips are required, upload them under the correct owner, named and recorded as every asset uploaded for the game is, and verify their IDs/permissions in the live experience.
- Character action, impact, and defeat presentation should be readable and timed to the authoritative events. Client presentation completion must never decide whether server gameplay can proceed.

## Imported creature rigs

For walking creatures, preserve authored geometry while assigning limbs to a small weighted skeleton. Keep bone names and the creature animation profile in agreement. Import with the custom rig intact, restore any dropped material colors by named mesh, and check the deformation in Play as the skill's verification says. Roblox stores the skin weights in the imported mesh asset; see [rigging and skinning](https://create.roblox.com/docs/art/modeling/rigging) and [Bone.Transform](https://create.roblox.com/docs/reference/engine/classes/Bone/Transform).

## Collision and stationary characters

For nonblocking NPCs, use an explicit collision group with player collision disabled; editor part flags alone may be changed by Humanoid behavior. Apply the group to runtime and serialized NPCs, and verify by walking past them.

Anchoring a player and setting `WalkSpeed=0` do not necessarily stop the running animation or clear the last movement input. For a gameplay mode that needs a stationary character, clear movement/velocity, suspend the normal Animate script where appropriate, stop conflicting tracks, and explicitly own the resting joint transforms for that mode in the phase **Procedural motion** describes. Restore the original Animate state on exit. Preserve intentional action animations, verify observer clients, and verify real walking resumes when the mode ends.
