---
name: voice-reply
description: "Speak replies to the user as audio clips they play in the chat, with the same words as text, so a conversation runs by voice: the user dictates, the agent answers out loud, restates what it heard and asks its clarifying questions. Use when the user asks to talk by voice, hear the agent, have replies read aloud, or hold a spoken back-and-forth to clarify what they want."
short_description: 'Speak replies as playable audio clips in the chat.'
---

# Voice Reply

The user talks through the harness's dictation; this skill gives the agent the other half of the
conversation. Each spoken reply is a clip the user plays where they read the chat, with its words
written beneath it, so the exchange is heard and recorded at once.

## Dependencies
- `share-captures`

## Setup

- **The voice is a local text-to-speech service with an OpenAI-compatible speech endpoint**, read
  from `VOICE_REPLY_SPEECH_URL` (default `http://localhost:8880/v1/audio/speech`) with the voice
  from `VOICE_REPLY_VOICE` (default `af_sky`). The VoiceMode installer (`uvx voice-mode-install`)
  sets up Kokoro on that port; `voicemode service start kokoro` starts it.
- Before the first reply, check the service answers at its `/health` route beside the endpoint, and
  start it when it does not. Its first clip after a start takes far longer while the model warms up.

## Speaking A Reply

**Speak only the replies that clarify**: one that restates what the agent understood, or asks the
user something about what they want. A report, a progress update or a reply that is mostly links,
code or paths stays text only, unless the user asks to hear it.

1. **Write the reply first**, as text the user reads. Shape the spoken part for listening: short
   sentences, no code, paths, links or tables read aloud, and those left to the written text.
2. **While the user is still describing what they want, the spoken part converses.** It restates
   what the agent understood in its own words, names what is still unclear, and asks one or two
   clarifying questions. It never commits to work the user has not described yet.
3. **Make the clip:** run `scripts/speak.py <output folder> <clip name>`, passing the spoken text on
   standard input. It prints the path of a self-contained HTML page holding an audio player with
   the clip embedded in it. Use a folder outside the repository checkout that the reader's view can
   still load, as `share-captures` says of captures.
4. **Show the player in the reply**, then the reply's text under it, through the route
   **Harness compatibility** names. A decision the reply asks still goes through the question tool,
   as the global rules say; the clip may speak it, and the tool asks it.

## Harness compatibility

- **T3 Code:** render the page with `html_render`, at a height of about 72 pixels. A Markdown link
  to an audio file does not play when the user's client connects to the agent's machine remotely,
  and a player that loads its sound from the page itself does.
- **Any other harness:** show the page the way it shows a rendered HTML preview; where it has none,
  send the page as a file the user opens, as `share-captures` says for that harness.
- Never play the clip on the agent machine's speakers as the reply: the user may not be at that
  machine.
