---
name: share-captures
description: "Send screenshots, recordings and rendered previews to the user as files, as they are read and with the questions that need them. Use whenever work produces captures of a product, a site, a game or a generated image, and before asking the user to choose between options that differ in how something looks."
short_description: 'Send captures and option previews to the user as files.'
---

# Share Captures

The global rules' **User-Facing Output** says which captures reach the user and when. This skill is how
they get there, the same way for a web walkthrough, a game playtest or a generated image.

## Send each capture as a file

- **Read it whole first**, region by region, as the global rules say; a capture you have not read is
  never sent.
- **Send it through the harness's file-sending tool** right after reading it, never held for the
  turn's last message, as **Harness compatibility** below says for the harnesses that need it. Where
  such a tool exists, text that only names or embeds a path is not a send: the reader may never see
  it, and nobody sees it while a question is open.
- **A harness with no file-sending tool:** embed the image in the message with Markdown image
  syntax naming a file the viewer serves, such as one in the session's listed working directories,
  copied there first. Say once that the harness cannot send files.
- **Caption every capture** with the page, place or screen it shows, the device or width, and the
  state, such as "the album's Sharing page at 1280" or "the level-select screen on a phone
  simulator, mid-transition".
- **Several items, each with captures,** go out item by item: one item's text and its captures,
  then the next. A caption never points at another message's images.

## Previews for a choice

A question between options that look different carries every option rendered, so the reader
judges what they will get, not a description of it.

1. **Render each option as the product would draw it**, at the widths or devices where the options
   differ, as an uncommitted preview where it does not exist yet: a branch build, a runtime toggle
   in the running product, or an edited copy of a capture. Read each preview whole.
2. **Make one image per option**, its views side by side (desktop beside phone, before beside
   after), so the reader compares options, not files. Tile them with any image tool on the
   machine, such as `ffmpeg -i a.png -i b.png -filter_complex "[0]scale=800:-2[a];[1]scale=800:-2,pad=800:<h>:0:(oh-ih)/2[b];[a][b]hstack=inputs=2" option-A.png`.
3. **Send the option images before the question**, through the file-sending tool above, in one
   message that names each image and says in a line what each option does.
4. **Then ask**, through the question tool, naming each option by the caption on its image, never
   by position, and keeping each option's label and one-line description matching that image. The question waits
   until every preview is sent.
5. **When the user says they cannot see the previews**, the send failed: fix the route and send
   them again before re-asking, never re-ask over the same broken route.

## Harness compatibility

- **T3 Code:** request an upload with `t3_attachment_prepare_upload` (type `image` or `file`, exact
  byte size), `POST` the file's bytes to the returned `relativeUrl` on the T3 server's local HTTP
  origin (the address the T3 app listens on, such as `http://127.0.0.1:<port>`, found from its
  listening socket), expect `204`, then send it with `t3_thread_send_attachments` to the session's
  own thread (`T3CODE_THREAD_ID`), with a message that captions each attachment in order. A pending
  attachment ID stays valid until its `expiresAt`.
