---
name: share-media
description: "Show screenshots, recordings, rendered previews and spoken audio to the user in the agent's own reply, as they are read and with the questions that need them. Use whenever work produces captures of a product, a site, a game or a generated image, before asking the user to choose between options that differ in how something looks, and when the user asks to talk by voice, hear the agent, have replies read aloud, or hold a spoken back-and-forth to clarify what they want."
short_description: 'Show captures, option previews and spoken replies where the user reads.'
---

# Share Media

The global rules' **User-Facing Output** says which captures reach the user and when. This skill is how
they get there, the same way for a web walkthrough, a game playtest or a generated image, and how a
reply reaches the user as speech.

## Dependencies
- `session-ledger`

## Send each capture where the reader sees it

- **Read it whole first**, region by region, as the global rules say; a capture you have not read is
  never sent. Read it for what is wrong anywhere in the frame, not for whether the thing you changed
  appears: the change showing is the smaller half, and a capture read only for it is a capture you
  have not read.
- **Fix what the reading finds before sending, then send the fixed capture.** A defect the work in
  hand can fix is fixed and captured again; the capture that showed it goes out only as the before
  half of that pair, or with the defect named as left and why, as the global rules'
  **User-Facing Output** says.
- **Show it in your own reply**, in the part of the reply the harness shows the reader, as
  **Harness compatibility** below says. A tool that posts a message to the thread on the user's
  behalf is never the route, and neither is text the harness folds away from the reader.
- **Keep the file where the reader's view can still load it**: copy it out of scratch and temporary
  folders into a folder the session lists as a working directory outside the repository checkout,
  such as an attachments folder, so the chat history keeps the image and the checkout stays clean.
- **Captions and order:** a capture of a page is captioned as the global rules say; any other
  capture, such as a game's place or screen or a generated image, is captioned with what it shows,
  its device or width, and its state, which is the name a question uses for it. Every caption then
  names what the reading found wrong, region by region: each defect, in the part the change touched or anywhere else in the
  frame, with whether it was fixed, or "read every region, nothing wrong" when the reading found
  none; a caption that only says what the capture shows, such as "the new toolbar renders", is
  incomplete. Each capture sits directly under the text it belongs to, as the global rules say.

## Previews for a choice

Which choices carry rendered options, and how each is rendered, is the global rules' bullet on
choices between substantially different versions of a page. Options that differ in how a game or a
generated image looks carry every option rendered too, at the devices or widths where they differ,
as page versions do. This is how those previews are sent.

1. **Read each rendered option whole** before it is tiled or sent.
2. **Make one image per option**, its views side by side (desktop beside phone, before beside
   after), so the reader compares options, not files. Tile them with any image tool on the
   machine, such as `ffmpeg -i a.png -i b.png -filter_complex "[0]scale=800:-2[a];[1]scale=800:-2,pad=800:<h>:0:(oh-ih)/2[b];[a][b]hstack=inputs=2" option-A.png`.
3. **Show the option images, then ask through the question tool**, never in chat. Each image goes
   under its caption with a line on what that option does, in a message the reader sees. Where only
   the message that ends a turn is shown, as in T3 Code, record the pending question in the
   session ledger through `session-ledger`, end the turn on that message, and ask the question
   through the question tool as the first action of the next turn; **Harness compatibility** says
   what starts that turn. The question names each option by its image's caption, never by
   position, and states in its own text what each does.
4. **When the user says they cannot see the previews**, the route failed: fix it and show them again
   before re-asking, never re-ask over the same broken route.

## Spoken replies

When the user asks to talk by voice, they speak through the harness's dictation and the agent
answers with a clip they play where they read the chat, its words written beneath it, so the
exchange is heard and recorded at once.

- **Speak only the replies that clarify**: one that restates what the agent understood, names what
  is still unclear, or asks one or two questions about what the user wants, never committing to
  work the user has not described yet. A report, a progress update or a reply that is mostly links,
  code or paths stays text only, unless the user asks to hear it.
- **Make and send each spoken reply** as [the spoken-replies reference](references/spoken-replies.md),
  this skill's procedure for the voice service and for making and showing a clip, describes. A
  question the reply asks goes through the question tool once the player and its text are shown,
  ordered as **Previews for a choice** step 3 orders a question after its images.
- Never play a clip on the agent machine's speakers as the reply: the user may not be at that machine.

## Harness compatibility

- **T3 Code:** write each capture into the reply as a Markdown image with its absolute path,
  `![caption](/absolute/path/to/capture.png)`; T3 renders local files inline. Only the message that
  ends the turn is shown: text written before a tool call is folded into the turn's work log, and an
  open question tool hides it too. So captures go in the turn's final message, and a capture made
  mid-work goes out when the turn ends on a wait for background work. A question never goes into
  that message: it goes through the question tool, as the global rules say. What starts the turn
  that asks it depends on the agent running in T3: under Claude Code, a background shell command of
  a few seconds started just before the turn ends re-invokes the agent when it completes; under an
  agent whose background commands do not re-invoke it, the user's next message starts that turn,
  so the images' message closes with one line asking the reader to reply once they have looked,
  such as "Reply when you've looked and I'll put the choice to you." That reply opens the question
  tool before anything else and approves nothing on its own. `t3_thread_send_attachments`
  posts a new message into the thread as the user, so it never carries the agent's own captures.
  Any other file the user should see, such as a plan or a detail file, is a Markdown link to its
  absolute path, `[name](/absolute/path/to/plan.md)`, kept in the working directory **Keep the
  file** above names, in the turn's final message; T3 opens it in its files viewer. A spoken
  reply's player page is shown with `html_render`, at a height of 80 pixels: a Markdown link to an
  audio file does not play when the user's client connects to the agent's machine remotely, and a
  player that carries its sound in the page does.
- **Any other harness:** show a spoken reply's player page the way the harness shows a rendered HTML
  preview; where it has none, send the page as a file the user opens.
