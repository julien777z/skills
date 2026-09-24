---
name: roblox-studio
description: Create, update, polish, and playtest Roblox games in Roblox Studio, including detailed maps, character presentation, Blender assets, background MCP playtests, and verified place delivery. Use the companion luau, roblox-react, and roblox-building skills for code, interfaces, and world design.
---

# Roblox Studio

Carry a Roblox game request through implementation, visual polish, real playtests, and the authorized delivery. Support both new experiences and changes to existing games. Adapt the mechanics and art direction to the user's game; do not transplant another project's names, story, map, assets, or architecture.

## Dependencies

- `luau` — apply when reading or changing Luau; owns code, types, server authority, and lifecycle cleanup.
- `roblox-react` — apply when inspecting, changing, or testing React-rendered interfaces; owns responsive layout, visual quality, and interaction checks.
- `roblox-building` — apply for environments, assets, traversal, and map/place architecture.
- `roblox-gameplay` — apply when modifying gameplay.
- `agent-lock` — coordinate exclusive access before controlling a shared runner.

## Work autonomously within the requested scope

- Treat an approved plan as an implementation request. Make routine design and engineering choices, fix failures, and continue through verification with minimal user input.
- Continue until the stated issue is resolved and verified, or a concrete blocker leaves no safe, authorized way to make further progress. An unresolved defect, passing CI, a pushed PR, a failed recovery attempt, or a status report is not a stopping point. Investigate the next supported hypothesis, repair the failed capability, or use an authorized alternative; do not make the user repeatedly say "continue".
- Before declaring a blocker, identify the exact required action that cannot succeed, the evidence, the relevant recovery and alternative paths tried, and the specific external change or user input needed. Distinguish an unavailable tool from an unsolved product defect. Continue independent work while a dependent action is blocked; avoid repeating unchanged attempts or turning an unconfirmed cause into a conclusion.
- First establish the workspace, intended place/experience, signed-in owner, existing source/art, and any explicitly excluded games. For a new game, create a genuinely new place. For an update, work against the verified intended place. Never use a similarly named recent place as proof of identity.
- Record the place ID, universe ID, owner, local file, source/build paths, and current verification status in the workspace. Preserve this state across long runs.
- Use authorization already supplied in the task. Publishing, paid assets, account changes, and computer-control fallbacks must remain within that authorization and the active tool policies. Do the reviewable work before any genuinely necessary final approval. Do not add a blanket approval gate for ordinary edits, fixes, imports, or tests.
- With independent guest input and capture, the host need not be unlocked. Capture and assess guest output in either host lock state; unlocking the host is not a remedy for guest rendering artifacts. An unlock is relevant only to a required operation that actually depends on that machine's desktop. Check host sleep, guest lock, and viewer availability separately; never bypass a lock. Read the [VM access and lifecycle reference](references/isolated-testing.md) before choosing a control path.

## Choose the tooling and protect the artwork

Inspect installed tools and project conventions before building. Prefer a suitable Studio connector/API or Rojo for supported operations, and computer control for Studio-only UI. Blender is encouraged for original editable assets; its background Python mode is useful for repeatable modeling, export, and contact-sheet renders. Python and the Luau CLI are useful for build orchestration, artifact validation, and pure rules tests.

Read the [source, editor, and publication reference](references/studio-workflow.md) when synchronizing source, importing/exporting, running Studio automation, or publishing. Read [source and place delivery](references/source-delivery.md) when synchronizing module/package trees or validating built places.

Read [world-space text inspection](references/world-space-text.md) whenever changing or testing an
authored sign or a runtime world-space message, regardless of its renderer.

Keep generated scripts separate from imported assets and Studio-authored scenery. Maintain editable source, Blender originals, exported assets, and build instructions. A routine script rebuild must preserve manual art. Test that the saved/rebuilt place contains the actual assets and terrain, rather than relying on the current Studio session or cached meshes.

## Avatars and assets

Read [Asset and avatar standards](references/assets-and-avatars.md) for imported assets and character presentation. Preserve the player's avatar unless an override is requested or required by the game. Verify proportions, faces, attachments, locomotion, and action animations in play.

## Record operational lessons as they occur

Distill a verified lesson into usable guidance in its owning skill. For setup or recovery instructions, give the parameterized command or API call, prerequisites, action order, fallback conditions, and success check; resolve machine-specific values from configuration. Generalizing a lesson must preserve the procedure that lets the next agent succeed, not reduce it to “inspect, retry, and verify.” Apply this to the entry point and every supporting reference.

Keep incident timelines, machine inventories, project identities, and dated evidence in the project record or verification output. Include a platform constraint only when it changes the procedure, with its applicability and source; one observation does not establish a universal cause or fix. Replace conflicting guidance rather than appending another exception.

Code, interface, gameplay, and environment lessons belong to their respective dependencies. Keep Studio operations here and avoid duplicating another owner's guidance.

## Experience and place operations

