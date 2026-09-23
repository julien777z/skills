# Studio workflow and operational lessons

## Identity, source, and assets

Record the intended experience (universe), place IDs, owner, local file, and build paths. Verify the active Studio title and place ID before writing or publishing. Create a new experience when requested; never copy an excluded recent project. Updates must preserve existing saved progress and authored artwork.

Use a scripts-only Rojo project during iteration, and a separate complete-place build containing serialized art, rig, map, and terrain archives. Test the complete build in a fresh session. Older Rojo versions can reject meshes/models serialized by newer Studio: a model rejected by Rojo 7.2.1 worked with 7.7.0. Check the installed version and current official release; do not conclude that the asset itself is corrupt.

Terrain is not ordinary geometry. Preserve it with `Terrain:CopyRegion()` and restore with `PasteRegion()` at the recorded voxel corner. Regions use 4-stud voxel coordinates. Archive distant maps separately to avoid serializing the empty space between them. Verify restored cell counts and walk the actual terrain in a rebuilt place. A current Studio viewport can hide a missing terrain export.

After restoring terrain, wait for a simulation step before building patrol/navigation samples with raycasts. In a verified case, sampling immediately after PasteRegion saw existing Parts but missed Terrain; after `RunService.Heartbeat:Wait()`, the same query found the full landscape. Compare initial samples with a later sample to catch this timing issue.

Studio's `SerializationService:SerializeInstancesAsync()` and `EncodingService:Base64Encode()` can export authored instances when available in the current editor security context. Keep exported binaries separate from generated script content. Do not repeatedly try an API that reports the operation is unavailable in that context.

## Multiple maps and persistence

A Roblox experience is a universe containing one or more places. Prefer separate places in the same experience for large independent maps; their DataStores are shared. If requested, make the start place a small loader that reads the durable profile and uses server-side `TeleportService:TeleportAsync()` to send the player to the saved map's entrance. Keep a validated map ID to place ID registry. Do not treat untrusted teleport data as inventory or progression authority.

Persist map identity rather than an arbitrary exact position when entrance-based resume is intended. Save and safely release session ownership before another place acquires the profile; freeze mutations during handoff. Handle both thrown errors and `TeleportInitFailed`, bounded retries, and recovery without dropping progress or duplicating grants. A failed load must never route using a default profile that overwrites real progress. Studio cannot execute actual cross-place teleports. Report them as unverified unless a live-client test was explicitly requested or needed to investigate a reported live-only defect; do not make that test a routine delivery gate.

Read current official guidance before relying on changing platform behavior:

- [Teleporting](https://create.roblox.com/docs/projects/teleport)
- [Data stores](https://create.roblox.com/docs/cloud-services/data-stores)
- [Rojo releases](https://github.com/rojo-rbx/rojo/releases)

## Editor automation

Prefer supported tools and APIs. A temporary trusted loopback bridge can make source synchronization and Studio test orchestration practical when no suitable connector exists. Bind only to loopback, execute only authored commands, serialize jobs, and keep the bridge and test fixtures out of the saved/published game. Do not turn it into a public code-execution endpoint or extract account cookies to work around UI limitations.

A command queue file disappearing means it was consumed, not that a long Studio test finished. Await the explicit result before queuing dependent commands. Avoid overwriting pending jobs. Editor code runs against the editable DataModel, not the separate running server/client DataModels. Inject isolated test fixtures and clean them up after termination.

Editor `require()` caches ModuleScript values even after source synchronization. Recreate or clone the relevant module instances before relying on changed content in an editor build operation; do not mistake stale cached values for a failed source update.

## Native UI fallback

Read fresh accessibility state and screenshots. Native menus often expose a `Cancel` secondary action that works when a generic Escape keystroke does not. An automation click can move the cursor without delivering a game click; verify the resulting UI state, not the tool's success status.

Use AppleScript/System Events or another native fallback only within the user's authorization and active tool policy. With authorized native HID input, activate and verify the exact target process immediately before sending input. Release all held keys/buttons. Identify the named main window: window 1 can be a tooltip or tiny auxiliary window. Convert downscaled screenshot coordinates to the actual window bounds before clicking. A PID-targeted event may behave differently from a foreground HID event.

Opening a local place can launch a separate Studio process. An existing app-control handle may remain attached to the old DataModel. Verify the new file and process before editing. Close each task-owned finished editor normally after saving needed changes and confirming any publication, before opening the next place. Do not retain unused editors merely because the control tool can distinguish them; they consume memory and complicate targeting. Preserve unrelated user-owned instances.

Multiple browser processes can have different tabs/accounts. An AppleScript browser query may reach a separate automation instance rather than the signed-in visible browser. Verify the actual page/account through the chosen surface. Do not browse unrelated user tabs to compensate.

If the computer locks, do not bypass it. Continue independent file work and identify the unlock dependency only when necessary.

## Delivery

To add a newly built map to an existing experience, use Studio’s Publish to Roblox As, select the verified experience, then Add as a new place. The dashboard’s Add A Place flow may list existing places to move instead. A Rojo project name does not guarantee the published place name; inspect and update the child place’s metadata after creation.

Save the actual Studio place, compare expected source revisions, and confirm temporary fixtures/bridge commands are absent. Retain a reproducible build and editable asset originals. Publish only to the authorized place, owner, and visibility. Inspect terminal publication success, destination, and version. Do not routinely launch the published client; use the narrow live-test criteria in [testing guidance](testing.md). A saved file, successful upload, Studio test, and live-client test are distinct evidence.

### Spatial queries in larger maps

Repeated queries with thousands of individual instances in `FilterDescendantsInstances`, plus repeated tree `GetPivot()` calls for every candidate, can turn map startup into a long stall. In a verified large-scene case, use a few scene-root filters with a query collision group, cache static obstacle positions in a spatial grid, and set `RespectCanCollide` when the intent is physical clearance. A query group can ignore foliage without changing its collisions with players. Confirm the entire activity footprint against terrain and safe regions after optimizing, and measure startup again; faster queries must preserve geometry checks. See [RaycastParams](https://create.roblox.com/docs/reference/engine/datatypes/RaycastParams) and [OverlapParams](https://create.roblox.com/docs/reference/engine/datatypes/OverlapParams).

## Explicit lighting in generated places

Set modern lighting explicitly in the Rojo place project. A tested fresh build that omitted it loaded as Compatibility and Studio migrated it to Voxel with Retro tone mapping, changing brightness and environment lighting. With Rojo 7.7, `Technology: Future`, `LightingStyle: Realistic`, and `PrioritizeLightingQuality: true` serialized successfully; the reopened Studio place reported Realistic and no migration ColorGradingEffect. Technology is deprecated and cannot be read from an ordinary command context in current Studio; verify the current LightingStyle instead. Keep runtime ambient/exposure settings consistent with the authored scene and visually compare a fresh rebuild. These quality choices are art-direction decisions, not a blanket physical-device performance guarantee. [Roblox Lighting reference](https://create.roblox.com/docs/reference/engine/classes/Lighting).

## Bounded binary exports through MCP

Studio 0.737 truncated a large textual `execute_luau` result near 100,000 characters, corrupting a base64 art export. Serialize once, split the encoded bytes into bounded chunks (70,000 characters worked), retrieve each chunk, and validate the complete base64 before replacing the local artifact. A single `StringValue` also rejected a 435,776-character value; use separate bounded temporary values if engine storage is needed. Remove the temporary export container in `finally`. Keep the original binary until validation succeeds.
