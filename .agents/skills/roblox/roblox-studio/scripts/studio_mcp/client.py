from __future__ import annotations

import atexit
import base64
import json
import logging
import os
import re
import select
import shlex
import subprocess
import tempfile
import threading
import time
from collections.abc import Callable, Collection, Mapping, Sequence
from datetime import timedelta
from pathlib import Path
from typing import IO, Final, cast

from studio_mcp.models import (CameraView, JsonRpcMessage, JsonValue, McpContent, PlaceIds, RunnerConfig,
                               RunnerOperation, StudioButton, StudioEntry, ToolArguments)
from studio_mcp.runner import (OPERATION_TIMEOUTS, RUNNER_SSH, SCRIPTS, LockOwnershipLost,
                               assert_editor_launch_allowed, assert_runner_lock_held, assert_runner_locks_kept,
                               focused_input, run_guest_command, runner_environment)

logger = logging.getLogger(__name__)

VIRTUAL_INPUT: Final[Path] = SCRIPTS / "virtual_input.luau"
GUEST_STUDIO_MCP: Final[Path] = SCRIPTS / "guest_studio_mcp.js"
STUDIO_APP: Final[str] = "/Applications/RobloxStudio.app"
STUDIO_MCP: Final[str] = f"{STUDIO_APP}/Contents/MacOS/StudioMCP"
STUDIO_EXECUTABLE: Final[str] = f"{STUDIO_APP}/Contents/MacOS/RobloxStudio"
GUEST_PLACES: Final[str] = "studio-places"
PROTOCOL_VERSION: Final[str] = "2024-11-05"
# The guest helper's port, which each editor's built-in Assistant plugin connects to.
HELPER_PORT: Final[int] = 13469
# Studio's editors reach MCP through a helper port the oldest running StudioMCP process holds, and every editor drops
# its connection when that process exits; a StudioMCP that never exits keeps the port while sessions come and go.
MCP_HELPER_KEEPER: Final[str] = f"""pidfile="$HOME/Library/Caches/studio-mcp-keeper.pid"
if [ -f "$pidfile" ] && kill -0 "$(cat "$pidfile")" 2>/dev/null; then exit 0; fi
nohup /bin/sh -c {shlex.quote(f"tail -f /dev/null | {shlex.quote(STUDIO_MCP)}")} > /dev/null 2>&1 < /dev/null &
echo $! > "$pidfile"
"""
POLL_INTERVAL: Final[timedelta] = timedelta(seconds=2)
DEFAULT_REGISTRATION_WAIT: Final[timedelta] = timedelta(seconds=100)
# A starved guest can hold an editor's connection to the helper this long before Studio retries it.
LISTING_RECOVERY_WAIT: Final[timedelta] = timedelta(seconds=260)
PLUGIN_ALERT_INTERVAL: Final[timedelta] = timedelta(seconds=60)
EDITOR_LIST_WAIT: Final[timedelta] = timedelta(seconds=20)
GUEST_NAME: Final[re.Pattern[str]] = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
EXTENDED_REGEX_SPECIAL: Final[re.Pattern[str]] = re.compile(r"([.^$*+?()\[\]{}|\\])")
LUAU_STRING_ESCAPE: Final[re.Pattern[str]] = re.compile(r'[\\"\x00-\x1f\x7f]')
KEEP_PLUGINS_SCRIPT: Final[str] = ('script=$(mktemp -t guest-studio-mcp) && cat > "$script" && '
                                   'osascript -l JavaScript "$script" keep-plugins; status=$?; rm -f "$script"; '
                                   'exit $status')
REGISTRATION_DIAGNOSIS_SCRIPT: Final[str] = f'''uptime
for pid in $(pgrep -x RobloxStudio); do
  if lsof -nP -a -p "$pid" -iTCP:{HELPER_PORT} -sTCP:ESTABLISHED >/dev/null 2>&1; then
    echo "Studio process $pid holds a connection to the MCP helper"
  else
    echo "Studio process $pid holds no connection to the MCP helper"
  fi
done'''
# Every Studio editor in the guest, leaving out Play test servers and clients. The executable is read on its own, since
# this script's own shell carries Studio's path in its command line.
RUNNING_EDITORS_SCRIPT: Final[str] = f"""pids=
for pid in $(pgrep -f {shlex.quote(STUDIO_EXECUTABLE)}); do
  case "$(ps -o comm= -p "$pid")" in {shlex.quote(STUDIO_EXECUTABLE)}) ;; *) continue;; esac
  case "$(ps -o command= -p "$pid")" in *-edittargetid*|*-playerEmulator*) continue;; esac
  pids="$pids $pid"
done"""


