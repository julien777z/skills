# Source, editor, and publication constraints

## Identity, source, and assets

Record the intended experience (universe), place IDs, owner, local file, and build paths. Verify the active Studio title and place ID before writing or publishing. Create a new experience when requested; never copy an excluded recent project. Updates must preserve existing saved progress and authored artwork.

Every place, for iteration and for delivery alike, is a `rojo build` of the repository's code, art, area and terrain files, laid out as [the project layout](#project-layout) says; test a built place's contents in a fresh session when serialization is affected. Check serializer compatibility against the installed versions and current official releases before diagnosing an asset as corrupt.

Terrain is not ordinary geometry, and Rojo cannot live-sync it. Keep each map's terrain in its own file: copy it with `Terrain:CopyRegion()` and restore it with `PasteRegion()` at the recorded voxel corner. Regions use 4-stud voxel coordinates. Copy distant maps separately to avoid serializing the empty space between them. Confirm the terrain file survives a `rojo build`: verify restored cell counts and walk the actual terrain in the built place. A current Studio viewport can hide a missing terrain file.

After restoring terrain, wait for a simulation step before building patrol/navigation samples with raycasts. Verify terrain readiness with representative samples before deriving navigation; part hits alone do not establish terrain readiness.

Keep saved binaries separate from generated script content, and save them as [saving files through MCP](#saving-files-through-mcp) describes.

## Project layout

Fully managed Rojo leaves several choices open; settle them this way:

- **Art** is one `.rbxm` per asset in an art directory the project mounts in ServerStorage; the file's name becomes the instance's name, so every asset name must be a safe file name.
- **An area is the unit of a level file.** An `.rbxm` has exactly one root and a Rojo node has one `$path`, so one directory cannot be merged into a folder that another also fills, and a role folder cannot be split across files. Each area file is therefore one Folder named for the area, holding that area's role folders. The world folder holds one folder per map, each mounting that map's area directory, at the same depth in every place, including a place that holds several maps, so no lookup branches on the place.
- **Lookups go through one shared helper** that finds an object by role and name across every area, and observes role folders as they stream in on the client; no code indexes a role folder of the world directly.
- **Area files live outside the code tree**, such as `world/<map>/<area>.rbxm` beside it, because the linters, the type checker and the Rojo sourcemap own the code tree.
- **Every object is filed by one deterministic rule**, most specific region first: the interior a door leads into, then a named area, then a district, then the map's base area. An object named for a world point, such as an NPC's post or an encounter's arena, files at that point; any other model files at its bounding-box center. An object no area holds is refused with its name and position and the map volume widened, never silently dropped.
- **A builder change reaches a level only once that level is rebuilt, or edited and saved.** Changing a builder changes no saved area file. Apply it by running the builder over the affected areas in an editor opened on the built place and saving those areas; re-saving rewrites only the files that changed, so the diff shows exactly the edit.
- **`rbx-merge`** is pinned with the project's tools (`rokit add kennethloeffler/rbx-merge`). One person runs `rbx-merge install --write-gitattributes` once and commits the `.gitattributes` block; every clone runs `rbx-merge install`, which belongs in the project's install recipe. In a git worktree it writes to the main clone's `.git/info/attributes`, which covers every worktree. Where no prebuilt binary exists, such as Linux arm64, the bootstrap builds it with `cargo install --git <rbx-merge repository> --tag <pinned tag> rbx_merge_cli`, which needs Rust 1.85 or newer. `git diff` on an area file then shows a readable instance tree.

### Converting an older pipeline

A pipeline that keeps whole-world archives, splices parts of them in place or exports maps by cutting a world apart is converted, never extended:

1. Measure the starting world from a `rojo build` of each place: how reused art is copied, which per-placement changes the copies carry, which role folders hold them, and whether every asset name is a safe file name.
2. Move the runtime first: the shared lookup helper and every consumer of the old role folders, and the server's marker swap wired into world start.
3. Write the authoring steps that turn each copy into a marker, proving each against the copy it replaces, and that file a built world into map, area and role. The project's world builder ends with both.
4. Run the conversion once from a script kept outside the repository: build the old place, run both steps in an Edit session, and save every area and asset file. Keep each Studio call short enough for the runner lease.
5. Mount the art and area directories in every Rojo project, and delete what the layout supersedes: the whole-world archives, splice and export tools, and any receiver that carried files back from Studio.
6. Verify as the testing reference's [placement and before-and-after verification](testing.md#placement-and-before-and-after-verification) says.

## Multiple maps and persistence

A Roblox experience is a universe containing one or more places. When using separate places in one experience for large independent maps, their DataStores are shared. If the game calls for a loader, make the start place a small loader that reads the durable profile and uses server-side `TeleportService:TeleportAsync()` to send the player to the saved map's entrance. Keep a validated map ID to place ID registry. Do not treat untrusted teleport data as inventory or progression authority.

Persist map identity rather than an arbitrary exact position when entrance-based resume is intended. Save and safely release session ownership before another place acquires the profile; freeze mutations during handoff. Handle both thrown errors and `TeleportInitFailed`, bounded retries, and recovery without dropping progress or duplicating grants. A failed load must never route using a default profile that overwrites real progress. Studio cannot execute actual cross-place teleports. Report them as unverified unless a live-client test was explicitly requested or needed to investigate a reported live-only defect; do not make that test a routine delivery gate.

Read current official guidance before relying on changing platform behavior:

- [Teleporting](https://create.roblox.com/docs/projects/teleport)
- [Data stores](https://create.roblox.com/docs/cloud-services/data-stores)
- [Rojo releases](https://github.com/rojo-rbx/rojo/releases)

## Editor automation

Use Studio's MCP server for editor operations and for bringing files back from Studio. A receiver listening on the host's loopback never reaches a Studio running inside the runner, so do not build one; never add a code-execution endpoint or extract account cookies to work around UI limitations. Editor code runs against the editable DataModel, not the separate running server/client DataModels. Inject isolated test fixtures, keep them out of every built place, and clean them up after termination.

Editor `require()` caches ModuleScript values even after source synchronization. Recreate or clone the relevant module instances before relying on changed content in an editor build operation; do not mistake stale cached values for a failed source update.

## Native UI fallback

Read fresh accessibility state and screenshots. Native menus often expose a `Cancel` secondary action that works when a generic Escape keystroke does not. An automation click can move the cursor without delivering a game click; verify the resulting UI state, not the tool's success status.

Use AppleScript/System Events or another native fallback only within the user's authorization and active tool policy. With authorized native HID input, activate and verify the exact target process immediately before sending input. Release all held keys/buttons. Identify the named main window: window 1 can be a tooltip or tiny auxiliary window. Convert downscaled screenshot coordinates to the actual window bounds before clicking. A PID-targeted event may behave differently from a foreground HID event.

Opening a local place can launch a separate Studio process. An existing app-control handle may remain attached to the old DataModel. Verify the new file and process before editing. Close each task-owned editor other than [the game's warm editor](testing.md#keep-the-games-editor-warm) once its changes are saved and any publication confirmed, before opening the next place, as [leaving the shared runner as you found it](testing.md#leave-the-shared-runner-as-you-found-it) describes. Preserve unrelated user-owned instances.

Multiple browser processes can have different tabs/accounts. An AppleScript browser query may reach a separate automation instance rather than the signed-in visible browser. Verify the actual page/account through the chosen surface. Do not browse unrelated user tabs to compensate.

Before sending native input, check the desktop that receives it — the runner's guest, or the user's own desktop when they chose host Studio: whether the screen is locked
(`CGSessionCopyCurrentDictionary()` reports `CGSSessionScreenIsLocked`) and whether the process
sending input is trusted for accessibility (`AXIsProcessTrusted()`). A small Swift script run with
`swift` reads both without extra packages. A locked screen drops synthetic input. The agent unlocks the guest itself; on the user's own
desktop the unlock is the user's step, while the settings change it unblocks stays the agent's.

For a Studio setting or permission an operation reports as missing, open the setting the error
names in the verified Studio window, make the change, and press that page's own Save; closing it
without saving discards the change. Confirm the change with a request that cannot create anything,
such as an upload with an invalid asset type, which an approved directory passes to a validation
error rather than a directory refusal, then retry the original request. Assistant MCP
permissions are stored per place and can be managed only in a place saved to Roblox, so open a
Roblox-saved place of the same owner — a private test place rather than the live game — when the
current editor holds a local file.

Open Cloud uploads read only from approved directories, and approving one needs the desktop. Approve
a single Roblox-branded staging directory once per machine, `~/Roblox/Uploads`, never a checkout,
worktree or build path that changes between sessions. Upload steps write or copy each artifact into
a per-project subfolder there, such as `~/Roblox/Uploads/<project>/`, and upload from it; the
repository keeps the editable source and export. Approve the directory as the setting paragraph
above says.

A locked desktop affects operations that depend on that desktop. Independent guest access follows the [testing reference](testing.md); independent file, build, and API work can continue.

## Delivery

To add a newly built map to an existing experience, use Studio’s Publish to Roblox As, select the verified experience, then Add as a new place. The dashboard’s Add A Place flow may list existing places to move instead. A Rojo project name does not guarantee the published place name; inspect and update the child place’s metadata after creation.

Build the place from the delivery head with `rojo build`, compare expected source revisions, and confirm temporary fixtures are absent. Retain a reproducible build and editable asset originals. Publish only to the authorized place, owner, and visibility. Inspect terminal publication success, destination, and version. Do not routinely launch the published client; use the narrow live-test criteria in [testing guidance](testing.md). A saved file, successful upload, Studio test, and live-client test are distinct evidence.

### Spatial queries in larger maps

Repeated queries with thousands of individual instances in `FilterDescendantsInstances`, plus repeated tree `GetPivot()` calls for every candidate, can turn map startup into a long stall. Use a few scene-root filters with a query collision group, cache static obstacle positions where useful, and set `RespectCanCollide` when the intent is physical clearance. A query group can ignore foliage without changing its collisions with players. Confirm the entire activity footprint against terrain and safe regions after optimizing, and measure startup again; faster queries must preserve geometry checks. See [RaycastParams](https://create.roblox.com/docs/reference/engine/datatypes/RaycastParams) and [OverlapParams](https://create.roblox.com/docs/reference/engine/datatypes/OverlapParams).

## Explicit lighting in generated places

Set the intended lighting properties explicitly in generated places using the current serializer
and Studio API. For example, a Rojo 7.7 build serialized `LightingStyle: Realistic` and
`PrioritizeLightingQuality: true`; omitting them changed the reopened scene's lighting. Inspect
the reopened place's `LightingStyle` and visually compare it with the authored scene.
Do not use the deprecated `Technology` property's ordinary command-context readback as proof of
the active style. Keep ambient/exposure choices consistent with the art direction and test affected
device behavior. See the [Lighting reference](https://create.roblox.com/docs/reference/engine/classes/Lighting).

## Saving files through MCP

Studio's Save to File menu command has no MCP equivalent. Save an asset or area to its file this
way:

1. In an Edit session, serialize the instance with `SerializationService:SerializeInstancesAsync()`,
   base64-encode the result with `EncodingService:Base64Encode()`, and hold the string in `shared`
   with its byte count. Do not repeatedly try an API that reports the operation is unavailable in
   the current security context.
2. Read the string back with `execute_luau` in chunks well under the tool's output limit: it
   truncates a result near 100,000 characters, and 60,000-character chunks leave room. Check each
   response's length; a `StringValue` cannot hold a large export.
3. Reassemble and decode, then check the byte count and that the file starts with the `<roblox!`
   signature before replacing the file. Keep the original until the check passes, and clear the
   value in `shared` even after a failure.

Wrap these steps in one repository helper that runs a script in an editor and saves named area and
asset files, so a conversion, a builder rerun and an ordinary edit all save the same way.
