# Source and place delivery

Treat checked-in Rojo projects as build inputs and derive expected source/module/package trees from actual builds, not a second hardcoded inventory. Synchronization must add, replace, and remove owned source trees while preserving unrelated serialized terrain and artwork byte-for-byte where possible. Compare every delivery place and the combined build with its own expected source closure, and reject test fixtures and bridges. Artifact checks complement the existing Studio result; they do not require another playtest when the tested source, packages, and assets match.

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

A terrain archive in ServerStorage proves that runtime can restore terrain, not that the saved editor file already contains Workspace terrain. Source/archive checks alone can miss this distinction. For an immediately editable delivery, restore its correct TerrainRegion at the recorded cell corner, save locally through Studio, reopen, and sample actual occupied voxels near the authored arrival. Keep source/package equality and fixture checks afterward. Do not publish to fix a local saved-file omission. A targeted terrain splice must also copy any referenced SharedString definitions and preserve unrelated artwork.

For repeatable engine reopening checks, verify exact editor/file identity, complete source equality, package requires, artwork/archive presence, live arrival terrain voxels, and fixture exclusion. This proves deserialization and package loading; it does not prove visual rendering or a published client. Terrain `ReadVoxels` arrays include a `Size` field, so iterate their numeric dimensions rather than treating every table entry as a voxel column.

Keep intentional asset updates explicit. Source-only synchronization correctly preserves old artwork, so importing a new rig does not automatically update saved delivery files. Use the project's explicit asset-sync operation to replace owned artwork while preserving unrelated serialized content. Copy every referenced SharedString definition, reject missing/conflicting definitions, and verify model hierarchy, mesh IDs, and bone rest poses. Give the synchronizer the actual prior source-layout revision when it requires one; the default branch may predate the saved file's module trees.
