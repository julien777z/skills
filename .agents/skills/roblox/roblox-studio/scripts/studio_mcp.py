from __future__ import annotations

import argparse
import atexit
import base64
import json
import os
import select
import shlex
import subprocess
import time
from pathlib import Path
from typing import IO, Any, Final, cast

RUNNER_SSH: Final[Path] = Path(__file__).resolve().with_name("runner_ssh.sh")
AGENT_LOCK: Final[Path] = Path.home() / ".agents/skills/agent-lock/resources/main.py"
STUDIO_APP: Final[str] = "/Applications/RobloxStudio.app"
STUDIO_MCP: Final[str] = f"{STUDIO_APP}/Contents/MacOS/StudioMCP"
GUEST_PLACES: Final[str] = "studio-places"
PROTOCOL_VERSION: Final[str] = "2024-11-05"


def runner(command: str, timeout: float = 60, data: bytes | None = None) -> bytes:
    result = subprocess.run([str(RUNNER_SSH), command], input=data, capture_output=True, timeout=timeout)

    if result.returncode != 0:
        raise RuntimeError(f"Runner command failed ({result.returncode}): {command}\n{result.stderr.decode()}")

    return result.stdout


class Session:
    """One MCP transport into the runner's Studio, used for sequential calls."""

    def __init__(self) -> None:
        self.process = subprocess.Popen([str(RUNNER_SSH), STUDIO_MCP], stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)
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
        raise RuntimeError(json.dumps(response)[:4000])

    return response["result"]["content"]


def text(content: list[dict[str, Any]]) -> str:
    return "\n".join(part["text"] for part in content if part.get("type") == "text")


def studios() -> list[dict[str, Any]]:
    return json.loads(text(tool("list_roblox_studios"))).get("studios", [])


class Studio:
    """One verified editor in the runner, addressed by its MCP studio ID."""

    def __init__(self, studio_id: str) -> None:
        self.studio_id = studio_id

    def tool(self, name: str, timeout: float = 55, **arguments: Any) -> list[dict[str, Any]]:
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

        # VirtualInput takes the full device coordinate space, safe insets included, where instance-path clicks
        # miss under device emulation.
        return self.execute(f'''local names = string.split({json.dumps(path, ensure_ascii=False)}, ".")
local button = game
if names[1] == "LocalPlayer" then button = game.Players.LocalPlayer; table.remove(names, 1)
elseif names[1] == "game" then table.remove(names, 1) end
for _, name in names do button = assert(button:FindFirstChild(name), "Missing button path") end
assert(button:IsA("GuiButton"), "Expected a button")
local center = button.AbsolutePosition + button.AbsoluteSize / 2
local ancestor = button
while ancestor do
	if ancestor:IsA("GuiObject") then
		assert(ancestor.Visible, "Button is inside hidden UI")
		if ancestor.ClipsDescendants then
			local low, high = ancestor.AbsolutePosition, ancestor.AbsolutePosition + ancestor.AbsoluteSize
			assert(center.X >= low.X and center.Y >= low.Y and center.X <= high.X and center.Y <= high.Y,
				"Scroll the button into view before clicking")
		end
	elseif ancestor:IsA("ScreenGui") then assert(ancestor.Enabled, "Button screen is disabled") end
	ancestor = ancestor.Parent
end
local point = center - game.GuiService:GetInsetArea(Enum.ScreenInsets.None).Min
local input = game.UserInputService:CreateVirtualInput()
for _ = 1, {count} do
	input:SendMousePosition(point)
	task.wait(0.08)
	input:SendMouseButton(point, Enum.UserInputType.MouseButton1, true, 0)
	task.wait(0.08)
	input:SendMouseButton(point, Enum.UserInputType.MouseButton1, false, 0)
end
return "Button input delivered"''', "Client")

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
    return f"{GUEST_PLACES}/{project}/{place.name}"


def own_runner_lock(lock_receipt: Path) -> None:
    result = subprocess.run(["python3", str(AGENT_LOCK), "check", "--receipt", str(lock_receipt)],
                            capture_output=True, text=True, timeout=30)
    status = json.loads(result.stdout or "{}").get("status")

    if status != "owned":
        raise RuntimeError(f"Runner lock not owned by receipt {lock_receipt}: {status}")


def close_place(project: str, place: Path, lock_receipt: Path) -> str:
    own_runner_lock(lock_receipt)

    pattern = shlex.quote(f"localPlaceFile .*{guest_place(project, place)}")
    # An editor with a place open answers SIGTERM with its unsaved-changes prompt, so it is then killed; the place file
    # is the task's own copy.
    script = f'''pids=$(pgrep -f {pattern} || true)
[ -z "$pids" ] && {{ echo closed; exit 0; }}
listed=$(echo $pids | tr ' ' ',')
kill -TERM $pids
for _ in 1 2 3 4 5; do ps -p "$listed" >/dev/null || {{ echo closed; exit 0; }}; sleep 1; done
kill -KILL $pids 2>/dev/null
for _ in 1 2 3 4 5; do ps -p "$listed" >/dev/null || {{ echo closed; exit 0; }}; sleep 1; done
echo still-open'''

    return runner(script, timeout=60).decode().strip()


def open_place(project: str, place: Path, out_dir: Path, lock_receipt: Path, wait_seconds: float = 180) -> Studio:
    own_runner_lock(lock_receipt)

    guest_path = guest_place(project, place)
    known = {studio["id"] for studio in studios()}

    runner(f"mkdir -p {shlex.quote(str(Path(guest_path).parent))} && cat > {shlex.quote(guest_path)}",
           timeout=120, data=place.read_bytes())

    runner(f'open -n -a {STUDIO_APP} --args --task EditFile --localPlaceFile "$HOME/{guest_path}"')

    deadline = time.monotonic() + wait_seconds

    while time.monotonic() < deadline:
        for studio in studios():
            if studio["id"] not in known and studio.get("name") == place.name:
                return Studio(studio["id"])

        time.sleep(2)

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"launch-failure-{place.stem}.png").write_bytes(
        runner("screencapture -x /tmp/studio-launch-failure.png && cat /tmp/studio-launch-failure.png"))

    close_place(project, place, lock_receipt)

    raise RuntimeError(f"{place.name} never registered with Studio MCP; screen saved to {out_dir}, editor closed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send one MCP request to the runner's Studio.")
    parser.add_argument("method")
    parser.add_argument("params", nargs="?", default="{}", help="JSON object, or @path to a JSON file")
    arguments = parser.parse_args()

    raw = Path(arguments.params[1:]).read_text() if arguments.params.startswith("@") else arguments.params

    print(json.dumps(call(arguments.method, json.loads(raw)), indent=2))
