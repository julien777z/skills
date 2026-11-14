from __future__ import annotations

import atexit
import base64
import json
import os
import re
import select
import shlex
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable, Collection, Mapping, Sequence
from datetime import timedelta
from pathlib import Path
from types import MappingProxyType
from typing import IO, Final, cast

from studio_mcp.models import (AgentLockAcquireReport, AgentLockCheckReport, CameraView, JsonRpcMessage, JsonValue,
                               McpContent, PlaceIds, RunnerConfig, RunnerLease, RunnerOperation, StudioButton,
                               StudioEntry, ToolArguments)

# Paths stay on the unresolved install link: installed skills sit side by side there, and a refresh that replaces
# the linked source mid-run leaves them valid.
SCRIPTS: Final[Path] = Path(__file__).absolute().parents[1]
RUNNER_SSH: Final[Path] = SCRIPTS / "runner_ssh.sh"
VIRTUAL_INPUT: Final[Path] = SCRIPTS / "virtual_input.luau"
AGENT_LOCK: Final[Path] = SCRIPTS.parents[1] / "agent-lock" / "resources" / "main.py"
STUDIO_APP: Final[str] = "/Applications/RobloxStudio.app"
STUDIO_MCP: Final[str] = f"{STUDIO_APP}/Contents/MacOS/StudioMCP"
GUEST_PLACES: Final[str] = "studio-places"
PROTOCOL_VERSION: Final[str] = "2024-11-05"
OPERATION_TIMEOUTS: Final[Mapping[RunnerOperation, timedelta]] = MappingProxyType({
    RunnerOperation.INITIALIZE: timedelta(seconds=55),
    RunnerOperation.TOOL_CALL: timedelta(seconds=55),
    RunnerOperation.COPY: timedelta(seconds=120),
    RunnerOperation.LAUNCH: timedelta(seconds=60),
    RunnerOperation.CAPTURE: timedelta(seconds=60),
    RunnerOperation.EDIT_PROBE: timedelta(seconds=15),
    RunnerOperation.PROCESS_LIST: timedelta(seconds=30),
    RunnerOperation.STOP: timedelta(seconds=60),
    RunnerOperation.REMOVAL: timedelta(seconds=30),
    RunnerOperation.LOCK_CHECK: timedelta(seconds=30),
    RunnerOperation.DESCRIBE: timedelta(seconds=30),
    RunnerOperation.SESSION_EXIT: timedelta(seconds=5),
})
CLOUD_CLOSE_BOUND: Final[timedelta] = (OPERATION_TIMEOUTS[RunnerOperation.PROCESS_LIST]
                                       + OPERATION_TIMEOUTS[RunnerOperation.STOP])
CLOSE_BOUND: Final[timedelta] = CLOUD_CLOSE_BOUND + OPERATION_TIMEOUTS[RunnerOperation.REMOVAL]
LEASE_CHECK_BOUND: Final[timedelta] = (OPERATION_TIMEOUTS[RunnerOperation.DESCRIBE]
                                       + OPERATION_TIMEOUTS[RunnerOperation.LOCK_CHECK])
LOCK_WAIT: Final[timedelta] = timedelta(seconds=50)
# agent-lock refuses a lease longer than this.
MAX_LEASE: Final[timedelta] = timedelta(seconds=900)
POLL_INTERVAL: Final[timedelta] = timedelta(seconds=2)
DEFAULT_REGISTRATION_WAIT: Final[timedelta] = timedelta(seconds=180)
EDITOR_LIST_WAIT: Final[timedelta] = timedelta(seconds=20)
GUEST_NAME: Final[re.Pattern[str]] = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
EXTENDED_REGEX_SPECIAL: Final[re.Pattern[str]] = re.compile(r"([.^$*+?()\[\]{}|\\])")
LUAU_STRING_ESCAPE: Final[re.Pattern[str]] = re.compile(r'[\\"\x00-\x1f\x7f]')


