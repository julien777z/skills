"""Turn reply text into a spoken clip embedded in a self-contained HTML audio player.

Usage: echo "<text to speak>" | python3 speak.py <output folder> <clip name>
Prints the path of the HTML page to show in the chat.
"""

import base64
import json
import os
import sys
import urllib.request
from pathlib import Path

DEFAULT_SPEECH_URL = "http://localhost:8880/v1/audio/speech"
DEFAULT_VOICE = "af_sky"
SPEECH_TIMEOUT_SECONDS = 300


def synthesize_speech(text: str) -> bytes:
    speech_url = os.environ.get("VOICE_REPLY_SPEECH_URL", DEFAULT_SPEECH_URL)
    voice = os.environ.get("VOICE_REPLY_VOICE", DEFAULT_VOICE)

    payload = json.dumps(
        {"model": "kokoro", "voice": voice, "response_format": "mp3", "input": text}
    ).encode()

    request = urllib.request.Request(
        speech_url, data=payload, headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(request, timeout=SPEECH_TIMEOUT_SECONDS) as response:
        return response.read()


def build_player_page(audio: bytes) -> str:
    encoded_audio = base64.b64encode(audio).decode()

    return (
        '<!doctype html><html><head><meta charset="utf-8">'
        "<style>body{margin:0}audio{width:100%}</style></head><body>"
        f'<audio controls preload="auto" src="data:audio/mpeg;base64,{encoded_audio}"></audio>'
        "</body></html>"
    )


def main() -> None:
    output_folder = Path(sys.argv[1])
    clip_name = sys.argv[2]
    text = sys.stdin.read().strip()

    if not text:
        sys.exit("No text to speak was given on standard input.")

    audio = synthesize_speech(text)

    output_folder.mkdir(parents=True, exist_ok=True)

    page_path = output_folder / f"{clip_name}.html"
    page_path.write_text(build_player_page(audio))

    print(page_path)


if __name__ == "__main__":
    main()
