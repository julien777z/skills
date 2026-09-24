# Background testing with Studio MCP

Prefer the [built-in Studio MCP server](https://create.roblox.com/docs/studio/mcp) for inspection,
playtest orchestration, player input, and viewport capture **inside the retained VM by default**.
Start the VM and reconnect automatically when it is stopped; use local Studio only for a concrete
VM limitation within existing authorization. Its input tools target the selected game data model, avoiding host keyboard/mouse injection.
However, input isolation is only one requirement: `StudioTestService:ExecuteMultiplayerTestAsync`
opened separate host client windows during verified two/four-player tests, and the user reported
that those windows obstructed their work. The earlier confirmation of no interference covered
single-client input, not client launch/window behavior. Do not generalize it to all testing.

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
operation. Keep unrelated projects untouched. On macOS, launching the Studio executable with the
absolute place path as a positional argument opened the intended file; `open -a` instead produced
a `file://` protocol launch that stayed on Home in the tested version. Verify the editor inventory,
not merely process creation. Record Studio's version because it updates independently.

For a cloud-backed editor needed for isolated save/rejoin tests, the documented
[Studio command-line interface](https://create.roblox.com/docs/studio/command-line-interface)
accepts `--task EditPlace --placeId <verified-place-id> --universeId <verified-universe-id>`.
On macOS, `open -n -a /Applications/RobloxStudio.app --args` followed by those arguments
opened the intended cloud place in the guest; MCP then confirmed both `game.PlaceId`
and `game.GameId`. Use `--task EditFile --localPlaceFile <absolute-path>` for a file.
Launch extra editors only inside the isolated runner. An ordinary local place file has
zero place/universe IDs and cannot establish cloud persistence coverage. Synchronizing
test source into a cloud editor does not publish it; keep fixture keys isolated and
discard those editor changes afterward unless publication is separately authorized.

The proxy can initialize and expose all tool schemas before Studio connects. Studio retries its
local WebSocket connection on an interval; terminating the proxy immediately can repeatedly return
`studios: []` even while the toggle is enabled. Keep the session alive and await a nonempty inventory
with a bounded timeout. In a verified case the editor appeared after about four seconds. Do not
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

### Restored macOS guest: enabled preferences still need a live Assistant

In the restored Tart guest running Studio 0.739.0.7390687, enabling the persisted preferences and
restarting did not immediately connect Studio. The verified recovery sequence was:

1. Preserve unrelated settings and scope changes to the signed-in guest account. The observed files
   were `~/Library/Roblox/AssistantSettings/<RobloxUserId>.json` with `"mcp-server": {"enabled": true}`
   and `~/Documents/Roblox/<RobloxUserId>/InstalledPlugins/0/settings.json` with
   `"Assistant-ExternalMCPEnabled": true`. Back up the original files inside ignored guest evidence.
   These are observed implementation details, not a stable public settings API; verify the installed
   version's actual files before using them. Do not replace whole files or transfer authentication.
2. Reopen the intended saved test build and resolve any normal recovery/save dialog. An empty proxy
   inventory is not proof that either preference is false. Avoid forced termination: it creates an
   auto-recovery prompt that can block initialization on the next launch.
3. Open Assistant. In this guest, the ribbon control and the default **Ask Assistant** shortcut were
   unreliable through Screen Sharing. **File → Customize Shortcuts**, searching `Assistant`, and
   assigning an unused guest-only key to **AI Assistant** opened the panel successfully. The pilot
   uses F6 for that action. Native menus/keyboard actions worked while embedded pointer controls did
   not reliably respond. Do not repeatedly click stale coordinates or assume a displayed hover is
   a successful activation. A layout reset was attempted during diagnosis but did not by itself
   establish a connection; do not recommend it as a routine prerequisite.
4. Keep the guest proxy alive for bounded discovery, then verify `list_roblox_studios` and execute a
   read-only command against the explicit guest ID. This sequence connected and returned the local
   intended build name and Studio version. It does not establish Play, rendering, or input support.

After bootstrap, close the task's remote viewer and use MCP over SSH. Keep the enabled preferences,
normal login, and useful guest setup for the next session; closing the viewer does not shut down the VM.

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

Use the live `execute_luau` schema to select `Client`, `Server`, or `Edit`. In Studio
0.739, `Client` successfully read `LocalPlayer.PlayerGui` and live camera/character
positions, despite older bundled device guidance saying execution was Edit-only.
Do not replace supported client inspection with guessed coordinates on that basis.
In the same version, requiring stateful server modules from a standalone MCP command
returned empty module tables while the live game and its instances were active.
Do not interpret that result as proof the gameplay service stopped. Use replicated
instance attributes/UI for observation, or a bounded ordinary server Script fixture
when inspecting the gameplay module's runtime state. Remove the fixture afterward;
do not advance progression to make an inspection succeed.

### Device-simulated button coordinates

Configure device simulation in the **Edit** data model before starting Play. MCP rejects
Edit execution during Play with "Edit datamodel is not available in Play mode"; stop the
owned test, configure the device, and start a fresh test rather than targeting another editor.

Activate a phone/tablet with `StudioDeviceSimulatorService:SetDeviceAsync` before
setting its orientation. In Studio 0.739, setting orientation from the default desktop
state failed with "orientation can only be set on mobile (phone or tablet) devices",
despite bundled guidance describing orientation preselection. Read the current device
list, choose the intended mobile device, set orientation, then verify the viewport.
If the simulated device extends beyond the editor viewport, set
`SetScalingModeAsync(Enum.DeviceSimulatorScalingMode.FitToWindow)` in Edit before Play.
This fits the preview without changing the chosen device resolution; record that resolution
separately from the scaled viewer image.

In Studio 0.739 with iPhone 17 Pro landscape simulation, `user_mouse_input` with an
`instance_path` returned success but selected a different spell card or missed the
intended target. Read the resulting selection/health/round; transport success does
not prove a click registered. The supported `UserInputService:CreateVirtualInput()`
worked in the Client data model with the button center transformed as
`AbsolutePosition + AbsoluteSize / 2 - GuiService:GetInsetArea(Enum.ScreenInsets.None).Min`.
Using only `GetGuiInset()` misses device safe areas. The fixture helper in
`../scripts/virtual_input.luau` uses this transform. Also check ancestor visibility and
clipping before sending actual mouse input.
Scroll hidden controls into view first. Verify selection, confirmation, and the
server outcome; do not call callbacks or fire remotes as a substitute. Guest-native
clicks also worked, but remain entirely inside the isolated runner.

Do not silently fall back to host client launches or native host HID automation if a capability is missing. Use a separately
authorized isolated machine when the runner cannot support the operation. Record the concrete blocker
and continue independent work. Keep Studio, simulated-device, persistence, and published-client
verification distinct; one does not establish another. Store reusable tools in the test tooling area
and keep screenshots, logs, temporary fixtures, and runner state ignored.

## Fresh editor discovery

A freshly opened local place did not initially appear in MCP inventory even after a bounded wait, although the baseline editor was connected. Opening that editor's Assistant → Manage MCP Servers showed the toggle already enabled; the editor subsequently registered without a toggle change. Check the correct process and open its setup page before asking the user to enable it again. Treat this as an observed recovery sequence, not proof that opening Settings is always required. Multiple Studio processes can show the same file; identify the actual connected data model and avoid duplicate launches. A termination request may open an unsaved-changes dialog rather than exit Studio, so verify process/window closure.

New Studio processes can also stop at sign-in while an existing editor remains authenticated.
In the retained VM, opening another local file through that editor's File menu still launched
a new process and did not avoid sign-in. Inspect the guest window before diagnosing an MCP
discovery failure. Preserve the working editor and retained credentials; close only unused
instances and use the normal visible-VM sign-in flow from the isolated-testing reference.
Do not repeatedly launch copies, log out the working editor, or copy session cookies.

## A queued solo fixture remains in Edit

In Studio 0.737, one repeated `StudioTestService:ExecutePlayModeAsync` call stayed pending with its fixture installed while `get_studio_state` still reported Edit. There was no permission dialog. An explicit MCP `start_stop_play(is_start=true)` started that same fixture; its `EndTest` result then returned successfully to the original call. Inspect the pending call and installed fixture before trying this recovery once. Do not inject another fixture or claim that Edit means the original request failed. This observation concerns a solo test; starting ordinary Play is not a substitute for the requested client count in a multiplayer test. Keep deadlines and clean up any abandoned fixture after resolving its test session.

## Roblox Jest through an existing editor

In Studio 0.737, Jest 3.20.1 needs privileged module-source access. Running its entry as an ordinary server Script failed before collecting tests with `lacking capability PluginOrOpenCloud`; dispatching through MCP in the Play server could read Source but failed with `loadstring() is not available`. `ServerScriptService.LoadStringEnabled` is [Not Scriptable](https://create.roblox.com/docs/reference/engine/classes/ServerScriptService); attempting to read or assign it in Luau reports that it is not a valid member. Do not repeatedly attempt that assignment or weaken game security to run a suite.

The verified path was a stopped, unpublished local editor: synchronize the dedicated test project, set the explicit test marker, and dispatch the disabled test entry through MCP's **Edit** context. That context supported `loadstring` and ran engine suites, including real Instance/CFrame assertions. `debug.loadmodule` was not enabled in this version. This is actual Roblox engine Jest in Edit, not a Play client/server simulation. Tests requiring live physics, replication, input, persistence, or multiple clients need their separate supported runner. Open Cloud uses its own privileged execution context and the serialized test project.

Give the project's Studio test runner a bounded wait, structured current-run results, and cleanup
in `finally`: restore the normal source tree and original test marker, remove all injected test and
authoring trees/packages, and leave Play stopped. Disable an Edit-only test entry for ordinary Play
so it cannot launch with insufficient permissions. Never parse a historical `all tests passed`
console line as the current result; Studio output can include old failures and passes. Keep result
attributes and current run identity authoritative.

Synchronize the complete test project's explicitly mounted trees. Copying packages while omitting
the suite can wait forever for an uninstalled runner. Verify the test entry before dispatch and
prove fixture removal after restoring the game project. Delivery builds must reject all test trees.

## Partial multiplayer startup

In the retained macOS VM with Studio 0.739.0.7390687, one two-client `ExecuteMultiplayerTestAsync` launch started a server and one player, while the second process logged `StartClient` followed by `EditFile` and opened the source file read-only. The fixture timed out waiting for the requested player count. Inspect the actual connected players and each process's data-model state; a requested count or open window does not prove that every client joined. Keep startup and gameplay deadlines separate, and return participant names, readiness, positions, and encounter state in fixture failure reports.

Closing guest Studio processes normally, preserving their files, and reopening the intended editor was followed by successful two- and four-client runs. The underlying startup cause remains unresolved; this is an observed recovery sequence, not a guaranteed fix. One later join timeout also preceded the passing runs, so preserve failed-run evidence and investigate recurrence rather than adding blanket retries. Extra client windows remained inside the VM throughout. Do not move a multiplayer test to the host to work around this failure.