Read [the multi-place reference](references/studio-workflow.md#multiple-maps-and-persistence) for loader, session handoff, and teleport operations. Preserve existing artwork and the authorized save contract. Keep temporary test profiles separate from live data.

## Test through completion

The retained VM is the shared **Roblox development environment for every game**, not a project-specific sandbox. Reuse its Studio installation, login, tooling, SSH identity, and settings across repositories. Keep connection configuration and tools outside individual game checkouts; use generic `ROBLOX_STUDIO_*` names. Give each game a separate guest workspace and verify the project/place before every operation. Use the VM access reference for the configured runner instead of provisioning another VM per game.

Read the [Studio MCP reference](references/mcp-testing.md) before automating Studio. When guest-native UI or capture requires a remote viewer, also read the [background viewer reference](references/hidden-vm-viewer.md). **Use the retained VM by default for Studio work whenever it can reliably perform the needed operation. If it is shut down, start it yourself and reconnect; being offline is not a reason to choose local Studio.** Verify the intended editor, rendering, input, and window/focus isolation. Use guest MCP for supported operations and the hidden guest viewer when viewport capture needs it.

Use local Studio only as a fallback for a concrete VM limitation, within the user's existing authorization. Record the failed capability and attempted recovery, then use the existing verified host editor through MCP without native host keyboard/mouse control or extra client windows. Do not prefer local Studio merely for convenience or parallel work. Multiplayer and other obstructive launches still require the isolated runner; keep those checks incomplete if it cannot run them. An explicit current user instruction choosing a different runner takes precedence.

Read [End-to-end testing and input lessons](references/testing.md) before writing or running the verification pass. The optional [VirtualInput helper](scripts/virtual_input.luau) handles normal game UI coordinates, including phone notch insets; inject it only into temporary Studio test fixtures.

Prepare the VM before handing it to the user: complete Screen Sharing/noVNC authentication and any guest macOS login yourself using the existing authorized guest credentials, then verify the desktop is visible. Opening a connection dialog is not a completed handoff. Follow [the authentication procedure](references/isolated-testing.md#authentication-and-user-handoff) and distinguish the viewer, guest OS, and Roblox account prompts. Reuse retained Roblox authentication; request user involvement only for a specific remaining step you cannot complete with available authorized credentials or sign-in methods. Do not request secrets in chat or transfer cookies.

If Studio's MCP server is disabled, enable it yourself as part of setup and verify the intended editor connects. Do not routinely ask the user to toggle it. Use the normal setting or a verified settings mechanism, preserve unrelated preferences, and keep the change scoped to the intended Studio/VM. An empty inventory alone does not prove the toggle is disabled; allow connection discovery and inspect the actual setting. Ask for a manual step only when a concrete tool/permission blocker prevents completion, explaining that blocker and opening the relevant page first where possible.

Close each task-owned Studio editor as soon as its authoring, test, or publication work is finished, after saving needed changes and confirming any upload completed. Do not accumulate finished editors until final cleanup; close them before opening the next place. Keep an editor open only while it has active work, and preserve unrelated user-owned editors.

Reuse the existing sandbox across sessions. At completion, save the authorized artifacts, close Studio normally, shut down the VM, and verify it is stopped. Preserve installed apps, login, files, settings, and SSH access. Do not uninstall, log out, reset, delete, or recreate the sandbox as cleanup. The VM access reference defines lifecycle and published-client qualification.

Use relevant automated checks and one focused Studio playtest for the affected behavior. Reuse passing evidence when the tested source, packages, and assets match the delivery build. Do not add a second walkthrough, saved-file reopening, or published-client test merely because delivery is approaching. Repeat only checks invalidated by a subsequent change or needed to investigate an observed failure. Follow [delivery build acceptance](references/source-delivery.md#test-the-delivery-build-directly) for artifact identity and targeted serialization checks.

Use normal player controls for the focused playtest; direct server calls provide separate integration evidence. Mobile, multiplayer, and persistence checks are targeted coverage when those behaviors are affected, not a checklist to repeat before every delivery. Fit relevant scenarios into the existing verification pass and reuse their results. A small shared-world fix normally needs only focused desktop visual/traversal checks.

For visual work, inspect actual screenshots and movement, and fix what looks wrong even when scripts compile. During normal-input playtests, deliberately rotate, pan, and zoom the player camera at intervals; a mostly fixed camera is insufficient visual coverage. Inspect avatars and held items from front, side, and rear while idle and moving, inspect props and entrances from both approaches, and check encounter framing and camera restoration. Use supported camera controls where the game permits them, respecting intentional camera locks. For multiplayer changes, test independent clients, joins/disconnects, duplicate requests, and reward isolation at the supported capacity. Report whether tests ran in Studio, the published client, a device simulator, or physical hardware.

## Deliver the verified result

For game changes, publication is part of finishing the task unless the user explicitly defers or excludes it. After implementation and required verification are complete, save the local places, retain editable source/art and a reproducible build, and publish every affected place to the verified experience, owner, and visibility. Do not stop at a commit, PR, local build, or Studio test. Confirm terminal publication success and the intended destination/version; do not routinely launch the published experience. Studio success is sufficient for normal delivery. Run live tests only when explicitly requested or needed to investigate a reported live-only defect. Report skipped live-only behavior, such as actual cross-place teleports, as unverified without making it an automatic delivery blocker. Update public-facing names/descriptions when changed by the task. If a concrete blocker prevents publication, report it and keep publication incomplete.

## Output

After a game task and cleanup are complete, report the verified changes, publication state, concise controls, source/place links, and material verification limits. Include a clickable Roblox game URL resolved from the verified experience start-place ID; label it as the existing published version when publication remains pending. Distinguish implementation, saved artifacts, publication, and live-client evidence. Do not call the task complete while required work remains or silently substitute a prototype for the requested playable scope.