class StudioMcpSession:
    """An MCP transport into the runner's Studio."""

    def __init__(self, config: RunnerConfig) -> None:
        """Open an initialized session to the configured runner."""

        self.vm = config["ROBLOX_STUDIO_VM"]

        run_guest_command(MCP_HELPER_KEEPER, config, OPERATION_TIMEOUTS[RunnerOperation.HELPER_CHECK])

        self.server_errors = tempfile.TemporaryFile()
        self.process = subprocess.Popen([str(RUNNER_SSH), STUDIO_MCP], stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=self.server_errors, bufsize=0,
                                        env=runner_environment(config))

        self.stdin = cast(IO[bytes], self.process.stdin)
        self.stdout = cast(IO[bytes], self.process.stdout)
        self.identity = 0
        self.received = b""
        initialized = False

        try:
            self.request("initialize", {"protocolVersion": PROTOCOL_VERSION, "capabilities": {},
                                        "clientInfo": {"name": "roblox-studio-skill", "version": "1.0"}},
                         OPERATION_TIMEOUTS[RunnerOperation.INITIALIZE])

            self.write(JsonRpcMessage(jsonrpc="2.0", method="notifications/initialized"))

            initialized = True
        finally:
            if not initialized:
                self.close()

    def write(self, message: JsonRpcMessage) -> None:
        """Send one JSON-RPC message to the server."""

        self.stdin.write((json.dumps(message) + "\n").encode())
        self.stdin.flush()

    def server_error_output(self) -> str:
        """Return what the server has written to stderr."""

        self.server_errors.seek(0)

        return self.server_errors.read().decode(errors="replace")

    def request(self, method: str, params: Mapping[str, JsonValue], timeout: timedelta) -> JsonRpcMessage:
        """Send a request to the server."""

        self.identity += 1
        self.write(JsonRpcMessage(jsonrpc="2.0", id=self.identity, method=method, params=params))

        deadline = time.monotonic() + timeout.total_seconds()

        while time.monotonic() < deadline:
            if b"\n" not in self.received:
                if not select.select([self.stdout], [], [], max(0, deadline - time.monotonic()))[0]:
                    break

                chunk = os.read(self.stdout.fileno(), 65536)

                if not chunk:
                    raise RuntimeError(f"Studio MCP exited: {self.server_error_output()}")

                self.received += chunk
                continue

            line, self.received = self.received.split(b"\n", 1)
            response: JsonRpcMessage = json.loads(line)

            if response.get("id") == self.identity:
                return response

        raise TimeoutError(f"Studio MCP timed out: {method}")

    def close(self) -> None:
        """Stop the server."""

        if self.process.poll() is None:
            self.process.terminate()

            try:
                self.process.wait(timeout=OPERATION_TIMEOUTS[RunnerOperation.SESSION_EXIT].total_seconds())
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()

        for stream in (self.stdin, self.stdout, self.server_errors):
            stream.close()


class StudioMcpConnection:
    """A Studio MCP connection to the runner."""

    def __init__(self) -> None:
        """Create the connection."""

        self.session: StudioMcpSession | None = None
        # The session reads every reply from one pipe and drops a reply meant for another request, so the threads
        # sharing this connection send one request at a time.
        self.turn = threading.Lock()

        atexit.register(self.close)

    def request(self, method: str, params: Mapping[str, JsonValue], timeout: timedelta,
                config: RunnerConfig) -> JsonRpcMessage:
        """Send a request over the session to the configured runner, waiting for its turn within the timeout."""

        started = time.monotonic()

        if not self.turn.acquire(timeout=timeout.total_seconds()):
            raise TimeoutError(f"Studio MCP timed out waiting for another request on the connection: {method}")

        try:
            return self.session_request(method, params, timeout - timedelta(seconds=time.monotonic() - started),
                                        config)
        finally:
            self.turn.release()

    def session_request(self, method: str, params: Mapping[str, JsonValue], timeout: timedelta,
                        config: RunnerConfig) -> JsonRpcMessage:
        """Send a request while holding the connection's turn, unless a renewal has found a lock on the runner lost."""

        assert_runner_locks_kept(config)

        if self.session is None:
            self.session = StudioMcpSession(config)
        elif self.session.vm != config["ROBLOX_STUDIO_VM"]:
            open_vm = self.session.vm

            self.close()

            raise RuntimeError(f"The open session reaches {open_vm}, but the game's VM is now "
                               f"{config['ROBLOX_STUDIO_VM']}")

        answered = False

        try:
            response = self.session.request(method, params, timeout)
            answered = True
        finally:
            if not answered:
                self.close()

        return response

    def close(self) -> None:
        """Close the open session."""

        if self.session is not None:
            self.session.close()
            self.session = None


