# VM access and lifecycle

## One shared Roblox development runner

All game creation and testing use the same configured, retained VM when its capabilities work.
It is shared infrastructure, not owned by one game repository. Keep Studio/Roblox, authentication,
SSH identity, and tool installations reusable across games; keep each game's source, artifacts, and
test data in its own guest workspace. Existing game directories may keep their game names. Never
copy one game's assets, profile keys, place IDs, or publication target into another just because they
use the same runner.

Host runner settings live outside repositories at `~/.config/roblox-studio/runner.env`; shared tools,
SSH keys, and verified host keys live under `~/.local/share/roblox-studio/`. These local files are not
committed or mirrored by Agent Sync. Preserve their permissions and authentication. Discover the configured runner identity; never assume a machine name from another session.

Load the shared settings, inspect the VM's state with the pinned Tart binary, and start it when stopped:

```sh
source "$HOME/.config/roblox-studio/runner.env"
"$ROBLOX_STUDIO_TART" get "$ROBLOX_STUDIO_VM"
# Start only when stopped, using an owned background process/session:
"$ROBLOX_STUDIO_TART" run "$ROBLOX_STUDIO_VM" --no-graphics --no-clipboard --no-audio
```

After startup, discover the current address; do not persist or assume a previous IP:

```sh
export ROBLOX_STUDIO_SSH="$ROBLOX_STUDIO_SSH_USER@$("$ROBLOX_STUDIO_TART" ip "$ROBLOX_STUDIO_VM")"
```

MCP helpers use `ROBLOX_STUDIO_SSH`, `ROBLOX_STUDIO_SSH_KEY`, and
`ROBLOX_STUDIO_KNOWN_HOSTS`. `ROBLOX_ALLOW_HOST_STUDIO=1` is the deliberate authorized
single-editor fallback, not the default. Inspect and reuse existing settings before provisioning
tools or asking for sign-in. Shared desktop ownership covers input, tests, open-project changes, and shutdown. Its lock key
identifies the configured machine across all games; a game-specific key cannot protect that shared
resource. Independent source/build work can continue while another task owns it.

## Runner selection

Use the retained VM as the default for all Studio operations it can reliably support. Locate it and
start it automatically if it is stopped, discover its current address, and reconnect to the intended
editor. An offline VM is a setup step, not a reason to fall back to the host. Prefer guest MCP and
use the hidden guest viewer for supported native UI or capture needs. Do not choose local Studio
just because it is already open or would allow parallel work.

Studio MCP can deliver input without moving the host pointer, but Studio's multiplayer test service
can still open several native client windows. Unattended game launches and interactive verification
must therefore run inside a VM or another
authorized isolated machine. Keep all Studio/client windows, input, screenshots, and device
simulation in that environment. Do not treat hiding a host window after launch as isolation.

## Headless guest capabilities

For a Tart runner, use the official [quick start](https://tart.run/quick-start/) and the installed
CLI's help. Keep actual versions, image identity, resource allocation, and qualification results in
local configuration and verification evidence. Reuse the retained runner before provisioning one.

Resolve a recovery attempt's reported prerequisites before retrying. For a macOS updater reporting
a missing recovery volume, inspect the guest's disk layout with `diskutil list`. If the required
recovery volume is absent, stop repeated installer downloads; downloading again does not supply
that disk prerequisite. Consult the image provider's recovery requirements: the
[Tart macOS image template](https://github.com/cirruslabs/macos-image-templates/blob/main/templates/vanilla-tahoe.pkr.hcl)
retains a recovery partition for software updates. This diagnosis applies to that reported
condition, not every update failure. Preserve the authenticated disk and use a documented recovery
path; destructive repairs require their own applicable authorization. Verify the prerequisite
before retrying the update.

Run with `--no-graphics --no-clipboard --no-audio` so the VM does not create a host window, share the
clipboard, or play test audio through the user's speakers. Transfer only the project/test files over
SSH, and invoke the guest's Studio MCP executable through SSH. Keep the guest proxy connection alive
long enough for Studio discovery, as described in the MCP reference. Retrieve viewport captures and
structured results through that channel. Do not mount the whole home directory or transfer a Roblox
session cookie. Use normal Roblox authentication.

Follow [authentication and user handoff](#authentication-and-user-handoff) before presenting the
viewer. A toggle enabled on the host does not enable the guest.

Qualify the existing runner before relying on it, and recheck affected capabilities after Studio or
VM updates: authenticate, discover the intended Studio, load the current assets, run client/server
Play, operate a real button and movement, capture the viewport, and launch two/four test clients
without host windows or focus changes. Studio launching alone is not compatibility proof. Keep
dated qualification results in workspace evidence; do not recreate a working runner to requalify it.

Use MCP inside the guest wherever supported. Native setup actions may be performed through the guest
desktop when necessary, but never drive the host's game input. If Roblox rejects virtualization or
rendering/input is unreliable, attempt the applicable documented recovery and record the concrete
remaining limitation. Local Studio may then serve as the fallback for an already-authorized,
non-disruptive single-editor operation. Use its verified MCP connection, without native host HID
control or extra client windows. Checks requiring obstructive launches remain incomplete until the
isolated runner works. Continue independent lint, type, test, and build work; do not silently change runners.

When viewport capture fails but the guest desktop is usable, the optional
[hidden VM viewer](hidden-vm-viewer.md) provides background images and guest-native UI
without a visible Screen Sharing window. It describes connection requirements, authentication,
unencrypted-transport limitation, live-image check, and cleanup. It does not establish
that the guest renders game assets correctly.

An explicit current user request to use their own local Studio overrides the default
runner choice. An existing authorization for local fallback also covers a concrete VM failure;
do not ask again solely because a fallback is needed. Use that existing editor through MCP, verify its identity, and avoid
native host input or additional multiplayer windows unless separately requested. In
MCP helpers use `ROBLOX_ALLOW_HOST_STUDIO=1` to enable this deliberate single-window
choice; do not set it speculatively to bypass the default isolation guard. Multiplayer
launches remain in the isolated runner.

## Direct guest control

Host Screen Sharing, guest SSH, and guest input are separate capabilities. When the host viewer
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

## End of session: preserve the machine, stop its resource use

Shut down only after meeting the [completion or blocker criteria](../SKILL.md#work-autonomously-within-the-requested-scope),
or when the user asks to pause or stop. A progress update does not end the test session.

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

## Qualification for game research

Qualify the guest browser/media path and the **published Roblox client** separately from Studio.
Browser/media viewing and published-client play each require ordinary input and usable captures
without host windows/focus/input interference. Studio MCP capability alone does not prove those
capabilities. Record each result separately. If qualification fails, keep the dependent work
incomplete; do not
silently revert to host interaction. Host-side read-only APIs may assist data retrieval/aggregation,
but must not become a workaround that opens host research/game windows.