def runner_config() -> RunnerConfig:
    """Return the game's runner configuration as its settings files name it now."""

    result = subprocess.run([str(RUNNER_SSH), "--describe"], capture_output=True, text=True,
                            timeout=OPERATION_TIMEOUTS[RunnerOperation.DESCRIBE].total_seconds())

    if result.returncode != 0:
        raise RuntimeError(f"No runner VM resolved for this game:\n{result.stderr}")

    values = dict(assignment.split("=", 1) for assignment in shlex.split(result.stdout))

    return RunnerConfig(ROBLOX_STUDIO_GAME=values["ROBLOX_STUDIO_GAME"],
                        ROBLOX_STUDIO_TART=values["ROBLOX_STUDIO_TART"],
                        ROBLOX_STUDIO_VM=values["ROBLOX_STUDIO_VM"],
                        ROBLOX_STUDIO_SSH_USER=values["ROBLOX_STUDIO_SSH_USER"],
                        ROBLOX_STUDIO_SSH_KEY=values["ROBLOX_STUDIO_SSH_KEY"],
                        ROBLOX_STUDIO_KNOWN_HOSTS=values["ROBLOX_STUDIO_KNOWN_HOSTS"])


def runner_environment(config: RunnerConfig) -> dict[str, str]:
    """Return the environment that holds runner_ssh.sh to the game a lease check resolved."""

    return {**os.environ, "ROBLOX_STUDIO_GAME": config["ROBLOX_STUDIO_GAME"]}


def acquire_runner_lock(lock_receipt: Path, owner: str, activity: str, lease: timedelta = MAX_LEASE,
                        wait: timedelta = LOCK_WAIT) -> AgentLockAcquireReport:
    """Take the lock on the game's runner VM for one segment of work, writing its receipt to lock_receipt."""

    lock_key = runner_config()["ROBLOX_STUDIO_VM"]

    lock_receipt.parent.mkdir(parents=True, exist_ok=True)

    result = subprocess.run([sys.executable, str(AGENT_LOCK), "acquire", lock_key, "--owner", owner, "--activity",
                             activity, "--receipt", str(lock_receipt), "--wait-seconds", str(wait.total_seconds()),
                             "--ttl-seconds", str(lease.total_seconds())],
                            capture_output=True, text=True,
                            timeout=(wait + OPERATION_TIMEOUTS[RunnerOperation.LOCK_CHECK]).total_seconds())

    if result.returncode != 0:
        raise RuntimeError(f"The {lock_key} lock was not acquired ({result.returncode}):\n"
                           f"{result.stdout}{result.stderr}")

    return json.loads(result.stdout)


def release_runner_lock(lock_receipt: Path) -> None:
    """Release the runner lock the receipt owns, stating to agent-lock that the runner is idle."""

    result = subprocess.run([sys.executable, str(AGENT_LOCK), "release", "--receipt", str(lock_receipt),
                             "--resource-idle"], capture_output=True, text=True,
                            timeout=OPERATION_TIMEOUTS[RunnerOperation.LOCK_CHECK].total_seconds())

    if result.returncode != 0:
        raise RuntimeError(f"Receipt {lock_receipt} did not release its lock:\n{result.stderr}")


def runner_lease(lock_receipt: Path) -> RunnerLease:
    """Return the game's runner and how long the receipt's lease on its lock has left."""

    config = runner_config()
    lock_key = config["ROBLOX_STUDIO_VM"]

    result = subprocess.run([sys.executable, str(AGENT_LOCK), "check", "--receipt", str(lock_receipt)],
                            capture_output=True, text=True,
                            timeout=OPERATION_TIMEOUTS[RunnerOperation.LOCK_CHECK].total_seconds())

    if result.returncode != 0:
        raise RuntimeError(f"Receipt {lock_receipt} does not own a lock:\n{result.stderr}")

    report: AgentLockCheckReport = json.loads(result.stdout)

    if report["ownership"]["key"] != lock_key:
        raise RuntimeError(f"Receipt {lock_receipt} owns {report['ownership']['key']}, not {lock_key}")

    return RunnerLease(config=config, remaining=timedelta(seconds=report["remaining_seconds"]))


