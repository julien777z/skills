from collections.abc import Mapping, Sequence
from enum import Enum
from typing import Literal, NotRequired, TypedDict

type JsonValue = str | int | float | bool | None | Sequence[JsonValue] | Mapping[str, JsonValue]
type ToolArguments = Mapping[str, JsonValue]


class StudioCall(Enum):
    """A kind of runner or Studio MCP call."""

    INITIALIZE = "initialize"
    TOOL = "tool"
    COPY = "copy"
    LAUNCH = "launch"
    CAPTURE = "capture"
    CLOSE = "close"
    REMOVAL = "removal"


class LockOwnership(TypedDict):
    """The ownership record an agent-lock check reports."""

    key: str


class AgentLockCheckReport(TypedDict):
    """An agent-lock check report."""

    status: str
    ownership: LockOwnership
    remaining_seconds: float


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
