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

## Keep the game's test helpers in its repository

Every step a check repeats has one tested helper, committed in the game repository's test tooling
area and built on the [studio_mcp](../scripts/studio_mcp/client.py) package for the transport:

- putting a disposable profile into a given state;
- walking the character to an NPC, prompt or place through real movement around the collision
  geometry, as a player does;
- pressing a prompt or a control through real input, and reading back that it responded;
- starting an encounter, a match or another game mode from its real entry point;
- running a multi-client test and counting the clients that actually joined;
- capturing the viewport and recording motion.

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

Studio work runs in an isolated runner: a Tart VM on a macOS host, the container runner below on Linux. The user's own desktop Studio is not the runner, even for an operation that sends no input, unless the user chooses it as described below, since opening a place, building or capturing still launches windows and takes focus there; a supported Studio MCP operation that avoids moving the host pointer does not change that. Qualify editor identity, input, capture, rendering, and window/focus isolation separately before claiming unattended testing is safe.

**Each game has its own runner VM**, named for the game, so one game's editors, settings, files and memory never land on another game's tests. When the game in hand has a configured VM, reuse its installed Studio, authentication, and tooling; when it has none, create it as [Add a VM for a game](#add-a-vm-for-a-game) says, without asking. Verify the intended place before acting, and coordinate exclusive control of the game's VM between the sessions working on that game. Start a stopped runner when needed, discover its current address, and leave it as [Leave the shared runner as you found it](#leave-the-shared-runner-as-you-found-it) says. An unavailable isolated capability, or a runner lock another session holds, leaves only the operations that need the runner waiting; every other part of the work — source, builds, world art, audio, tests and later plan steps — continues meanwhile. Never switch to the host's desktop Studio on your own. Inside the runner, install or update Studio and the tools the work needs, sign in with the retained session, and create the upload staging directory, without asking.

### Retained Tart/macOS runner

This example applies only when the host configures the shared values in `~/.config/roblox-studio/runner.env` (`ROBLOX_STUDIO_TART`, `ROBLOX_STUDIO_SSH_USER` and `ROBLOX_STUDIO_SSH_KEY`) and each game's own in `~/.config/roblox-studio/games/<game>.env` (`ROBLOX_STUDIO_VM`, its VM's name, and `ROBLOX_STUDIO_KNOWN_HOSTS`, that VM's pinned host key). The game is `ROBLOX_STUDIO_GAME` when set, or else the name of the folder holding the main checkout of the repository the command runs in, so every worktree of one game reaches the same VM. Shared tools and keys live outside game checkouts. Discover the configured machine; do not assume its name or address from another session. Hold the runner lock on the key that is the game's VM name, shared by every session working on that game. **A game's VM is named `<game>-vm`**, from the game's slug, such as `example-game-vm`, and that name is its lock key. A VM named otherwise keeps working through its game's settings file; never rename another session's VM. A rename is made only while no one holds its lock, with the game's settings file updated in the same step.

```sh
eval "$(runner_ssh.sh --describe)"   # the game's resolved values, from inside its repository
"$ROBLOX_STUDIO_TART" get "$ROBLOX_STUDIO_VM"
# Start only when stopped, detached so the VM outlives the agent's own task limits:
mkdir -p "$HOME/.local/state/roblox-studio"
nohup "$ROBLOX_STUDIO_TART" run "$ROBLOX_STUDIO_VM" --no-graphics --no-clipboard --no-audio \
  > "$HOME/.local/state/roblox-studio/$ROBLOX_STUDIO_VM.log" 2>&1 < /dev/null & disown
"$ROBLOX_STUDIO_TART" ip "$ROBLOX_STUDIO_VM" --wait 180   # wait until the guest has an address
```

Reach the guest only through [runner_ssh.sh](../scripts/runner_ssh.sh), which resolves the game, reads
`runner.env` and the game's file, refuses a game with no VM configured rather than reaching another game's, and
finds the guest's address through Tart on every call, so no shell variable has to carry the target from one command to
the next. The runner's Studio MCP is `runner_ssh.sh /Applications/RobloxStudio.app/Contents/MacOS/StudioMCP`,
spoken over stdio: give an MCP client that command.

Drive the runner's Studio from scripts through the [studio_mcp](../scripts/studio_mcp/client.py) package, which every game uses
from the installed `roblox-studio` skill's `scripts` folder, put on `sys.path`; no game keeps its own MCP
client. Each `Studio` holds its own MCP session through `runner_ssh.sh`, and the module has no shell command line.
Each `Studio` method, `run_in_runner`, `open_place` and `close_place` first confirms through `agent-lock` that the
caller's receipt owns the lock on the game's VM name with enough of its lease left for every call it can make, each
counted at its full timeout, so no call outlives the lease; a long operation, such as `open_place` with its
registration wait, needs a lease acquired or renewed for it. `open_place(project, place, out_dir, lock_receipt)`
copies a built place into the guest under `studio-places/<project>/`, launches an editor for it and returns a
`Studio(studio_id, lock_receipt)` once that editor registers; when the launch fails at any point once the copy starts,
it closes the editor, saving the guest's screen when the editor never registered, and raises. The project and place
file names use only letters, digits, `.`, `_` and `-`, starting with a letter or digit. `close_place(project, place,
lock_receipt)` ends the editor that has exactly that copy open and deletes the copy, and raises, keeping the copy,
when the editor stays open. `run_in_runner(command, lock_receipt, timeout)` runs a shell command in the guest.
`Studio` executes Luau, captures, reads the console, sends keys, and clicks a button by its instance path through
the bundled VirtualInput helper; `Studio.tool(name, arguments)` calls any other Studio MCP tool on that editor.

**No Studio operation reaches the host by falling back.** A client, helper or MCP server that picks its target
from a variable or setting and drives the host's Studio when that target is missing is not a runner route, even
for a read: a game repository's helper run with its runner variable unset, or the harness's own Studio MCP tools
connected to this machine. Before a connection's first call, confirm its target: `list_roblox_studios` names the
editors `runner_ssh.sh 'pgrep -fl RobloxStudio'` shows in the guest, never the host's.

A harness that stops background commands after a time limit stops a `tart run` it owns, and the
VM with it, so the VM runs detached and `tart stop` ends it.

Verify SSH host keys, the intended guest editor, and the source/place before running tests. The no-graphics, no-clipboard, no-audio options keep the VM from opening a host window or sharing clipboard/audio. Store versions and qualification evidence outside this skill. Do not provision or reset a working retained VM as routine setup.

#### Size the host for its VMs

A running VM holds its whole memory allocation on the host, and its disk image grows as the guest
writes. Budget each game's VM at 6 CPU cores, 12 GB of memory and a 50 GB disk: a guest with less
memory swaps with one editor and a Play session open. Before starting or creating a VM, read the
host's free memory and disk. Start one only while every running VM's memory plus 8 GB for the host
fits in the host's memory, and create one only while the host's free disk exceeds the new VM's disk
size plus 20 GB. macOS runs at most two macOS guests at once, whatever the host's size. When the
budget leaves no room, stop the VM of a game no session is using (no one holds its lock), never one
another session holds; otherwise the Studio work for this game waits for room as a held lock does,
and the rest of the work continues.

#### Add a VM for a game

When `runner.env` exists but the game has no `games/<game>.env`, create the game's VM and continue
the work there, without asking: a game's VM is part of the runner setup the work already has. Each step
ends with its check:

1. **Clone** a stopped qualified VM of another game, or the retained Cirrus Labs base image when no
   qualified VM can be stopped, with `tart clone <source> <game>-vm`, within the budget
   above. A clone of a qualified VM keeps its installed Studio, Roblox player, guest settings and
   signed-in session; a clone of the base image starts at step 2 of
   [Provision a runner when none exists](#provision-a-runner-when-none-exists) for everything after
   the clone. `tart set` the budgeted CPU, memory and disk, then start it detached as above;
   `tart ip --wait` returns its address.
2. **Pin its host key.** Record the clone's host key at its own address in
   `~/.config/roblox-studio/<game>_known_hosts` and verify its fingerprint through `tart exec`, as
   step 3 of provisioning says. The shared SSH key a clone of a qualified VM carries needs no new
   `authorized_keys` entry.
3. **Write `games/<game>.env`** with `ROBLOX_STUDIO_VM` and `ROBLOX_STUDIO_KNOWN_HOSTS`;
   `runner_ssh.sh --describe` from the game's repository prints them, and `runner_ssh.sh hostname`
   answers from the new guest.
4. **Clear the source's task state.** Remove another game's places, captures and task folders the
   clone carried, and close any editor its last session restored; the runner's persistent setup
   stays.
5. **Sign in and qualify** as [authentication](#authentication-and-user-handoff) and
   [Qualify input and capture](#qualify-input-and-capture) describe; a session cloned signed in is
   confirmed from Studio's start page, not assumed.

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
   guest must log its desktop user in on boot, which everything run while the host is locked
   depends on: `defaults read /Library/Preferences/com.apple.loginwindow autoLoginUser` in the guest
   names that user on a Cirrus Labs image.
3. **Pin SSH before trusting it.** Generate a dedicated key in `~/.config/roblox-studio/`. Record
   the guest's host key with `ssh-keyscan -t ed25519`, then compare its `ssh-keygen -lf` fingerprint with the
   one `tart exec <vm> ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub` reports through the guest
   agent; a mismatch stops setup. Append the public key to the guest's `authorized_keys` through
   `tart exec -i`, so no guest password passes through a command line, and confirm a `BatchMode=yes`
   login. Write the three shared values to `runner.env` and the game's two to `games/<game>.env`.
4. **Install Studio in the guest** from Roblox's official macOS installer image. Mount it there,
   confirm the installer's code-signing team matches the host Studio's, and `open` it in the
   signed-in guest session; the check is `/Applications/RobloxStudio.app` in the guest and Studio's
   window in a guest capture.
5. **Sign in, enable MCP, and qualify** as [authentication](#authentication-and-user-handoff),
   [direct guest control](#direct-guest-control) and
   [Qualify input and capture](#qualify-input-and-capture) describe.

#### Add the published Roblox player

Playing a published experience needs the Roblox player in the guest, which Studio does not include.
Add it to any runner that lacks `/Applications/Roblox.app`, newly provisioned or retained. Each step
ends with its check:

1. **Download the macOS build in the guest.** Roblox's web download link serves the Windows
   installer to a client that is not a browser, so read `clientVersionUpload` from
   `https://clientsettingscdn.roblox.com/v2/client-version/MacPlayer` and download
   `https://setup.rbxcdn.com/mac/arm64/<clientVersionUpload>-RobloxPlayer.zip`; `file` reports a
   zip archive.
2. **Verify and install it.** Unpack it with `ditto -x -k`, then confirm that
   `codesign --verify --deep --strict` passes, that its team matches the guest Studio's, and that
   `spctl -a -vv` reports a notarized Developer ID. Copy it to `/Applications/Roblox.app`; opening
   it shows its sign-in page. It registers itself as a login item.
3. **Sign it in by QR code.** Choose Sign In, then QR code, capture the code it shows, and relay
   the capture and code through the question tool with a confirmation option and one for a new
   code, since a code expires in about two minutes. A prompt Roblox shows the account after
   sign-in, such as updated terms, is the user's to accept: ask before clicking it.
4. **Launch and qualify it.** `open "roblox://experiences/start?placeId=<place id>"` in the guest
   starts an experience. Qualify input and capture on a neutral place, as
   [direct guest control](#direct-guest-control) describes, before relying on it, and quit the
   player afterward.
5. **Turn off the Dictation shortcut in the guest.** A Cirrus Labs image enables it, and held game
   keys can open Dictation instead of moving: set symbolic hot key 164 to disabled in
   `com.apple.symbolichotkeys`, then run `activateSettings -u`; holding a movement key in a game no
   longer opens Dictation.

The player ignores `SIGTERM`, and quitting it can leave a game running in its `-launchToTray`
process, so a process listing does not show whether a game is open. Stop it with
`pkill -KILL -x RobloxPlayer` and confirm from a guest capture that no game is on screen; the tray
process restarts at once and is out of any experience.

On a Tart macOS guest, whose player log names Apple's paravirtual Metal device, simple places have
drawn correctly while some complex scenes showed a white or dark world with only outlines and UI,
stretched polygons or wrong textures, though gameplay footage of the same scenes renders normally.
Lowering graphics quality did not change it, and the client's OpenGL preference flag was ignored on
macOS. Until a guest configuration is shown to draw such a scene, treat its 2D UI as evidence and
its world visuals as untested.

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

## Tart guest capabilities

For a configured Tart runner, use the official [quick start](https://tart.run/quick-start/) and the installed
CLI's help. Keep actual versions, image identity, resource allocation, and qualification results in
local configuration and verification evidence. Reuse the retained runner before provisioning one.

With the Tart options above, the VM does not create a host window, share the clipboard, or play test audio through the user's speakers. Transfer only the project/test files over
SSH, and invoke the guest's Studio MCP executable through `runner_ssh.sh`. Keep the guest proxy connection alive
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
remaining limitation. Repair the runner itself, reinstalling Studio or recreating the VM where
that is what it takes; the Studio work waits for it rather than moving to the host's desktop.

When viewport capture fails but the guest desktop is usable, the optional
[guest desktop viewer](#optional-guest-desktop-viewer) provides background images and guest-native UI
without a visible Screen Sharing window. It describes connection requirements, authentication,
unencrypted-transport limitation, live-image check, and cleanup. It does not establish
that the guest renders game assets correctly.

Use the host's desktop Studio only when the user explicitly chooses it for the task. Then keep host input and extra client windows within their authorization, and set a local installation's host-Studio override, such as `ROBLOX_ALLOW_HOST_STUDIO=1`, only for that choice.

On a macOS host, native input and screen capture need Accessibility and Screen Recording granted to
the app the agent runs under, identified by the agent's process ancestry, not to its shell or
interpreter; macOS applies a new grant only after that app restarts. Check the grant with
`AXIsProcessTrusted()` and a test capture before driving input, and name that exact app when the
user must grant it.

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

Every guest setting and permission change is the agent's own step under the global rules'
user-action bullet, since the agent controls the whole guest. Input posted inside the guest leaves the host's cursor alone and
is the route for guest UI work; a host viewer click moves the user's cursor and serves only where
guest input cannot reach. Read the guest's Accessibility list first: a Cirrus Labs image already
grants `osascript`, `sshd-keygen-wrapper` and `tart-guest-agent`, so `osascript -l JavaScript`
over SSH posts working CoreGraphics clicks. A missing grant is added in the guest's System Settings,
opened over SSH with `open "x-apple.systempreferences:com.apple.settings.PrivacySecurity.extension?Privacy_Accessibility"`
and operated by the agent through the [guest desktop viewer](#optional-guest-desktop-viewer), or the
host's Screen Sharing when no hidden viewer is available, since posted input is what the grant
enables. Guest input behaves like this:

- **Coordinates are points.** A HiDPI guest's captures have twice the pixels of its screen points;
  read `NSScreen.mainScreen.frame` and divide capture coordinates accordingly.
- **Studio can hold a stale window origin** and register clicks one title bar lower than they land.
  Set its window's position and size through System Events before clicking, and check with a
  visible control such as a ribbon tab.
- **Studio's widgets need a real click shape:** move the pointer toward the target first, and give
  each press a click count (`kCGMouseEventClickState`) from the HID system event source.
- **Studio's embedded web panels,** such as Assistant, take one click to focus and then toggle on
  each click; capture after every click rather than repeating one.
- The first `screencapture` over SSH raises a guest Screen Recording prompt for the SSH session;
  the agent approves it through the guest desktop viewer, or the host's Screen Sharing when no hidden
  viewer is available.

Tart's own `--vnc-experimental` endpoint returns black frames while the VM runs with
`--no-graphics`; a viewer connects to the guest's built-in Screen Sharing service on port 5900.

To turn the guest Studio's MCP server on or off, copy
[guest_studio_mcp.js](../scripts/guest_studio_mcp.js) into the guest and run
`osascript -l JavaScript guest_studio_mcp.js <studio-pid> on` over SSH. It finds each control by
its text or tooltip, so it does not depend on the guest's display size, and reaches the Assistant
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

Authenticate each viewer the agent opens normally; one viewer's connection does not authenticate
another, and a viewer connection dialog is not a connected desktop.

**Roblox sign-in in a runner is the agent's to drive; the user's only part is entering a code.**
Reuse a retained Roblox session first. When Studio shows its sign-in screen, or its log reports
`Authenticated : NO`:

1. **Choose Quick Sign-in yourself**, through input posted inside the guest as
   [direct guest control](#direct-guest-control) describes, or the Linux runner's display input.
2. **Read the code immediately before each asking**, a re-ask after a timeout included, since it
   expires in about two minutes: from the newest `awaitQuickSignIn via polling: code=` line in
   Studio's log when it is there, or from a guest capture of the code Studio shows.
3. **Ask through the question tool** for that one step: enter the code at
   <https://www.roblox.com/crossdevicelogin/ConfirmCode> on a device already signed in to Roblox,
   with a Done option and one for a new code. A new-code answer, or a timeout, goes back to step 2.
4. **Finish every later screen yourself**, such as choosing the account and its **Continue**, then
   confirm `Authenticated : YES` in the log and the account on Studio's start page before relying on
   the runner.

Never ask the user to sign in through a viewer, Screen Sharing or any other route to the guest's
screen, and never ask for a password or a second factor: a screen inside the runner is one the
agent's input reaches, so only the code entered on the user's own device is theirs. Do not transfer
session cookies. Continue independent work while the question waits.

## Keep the game's editor warm

The default check loop reuses one Studio editor kept open in the game's VM on the game's built
place, with source synced into it live, so a check costs a sync and a Play session rather than a
build, a copy and an editor launch.

- **Open it once.** Build the place, open it with `studio_mcp.open_place` under the project name
  `warm`, and leave it open: it belongs to the game's VM, not to the task that opened it. A session
  that finds the game's warm editor registered in `list_roblox_studios` uses it, after confirming
  its place name.
- **Sync source live, served inside the guest.** Install the Rojo plugin matching the game's
  pinned Rojo version into the guest's Studio plugins folder (`~/Documents/Roblox/Plugins` in a
  macOS guest), and run `rojo serve` in the guest on its loopback address, against a copy of the
  session's checkout in the guest that each sync updates. Serving from the host instead needs a
  listener on the VM network, which can raise a firewall prompt on the user's desktop. The session
  holding the VM's lock syncs its own checkout into that copy, so the editor holds that checkout's
  tree.
- **Connect the right plugin.** An older Rojo plugin can share the toolbar label, so open the panel
  whose title shows the pinned version. A local place file has place ID 0, which the plugin's
  automatic reconnect skips, so press **Connect** through input posted inside the guest each time
  the editor opens.
- **Check the session's parts, and restore them with one command.** The editor can be gone, the
  server stopped, or the plugin disconnected; read each from the guest: the editor in
  `list_roblox_studios`, the server's process, and the plugin's open TCP connection to the
  server's port (`lsof` shows Studio's process name cut short, such as `RobloxStu`). The game's
  start command for its warm session brings back whichever is missing, never only one.
- **Record what the session holds inside it**: the source revision, a manifest of the synced files
  and a digest of the built world, kept in the guest beside the session, so a later session reads
  whether the warm editor matches its checkout instead of guessing.
- **Confirm each sync before a check.** Read each changed script's source back from the Edit data
  model through `execute_luau`; a plugin showing connected does not show that a change landed.
  Then start Play from that editor, and stop it when the check ends.
- **Rebuild only for what the plugin cannot write.** Content the place's build step makes rather
  than a file maps, such as terrain or generated models; properties scripts cannot set, such as a
  mesh part's mesh; a project-file change to which containers are mapped; and a sync the plugin
  reports as failed or partial. Then rebuild the place, close the warm editor with
  `close_place`, and open the new build the same way. A check that left fixtures or state it
  cannot remove is a reason to reopen it too.
- **Delivery evidence still comes from the built place.** A warm editor proves behavior of the
  synced source; [delivery build acceptance](source-delivery.md#test-the-delivery-build-directly)
  still tests the artifact being delivered.

## Leave the shared runner as you found it

Every session working on one game shares that game's VM, so whatever one leaves behind lands on the next. The
game's warm editor stays, as the section above says; no other task process
outlives any release of the runner lock, and before the task's last release its own files are gone and
every setting it changed reads back at the value it found.

- **Settings.** A Studio or engine setting changed from a script or a dialog, such as
  `settings().Rendering`'s quality levels or `UserGameSettings`, persists across editors and applies to
  every session in the runner. Prefer a route scoped to the test, such as the device simulator's own
  profile. When a shared setting must change, record its value first, restore it from an Edit-mode
  editor once the test is done, and read it back from a newly opened editor; a restore issued from a
  Play client, or one never read back, has not happened. Granting a permission an operation needs is
  setup, not a setting to restore.
- **Files.** Everything the task copies or writes in the guest, such as places, captures, scratch
  output, worktrees and lock files, sits under a folder named for the task or its project and is
  removed when the task's runner work ends. `studio_mcp.close_place` deletes the place copy
  `open_place` made. The runner's persistent setup is not task output and stays, as the next section
  says.
- **Resources.** Before a heavy run, such as Play, a multiplayer test or a device simulation, read the
  guest's free disk and swap (`df -h /` with `sysctl vm.swapusage` in a Tart guest, `free -h` in the
  Linux runner). Low disk or swap already in use is investigated before the run: remove what the task
  itself left and restore what it changed, and report what another session left without deleting it. A
  run that could run away gets a watchdog: a loop in the guest that reads the task's editor's resident
  memory (`ps -o rss= -p <pid>`) every few seconds and kills that editor past a ceiling well under the
  guest's memory, so one run cannot push the shared guest into swap.

## End of session for a retained VM

These steps apply only to a task-owned or configured retained VM. Finish or record the task blocker before shutdown; a progress update does not end the test session.

**Take a step only when the agent can undo it with the host locked.** The user's Mac can lock at any
moment, and a locked host refuses host-side clicks, screenshots and window control. Everything a
retained runner needs to come back runs without the host's screen: `tart run --no-graphics`, SSH,
the guest's automatic desktop login, Studio relaunched in the guest, input posted inside the guest,
and guest MCP. Check that the route still holds before ending a session. Leave running, rather than closing, anything
whose restoration needs the host's screen or the user: a host viewer the user is using, Studio on
the host, a guest state only a host viewer could recreate, or a Roblox session that would need the
user to enter a new code. Powering the guest off is fine, because its automatic login brings the desktop back.

When the game work is done, save the authorized project artifacts, close Roblox Studio normally,
and **shut down the guest VM** so it is no longer running locally. Verify that Studio closed and the
VM is stopped. Do not leave the VM running or substitute a suspended/running state for the requested
shutdown. If an unfinished test must continue, report that explicitly rather than claiming shutdown.

**Do not tear down the sandbox's persistent state.** Do not uninstall Studio or Roblox, log out,
delete/recreate the VM, reset its disk, remove its project setup, clear caches/keychains, or erase its
settings/authentication as end-of-task cleanup. A task's own copies and output are not that state;
[the section above](#leave-the-shared-runner-as-you-found-it) removes them. Closing Studio and powering off the guest are the
normal shutdown actions. Keep the VM, installed apps, signed-in accounts, files, configuration, and
SSH access available for another session. Do not publish or commit the authenticated image or keys.

At the next session, locate and start the existing VM with the same no-window/no-clipboard/no-audio
options. Discover its current IP rather than assuming the prior address, reconnect via SSH, and
verify the intended Studio/project. Create a replacement only when necessary and authorized; a new
session is not a reason to rebuild or ask the user to sign in again. Open a viewer automatically
when a guest UI step needs one that posted guest input cannot give.

## Studio MCP connection and input

Prefer the [built-in Studio MCP server](https://create.roblox.com/docs/studio/mcp) when the installed Studio and tool surface support it. Inspect tool schemas and connect to the verified editor. MCP input can avoid host keyboard/mouse injection; qualify any windows it launches separately.

If an installed isolated runner fails a capability, inspect and recover that capability in the runner. A single editor answering MCP does not establish that multiplayer windows or guest rendering work. Keep evidence separate for input, capture, rendering, isolation, Studio Play, and a published client.

## Connect to the intended editor

On macOS installations, the stdio executable may be `/Applications/RobloxStudio.app/Contents/MacOS/StudioMCP`; discover the installed location before connecting.
Enable Assistant → … → Settings → MCP Servers → Enable Studio as MCP server **yourself if disabled**;
in a guest, [direct guest control](#direct-guest-control) runs the bundled script for it.
This is part of the authorized setup and never a step for the user: the agent reaches the setting
itself, through input posted inside the guest or, for an editor on an unlocked host where the task
authorizes host input, through the host's own input. A setting enabled in another machine
or guest does not enable the local editor. Follow the [authentication procedure](#authentication-and-user-handoff):
complete viewer/guest login and the Roblox sign-in screens yourself; the user's only step is
entering the sign-in code. Never transfer cookies or ask for credentials in chat.

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
editor's current UI. Resolve blocking dialogs, then inspect the normal MCP setting before changing
it under **Assistant → … → Settings → MCP Servers**; in a guest, the bundled script does both. If remote pointer input cannot open Assistant, use its
native menu or the installed editor's shortcut configuration; inspect the current binding rather
than assuming a key. Restore any temporary binding afterward. Keep the proxy alive during bounded
discovery, then verify the intended editor with a read-only command against its explicit ID before
orchestration. Preserve unrelated preferences;
undocumented preference-file keys are not a stable setup API. This uses the normal
[MCP setup and connection checks](https://create.roblox.com/docs/studio/mcp).

A normal quit can stop at an unsaved-changes dialog. Verify closure before reopening, and avoid
repeated duplicate launches. Stop any Play session or multiplayer test through MCP first. An editor
`studio_mcp.open_place` made is then closed with `close_place`: its place is a disposable copy, so
ending the process is the same as Don't Save. The test server and client windows a multiplayer test
starts are separate processes `close_place` does not match, so confirm with `pgrep` that they exited
too. To close any other task-owned editor, quit that process through its own window — Cmd-Q or the File menu sent
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
World-space text, such as floating damage numbers, status words and nameplates, is verified only in a
capture shown to draw it: confirm a known label appears in the frame before judging its spacing or
style from it. `screen_capture` has been observed leaving out BillboardGui content in a Tart guest,
where a recording of the guest's own desktop (`screencapture -v` inside the guest) drew it; on the
Linux runner, use an X screenshot or recording of the Xvfb display.

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
[Tart guest capabilities](#tart-guest-capabilities) describes when it cannot support the operation. Record the concrete blocker. Keep Studio, simulated-device, persistence, and published-client
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

## Optional guest desktop viewer

Use this optional viewer when the configured guest and permitted browser support it, the guest
desktop renders a usable image, and either Studio viewport capture is unavailable or black or a
guest UI step needs input that posted guest input cannot give, such as a permission prompt or an
Accessibility grant. A hidden viewer is a normal remote-desktop client in
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
  The tab stays hidden unless the user asks to watch.

For the optional retained Tart/macOS setup above, load the runner identity and
derive the current guest address from Tart rather than a saved IP. Verify that noVNC and websockify
are installed at the shared tool path, port 6080 is unused, and the guest's authenticated VNC
service is reachable. Start the proxy as a tracked task-owned process:

```sh
eval "$(runner_ssh.sh --describe)"   # the game's resolved values, from inside its repository
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