def assert_runner_lease_covers(lock_receipt: Path, needed: timedelta) -> RunnerConfig:
    """Assert that the receipt owns the game's runner lock for at least the needed time, and return that runner."""

    lease = runner_lease(lock_receipt)

    if lease["remaining"] < needed:
        raise RuntimeError(f"The {lease['config']['ROBLOX_STUDIO_VM']} lease has "
                           f"{lease['remaining'].total_seconds():.0f} s left; this call can take up to "
                           f"{needed.total_seconds():.0f} s")

    return lease["config"]


def run_in_runner(command: str, lock_receipt: Path, timeout: timedelta, data: bytes | None = None) -> bytes:
    """Run a shell command in the runner guest."""

    return run_guest_command(command, assert_runner_lease_covers(lock_receipt, timeout), timeout, data)


def run_guest_command(command: str, config: RunnerConfig, timeout: timedelta, data: bytes | None = None) -> bytes:
    """Run a shell command in the guest of a runner whose lease the caller has already checked."""

    # The guest's login shell may be zsh, which splits words differently, so commands always run under sh.
    result = subprocess.run([str(RUNNER_SSH), f"/bin/sh -c {shlex.quote(command)}"], input=data,
                            capture_output=True, timeout=timeout.total_seconds(), env=runner_environment(config))

    if result.returncode != 0:
        raise RuntimeError(f"Runner command failed ({result.returncode}): {command}\n{result.stderr.decode()}")

    return result.stdout


class StudioMcpSession:
    """An MCP transport into the runner's Studio."""

    def __init__(self, config: RunnerConfig) -> None:
        """Open an initialized session to the configured runner."""

        self.vm = config["ROBLOX_STUDIO_VM"]
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

        atexit.register(self.close)

    def request(self, method: str, params: Mapping[str, JsonValue], timeout: timedelta,
                config: RunnerConfig) -> JsonRpcMessage:
        """Send a request over the session to the configured runner."""

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

    config = assert_runner_lease_covers(lock_receipt, tool_call_bound(connection.session is None, timeout))

    return studio_tool_reply(connection, name, arguments, config, timeout)


def tool_call_bound(opens_session: bool,
                    timeout: timedelta = OPERATION_TIMEOUTS[RunnerOperation.TOOL_CALL]) -> timedelta:
    """Return the longest one Studio MCP tool call can take."""

    opening = OPERATION_TIMEOUTS[RunnerOperation.INITIALIZE] if opens_session else timedelta()

    return opening + timeout + OPERATION_TIMEOUTS[RunnerOperation.SESSION_EXIT]


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

    config = assert_runner_lease_covers(lock_receipt, tool_call_bound(connection.session is None))

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


def wait_for_studios(connection: StudioMcpConnection, lock_receipt: Path,
                     wait: timedelta = EDITOR_LIST_WAIT) -> list[StudioEntry]:
    """List the runner's editors, waiting out the empty list a new MCP connection reports at first."""

    return awaited_studios(connection, assert_runner_lease_covers(lock_receipt, editor_wait_bound(wait)), wait)


def editor_wait_bound(wait: timedelta) -> timedelta:
    """Return the longest waiting out a new connection's empty editor list can take."""

    if wait < timedelta():
        raise ValueError("Wait a duration of zero or more for the editor list")

    return wait + POLL_INTERVAL + tool_call_bound(opens_session=True)


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

    def tool(self, name: str, arguments: ToolArguments,
             timeout: timedelta = OPERATION_TIMEOUTS[RunnerOperation.TOOL_CALL]) -> list[McpContent]:
        """Call a Studio MCP tool on this editor."""

        return call_studio_tool(self.connection, name, {**arguments, "studio_id": self.studio_id},
                                self.lock_receipt, timeout)

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


