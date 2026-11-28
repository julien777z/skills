from typing import TypedDict


class HookInput(TypedDict):
    """The hook payload fields the guidance-change check reads."""

    session: str | None
    event: str | None
    transcript_path: str | None


class SessionState(TypedDict):
    """The install a session last saw, and the transcript whose lifetime bounds the record."""

    commit: str
    transcript_path: str | None
