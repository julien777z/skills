# Spoken Replies

## Voice service

- The voice is a text-to-speech service with an OpenAI-compatible speech endpoint, read from
  `VOICE_REPLY_SPEECH_URL` (default `http://localhost:8880/v1/audio/speech`), with the model from
  `VOICE_REPLY_MODEL` (default `kokoro`) and the voice from `VOICE_REPLY_VOICE` (default
  `af_bella`).
- The default is a local Kokoro service, which the VoiceMode installer (`uvx voice-mode-install`)
  sets up on that port. Before its first clip, check it answers at `http://localhost:8880/health`
  and start it with `voicemode service start kokoro` when it does not; the first clip after a start
  takes far longer while the model warms up.
- A failed clip is reported with its error, and the reply goes out as text.

## Making a reply

1. **Write the reply first.** Shape the spoken part for listening: short sentences, with code,
   paths, links and tables left to the written text.
2. **Make the clip:** run `python3 scripts/speak.py <output folder> <clip name>` from the skill's
   folder, with the spoken text on standard input. The clip name is a plain file name. The script
   prints the path of a self-contained HTML page holding an audio player with the clip embedded in
   it. The output folder is the one the skill's **Keep the file** bullet names.
3. **Show the player, then the reply's text under it**, through the route the skill's **Harness
   compatibility** section names. The clip may speak a question; the question tool asks it.
