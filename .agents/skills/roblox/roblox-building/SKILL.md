---
name: roblox-building
description: Apply when planning, inspecting, creating, modifying, importing, optimizing, or playtesting Roblox maps, worlds, terrain, buildings, props, environmental meshes, or Blender assets. Require coherent and interesting environments, separate Roblox places for independent maps, economical measured geometry, readable traversal, preserved artwork, and player-height visual/performance checks.
---

# Roblox building and world design

Build worlds that make sense, look intentional, and reward exploration. Preserve the requested genre, existing artwork, gameplay, and visual identity. Use this skill for environment work; it does not authorize a visual redesign during an unrelated code task.

## Give every map a purpose

Before extending a world, identify its role in the overall game, arrival/exit routes, neighboring maps, landmarks, terrain, inhabitants, activities, and intended traversal. Give each region a recognizable identity within one coherent palette and architectural language. Its geography and connections should be understandable: roads lead somewhere useful, bridges cross meaningful obstacles, water and terrain connect plausibly, and settlements have believable entrances and functions.

Keep major independent maps as separate Roblox **places** in the same experience by default. A region within a continuous map can remain in that place. Do not hide independent maps far apart in one production Workspace or let distant staging areas leak into the player's view. A combined developer build is a test artifact, not the delivery architecture. Keep each place's own scenery, terrain archive, spawn/exit definitions, and build inputs. Use a validated map/place registry and deliberate transitions; follow [Studio's multi-place workflow](../roblox-studio/references/studio-workflow.md#multiple-maps-and-persistence) for session handoff and teleport verification. Do not create separate universes or publish places without task authorization.

## Avoid bland or arbitrary environments

Vary terrain shape, sightlines, silhouettes, landmarks, architecture, vegetation, lighting, and the rhythm of enclosed/open spaces. Compose focal areas with quieter spaces between them. Make routes readable and reward looking around with meaningful environmental detail, optional discoveries, or views appropriate to the scope. Do not substitute a larger empty field, random prop scattering, or endless copies of one tree for a designed map.

Give every district a useful role and connect it visually to its neighbors. Inspect approached building faces, roof orientation, doorways, signs, supports, interior scale, shoreline transitions, and terrain joins. Detail must support navigation, story, or atmosphere while leaving room for player movement and the gameplay camera. Preserve established safe-zone and encounter rules.

Evaluate every object's placement in the complete scene: why it belongs there, what
it faces or connects to, how it is approached and used, and whether its neighbors
support or obstruct that purpose. Reserve the full approach, interaction, and exit
space before adding decorative props. Apply the functional-placement criteria in
the map-making reference; isolated asset quality, collision checks, and successful
interactions do not establish a coherent arrangement.

Read [Map making and surface integration](references/map-making.md) for composition, traversal, terrain joins, collision, and inspection. Use shared map/model frames and named anchors as described in [luau](../luau/SKILL.md); update geometry and its gameplay consumers together.

## Blender and economical meshes

Use Blender when original editable meshes improve silhouettes and cohesive detail. Keep the `.blend` source, export recipe, asset identity, and measured geometry counts. Read [Blender and imported assets](references/blender-assets.md) before creating/importing assets.

Keep meshes low in triangles for their visible purpose and expected repetition. Spend detail on silhouettes and close focal objects; simplify repeated/background props. Do not use Roblox's maximum import limits as a production budget. Agree a project-appropriate budget from target devices and visible density, then record actual triangulated counts per asset and representative loaded scene. A tree repeated hundreds of times has a different budget from a single landmark.

Remove hidden/internal faces where they cannot become visible, unnecessary edge loops, and excessive subdivisions. Preserve normals, UVs, outline, and important deformation when simplifying. Inspect the exported triangulated result, not only Blender's quad count. Texture/material detail can replace geometry where it remains convincing at player distance; keep texture memory and material splits economical too.

Reuse identical mesh/texture assets and IDs instead of repeatedly uploading duplicates. Prefer appropriate automatic/performance render fidelity, simple collision shapes, and selective shadows. Avoid unnecessary precise collision or a single enormous combined mesh that defeats useful streaming boundaries. These choices follow [Roblox performance guidance](https://create.roblox.com/docs/performance-optimization/improve); measure their effect in the actual scene.

Low triangle counts alone do not guarantee smooth play. Also inspect draw calls, materials, transparency/overdraw, texture memory, particles, lights, physics, scripts, and streaming load. Measure representative busy views and startup using Studio performance tools. Record device/simulator, graphics level, frame time, and memory where available. Do not describe a desktop or simulator result as physical mobile performance.

## Build and Play test

Use [roblox-studio](../roblox-studio/SKILL.md) for imports, preserved terrain, source synchronization, background MCP tests, and authorized delivery. Apply [luau](../luau/SKILL.md) when opening or modifying builders/scripts. UI belongs to [roblox-react](../roblox-react/SKILL.md).

Trace every affected entrance and activity access route all the way to the established traversal network; a reachable destination or walkable grass does not prove its authored path connects. Apply the route-continuity criteria in the map-making reference. Walk the arrival route, every changed connection, bridges/ramps, doors, and activity boundaries in both directions. Inspect at player height and supported camera zoom/pitch from multiple approaches. Check clipping, floating props, flicker, inaccessible steps, collision snags, misleading paths, bland sightlines, and accidental views of other maps. Fix defects in the canonical builder and saved artwork so rebuilding preserves the repair.

For major maps or streaming changes, test stream-out/re-entry, destination preloading, interiors, missing assets, and appropriate mobile coverage. Verify complete activity footprints avoid protected routes. Reopen a fresh build to check terrain, assets, lighting, source/package closure, and absence of test fixtures. Report code checks, Studio traversal, simulation, performance measurements, and published-client results separately.

Keep reusable building lessons here, Studio operations in `roblox-studio`, and game-specific world design in the project skill. Update canonical `.agents` sources only; leave provider mirrors to Agent Sync.

Sources for place architecture: [Roblox places](https://create.roblox.com/docs/production/publishing/publish-games-and-places), [teleporting](https://create.roblox.com/docs/projects/teleport).
