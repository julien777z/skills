# Background VM desktop viewing

Use this optional fallback when Studio's viewport capture is unavailable or black but the
guest desktop renders a usable image. A hidden viewer is a normal remote-desktop client in
a background browser tab; it is not a second VM or a host-screen recorder. It can keep
showing the guest after the native Screen Sharing window closes. Closing the browser tab
ends that viewing connection, not the VM. Follow an explicit user request to use their
local Studio or a visible viewer instead.

## Verified setup and limits

The September 2026 Tart/Studio 0.739 pilot used official [noVNC](https://github.com/novnc/noVNC)
**v1.7.0**, commit `63107bd06d9e1f6136ff21aeda8cd62cbf0d433e`, and
[websockify](https://github.com/novnc/websockify) **0.13.0**. Keep their files and the Python
environment in the shared `~/.local/share/roblox-studio/tools/` directory; record versions in
verification evidence. Inspect and reuse installed tools before installing another copy.

1. Start the existing qualified VM without a host window/clipboard/audio, discover its
   current private IP, and retain the normal authenticated Screen Sharing service. Use the
   existing guest login; do not disable authentication, transfer Roblox cookies, or place
   credentials in a URL, command line, repository file, or report.
2. Serve only the noVNC distribution and bind the browser proxy to **loopback**:

    ```text
    "$ROBLOX_STUDIO_HOME/tools/novnc-env/bin/python" -m websockify --web "$ROBLOX_STUDIO_HOME/tools/noVNC" 127.0.0.1:6080 <vm-ip>:5900
    ```

    This was the verified direct recipe. Never serve the repository/home directory, bind
    this helper to `0.0.0.0`, or expose it through public forwarding as a convenience.

3. Open a hidden in-app browser through the supported computer-use tool:

    ```text
    let vmTab = await cua.createBrowserTab(
        "iab",
        "http://127.0.0.1:6080/vnc.html?autoconnect=1&resize=scale&shared=1&bell=0",
        { visible: false }
    )
    ```

    Complete the displayed guest login form yourself using the existing authorized macOS guest
    credentials. noVNC's Apple Remote Desktop handshake worked with that account. Verify the desktop
    appears before a user handoff; follow [authentication guidance](isolated-testing.md#authentication-and-user-handoff).
    Leave clipboard transfer unused.

4. Inspect `vmTab.getScreenshot()` and perform a harmless, meaningful guest action. Close
   the task's native Screen Sharing window, then verify the next browser image reflects
   the changed game state. The pilot confirmed a quest window closing and character
   movement through MCP while the native viewer was closed. Do not accept an old frame
   or the connection banner as proof of live rendering.
5. Prefer MCP for orchestration and supported player input. When native guest UI is needed,
   operate the noVNC tab through the computer-use tool, using fresh screenshots/state.
   Never substitute host keyboard/mouse injection. Keep the tab hidden unless the user
   needs to sign in or explicitly wants to watch.

The viewer disconnected once during a longer run; **Connect** and the normal guest login
restored the same desktop without restarting Studio or the VM. Inspect connection state
before assuming a game crash. Do not repeatedly reconnect an already live tab.

## Security boundary

Loopback restricts the browser proxy to the Mac; it does not itself restrict the guest's
VNC listener. Verify the VM is on its intended private network and has no unintended
public forwarding. Local processes can still reach the proxy, and guest authentication
remains necessary. Serve trusted pinned client code, not an arbitrary hosted viewer.

The verified `http://` / WebSocket / direct-VNC recipe did **not** add transport encryption;
the viewer reported an unencrypted connection. Do not describe it as end-to-end encrypted
or hardened. A stronger guest login and VNC carried through the existing SSH connection
are appropriate hardening. A loopback SSH forward to the guest's `127.0.0.1:5900`, followed
by websockify targeting that local forwarded port, encrypts the Mac-to-guest leg; qualify
that variant before claiming it was tested. Preserve host-key verification and existing
access boundaries. Credential changes still require the user to perform the normal flow.

There is no third-party remote-desktop relay in this local recipe. However, screenshots
submitted to the assistant still pass through Codex's normal tool/model processing; do
not promise they remain exclusively on the Mac. A hidden tab is a convenience, not a
privacy or security guarantee.

## Evidence and cleanup

Successful desktop viewing does not fix or qualify Studio-native capture, mesh rendering,
asset permissions, sound, or published-client behavior. In the pilot, a cold VM restart,
an explicit capture camera, Studio's native Screenshot command, and low-quality/720p
settings still produced black Play captures. OpenGL failed with `Error creating pixel
format`; Automatic was restored. The cause remained unresolved. The VM also displayed
mesh distortion in the saved baseline, so visual acceptance remained separately qualified.
Keep dated images/logs in ignored verification output rather than treating this as a
permanent diagnosis or requiring all experiments in every session.

When switching away or ending the session, close the hidden tab and stop its websockify
process and any task-owned SSH forward. Verify their listening ports closed. Follow the
[persistent VM lifecycle](isolated-testing.md#end-of-session-preserve-the-machine-stop-its-resource-use):
save project artifacts, close Studio normally, shut down the VM, and preserve its disk,
installed software, login, preferences, and SSH setup. Never remove the VM to clean up a viewer.

## Guest file pickers

In the qualified noVNC guest, bulk paste/type delivered incomplete text to Studio’s native file picker. Per-character `pressKey` calls worked; verify the complete field, including the leading slash, before confirming. Guest display updates can lag the browser accessibility response, so inspect the next rendered frame before repeating an action. This also affected sign-in: batching a field change with typing sent some characters to the wrong field. Select the complete field, verify its rendered selection, enter characters with state observations, and verify completion before moving to the next field. Do not submit visibly incomplete credentials or repeatedly retry a login without checking entry. Studio’s import preview can cover the import queue: close the preview after checking its options, then use the queue’s Start Import button and verify its success indicator.
