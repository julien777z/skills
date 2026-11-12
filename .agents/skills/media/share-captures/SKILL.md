---
name: share-captures
description: "Show screenshots, recordings and rendered previews to the user in the agent's own reply, as they are read and with the questions that need them. Use whenever work produces captures of a product, a site, a game or a generated image, and before asking the user to choose between options that differ in how something looks."
short_description: 'Show captures and option previews where the user reads.'
---

# Share Captures

The global rules' **User-Facing Output** says which captures reach the user and when. This skill is how
they get there, the same way for a web walkthrough, a game playtest or a generated image.

## Send each capture where the reader sees it

- **Read it whole first**, region by region, as the global rules say; a capture you have not read is
  never sent.
- **Show it in your own reply**, in the part of the reply the harness shows the reader, as
  **Harness compatibility** below says. A tool that posts a message to the thread on the user's
  behalf is never the route, and neither is text the harness folds away from the reader.
- **Keep the file where the reader's view can still load it**: copy it out of scratch and temporary
  folders into a folder the session lists as a working directory outside the repository checkout,
  such as an attachments folder, so the chat history keeps the image and the checkout stays clean.
- **Captions and order:** a capture of a page is captioned as the global rules say; any other
  capture, such as a game's place or screen or a generated image, is captioned with what it shows,
  its device or width, and its state. Each capture sits directly under the text it belongs to, as
  the global rules say.

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
   the message that ends a turn is shown, as in T3 Code, that message ends the turn, and the
   question goes through the question tool at the start of the next one. The question names each
   option by its image's caption, never by position, and states in its own text what each does.
4. **When the user says they cannot see the previews**, the route failed: fix it and show them again
   before re-asking, never re-ask over the same broken route.

## Harness compatibility

- **T3 Code:** write each capture into the reply as a Markdown image with its absolute path,
  `![caption](/absolute/path/to/capture.png)`; T3 renders local files inline. Only the message that
  ends the turn is shown: text written before a tool call is folded into the turn's work log, and an
  open question tool hides it too. So captures go in the turn's final message, and a capture made
  mid-work goes out when the turn ends on a wait for background work. A question never goes into
  that message: it goes through the question tool, as the global rules say. `t3_thread_send_attachments`
  posts a new message into the thread as the user, so it never carries the agent's own captures.
  Any other file the user should see, such as a plan or a detail file, is a Markdown link to its
  absolute path, `[name](/absolute/path/to/plan.md)`, kept in the working directory **Keep the
  file** above names, in the turn's final message; T3 opens it in its files viewer.