def cloud_editor_pids_script(place_id: int) -> str:
    """Return guest shell that sets pids to the editors open_cloud_place launched on a published place."""

    return f'''pids=
for pid in $(pgrep -f 'placeId {place_id}( |$)'); do
  process_command=$(ps -o command= -p "$pid") || continue
  case "$process_command " in *" --task EditPlace "*) ;; *) continue;; esac
  case "$process_command " in *" --placeId {place_id} "*) pids="$pids $pid";; esac
done'''


def guest_pids(pids_script: str, config: RunnerConfig) -> set[int]:
    """Run guest shell that sets pids and return the process IDs it found."""

    listed = run_guest_command(f"{pids_script}\necho $pids", config,
                               OPERATION_TIMEOUTS[RunnerOperation.PROCESS_LIST]).decode()

    return {int(pid) for pid in listed.split()}


def stop_guest_processes(pids: Collection[int], lock_receipt: Path) -> set[int]:
    """Stop guest processes and return those still running."""

    config = assert_runner_lease_covers(lock_receipt, OPERATION_TIMEOUTS[RunnerOperation.STOP])

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


def guest_screenshot(path: Path, lock_receipt: Path) -> Path:
    """Save the runner guest's whole screen to path."""

    config = assert_runner_lease_covers(lock_receipt, OPERATION_TIMEOUTS[RunnerOperation.CAPTURE])

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

    close_place_copy_on_runner(project, place, assert_runner_lease_covers(lock_receipt, CLOSE_BOUND))


def close_place_copy_on_runner(project: str, place: Path, config: RunnerConfig) -> None:
    """Close a project's place copy in a runner whose lease the caller has already checked."""

    guest_path = guest_place(project, place)

    survivors = stopped_survivors(guest_pids(editor_pids_script(guest_path), config), config)

    if survivors:
        raise RuntimeError(f"The editor for {guest_path} is still open, so its copy stays in the guest")

    # Studio leaves a lock file beside a place it opened.
    files = f"{shlex.quote(guest_path)} {shlex.quote(f'{guest_path}.lock')}"
    folder = shlex.quote(str(Path(guest_path).parent))

    run_guest_command(f'cd "$HOME" && rm -f {files}; rmdir {folder} 2>/dev/null; true', config,
                      OPERATION_TIMEOUTS[RunnerOperation.REMOVAL])


def close_cloud_place(place_id: int, lock_receipt: Path) -> None:
    """End, without saving, the runner editors open_cloud_place launched on a published place."""

    close_cloud_editors_on_runner(place_id, assert_runner_lease_covers(lock_receipt, CLOUD_CLOSE_BOUND))


def close_cloud_editors_on_runner(place_id: int, config: RunnerConfig) -> None:
    """End, without saving, the cloud editors on a place in a runner whose lease the caller has already checked."""

    survivors = stopped_survivors(guest_pids(cloud_editor_pids_script(place_id), config), config)

    if survivors:
        raise RuntimeError(f"The editor for place {place_id} is still open: {sorted(survivors)}")


