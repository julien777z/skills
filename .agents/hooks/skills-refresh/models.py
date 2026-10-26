from enum import StrEnum
from typing import NotRequired, TypedDict


class InstallationMode(StrEnum):
    """Name the configuration command modes."""

    APPLY = "apply"
    CHECK = "check"
    PREFLIGHT = "preflight"


class StartupContext(TypedDict):
    """Provider startup context."""

    hookEventName: str
    additionalContext: str
    reloadSkills: NotRequired[bool]


class StartupResult(TypedDict):
    """Provider startup response."""

    hookSpecificOutput: StartupContext


class StartupEvent(TypedDict):
    """Native lifecycle fields used by the shared startup entrypoint."""

    hook_event_name: str
    source: NotRequired[str]


class CursorStartupResult(TypedDict):
    """Cursor's native startup context response."""

    additional_context: str


class HookCommand(TypedDict):
    """An installed provider command derived from the shared registration."""

    type: str
    command: str
    timeout: int
    statusMessage: NotRequired[str]


class HookGroup(TypedDict):
    """The owned native lifecycle registration."""

    matcher: str
    hooks: list[HookCommand]


class RefreshOutcome(StrEnum):
    """Local installation check outcome."""

    CURRENT = "current"
    BUSY = "busy"
    RECONCILE = "reconcile"
    REPAIRED = "repaired"
    FAILED = "failed"


class CodexClientInfo(TypedDict):
    name: str
    version: str


class CodexTrustStatus(StrEnum):
    """Native hook trust states exposed by the Codex app server."""

    MANAGED = "managed"
    UNTRUSTED = "untrusted"
    TRUSTED = "trusted"
    MODIFIED = "modified"


class CodexInitialize(TypedDict):
    clientInfo: CodexClientInfo


class CodexHooksQuery(TypedDict):
    cwds: list[str]


class CodexHookTrust(TypedDict):
    trusted_hash: str


class CodexTrustEdit(TypedDict):
    keyPath: str
    value: dict[str, CodexHookTrust]
    mergeStrategy: str


class CodexTrustWrite(TypedDict):
    edits: list[CodexTrustEdit]
    reloadUserConfig: bool


class CodexRequest(TypedDict):
    id: int
    method: str
    params: CodexInitialize | CodexHooksQuery | CodexTrustWrite
