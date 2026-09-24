# Background testing with Studio MCP

Prefer the [built-in Studio MCP server](https://create.roblox.com/docs/studio/mcp) for inspection,
playtest orchestration, player input, and viewport capture **inside the retained VM by default**.
Start the VM and reconnect automatically when it is stopped; use local Studio only for a concrete
VM limitation within existing authorization. Its input tools target the selected game data model, avoiding host keyboard/mouse injection.
Input, window/focus isolation, capture, and rendering each need qualification. A tool that avoids
host pointer movement can still launch native client windows; that is not complete isolation.

Use guest MCP for inspection and source work as well as tests whenever it works. Run unattended Play,
multiplayer clients, device simulation, and any native game input inside the VM or a separately
authorized isolated machine. Do not resume host launches while restoring the runner. See
[isolated runner setup](isolated-testing.md). Qualify both input and window/focus isolation before
claiming the user can continue working normally.

If the user has authorized their existing local Studio as a fallback and the VM is unreliable,
use that one verified editor through MCP and supported VirtualInput. Recheck the affected VM
capability after repairs or updates and return to the VM once it works. An earlier guest rendering
failure is not a standing reason to avoid a now-working runner.
This authorization is specific to the existing single-window workflow: do not introduce
native host HID control or extra multiplayer client windows. Leave the host editor stopped
and restore temporary device simulation afterward. Preserve and shut down the VM normally.

## Connect to the intended editor

On macOS, the stdio executable is `/Applications/RobloxStudio.app/Contents/MacOS/StudioMCP`.
Enable Assistant → … → Manage MCP Servers → Enable Studio as MCP server **yourself if disabled**.
This is part of the authorized setup, not a routine manual task for the user. If a concrete capability
blocker requires their help, open that page for them and explain the blocker. A setting enabled in another machine
or guest does not enable the local editor. Follow the [authentication procedure](isolated-testing.md#authentication-and-user-handoff):
complete viewer/guest login yourself and verify the desktop before any user handoff. Reuse Roblox
authentication and request help only for the specific remaining step you cannot complete. Never
transfer cookies or ask for credentials in chat.

Use `list_roblox_studios`, verify the target file/place, and pass its explicit `studio_id` to every
operation. Keep unrelated projects untouched. Use the installed Studio version's documented launch
arguments and verify the resulting editor inventory, not merely process creation. Record the
version in test evidence because it updates independently.

For a cloud-backed editor needed for isolated save/rejoin tests, the documented
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
[hidden VM viewer fallback](hidden-vm-viewer.md) when appropriate. Keep capture failure
separate from rendering/asset acceptance and respect the user's chosen testing environment.

Inspect current tool schemas rather than guessing signatures. Use supported MCP tools and
[StudioTestService](https://create.roblox.com/docs/reference/engine/classes/StudioTestService) for
orchestration. Normal-input walkthroughs still require real movement, prompts, menus, cards, and
camera controls. Direct progression changes belong in separate edge-case fixtures.

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

Read the resulting selection, health, or round after a click; transport success does not prove
the intended control responded. Where direct VirtualInput is supported, the full-inset transform in
the [input reference](testing.md#input-coordinates-the-phone-notch-matters) maps the button center
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

## Roblox Jest through an existing editor

A suite that reads module source or compiles it needs an execution context with those capabilities.
A permission error during collection is a runner problem, not a failed gameplay assertion. Use the
project's dedicated test setup in a stopped, unpublished local editor when it requires privileged
Edit execution; never weaken production security to run it. Settings marked
[Not Scriptable](https://create.roblox.com/docs/reference/engine/classes/ServerScriptService)
cannot be assigned through Luau. Qualify the actual runner instead of repeating unsupported writes.

Engine tests in Edit establish engine behavior in that context. Live physics, replication, input,
persistence, and multiple clients need their own supported execution context. Open Cloud likewise
uses its own privileged context and serialized test project.

Give the project's Studio test runner a bounded wait, structured current-run results, and cleanup
in `finally`: restore the normal source tree and original test marker, remove all injected test and
authoring trees/packages, and leave Play stopped. Disable an Edit-only test entry for ordinary Play
so it cannot launch with insufficient permissions. Never parse a historical `all tests passed`
console line as the current result; Studio output can include old failures and passes. Keep result
attributes and current run identity authoritative.

Synchronize the complete test project's explicitly mounted trees. Copying packages while omitting
the suite can wait forever for an uninstalled runner. Verify the test entry before dispatch and
prove fixture removal after restoring the game project. Delivery builds must reject all test trees.
