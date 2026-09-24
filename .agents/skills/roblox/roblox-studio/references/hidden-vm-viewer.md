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

With the retained tool layout described in the VM access reference, load the runner identity and
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

Remote input can arrive before a field gains focus or before its display updates. Focus the field,
wait for its active state, enter the text, and verify the rendered value before submitting or moving
fields. If bulk entry drops characters, correct the field and use the active tool's per-character
key input with brief intervals; verify completion, including the full path in a file picker.
Do not repeatedly submit incomplete credentials. For an import queue covered by a preview, finish
the preview options and close it before activating **Start Import** in the queue. Verify the
terminal import result; opening or configuring the preview does not commit the import.