class StudioToolError(RuntimeError):
    """A Studio MCP tool call that Studio answered with an error."""


def call_studio_tool(connection: StudioMcpConnection, name: str, arguments: ToolArguments, lock_receipt: Path,
                     timeout: timedelta = OPERATION_TIMEOUTS[RunnerOperation.TOOL_CALL]) -> list[McpContent]:
    """Call a Studio MCP tool."""

    config = assert_runner_lock_held(lock_receipt)

    return studio_tool_reply(connection, name, arguments, config, timeout)


def studio_tool_reply(connection: StudioMcpConnection, name: str, arguments: ToolArguments, config: RunnerConfig,
                      timeout: timedelta = OPERATION_TIMEOUTS[RunnerOperation.TOOL_CALL]) -> list[McpContent]:
    """Call a Studio MCP tool on a runner whose lease the caller has already checked."""

    response = connection.request("tools/call", {"name": name, "arguments": arguments}, timeout, config)

    if "error" in response or "result" not in response or response["result"].get("isError"):
        raise StudioToolError(json.dumps(response))

    return response["result"]["content"]


def mcp_content_text(content: list[McpContent]) -> str:
    """Join the text parts of an MCP tool result."""

    return "\n".join(part["text"] for part in content if part["type"] == "text")


def studios(connection: StudioMcpConnection, lock_receipt: Path) -> list[StudioEntry]:
    """List the editors the runner's Studio MCP knows."""

    config = assert_runner_lock_held(lock_receipt)

    return listed_studios(connection, config)


def listed_studios(connection: StudioMcpConnection, config: RunnerConfig) -> list[StudioEntry]:
    """List the editors the Studio MCP of a runner whose lease the caller has already checked knows."""

    listing = mcp_content_text(studio_tool_reply(connection, "list_roblox_studios", {}, config))

    return json.loads(listing).get("studios", [])


def poll_until[T](probe: Callable[[], T | None], wait: timedelta) -> T | None:
    """Poll probe until it gives a value or wait runs out."""

    deadline = time.monotonic() + wait.total_seconds()

    while True:
        value = probe()

        if value is not None or time.monotonic() >= deadline:
            return value

        time.sleep(POLL_INTERVAL.total_seconds())


def keep_studio_plugins(config: RunnerConfig) -> None:
    """Answer every open stalled-plugin alert in the editors of a runner whose lease the caller has already checked."""

    try:
        report = run_guest_command(KEEP_PLUGINS_SCRIPT, config, OPERATION_TIMEOUTS[RunnerOperation.PLUGIN_ALERT],
                                   GUEST_STUDIO_MCP.read_bytes()).decode().strip()
    except (RuntimeError, subprocess.TimeoutExpired):
        logger.warning("Studio's stalled-plugin alerts were not answered", exc_info=True)

        return

    if report:
        logger.warning("Studio's stalled-plugin alerts: %s", report)


def poll_registration[T](probe: Callable[[], T | None], wait: timedelta, config: RunnerConfig) -> T | None:
    """Return the first value probe gives within wait, keeping stalled Studio plugins running meanwhile, or None."""

    deadline = time.monotonic() + wait.total_seconds()
    next_alert_pass = time.monotonic() + PLUGIN_ALERT_INTERVAL.total_seconds()

    def _probe_keeping_plugins() -> T | None:
        nonlocal next_alert_pass

        value = probe()
        now = time.monotonic()
        alert_pass_fits = deadline - now > OPERATION_TIMEOUTS[RunnerOperation.PLUGIN_ALERT].total_seconds()

        if value is None and now >= next_alert_pass and alert_pass_fits:
            keep_studio_plugins(config)

            next_alert_pass = time.monotonic() + PLUGIN_ALERT_INTERVAL.total_seconds()

        return value

    return poll_until(_probe_keeping_plugins, wait)


