from typing import TypedDict


class SpeechRequest(TypedDict):
    model: str
    voice: str
    response_format: str
    input: str
