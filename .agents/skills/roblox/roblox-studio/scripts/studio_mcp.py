from __future__ import annotations

import atexit
import base64
import functools
import json
import os
import re
import select
import shlex
import subprocess
import sys
import tempfile
import time
from collections.abc import Mapping, Sequence
from datetime import timedelta
from enum import Enum
from pathlib import Path
from typing import IO, Final, NotRequired, TypedDict, cast

type JsonValue = str | int | float | bool | None | Sequence[JsonValue] | Mapping[str, JsonValue]
type ToolArguments = Mapping[str, JsonValue]


class StudioCall(Enum):
    """A runner or Studio MCP call whose timeout counts against the lease."""

    INITIALIZE = "initialize"
    TOOL = "tool"
    COPY = "copy"
    LAUNCH = "launch"
    CAPTURE = "capture"
    CLOSE = "close"
    REMOVAL = "removal"


RUNNER_SSH: Final[Path] = Path(__file__).resolve().with_name("runner_ssh.sh")
VIRTUAL_INPUT: Final[Path] = Path(__file__).resolve().with_name("virtual_input.luau")
# Installed skills sit side by side; the unresolved path keeps the install root rather than the source tree.
AGENT_LOCK: Final[Path] = Path(__file__).absolute().parents[2] / "agent-lock" / "resources" / "main.py"
STUDIO_APP: Final[str] = "/Applications/RobloxStudio.app"
STUDIO_MCP: Final[str] = f"{STUDIO_APP}/Contents/MacOS/StudioMCP"
GUEST_PLACES: Final[str] = "studio-places"
PROTOCOL_VERSION: Final[str] = "2024-11-05"
CALL_TIMEOUTS: Final[dict[StudioCall, timedelta]] = {
    StudioCall.INITIALIZE: timedelta(seconds=55),
    StudioCall.TOOL: timedelta(seconds=55),
    StudioCall.COPY: timedelta(seconds=120),
    StudioCall.LAUNCH: timedelta(seconds=60),
    StudioCall.CAPTURE: timedelta(seconds=60),
    StudioCall.CLOSE: timedelta(seconds=60),
    StudioCall.REMOVAL: timedelta(seconds=30),
}
LOCK_CHECK_TIMEOUT: Final[timedelta] = timedelta(seconds=30)
SESSION_EXIT_TIMEOUT: Final[timedelta] = timedelta(seconds=5)
REGISTRATION_POLL: Final[timedelta] = timedelta(seconds=2)
DEFAULT_REGISTRATION_WAIT: Final[timedelta] = timedelta(seconds=180)
GUEST_NAME: Final[re.Pattern[str]] = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
EXTENDED_REGEX_SPECIAL: Final[re.Pattern[str]] = re.compile(r"([.^$*+?()\[\]{}|\\])")
LUAU_STRING_ESCAPE: Final[re.Pattern[str]] = re.compile(r'[\\"\x00-\x1f\x7f]')


class LockOwnership(TypedDict):
    """The ownership record an agent-lock check reports."""

    key: str


class AgentLockCheckReport(TypedDict):
    """The report agent-lock prints for a receipt that still owns its lock."""

    status: str
    ownership: LockOwnership
    remaining_seconds: float


class McpContentPart(TypedDict):
    """One part of an MCP tool result's content."""

    type: str
    text: NotRequired[str]
    data: NotRequired[str]
    mimeType: NotRequired[str]


class ToolCallResult(TypedDict):
    """The result of an MCP tools/call request."""

    content: list[McpContentPart]
    isError: NotRequired[bool]


class JsonRpcError(TypedDict):
    """The error member of a JSON-RPC response."""

    code: int
    message: str


class JsonRpcMessage(TypedDict):
    """A JSON-RPC request, notification or response."""

    jsonrpc: str
    id: NotRequired[int]
    method: NotRequired[str]
    params: NotRequired[Mapping[str, JsonValue]]
    result: NotRequired[ToolCallResult]
    error: NotRequired[JsonRpcError]


class StudioEntry(TypedDict):
    """One editor list_roblox_studios reports."""

    id: str
    name: NotRequired[str]


class StudioButton(TypedDict):
    """A TextButton on a player's screen, as Studio.buttons reports it."""

    path: str
    text: str
    active: bool
    x: float
    y: float
    width: float
    height: float


