# Source and place delivery

Treat checked-in Rojo projects as build inputs: every delivery place is a `rojo build` of the repository's code, art, area and terrain files, and expected source/module/package trees are derived from actual builds, not a second hardcoded inventory. Compare every delivery place and the combined build with its own expected source closure, check that every marker names an asset in the art directory and that marker counts match a fresh build, and reject test fixtures. Artifact checks complement the existing Studio result; they do not require another playtest when the tested source, packages, and assets match.

## Test the delivery build directly

Prefer building delivery files before the focused Studio playtest so the same session covers gameplay and artifact loading. A synchronized working editor also supplies sufficient gameplay evidence when source/package equality, authored assets/terrain, and fixture exclusion establish that the delivery build matches it. Record the tested revision and delivery identity; do not reopen every file or replay the journey just to change the form of evidence.

For multiple places, check their expected source closures and place configuration. Exercise place-specific startup only when it changed or an observed failure requires investigation. Keep injected fixtures in disposable copies, never in delivery files. Rebuild and check integrity after changes, then repeat only behavior whose passing result was invalidated. Formatting-only or guidance edits do not require another gameplay pass.

Reopen specifically to investigate serialization failures or verify a saved-file repair. Cross-place transport remains unverified without a live client; that is a reporting distinction, not a routine delivery gate. Follow [testing guidance](testing.md) for the narrow conditions that justify live tests.

## Serialization and synchronization lessons

A Rojo-built place holds only what its project file declares, while a place Studio creates also holds default
containers the engine fills at run time. When a project maps a service such as `StarterPlayer`, declare every
default container under it that the engine or the game needs — `StarterPlayerScripts`, which receives the
engine's `PlayerModule` (controls and camera), and `StarterCharacterScripts`. A missing container cannot be added
from a script (`Instance.new` refuses those classes), and its absence fails silently: the engine never inserts
the module, so anything waiting on it yields forever while the rest of the game loads. Read a new project file
against the service's children in a fresh Studio place, and check the first Play's console for an infinite-yield
warning on an engine module before judging any gameplay.

Rojo XML can serialize script Source as `<string name="Source">`, while Studio saves may use `<ProtectedString name="Source">`. Read the named property independent of its XML tag and reject missing Source on script instances. Cover both encodings in synchronization tests. Verify actual source text after updating an editor; creating a correctly named ModuleScript is insufficient. A missing-property default of the empty string can falsely make all expected sources appear equal.

A terrain file the runtime pastes at world start proves that the game can restore terrain, not that the built place already shows Workspace terrain in Edit. File checks alone can miss this distinction. Confirm the terrain survives the `rojo build`: open the built place, restore its TerrainRegion at the recorded cell corner, and sample actual occupied voxels near the authored arrival. Keep source/package equality and fixture checks afterward. Do not publish to fix a local build omission.

For repeatable engine reopening checks, verify exact editor/file identity, complete source equality, package requires, art, area and terrain file presence, live arrival terrain voxels, and fixture exclusion. This proves deserialization and package loading; it does not prove visual rendering or a published client. Terrain `ReadVoxels` arrays include a `Size` field, so iterate their numeric dimensions rather than treating every table entry as a voxel column.

Keep intentional asset updates explicit. An asset reaches a place only through its own file: edit or reimport it in Studio, save it to that file, and rebuild the place, and every level that places it as a marker picks it up unchanged. A copy placed in an area is a separate instance a built place never relinks, so it keeps the old asset. After saving, verify the file's model hierarchy, mesh IDs, and bone rest poses in the built place.