def registration_failure_cause(config: RunnerConfig) -> str:
    """Describe why a checked runner's Studio MCP does not list an editor whose process runs."""

    try:
        diagnosis = run_guest_command(REGISTRATION_DIAGNOSIS_SCRIPT, config,
                                      OPERATION_TIMEOUTS[RunnerOperation.DIAGNOSIS]).decode()

        state = "; ".join(line.strip() for line in diagnosis.splitlines() if line.strip())
    except (RuntimeError, subprocess.TimeoutExpired) as error:
        logger.warning("The guest's Studio MCP state could not be read", exc_info=True)

        state = f"unreadable ({type(error).__name__}: {error})"

    return (f"each editor reaches Studio MCP through its built-in Assistant plugin, which stalls while the guest is "
            f"starved; guest state: {state}")


def wait_for_studios(connection: StudioMcpConnection, lock_receipt: Path,
                     wait: timedelta = EDITOR_LIST_WAIT) -> list[StudioEntry]:
    """List the runner's editors, waiting out the empty list a new MCP connection reports at first."""

    return awaited_studios(connection, assert_runner_lock_held(lock_receipt), wait)


def awaited_studios(connection: StudioMcpConnection, config: RunnerConfig, wait: timedelta) -> list[StudioEntry]:
    """List the editors of a runner whose lease the caller has already checked, waiting out an empty list."""

    return poll_until(lambda: listed_studios(connection, config) or None, wait) or []


def listed_editor_ids(connection: StudioMcpConnection, lock_receipt: Path) -> set[str]:
    """Snapshot the IDs of the runner's editors on a connection, for new_editors to compare against."""

    return {studio["id"] for studio in wait_for_studios(connection, lock_receipt)}


def new_editors(known: Collection[str], connection: StudioMcpConnection, lock_receipt: Path) -> list[StudioEntry]:
    """List the editors the connection reports beyond the known IDs a listed_editor_ids snapshot gave."""

    return [studio for studio in studios(connection, lock_receipt) if studio["id"] not in known]


def luau_string_literal(value: str) -> str:
    """Quote a string as a Luau string literal."""

    escaped = LUAU_STRING_ESCAPE.sub(lambda match: f"\\x{ord(match.group()):02x}", value)

    return f'"{escaped}"'