@functools.cache
def runner_config() -> dict[str, str]:
    """Return the game's runner configuration, resolved once so every later call reaches the same VM."""

    result = subprocess.run([str(RUNNER_SSH), "--describe"], capture_output=True, text=True,
                            timeout=LOCK_CHECK_TIMEOUT.total_seconds())

    if result.returncode != 0:
        raise RuntimeError(f"No runner VM resolved for this game:\n{result.stderr}")

    return dict(assignment.split("=", 1) for assignment in shlex.split(result.stdout))


def runner_environment() -> dict[str, str]:
    """Return the environment that pins runner_ssh.sh to the resolved game."""

    return {**os.environ, "ROBLOX_STUDIO_GAME": runner_config()["ROBLOX_STUDIO_GAME"]}


def runner_lock_key() -> str:
    """Return the runner lock key, which is the game's VM name."""

    return runner_config()["ROBLOX_STUDIO_VM"]


def assert_runner_lease_covers(lock_receipt: Path, needed: timedelta) -> None:
    """Assert that the receipt owns the game's runner lock for at least the needed time."""

    lock_key = runner_lock_key()

    result = subprocess.run([sys.executable, str(AGENT_LOCK), "check", "--receipt", str(lock_receipt)],
                            capture_output=True, text=True, timeout=LOCK_CHECK_TIMEOUT.total_seconds())

    if result.returncode != 0:
        raise RuntimeError(f"Receipt {lock_receipt} does not own a lock:\n{result.stderr}")

    report: AgentLockCheckReport = json.loads(result.stdout)

    if report["ownership"]["key"] != lock_key:
        raise RuntimeError(f"Receipt {lock_receipt} owns {report['ownership']['key']}, not {lock_key}")

    remaining = timedelta(seconds=report["remaining_seconds"])

    if remaining < needed:
        raise RuntimeError(f"The {lock_key} lease has {remaining.total_seconds():.0f} s left; this call can "
                           f"take up to {needed.total_seconds():.0f} s")


def run_in_runner(command: str, lock_receipt: Path, timeout: timedelta, data: bytes | None = None) -> bytes:
    """Run a shell command in the runner guest and return its output."""

    assert_runner_lease_covers(lock_receipt, timeout)

    # The guest's login shell may be zsh, which splits words differently, so commands always run under sh.
    result = subprocess.run([str(RUNNER_SSH), f"/bin/sh -c {shlex.quote(command)}"], input=data,
                            capture_output=True, timeout=timeout.total_seconds(), env=runner_environment())

    if result.returncode != 0:
        raise RuntimeError(f"Runner command failed ({result.returncode}): {command}\n{result.stderr.decode()}")

    return result.stdout


class StudioMcpSession:
    """One MCP transport into the runner's Studio, used for sequential calls."""

    def __init__(self) -> None:
        """Start the runner's Studio MCP server and initialize the session."""

        self.server_errors = tempfile.TemporaryFile()
        self.process = subprocess.Popen([str(RUNNER_SSH), STUDIO_MCP], stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=self.server_errors, bufsize=0,
                                        env=runner_environment())

        self.stdin = cast(IO[bytes], self.process.stdin)
        self.stdout = cast(IO[bytes], self.process.stdout)
        self.identity = 0
        self.received = b""
        initialized = False

        try:
            self.request("initialize", {"protocolVersion": PROTOCOL_VERSION, "capabilities": {},
                                        "clientInfo": {"name": "roblox-studio-skill", "version": "1.0"}},
                         CALL_TIMEOUTS[StudioCall.INITIALIZE])

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
        """Send a request and return its response."""

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
        """Stop the server and close its streams."""

        if self.process.poll() is None:
            self.process.terminate()

            try:
                self.process.wait(timeout=SESSION_EXIT_TIMEOUT.total_seconds())
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()

        for stream in (self.stdin, self.stdout, self.server_errors):
            stream.close()


class StudioMcpConnection:
    """A Studio MCP session opened on first use and reopened after a failed call."""

    def __init__(self) -> None:
        """Hold no session until the first call."""

        self.session: StudioMcpSession | None = None

        atexit.register(self.close)

    def request(self, method: str, params: Mapping[str, JsonValue], timeout: timedelta) -> JsonRpcMessage:
        """Send a request over the session, closing the session when the call fails."""

        if self.session is None:
            self.session = StudioMcpSession()

        answered = False

        try:
            response = self.session.request(method, params, timeout)
            answered = True
        finally:
            if not answered:
                self.close()

        return response

    def close(self) -> None:
        """Close the session if one is open."""

        if self.session is not None:
            self.session.close()
            self.session = None


