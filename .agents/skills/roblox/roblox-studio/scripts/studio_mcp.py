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
import time
from pathlib import Path
from typing import IO, Any, Final, cast

RUNNER_SSH: Final[Path] = Path(__file__).resolve().with_name("runner_ssh.sh")
VIRTUAL_INPUT: Final[Path] = Path(__file__).resolve().with_name("virtual_input.luau")
# Installed skills sit side by side; the unresolved path keeps the install root rather than the source tree.
AGENT_LOCK: Final[Path] = Path(__file__).absolute().parents[2] / "agent-lock" / "resources" / "main.py"
STUDIO_APP: Final[str] = "/Applications/RobloxStudio.app"
STUDIO_MCP: Final[str] = f"{STUDIO_APP}/Contents/MacOS/StudioMCP"
GUEST_PLACES: Final[str] = "studio-places"
PROTOCOL_VERSION: Final[str] = "2024-11-05"
GUEST_NAME: Final[re.Pattern[str]] = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


@functools.cache
def runner_config() -> dict[str, str]:
    """The game's runner configuration, resolved once so every later call reaches the same VM."""
    result = subprocess.run([str(RUNNER_SSH), "--describe"], capture_output=True, text=True, timeout=30)

    if result.returncode != 0:
        raise RuntimeError(f"No runner VM resolved for this game:\n{result.stderr}")

    return dict(assignment.split("=", 1) for assignment in shlex.split(result.stdout))


def runner_environment() -> dict[str, str]:
    return {**os.environ, "ROBLOX_STUDIO_GAME": runner_config()["ROBLOX_STUDIO_GAME"]}


def runner_lock_key() -> str:
    # Each game's VM is locked under the VM's own name.
    return runner_config()["ROBLOX_STUDIO_VM"]


def own_runner_lock(lock_receipt: Path) -> None:
    lock_key = runner_lock_key()

    result = subprocess.run([sys.executable, str(AGENT_LOCK), "check", "--receipt", str(lock_receipt)],
                            capture_output=True, text=True, timeout=30)

    try:
        report = json.loads(result.stdout)
    except ValueError:
        report = {}

    owned = report.get("status") == "owned" and report.get("ownership", {}).get("key") == lock_key

    if result.returncode != 0 or not owned:
        raise RuntimeError(f"Receipt {lock_receipt} does not own the {lock_key} lock:\n"
                           f"{result.stdout}{result.stderr}")


def runner(command: str, lock_receipt: Path, timeout: float = 60, data: bytes | None = None) -> bytes:
    own_runner_lock(lock_receipt)

    result = subprocess.run([str(RUNNER_SSH), command], input=data, capture_output=True, timeout=timeout,
                            env=runner_environment())

    if result.returncode != 0:
        raise RuntimeError(f"Runner command failed ({result.returncode}): {command}\n{result.stderr.decode()}")

    return result.stdout


class Session:
    """One MCP transport into the runner's Studio, used for sequential calls."""

    def __init__(self) -> None:
        self.process = subprocess.Popen([str(RUNNER_SSH), STUDIO_MCP], stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0,
                                        env=runner_environment())
        # Popen with PIPE always opens all three streams.
        self.stdin = cast(IO[bytes], self.process.stdin)
        self.stdout = cast(IO[bytes], self.process.stdout)
        self.stderr = cast(IO[bytes], self.process.stderr)
        self.identity = 0
        self.received = b""

        try:
            self.request("initialize", {"protocolVersion": PROTOCOL_VERSION, "capabilities": {},
                                        "clientInfo": {"name": "roblox-studio-skill", "version": "1.0"}})
            self.write({"jsonrpc": "2.0", "method": "notifications/initialized"})
        except Exception:
            self.close()
            raise

    def write(self, message: dict[str, Any]) -> None:
        self.stdin.write((json.dumps(message) + "\n").encode())
        self.stdin.flush()

    def request(self, method: str, params: dict[str, Any], timeout: float = 55) -> dict[str, Any]:
        self.identity += 1
        self.write({"jsonrpc": "2.0", "id": self.identity, "method": method, "params": params})

        deadline = time.monotonic() + timeout

        while time.monotonic() < deadline:
            if b"\n" not in self.received:
                if not select.select([self.stdout], [], [], max(0, deadline - time.monotonic()))[0]:
                    break

                chunk = os.read(self.stdout.fileno(), 65536)

                if not chunk:
                    raise RuntimeError(f"Studio MCP exited: {self.stderr.read().decode()}")

                self.received += chunk
                continue

            line, self.received = self.received.split(b"\n", 1)
            response = json.loads(line)

            if response.get("id") == self.identity:
                return response

        raise TimeoutError(f"Studio MCP timed out: {method}")

    def close(self) -> None:
        if self.process.poll() is None:
            self.process.terminate()

            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()

        for stream in (self.stdin, self.stdout, self.stderr):
            stream.close()


_session: Session | None = None


def close_session() -> None:
    global _session

    if _session is not None:
        _session.close()
        _session = None


atexit.register(close_session)


def call(method: str, params: dict[str, Any], timeout: float = 55) -> dict[str, Any]:
    global _session

    if _session is None:
        _session = Session()

    try:
        return _session.request(method, params, timeout)
    except Exception:
        # A transport failure may follow a completed action, so the call is never replayed.
        close_session()
        raise


def tool(name: str, timeout: float = 55, **arguments: Any) -> list[dict[str, Any]]:
    response = call("tools/call", {"name": name, "arguments": arguments}, timeout)

    if "error" in response or response.get("result", {}).get("isError"):
        raise RuntimeError(json.dumps(response))

    return response["result"]["content"]