class Studio:
    """An editor in the runner."""

    def __init__(self, studio_id: str, lock_receipt: Path, connection: StudioMcpConnection | None = None) -> None:
        """Address an editor by its MCP studio ID."""

        self.studio_id = studio_id
        self.lock_receipt = lock_receipt
        self.connection = connection if connection is not None else StudioMcpConnection()

    def await_listing(self, config: RunnerConfig) -> None:
        """Wait for the connection to list this editor, keeping stalled Studio plugins running meanwhile."""

        def _listed() -> bool | None:
            return any(studio["id"] == self.studio_id for studio in listed_studios(self.connection, config)) or None

        if poll_registration(_listed, LISTING_RECOVERY_WAIT, config) is None:
            raise RuntimeError(f"Studio MCP has not listed editor {self.studio_id} for "
                               f"{LISTING_RECOVERY_WAIT.total_seconds():.0f} s: {registration_failure_cause(config)}")

    def tool(self, name: str, arguments: ToolArguments,
             timeout: timedelta = OPERATION_TIMEOUTS[RunnerOperation.TOOL_CALL]) -> list[McpContent]:
        """Call a Studio MCP tool on this editor, once a new connection lists it."""

        arguments = {**arguments, "studio_id": self.studio_id}

        if self.connection.session is not None:
            return call_studio_tool(self.connection, name, arguments, self.lock_receipt, timeout)

        config = assert_runner_lock_held(self.lock_receipt)

        self.await_listing(config)

        return studio_tool_reply(self.connection, name, arguments, config, timeout)

    def execute(self, code: str, data_model: str = "Client",
                timeout: timedelta = OPERATION_TIMEOUTS[RunnerOperation.TOOL_CALL]) -> str:
        """Run Luau in one of the editor's data models."""

        return mcp_content_text(self.tool("execute_luau", {"datamodel_type": data_model, "code": code}, timeout))

    def console(self) -> str:
        """Return the editor's console output."""

        return mcp_content_text(self.tool("get_console_output", {}))

    def capture(self, name: str, out_dir: Path, view: CameraView | None = None) -> list[Path]:
        """Save the editor's screenshots under out_dir."""

        if Path(name).name != name:
            raise ValueError(f"Name a capture with one file name, not a path: {name!r}")

        arguments: dict[str, JsonValue] = {"capture_id": name}

        if view is not None:
            arguments["camera_position"] = view["position"]
            arguments["look_at_position"] = view["look_at"]

        out_dir.mkdir(parents=True, exist_ok=True)

        paths: list[Path] = []

        for index, part in enumerate(self.tool("screen_capture", arguments)):
            if part["type"] == "image":
                path = out_dir / f"{name}-{index}.png"

                path.write_bytes(base64.b64decode(part["data"]))
                paths.append(path)

        if not paths:
            raise RuntimeError("Studio returned no screenshot")

        return paths

    def keys(self, actions: Sequence[Mapping[str, JsonValue]]) -> list[McpContent]:
        """Send keyboard actions to the editor's client."""

        return self.tool("user_keyboard_input", {"datamodel_type": "Client", "actions": actions})

    def run_input(self, code: str, timeout: timedelta = OPERATION_TIMEOUTS[RunnerOperation.TOOL_CALL]) -> str:
        """Run Luau on the editor's client with the bundled VirtualInput helper bound to Input."""

        return self.execute(f"local Input = (function()\n{VIRTUAL_INPUT.read_text()}\nend)()\n{code}", "Client",
                            timeout)

    def click(self, path: str, count: int = 1) -> str:
        """Click a button by its instance path."""

        if not 1 <= count <= 10:
            raise ValueError("Use one to ten button clicks")

        return self.run_input(f'''local names = string.split({luau_string_literal(path)}, ".")
local button = game
if names[1] == "LocalPlayer" then button = game.Players.LocalPlayer; table.remove(names, 1)
elseif names[1] == "game" then table.remove(names, 1) end
for _, name in names do button = assert(button:FindFirstChild(name), "Missing button path") end
local input = Input.new()
for _ = 1, {count} do input:click(button) end
input:release()
return "Button input delivered"''')

    def hold_key(self, key: str, duration: timedelta) -> str:
        """Hold a key, named as its Enum.KeyCode member, on the editor's client for the duration."""

        if duration <= timedelta():
            raise ValueError("Hold a key for a positive duration")

        return self.run_input(f'''local keyCode = Enum.KeyCode[{luau_string_literal(key)}]
local input = Input.new()
local held, problem = pcall(input.key, input, keyCode, {duration.total_seconds()})
input:release()
if not held then error(problem, 0) end
return "Key input delivered"''', OPERATION_TIMEOUTS[RunnerOperation.TOOL_CALL] + duration)

    def buttons(self, screen: str) -> list[StudioButton]:
        """List the TextButtons on one of the player's screens."""

        return json.loads(self.execute(f'''local buttons = {{}}
for _, object in game.Players.LocalPlayer.PlayerGui[{luau_string_literal(screen)}]:GetDescendants() do
	if object:IsA("TextButton") then
		table.insert(buttons, {{path = object:GetFullName(), text = object.Text, active = object.Interactable,
			x = object.AbsolutePosition.X, y = object.AbsolutePosition.Y,
			width = object.AbsoluteSize.X, height = object.AbsoluteSize.Y}})
	end
end
return game.HttpService:JSONEncode(buttons)''', "Client"))


def guest_place(project: str, place: Path) -> str:
    """Return the guest path of a project's place copy."""

    for name in (project, place.name):
        if not GUEST_NAME.fullmatch(name):
            raise ValueError(f"Guest place names use letters, digits, '.', '_' and '-': {name!r}")

    return f"{GUEST_PLACES}/{project}/{place.name}"


def extended_regex_literal(value: str) -> str:
    """Escape a string for a POSIX extended regular expression."""

    return EXTENDED_REGEX_SPECIAL.sub(r"\\\1", value)


