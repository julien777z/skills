# Studio testing

Choose coverage for the affected behavior, qualify the available runner, then verify real input and the delivered result. Keep setup procedures conditional on the installed tools and the user's chosen environment.

## Coverage and verification

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

Prefer the built-in Studio MCP orchestration and input tools in the [chosen runner](#choose-and-qualify-a-runner). Qualify input and launch/window behavior separately; unattended client launches stay in the runner. Inspect running/queued state before another launch and give profile-load/setup waits explicit deadlines.

Inject temporary server/client probes deliberately. Create LocalScripts/Script/ModuleScript with the correct classes; exclude fixtures from Rojo production projects. Have an explicit deadline and a structured result. Clean up scripts, test-only remotes, time-scale overrides, persistence flags, and disabled encounter directors even after failure. Do not leave testing hooks in the published game.

When multiplayer behavior changes, test at least two independent clients and the supported capacity where relevant. Include real disconnects, independent progression, joining during supported phases, duplicate/late requests, unrelated players receiving no rewards, and restoration of movement/UI after exit. If an ordinary server fixture disables automatic engagement for deterministic tests, separately prove actual proximity entry in normal play.

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

Assert that the intended control actually responds through visible state and its authoritative outcome. A timeout or automatic transition can falsely attribute progression to a click that never worked. Inspect input events and the actual UI hierarchy when uncertain.

Before clicking an underlying control, dismiss any current tutorial/modal overlay. Do not mistake a blocked test click behind an overlay for a broken control. Recheck the current round and modal after every transition.

## Coverage and visual inspection

For affected systems, exercise their normal actions and relevant failure boundaries: unavailable resources, invalid targets, timeouts, defeat, retreat, respawn, rewards, and save/rejoin where applicable. Preserve resources on invalidated actions according to the game's rules and prevent duplicate rewards.

Map coverage includes surface and traversal criteria when world content is affected. Inspect the real scene and UI at spawn, along principal routes, during encounters, after restoration/state changes, and at the finale. Verify animation movement and replication, asset loading errors, camera framing, target readability, and cleanup after repeated encounters. Check navigation around actual collision geometry rather than validating only waypoint coordinates.

Actively use the camera during the walkthrough. Periodically orbit left and right, change pitch, and zoom in and out through the supported range, then resume walking from the new view. At visual checkpoints, inspect the avatar and held objects from front, side, and rear during idle, locomotion, and relevant actions; circle signs and doorways to inspect supports, lettering, and approach visibility. Enter and leave a conversation or encounter from a changed camera heading and verify control/framing restore correctly. Respect intentionally locked cameras. Capture representative alternate angles and record that the camera was operated; static editor views and a fixed-heading input driver do not substitute for this coverage.

When the game supports normal camera-orbit input, press the right mouse button, allow a frame for the camera to lock the cursor, then use `VirtualInput:SendMouseDelta()` while locked. `SendMousePosition()` positions the pointer; use relative motion for locked-cursor camera controls. Assert that the camera actually changed and the character stayed still. Release the mouse button in failure cleanup as well as on success. See [VirtualInput](https://create.roblox.com/docs/reference/engine/classes/VirtualInput).

When mobile coverage is warranted by the change, use Studio's device simulator to test the touch branch and actual interactions. Confirm that touch input was delivered, that affected scrollable content moves, and that movement controls do not overlap interactive UI. Record the simulated device and safe viewport; do not claim physical-device performance from an emulator.

## Report honestly

Keep a concise latest-results report plus enough raw evidence to explain meaningful failures and fixes. Record the tested revision and any task-authorized publication outcome. Separate verified behavior from untested internet latency, physical-device performance, estimates, or remaining external blockers.

Official references: [Studio testing modes](https://create.roblox.com/docs/studio/testing-modes), [VirtualInput](https://create.roblox.com/docs/reference/engine/classes/VirtualInput), [GuiService inset areas](https://create.roblox.com/docs/reference/engine/classes/GuiService#GetInsetArea), [data stores](https://create.roblox.com/docs/cloud-services/data-stores).

## Persistence fixtures and place arrival

When testing saved place or resume state, distinguish profile loading from place-arrival
logic. Arrival logic may deliberately update the loaded profile's current destination and safe spawn before a fixture reads it. The persistence fixture must assert the expected arrival
contract for the actual place while checking retained quest progress, rewards, and custom
data. Do not force a multi-place fixture into a single-place artifact when required scenery or services are absent. Real cross-place teleport
behavior is a separate check.
Do not weaken gameplay arrival behavior to satisfy a persistence fixture's wrong destination assumption. For teleport failure coverage, substitute only the external transport in a disposable test copy, exercise the actual persistence and session recovery path, and remove injected modules afterward. A mocked failure is not a
successful published-client teleport.

## Choose and qualify a runner

Use the environment the current project and user authorize. A local Studio editor is suitable when its windows and input will not interrupt the user's desktop. Use an isolated VM or another qualified machine for unattended Play, multiplayer clients, or native input that would interfere. A supported Studio MCP operation can avoid moving the host pointer, but may still launch native windows. Qualify editor identity, input, capture, rendering, and window/focus isolation separately before claiming unattended testing is safe.

When a reusable isolated runner is configured, reuse its installed Studio, authentication, and tooling. Keep each game's source and test data separate, verify the intended place before acting, and coordinate exclusive control of its desktop. Start a stopped runner when needed, discover its current address, and close task-owned windows and processes after testing. An unavailable isolated capability leaves only its dependent checks incomplete; continue independent source and build work. Do not silently switch to an intrusive host workflow.

### Optional retained Tart/macOS runner

This example applies only when the host already configures `ROBLOX_STUDIO_TART`, `ROBLOX_STUDIO_VM`, `ROBLOX_STUDIO_SSH_USER`, `ROBLOX_STUDIO_SSH_KEY`, and `ROBLOX_STUDIO_KNOWN_HOSTS` in `~/.config/roblox-studio/runner.env`. Shared tools and keys live outside game checkouts. Discover the configured machine; do not assume its name or address from another session. Use a single shared desktop lock key across games using that VM.

```sh
source "$HOME/.config/roblox-studio/runner.env"
"$ROBLOX_STUDIO_TART" get "$ROBLOX_STUDIO_VM"
# Start only when stopped, in an owned background process/session:
"$ROBLOX_STUDIO_TART" run "$ROBLOX_STUDIO_VM" --no-graphics --no-clipboard --no-audio
export ROBLOX_STUDIO_SSH="$ROBLOX_STUDIO_SSH_USER@$("$ROBLOX_STUDIO_TART" ip "$ROBLOX_STUDIO_VM")"
```

Verify SSH host keys, the intended guest editor, and the source/place before running tests. The no-graphics, no-clipboard, no-audio options keep the VM from opening a host window or sharing clipboard/audio. Store versions and qualification evidence outside this skill. Do not provision or reset a working retained VM as routine setup.

### Linux container runner

A Linux host, such as a cloud agent container, can provide the Windows Studio build under Wine on an
Xvfb display. The environment's setup installs Studio, Wine, the Wine prefix, and the toolchain, and
owns them: a task never installs, repairs, or recreates any of them. A launch that fails before
Studio starts is reported to the user with its command and output as a setup change. Start Studio
through the project's launch command, or run `RobloxStudioBeta.exe` from its directory under `wine`
with `DISPLAY` set to the Xvfb display. A Studio window, its sign-in page or start page, in an X
screenshot of that display shows the launch succeeded; qualify the rest as [Qualify input and
capture](#qualify-input-and-capture) describes.

Studio's logs are in `"$WINEPREFIX/drive_c/users/$USER/AppData/Local/Roblox/logs"`. When they
report `Embedded Web Browser fail to load` (WebView2 failed to start under Wine), the embedded
sign-in is unavailable; sign in by code as [Authentication and user handoff](#authentication-and-user-handoff)
describes. When Studio offers only **Login via Browser**, Roblox has not given this installation
Quick Sign-in; report that, since only the environment's setup can provide another installation.

## Optional Tart guest capabilities

For a configured Tart runner, use the official [quick start](https://tart.run/quick-start/) and the installed
CLI's help. Keep actual versions, image identity, resource allocation, and qualification results in
local configuration and verification evidence. Reuse the retained runner before provisioning one.

With the Tart options above, the VM does not create a host window, share the clipboard, or play test audio through the user's speakers. Transfer only the project/test files over
SSH, and invoke the guest's Studio MCP executable through SSH. Keep the guest proxy connection alive
long enough for Studio discovery, as described in the MCP reference. Retrieve viewport captures and
structured results through that channel. Do not mount the whole home directory or transfer a Roblox
session cookie. Use normal Roblox authentication.

Follow [authentication and user handoff](#authentication-and-user-handoff) before presenting the
viewer. A toggle enabled on the host does not enable the guest.

Qualify the existing runner before relying on it, and recheck affected capabilities after Studio or
VM updates: authenticate, discover the intended Studio, load the current assets, run client/server
Play, operate a real button and movement, and capture the viewport without host windows or focus changes. For multiplayer coverage, also qualify the requested number of independent clients. Studio launching alone is not compatibility proof. Keep
dated qualification results in workspace evidence; do not recreate a working runner to requalify it.

Use MCP inside the guest wherever supported. Native setup actions may be performed through the guest
desktop when necessary, but never drive the host's game input. If Roblox rejects virtualization or
rendering/input is unreliable, attempt the applicable documented recovery and record the concrete
remaining limitation. Local Studio may then serve as the fallback for an already-authorized,
non-disruptive single-editor operation. Use its verified MCP connection, without native host HID
control or extra client windows. Checks requiring obstructive launches remain incomplete until the
isolated runner works. Continue independent lint, type, test, and build work; do not silently change runners.

When viewport capture fails but the guest desktop is usable, the optional
[guest desktop viewer](#optional-guest-desktop-viewer) provides background images and guest-native UI
without a visible Screen Sharing window. It describes connection requirements, authentication,
unencrypted-transport limitation, live-image check, and cleanup. It does not establish
that the guest renders game assets correctly.

Follow an explicit user choice of local Studio. Use the verified editor through supported operations and keep host input and extra client windows within the user's authorization. Where a local installation defines `ROBLOX_ALLOW_HOST_STUDIO=1` as an intentional single-editor fallback, set it only for that documented path, never as a speculative isolation bypass.

## Direct guest control

On a configured macOS guest, host Screen Sharing, guest SSH, and guest input are separate capabilities. When the host viewer
is unavailable, first check whether the retained VM is running and SSH still reaches its normal
signed-in desktop. Prefer guest MCP for supported Studio actions. When the active tool policy and
user authorization permit direct guest input, an existing guest-native helper can operate the
published Roblox player over SSH without opening a host viewer. Otherwise use the permitted
hidden viewer or Screen Sharing path; do not infer that the VM needs rebuilding or new Roblox login.

Before relying on direct control, take a fresh capture, click a real visible button, hold and release
a movement key briefly, then capture the result. Permission checks and screenshots alone do not
qualify input: include this active test in the plan and execute it before calling control usable.
Verify the intended application, account, and place. Keep input and
capture entirely inside the VM, retain the shared desktop lock, and release every held key/button.
A helper should refuse host execution, target a verified process/window, confirm foreground focus
before input, and bound key holds. Check existing guest Accessibility and Screen Recording access;
use normal guest permission/login UI when required, never disable authentication or edit privacy
databases. SSH access alone does not establish UI permission or an unlocked guest.

For a macOS helper using CoreGraphics input and window capture, capture the target window with
`screencapture -x -o -l <window-id> <path>`: `-o` removes shadow padding. Map coordinates from the
actual PNG dimensions to that same window's `CGWindowBounds`, including its origin and Retina
scale. Recapture after resizing, navigation, or process replacement.
Do not reuse coordinates from a resized image without converting them back to its source dimensions.
A main-window capture can omit a separate save or permission dialog. If input appears ineffective,
inspect the guest window inventory or capture the guest desktop before retrying; never substitute
a host-desktop capture.

Control, capture, and rendering are separate capabilities. A usable screenshot proves capture;
its contents still need visual inspection. Diagnose artifacts where the image is rendered, using
the same source and assets for comparisons. Keep host-UI availability separate from independent
guest access, and record any untested capability without blocking the ones that work.

## Authentication and user handoff

Treat viewer authentication, guest macOS login/unlock, and Roblox account sign-in as separate steps.
Complete the viewer and guest login yourself with the existing authorized guest credentials. Use
the normal UI; do not disable authentication or change credentials to avoid a prompt. Keep secrets
out of repository files, commands, URLs, and reports. If credentials are unavailable, identify that
specific missing access rather than assuming the user must handle every login.

Before asking the user to interact with the VM, verify that its desktop and the intended application
page are visible. A viewer connection dialog is not a connected desktop. Complete the normal
connection options and verify the rendered application before handoff. Authenticate each chosen
viewer normally; one viewer's connection does not authenticate another.

Reuse retained Roblox sessions and available authorized sign-in methods. If Roblox itself requires
a step the agent cannot complete, automatically open its normal sign-in or Quick Sign-in page in
the already-connected viewer and explain the exact remaining step. Do not request passwords in chat
or transfer session cookies. Likewise, open the guest's actual Assistant/MCP settings when a concrete
blocker requires user action. Continue independent work while waiting. After setup, close or minimize
only the task's viewer so unattended guest windows stay out of the user's way.

Where the user can reach no viewer, relay Quick Sign-in by code. Read the newest
`awaitQuickSignIn via polling: code=` line from Studio's log immediately before sending it: codes
expire after about two minutes and Studio logs each replacement. The user enters the code on a
device already signed in to Roblox. Confirm sign-in from the Studio start page before relying on
the runner.

## End of session for a retained VM

These steps apply only to a task-owned or configured retained VM. Finish or record the task blocker before shutdown; a progress update does not end the test session.

When the game work is done, save the authorized project artifacts, close Roblox Studio normally,
and **shut down the guest VM** so it is no longer running locally. Verify that Studio closed and the
VM is stopped. Do not leave the VM running or substitute a suspended/running state for the requested
shutdown. If an unfinished test must continue, report that explicitly rather than claiming shutdown.

**Do not tear down the sandbox's persistent state.** Do not uninstall Studio or Roblox, log out,
delete/recreate the VM, reset its disk, remove project files, clear caches/keychains, or erase its
settings/authentication as end-of-task cleanup. Closing Studio and powering off the guest are the
normal shutdown actions. Keep the VM, installed apps, signed-in accounts, files, configuration, and
SSH access available for another session. Do not publish or commit the authenticated image or keys.

At the next session, locate and start the existing VM with the same no-window/no-clipboard/no-audio
options. Discover its current IP rather than assuming the prior address, reconnect via SSH, and
verify the intended Studio/project. Create a replacement only when necessary and authorized; a new
session is not a reason to rebuild or ask the user to sign in again. Open the viewer automatically
only if normal authentication or another required user setup step is actually needed.

## Qualification for game research on an isolated runner

When research uses an isolated runner, qualify the guest browser/media path and the **published Roblox client** separately from Studio.
Browser/media viewing and published-client play each require ordinary input and usable captures
without host windows/focus/input interference. Studio MCP capability alone does not prove those
capabilities. Record each result separately. If qualification fails, keep the dependent work
incomplete; do not
silently revert to host interaction. Host-side read-only APIs may assist data retrieval/aggregation,
but must not become a workaround that opens host research/game windows.

## Studio MCP connection and input

Prefer the [built-in Studio MCP server](https://create.roblox.com/docs/studio/mcp) when the installed Studio and tool surface support it. Inspect tool schemas and connect to the verified editor. MCP input can avoid host keyboard/mouse injection; qualify any windows it launches separately. Run unattended or multiplayer clients in a runner whose window behavior is safe for the user's desktop.

If an installed isolated runner fails a capability, inspect and recover that capability before choosing another authorized environment. A local single-editor MCP fallback does not establish that multiplayer windows or guest rendering work. Keep evidence separate for input, capture, rendering, isolation, Studio Play, and a published client.

## Connect to the intended editor

On macOS installations, the stdio executable may be `/Applications/RobloxStudio.app/Contents/MacOS/StudioMCP`; discover the installed location before connecting.
Enable Assistant → … → Manage MCP Servers → Enable Studio as MCP server **yourself if disabled**.
This is part of the authorized setup, not a routine manual task for the user. If a concrete capability
blocker requires their help, open that page for them and explain the blocker. A setting enabled in another machine
or guest does not enable the local editor. Follow the [authentication procedure](#authentication-and-user-handoff):
complete viewer/guest login yourself and verify the desktop before any user handoff. Reuse Roblox
authentication and request help only for the specific remaining step you cannot complete. Never
transfer cookies or ask for credentials in chat.

Use `list_roblox_studios`, verify the target file/place, and pass its explicit `studio_id` to every
operation. Keep unrelated projects untouched. Use the installed Studio version's documented launch
arguments and verify the resulting editor inventory, not merely process creation. Record the
version in test evidence because it updates independently.

For a cloud-backed editor when isolated save/rejoin tests are required, the documented
[Studio command-line interface](https://create.roblox.com/docs/studio/command-line-interface)
accepts `--task EditPlace --placeId <verified-place-id> --universeId <verified-universe-id>`.
On macOS, `open -n -a /Applications/RobloxStudio.app --args` followed by those arguments
launches a cloud editor; confirm both `game.PlaceId` and `game.GameId` through MCP. Use `--task EditFile --localPlaceFile <absolute-path>` for a file.
Launch extra editors only inside the isolated runner. An ordinary local place file has
zero place/universe IDs and cannot establish cloud persistence coverage. Synchronizing
test source into a cloud editor does not publish it; keep fixture keys isolated and
discard those editor changes afterward unless publication is separately authorized.

The proxy can initialize and expose all tool schemas before Studio connects. Studio retries its
local WebSocket connection on an interval; terminating the proxy immediately can repeatedly return
`studios: []` even while the toggle is enabled. Keep the session alive and await a nonempty inventory
with a bounded timeout. Do not
infer a toggle failure from an empty inventory or ask the user to repeatedly toggle it.

A stdio client must handle notifications and responses sharing a read. With Python `select`, a
buffered text `readline()` can leave the response in a Python buffer while `select` waits for OS
bytes. Read binary chunks into a retained newline-delimited JSON buffer and match response IDs.
Keep transport errors and action failures distinct.

Keep one owned transport open throughout a sequential walkthrough instead of reconnecting for every
button, movement, and state read. Wait for tool schemas before editor discovery, use distinct request
IDs, and close the transport on failure or process exit. Reuse the project's transport owner.
Serialize control of one editor; avoid competing proxy processes
and overlapping input routines. A transport timeout does not establish a game failure, and must not
automatically replay an action that may already have completed. Inspect the visible state before
resuming normal controls.

### Discovery and setup failures

An empty inventory does not establish that MCP is disabled. The intended process may be waiting
on sign-in, a recovery dialog, Assistant initialization, or the proxy connection. Inspect that
editor's current UI. Resolve blocking dialogs, open **Assistant → Manage MCP Servers**, and inspect
the normal MCP setting before changing it. If remote pointer input cannot open Assistant, use its
native menu or the installed editor's shortcut configuration; inspect the current binding rather
than assuming a key. Restore any temporary binding afterward. Keep the proxy alive during bounded
discovery, then verify the intended editor with a read-only command against its explicit ID before
orchestration. Preserve unrelated preferences;
undocumented preference-file keys are not a stable setup API. This uses the normal
[MCP setup and connection checks](https://create.roblox.com/docs/studio/mcp).

A normal quit can stop at an unsaved-changes dialog. Verify closure before reopening, and avoid
forced termination or repeated duplicate launches. Multiple processes can show the same file or
have different authentication states. Preserve the working editor and retained credentials.

## Qualify input and capture

Verify client/server play, an actual game button, movement, and a viewport screenshot **in the runner**.
Also launch the maximum requested multiplayer clients there and confirm none appears on the host.
Confirm the resulting game state and that the user can continue using their desktop. Successful code
execution or single-client input alone does not establish complete isolation. Use `screen_capture` for the game viewport, not a host
screen recording that could include unrelated private content. Its image can be returned as an MCP
image block; save/decode that block directly instead of printing its base64 data.

If those captures are black while the guest desktop remains visible, use the qualified
[guest desktop viewer](#optional-guest-desktop-viewer) when appropriate. Keep capture failure
separate from rendering/asset acceptance and respect the user's chosen testing environment.

Inspect current tool schemas rather than guessing signatures. Use supported MCP tools and
[StudioTestService](https://create.roblox.com/docs/reference/engine/classes/StudioTestService) for
orchestration. Normal-input walkthroughs still require real movement, prompts, menus, and camera controls. Direct progression changes belong in separate edge-case fixtures.

Use the live `execute_luau` schema to select a supported `Client`, `Server`, or `Edit` context.
Read live UI, camera, and character state from the appropriate running context. A standalone command
may not share a gameplay module's initialized state; an empty module result alone does not prove
that the service stopped. Prefer replicated instance/UI observation or a bounded ordinary server
fixture for runtime state. Remove fixtures afterward and never advance progression for inspection.

### Device-simulated button coordinates

Configure device simulation in the **Edit** data model before starting Play. MCP rejects
Edit execution during Play with "Edit datamodel is not available in Play mode"; stop the
owned test, configure the device, and start a fresh test rather than targeting another editor.

Activate a phone/tablet with `StudioDeviceSimulatorService:SetDeviceAsync` before setting its
orientation. Read the current device list, choose the intended device, and verify the viewport.
If the simulated device extends beyond the editor viewport, set
`SetScalingModeAsync(Enum.DeviceSimulatorScalingMode.FitToWindow)` in Edit before Play.
This fits the preview without changing the chosen device resolution; record that resolution
separately from the scaled viewer image.

Read the resulting control state after a click; transport success does not prove
the intended control responded. Where direct VirtualInput is supported, the full-inset transform in
the [input coordinates](#input-coordinates-the-phone-notch-matters) maps the button center
correctly. Also check ancestor visibility and clipping, and scroll hidden controls into view first.
Verify selection, confirmation, and the server outcome; callbacks or remote calls are separate
integration evidence, not a substitute for player input.

Do not silently fall back to host client launches or native host HID automation if a capability is missing. Use a separately
authorized isolated machine when the runner cannot support the operation. Record the concrete blocker
and continue independent work. Keep Studio, simulated-device, persistence, and published-client
verification distinct; one does not establish another. Store reusable tools in the test tooling area
and keep screenshots, logs, temporary fixtures, and runner state ignored.

## Pending and partial test startup

A pending test call with its fixture installed can remain in Edit before Play begins. Inspect the
request, fixture, dialogs, and `get_studio_state` before recovery. For a solo test, when the original
request is still pending, its fixture is installed in the intended editor, and no dialog blocks it,
try the supported `start_stop_play(is_start=true)` once against that same `studio_id`. Wait for the
original request's result within its existing deadline; entering Play alone is not a passed test.
Do not inject a duplicate fixture, replay an ambiguous timed-out request, or start solo Play for a
multiplayer test. Clean up abandoned fixtures after resolving their test session.

For multiplayer tests, count actual connected players and inspect each process's data-model state.
A requested count or open window does not prove that every client joined. Keep startup and gameplay
deadlines separate; failure results include participants, readiness, positions, and encounter state.
Investigate the observed failure before a bounded retry, preserve its evidence, and keep every
client in the isolated runner. If a client opened the wrong data model, end the failed test, close
its task-owned client processes normally, and reopen the intended test editor only if needed.
Confirm editor identity and fixture cleanup before one fresh launch, then verify the actual joined
count. A restart is a recovery attempt, not proof of the startup cause or a reason for repeated retries.

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
prove fixture removal after restoring the game project. Delivery builds must reject all test trees.

## Optional guest desktop viewer

Use this optional fallback only when the configured guest and permitted browser support it, Studio viewport capture is unavailable or black, and the guest desktop renders a usable image. A hidden viewer is a normal remote-desktop client in
a background browser tab; it is not a second VM or a host-screen recorder. It can keep
showing the guest after the native Screen Sharing window closes. Closing the browser tab
ends that viewing connection, not the VM. Follow an explicit user request to use their
local Studio or a visible viewer instead.

### Connection requirements

Reuse an installed, trusted [noVNC](https://github.com/novnc/noVNC) client and
[websockify](https://github.com/novnc/websockify) proxy, or the available equivalent. Keep their
installation outside game checkouts and record actual versions in verification evidence.

- The configured VM is running without host windows, clipboard sharing, or audio. Its current
  private address and normal authenticated remote-desktop service are verified.
- The proxy serves only the viewer distribution and binds to a free **loopback** port. Its target
  is the intended guest endpoint, optionally reached through an existing SSH tunnel. It never
  serves the repository/home directory or exposes public forwarding for convenience.
- A permitted browser-control surface holds a background tab for the local viewer. Guest login
  uses the existing authorized credentials through the normal form; credentials never enter URLs,
  command lines, repository files, or reports. Clipboard transfer stays unused.
- A fresh image reflects a harmless guest action after any native viewer closes. A connection
  banner or unchanged frame does not establish live capture. MCP remains preferred for supported
  orchestration; viewer input stays inside the guest and uses current screenshots/state.
- Reconnection checks the existing viewer's connection state before restarting Studio or the VM.
  The tab stays hidden unless the user needs to sign in or wants to watch.

For the optional retained Tart/macOS setup above, load the runner identity and
derive the current guest address from Tart rather than a saved IP. Verify that noVNC and websockify
are installed at the shared tool path, port 6080 is unused, and the guest's authenticated VNC
service is reachable. Start the proxy as a tracked task-owned process:

```sh
source "$HOME/.config/roblox-studio/runner.env"
studio_tools_dir="$HOME/.local/share/roblox-studio/tools"
studio_guest_ip="$("$ROBLOX_STUDIO_TART" ip "$ROBLOX_STUDIO_VM")"
test -f "$studio_tools_dir/noVNC/vnc.html"
test -x "$studio_tools_dir/novnc-env/bin/python"
if lsof -nP -iTCP:6080 -sTCP:LISTEN | grep -q .; then
  echo "Choose another unused viewer port" >&2
  exit 1
fi
nc -z "$studio_guest_ip" 5900
"$studio_tools_dir/novnc-env/bin/python" -m websockify \
  --web "$studio_tools_dir/noVNC" 127.0.0.1:6080 "$studio_guest_ip:5900"
```

Open `http://127.0.0.1:6080/vnc.html?autoconnect=1&resize=scale&shared=1&bell=0` in the permitted
background browser and connect through the normal authentication form. If the installed tool path,
viewer port, or VNC endpoint differs, inspect the actual installation and runner configuration,
substitute verified values in the command and URL, and check them before launch. If an SSH forward
supplies the VNC endpoint, establish and verify it before starting the proxy. Confirm the listening
address and fresh guest frames, then retain the process handle for
the cleanup below. Use the installed tools' help when their options differ; this recipe follows
the [noVNC quick start](https://github.com/novnc/noVNC#quick-start) and
[websockify web-server option](https://github.com/novnc/websockify#additional-websockify-features).

### Security boundary

Loopback restricts the browser proxy to the Mac; it does not itself restrict the guest's
VNC listener. Verify the VM is on its intended private network and has no unintended
public forwarding. Local processes can still reach the proxy, and guest authentication
remains necessary. Serve trusted pinned client code, not an arbitrary hosted viewer.

An `http://` / WebSocket / direct-VNC connection does **not** add transport encryption. Do not describe it as end-to-end encrypted
or hardened. A stronger guest login and VNC carried through the existing SSH connection
can protect the connection when required by the chosen environment. A loopback SSH forward to the guest's `127.0.0.1:5900`, followed
by websockify targeting that local forwarded port, encrypts the Mac-to-guest leg; qualify
that variant before claiming it was tested. Preserve host-key verification and existing
access boundaries. Credential changes still require the user to perform the normal flow.

There is no third-party remote-desktop relay in this local recipe. However, screenshots
submitted to the assistant still pass through the active tool's normal image/model processing; do
not promise they remain exclusively on the Mac. A hidden tab is a convenience, not a
privacy or security guarantee.

### Evidence and cleanup

Successful desktop viewing does not qualify Studio-native capture, mesh rendering, asset
permissions, sound, or published-client behavior. Each capability needs its own relevant evidence.
A viewer can expose a rendering defect but cannot repair the renderer. Keep dated images and
recovery attempts in verification output; only a reusable decision rule belongs in this reference.

When switching away or ending the session, close the hidden tab and stop its websockify
process and any task-owned SSH forward. Verify their listening ports closed. Follow the
[retained VM lifecycle](#end-of-session-for-a-retained-vm):
save project artifacts, close Studio normally, shut down the VM, and preserve its disk,
installed software, login, preferences, and SSH setup. Never remove the VM to clean up a viewer.

### Guest file pickers

Remote input can arrive before a field gains focus or before its display updates. Focus the field,
wait for its active state, enter the text, and verify the rendered value before submitting or moving
fields. If bulk entry drops characters, correct the field and use the active tool's per-character
key input with brief intervals; verify completion, including the full path in a file picker.
Do not repeatedly submit incomplete credentials. For a preview or staged import, complete its options and verify the terminal result; opening a preview alone does not commit the import.
