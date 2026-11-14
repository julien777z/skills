---
name: roblox-worldbuilding
description: Apply when planning, inspecting, creating, modifying, importing, optimizing, or playtesting anything placed in a Roblox world — maps, terrain, water, roads, buildings, rooms, props, environmental meshes, or Blender assets. Also apply when handling authored signs or runtime world-space text, regardless of renderer. Require coherent environments, deliberate place architecture, economical measured geometry, readable traversal, preserved artwork, and player-height visual/performance checks.
short_description: 'Build and improve Roblox worlds, terrain, structures, props, and assets.'
---

# Roblox worldbuilding

## Dependencies

- `luau`
- `subagent-matrix`
- `council`

## Give every map a purpose

Build worlds that make sense, look intentional, and reward exploration. Preserve the requested genre, existing artwork, gameplay, and visual identity. Use this skill for environment work; it does not authorize a visual redesign during an unrelated code task.

Before extending a world, identify its role in the overall game, arrival/exit routes, neighboring maps, landmarks, terrain, inhabitants, activities, and intended traversal. Give each region a recognizable identity within one coherent palette and architectural language. Its geography and connections should be understandable: roads lead somewhere useful, bridges cross meaningful obstacles, water and terrain connect plausibly, and settlements have believable entrances and functions.

Choose one place or multiple places according to the game's established architecture and intended transitions. A region within a continuous map can remain in one place; independent destinations may warrant separate places within an experience. Do not hide distant production maps as staging areas visible to players. When using multiple places, keep each place's scenery, terrain, spawn/exit definitions, and build inputs separate, and use a validated registry and deliberate transitions. Require session handoff and teleport verification for multiple places; return editor operations and testing to the caller. Do not create experiences or publish places without task authorization.

## Avoid bland or arbitrary environments

Vary terrain shape, sightlines, silhouettes, landmarks, architecture, vegetation, lighting, and the rhythm of enclosed/open spaces. Compose focal areas with quieter spaces between them. Make routes readable and reward looking around with meaningful environmental detail, optional discoveries, or views appropriate to the scope. Do not substitute a larger empty field, random prop scattering, or endless copies of one tree for a designed map.

Give every district a useful role and connect it visually to its neighbors. Inspect approached building faces, roof orientation, doorways, signs, supports, interior scale, shoreline transitions, and terrain joins. Detail must support navigation, story, or atmosphere while leaving room for player movement and the gameplay camera. Every sign states what is true where it hangs: an interior's own name sign names that room, never the place outside its door, while an exit or direction sign names the destination it points to. Preserve established safe-zone and encounter rules.

Evaluate every object's placement in the complete scene: why it belongs there, what
it faces or connects to, how it is approached and used, and whether its neighbors
support or obstruct that purpose. Reserve the full approach, interaction, and exit
space before adding decorative props. Apply the functional-placement criteria in
the map-making reference; isolated asset quality, collision checks, and successful
interactions do not establish a coherent arrangement.

Read [Map making and surface integration](references/map-making.md) for composition, traversal, terrain joins, collision, and inspection. Before accepting a new map or a visual pass, a new or rebuilt interior included, run its **Scene audit** and then a fresh-eye review: invoke `subagent-matrix` at its standard capability level for one reviewer given only the audit's captures, with places of one kind side by side, and the game's stated art direction or the reference the user gave, never the build notes, and ask what reads as unfinished, repetitive, empty, off-palette or wrongly turned. Fix confirmed findings and recapture; a finding you would reject goes to `council` in **Ask** mode and its ruling is followed. Read [world-space text inspection](references/world-space-text.md) for authored signs or runtime messages in the world. Use shared map/model frames and named anchors as described in `luau`; update geometry and its gameplay consumers together.

## Blender and economical meshes

Use Blender when original editable meshes improve silhouettes and cohesive detail. Keep the `.blend` source, export recipe, asset identity, and measured geometry counts. Read [Blender and imported assets](references/blender-assets.md) before creating/importing assets.

