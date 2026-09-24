# Map making and surface integration

Apply this guidance to the requested genre and map. Preserve its art direction, authored scenery, and intended gameplay rules.

## Composition and traversal

- Establish a small visual language: palette, materials, architecture, vegetation, silhouettes, and focal landmarks. Detail the player's arrival and main routes first, then connect the rest of the world coherently.
- Compose views at normal camera height. Use varied tree/building clusters, terrain contours, paths, landmarks, foreground detail, and quieter resting spaces. Keep routes readable and preserve space for movement and gameplay cameras.
- Detail the faces players actually approach. A building can appear finished from one side while presenting blank walls on the main path. Check roof orientation, gables, windows, doors, trim, and ground transitions in both directions.
- Treat entrances, branches, crossings, and the main traversal network as connected routes. Every intended access path must meet both its destination threshold and an actual connected route edge. Do not stop a connector at an arbitrary length, clamped coordinate, or nearby point and assume the remaining gap is acceptable. Intentional broken routes, dead ends, or unpaved transitions need a clear visual purpose and navigable continuation where gameplay requires it.
- Derive connector endpoints from canonical entrance anchors and the receiving route's actual geometry. Account for width, curve, slope, and elevation so surfaces meet across a usable walking corridor. Recompute affected connections when either endpoint, the building orientation, or the network changes; inspect the joins in the saved/rebuilt scene.
- Verify visual continuity separately from reachability: walk each affected route from the network to its destination and back without an unintended detour, grass crossing, jump, or drop. Inspect both endpoint joins and intermediate seams at player height. Record any gap even when pathfinding reaches the destination; an isolated building screenshot does not validate its connection.
- Inspect boundaries from the full supported zoom range. Distant islands, tutorial areas, and staging platforms should not become accidental scenery. Separate distinct spaces sufficiently and enclose them intentionally; do not rely on a fog value without checking the active Atmosphere/lighting configuration in play.
- Verify bridges and ramps with real walking. Decks should connect flush to approaches, collision surfaces should cover the route, and rails should run along the sides. A decorative bridge above water may still let a character pass underneath, swim, or become stuck. Use an appropriate hidden foundation/collision surface when the geometry needs it.
- Check small decorative blockers too: a thin lamp post in a road can snag both players and a pathfinding driver. Place posts on the shoulder and disable collision on purely decorative thin props when appropriate. For generated terrain, ground props against a raycast of the rendered voxel surface; the analytic height can sit noticeably above it. For imported meshes with retained rotations, use their actual bounds and world axes when fitting or grounding them.
- Place encounters, collection objects, and navigation waypoints in their intended areas. Follow bridges and gates with authored route nodes or suitable pathfinding. A direct arrow through an obstacle is not usable navigation.
- Keep requested duels/activities inside the explorable map. If a separate scene is an intentional product choice, give it a deliberate transition and return path. Do not silently move gameplay to an off-map development platform.
- Place wayfinding information where it is visible and readable from the intended walking route before the relevant choice or destination. Validate each expected approach direction using the normal gameplay camera while staying on the route; a close-up from a specially chosen angle is not acceptance. Set orientation, setback, height, and reading distance together, keeping supports and scenery clear of the message. Choose one or multiple readable faces according to the approaches served. If physical signage cannot communicate reliably there, use another presentation suited to the game's visual language rather than requiring players to leave the route or hunt for the readable side.
- Apply [world-space text inspection](../../roblox-studio/references/world-space-text.md) to authored signs and runtime messages placed in the map.
- Give a larger map distinct, connected areas with believable transitions in terrain, materials, buildings, and vegetation. Detail should support each area's role and guide exploration; scattered repeated props do not substitute for composition.
- Use textured, economical meshes where silhouette and surface detail improve the scene. Measure mesh budgets, reuse assets, and verify performance and loading in play. Enable streaming when appropriate for scale, then test destination loading, disappearance/reappearance, and interior transitions; triangle counts alone do not prove performance.
- Exclude content spatially when it does not belong in an introductory or restricted area instead of scattering unusable interactions through that area.

## Functional placement

Place each object for a legible gameplay, environmental, or compositional purpose.
Choose its location, orientation, scale, support, and neighboring objects together.
Interactive objects need recognizable approaches connected to the intended routes,
usable standing space, and clear arrival and departure directions. Decorative objects
must support the scene's use and visual hierarchy rather than merely fill empty space.

Reserve the space needed to approach, operate, animate, arrive at, and leave an object,
including character and camera clearance. Check this space against nearby props,
architecture, terrain, and other interactions. Disabling collision does not resolve
a visual obstruction or a placement that contradicts the object's apparent use.
Keep deliberately obstructed or unusual arrangements only when their purpose is
understandable and consistent with the intended gameplay.

