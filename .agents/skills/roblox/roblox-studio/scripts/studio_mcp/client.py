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
from pathlib import Path
from typing import IO, Final, cast

from studio_mcp.models import (AgentLockCheckReport, JsonRpcMessage, JsonValue, McpContent, StudioButton, StudioCall,
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
    """Run a shell command in the runner guest."""

    assert_runner_lease_covers(lock_receipt, timeout)

    # The guest's login shell may be zsh, which splits words differently, so commands always run under sh.
    result = subprocess.run([str(RUNNER_SSH), f"/bin/sh -c {shlex.quote(command)}"], input=data,
                            capture_output=True, timeout=timeout.total_seconds(), env=runner_environment())

    if result.returncode != 0:
        raise RuntimeError(f"Runner command failed ({result.returncode}): {command}\n{result.stderr.decode()}")

    return result.stdout


class StudioMcpSession:
    """An MCP transport into the runner's Studio."""

    def __init__(self) -> None:
        """Open an initialized session."""

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
                self.process.wait(timeout=SESSION_EXIT_TIMEOUT.total_seconds())
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

    def request(self, method: str, params: Mapping[str, JsonValue], timeout: timedelta) -> JsonRpcMessage:
        """Send a request over the session."""

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
        """Close the open session."""

        if self.session is not None:
            self.session.close()
            self.session = None


def call_studio_tool(connection: StudioMcpConnection, name: str, arguments: ToolArguments, lock_receipt: Path,
                     timeout: timedelta = CALL_TIMEOUTS[StudioCall.TOOL]) -> list[McpContent]:
    """Call a Studio MCP tool."""

    opening = CALL_TIMEOUTS[StudioCall.INITIALIZE] if connection.session is None else timedelta()

    assert_runner_lease_covers(lock_receipt, timeout + opening)

    response = connection.request("tools/call", {"name": name, "arguments": arguments}, timeout)

    if "error" in response or "result" not in response or response["result"].get("isError"):
        raise RuntimeError(json.dumps(response))

    return response["result"]["content"]


def mcp_content_text(content: list[McpContent]) -> str:
    """Join the text parts of an MCP tool result."""

    return "\n".join(part["text"] for part in content if part["type"] == "text")


def studios(connection: StudioMcpConnection, lock_receipt: Path) -> list[StudioEntry]:
    """List the editors the runner's Studio MCP knows."""

    listing = mcp_content_text(call_studio_tool(connection, "list_roblox_studios", {}, lock_receipt))

    return json.loads(listing).get("studios", [])


def luau_string_literal(value: str) -> str:
    """Quote a string as a Luau string literal."""

    escaped = LUAU_STRING_ESCAPE.sub(lambda match: f"\\x{ord(match.group()):02x}", value)

    return f'"{escaped}"'


class Studio:
    """An editor in the runner."""

    def __init__(self, studio_id: str, lock_receipt: Path) -> None:
        """Address an editor by its MCP studio ID."""

        self.studio_id = studio_id
        self.lock_receipt = lock_receipt
        self.connection = StudioMcpConnection()

    def tool(self, name: str, arguments: ToolArguments,
             timeout: timedelta = CALL_TIMEOUTS[StudioCall.TOOL]) -> list[McpContent]:
        """Call a Studio MCP tool on this editor."""

        return call_studio_tool(self.connection, name, {**arguments, "studio_id": self.studio_id},
                                self.lock_receipt, timeout)

    def execute(self, code: str, data_model: str = "Client",
                timeout: timedelta = CALL_TIMEOUTS[StudioCall.TOOL]) -> str:
        """Run Luau in one of the editor's data models."""

        return mcp_content_text(self.tool("execute_luau", {"datamodel_type": data_model, "code": code}, timeout))

    def console(self) -> str:
        """Return the editor's console output."""

        return mcp_content_text(self.tool("get_console_output", {}))

    def capture(self, name: str, out_dir: Path) -> list[Path]:
        """Save the editor's screenshots under out_dir."""

        out_dir.mkdir(parents=True, exist_ok=True)

        paths: list[Path] = []

        for index, part in enumerate(self.tool("screen_capture", {"capture_id": name})):
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

    def click(self, path: str, count: int = 1) -> str:
        """Click a button by its instance path."""

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
    """Close a project's place copy in the runner."""

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
    """Open a built place in a runner editor."""

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
                               'capture_status=$?; rm -f "$f"; exit $capture_status', lock_receipt, CALL_TIMEOUTS[StudioCall.CAPTURE])

        out_dir.mkdir(parents=True, exist_ok=True)

        (out_dir / f"launch-failure-{place.stem}.png").write_bytes(screen)

        raise RuntimeError(f"{place.name} never registered with Studio MCP; screen saved to {out_dir}")
    finally:
        connection.close()

        if not opened:
            close_place(project, place, lock_receipt)
