from collections.abc import Mapping, Sequence
from datetime import timedelta
from enum import StrEnum, auto
from typing import Literal, NotRequired, TypedDict

type JsonValue = str | int | float | bool | None | Sequence[JsonValue] | Mapping[str, JsonValue]
type ToolArguments = Mapping[str, JsonValue]
type Position = tuple[float, float, float]


class RunnerOperation(StrEnum):
    """An operation in the runner that has its own time limit."""

    INITIALIZE = auto()
    TOOL_CALL = auto()
    COPY = auto()
    LAUNCH = auto()
    CAPTURE = auto()
    EDIT_PROBE = auto()
    PROCESS_LIST = auto()
    STOP = auto()
    REMOVAL = auto()
    LOCK_CHECK = auto()
    DESCRIBE = auto()
    SESSION_EXIT = auto()


class RunnerConfig(TypedDict):
    """The game's runner configuration, as `runner_ssh.sh --describe` prints it."""

    ROBLOX_STUDIO_GAME: str
    ROBLOX_STUDIO_TART: str
    ROBLOX_STUDIO_VM: str
    ROBLOX_STUDIO_SSH_USER: str
    ROBLOX_STUDIO_SSH_KEY: str
    ROBLOX_STUDIO_KNOWN_HOSTS: str


class LockOwnership(TypedDict):
    """The ownership record an agent-lock check reports."""

    key: str


class AgentLockCheckReport(TypedDict):
    """An agent-lock check report."""

    status: str
    ownership: LockOwnership
    remaining_seconds: float


class AgentLockAcquireReport(TypedDict):
    """An agent-lock acquire report."""

    status: str
    ownership: LockOwnership
    remaining_seconds: NotRequired[float]
    expired_owner: NotRequired[str | None]


class RunnerLease(TypedDict):
    """The game's runner and how long a receipt's lease on its lock has left."""

    config: RunnerConfig
    remaining: timedelta


class McpTextContent(TypedDict):
    """A text part of an MCP tool result."""

    type: Literal["text"]
    text: str


class McpImageContent(TypedDict):
    """An image part of an MCP tool result."""

    type: Literal["image"]
    data: str
    mimeType: str


type McpContent = McpTextContent | McpImageContent


class ToolCallResult(TypedDict):
    """The result of an MCP tools/call request."""

    content: list[McpContent]
    isError: NotRequired[bool]


class JsonRpcError(TypedDict):
    """The error member of a JSON-RPC response."""

    code: int
    message: str


class JsonRpcMessage(TypedDict):
    """A JSON-RPC message."""

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
    """A TextButton on a player's screen."""

    path: str
    text: str
    active: bool
    x: float
    y: float
    width: float
    height: float


class PlaceIds(TypedDict):
    """The place and universe IDs an editor's Edit data model reports."""

    place_id: int
    universe_id: int


class CameraView(TypedDict):
    """A camera position and the point it looks at."""

    position: Position
    look_at: Position
