# Background VM desktop viewing

Use this optional fallback when Studio's viewport capture is unavailable or black but the
guest desktop renders a usable image. A hidden viewer is a normal remote-desktop client in
a background browser tab; it is not a second VM or a host-screen recorder. It can keep
showing the guest after the native Screen Sharing window closes. Closing the browser tab
ends that viewing connection, not the VM. Follow an explicit user request to use their
local Studio or a visible viewer instead.

## Connection requirements

Reuse an installed, trusted [noVNC](https://github.com/novnc/noVNC) client and
[websockify](https://github.com/novnc/websockify) proxy, or the available equivalent. Keep their
installation outside game checkouts and record actual versions in verification evidence.

- The retained VM is running without host windows, clipboard sharing, or audio. Its current
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

## Security boundary

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

## Evidence and cleanup

Successful desktop viewing does not qualify Studio-native capture, mesh rendering, asset
permissions, sound, or published-client behavior. Each capability needs its own relevant evidence.
A viewer can expose a rendering defect but cannot repair the renderer. Keep dated images and
recovery attempts in verification output; only a reusable decision rule belongs in this reference.

When switching away or ending the session, close the hidden tab and stop its websockify
process and any task-owned SSH forward. Verify their listening ports closed. Follow the
[persistent VM lifecycle](isolated-testing.md#end-of-session-preserve-the-machine-stop-its-resource-use):
save project artifacts, close Studio normally, shut down the VM, and preserve its disk,
installed software, login, preferences, and SSH setup. Never remove the VM to clean up a viewer.

## Guest file pickers

Remote input can arrive before a field gains focus or before its display updates. Verify the
active field and rendered text before submitting, including full paths in file pickers. If bulk
input is incomplete, use the supported slower input method and check completion before moving
fields. Do not repeatedly submit incomplete credentials. Separate modal previews from the action
that commits an import, and verify the import's terminal result.