def call_studio_tool(connection: StudioMcpConnection, name: str, arguments: ToolArguments, lock_receipt: Path,
                     timeout: timedelta = CALL_TIMEOUTS[StudioCall.TOOL]) -> list[McpContentPart]:
    """Call a Studio MCP tool and return its content."""

    opening = CALL_TIMEOUTS[StudioCall.INITIALIZE] if connection.session is None else timedelta()

    assert_runner_lease_covers(lock_receipt, timeout + opening)

    response = connection.request("tools/call", {"name": name, "arguments": arguments}, timeout)

    if "error" in response or "result" not in response or response["result"].get("isError"):
        raise RuntimeError(json.dumps(response))

    return response["result"]["content"]


def mcp_content_text(content: list[McpContentPart]) -> str:
    """Join the text parts of an MCP tool result."""

    return "\n".join(part["text"] for part in content if part["type"] == "text" and "text" in part)


def studios(connection: StudioMcpConnection, lock_receipt: Path) -> list[StudioEntry]:
    """List the editors the runner's Studio MCP knows."""

    listing = mcp_content_text(call_studio_tool(connection, "list_roblox_studios", {}, lock_receipt))

    return json.loads(listing).get("studios", [])


def luau_string_literal(value: str) -> str:
    """Quote a string as a Luau string literal."""

    escaped = LUAU_STRING_ESCAPE.sub(lambda match: f"\\x{ord(match.group()):02x}", value)

    return f'"{escaped}"'


class Studio:
    """One verified editor in the runner, addressed by its MCP studio ID."""

    def __init__(self, studio_id: str, lock_receipt: Path) -> None:
        """Address the editor through its own Studio MCP connection."""

        self.studio_id = studio_id
        self.lock_receipt = lock_receipt
        self.connection = StudioMcpConnection()

    def tool(self, name: str, arguments: ToolArguments,
             timeout: timedelta = CALL_TIMEOUTS[StudioCall.TOOL]) -> list[McpContentPart]:
        """Call a Studio MCP tool on this editor."""

        return call_studio_tool(self.connection, name, {**arguments, "studio_id": self.studio_id},
                                self.lock_receipt, timeout)

    def execute(self, code: str, data_model: str = "Client",
                timeout: timedelta = CALL_TIMEOUTS[StudioCall.TOOL]) -> str:
        """Run Luau in one of the editor's data models and return its output."""

        return mcp_content_text(self.tool("execute_luau", {"datamodel_type": data_model, "code": code}, timeout))

    def console(self) -> str:
        """Return the editor's console output."""

        return mcp_content_text(self.tool("get_console_output", {}))

    def capture(self, name: str, out_dir: Path) -> list[Path]:
        """Save the editor's screenshots under out_dir."""

        out_dir.mkdir(parents=True, exist_ok=True)

        paths: list[Path] = []

        for index, part in enumerate(self.tool("screen_capture", {"capture_id": name})):
            if part["type"] == "image" and "data" in part:
                path = out_dir / f"{name}-{index}.png"
                path.write_bytes(base64.b64decode(part["data"]))
                paths.append(path)

        if not paths:
            raise RuntimeError("Studio returned no screenshot")

        return paths

    def keys(self, actions: Sequence[Mapping[str, JsonValue]]) -> list[McpContentPart]:
        """Send keyboard actions to the editor's client."""

        return self.tool("user_keyboard_input", {"datamodel_type": "Client", "actions": actions})

    def click(self, path: str, count: int = 1) -> str:
        """Click a button by its instance path through the VirtualInput helper."""

        if not 1 <= count <= 10:
            raise ValueError("Use one to ten button clicks")

        lookup = f'''local names = string.split({luau_string_literal(path)}, ".")
local button = game
if names[1] == "LocalPlayer" then button = game.Players.LocalPlayer; table.remove(names, 1)
elseif names[1] == "game" then table.remove(names, 1) end
for _, name in names do button = assert(button:FindFirstChild(name), "Missing button path") end
local input = Input.new()
for _ = 1, {count} do input:click(button) end
input:release()
return "Button input delivered"'''

        return self.execute(f"local Input = (function()\n{VIRTUAL_INPUT.read_text()}\nend)()\n{lookup}", "Client")

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