def editor_pids_script(guest_path: str) -> str:
    """Return guest shell that sets pids to the editors holding a place copy open."""

    pattern = shlex.quote(f"localPlaceFile ([^ ]*/)?{extended_regex_literal(guest_path)}( |$)")

    return f'''target="$HOME"/{shlex.quote(guest_path)}
pids=
for pid in $(pgrep -f {pattern}); do
  process_command=$(ps -o command= -p "$pid") || continue
  case "$process_command " in *" --localPlaceFile $target "*) pids="$pids $pid";; esac
done'''


def named_editor_pids_script(place_name: str) -> str:
    """Return guest shell that sets pids to the editors holding any project's copy of a place file name open."""

    pattern = shlex.quote(f"localPlaceFile ([^ ]*/)?{GUEST_PLACES}/[^/ ]+/{extended_regex_literal(place_name)}( |$)")

    return f'''pids=
for pid in $(pgrep -f {pattern}); do
  process_command=$(ps -o command= -p "$pid") || continue
  case "$process_command " in *" --localPlaceFile $HOME/{GUEST_PLACES}/"*"/{place_name} "*) pids="$pids $pid";; esac
done'''


def cloud_editor_pids_script(place_id: int) -> str:
    """Return guest shell that sets pids to the editors open_cloud_place launched on a published place."""

    return f'''pids=
for pid in $(pgrep -f 'placeId {place_id}( |$)'); do
  process_command=$(ps -o command= -p "$pid") || continue
  case "$process_command " in *" --task EditPlace "*) ;; *) continue;; esac
  case "$process_command " in *" --placeId {place_id} "*) pids="$pids $pid";; esac
done'''


def guest_pid_sets(pids_scripts: Sequence[str], config: RunnerConfig) -> list[set[int]]:
    """Run guest shell scripts that each set pids, returning the process IDs each one found."""

    command = "\n".join(f"{pids_script}\necho $pids" for pids_script in pids_scripts)
    listed = run_guest_command(command, config, OPERATION_TIMEOUTS[RunnerOperation.PROCESS_LIST]).decode().split("\n")

    return [{int(pid) for pid in line.split()} for line in listed[:len(pids_scripts)]]


def stop_guest_processes(pids: Collection[int], lock_receipt: Path) -> set[int]:
    """Stop guest processes and return those still running."""

    config = assert_runner_lock_held(lock_receipt)

    return stopped_survivors(pids, config)


def stopped_survivors(pids: Collection[int], config: RunnerConfig) -> set[int]:
    """Stop processes in the guest of a runner whose lease the caller has already checked, and return survivors."""

    if any(pid < 2 for pid in pids):
        raise ValueError("Guest process IDs start at 2")

    if not pids:
        return set()

    spaced = " ".join(str(pid) for pid in sorted(pids))
    listed = spaced.replace(" ", ",")

    # An editor with a place open answers SIGTERM with its unsaved-changes prompt, so it is then killed.
    script = f'''kill -TERM {spaced} 2>/dev/null
for _ in 1 2 3 4 5; do ps -p {listed} >/dev/null || exit 0; sleep 1; done
kill -KILL {spaced} 2>/dev/null
for _ in 1 2 3 4 5; do ps -p {listed} >/dev/null || exit 0; sleep 1; done
ps -o pid= -p {listed}
true'''

    survivors = run_guest_command(script, config, OPERATION_TIMEOUTS[RunnerOperation.STOP]).decode()

    return {int(pid) for pid in survivors.split()}


def listed_place_editors(project: str, place: Path, connection: StudioMcpConnection,
                         lock_receipt: Path) -> list[StudioEntry]:
    """List the editors named for a project's place copy once Studio MCP lists one, or none while none has it open."""

    guest_path = guest_place(project, place)

    config = assert_runner_lock_held(lock_receipt)

    [pids] = guest_pid_sets([editor_pids_script(guest_path)], config)

    if not pids:
        return []

    def _listed() -> list[StudioEntry] | None:
        return [studio for studio in listed_studios(connection, config) if studio.get("name") == place.name] or None

    listed = poll_registration(_listed, LISTING_RECOVERY_WAIT, config)

    if listed is None:
        raise RuntimeError(f"The editor for {guest_path} runs as process {sorted(pids)}, but Studio MCP has not listed "
                           f"it for {LISTING_RECOVERY_WAIT.total_seconds():.0f} s: "
                           f"{registration_failure_cause(config)}")

    return listed


