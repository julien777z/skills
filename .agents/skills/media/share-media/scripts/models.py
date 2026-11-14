from typing import TypedDict


class SpeechRequest(TypedDict):
    """The request body an OpenAI-compatible speech endpoint takes."""

    model: str
    voice: str
    response_format: str
    input: str
