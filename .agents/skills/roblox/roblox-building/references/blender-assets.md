# Blender and imported assets

Use Blender for original reusable meshes when it improves the result: characters/creatures, accessories, vegetation, props, architecture details, focal objects, and spell models. Background Python scripts can create and export a cohesive library; save the editable `.blend` files and inspect a render/contact sheet before import.

- Establish scale, origin/pivot, material names, normals, and object/model names before export. Use model-level scaling where appropriate and verify actual bounds after import.
- Prefer named material pieces and intentional material assignments. An FBX may import its geometry successfully while dropping the expected Blender colors. Inspect actual Studio MeshParts; repair named-piece colors/materials or supported textures explicitly, then verify again.
- Keep the imported asset library separate from generated scripts and scene placement. Preserve ownership/asset-ID metadata with the project. Reimports may generate new IDs or change grouping and need another permission/loading check.
- Import through Studio's supported pipeline under the intended creator. Loading an asset in the editor or from cache does not prove the published experience can load it. Test mesh, texture, audio, and animation permissions in that experience.
- Do not ship scripts embedded in catalog/model imports merely because the geometry is useful. Inspect imported executable content and retain only intended, understood game code.

Follow the parent [building skill](../SKILL.md) for measured triangle budgets, reuse, scene composition, and performance verification. Keep the editable source and confirm the final Studio import matches the intended materials, scale, and silhouette.

For walking creatures, preserve authored geometry while assigning limbs to a small weighted skeleton. Keep bone names and the creature animation profile in agreement. Import with the custom rig intact, restore any dropped material colors by named mesh, and verify actual limb deformation in Play. A successful Bone.Transform assignment is not visual proof. Roblox stores the skin weights in the imported mesh asset; see [rigging and skinning](https://create.roblox.com/docs/art/modeling/rigging) and [Bone.Transform](https://create.roblox.com/docs/reference/engine/classes/Bone/Transform).
