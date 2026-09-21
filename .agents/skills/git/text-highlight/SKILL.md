---
name: text-highlight
description: "Show changes as diff-shaped code blocks a reader can locate at a glance: an edited line marked + in the form it now takes, a line dropped with nothing in its place marked -, a few unchanged lines around each change, and ... where the file goes on. Every file fences with diff so the marks colour, a document as readily as a module; text mode drops to a plain fence only when asked for. Invoke as /text-highlight [code|text] [paths], or from a skill that declares it."
---

# Text Highlight

Render what changed so a reader sees each change where it sits in the file, without opening the
diff themselves: the changed lines marked, enough unchanged lines to place them, and nothing else.

## Modes

- **code** — the block is fenced ```` ```diff ````, so a renderer colours a changed line green and
  a dropped line red while unchanged lines read as ordinary text. **Every file renders this way**,
  a document as readily as a module: colour is what lets a reader find the change without reading
  for it, and prose needs that more than code does, not less.
- **text** — the same shape in a bare ```` ``` ```` fence, with no colouring. It exists for a
  destination that renders no diff fence, and is reached only by asking for it.

Mode is code unless the invocation or a caller asks for text, and that choice covers every file in
the call.

## Workflow

1. **Resolve the scope.** With paths, the hunks of those files; without, the branch's diff against
   its merge base with the remote default branch, plus untracked files the branch adds. A caller
   may hand over a diff instead; use it as given.
2. **Take the hunks from the diff, never from memory.** Read `git diff -U3` (or the caller's diff)
   for each file and carry its hunks across: the diff's own line content, its own three lines of
   context above and below each change, and its own order. A line that is not in the diff is not in
   the block, and a block that does not match the diff is a defect.
3. **Shape each file's block.** Drop the diff headers and hunk markers, and keep every line's mark
   exactly as `git diff` writes it: one space for an unchanged line, `-` for a removed one, `+` for
   an added one, each immediately followed by the line itself with no second space.
   - **The leading space on an unchanged line is load-bearing, not decoration.** A `diff` fence
     colours every line that opens with `-`, so a document's own `- ` bullet renders as a deletion
     the moment that space is dropped, and a Markdown file is mostly bullets. The space is what
     makes an unchanged line read as unchanged and a removal read as a removal.
   - **An edited line shows only what it now says.** Where a run of removed lines is immediately
     followed by a run of added lines, the removed run is an earlier draft of the added one: print
     the added lines and drop the removed ones. So `+` reads as "this is what the line says now",
     and `-` is kept for a line that goes with nothing in its place — a run of removals no addition
     follows. A reader comparing two near-identical paragraphs word by word is reading noise; the
     one that stands is the one worth reading.
   Where the file continues before the first hunk, after the last
   one, or between two hunks, put `...` on its own line in that place. Two hunks whose context
   overlaps or touches become one run with no `...` between them. A file added or deleted whole has one
   hunk holding every line, so it renders whole with no `...` anywhere; a rename with no content
   change shows the two paths and no block.
4. **Write the path line.** Each block is preceded by a line holding the file's repository path in
   backticks, and, when the file was renamed, `old → new`.
5. **Order the files** as the diff orders them, one block each, a blank line between files.

## Output

Return exactly this shape, one entry per file, and nothing else:

````markdown
`<path>`

```diff
...
 <unchanged line>
 <unchanged line>
 <unchanged line>
+<line as it now reads>
-<line dropped with nothing in its place>
 <unchanged line>
 <unchanged line>
 <unchanged line>
...
```

`<next path>`

```diff
 <unchanged line>
+<line as it now reads>
 <unchanged line>
...
```
````

Every entry takes the `diff` fence, whatever the file is. `...` is the one line with no mark, since
it stands for the file rather than quoting it. With nothing to show, return the single line
`No changes to show.`

**The four-backtick fence above belongs to this page, not to the answer.** It is here so the
template's own fences are readable; a response that repeats it nests one fence inside another and
the reader sees the backticks as text instead of a coloured diff. Emit what is inside it and
nothing around it, and never wrap a block in a second fence to show its markers.

## Guardrails

- Never invent or paraphrase a line: every line in a block comes from the diff verbatim, prefix
  aside.
- Never omit a hunk to shorten the response; a file with many hunks shows every one of them, each
  placed by `...`. The superseded run step 3 drops is the one omission there is, and it is dropped
  because the line that replaced it is right there.
- Never add commentary inside or between the blocks; a caller that wants headings or links writes
  them around the blocks it receives.