def guest_screenshot(path: Path, lock_receipt: Path) -> Path:
    """Save the runner guest's whole screen to path."""

    config = assert_runner_lock_held(lock_receipt)

    return saved_guest_screen(path, config)


def saved_guest_screen(path: Path, config: RunnerConfig) -> Path:
    """Save the whole screen of a runner guest whose lease the caller has already checked to path."""

    screen = run_guest_command('f=$(mktemp -t studio-screen) && screencapture -x -t png "$f" && cat "$f"; '
                               'capture_status=$?; rm -f "$f"; exit $capture_status', config,
                               OPERATION_TIMEOUTS[RunnerOperation.CAPTURE])

    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_bytes(screen)

    return path


def close_place(project: str, place: Path, lock_receipt: Path) -> None:
    """Close a project's place copy in the runner."""

    close_place_copy_on_runner(project, place, assert_runner_lock_held(lock_receipt))


def close_place_copy_on_runner(project: str, place: Path, config: RunnerConfig) -> None:
    """Close a project's place copy in a runner whose lease the caller has already checked."""

    guest_path = guest_place(project, place)

    [holding] = guest_pid_sets([editor_pids_script(guest_path)], config)
    survivors = stopped_survivors(holding, config)

    if survivors:
        raise RuntimeError(f"The editor for {guest_path} is still open, so its copy stays in the guest")

    # Studio leaves a lock file beside a place it opened.
    files = f"{shlex.quote(guest_path)} {shlex.quote(f'{guest_path}.lock')}"
    folder = shlex.quote(str(Path(guest_path).parent))

    run_guest_command(f'cd "$HOME" && rm -f {files}; rmdir {folder} 2>/dev/null; true', config,
                      OPERATION_TIMEOUTS[RunnerOperation.REMOVAL])


def close_cloud_place(place_id: int, lock_receipt: Path) -> None:
    """End, without saving, the runner editors open_cloud_place launched on a published place."""

    close_cloud_editors_on_runner(place_id, assert_runner_lock_held(lock_receipt))


def close_cloud_editors_on_runner(place_id: int, config: RunnerConfig) -> None:
    """End, without saving, the cloud editors on a place in a runner whose lease the caller has already checked."""

    [holding] = guest_pid_sets([cloud_editor_pids_script(place_id)], config)
    survivors = stopped_survivors(holding, config)

    if survivors:
        raise RuntimeError(f"The editor for place {place_id} is still open: {sorted(survivors)}")


def reported_place_ids(connection: StudioMcpConnection, studio_id: str, config: RunnerConfig) -> PlaceIds | None:
    """Return the place and universe IDs an editor's Edit data model reports, or None while it runs no code yet."""

    # An editor still loading its place answers with an error or not at all.
    try:
        reply = studio_tool_reply(connection, "execute_luau", {
            "studio_id": studio_id, "datamodel_type": "Edit",
            "code": 'return game:GetService("HttpService"):JSONEncode({place_id = game.PlaceId, '
                    'universe_id = game.GameId})'}, config, OPERATION_TIMEOUTS[RunnerOperation.EDIT_PROBE])
    except (StudioToolError, TimeoutError):
        return None

    return json.loads(mcp_content_text(reply))