def text(content: list[dict[str, Any]]) -> str:
    return "\n".join(part["text"] for part in content if part.get("type") == "text")


def studios() -> list[dict[str, Any]]:
    return json.loads(text(tool("list_roblox_studios"))).get("studios", [])


class Studio:
    """One verified editor in the runner, addressed by its MCP studio ID."""

    def __init__(self, studio_id: str, lock_receipt: Path) -> None:
        self.studio_id = studio_id
        self.lock_receipt = lock_receipt

    def tool(self, name: str, timeout: float = 55, **arguments: Any) -> list[dict[str, Any]]:
        # A lease can expire between calls, so ownership is checked on every one.
        own_runner_lock(self.lock_receipt)

        return tool(name, timeout, studio_id=self.studio_id, **arguments)

    def execute(self, code: str, data_model: str = "Client", timeout: float = 55) -> str:
        return text(self.tool("execute_luau", timeout, datamodel_type=data_model, code=code))

    def console(self) -> str:
        return text(self.tool("get_console_output"))

    def capture(self, name: str, out_dir: Path) -> list[Path]:
        out_dir.mkdir(parents=True, exist_ok=True)
        paths = []

        for index, part in enumerate(self.tool("screen_capture", capture_id=name)):
            if part.get("type") == "image":
                path = out_dir / f"{name}-{index}.png"
                path.write_bytes(base64.b64decode(part["data"]))
                paths.append(path)

        if not paths:
            raise RuntimeError("Studio returned no screenshot")

        return paths

    def keys(self, actions: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return self.tool("user_keyboard_input", datamodel_type="Client", actions=actions)

    def click(self, path: str, count: int = 1) -> str:
        if not 1 <= count <= 10:
            raise ValueError("Use one to ten button clicks")

        lookup = f'''local names = string.split({json.dumps(path, ensure_ascii=False)}, ".")
local button = game
if names[1] == "LocalPlayer" then button = game.Players.LocalPlayer; table.remove(names, 1)
elseif names[1] == "game" then table.remove(names, 1) end
for _, name in names do button = assert(button:FindFirstChild(name), "Missing button path") end
local input = Input.new()
for _ = 1, {count} do input:click(button) end
input:release()
return "Button input delivered"'''

        return self.execute(f"local Input = (function()\n{VIRTUAL_INPUT.read_text()}\nend)()\n{lookup}", "Client")

    def buttons(self, screen: str) -> list[dict[str, Any]]:
        return json.loads(self.execute(f'''local buttons = {{}}
for _, object in game.Players.LocalPlayer.PlayerGui[{json.dumps(screen)}]:GetDescendants() do
	if object:IsA("TextButton") then
		table.insert(buttons, {{path = object:GetFullName(), text = object.Text, active = object.Interactable,
			x = object.AbsolutePosition.X, y = object.AbsolutePosition.Y,
			width = object.AbsoluteSize.X, height = object.AbsoluteSize.Y}})
	end
end
return game.HttpService:JSONEncode(buttons)''', "Client"))


def guest_place(project: str, place: Path) -> str:
    for name in (project, place.name):
        if not GUEST_NAME.fullmatch(name):
            raise ValueError(f"Guest place names use letters, digits, '.', '_' and '-': {name!r}")

    return f"{GUEST_PLACES}/{project}/{place.name}"


def extended_regex_literal(value: str) -> str:
    return re.sub(r"([.^$*+?()\[\]{}|\\])", r"\\\1", value)


def close_place(project: str, place: Path, lock_receipt: Path) -> str:
    guest_path = guest_place(project, place)
    pattern = shlex.quote(f"localPlaceFile ([^ ]*/)?{extended_regex_literal(guest_path)}( |$)")
    # pgrep's pattern is a prefilter; each match is signaled only when its command line names exactly this copy. An
    # editor with a place open answers SIGTERM with its unsaved-changes prompt, so it is then killed; the place file is
    # the task's own copy.
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
    removal = f"rm -f {files}; rmdir {folder} 2>/dev/null; true"

    state = runner(script, lock_receipt).decode().strip()

    if state == "closed":
        runner(removal, lock_receipt, timeout=30)

    return state


def open_place(project: str, place: Path, out_dir: Path, lock_receipt: Path, wait_seconds: float = 180) -> Studio:
    guest_path = guest_place(project, place)

    own_runner_lock(lock_receipt)

    known = {studio["id"] for studio in studios()}

    try:
        runner(f"mkdir -p {shlex.quote(str(Path(guest_path).parent))} && cat > {shlex.quote(guest_path)}",
               lock_receipt, timeout=120, data=place.read_bytes())

        runner(f'cd "$HOME" && open -n -a {shlex.quote(STUDIO_APP)} --args --task EditFile --localPlaceFile '
               f'"$HOME"/{shlex.quote(guest_path)}', lock_receipt)

        deadline = time.monotonic() + wait_seconds

        while time.monotonic() < deadline:
            for studio in studios():
                if studio["id"] not in known and studio.get("name") == place.name:
                    return Studio(studio["id"], lock_receipt)

            time.sleep(2)

        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"launch-failure-{place.stem}.png").write_bytes(
            runner('f=$(mktemp -t studio-launch) && screencapture -x -t png "$f" && cat "$f"; status=$?; rm -f "$f"; '
                   'exit $status', lock_receipt))

        raise RuntimeError(f"{place.name} never registered with Studio MCP; screen saved to {out_dir}")
    except BaseException as error:
        try:
            error.add_note(f"close_place after the failed launch: {close_place(project, place, lock_receipt)}")
        except BaseException as cleanup_error:
            error.add_note(f"close_place after the failed launch raised {cleanup_error!r}")

        raise