Keep meshes low in triangles for their visible purpose and expected repetition. Spend detail on silhouettes and close focal objects; simplify repeated/background props. Do not use Roblox's maximum import limits as a production budget. Agree a project-appropriate budget from target devices and visible density, then record actual triangulated counts per asset and representative loaded scene. A tree repeated hundreds of times has a different budget from a single landmark.

Remove hidden/internal faces where they cannot become visible, unnecessary edge loops, and excessive subdivisions. Preserve normals, UVs, outline, and important deformation when simplifying. Inspect the exported triangulated result, not only Blender's quad count. Texture/material detail can replace geometry where it remains convincing at player distance; keep texture memory and material splits economical too.

**Apply the cheap performance defaults to every mesh, prop and light as it is built, never waiting for a measured slowdown.** Each one costs nothing a player sees, and its saving only shows once many pieces carry or lack it, by which point the whole world needs reworking. They follow [Roblox performance guidance](https://create.roblox.com/docs/performance-optimization/improve):

- One upload per distinct geometry, copied in the editor. Each use takes its own color or tint (`Color`, `SurfaceAppearance.Color`), never a recolored re-upload, and one texture or SurfaceAppearance is shared per kind of prop.
- Decoration, meaning anything players do not stand on, need to be stopped by, or interact with, takes `CollisionFidelity` Box, with `CanCollide`, `CanTouch` and `CanQuery` false. A piece a touch trigger, pickup or raycast relies on keeps the flag that serves it, and where a piece must block movement or the camera, a simple invisible collider does it.
- `CastShadow` false on small decoration and on anything indoors or under a roof, and `Shadows` false on interior lights the scene does not need.
- `RenderFidelity` Automatic, never Precise.
- No decorative part with partial transparency. Glass and glow use an opaque or Neon material or one shared transparent surface.
- Textures at 512 px or less, 256 px for minor props.
- Distant models use `LevelOfDetail` where the place streams.

A default is left off only where it visibly breaks the result, such as a shadow the scene's lighting depends on, and the reason goes beside that piece. Enforce the defaults where the project builds or imports pieces, so a new piece cannot skip them. Measurement checks a scene against its budget; it never decides whether a default applies. Avoid a single enormous combined mesh that defeats useful streaming boundaries.

Low triangle counts alone do not guarantee smooth play. Also inspect draw calls, materials, transparency/overdraw, texture memory, particles, lights, physics, scripts, and streaming load. Measure representative busy views and startup using Studio performance tools. Record device/simulator, graphics level, frame time, and memory where available. Do not describe a desktop or simulator result as physical mobile performance.

## Build and Play test

Return imports, terrain preservation, source synchronization, background MCP tests, and authorized delivery to the caller. Keep each area of a map in its own file and place a reused kit piece in it as a marker that a runtime script swaps for the asset, never as a copy, as Roblox's [fully managed project layout](https://create.roblox.com/docs/projects/rojo/fully-managed) does. Apply `luau` when opening or modifying builders/scripts.

Trace every affected entrance and activity access route all the way to the established traversal network; a reachable destination or walkable grass does not prove its authored path connects. Apply the route-continuity criteria in the map-making reference. Walk the arrival route, every changed connection, bridges/ramps, doors, and activity boundaries in both directions. Inspect at player height and supported camera zoom/pitch from multiple approaches. Check clipping, floating props, flicker, inaccessible steps, collision snags, misleading paths, bland sightlines, and accidental views of other maps. Fix defects in the canonical builder and saved artwork so rebuilding preserves the repair.

For major maps or streaming changes, test stream-out/re-entry, destination preloading, interiors, missing assets, and appropriate mobile coverage. Verify complete activity footprints avoid protected routes. Check the saved or rebuilt artifact for terrain, assets, lighting, source/package closure, and absence of test fixtures; reopen it when serialization needs verification. Report code checks, Studio traversal, simulation, performance measurements, and published-client results separately.

Keep reusable worldbuilding lessons here, a lesson whose subject another skill owns there, and game-specific world design in the project skill. Update canonical `.agents` sources only; leave provider mirrors to Agent Sync.

Sources for place architecture: [Roblox places](https://create.roblox.com/docs/production/publishing/publish-games-and-places), [teleporting](https://create.roblox.com/docs/projects/teleport).