def launch_editor(launch: str, data: bytes | None, editor_name: str | None, expected: PlaceIds | None,
                  failure_screen: Path, close: Callable[[RunnerConfig], None], config: RunnerConfig,
                  lock_receipt: Path, registration_wait: timedelta) -> Studio:
    """Launch an editor through a guest command and return it once its Edit data model answers."""

    connection = StudioMcpConnection()
    opened = False

    try:
        known = {studio["id"] for studio in awaited_studios(connection, config, EDITOR_LIST_WAIT)}

        run_guest_command(launch, config, OPERATION_TIMEOUTS[RunnerOperation.COPY]
                          + OPERATION_TIMEOUTS[RunnerOperation.LAUNCH], data)

        probed: list[str] = []
        reports: dict[str, PlaceIds | None] = {}

        def _next_answering() -> str | None:
            """Probe the least recently probed new editor, returning it once it answers for the expected place."""

            listed = listed_studios(connection, config)
            candidates = [studio["id"] for studio in listed if studio["id"] not in known
                          and (editor_name is None or studio.get("name") == editor_name)]

            if not candidates:
                return None

            fresh = [candidate for candidate in candidates if candidate not in probed]
            studio_id = fresh[0] if fresh else next(candidate for candidate in probed if candidate in candidates)

            if studio_id in probed:
                probed.remove(studio_id)

            probed.append(studio_id)

            ids = reported_place_ids(connection, studio_id, config)
            reports[studio_id] = ids

            return studio_id if ids is not None and (expected is None or ids == expected) else None

        studio_id = poll_registration(_next_answering, registration_wait, config)

        if studio_id is not None:
            opened = True

            return Studio(studio_id, lock_receipt, connection)

        if not reports:
            failure = f"never registered with Studio MCP: {registration_failure_cause(config)}"
        elif expected is None:
            failure = "never ran code in its Edit data model"
        else:
            answers = "; ".join(f"{candidate} ran no code" if ids is None else f"{candidate} reported {ids}"
                                for candidate, ids in reports.items())

            failure = (f"never reported place {expected['place_id']} of universe {expected['universe_id']}; "
                       f"the new editors: {answers}")

        try:
            saved_guest_screen(failure_screen, config)
        except LockOwnershipLost as lost:
            raise LockOwnershipLost(f"{lost}; the editor {failure}") from lost

        raise RuntimeError(f"The editor {failure}; screen saved to {failure_screen}")
    finally:
        if not opened:
            connection.close()

            try:
                assert_runner_locks_kept(config)
            except LockOwnershipLost:
                logger.warning("The failed launch's editor stays open, since its runner lock was lost", exc_info=True)
            else:
                close(config)


def open_place(project: str, place: Path, out_dir: Path, lock_receipt: Path,
               registration_wait: timedelta = DEFAULT_REGISTRATION_WAIT) -> Studio:
    """Open a built place in a runner editor, returning it once its Edit data model runs code."""

    guest_path = guest_place(project, place)

    config = assert_runner_lock_held(lock_receipt)
    launch = (f'cd "$HOME" && mkdir -p {shlex.quote(str(Path(guest_path).parent))} && '
              f'cat > {shlex.quote(guest_path)} && open -n -a {shlex.quote(STUDIO_APP)} --args --task EditFile '
              f'--localPlaceFile "$HOME"/{shlex.quote(guest_path)}')

    # Editors starting together refresh Studio's shared sign-in at once, and Roblox revokes a refresh token used twice.
    with focused_input(lock_receipt, f"Launch {place.name}"):
        # Studio MCP names an editor by its place's file name alone, so two open copies of one name cannot be told
        # apart.
        holding, running = guest_pid_sets([named_editor_pids_script(place.name), RUNNING_EDITORS_SCRIPT], config)

        if holding:
            raise RuntimeError(f"An editor already has a place named {place.name} open, {guest_path} or another "
                               "project's copy; use it or close it with close_place first")

        assert_editor_launch_allowed(lock_receipt, config, project, running)

        return launch_editor(launch, place.read_bytes(), place.name, None,
                             out_dir / f"launch-failure-{place.stem}.png",
                             lambda checked: close_place_copy_on_runner(project, place, checked), config, lock_receipt,
                             registration_wait)


def open_cloud_place(place_id: int, universe_id: int, out_dir: Path, lock_receipt: Path,
                     registration_wait: timedelta = DEFAULT_REGISTRATION_WAIT) -> Studio:
    """Open a published place in a runner editor, returning it once its Edit data model reports that place."""

    if place_id < 1 or universe_id < 1:
        raise ValueError("Published places have positive place and universe IDs")

    config = assert_runner_lock_held(lock_receipt)
    launch = (f"open -n -a {shlex.quote(STUDIO_APP)} --args --task EditPlace --placeId {place_id} "
              f"--universeId {universe_id}")

    with focused_input(lock_receipt, f"Launch place {place_id}"):
        holding, running = guest_pid_sets([cloud_editor_pids_script(place_id), RUNNING_EDITORS_SCRIPT], config)

        if holding:
            raise RuntimeError(f"An editor already has place {place_id} open; use it or close it with "
                               "close_cloud_place first")

        assert_editor_launch_allowed(lock_receipt, config, None, running)

        return launch_editor(launch, None, None, PlaceIds(place_id=place_id, universe_id=universe_id),
                             out_dir / f"launch-failure-place-{place_id}.png",
                             lambda checked: close_cloud_editors_on_runner(place_id, checked), config, lock_receipt,
                             registration_wait)