Visible barriers, fields, and other effects must communicate their source, purpose,
extent, and active state through their shape, material, placement, and appropriate
visual cues. A translucent primitive alone does not establish that meaning. Inspect
them from normal walking and gameplay cameras, including both sides and views where
they overlap characters or other transparent surfaces. Keep trigger volumes, collision
proxies, debug planes, and other technical helpers invisible in player builds. Verify
state-dependent effects appear and clear at the intended moments, including after
interruption, rejoin, and streaming; an unexplained pane or lingering effect fails
visual acceptance even when it does not block movement.

Review the assembled scene from each normal approach and perform its intended
activities in context. Check both individual placements and their relationships;
objects that work separately can form an incoherent or obstructed scene together.
After moving or adding an object, recheck its neighbors, sightlines, routes, and
interaction clearances. Scene acceptance must record this review separately from
functional tests; move, reorient, or remove unexplained placements before passing it.

## Terrain, paving, and adjoining parts

Treat visible intersections as map defects to repair during the affected visual pass, even when compilation and gameplay assertions pass. Avoid unrelated map redesign; preserve intentional embedded foundations, overlaps, and terrain variation.

- Inspect the entire footprint and perimeter of circular plazas, disks, pools, steps, thin slabs, roof edges, and other parts touching terrain or geometry. Checking only the center misses grass wedges at curved edges and crossings at road joins.
- Trace the actual source of clipping: solid terrain, decorative grass, a placed plant/mesh, intersecting parts, or nearly coplanar faces. Fix the relevant geometry/material/placement rather than concealing it with lighting or a camera restriction.
- Clear or grade terrain beneath paving with enough margin for the voxel surface's interpolation. Use suitable non-grass material under hard surfaces when needed to prevent blades protruding. Prefer a local terrain edit that preserves nearby water, landscaping, and contours. Do not globally remove vegetation to fix one plaza.
- Thin parts need a deliberate foundation and clearance. Avoid nearly coplanar surfaces that flicker, exposed undersides, unsupported rims, holes, or floating slabs. Increasing thickness below the intended walking surface can help; simply raising the top can create an unintended step and leave the original terrain collision unresolved.
- Fit adjacent roads, ramps, curbs, and circular edges into continuous walkable approaches. Blend the surrounding grade; do not leave a trench or conspicuous bare ring as the fix. Check actual imported bounds and terrain raycasts rather than assuming mathematical centers or analytic terrain heights match the rendered surface.
- Correct both the canonical builder/source and the preserved map. Re-export affected terrain/art archives and verify a fresh saved/rebuilt place so the defect does not return on rebuild.

## Spatial rules and inspection

If a game defines protected traversal areas, share their actual geometry between scenery and gameplay. Validate whole activity footprints and moving NPC body bounds, not just center points, and apply the game's intended trigger exclusions. After moving an activity area, update its authored geometry and rewalk the affected routes. This is a geometric technique; it does not make every game's roads safe.

For a local geometry repair, focused desktop coverage is normally sufficient; use the [testing scope rules](../../roblox-studio/references/testing.md#choose-coverage-for-the-change) for new maps, substantial changes, or device-specific concerns. Walk across repaired surfaces and joins in both directions, then move the camera around them at low, normal, and elevated supported angles. Inspect the perimeter as well as the main approach for grass penetration, flicker, gaps, floating edges, and collision snags. Fix defects found in that pass and recheck their immediate neighbors. Record representative views of the actual saved/rebuilt scene, not only the currently edited viewport.

Use [End-to-end testing](../../roblox-studio/references/testing.md) for normal-input coverage and [Studio workflow](../../roblox-studio/references/studio-workflow.md) for safe terrain archives, spatial-query performance, explicit lighting, and delivery. Use [Blender and imported assets](blender-assets.md) for Blender/import details; keep those procedures canonical there.

## Frame-relative terrain and scenery

Keep analytic height/material functions in map-local coordinates, including fixed noise phases. Convert at the terrain writer and scenery boundary. Heightfield terrain should explicitly support upright translation/yaw and reject pitch/roll unless the generator implements them. A yaw-rotated terrain volume needs an enclosing voxel archive plus a mask for empty corners; transforming only its minimum and maximum is insufficient.

Use the canonical house/door definitions for planting exclusions and approaches as well as visible architecture. Duplicated convenience lists can leave vegetation behind when the map moves. Give procedural random generators a per-build seed so repeating generation is reproducible. Compare generated part positions, rotations, sizes, appearance, and collision before/after refactoring, and test translated/rotated frame consumers in temporary folders without clearing the user's saved terrain. Ordinary source synchronization must preserve saved artwork; deliberate world regeneration is a separate operation.