def open_bound(registration_wait: timedelta) -> timedelta:
    """Return the longest an editor launch can take, closing the editor after a failure included."""

    if registration_wait < timedelta():
        raise ValueError("Wait a duration of zero or more for the editor to register")

    editor_snapshot = editor_wait_bound(EDITOR_LIST_WAIT)
    launch = OPERATION_TIMEOUTS[RunnerOperation.COPY] + OPERATION_TIMEOUTS[RunnerOperation.LAUNCH]
    registering_call = (POLL_INTERVAL + OPERATION_TIMEOUTS[RunnerOperation.INITIALIZE]
                        + OPERATION_TIMEOUTS[RunnerOperation.TOOL_CALL])
    first_probe = tool_call_bound(opens_session=False, timeout=OPERATION_TIMEOUTS[RunnerOperation.EDIT_PROBE])
    failure_cleanup = (OPERATION_TIMEOUTS[RunnerOperation.CAPTURE] + OPERATION_TIMEOUTS[RunnerOperation.SESSION_EXIT]
                       + CLOSE_BOUND)

    return (OPERATION_TIMEOUTS[RunnerOperation.PROCESS_LIST] + editor_snapshot + launch + registration_wait
            + registering_call + first_probe + failure_cleanup)


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

        deadline = time.monotonic() + registration_wait.total_seconds()
        registered = poll_until(lambda: next((studio for studio in listed_studios(connection, config)
                                              if studio["id"] not in known
                                              and (editor_name is None or studio.get("name") == editor_name)), None),
                                registration_wait)

        if registered is None:
            failure = "never registered with Studio MCP"
        else:
            studio_id = registered["id"]

            def _answered() -> PlaceIds | None:
                """Return the IDs the editor reports once they match the expected place."""

                ids = reported_place_ids(connection, studio_id, config)

                return ids if ids is not None and (expected is None or ids == expected) else None

            remaining = timedelta(seconds=max(0.0, deadline - time.monotonic()))

            if poll_until(_answered, remaining) is not None:
                opened = True

                return Studio(studio_id, lock_receipt, connection)

            failure = ("never ran code in its Edit data model" if expected is None
                       else f"never reported place {expected['place_id']} of universe {expected['universe_id']}")

        saved_guest_screen(failure_screen, config)

        raise RuntimeError(f"The editor {failure}; screen saved to {failure_screen}")
    finally:
        if not opened:
            connection.close()
            close(config)


def open_place(project: str, place: Path, out_dir: Path, lock_receipt: Path,
               registration_wait: timedelta = DEFAULT_REGISTRATION_WAIT) -> Studio:
    """Open a built place in a runner editor, returning it once its Edit data model runs code."""

    guest_path = guest_place(project, place)

    config = assert_runner_lease_covers(lock_receipt, open_bound(registration_wait))

    if guest_pids(editor_pids_script(guest_path), config):
        raise RuntimeError(f"An editor already has {guest_path} open; use it or close it with close_place first")

    launch = (f'cd "$HOME" && mkdir -p {shlex.quote(str(Path(guest_path).parent))} && '
              f'cat > {shlex.quote(guest_path)} && open -n -a {shlex.quote(STUDIO_APP)} --args --task EditFile '
              f'--localPlaceFile "$HOME"/{shlex.quote(guest_path)}')

    return launch_editor(launch, place.read_bytes(), place.name, None, out_dir / f"launch-failure-{place.stem}.png",
                         lambda checked: close_place_copy_on_runner(project, place, checked), config, lock_receipt,
                         registration_wait)


def open_cloud_place(place_id: int, universe_id: int, out_dir: Path, lock_receipt: Path,
                     registration_wait: timedelta = DEFAULT_REGISTRATION_WAIT) -> Studio:
    """Open a published place in a runner editor, returning it once its Edit data model reports that place."""

    if place_id < 1 or universe_id < 1:
        raise ValueError("Published places have positive place and universe IDs")

    config = assert_runner_lease_covers(lock_receipt, open_bound(registration_wait))

    if guest_pids(cloud_editor_pids_script(place_id), config):
        raise RuntimeError(f"An editor already has place {place_id} open; use it or close it with close_cloud_place "
                           "first")

    launch = (f"open -n -a {shlex.quote(STUDIO_APP)} --args --task EditPlace --placeId {place_id} "
              f"--universeId {universe_id}")

    return launch_editor(launch, None, None, PlaceIds(place_id=place_id, universe_id=universe_id),
                         out_dir / f"launch-failure-place-{place_id}.png",
                         lambda checked: close_cloud_editors_on_runner(place_id, checked), config, lock_receipt,
                         registration_wait)