def close_place(project: str, place: Path, lock_receipt: Path) -> None:
    """End the editor that has a project's place copy open and delete the copy."""

    assert_runner_lease_covers(lock_receipt, CALL_TIMEOUTS[StudioCall.CLOSE] + CALL_TIMEOUTS[StudioCall.REMOVAL])

    guest_path = guest_place(project, place)
    pattern = shlex.quote(f"localPlaceFile ([^ ]*/)?{extended_regex_literal(guest_path)}( |$)")
    # An editor with a place open answers SIGTERM with its unsaved-changes prompt, so it is then killed.
    script = f'''target="$HOME"/{shlex.quote(guest_path)}
pids=
for pid in $(pgrep -f {pattern}); do
  process_command=$(ps -o command= -p "$pid") || continue
  case "$process_command " in *" --localPlaceFile $target "*) pids="$pids $pid";; esac
done
[ -z "$pids" ] && {{ echo closed; exit 0; }}
listed=$(echo $pids | tr ' ' ',')
kill -TERM $pids
for _ in 1 2 3 4 5; do ps -p "$listed" >/dev/null || {{ echo closed; exit 0; }}; sleep 1; done
kill -KILL $pids 2>/dev/null
for _ in 1 2 3 4 5; do ps -p "$listed" >/dev/null || {{ echo closed; exit 0; }}; sleep 1; done
echo still-open'''

    # Studio leaves a lock file beside a place it opened.
    files = f"{shlex.quote(guest_path)} {shlex.quote(f'{guest_path}.lock')}"
    folder = shlex.quote(str(Path(guest_path).parent))
    removal = f'cd "$HOME" && rm -f {files}; rmdir {folder} 2>/dev/null; true'

    state = run_in_runner(script, lock_receipt, CALL_TIMEOUTS[StudioCall.CLOSE]).decode().strip()

    if state != "closed":
        raise RuntimeError(f"The editor for {guest_path} is still open, so its copy stays in the guest")

    run_in_runner(removal, lock_receipt, CALL_TIMEOUTS[StudioCall.REMOVAL])


def open_place(project: str, place: Path, out_dir: Path, lock_receipt: Path,
               registration_wait: timedelta = DEFAULT_REGISTRATION_WAIT) -> Studio:
    """Copy a built place into the runner, open it in an editor, and return that editor."""

    guest_path = guest_place(project, place)
    bound = (CALL_TIMEOUTS[StudioCall.INITIALIZE] + CALL_TIMEOUTS[StudioCall.TOOL] + CALL_TIMEOUTS[StudioCall.COPY]
             + CALL_TIMEOUTS[StudioCall.LAUNCH] + registration_wait + CALL_TIMEOUTS[StudioCall.TOOL]
             + REGISTRATION_POLL + CALL_TIMEOUTS[StudioCall.CAPTURE] + CALL_TIMEOUTS[StudioCall.CLOSE]
             + CALL_TIMEOUTS[StudioCall.REMOVAL])

    assert_runner_lease_covers(lock_receipt, bound)

    connection = StudioMcpConnection()
    known = {studio["id"] for studio in studios(connection, lock_receipt)}
    opened = False

    try:
        run_in_runner(f'cd "$HOME" && mkdir -p {shlex.quote(str(Path(guest_path).parent))} && '
                      f'cat > {shlex.quote(guest_path)}', lock_receipt, CALL_TIMEOUTS[StudioCall.COPY],
                      data=place.read_bytes())

        run_in_runner(f'cd "$HOME" && open -n -a {shlex.quote(STUDIO_APP)} --args --task EditFile --localPlaceFile '
                      f'"$HOME"/{shlex.quote(guest_path)}', lock_receipt, CALL_TIMEOUTS[StudioCall.LAUNCH])

        deadline = time.monotonic() + registration_wait.total_seconds()

        while time.monotonic() < deadline:
            registered = next((studio for studio in studios(connection, lock_receipt)
                               if studio["id"] not in known and studio.get("name") == place.name), None)

            if registered is not None:
                opened = True

                return Studio(registered["id"], lock_receipt)

            time.sleep(REGISTRATION_POLL.total_seconds())

        screen = run_in_runner('f=$(mktemp -t studio-launch) && screencapture -x -t png "$f" && cat "$f"; '
                               'status=$?; rm -f "$f"; exit $status', lock_receipt, CALL_TIMEOUTS[StudioCall.CAPTURE])

        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"launch-failure-{place.stem}.png").write_bytes(screen)

        raise RuntimeError(f"{place.name} never registered with Studio MCP; screen saved to {out_dir}")
    finally:
        connection.close()

        if not opened:
            close_place(project, place, lock_receipt)
