# Spoken Replies

The `share-media` skill's procedure for sending a reply as speech: the voice service it uses, how a
clip is made, and what the spoken part says.

## Voice service

- The voice is a text-to-speech service with an OpenAI-compatible speech endpoint, read from
  `VOICE_REPLY_SPEECH_URL` (default `http://localhost:8880/v1/audio/speech`), with the voice from
  `VOICE_REPLY_VOICE` (default `af_bella`).
- The default is a local Kokoro service, which the VoiceMode installer (`uvx voice-mode-install`)
  sets up on that port. Before its first clip, check it answers at `http://localhost:8880/health`
  and start it with `voicemode service start kokoro` when it does not; the first clip after a start
  takes far longer while the model warms up.
- An endpoint set through `VOICE_REPLY_SPEECH_URL` is checked by making the clip itself: a failed
  request is reported with its error, and the reply goes out as text.

## Making a reply

1. **Write the reply first**, as text the user reads. Shape the spoken part for listening: short
   sentences, with code, paths, links and tables left to the written text.
2. **While the user is still describing what they want, the spoken part converses.** It restates
   what the agent understood in its own words, names what is still unclear, and asks one or two
   clarifying questions. It never commits to work the user has not described yet.
3. **Make the clip:** run `python3 scripts/speak.py <output folder> <clip name>` from the skill's
   folder, with the spoken text on standard input. The clip name is a plain file name. The script
   prints the path of a self-contained HTML page holding an audio player with the clip embedded in
   it. The output folder is the one the skill's **Keep the file** bullet names.
4. **Show the player, then the reply's text under it**, through the route the skill's **Harness
   compatibility** section names. A decision the reply asks still goes through the question tool,
   as the global rules say; the clip may speak it, and the tool asks it.
