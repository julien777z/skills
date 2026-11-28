---
name: self-improvement-protocol
description: How an agent improves its own work and guidance — the interface it delivers, such as a dashboard, its own process, such as wasted effort, repeated or empty review rounds and subagents that cost more than they found, and the guidance that let either through — judged from evidence as the person the work is for, fixed at the owner every case shares, and repeated until a pass finds nothing worth changing, apart from the single end-of-task pass. Read from a skill that declares it, such as a skill that improves dashboards, a look-over before delivering a page, or the end-of-task look-over; never invoked on its own.
short_description: 'Judge and fix the agent''s own interfaces, process and guidance from evidence.'
user-invocable: false
---

# Self-Improvement Protocol

A skill that has the agent improve its own work runs this protocol and adds only what is specific to
its subject. The product or code a task is about is the task's own work, never self-improvement;
an audit of a product's repository is a doctor skill's work.

## Dependencies
- `skill-pass`
- `use-browser`
- `session-ledger`

## What To Look For

- **Interface**, anything the agent delivers for a person to read or use, such as a dashboard or a
  report:
  - information the reader came for that is missing, or that takes a click to find when it should
    be in view;
  - the same fact shown twice, a label repeating its heading, a value that looks like another kind
    of value, such as a duration drawn like a tag;
  - a claim the evidence does not support, such as a figure computed the wrong way or a cause never
    traced;
  - rows, columns or figures that do not line up, so like things cannot be compared;
  - hover, focus and click states that show nothing useful, open the wrong thing or leave the
    reader stranded;
  - one thing drawn two ways across pages or across skills, and a part two skills each build that
    belongs in their shared owner.
- **Process**, what the agent and its subagents did, read from transcripts and timings:
  - effort spent on work nobody asked for, and the guidance that drove it;
  - review, gate or loop rounds that found nothing, or found the same thing again because a rule
    was written in several places;
  - subagents whose cost was out of proportion to what they found, or that duplicated another's
    work;
  - work redone, traced to the decision that caused it, such as a reviewer's suggestion followed
    literally or a step run in the wrong environment;
  - waits and stalls, such as a run lost to a rate limit, and what would have avoided them.
- **Captures of what the agent built**, such as screenshots and recordings of a game, a page or an
  app: each flaw judged in one is also checked against the skills governing that product, and a
  flaw those skills would not have prevented is recorded as a guidance fix for its class.
- **Guidance**: a rule restated in several skills, a rule that let a miss through, a trigger that
  did not fire, a step the agent performed that no skill describes.

## How To Judge

- **Use it as the person it is for.** An interface is judged rendered, never from its source: open
  every page in the browser `use-browser` selects and try one or two of each kind of item, dialog
  and tab, as a reader samples a page rather than opening everything, at a phone width as well. A process is judged from its transcripts and
  timings, never from memory of the run.
- **Ask what that person came for.** Read the owning skill's statement of its purpose and check
  whether each page answers it at a glance; a page that renders correctly but leaves the reader
  hunting is a finding.
- **Trace before stating a cause**, as the global rules require: a finding that blames guidance
  reads when that guidance took effect.

## Where A Fix Goes

- A flaw every case would share goes to the shared owner: the renderer and its rules for anything
  every dashboard draws, a rule file for a subject several skills meet. A part two skills each
  build goes there once, and each skill points to it.
- A flaw in one skill's data, pages or process goes to that skill.
- A flaw in the work in hand, such as a wrong figure in one rendered page, is fixed in that work
  as well as in the guidance that let it through.
- Every guidance fix runs through the guidance-editing workflow, written for the class of the flaw
  as its Scope Statement sets, and placed as `skill-pass`'s **Where Guidance Lives** says.

## Delivery

The guidance fixes a pass makes go on the session's self-improvement pull request, which the GitHub
rule's **Merge Authorization** holds and says what joins: open it with the first fix, based on the
freshly fetched default branch, or on the task pull request's branch when a fixed file is changed
there, and record its creation receipt through `session-ledger`.

## End Of Task

The look-over a task's ledger processing runs at its completion is one pass that records guidance fixes
only: it sweeps the run for flaws, such as those in captures, that no guidance fix recorded when
they were judged, sends no worker back to rework what the task delivered, and does not iterate.

## Iterate

Apart from **End Of Task**, fix, re-render or re-run, and judge again. Stop when a whole pass
finds nothing worth changing. Report what changed, grouped by skill, each line naming what the
reader now sees or what the agent now does, never how a page was built or why it looked wrong
before. A part moved to its one shared owner is one plain clause saying what that gives the reader,
such as "the Work board is one shared part, so both dashboards show the same cards". A skill whose
files the pass did not edit is reported as unchanged.

## Output

```markdown
**<skill>:** <each change, one line, as what the reader sees or the agent does now, or unchanged>
**<skill>:** ...
**Passes:** <n>, the last finding nothing worth changing, or 1 at the end of a task
```
