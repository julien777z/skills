# End-to-end testing and input lessons

UI coverage follows the interface dependency declared in the entry point. Scale the tests to the actual task. A small UI edit needs focused visual/input verification; a complete game chapter needs a complete journey and relevant systems coverage.

Default to relevant automated checks and one focused Studio playtest. Reuse passing evidence when source, packages, and assets match the delivery build, following [delivery build acceptance](source-delivery.md#test-the-delivery-build-directly). Do not add a final walkthrough, reopen, or live-client launch after sufficient evidence already exists.

## Choose coverage for the change

Mobile testing is selective, not a required step in every iteration. For a game that supports both desktop and mobile:

- **UI changes:** test the affected screens and interactions on desktop and mobile, including layout, touch targets, safe areas, scrolling, and modal behavior. A shared UI component change should cover its affected consumers; it does not require replaying the whole game.
- **Significant changes:** include mobile coverage for an entire new map, a substantial world expansion, major gameplay/input changes, or changes to streaming/rendering/performance that can behave differently on mobile. Choose representative journeys and device checks for the actual impact.
- **Small shared-world fixes:** grass clipping, a misplaced prop, a sign support, or a local terrain seam normally need desktop visual inspection and relevant walking/collision checks only. Do not repeat the same verification on mobile when the geometry and behavior are shared and there is no device-specific concern.
- **Mobile defects or explicit requests:** reproduce and verify on the affected mobile layout/device regardless of change size.

After the relevant checks pass, continue to delivery. Repeat or broaden testing only when a subsequent change invalidates passing evidence or an observed failure requires investigation; do not restart a blanket desktop/mobile suite at every follow-up.

## Evidence types, not sequential delivery gates

Select coverage for the affected behavior and combine it in the existing pass. This list does not require running every layer. Mobile, multiplayer, and persistence checks apply only when affected or explicitly requested.

1. **Standalone behavior:** Run the project's configured engine-independent suites for target validation, costs, rewards, transitions, failures, and cleanup. Lute Jest-compatible execution and actual Roblox Jest provide different evidence; an Edit-context engine result is also distinct from Play integration.
2. **Studio integration:** Use actual server/client instances for authority, replication, persistence boundaries, joins, disconnects, and cleanup. Direct server fixtures are useful here, but are not a normal-input walkthrough.
3. **Player journey:** Start from a fresh disposable profile and operate real movement, prompts, menus, targets, and action buttons. Follow authored routes, complete objectives, claim rewards, and finish the requested content. Fix any blocked route or unusable control discovered along the way.
4. **Live-only investigation (optional):** Run a published-client test only when explicitly requested or necessary to investigate a reported live-only defect. Otherwise confirm publication success and destination/version without launching the game. Studio evidence is sufficient for normal delivery; it does not establish actual cross-place transport or published asset permissions. Mark skipped live-only behavior unverified, without blocking delivery.

Record which layer each result proves. A fast automated driver skips reading and deliberation; its elapsed time is not the expected first-time player session length.

## Studio test orchestration

Recent Studio builds expose `StudioTestService:ExecutePlayModeAsync(args)` and `ExecuteMultiplayerTestAsync(playerCount, args)` from an editor-capable context, with `EndTest(result)` inside the test. Check current official docs/tool capabilities before relying on an API in a different Studio version.

Prefer the built-in Studio MCP orchestration and input tools inside the [isolated runner](isolated-testing.md); see [background testing](mcp-testing.md). Qualify input and launch/window behavior separately; unattended client launches stay in the runner. Inspect running/queued state before another launch and give profile-load/setup waits explicit deadlines.

Inject temporary server/client probes deliberately. Create LocalScripts/Script/ModuleScript with the correct classes; exclude fixtures from Rojo production projects. Have an explicit deadline and a structured result. Clean up scripts, test-only remotes, time-scale overrides, persistence flags, and disabled encounter directors even after failure. Do not leave testing hooks in the published game.

When multiplayer behavior changes, test at least two independent clients and the game's supported encounter capacity where relevant. Include real disconnects, independent progression, joining during supported phases, duplicate/late requests, unrelated players receiving no rewards, and restoration of movement/UI after exit. If an ordinary server fixture disables automatic engagement for deterministic tests, separately prove actual proximity entry in normal play.

Use ordinary Studio profiles that cannot overwrite live player progress. When persistence changes warrant real DataStore verification, use clearly isolated validation keys under the intended experience, save partial progress, end/rejoin across distinct sessions, and prove rewards remain single-grant. Verify competing session ownership, failed loads, and shutdown behavior where applicable. Never infer persistence from a table surviving in one process.

## Input coordinates: the phone notch matters

Use `UserInputService:CreateVirtualInput()` for Studio automation when available. It drives actual experience input; it is not a way to control CoreGui, Roblox's account UI, or the operating system. Check that it exists, and honor its restrictions.

Prefer MCP `user_mouse_input` targeting the actual instance and `user_keyboard_input`. Verify actual events/results rather than transport success. The following conversion applies to direct VirtualInput helpers; input stays in the authorized runner.

GuiObject absolute coordinates are relative to the core UI area. For virtual pointer input, convert a button center into full-screen coordinates:

```luau
local GuiService = game:GetService("GuiService")
local center = button.AbsolutePosition + button.AbsoluteSize / 2
local screenPosition = center - GuiService:GetInsetArea(Enum.ScreenInsets.None).Min
```

Use the full inset rectangle; top-bar offsets alone omit device safe areas. Wide controls can mask a coordinate error, so also verify a small target and the resulting selection.

The bundled `scripts/virtual_input.luau` implements this conversion. Its `release()` method clears tracked keyboard input; the calling fixture must also release any pressed mouse button if a click is interrupted. It is a test helper, not a production dependency. Wait for the relevant UI/state, move the pointer, then press/release. For moving/animated widgets, recompute the target after the UI settles.

Assert that the intended control actually responds: selected card/target state, an authoritative pending action, or a completed round. A test that waits long enough for the round timeout may falsely attribute that progression to a click that never worked. Inspect input events and the actual UI hierarchy when uncertain.

Before clicking an underlying control, dismiss any current tutorial/modal overlay. Do not mistake a blocked test click behind a lesson for a broken flee/cast button. Recheck the current round and modal after every transition.

## Coverage and visual inspection

For the systems the game implements, exercise normal actions and relevant boundaries: insufficient resources, invalid/dead targets, random misses, discard/exhaustion/refill, timeout, defeat, retreat, respawn/replay, rewards, and save/rejoin. Preserve resources on invalidated actions according to the game's rules, and prevent duplicate rewards.

Map coverage includes the surface and traversal criteria from the building dependency. Inspect the real scene and UI at spawn, along principal routes, during encounters, after restoration/state changes, and at the finale. Verify animation movement and replication, asset loading errors, camera framing, target readability, and cleanup after repeated encounters. Check navigation around actual collision geometry rather than validating only waypoint coordinates.

Actively use the camera during the walkthrough. Periodically orbit left and right, change pitch, and zoom in and out through the supported range, then resume walking from the new view. At visual checkpoints, inspect the avatar and held objects from front, side, and rear during idle, locomotion, and relevant actions; circle signs and doorways to inspect supports, lettering, and approach visibility. Enter and leave a conversation or encounter from a changed camera heading and verify control/framing restore correctly. Respect intentionally locked cameras. Capture representative alternate angles and record that the camera was operated; static editor views and a fixed-heading input driver do not substitute for this coverage.

When mobile coverage is warranted by the change, use Studio's device simulator to test the touch branch and actual interactions. Confirm that touch input was delivered, that the hand/list can scroll, and that movement controls do not overlap interactive UI. Record the simulated device and safe viewport; do not claim physical-device performance from an emulator.

## Report honestly

Keep a concise latest-results report plus enough raw evidence to explain meaningful failures and fixes. Record the deployed revision and publication outcome. Separate verified behavior from untested internet latency, physical-device performance, estimates, or remaining external blockers.

Official references: [Studio testing modes](https://create.roblox.com/docs/studio/testing-modes), [VirtualInput](https://create.roblox.com/docs/reference/engine/classes/VirtualInput), [GuiService inset areas](https://create.roblox.com/docs/reference/engine/classes/GuiService#GetInsetArea), [data stores](https://create.roblox.com/docs/cloud-services/data-stores).

For normal camera-orbit input, press the right mouse button, allow a frame for the camera to lock the cursor, then use `VirtualInput:SendMouseDelta()` while locked. `SendMousePosition()` positions the pointer; use relative motion for locked-cursor camera controls. Assert that the camera actually changed and the character stayed still. Release the mouse button in failure cleanup as well as on success. See [VirtualInput](https://create.roblox.com/docs/reference/engine/classes/VirtualInput).

## Cloud persistence fixtures and map arrival

When testing saved map/resume state, distinguish profile loading from place-arrival
logic. A fixed map can deliberately update the loaded profile's current map and safe
spawn before a fixture reads it. The persistence fixture must assert the expected arrival
contract for the actual map while checking retained quest progress, rewards, and custom
data. Do not force a combined-world map context into a single-map artifact: missing terrain
for its other regions can correctly prevent server startup. Real cross-place teleport
behavior is a separate check.
Do not weaken gameplay arrival behavior to satisfy a persistence fixture's wrong map
assumption. For teleport failure coverage, substitute only the external transport in a
temporary copy of the production travel module, exercise real persistence and lease
recovery, and remove all injected modules after the test. A mocked failure is not a
successful published-client teleport.
