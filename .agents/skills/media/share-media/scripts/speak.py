from base64 import b64encode
from json import dumps
from os import environ
from pathlib import Path
from sys import argv, exit, stdin
from typing import Final, TypedDict
from urllib.request import Request, urlopen

DEFAULT_SPEECH_URL: Final = "http://localhost:8880/v1/audio/speech"
DEFAULT_VOICE: Final = "af_bella"
SPEECH_MODEL: Final = "kokoro"
SPEECH_TIMEOUT_SECONDS: Final = 300


class SpeechRequest(TypedDict):
    model: str
    voice: str
    response_format: str
    input: str


def synthesize_speech(text: str) -> bytes:
    """Return MP3 audio of the text from the configured OpenAI-compatible speech endpoint."""

    speech_url = environ.get("VOICE_REPLY_SPEECH_URL", DEFAULT_SPEECH_URL)
    voice = environ.get("VOICE_REPLY_VOICE", DEFAULT_VOICE)

    speech_request = SpeechRequest(
        model=SPEECH_MODEL, voice=voice, response_format="mp3", input=text
    )

    request = Request(
        speech_url,
        data=dumps(speech_request).encode(),
        headers={"Content-Type": "application/json"},
    )

    with urlopen(request, timeout=SPEECH_TIMEOUT_SECONDS) as response:
        return response.read()


def build_player_page(audio: bytes) -> str:
    """Return a self-contained HTML page whose audio player carries the clip in the page."""

    encoded_audio = b64encode(audio).decode()

    return (
        '<!doctype html><html><head><meta charset="utf-8">'
        "<style>body{margin:0}audio{width:100%}</style></head><body>"
        f'<audio controls preload="auto" src="data:audio/mpeg;base64,{encoded_audio}"></audio>'
        "</body></html>"
    )


def main() -> None:
    """Speak the text on standard input into `<output folder>/<clip name>.html` and print its path."""

    output_folder = Path(argv[1])
    clip_name = argv[2]
    text = stdin.read().strip()

    if Path(clip_name).name != clip_name or clip_name in ("", ".", ".."):
        exit("The clip name must be a plain file name.")

    if not text:
        exit("No text to speak was given on standard input.")

    audio = synthesize_speech(text)

    output_folder.mkdir(parents=True, exist_ok=True)

    page_path = output_folder / f"{clip_name}.html"

    page_path.write_text(build_player_page(audio))

    print(page_path)


if __name__ == "__main__":
    main()
