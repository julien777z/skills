# Studio testing

Choose coverage for the affected behavior, qualify the available runner, then verify real input and the delivered result. Keep setup procedures conditional on the installed tools and the user's chosen environment. Choosing, qualifying, provisioning, connecting to and controlling the runner are in the [runner reference](runner.md).

Contents: **Coverage and verification**, **Choose coverage for the change**, **Evidence types, not
sequential delivery gates**, **Studio test orchestration**, **Keep the game's test helpers in its
repository**, **Input coordinates: the phone notch matters**, **Coverage and visual inspection**,
**Placement and before-and-after verification**, **Report honestly**, **Persistence fixtures and
place arrival**, **Engine test suites through an existing editor**.

## Coverage and verification

Scale UI coverage to the change: the repeated-click pass runs at the checkpoints `roblox-ui` sets. Scale the tests to the actual task. A small UI edit needs focused visual/input verification; a complete game chapter needs a complete journey and relevant systems coverage.

Default to relevant automated checks and one focused Studio playtest, reusing passing evidence as [delivery build acceptance](source-delivery.md#test-the-delivery-build-directly) says.

## Choose coverage for the change

Mobile testing is selective, not a required step in every iteration. For a game that supports both desktop and mobile:

- **UI changes:** test the affected screens and interactions on desktop and mobile, including layout, touch targets, safe areas, scrolling, and modal behavior. A shared UI component change should cover its affected consumers; it does not require replaying the whole game.
- **Significant changes:** include mobile coverage for an entire new map, a substantial world expansion, major gameplay/input changes, or changes to streaming/rendering/performance that can behave differently on mobile. Choose representative journeys and device checks for the actual impact.
- **Small shared-world fixes:** grass clipping, a misplaced prop, a sign support, or a local terrain seam normally need the grounding, blocking, boundary and surface audit below, desktop visual inspection and relevant walking checks only. Do not repeat the same verification on mobile when the geometry and behavior are shared and there is no device-specific concern.
- **Mobile defects or explicit requests:** reproduce and verify on the affected mobile layout/device regardless of change size.

After the relevant checks pass, continue to delivery, repeating only what a later change or an observed failure invalidated, as [delivery build acceptance](source-delivery.md#test-the-delivery-build-directly) says.

## Evidence types, not sequential delivery gates

Select coverage for the affected behavior and combine it in the existing pass. This list does not require running every layer. Mobile, multiplayer, and persistence checks apply only when affected or explicitly requested.

1. **Standalone behavior:** Run the project's configured engine-independent suites for target validation, costs, rewards, transitions, failures, and cleanup. Lute Jest-compatible execution and actual Roblox Jest provide different evidence; an Edit-context engine result is also distinct from Play integration.
2. **Studio integration:** Use actual server/client instances for authority, replication, persistence boundaries, joins, disconnects, and cleanup. Direct server fixtures are useful here, but are not a normal-input walkthrough.
3. **Player journey:** Start from a fresh disposable profile and operate real movement, prompts, menus, targets, and action buttons. Follow authored routes, complete objectives, claim rewards, and finish the requested content. Fix any blocked route or unusable control discovered along the way.
4. **Live-only investigation (optional):** Run a published-client test only when explicitly requested or necessary to investigate a reported live-only defect. Otherwise confirm publication success and destination/version without launching the game. Studio evidence is sufficient for normal delivery; it does not establish actual cross-place transport or published asset permissions. Mark skipped live-only behavior unverified, without blocking delivery.

Record which layer each result proves. A fast automated driver skips reading and deliberation; its elapsed time is not the expected first-time player session length.

## Studio test orchestration

Studio exposes `StudioTestService:ExecutePlayModeAsync(args)` and `ExecuteMultiplayerTestAsync(playerCount, args)` from an editor-capable context, with `EndTest(result)` inside the test. Check current official docs/tool capabilities before relying on an API in a different Studio version.

Prefer the built-in Studio MCP orchestration and input tools in the [chosen runner](runner.md#choose-and-qualify-a-runner). Qualify input and launch/window behavior separately; unattended client launches stay in the runner. Inspect running/queued state before another launch and give profile-load/setup waits explicit deadlines.

Inject temporary server/client probes deliberately. Create LocalScripts/Script/ModuleScript with the correct classes; exclude fixtures from Rojo production projects. Have an explicit deadline and a structured result. Clean up scripts, test-only remotes, time-scale overrides, persistence flags, and disabled encounter directors even after failure.

When multiplayer behavior changes, test at least two independent clients and the supported capacity where relevant. Include real disconnects, independent progression, joining during supported phases, duplicate/late requests, unrelated players receiving no rewards, and restoration of movement/UI after exit. If an ordinary server fixture disables automatic engagement for deterministic tests, separately prove actual proximity entry in normal play.

Use ordinary Studio profiles that cannot overwrite live player progress. When persistence changes warrant real DataStore verification, use clearly isolated validation keys under the intended experience, save partial progress, end/rejoin across distinct sessions, and prove rewards remain single-grant. Verify competing session ownership, failed loads, and shutdown behavior where applicable. Never infer persistence from a table surviving in one process.

## Keep the game's test helpers in its repository

Every step a check repeats has one tested helper, committed in the game repository's test tooling
area and built on the [studio_mcp](../scripts/studio_mcp/__init__.py) package for the transport. The
helpers load the package only when an agent runs them; their tests build the values it returns and
double it where a helper calls it, so the game's CI runs them with no skills present. Helpers cover:

- putting a disposable profile into a given state;
- walking the character to an NPC, prompt or place through real movement around the collision
  geometry, as a player does;
- pressing a prompt or a control through real input, and reading back that it responded;
- starting an encounter, a match or another game mode from its real entry point;
- running a multi-client test and counting the clients that actually joined;
- capturing the viewport and recording motion.

What every helper must get right:

- **Set up on the server, act as the player.** State a check starts from, such as a profile or a
  spawned encounter, is made server-side; everything the check judges is driven by the player's
  input on the client.
- **Confirm every input registered** from the state it should change, never from the call
  returning. Input goes through the real input path, such as `Studio.click` or the
  [VirtualInput helper](../scripts/virtual_input.luau); a script run during Play that sets the
  camera or a character's position directly, or calls the game's handlers in place of the input
  that reaches them, is refused, since it fakes what the check judges.
- **Stop a walk to a prompt inside the prompt's activation distance**, measured from the prompt's
  own part, so the press that follows can land.
- **Rerun a multi-client test only when a client did not join**, read from the connected-player
  count; a joined client's failure is the result, not a reason to retry.
- **List editors with `studio_mcp.wait_for_studios`**, which waits out the empty list a new MCP
  connection reports at first, before concluding no editor is open. To find the windows a launch
  adds, take the snapshot with `listed_editor_ids` before it and poll `new_editors` on that same
  connection after it; a snapshot from `studios` on a new connection is empty, so every editor
  already open reads as new.
- **A check keeps its slot for as long as it renews it.** `agent-lock` hands a lock left unrenewed
  for five minutes to the next waiter, so a session that dies frees its slot without anyone choosing
  how long a check may run. Every `studio_mcp` call that reaches the VM renews the receipt's locks,
  and a process that acquired or used a receipt keeps renewing them every minute in the background
  until it releases them or exits; a check that runs as several separate scripts calls
  `runner_lease(receipt)` about every minute between them. A check takes a slot with
  `acquire_editor_lock`, opens what it needs right after acquiring, does the check, closes every
  editor and test process it started, and releases with `release_runner_lock`. The slot's warm
  editor is the one editor a check leaves open. A check whose open meets `RunnerLockBusy`, because
  other slots' launches kept the VM's focus, releases its slot and runs again rather than failing.

Workers use these helpers and extend them for each new repeatable step; a repeatable step is never
a throwaway script in a temporary folder or Luau pasted into one run. Each helper returns a
structured result and fails with what it observed, never a bare timeout. A false alarm traced to a
helper, such as a walk that stops short or a press that lands on another control, is fixed in the
helper, never worked around in the run that met it. Helpers are test support and are reviewed as the entry point says. A brief for Studio work names the
helpers the worker uses.

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

Assert that the intended control actually responds through visible state and its authoritative outcome. A timeout or automatic transition can falsely attribute progression to a click that never worked. Inspect input events and the actual UI hierarchy when uncertain.

Dismiss any current tutorial or modal overlay before clicking an underlying control, because a click behind an overlay fails whatever the control does and reads as a broken control. Recheck the current round and modal after every transition.

## Coverage and visual inspection

For affected systems, exercise their normal actions and relevant failure boundaries: unavailable resources, invalid targets, timeouts, defeat, retreat, respawn, rewards, and save/rejoin where applicable. Preserve resources on invalidated actions according to the game's rules and prevent duplicate rewards.

Map coverage includes surface and traversal criteria when world content is affected. Inspect the real scene and UI at spawn, along principal routes, during encounters, after restoration/state changes, and at the finale. Verify animation movement and replication, asset loading errors, camera framing, target readability, and cleanup after repeated encounters. Check navigation around actual collision geometry rather than validating only waypoint coordinates.

Actively use the camera during the walkthrough. Periodically orbit left and right, change pitch, and zoom in and out through the supported range, then resume walking from the new view. At visual checkpoints, inspect the avatar and held objects from front, side, and rear during idle, locomotion, and relevant actions; circle signs and doorways to inspect supports, lettering, and approach visibility. Enter and leave a conversation or encounter from a changed camera heading and verify control/framing restore correctly. Respect intentionally locked cameras. Capture representative alternate angles and record that the camera was operated; static editor views and a fixed-heading input driver do not substitute for this coverage. **An arrangement is checked in world terms**, whoever runs the check: a formation, placement, facing or spacing is asserted from world positions and facing relative to what the characters or objects face, such as two guards meant to flank a gate standing side by side across its width rather than one behind the other along the path to it, and then shown in a capture from where the player sees it. How it projects into one camera view proves nothing, since a single view hides depth along its own line of sight.

When the game supports normal camera-orbit input, press the right mouse button, allow a frame for the camera to lock the cursor, then use `VirtualInput:SendMouseDelta()` while locked. `SendMousePosition()` positions the pointer; use relative motion for locked-cursor camera controls. Assert that the camera actually changed and the character stayed still. Release the mouse button in failure cleanup as well as on success. See [VirtualInput](https://create.roblox.com/docs/reference/engine/classes/VirtualInput).

When mobile coverage is warranted by the change, use Studio's device simulator to test the touch branch and actual interactions. Confirm that touch input was delivered, that affected scrollable content moves, and that movement controls do not overlap interactive UI. Record the simulated device and safe viewport.

## Placement and before-and-after verification

A change to the place layout, to how art is placed, or to where anything stands is verified in the
world's data first and in captures second:

- **A whole-world placement diff decides it** for a change to the place layout or to how art is
  placed, and for one that moves more than a few pieces; a fix to a few pieces, such as a misplaced
  prop, is checked by its save's own file diff and the audit in Play below. Read every part's frame,
  size and look — color, material, transparency, collision flags, and the appearance and text it
  carries — from the place before the change and the place after it, in Edit with markers placed
  exactly as the server places them, and match parts across the two. Every difference must be one
  the change intends; an area or object that differs for any other reason is a defect. Captures
  alone never establish placement: a pair can look the same while parts moved, and look different
  while nothing did.
- **The diff runs for every published place, each against its own build.** Build that place's own
  project at the commit just before the change and at the change, each with that commit's world, art
  and terrain, dump each build in its own runner lease, waiting for a busy runner rather than
  sharing one, and report each place separately. One combined build, such as a development place
  holding every map, never stands in for them: when it carries a stale copy of a map on both sides,
  the diff shows nothing while the map's own place loses or regains content. Two matching rules keep
  a layout change from reading as moves: a world from before the area files exist is read as one
  unfiled area, and an older copy of an asset that nests its model under a model of the same name
  matches the marker that replaced it.
- **A grounding, blocking, boundary and surface audit in Play decides whether pieces rest, block and
  meet flush, and whether the player stays inside.** Any change to a world runs it, never a visual
  pass, after the runtime swap has placed every piece. It checks every placed art piece, water
  piece, resting single part and pickup, and skips characters and creatures, actors staged to hover,
  worn items, and pieces their builder marks as hanging. For each piece it casts down from 2.5 studs
  above each foot, a plant's feet being its stem bottoms and any other piece's its lowest parts,
  then from its middle, then a terrain-only cast from high above; a flat-based piece, paving
  included, is also cast at its corners and along its edges, so a side hanging over a slope reports
  its gap. Terrain, solid or visible structural parts, a solid resting piece, flat kit meshes at
  most 1 stud tall and floors count as support; plants, other box-collision kit meshes and invisible
  colliders do not. A piece floats when its base is more than 0.3 studs above its support, a pickup
  more than 1.2 and a water piece more than 0.25 off the water either way, and is buried when it
  sinks by more than a set share of its own height. A blocking pass reports every floor-standing
  piece at least 2 studs tall whose collision reaches less than 70% of its height. A boundary pass
  walks, jumps and swims toward every map edge, drop and stretch of open water from each reachable
  side and height, and reports every spot where the player gets past. A surface pass reports
  overlapping faces within a small tolerance of one plane, part against part and part against
  terrain, each step where walkable pieces meet, and each edging strip off its edge by more than a
  set angle or gap or leaving a stretch of the edge bare. Findings group by piece, area and problem,
  each with its count, the worst gap and three sample positions. Fix them in the builders and rerun
  until the audit reports none.
- **The quest-gate audit `roblox-gameplay` requires runs in Play**, over the objects that exist for
  a quest as it defines them, never scenery or residents a step also references. Once it reports
  none, confirm in Play with a fresh profile and with a profile at each affected step that each
  object appears when its step becomes active and stays once the quest is done.
- **A view that looks different gets a Play dump** of the parts around it, read on the server and on
  a client, in both places: present, anchored and in place on both sides means the capture, not the
  world, differs.
- **Prove the runtime swap in Play in every place**, not only in Edit or in engine specs that run in
  Edit, because capability errors, such as a property a running game cannot write or a reserved
  attribute, appear only in Play. When world start fails without printing its reason, open the
  built place in a scratch editor, patch the server entry to `warn` the startup error, and play.
- **Before captures come from the commit just before the change**, never an older head, whose
  unrelated changes would show as differences.
- **A capture waits for its view to settle.** Wait until the scripted camera draws from the view,
  preload the parts around it with `ContentProvider:PreloadAsync`, and close any one-time windows
  that cover it. Throw away the first capture of each session, which can still predate the camera.
- **Pair fixed-camera views.** A scripted view frames the same way every run; a free-camera walk-up
  swings with toasts and nearby characters, especially on a phone, so it is evidence of what it
  shows close up, such as lettering, never of placement.
- **Read every capture before trusting a difference**, and before calling a pair identical; when
  the two disagree, read the same object's properties in both places in Play.

## Report honestly

Report each result as evidence of the layer it came from, and state what that layer cannot show: a simulator does not establish physical-device performance, a mock save does not establish durable persistence, a viewer image does not establish rendering, and Studio does not establish cross-place transport or published asset permissions. Keep a concise latest-results report with the tested revision, any publication outcome and enough raw evidence to explain meaningful failures and fixes. Separate verified behavior from untested internet latency, estimates, or remaining external blockers.

Official references: [Studio testing modes](https://create.roblox.com/docs/studio/testing-modes), [VirtualInput](https://create.roblox.com/docs/reference/engine/classes/VirtualInput), [GuiService inset areas](https://create.roblox.com/docs/reference/engine/classes/GuiService#GetInsetArea), [data stores](https://create.roblox.com/docs/cloud-services/data-stores).

## Persistence fixtures and place arrival

When testing saved place or resume state, distinguish profile loading from place-arrival
logic. Arrival logic may deliberately update the loaded profile's current destination and safe spawn before a fixture reads it. The persistence fixture must assert the expected arrival
contract for the actual place while checking retained quest progress, rewards, and custom
data. Do not force a multi-place fixture into a single-place artifact when required scenery or services are absent. Real cross-place teleport
behavior is a separate check.
Keep gameplay arrival behavior as it is and correct the fixture's destination assumption, because the fixture exists to check that behavior. For teleport failure coverage, substitute only the external transport in a disposable test copy, exercise the actual persistence and session recovery path, and remove injected modules afterward. A mocked failure is not a
successful published-client teleport.

## Engine test suites through an existing editor

If the project uses Roblox Jest or another engine suite that reads module source or compiles it, its execution context needs those capabilities.
A permission error during collection is a runner problem, not a failed gameplay assertion. Use the
project's dedicated test setup in a stopped, unpublished local editor when it requires privileged
Edit execution; never weaken production security to run it. Settings marked
[Not Scriptable](https://create.roblox.com/docs/reference/engine/classes/ServerScriptService)
cannot be assigned through Luau. Qualify the actual runner instead of repeating unsupported writes.

Engine tests in Edit establish engine behavior in that context. Live physics, replication, input,
persistence, and multiple clients need their own supported execution context. Open Cloud likewise
uses its own privileged context and serialized test project.

When the project has a Studio test runner, give it a bounded wait, structured current-run results, and cleanup
in `finally`: restore the normal source tree and original test marker, remove all injected test and
authoring trees/packages, and leave Play stopped. Disable an Edit-only test entry for ordinary Play
so it cannot launch with insufficient permissions. Never parse a historical `all tests passed`
console line as the current result; Studio output can include old failures and passes. Keep result
attributes and current run identity authoritative.

If using a separate test project, synchronize its complete explicitly mounted trees. Copying packages while omitting the suite can wait forever for an uninstalled runner. Verify the test entry before dispatch and
prove fixture removal after restoring the game project.
