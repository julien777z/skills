# Studio testing

Choose coverage for the affected behavior, qualify the available runner, then verify real input and the delivered result. Keep setup procedures conditional on the installed tools and the user's chosen environment.

## Coverage and verification

UI coverage follows the interface dependency declared in the entry point. Scale the tests to the actual task. A small UI edit needs focused visual/input verification; a complete game chapter needs a complete journey and relevant systems coverage.

Default to relevant automated checks and one focused Studio playtest. Reuse passing evidence when source, packages, and assets match the delivery build, following [delivery build acceptance](source-delivery.md#test-the-delivery-build-directly). Do not add a final walkthrough, reopen, or live-client launch after sufficient evidence already exists.

## Choose coverage for the change

Mobile testing is selective, not a required step in every iteration. For a game that supports both desktop and mobile:

- **UI changes:** test the affected screens and interactions on desktop and mobile, including layout, touch targets, safe areas, scrolling, and modal behavior. A shared UI component change should cover its affected consumers; it does not require replaying the whole game.
- **Significant changes:** include mobile coverage for an entire new map, a substantial world expansion, major gameplay/input changes, or changes to streaming/rendering/performance that can behave differently on mobile. Choose representative journeys and device checks for the actual impact.
- **Small shared-world fixes:** grass clipping, a misplaced prop, a sign support, or a local terrain seam normally need the grounding, blocking, boundary and surface audit below, desktop visual inspection and relevant walking checks only. Do not repeat the same verification on mobile when the geometry and behavior are shared and there is no device-specific concern.
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

## Keep the game's test helpers in its repository

Every step a check repeats has one tested helper, committed in the game repository's test tooling
area and built on the [studio_mcp](../scripts/studio_mcp/__init__.py) package for the transport:

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
helper, never worked around in the run that met it. Helpers are test support under `test-fixture`
and go through the game's source pull request with its checks. A brief for Studio work names the
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

Before clicking an underlying control, dismiss any current tutorial/modal overlay. Do not mistake a blocked test click behind an overlay for a broken control. Recheck the current round and modal after every transition.

## Coverage and visual inspection

For affected systems, exercise their normal actions and relevant failure boundaries: unavailable resources, invalid targets, timeouts, defeat, retreat, respawn, rewards, and save/rejoin where applicable. Preserve resources on invalidated actions according to the game's rules and prevent duplicate rewards.

Map coverage includes surface and traversal criteria when world content is affected. Inspect the real scene and UI at spawn, along principal routes, during encounters, after restoration/state changes, and at the finale. Verify animation movement and replication, asset loading errors, camera framing, target readability, and cleanup after repeated encounters. Check navigation around actual collision geometry rather than validating only waypoint coordinates.

Actively use the camera during the walkthrough. Periodically orbit left and right, change pitch, and zoom in and out through the supported range, then resume walking from the new view. At visual checkpoints, inspect the avatar and held objects from front, side, and rear during idle, locomotion, and relevant actions; circle signs and doorways to inspect supports, lettering, and approach visibility. Enter and leave a conversation or encounter from a changed camera heading and verify control/framing restore correctly. Respect intentionally locked cameras. Capture representative alternate angles and record that the camera was operated; static editor views and a fixed-heading input driver do not substitute for this coverage. **An arrangement is checked in world terms**, whoever runs the check: a formation, placement, facing or spacing is asserted from world positions and facing relative to what the characters or objects face, such as two guards meant to flank a gate standing side by side across its width rather than one behind the other along the path to it, and then shown in a capture from where the player sees it. How it projects into one camera view proves nothing, since a single view hides depth along its own line of sight.

When the game supports normal camera-orbit input, press the right mouse button, allow a frame for the camera to lock the cursor, then use `VirtualInput:SendMouseDelta()` while locked. `SendMousePosition()` positions the pointer; use relative motion for locked-cursor camera controls. Assert that the camera actually changed and the character stayed still. Release the mouse button in failure cleanup as well as on success. See [VirtualInput](https://create.roblox.com/docs/reference/engine/classes/VirtualInput).

When mobile coverage is warranted by the change, use Studio's device simulator to test the touch branch and actual interactions. Confirm that touch input was delivered, that affected scrollable content moves, and that movement controls do not overlap interactive UI. Record the simulated device and safe viewport; do not claim physical-device performance from an emulator.

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

Keep a concise latest-results report plus enough raw evidence to explain meaningful failures and fixes. Record the tested revision and any publication outcome. Separate verified behavior from untested internet latency, physical-device performance, estimates, or remaining external blockers.

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

Studio work runs in an isolated runner: a Tart VM on a macOS host, the container runner below on Linux. The user's own desktop Studio is not the runner, even for an operation that sends no input, unless the user chooses it as described below, since opening a place, building or capturing still launches windows and takes focus there; a supported Studio MCP operation that avoids moving the host pointer does not change that. Qualify editor identity, input, capture, rendering, and window/focus isolation separately before claiming unattended testing is safe.

**On the Tart runner, each game has its own VM**, named for the game, so one game's editors, settings, files and memory never land on another game's tests. When the game in hand has a configured VM, reuse its installed Studio, authentication, and tooling; when it has none, create it as [Add a VM for a game](#add-a-vm-for-a-game) says, without asking. Verify the intended place before acting, and coordinate exclusive control of the game's VM between the sessions working on that game. Start a stopped runner when needed, discover its current address, and leave it as [Leave the shared runner as you found it](#leave-the-shared-runner-as-you-found-it) says. An unavailable isolated capability, or a runner lock another session holds, leaves only the operations that need the runner waiting; every other part of the work — source, builds, world art, audio, tests and later plan steps — continues meanwhile. The [Linux container runner](#linux-container-runner) serves the one session its container runs, so it has no VM to name, create or lock. Never switch to the host's desktop Studio on your own. Inside the runner, install or update Studio and the tools the work needs, sign in with the retained session, and create the upload staging directory, without asking.

### Retained Tart/macOS runner

This example applies only when the host configures the shared values in `~/.config/roblox-studio/runner.env` (`ROBLOX_STUDIO_TART`, `ROBLOX_STUDIO_SSH_USER` and `ROBLOX_STUDIO_SSH_KEY`) and each game's own in `~/.config/roblox-studio/games/<game>.env` (`ROBLOX_STUDIO_VM`, its VM's name, `ROBLOX_STUDIO_KNOWN_HOSTS`, that VM's pinned host key, and `ROBLOX_STUDIO_EDITORS`, how many editors its VM keeps for checks to run in at once). **The game's name**, `<game>` below, is `ROBLOX_STUDIO_GAME` when set, or else the name of the folder holding the main checkout of the repository the command runs in, so every worktree of one game reaches the same VM; a bare or submodule checkout sets `ROBLOX_STUDIO_GAME`. Shared tools and keys live outside game checkouts. Discover the configured machine; do not assume its name or address from another session. **A game's VM is named `<game>-vm`**, such as `example-game-vm`. **Every session working on the game shares the VM's locks**, each named from the `ROBLOX_STUDIO_VM` its game's file sets, so a VM named otherwise keeps working through that file:

| Key | Held for |
| --- | --- |
| `<vm>/editor-<n>`, one per slot | One check in that slot: its Play sessions, its captures, its VM folder and its code sync. A check takes whichever slot comes free first with `acquire_editor_lock` |
| `<vm>` | Work on the whole VM: starting, stopping, restarting or resizing it, updating Studio, signing in, renaming. `acquire_runner_lock` takes it and then every editor's key, so the work starts once no check holds an editor; the key alone holds off no check and launches no editor |
| `<vm>/focus` | A step that reaches only the VM's frontmost window, held through `focused_input` for that step alone: an editor launch until the editor registers, and a click or capture another editor's window would take |

A rename holds the locks on both the old and the new name, in the order `agent-lock` sets for several keys, through `tart rename`, the settings-file update and moving the host-key pin to the new name, confirmed by a `runner_ssh.sh hostname` that answers; never rename another session's VM while it is in use.

```sh
runner_ssh="<installed roblox-studio skill>/scripts/runner_ssh.sh"
eval "$("$runner_ssh" --describe)"   # the game's resolved values, from inside its repository
"$ROBLOX_STUDIO_TART" get "$ROBLOX_STUDIO_VM"
# Start only when stopped, as a launchd job, so the VM outlives every agent session and turn:
job="roblox-studio.runner-vm.$ROBLOX_STUDIO_VM"
state="$HOME/.local/state/roblox-studio"
mkdir -p "$state"
cat > "$state/$job.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>$job</string>
  <key>ProgramArguments</key><array><string>$ROBLOX_STUDIO_TART</string><string>run</string>
    <string>$ROBLOX_STUDIO_VM</string><string>--no-graphics</string><string>--no-clipboard</string>
    <string>--no-audio</string></array>
  <key>StandardOutPath</key><string>$state/$ROBLOX_STUDIO_VM.log</string>
  <key>StandardErrorPath</key><string>$state/$ROBLOX_STUDIO_VM.log</string>
</dict></plist>
PLIST
launchctl bootout "gui/$(id -u)/$job" 2>/dev/null
launchctl bootstrap "gui/$(id -u)" "$state/$job.plist"
launchctl kickstart "gui/$(id -u)/$job"
"$ROBLOX_STUDIO_TART" ip "$ROBLOX_STUDIO_VM" --wait 180   # wait until the VM has an address
```

Reach the VM only through [runner_ssh.sh](../scripts/runner_ssh.sh), which resolves the game, reads
`runner.env` and the game's file, refuses a game with no VM configured rather than reaching another game's, and
finds the VM's address through Tart on every call, so no shell variable has to carry the target from one command to
the next. The runner's Studio MCP is `runner_ssh.sh /Applications/RobloxStudio.app/Contents/MacOS/StudioMCP`,
spoken over stdio: give an MCP client that command.

Drive the runner's Studio from scripts through the [studio_mcp](../scripts/studio_mcp/__init__.py) package, which every game uses
from the installed `roblox-studio` skill's `scripts` folder, put on `sys.path`, importing only the names its
`__init__.py` exports (`from studio_mcp import Studio, open_place, ...`); no game keeps its own MCP client or copies
one of these mechanisms. Each `Studio` holds its own MCP session through `runner_ssh.sh`, and the module has no shell
command line. Every call that reaches the VM first confirms, once, through `agent-lock` that the caller's receipt
owns the game's VM or one of its editors, renewing it, and the process keeps that receipt's locks renewed while it runs,
so a call takes as long as its own timeouts allow. Project and place file names use only letters, digits, `.`, `_` and `-`,
starting with a letter or digit.

| Call                                                                                          | What it does                                                                                                                                                                                                                 |
| --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `acquire_editor_lock(lock_receipt, owner, activity, wait=LOCK_WAIT)`                          | Takes whichever of the game's editors comes free first for a check and returns the acquire report, whose `expired_owner` names a predecessor whose leftovers must be stopped first |
| `acquire_runner_lock(lock_receipt, owner, activity, wait, priority=False)`                    | Takes the whole VM, its own key and then every editor's, writing each editor's receipt beside `lock_receipt`; `priority` for work that lets the waiters in |
| `release_runner_lock(lock_receipt)`                                                           | Releases the editor, or the whole VM, a receipt holds, telling `agent-lock` it is idle, so the caller first closes every editor and process the segment started                                                              |
| `runner_lease(lock_receipt)`                                                                  | Renews the receipt's locks and keeps them renewed while the process runs, returning the runner's configuration and the editor the receipt holds (`None` for the whole VM) as `{"config", "editor"}` |
| `editor_slots(config)`                                                                        | The game's editors, each with its lock key and VM project folder (`editor-<n>`)                                                                                                                                           |
| `focused_input(lock_receipt, activity, wait)`                                                 | Holds the VM's focus lock for a step that reaches only the frontmost window; `open_place` and `open_cloud_place` hold it themselves |
| `open_place(project, place, out_dir, lock_receipt, registration_wait)`                        | Copies a built place into the VM under `studio-places/<project>/`, launches an editor for it and returns a `Studio` once the editor registers and its Edit data model runs code, over the connection that saw it register. Studio MCP names an editor by its place's file name alone, so it refuses a place whose file name any project already has open |
| `open_cloud_place(place_id, universe_id, out_dir, lock_receipt, registration_wait)`           | Opens a published place in an editor the same way, returning it once its Edit data model reports that place and universe; it is never saved or published from there                                                          |
| `close_place(project, place, lock_receipt)`                                                   | Ends the editor that has exactly that copy open and deletes the copy; raises, keeping the copy, when the editor stays open                                                                                                   |
| `close_cloud_place(place_id, lock_receipt)`                                                   | Ends, without saving, the `EditPlace` editors on exactly that place; raises when one stays open                                                                                                                              |
| `stop_guest_processes(pids, lock_receipt)`                                                    | Sends SIGTERM, waits, sends SIGKILL to what remains, and returns the IDs that survive, such as the test server and clients a multiplayer test left                                                                           |
| `listed_editor_ids(connection, lock_receipt)`, `new_editors(known, connection, lock_receipt)` | A snapshot of the editors listed before a launch, waiting out a new connection's empty list, and the editors listed since on the same connection, such as a multiplayer test's windows                                       |
| `listed_place_editors(project, place, connection, lock_receipt)`                              | Lists the editors named for a project's place copy once Studio MCP lists one, or none when no editor process has the copy open |
| `guest_screenshot(path, lock_receipt)`                                                        | Saves the VM's whole screen, for a failure the editor cannot capture                                                                                                                                                      |
| `run_in_runner(command, lock_receipt, timeout)`                                               | Runs a shell command in the VM                                                                                                                                                                                            |

Each lock call raises `RunnerLockBusy`, a `RuntimeError`, when the lock stays held for the whole wait, so a step
can give its editor back and retry. An open holds the VM's focus lock from the launch until the editor
registers, so editors launch one at a time: editors starting together each refresh the account's shared sign-in
token, and Roblox revokes the session when one rotated token is used twice, which signs every editor out; several
launching at once also starve the VM until none registers.

When the editor either open call launched never registers or never answers in its Edit data model, the call saves
the VM's screen under `out_dir`, closes the editor and raises; any other failure once the launch starts closes
the editor and raises. A `Studio` executes Luau, captures, optionally from a `CameraView` of a camera position and the
point it looks at, reads
the console, sends keys, holds a key for a duration (`hold_key`), and clicks a button by its instance path through
the bundled VirtualInput helper, which `run_input` binds as `Input` for other input fixtures;
`Studio.tool(name, arguments)` calls any other Studio MCP tool on that editor, first waiting for a new connection to
list it. `luau_string_literal` quotes a value for Luau code a helper builds.

An editor reaches Studio MCP through its built-in Assistant plugin, which connects to the VM's `StudioMCP` helper
whenever a session has one running. A starved VM can hold that connection for minutes and raise Studio's
"*plugin* is not responding" alert, and while the alert is open the editor does not answer. Every wait for an editor
to list, whether registration in either open call, `listed_place_editors`, or a `Studio`'s first call on a new
connection, answers those alerts with their keep-waiting button once a minute, logging each one it answers, and waits
out a held connection, up to 260 s for an editor already running. An editor still unlisted then raises an error naming
the VM's load and whether each Studio process holds a connection to the helper.

**No Studio operation reaches the host by falling back.** A client, helper or MCP server that picks its target
from a variable or setting and drives the host's Studio when that target is missing is not a runner route, even
for a read: a game repository's helper run with its runner variable unset, or the harness's own Studio MCP tools
connected to this machine. Before a connection's first call, confirm its target: `list_roblox_studios` names the
editors `"$runner_ssh" 'pgrep -fl RobloxStudio'` shows in the VM, never the host's.

An agent harness ends what a session or a turn started when it exits, whether the command ran in
the background, under `nohup` and `disown`, or in a session of its own, and the VM stops with its
`tart run`; a runtime that runs each turn as its own process does that at every turn's end. launchd
runs the job above, so no agent process owns `tart run`: `launchctl print "gui/$(id -u)/$job"`
shows it running, and `ps -o ppid=` on `tart run` shows `1`.

Verify SSH host keys, the intended VM editor, and the source/place before running tests. The no-graphics, no-clipboard, no-audio options keep the VM from opening a host window or sharing clipboard/audio. Store versions and qualification evidence outside this skill. Do not provision or reset a working retained VM as routine setup.

#### Size the host for its VMs

A running VM holds its whole memory allocation on the host, and its disk image grows as the VM
writes. **A VM's default size follows its editors**: 6 CPU cores, a 50 GB disk, and 4 GB of memory for
the VM plus 4 GB for each editor its game's file names, since an editor on a game's built place
holds 3 to 4 GB in the VM, and Play adds little to it; a VM below that swaps once its editors are
all open. A VM's free page count reads near zero while its inactive pages hold the slack, so judge
its memory by swap use and load, never by free pages alone.

**Read the host's actual free memory before starting a VM or raising its memory**, not its total
(`vm_stat` for free and compressed pages, `sysctl vm.swapusage` for swap). Start one only while every
running VM's memory fits in what the host has free, leaving 8 GB for the host itself; a host already
swapping pages the VM's memory out, and the VM then stalls whatever its own free memory reads:
SSH takes tens of seconds, the load average climbs past the VM's cores, editors stop answering
Studio MCP and Play sessions drop. Create a VM only while the host's free disk exceeds its disk size
plus 20 GB. macOS runs at most two macOS VMs at once, whatever the host's size. When the host cannot
back a VM and another session's VM is up and idle, shut that idle VM down first, as
[End of session for a retained VM](#end-of-session-for-a-retained-vm) says of when a VM counts as
idle and how to shut it down; propose a
size change only when the host is still short.

**A VM's size is a setting the user approves, never a wall.** When the measured need differs from the
VM's size, or the host still cannot back it after that, propose the change to the user with the measurement: the
VM's memory with its editors in Play, the host's free memory and swap, and what else holds the
host's memory. Once they approve it, take the whole VM with `acquire_runner_lock(priority=True)`,
stop the VM, run `tart set <vm> --memory <MB> --cpu <cores>`, start it as above and confirm the new
size with `tart get <vm>` and Studio signed in. Meanwhile the game's Studio work waits only on what
the VM cannot run, and the rest of the work continues; work never stops a VM whose lock it does not
hold.

#### Add a VM for a game

When `runner.env` exists but the game has no `games/<game>.env`, create the game's VM and continue
the work there, without asking: a game's VM is part of the runner setup the work already has. The
same procedure finishes a VM whose game's file records `ROBLOX_STUDIO_QUALIFIED=0`, resuming at
the first step whose check fails; no other Studio work runs in that VM until it does. A file without the
variable belongs to a qualified VM and keeps working as it is. The game's VM name below
is `<game>-vm` for a VM this procedure creates, or the `ROBLOX_STUDIO_VM` its file sets when
resuming. Each step runs holding the whole VM, taken for that step, and before
acting checks again that the step is still needed. Until step 3 has written `games/<game>.env`,
the step takes the VM's own key, the game's VM name, directly through `agent-lock`, since
`acquire_runner_lock` reads the game's file to find its keys and a VM not yet set up has no editors
to hold; once the file exists, the step takes `acquire_runner_lock`. Each step ends with its check:

1. **Clone** the retained Cirrus Labs base image, or a stopped qualified VM whose lock this session
   holds for the clone together with the game's, both taken in the order `agent-lock` sets for
   several keys, with `tart clone <source> <game>-vm`, within the budget above. `tart set` the
   budgeted CPU, memory and disk, then start it detached as above; `tart ip --wait` returns its
   address. A clone of a qualified VM keeps its installed Studio, Roblox player, VM settings,
   signed-in session and the shared SSH key's `authorized_keys` entry. A clone of the base image
   gets its automatic desktop login confirmed as step 2 of
   [Provision a runner when none exists](#provision-a-runner-when-none-exists) says, and the
   existing shared public key appended to the VM's `authorized_keys` through `tart exec -i`;
   the shared key and `runner.env` stay as they are, since every other game's VM uses them.
2. **Pin its host key.** Record the clone's host key under the game's VM name in
   `~/.config/roblox-studio/games/<game>_known_hosts` and verify its fingerprint through
   `tart exec`, as step 3 of provisioning says, then confirm a `BatchMode=yes` login.
3. **Write `games/<game>.env`** with `ROBLOX_STUDIO_VM`, `ROBLOX_STUDIO_KNOWN_HOSTS`,
   `ROBLOX_STUDIO_EDITORS`, the number of editors the VM was sized for in step 1, and
   `ROBLOX_STUDIO_QUALIFIED=0`; `"$runner_ssh" --describe` from the game's repository prints them,
   and `"$runner_ssh" hostname` answers from the new VM. These are the only files written on the
   host.
4. **Prepare the VM.** For a clone of a qualified VM, remove another game's places, captures and
   task folders it carried, and close any editor its last session restored; the runner's persistent
   setup stays. For a clone of the base image, install Studio as step 4 of provisioning says.
   Either way, [turn off the daemons a headless VM does not use](#turn-off-daemons-a-headless-vm-does-not-use)
   and check them as that section says.
5. **Sign in and qualify** as [authentication](#authentication-and-user-handoff) and
   [Qualify input and capture](#qualify-input-and-capture) describe, installing the
   [geometry buffer cap](#cap-studios-geometry-buffers-in-a-tart-vm) and the runner's
   [fixed graphics quality](#leave-the-shared-runner-as-you-found-it) and confirming both in the
   editor first; a session cloned signed in is confirmed from Studio's start page, not assumed, and
   that start window is closed once read.
   Release the lock before asking the user for a sign-in code, and take it again, with its receipt
   checked and the VM's state read back, before continuing. Then set
   `ROBLOX_STUDIO_QUALIFIED=1` in `games/<game>.env`.

#### Provision a runner when none exists

When `runner.env` is absent, ask the user through the question tool whether to install Tart and set up the runner, before any Studio work; once they agree, provision it for the game in hand and continue the work there. Each step
ends with its check:

1. **Install Tart** through the package manager the host uses. When that route fails, install the
   official [GitHub release](https://github.com/cirruslabs/tart/releases): verify the archive
   against the release's checksum file, unpack it outside checkouts, confirm the app's code
   signature, and run its `--version`.
2. **Create the VM** with `tart clone` from a Cirrus Labs macOS base image, named
   `<game>-vm`, then `tart set` its CPU, memory, and display before the first boot, within
   [the host's budget](#size-the-host-for-its-vms). Start it with the options above and
   `tart ip --wait <seconds>` for its address; `tart list` shows the stopped VM afterward. The
   VM must log its desktop user in on boot, which everything run while the host is locked
   depends on: `defaults read /Library/Preferences/com.apple.loginwindow autoLoginUser` in the VM
   names that user on a Cirrus Labs image.
3. **Pin SSH before trusting it.** Generate a dedicated key in `~/.config/roblox-studio/`. Record
   the VM's host key under the VM's name, not its address, since `runner_ssh.sh` looks it up by
   that name and Tart can give the VM a new address (`ssh-keyscan -t ed25519 <address>` with its
   first field replaced by the VM name), then compare its `ssh-keygen -lf` fingerprint with the
   one `tart exec <vm> ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub` reports through the guest
   agent; a mismatch stops setup. Append the public key to the VM's `authorized_keys` through
   `tart exec -i`, so no VM password passes through a command line, and confirm a `BatchMode=yes`
   login. Write the three shared values to `runner.env` and the game's to `games/<game>.env`, with
   `ROBLOX_STUDIO_QUALIFIED=0`.
4. **Install Studio in the VM** from Roblox's official macOS installer image. Mount it there,
   confirm the installer's code-signing team matches the host Studio's, and `open` it in the
   signed-in VM session; the check is `/Applications/RobloxStudio.app` in the VM and Studio's
   window in a VM capture. Then
   [turn off the daemons a headless VM does not use](#turn-off-daemons-a-headless-vm-does-not-use).
5. **Sign in, enable MCP, and qualify** as [authentication](#authentication-and-user-handoff),
   [direct VM control](#direct-vm-control) and
   [Qualify input and capture](#qualify-input-and-capture) describe, with the
   [geometry buffer cap](#cap-studios-geometry-buffers-in-a-tart-vm) and the runner's
   [fixed graphics quality](#leave-the-shared-runner-as-you-found-it) set and confirmed in the
   editor; qualification includes a capture of a large place drawing its meshes correctly.
   Then set `ROBLOX_STUDIO_QUALIFIED=1` in `games/<game>.env`.

#### Add the published Roblox player

Playing a published experience needs the Roblox player in the VM, which Studio does not include.
Add it to any runner that lacks `/Applications/Roblox.app`, newly provisioned or retained. Each step
ends with its check:

1. **Download the macOS build in the VM.** Roblox's web download link serves the Windows
   installer to a client that is not a browser, so read `clientVersionUpload` from
   `https://clientsettingscdn.roblox.com/v2/client-version/MacPlayer` and download
   `https://setup.rbxcdn.com/mac/arm64/<clientVersionUpload>-RobloxPlayer.zip`; `file` reports a
   zip archive.
2. **Verify and install it.** Unpack it with `ditto -x -k`, then confirm that
   `codesign --verify --deep --strict` passes, that its team matches that of the VM's Studio, and that
   `spctl -a -vv` reports a notarized Developer ID. Copy it to `/Applications/Roblox.app`; opening
   it shows its sign-in page. It registers itself as a login item.
3. **Sign it in by QR code.** Choose Sign In, then QR code. A code expires in about two minutes,
   so capture it just before the message that shows it, show that capture as `share-media`
   says, then ask through the question tool for the user to scan it, with a Done option, one for
   a new code and one for later. A new-code answer or a timeout captures a fresh code and shows it
   again before asking again. A prompt asking the account to accept something goes to the user,
   as [authentication](#authentication-and-user-handoff) says.
4. **Launch and qualify it.** `open "roblox://experiences/start?placeId=<place id>"` in the VM
   starts an experience. Qualify input and capture on a neutral place, as
   [direct VM control](#direct-vm-control) describes, before relying on it, and quit the
   player afterward.
5. **Turn off the Dictation shortcut in the VM.** A Cirrus Labs image enables it, and held game
   keys can open Dictation instead of moving: set symbolic hot key 164 to disabled in
   `com.apple.symbolichotkeys`, then run `activateSettings -u`; holding a movement key in a game no
   longer opens Dictation.

The player ignores `SIGTERM`, and quitting it can leave a game running in its `-launchToTray`
process, so a process listing does not show whether a game is open. Stop it with
`pkill -KILL -x RobloxPlayer` and confirm from a VM capture that no game is on screen; the tray
process restarts at once and is out of any experience.

#### Cap Studio's geometry buffers in a Tart VM

On a Tart macOS VM, Apple's paravirtual Metal driver keeps only the low 16 bits of an indexed
draw's base vertex. Once a Studio session has loaded more than 65,536 vertices into one of its
shared geometry buffers, later meshes are drawn with other meshes' vertices and show as stretched
wedges and black slabs, while small places look fine. The VM has no OpenGL fallback
(`Failed to init graphics mode 4-OpenGL`). Cap Studio's geometry buffers in the VM's
`~/Library/Roblox/ClientSettings/ClientAppSettings.json`: `FIntGeometryBufferMaxBytesMesh`,
`FIntGeometryBufferMaxBytesModel`, `FIntGeometryBufferMaxBytesParts`,
`FIntGeometryBufferMaxBytesFCSkinned` and `FIntGeometryBufferMaxBytesFCStandard` at `524288`, and
`FIntSuperClusterFastClusterMeshVertexSize` at `60000`. That folder survives Studio updates. The
host keeps the source copy at `~/.config/roblox-studio/studio-client-settings.json`, and
`"$runner_ssh" 'mkdir -p "$HOME/Library/Roblox/ClientSettings" && cat > "$HOME/Library/Roblox/ClientSettings/ClientAppSettings.json"' < ~/.config/roblox-studio/studio-client-settings.json`
restores it while holding the whole VM. Before a rendering check, confirm the file is present and that
`settings():GetFVariable("GeometryBufferMaxBytesMesh")` returns `524288` in the editor. Studio reads
the file only when it launches, so an editor that reports another value, the game's warm editors
included, is closed and opened again before the check. With the cap
in place, a capture of Studio draws the scene correctly, so stretched wedges or black slabs in one
are a defect to diagnose, never a VM artifact to set aside. The published player in the VM
has the same driver limit and no such setting, so treat its 3D visuals as untested.

#### Turn off daemons a headless VM does not use

A Tart macOS VM runs system daemons for hardware and services it lacks, and some of them burn
CPU there, more the longer the VM runs:

- **`airportd`**, the Wi-Fi daemon. The VM has no Wi-Fi port. `bluetoothd`'s Wi-Fi coexistence
  code finds no Wi-Fi device, retries about every 11 seconds, and opens two new connections to
  `airportd` each time, which `airportd` never closes. `airportd` sends every network
  configuration event to each of them, so its CPU grows with uptime, past a full core after two
  days.
- **`audioanalyticsd`**, which processes the overload reports `coreaudiod` writes each time a
  Studio or player audio cycle misses on a loaded VM, tens of them a second.

Disable both in the VM, under the runner lock; launchd keeps the setting across reboots:

```sh
"$runner_ssh" 'for service in com.apple.airportd com.apple.audioanalyticsd; do
  sudo launchctl disable "system/$service"; sudo launchctl bootout "system/$service"; done'
```

Leave `bluetoothd` running: without it, `coreaudiod`'s Bluetooth audio plugin looks up a
`bluetoothd` service through launchd thousands of times a second. The check:
`sudo launchctl print-disabled system` lists both services as disabled, `pgrep -x airportd` and
`pgrep -x audioanalyticsd` find nothing, `en0` keeps its address, and `top -o cpu` shows neither
daemon and no busy `launchd`. A clone of a configured VM keeps the setting, so confirm it there
rather than repeat it. Another system daemon among the VM's busiest processes is handled the
same way: find its cause with `sample` and `log show --predicate 'process == "<name>"'`, disable it
only when nothing the runner uses depends on it, read launchd's failed lookups afterward, and add
it here.

### Linux container runner

A Linux host, such as a cloud agent container, can provide the Windows Studio build under Wine on an
Xvfb display. The project's setup script, the entrypoint of its setup or bootstrap folder, installs
Studio, Wine, the Wine prefix, and the toolchain. Start Studio through the project's launch command;
where the project defines none, start Xvfb and run `RobloxStudioBeta.exe` from its directory under
`wine`, with `DISPLAY` set to that display and `WINEPREFIX` to the prefix the setup script created.
A Studio window, its sign-in page or start page, in an X screenshot of that display shows the launch
succeeded. When `wine` or the Studio directory is missing, or the launch fails before that window
appears, rerun the setup script and launch again. Qualify the rest as [Qualify input and
capture](#qualify-input-and-capture) describes.

Studio's logs are in `"$WINEPREFIX/drive_c/users/$USER/AppData/Local/Roblox/logs"`. When they
report `Embedded Web Browser fail to load` (WebView2 failed to start under Wine), the embedded
sign-in is unavailable; sign in by code as [Authentication and user handoff](#authentication-and-user-handoff)
describes. When Studio offers only **Login via Browser**, Roblox has not given this installation
Quick Sign-in, and rerunning setup does not change that; report it to the user as a sign-in
blocker, naming the screen and the log line.

## Tart VM capabilities

For a configured Tart runner, use the official [quick start](https://tart.run/quick-start/) and the installed
CLI's help. Keep actual versions, image identity, resource allocation, and qualification results in
local configuration and verification evidence. Reuse the retained runner before provisioning one.

With the Tart options above, the VM does not create a host window, share the clipboard, or play test audio through the user's speakers. Transfer only the project/test files over
SSH, and invoke the VM's Studio MCP executable through `runner_ssh.sh`. Keep the VM proxy connection alive
long enough for Studio discovery, as [Connect to the intended editor](#connect-to-the-intended-editor) describes. Retrieve viewport captures and
structured results through that channel. Do not mount the whole home directory or transfer a Roblox
session cookie. Use normal Roblox authentication.

Follow [authentication and user handoff](#authentication-and-user-handoff) before presenting the
viewer. A toggle enabled on the host does not enable the VM.

Qualify the existing runner before relying on it, and recheck affected capabilities after Studio or
VM updates: confirm the [daemons a headless VM does not use](#turn-off-daemons-a-headless-vm-does-not-use)
are off, applying that section where they are not, authenticate, discover the intended Studio, load the current assets, run client/server
Play, operate a real button and movement, and capture the viewport without host windows or focus changes. For multiplayer coverage, also qualify the requested number of independent clients. Studio launching alone is not compatibility proof. Keep
dated qualification results in workspace evidence; do not recreate a working runner to requalify it.

Use MCP inside the VM wherever supported. Every other UI step in the VM uses input posted inside
it, as [Direct VM control](#direct-vm-control) says; never drive the host's game input. If Roblox rejects virtualization or
rendering/input is unreliable, attempt the applicable documented recovery and record the concrete
remaining limitation. Repair the runner itself, reinstalling Studio or recreating the VM where
that is what it takes; the Studio work waits for it rather than moving to the host's desktop.

When viewport capture fails but the VM desktop is usable, the optional
[VM desktop viewer](#optional-vm-desktop-viewer) provides background images and VM-native UI
without a visible Screen Sharing window. It describes connection requirements, authentication,
unencrypted-transport limitation, live-image check, and cleanup. It does not establish
that the VM renders game assets correctly.

Use the host's desktop Studio only when the user explicitly chooses it for the task. Then keep host input and extra client windows within their authorization, and set a local installation's host-Studio override, such as `ROBLOX_ALLOW_HOST_STUDIO=1`, only for that choice.

On a macOS host, native input and screen capture need Accessibility and Screen Recording granted to
the app the agent runs under, identified by the agent's process ancestry, not to its shell or
interpreter; macOS applies a new grant only after that app restarts. Check the grant with
`AXIsProcessTrusted()` and a test capture before driving input, and name that exact app when the
user must grant it.

## Direct VM control

On a configured macOS VM, host Screen Sharing, SSH into the VM, and input posted inside the VM are
separate capabilities. When the host viewer is unavailable, first check whether the retained VM is
running and SSH still reaches its normal signed-in desktop. Prefer MCP inside the VM for supported
Studio actions. **Input posted inside the VM is the default for every other UI step and needs no
user authorization**: a helper native to the VM operates the published Roblox player and the VM's
own UI over SSH without opening a host viewer. Where posted input cannot reach, use the hidden
viewer; Screen Sharing on the user's Mac is the last resort. Do not infer that the VM needs
rebuilding or new Roblox login.

Before relying on direct control, take a fresh capture, click a real visible button, hold and release
a movement key briefly, then capture the result. Permission checks and screenshots alone do not
qualify input: include this active test in the plan and execute it before calling control usable.
Verify the intended application, account, and place. Keep input and
capture entirely inside the VM, hold the editor's lock, and the focus lock for input through the
window system, and release every held key/button.
**A check needs no window in front; only input and captures through the VM's window system do.**
Studio MCP's input and the [VirtualInput helper](../scripts/virtual_input.luau) reach an editor's Client data model
whichever window is in front, and `screencapture -o -l <window-id>` grabs an editor's window while another covers
it, drawn as it is now, and a covered editor keeps running and drawing. So a check sends input through its editor's
own MCP connection, captures its own editor's window by ID, and records motion as a run of those window grabs. Input
posted through CoreGraphics or System Events, a whole-screen capture or recording, and an editor launch reach or take
the front window, so each runs as a short step under the VM's focus lock (`studio_mcp.focused_input`) while the
other editors' checks go on; a whole-screen capture serves runner diagnostics, never a check's evidence.

A helper should refuse host execution, target a verified process/window, confirm foreground focus
before input, and bound key holds. Check existing VM Accessibility and Screen Recording access;
use normal VM permission/login UI when required, never disable authentication or edit privacy
databases. SSH access alone does not establish UI permission or an unlocked VM.

Every setting and permission change in the VM is the agent's own step, never a request
to the user, since the agent controls the whole VM. Input posted inside the VM leaves the host's cursor alone and
is the route for the VM's UI work; a host viewer click moves the user's cursor and serves only where
posted input cannot reach. Read the VM's Accessibility list first: a Cirrus Labs image already
grants `osascript`, `sshd-keygen-wrapper` and `tart-guest-agent`, so `osascript -l JavaScript`
over SSH posts working CoreGraphics clicks. A missing grant is added in the VM's System Settings,
opened over SSH with `open "x-apple.systempreferences:com.apple.settings.PrivacySecurity.extension?Privacy_Accessibility"`
and operated by the agent through the [desktop viewer](#optional-vm-desktop-viewer), or, as the
last resort, Screen Sharing on the user's Mac when no hidden viewer is available, since posted
input is what the grant enables. Input posted inside the VM behaves like this:

- **Coordinates are points.** A HiDPI VM's captures have twice the pixels of its screen points;
  read `NSScreen.mainScreen.frame` and divide capture coordinates accordingly.
- **Studio can hold a stale window origin** and register clicks one title bar lower than they land.
  Set its window's position and size through System Events before clicking, and check with a
  visible control such as a ribbon tab.
- **Studio's widgets need a real click shape:** move the pointer toward the target first, and give
  each press a click count (`kCGMouseEventClickState`) from the HID system event source.
- **Studio's embedded web panels,** such as Assistant, take one click to focus and then toggle on
  each click; capture after every click rather than repeating one.
- The first `screencapture` over SSH raises a VM Screen Recording prompt for the SSH session;
  the agent approves it through the VM desktop viewer, or the host's Screen Sharing when no hidden
  viewer is available.

Tart's own `--vnc-experimental` endpoint returns black frames while the VM runs with
`--no-graphics`; a viewer connects to the VM's built-in Screen Sharing service on port 5900.

To turn the MCP server of the VM's Studio on or off, copy
[guest_studio_mcp.js](../scripts/guest_studio_mcp.js) into the VM and run
`osascript -l JavaScript guest_studio_mcp.js <studio-pid> on` over SSH. It finds each control by
its text or tooltip, so it does not depend on the VM's display size, and reaches the Assistant
panel wherever it is docked in the main window at its default width. It opens Assistant → … →
Settings → MCP Servers, sets the switch, closes the dialog, and retries a
pass that a dropped click spoiled. It exits nonzero unless the status bar reads the target state;
`osascript -l JavaScript guest_studio_mcp.js read` prints what it recognizes on screen when a step
fails.

For a macOS helper using CoreGraphics input and window capture, capture the target window with
`screencapture -x -o -l <window-id> <path>`: `-o` removes shadow padding. Map coordinates from the
actual PNG dimensions to that same window's `CGWindowBounds`, including its origin and Retina
scale. Recapture after resizing, navigation, or process replacement.
Do not reuse coordinates from a resized image without converting them back to its source dimensions.
A main-window capture can omit a separate save or permission dialog. If input appears ineffective,
inspect the VM window inventory or capture the VM desktop before retrying; never substitute
a host-desktop capture.

Control, capture, and rendering are separate capabilities. A usable screenshot proves capture;
its contents still need visual inspection. Diagnose artifacts where the image is rendered, using
the same source and assets for comparisons. Keep host-UI availability separate from independent
VM access, and record any untested capability without blocking the ones that work.

## Authentication and user handoff

Treat viewer authentication, the VM's macOS login/unlock, and Roblox account sign-in as separate steps.
Complete the viewer and VM login yourself with the existing authorized VM credentials. Use
the normal UI; do not disable authentication or change credentials to avoid a prompt. Keep secrets
out of repository files, commands, URLs, and reports. If credentials are unavailable, identify that
specific missing access rather than assuming the user must handle every login.

Authenticate each viewer the agent opens normally; one viewer's connection does not authenticate
another, and a viewer connection dialog is not a connected desktop.

**Roblox sign-in in a runner is the agent's to drive.** The user's part is entering the code on
their own device, and deciding any prompt that asks the account to accept something, such as
updated terms; everything else is the agent's.
Reuse a retained Roblox session first. **The session survives the VM**: Studio keeps it in the VM's
own cookie store and login keychain, so a restart, stop or resize of the VM leaves it signed in,
as a Mac's own restart does; a Studio that starts signed out after one has another cause. **Read the
cause from Studio's logs before signing in again**: the newest
`~/Library/Logs/Roblox/*Studio*.log` with `Authenticated : NO` and no later `YES`, and the error it
logged with it. `Token has been revoked` means Roblox ended the session because editors started
together, as the [studio_mcp open calls](#retained-tartmacos-runner) explain, so every Studio launch in the runner goes through `open_place` or `open_cloud_place`, which launch one
editor at a time, never through another route at the same moment. Fix what started the
editors together before asking for a new sign-in, or the next launches revoke it again. A Play
test's client process (`-playerEmulator`) runs as a test player and never signs in, so its log is
no sign-out. When Studio shows its sign-in screen, or its log reports `Authenticated : NO`:

1. **Choose Quick Sign-in yourself**, through input posted inside the VM as
   [direct VM control](#direct-vm-control) describes, or the Linux runner's display input.
2. **Read the code immediately before each asking**, a re-ask after a timeout included, since it
   expires in about two minutes: from the newest `awaitQuickSignIn via polling: code=` line in
   Studio's log when it is there, or from a VM capture of the code Studio shows.
3. **Confirm the code in the VM's own browser** when the VM's Safari is signed in to the same
   Roblox account, which `https://www.roblox.com/home` shows by its account name: open the
   confirmation page there with input posted inside the VM under its focus lock, enter the code
   and confirm. Go on to step 4 only when that browser is signed in to another account or none, or
   the page asks for something only the user can give.
4. **Ask through the question tool** for that one step: enter the code at
   <https://www.roblox.com/crossdevicelogin/ConfirmCode>, or in the Roblox app under More, then
   Quick Sign In, on a device already signed in to Roblox, with a Done option, one for a new code
   and one for later. A new-code answer, or a timeout, goes back to step 2. **A question that can
   reach the user minutes late**, such as one a delegated worker asks, goes first as its own
   question, asking the user to open the page and say when they are ready, with a Ready option;
   step 2 then reads a fresh code the moment they answer, under the VM's focus lock alone, and
   this step asks for it at once.
5. **Finish every later screen of the sign-in yourself**, such as choosing the account and its
   **Continue**, leaving an acceptance prompt to the user as the lead above says. Then
   confirm `Authenticated : YES` in the log and the account on Studio's start page before relying on
   the runner, then close that start window, which no editor slot owns.

Never ask the user to sign in through a viewer, Screen Sharing or any other route to the VM's
screen, and never ask for a password or a second factor: a screen inside the runner is one the
agent's input reaches. Do not transfer
session cookies. Continue independent work while the question waits.

## Keep the game's editors warm

The default check loop reuses the editors kept open in the game's VM on the game's built place, one
per slot of its pool, each with source synced into it over its own Studio MCP connection, so a
check costs a sync and a Play session rather than a build, a copy and an editor launch, and as many
checks run at once as the pool has slots.

- **Each slot of the pool has its own of everything a check touches.** Its lock key, its VM
  folder `studio-places/editor-<n>/` holding its place copy, its place file named for the slot, so
  `list_roblox_studios` tells the editors apart, its MCP connection, and its own Play session and test
  processes. `studio_mcp.editor_slots` names them; a check reaches only the slot its receipt holds,
  which `runner_lease` reports.
- **A slot runs one editor, and the VM no more than its pool has slots.** A check that needs a place
  of its own, such as a save or a fixture place, closes its slot's warm editor and opens that place in
  the slot's VM folder; the slot's next session reopens the warm editor. Before any launch, close
  every Studio process that belongs to no slot: a Studio start window left open, such as one a
  sign-in check read, and an editor of a place outside every slot's folder.
  A cloud place's editor, which has no VM folder, stays with the check that opened it.
  `open_place` and `open_cloud_place` refuse a launch while the VM already runs one editor per slot,
  one under a slot's lock in another project than that slot's, and one under the VM's own lock
  without its slots' receipts beside it: each extra editor takes a share of the VM's processors even
  when idle, which slows every check the VM runs.
- **Each check names its device, and leaves the default.** Set the device simulator a check needs in
  Edit before Play and read it back from the editor; once the check ends, return the editor to the
  game's default device and read that back too, so a later check never inherits a phone layout.
- **Open each once.** Build the place, open it with `studio_mcp.open_place` under the slot's
  project name as the step's first VM operation,
  and leave it open until the VM shuts down as [End of session for a retained VM](#end-of-session-for-a-retained-vm)
  says: it belongs to the game's VM, not to the task that opened it. A session finds its slot's
  warm editor with `studio_mcp.listed_place_editors`, which waits for a running warm editor to
  list, and uses it after confirming its place name; only an editor no process holds open is
  opened again.
- **Sync code over the editor's own MCP connection.** Read a digest of every script's source in
  the editor's Edit data model through `execute_luau`, compare it with the session's checkout, and
  write only the scripts that differ, creating a missing one under its parent; a file removed since
  the last sync, or a sync that failed, resends the whole code tree and prunes what the checkout no
  longer holds. Record in the editor which files the sync covered, so the next one sees a removal.
  On a warm editor holding about 600 scripts, comparing every digest takes about a second, one
  changed script about 3 seconds, and the whole tree with its prune about 30 seconds. Rojo's live
  sync does not fit a pool: its Studio plugin reconnects by itself only to a place with a place ID,
  which a local place file lacks, so connecting it takes clicks in the editor's front window, and the
  port it connects to is set only in its panel, so an editor left on Rojo's default port takes
  another editor's server and with it another checkout's code. The sync needs no window in front, no
  server in the VM and no copy of the checkout there.
- **Check the session's parts, and restore them with one command.** The editor can be gone, or its
  code behind the checkout; read the editor in `list_roblox_studios` and its sources as the bullet
  above reads them. The game's start command for an editor's warm session reopens a missing editor
  and syncs a present one.
- **Recover an editor left in Play inside its own lease.** A step that ended mid-Play can leave an
  editor that Studio MCP lists only as its Play session, which answers in no Edit data model. Stop
  Play through each entry listed under that editor's place; when none answers in Edit after that,
  close that editor's place copy and its test processes, and open it again. Only that editor is
  touched, and the other editors' checks go on.
- **Record what the session holds inside it**: the source revision, a manifest of the synced files
  and a digest of the built world, kept in the editor beside the session, so a later session reads
  whether the warm editor matches its checkout instead of guessing, and compares that manifest with
  its checkout before each check.
- **Confirm each sync before a check.** Read each written script's digest back from the Edit data
  model; a write call returning does not show that a change landed. Then start Play from that editor, and stop it when the check ends, closing the test processes that
  editor launched, which name it by their `-editpid`, never another editor's.
- **Rebuild only for what the sync cannot write.** Content the place's build step makes rather
  than a file maps, such as terrain or generated models; properties scripts cannot set, such as a
  mesh part's mesh; a project-file change to which containers are mapped; and a sync that
  cannot confirm its writes. Then rebuild the place, close the warm editor with
  `close_place`, and open the new build the same way. A check that left fixtures or state it
  cannot remove is a reason to reopen it too.
- **Delivery evidence still comes from the built place.** A warm editor proves behavior of the
  synced source; [delivery build acceptance](source-delivery.md#test-the-delivery-build-directly)
  still tests the artifact being delivered.

## Leave the shared runner as you found it

Every session working on one game shares that game's VM, so whatever one leaves behind lands on the next. The
game's warm sessions stay, as the section above says; no other task process
outlives any release of an editor's or the VM's lock, and before the task's last release its own files are gone and
every setting it changed reads back at the runner's configured value.

- **Settings.** A Studio or engine setting, such as `settings().Rendering`'s quality level or
  `UserGameSettings`, persists across editors and applies to every session in the runner. On the
  runner VM it is the runner's own configuration, which the agent manages: set it once to the value
  the tests need, leave it there, and confirm it when the runner is qualified. Graphics quality is a
  fixed level high enough to draw shadows, never Automatic, which draws less as the VM gets
  busier, so draw calls, triangles and shadows would move with load. A test that needs another
  value prefers a route scoped to itself, such as the device simulator's own profile, and otherwise
  returns the setting to the runner's configured value once it is done. On the host's own Studio
  the settings are the user's: record each value before changing it and restore it once the test is
  done. A change or restore is made from an Edit-mode editor and read back from a newly opened
  editor; one issued from a Play client, or never read back, has not happened. Granting a permission
  an operation needs is setup, not a setting to restore.
- **Apps reopened at login.** The VM reopens at login the apps its last session had open, from
  the list in `~/Library/Group Containers/group.com.apple.loginwindow.persistent-apps/persistantApps`,
  and Studio comes back from it as a start window no editor slot owns. The login window saves that
  list whenever an app launches, whatever its logout setting says, so the runner's configuration
  replaces it with an empty file nothing can rewrite: remove it, create it empty, and run
  `chflags uchg` on it, then `sync` before the next shutdown. Confirm it after a restart: no Studio
  runs before the first editor opens, and the file is still empty.
- **Files.** Everything the task copies or writes in the runner, such as places, captures, scratch
  output, worktrees and lock files, sits under a folder named for the task or its project and is
  removed when the task's runner work ends. `studio_mcp.close_place` deletes the place copy
  `open_place` made. The runner's persistent setup is not task output and stays, as the next section
  says, and so are the game's warm sessions: each editor, its place copy and the record of what it
  holds belong to the game's VM.
- **Resources.** Before a heavy run, such as Play, a multiplayer test or a device simulation, read the
  runner's free disk and swap (`df -h /` with `sysctl vm.swapusage` in a Tart VM, `free -h` in the
  Linux runner). Low disk or swap already in use is investigated before the run: remove what the task
  itself left and restore what it changed, and report what another session left without deleting it. A
  run that could run away gets a watchdog: a loop in the runner that reads the resident memory
  (`ps -o rss= -p <pid>`) of each process running the task's Play session every few seconds and,
  past a ceiling well under the runner's memory, stops that Play session, killing the process only
  when the stop does not take, so one run cannot push the shared runner into swap. A warm editor
  killed this way is brought back with the game's start command for that editor's warm session.

## End of session for a retained VM

These steps apply only to a task-owned or configured retained VM. A progress update does not end
the test session.

**A session's end leaves the VM running and the game's warm editors open.** When the game work is
done, save the authorized project artifacts and close what the session itself opened, as
[the section above](#leave-the-shared-runner-as-you-found-it) says. Shut a VM down and leave it
down in two cases only:

- the user asks for it;
- the host needs memory, and another session has a VM up that it has left idle: no lock on that VM
  or any of its editors is held now or shows a `last_activity_at`, in `agent-lock`'s `status` for
  that key, within the last 30 minutes. That
  idle VM is the one shut down. A free lock alone does not show idleness, because a session keeps
  its game's warm editors open and unlocked between the steps of its work, and a shutdown then
  closes the editors it is about to reuse.

A stop that starts the VM again in the same step, under the VM's own lock, is the VM's own
maintenance and not a shutdown: an approved resize, a runner repair and a configuration check that
needs a restart.

**Take a step only when the agent can undo it with the host locked.** The user's Mac can lock at any
moment, and a locked host refuses host-side clicks, screenshots and window control. Everything a
retained runner needs to come back runs without the host's screen: `tart run --no-graphics`, SSH,
the VM's automatic desktop login, Studio relaunched in the VM, input posted inside the VM,
and MCP inside the VM. Check that the route still holds before ending a session. Leave running, rather than closing, anything
whose restoration needs the host's screen or the user: a host viewer the user is using, Studio on
the host, a VM state only a host viewer could recreate, or a Roblox session that would need the
user to enter a new code. Powering the VM off in one of the two cases above is fine, because its automatic login brings the desktop back.

To shut a VM down, finish or record the task blocker first, hold the VM's lock, close Roblox
Studio normally, the game's warm sessions included, and run `"$runner_ssh" sudo -n shutdown -h
now`, then wait until `tart run` exits. `tart stop` can end the VM before it writes recent changes
to its disk, so a file or setting changed seconds before is lost; use it only when the VM does not
shut down. A restart is the same shutdown followed by `launchctl kickstart "gui/$(id -u)/$job"`. Verify that Studio closed and the
VM is stopped; do not substitute a suspended state for a requested shutdown. If an unfinished test
must continue, report that explicitly rather than claiming shutdown.

**Do not tear down the sandbox's persistent state.** Do not uninstall Studio or Roblox, log out,
delete/recreate the VM, reset its disk, remove its project setup, clear caches/keychains, or erase its
settings/authentication as end-of-task cleanup. A task's own copies and output are not that state;
[the section above](#leave-the-shared-runner-as-you-found-it) removes them. Keep the VM, installed apps, signed-in accounts, files, configuration, and
SSH access available for another session. Do not publish or commit the authenticated image or keys.

At the next session, locate the existing VM, starting it when it is stopped with the same
no-window/no-clipboard/no-audio options. Discover its current IP rather than assuming the prior address, reconnect via SSH, and
verify the intended Studio/project. Create a replacement only when a repair needs it, as [Tart VM capabilities](#tart-vm-capabilities) says; a new
session is not a reason to rebuild or ask the user to sign in again. Open a viewer automatically
when a UI step in the VM needs one that input posted inside the VM cannot give.

## Studio MCP connection and input

Prefer the [built-in Studio MCP server](https://create.roblox.com/docs/studio/mcp) when the installed Studio and tool surface support it. Inspect tool schemas and connect to the verified editor. MCP input can avoid host keyboard/mouse injection; qualify any windows it launches separately.

If an installed isolated runner fails a capability, inspect and recover that capability in the runner. A single editor answering MCP does not establish that multiplayer windows or VM rendering work. Keep evidence separate for input, capture, rendering, isolation, Studio Play, and a published client.

**Keep one StudioMCP running in the VM for as long as the VM runs.** Every editor reaches Studio
MCP through one helper port that the oldest running `StudioMCP` process holds, and when that process
exits every editor drops its connection and reconnects, losing the calls in flight from every other
session; Studio's log shows it as `Failed ws recv` on `localhost:13469`, and then `Connection
refused` while no process holds the port. Checks in several editors at once open and close sessions
constantly, so each session first makes sure a `StudioMCP` that never exits is running, started
detached with its input held open (`tail -f /dev/null | StudioMCP`) and its process recorded, as
`studio_mcp` does; it then holds the port while other sessions come and go.

## Connect to the intended editor

On macOS installations, the stdio executable may be `/Applications/RobloxStudio.app/Contents/MacOS/StudioMCP`; discover the installed location before connecting.
Enable Assistant → … → Settings → MCP Servers → Enable Studio as MCP server **yourself if disabled**;
in a VM, [direct VM control](#direct-vm-control) runs the bundled script for it.
This is part of the authorized setup and never a step for the user: the agent reaches the setting
itself, through input posted inside the VM or, for an editor on an unlocked host where the task
authorizes host input, through the host's own input. A setting enabled in another machine
or VM does not enable the local editor. Follow the [authentication procedure](#authentication-and-user-handoff):
complete viewer/VM login yourself and sign in to Roblox as that section says.

Use `list_roblox_studios`, verify the target file/place, and pass its explicit `studio_id` to every
operation. Keep unrelated projects untouched. Use the installed Studio version's documented launch
arguments and verify the resulting editor inventory, not merely process creation. Record the
version in test evidence because it updates independently.

For a cloud-backed editor when isolated save/rejoin tests are required, the documented
[Studio command-line interface](https://create.roblox.com/docs/studio/command-line-interface)
accepts `--task EditPlace --placeId <verified-place-id> --universeId <verified-universe-id>`.
On macOS, `open -n -a /Applications/RobloxStudio.app --args` followed by those arguments
launches a cloud editor, which `studio_mcp.open_cloud_place` does, confirming both `game.PlaceId` and
`game.GameId` through MCP before it returns. Use `--task EditFile --localPlaceFile <absolute-path>` for a file.
Launch extra editors only inside the isolated runner. An ordinary local place file has
zero place/universe IDs and cannot establish cloud persistence coverage. Synchronizing
test source into a cloud editor does not publish it; keep fixture keys isolated and
discard those editor changes afterward unless publication is separately authorized.

The proxy can initialize and expose all tool schemas before Studio connects. Studio retries its
local WebSocket connection on an interval; terminating the proxy immediately can repeatedly return
`studios: []` even while the toggle is enabled. Keep the session alive and await a nonempty inventory
with a bounded timeout. Do not
infer a toggle failure from an empty inventory or toggle it repeatedly.

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
editor's current UI. Resolve blocking dialogs; in the runner, the `studio_mcp` waits answer Studio's
"*plugin* is not responding" alerts themselves. Then inspect the normal MCP setting before changing
it under **Assistant → … → Settings → MCP Servers**; in a VM, the bundled script does both. If remote pointer input cannot open Assistant, use its
native menu or the installed editor's shortcut configuration; inspect the current binding rather
than assuming a key. Restore any temporary binding afterward. Keep the proxy alive during bounded
discovery, then verify the intended editor with a read-only command against its explicit ID before
orchestration. Preserve unrelated preferences;
undocumented preference-file keys are not a stable setup API. This uses the normal
[MCP setup and connection checks](https://create.roblox.com/docs/studio/mcp).

A normal quit can stop at an unsaved-changes dialog. Verify closure before reopening, and avoid
repeated duplicate launches. Stop any Play session or multiplayer test through MCP first. An editor
`studio_mcp.open_place` made, other than [the game's warm editors](#keep-the-games-editors-warm), is
then closed with `close_place`: its place is a disposable copy, so
ending the process is the same as Don't Save. The test server and client windows a multiplayer test
starts are separate processes `close_place` does not match, so list them with `pgrep` before and after
the test and stop those it added with `studio_mcp.stop_guest_processes`. A cloud editor
`open_cloud_place` made is closed with `close_cloud_place`. To close any other task-owned editor, quit that process through its own window — Cmd-Q or the File menu sent
to the verified process — and answer an unsaved-changes prompt with Don't Save when the place is a
disposable build artifact whose source lives in the repository, or Save when it holds work that
exists nowhere else. Confirm with `pgrep` that the process exited. A process that ignores a quit
and shows no prompt, or a test server or client left behind by a failed test call, is
force-stopped only when it is task-owned and holds nothing unsaved, recorded as such; other
sessions' processes are never touched. Multiple processes can show the same file or
have different authentication states. Preserve the working editor and retained credentials.

## Qualify input and capture

Verify client/server play, an actual game button, movement, and a viewport screenshot **in the runner**.
Also launch the maximum requested multiplayer clients there and confirm none appears on the host.
Confirm the resulting game state and that the user can continue using their desktop. Successful code
execution or single-client input alone does not establish complete isolation. Use `screen_capture` for the game viewport, never a host
screenshot or screen recording that could include unrelated private content. Its image can be returned as an MCP
image block; save/decode that block directly instead of printing its base64 data.
World-space text, such as floating score labels, status words and nameplates, is verified only in a
capture shown to draw it: confirm a known label appears in the frame before judging its spacing or
style from it. Take that capture as a grab of the Studio window inside the VM
(`screencapture -x -o -l <window-id>`, as [direct VM control](#direct-vm-control) describes),
which draws that text, or, for text that appears and fades, a recording of the VM's desktop
(`screencapture -v` inside the VM) turned into frames and one contact sheet of them; on the Linux
runner, an X screenshot or recording of the Xvfb display. The game's capture helper uses the window
grab for every check that judges world-space text.

If those captures are black while the VM desktop remains visible, use the qualified
[VM desktop viewer](#optional-vm-desktop-viewer) when appropriate. Keep capture failure
separate from rendering/asset acceptance and respect the user's chosen testing environment.

Inspect current tool schemas rather than guessing signatures. Use supported MCP tools and
[StudioTestService](https://create.roblox.com/docs/reference/engine/classes/StudioTestService) for
orchestration. Normal-input walkthroughs still require real movement, prompts, menus, and camera controls. Direct progression changes belong in separate edge-case fixtures.

Use the live `execute_luau` schema to select a supported `Client`, `Server`, or `Edit` context.
Read live UI, camera, and character state from the appropriate running context. A standalone command
may not share a gameplay module's initialized state; an empty module result alone does not prove
that the service stopped. Prefer replicated instance/UI observation or a bounded ordinary server
fixture for runtime state. Remove fixtures afterward and never advance progression for inspection.
A `Client` script can reset a scripted camera to the default camera type, so run none while a
game-owned camera frames the scene being judged, or a capture shows a framing defect the game does
not have.

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
the intended control responded. MCP clicks aimed at an instance can land offset by the device's
safe-area inset; when one misses, click by coordinates instead. Where direct VirtualInput is supported, the full-inset transform in
the [input coordinates](#input-coordinates-the-phone-notch-matters) maps the button center
correctly. Also check ancestor visibility and clipping, and scroll hidden controls into view first.
Verify selection, confirmation, and the server outcome; callbacks or remote calls are separate
integration evidence, not a substitute for player input.

Do not silently fall back to host client launches or native host HID automation if a capability is missing. Repair the runner as
[Tart VM capabilities](#tart-vm-capabilities) describes when it cannot support the operation. Record the concrete blocker. Keep Studio, simulated-device, persistence, and published-client
verification distinct; one does not establish another. Keep reusable tools in the test tooling area as
[the game's test helpers](#keep-the-games-test-helpers-in-its-repository) says, and keep screenshots, logs,
temporary fixtures, and runner state ignored.

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

## Optional VM desktop viewer

Use this optional viewer when the configured VM and permitted browser support it, the VM
desktop renders a usable image, and either Studio viewport capture is unavailable or black or a
VM UI step needs input that input posted inside the VM cannot give, such as a permission prompt or an
Accessibility grant. A hidden viewer is a normal remote-desktop client in
a background browser tab; it is not a second VM or a host-screen recorder. It can keep
showing the VM after the native Screen Sharing window closes. Closing the browser tab
ends that viewing connection, not the VM. Follow an explicit user request to use their
local Studio or a visible viewer instead.

### Connection requirements

Reuse an installed, trusted [noVNC](https://github.com/novnc/noVNC) client and
[websockify](https://github.com/novnc/websockify) proxy, or the available equivalent. Keep their
installation outside game checkouts and record actual versions in verification evidence.

- The configured VM is running without host windows, clipboard sharing, or audio. Its current
  private address and normal authenticated remote-desktop service are verified.
- The proxy serves only the viewer distribution and binds to a free **loopback** port. Its target
  is the intended VM endpoint, optionally reached through an existing SSH tunnel. It never
  serves the repository/home directory or exposes public forwarding for convenience.
- A permitted browser-control surface holds a background tab for the local viewer. VM login
  uses the existing authorized credentials through the normal form; credentials never enter URLs,
  command lines, repository files, or reports. Clipboard transfer stays unused.
- A fresh image reflects a harmless VM action after any native viewer closes. A connection
  banner or unchanged frame does not establish live capture. MCP remains preferred for supported
  orchestration; viewer input stays inside the VM and uses current screenshots/state.
- Reconnection checks the existing viewer's connection state before restarting Studio or the VM.
  The tab stays hidden unless the user asks to watch.

For the optional retained Tart/macOS setup above, load the runner identity and
derive the current VM address from Tart rather than a saved IP. Verify that noVNC and websockify
are installed at the shared tool path, port 6080 is unused, and the VM's authenticated VNC
service is reachable. Start the proxy as a tracked task-owned process:

```sh
eval "$("<installed roblox-studio skill>/scripts/runner_ssh.sh" --describe)"   # from inside the game's repository
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
address and fresh VM frames, then retain the process handle for
the cleanup below. Use the installed tools' help when their options differ; this recipe follows
the [noVNC quick start](https://github.com/novnc/noVNC#quick-start) and
[websockify web-server option](https://github.com/novnc/websockify#additional-websockify-features).

### Security boundary

Loopback restricts the browser proxy to the Mac; it does not itself restrict the VM's
VNC listener. Verify the VM is on its intended private network and has no unintended
public forwarding. Local processes can still reach the proxy, and VM authentication
remains necessary. Serve trusted pinned client code, not an arbitrary hosted viewer.

An `http://` / WebSocket / direct-VNC connection does **not** add transport encryption. Do not describe it as end-to-end encrypted
or hardened. A stronger VM login and VNC carried through the existing SSH connection
can protect the connection when required by the chosen environment. A loopback SSH forward to the VM's `127.0.0.1:5900`, followed
by websockify targeting that local forwarded port, encrypts the Mac-to-VM leg; qualify
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
save project artifacts, leave the VM running unless one of that section's two shutdown cases
holds, and preserve its disk, installed software, login, preferences, and SSH setup. Never remove the VM to clean up a viewer.

### VM file pickers

Remote input can arrive before a field gains focus or before its display updates. Focus the field,
wait for its active state, enter the text, and verify the rendered value before submitting or moving
fields. If bulk entry drops characters, correct the field and use the active tool's per-character
key input with brief intervals; verify completion, including the full path in a file picker.
Do not repeatedly submit incomplete credentials. For a preview or staged import, complete its options and verify the terminal result; opening a preview alone does not commit the import.
