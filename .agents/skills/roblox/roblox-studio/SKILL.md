---
name: roblox-studio
description: Create, update, polish, and playtest Roblox games in Roblox Studio, including maps, assets, interfaces, playtests, and authorized place delivery. Apply companion skills for code, interfaces, world design, and gameplay when relevant.
---

# Roblox Studio

Carry a Roblox game request through implementation, visual polish, real playtests, and the authorized delivery. Adapt the mechanics and art direction to the user's game; do not transplant another project's names, story, map, assets, or architecture.

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
- First establish the workspace, intended place/experience, signed-in owner, existing source/art, and any explicitly excluded games. Verify whether the task calls for creating a place or updating one, then work against that destination. Never use a similarly named recent place as proof of identity.
- Record the place ID, universe ID, owner, local file, source/build paths, and current verification status in the workspace. Preserve this state across long runs.
- Use authorization already supplied in the task. Publishing, paid assets, account changes, and computer-control fallbacks must remain within that authorization and the active tool policies. Do the reviewable work before any genuinely necessary final approval. Do not add a blanket approval gate for ordinary edits, fixes, imports, or tests.
- Choose a runner that can execute the required Studio operations without interfering with the user's active desktop. Confirm its input, capture, and window behavior before relying on it. Read the [testing reference](references/testing.md) before choosing the control path.

## Choose the tooling and protect the artwork

Inspect installed tools and project conventions before building. Use Rojo for source/place synchronization, a suitable Studio connector/API for editor operations, and authorized computer control for Studio-only UI. Blender is encouraged for original editable assets; its background Python mode is useful for repeatable modeling, export, and contact-sheet renders. Python and the Luau CLI are useful for build orchestration, artifact validation, and pure rules tests.

Read the [source, editor, and publication reference](references/studio-workflow.md) when synchronizing source, importing/exporting, running Studio automation, or publishing. Read [source and place delivery](references/source-delivery.md) when synchronizing module/package trees or validating built places.

Apply `roblox-building` and its world-space text reference whenever changing or testing an authored sign or runtime world-space message, regardless of renderer.

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

Read [Studio testing](references/testing.md) before choosing a runner or verification pass. Select the available qualified Studio environment from the project's configuration and the user's instructions. Prefer supported Studio MCP operations for editor inspection, Play orchestration, input, and viewport capture. Apply `agent-lock` before controlling a shared runner. Use an isolated runner for unattended or multiplayer launches that would obstruct the user's desktop; qualify input, capture, rendering, and window isolation separately. The testing reference includes an optional retained Tart/macOS runner and guest viewer procedure for installations that have them.

The optional [VirtualInput helper](scripts/virtual_input.luau) converts UI coordinates across safe insets; inject it only into temporary Studio test fixtures.

Verify the intended editor and place before every operation. If a tool is unavailable, inspect its actual setting and connection state before changing it. Keep unrelated editors and user windows untouched. Complete normal authentication with available authorized methods; ask for a specific user-only step only when required. Never request secrets in chat or transfer cookies.

Use relevant automated checks and one focused Studio playtest for the affected behavior. Exercise normal player controls and inspect the visible result; direct server calls provide different evidence. Add device, multiplayer, or persistence coverage when the change affects those behaviors. Reuse passing evidence when the tested source, packages, and assets match the delivery build. Repeat checks only after an invalidating change or observed failure. Follow [delivery build acceptance](references/source-delivery.md#test-the-delivery-build-directly) for artifact identity.

For visual work, inspect actual screenshots and movement, including camera angles and approaches relevant to the change. Record whether evidence came from Studio, a published client, a device simulator, or physical hardware. Remove temporary fixtures, restore settings, close task-owned editors and test windows, and stop task-owned runner processes. Preserve unrelated user sessions and retained runner state.

## Deliver the verified result

Save the authorized source, artwork, and place artifacts and verify their destination and content. Publish only when the current task authorizes publication, to the verified experience, owner, place, and visibility. Confirm terminal publication success and version when publishing. Do not infer live-client behavior from Studio evidence; run published-client tests only when requested or needed to investigate a live-only defect. Report any unverified live-only behavior accurately.

## Output

After a game task and cleanup are complete, report the verified changes, publication state, concise controls, source/place links, and material verification limits. Include a clickable Roblox game URL when a verified published experience exists; label an existing version clearly when no publication was authorized. Distinguish implementation, saved artifacts, publication, and live-client evidence. Do not call the task complete while required work remains or silently substitute a prototype for the requested playable scope.
