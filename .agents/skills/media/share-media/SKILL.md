---
name: share-media
description: "Show the user what they need to see in the part of the agent's reply the harness shows them: screenshots, recordings, rendered previews and spoken audio as they are read, and any table, plan, list or file a report or question relies on. Use before sending any file, image or recording, which is read whole first, to decide when a capture reaches the user, and when per-item detail past five items goes in a file. Use whenever work produces captures of a product, a site, a game or a generated image, whenever a reply points the user to material to look at, before any question whose supporting material is not inside the question itself, and when the user asks to talk by voice, hear the agent, have replies read aloud, or hold a spoken back-and-forth to clarify what they want."
short_description: 'Show captures, option previews, spoken replies and the material a reply relies on where the user reads.'
---

# Share Media

This skill says which captures and files reach the user and when, and how they get there, the
same way for a web walkthrough, a game playtest or a generated image, and how a reply reaches the
user as speech.

## Dependencies
- `session-ledger`
- `pre-production`

## What reaches the user, and when

- **Read every file, image and recording whole before sending or presenting it, and every capture
  taken to check work, whoever produced it.** One you have not read is never sent. Checking that it
  shows what the message says it does is the smaller half, and a capture read only for whether the
  thing you changed appears is a capture you have not read: go through it region by region — each
  section, banner, message, badge, empty state and control in the frame — and ask of each whether
  the product should show that, there. **Look before reading the sender's account of it:** a
  description read first narrows the look to the claim it makes, so judge the frame on its own,
  then check the claim. In a rendered scene, such as a game or a 3D view, the regions include every
  subject and what it touches: a character or object passing into a wall, a ceiling, the ground or
  another object, floating above what should hold it, or hidden behind something in front of it.
- **Fix what the reading finds before sending, then send the fixed capture.** A defect anywhere in
  it, in a region the message never mentions as much as the one it does — a state or error shown in
  a section it does not concern, a message repeated, a wrong value or tone — is named with the
  capture and fixed rather than offered, as `pre-production`'s **Encountered Issues** says. A defect
  the work in hand can fix is fixed and captured again; the capture that showed it goes out only as
  the before half of that pair; a defect whose fix a named gate holds goes out with that gate named.
- **A capture of a change reaches the user while the work is still running.** A screenshot, a
  recording, or a generated image that shows something the run changed — the screen after an edit, a
  before-and-after pair, a design it generated — is shown to the user as this skill says, once the
  agent that made it has read it as the first bullet says, never held for the final report, where
  it arrives in a pile the user can no longer follow. A capture nobody asked for that shows no
  change — taken while navigating, diagnosing, or recording a baseline before anything changed —
  stays where it was saved and is not shown, except as the before half of a pair once its after
  exists; a capture the user or the running skill asked for is shown as it is made, change or not. A
  subagent, whose reply the user does not see, hands each capture up to the agent that delegated to
  it, as its brief describes, and that agent reads and forwards each one on arrival. A brief that
  asks a worker for captures asks for them this way.
- **A capture sits directly under the text it belongs to.** A message holding several findings or
  changes that each have their own captures goes out as text and captures in turn: one item's text,
  then its captures right after it, then the next item's text and its captures, with a short
  closing line after the last. An item never points to its captures by position or by an earlier
  message — "the first three captures", "capture 6", "the screenshots above" — because a pile of
  captures shown together leaves the reader matching each one to its item. An item put to the user
  in a later message has its captures shown again directly beneath it, even those already shown as
  they were made; a question, asked again or for the first time, has its captures shown just before
  it, as **Previews for a choice** says.
- **A capture sent to the user shows which page it is.** The reader cannot ask, so a view leads
  with a capture at a width where the product's navigation shows the page's place, for the role
  whose page it is; a phone-width view or a close-up of the same page goes beside that one, never
  alone, since either can belong to several pages. The caption names the page as the reader reaches
  it, such as "the album's Sharing page".
- **A file the user should see reaches them where they read.** Per-item detail past five items —
  findings, rows — and the user's copy of any plan a skill gates go in a file that reaches the user
  from the agent's own reply, as **Harness compatibility** says for the harness, and the text that
  reports the result stays the turn's final message. An item with captures stays in chat, as the
  bullets above say; the file holds only the items without them. A text file sent this way reads on
  its own: it opens with the table or summary its detail belongs to, never the detail alone. Text
  reports sent together go as one markdown file, each report's table or summary before any detail.
  A path alone names nothing a user in a cloud or remote session can reach. The parent sends what a
  subagent produced. Where the harness gives a file no route to the reader, say so and put what
  fits inline.

## Send each capture where the reader sees it

- **Show it in your own reply**, in the part of the reply the harness shows the reader, as
  **Harness compatibility** below says. A tool that posts a message to the thread on the user's
  behalf is never the route, and neither is text the harness folds away from the reader.
- **Keep the file in the worktree's `.agent_sources/`**: a capture lives in its `captures/`
  folder. A copy goes elsewhere only where the harness's viewer cannot read that folder.
- **Captions and order:** a capture of a page is captioned as **What reaches the user, and when**
  says; any other
  capture, such as a game's place or screen or a generated image, is captioned with what it shows,
  its device or width, and its state, which is the name a question uses for it. Every caption then
  names what the reading found wrong, region by region: each defect, in the part the change touched or anywhere else in the
  frame, with whether it was fixed, or "read every region, nothing wrong" when the reading found
  none; a caption that only says what the capture shows, such as "the new toolbar renders", is
  incomplete. Each capture sits directly under the text it belongs to, as that section says.

## Previews for a choice

A choice between substantially different versions of a page, whose options differ in layout,
structure or the controls the reader uses, carries every option rendered. Options that differ in how a game or a
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
  ordered as **Previews for a choice** orders a question after its option images.
- Never play a clip on the agent machine's speakers as the reply: the user may not be at that machine.

## Harness compatibility

- **T3 Code:** write each capture into the reply as a Markdown image with its absolute path,
  `![caption](/absolute/path/to/capture.png)`; T3 renders local files inline. Only the message that
  ends the turn is shown: text written before a tool call is folded into the turn's work log, and an
  open question tool hides it too. So everything the reader must see goes in the turn's final
  message: captures, and also a table, a plan, a list of options, a file link and the facts a
  question relies on. A capture made mid-work goes out when the turn ends on a wait for background
  work. A question never goes into
  that message: it goes through the question tool, as the global rules say. What starts the turn
  that asks it depends on the agent running in T3: under Claude Code, a background shell command of
  a few seconds started just before the turn ends re-invokes the agent when it completes; under an
  agent whose background commands do not re-invoke it, the user's next message starts that turn,
  so the images' message closes with one line asking the reader to reply once they have looked,
  such as "Reply when you've looked and I'll put the choice to you." That reply opens the question
  tool before anything else and approves nothing on its own. `t3_thread_send_attachments`
  posts a new message into the thread as the user, so it never carries the agent's own captures.
  A file among that material, such as a plan or a detail file, is a Markdown link to its absolute
  path, `[name](/absolute/path/to/plan.md)`, kept where **Keep the file** above says; T3 opens it in its files viewer. A spoken reply's player page is shown with `html_render`,
  at a height of 80 pixels: a Markdown link to an audio file does not play when the user's client
  connects to the agent's machine remotely, and a player that carries its sound in the page does.
- **Any other harness:** show a capture or file through the harness's own way of attaching or
  rendering a local file in the reply; where it has none, say so and put what fits inline. Show a
  spoken reply's player page the way the harness shows a rendered HTML preview; where it has none,
  send the page as a file the user opens.
