# VM Mesh Rendering

Status: open. Recorded 2026-09-23 PDT. Repository: julien777z/skills. Origin PR: #5.

The shared Roblox development VM accepts guest input and captures but renders some meshes as torn triangles, missing surfaces, and long spikes. It cannot establish clean visual acceptance. Host lock does not explain this defect: guest control/capture worked during an observed host lock, and corruption persisted after the user unlocked the host.

## Evidence

| Comparison                                                                 | Observed result                                                                                                                                                                                |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Host macOS 26.6.2 (25G83), Studio 0.737.0.7371584                          | The same serialized three-outfit asset renders cleanly from front, side, rear, and in animated ViewportFrame previews.                                                                         |
| Guest macOS 15.7.7 (24G720), the same signed Studio 0.737.0.7371584 bundle | A minimal scene with no game scripts reproduces torn geometry. This comparison controls the Studio-version difference.                                                                         |
| Guest Studio 0.739.0.7390687 and 0.740.0.7400927                           | Corruption persists in Workspace and ViewportFrames, including near the origin with the published player closed. Studio's orientation gizmo also distorted.                                    |
| Guest renderer                                                             | Apple Paravirtual Metal; retained Tart 2.37.0.                                                                                                                                                 |
| Existing renderer recovery                                                 | Cold start and eager-rendering change did not repair meshes. OpenGL startup reports `Error creating pixel format`. Automatic graphics and EagerBulkExecution=false are restored.               |
| Guest OS update                                                            | Update personalization reports `Failed to find SFR recovery volume` (SUOSU 201 / SUMacController 7723 / MobileSoftwareUpdate 1256). The base-image disk lacks the separate recovery partition. |

The compared binary asset SHA-256 is `066d461998e79a29867c1354bd6eb48ca4987bf860821cd16e8377ab3211c814`. The host's current UI was checked at 1081×635, 844×320, and 375×575. Pointer selection, confirmation, and horizontal scrolling passed. These observations narrow the rendering difference to the environments; they do not prove a particular GPU-driver defect or pixel-identical results across host lock states.

The retained image is `ghcr.io/cirruslabs/macos-sequoia-base@sha256:4947ac5ab1b2fdc46ab856132d2ba958f8e45b5f85192c66370dafc028c514dd`. It retains its apps, files, login and SSH identity. No disk repartition, VM replacement, security bypass, or authentication change was performed.

## Why It Remains Open

The supported recoveries tested in the retained guest do not repair the defect. Its ordinary OS update is blocked by the missing recovery volume. A supported guest/host graphics correction or an explicitly scoped recoverable runner upgrade is needed; its success is unproven. The existing host editor through MCP supplies clean single-window visual checks within its authorization. Guest input/capture remains useful independently. Host sleep is untested.

## Pickup And Resolution

Identify a supported change to the retained runner that can be reversed without losing its data or sign-in. Preserve the current runner before any storage/OS change and establish the scope before replacement. Reproduce with a minimal scene and identical asset bytes, record host/guest OS and Studio versions, and inspect animated as well as static meshes from multiple angles. Requalify guest ordinary input, capture, a representative published client, and host-window isolation after a repair. Close this record only when guest mesh rendering is visually clean and the result is repeatable; successful input alone is insufficient.

| Supporting source                                                                                         | Purpose                                                                                                    |
| --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `.agents/skills/roblox/roblox-studio/references/isolated-testing.md`                                      | Shared runner ownership, qualified control and preservation requirements.                                  |
| `.agents/skills/roblox/roblox-studio/references/hidden-vm-viewer.md`                                      | Capture/rendering separation and observed renderer limits.                                                 |
| [Tart recovery-partition explanation](https://github.com/openai/tart/issues/1232#issuecomment-4449144329) | Base-image update prerequisite, from the maintainer.                                                       |
| [Tart graphics compatibility discussion](https://github.com/openai/tart/issues/1032)                      | Maintainer notes dependence on both guest and host OS versions; not a diagnosis of this particular defect. |

Linear tooling was unavailable at preflight, before any write; this repository record is the sole deferral store. Dated screenshots and logs remain untracked in the originating task workspace; the essential observations are preserved above.
