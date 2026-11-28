# Open Decisions

This reference of `user-facing-output` holds how the list of unresolved decisions is written, how a
decision waiting on evidence is reported, and how an action the reader owns is handled. The skill's
**Open Decisions** section says when each applies.

## The list

- The list is numbered, and each item starts with a **bold subject**.
- An evidence-pending item states its pending work.
- A ready item identifies the question-tool request already sent for it, in the turn its supporting
  material was ready, and the work depending on it.
- An item with neither a sent request nor pending evidence work is asked in this turn, through the
  question tool.
- Identify optional choices and any implementation assumption, without presenting either as
  approval.
- A list longer than five items is grouped into blocks of at most five, omitting no optional or
  unresolved item, even where another output rule shows only the first few items of a list.
- The list accompanies a skill's required direct-chat result even when that skill says to return
  only its result or nothing else; the result keeps its own shape.

## Evidence-pending decisions

- **A decision whose support the reader asked for stays unresolved, with its evidence work marked
  pending.** Until the requested support or explanation is provided, report that work and what
  remains to supply instead of asking for the choice again. Provide the support before making the
  same question actionable; a capture or report that exists but has not been shown does not
  establish readiness.
- **A change the reader asked for that alters what an open question is about makes it
  evidence-pending the same way**, such as a field added to the form whose layout is being chosen:
  the evidence already shown does not show what the reader would choose about, and the change may
  settle the question or remove it. Report the change in progress instead of the question; once it
  lands, show the changed state with the question, or drop the question when the change answered
  it.
- Only the question the evidence or the change concerns waits. Every other open question stays
  active through the global rules' **Asking the user** procedure and visible in the list.

## Reader-owned actions

- **Timing.** Preparation is only work that changes what the reader will do; other queued work, a
  guidance edit included, waits behind the question, which goes out in the turn the need is
  established. Chat text never announces the step ahead of that question, apart from the material
  the question shows, such as a report whose `Next:` line names the review it asks for.
- **Content.** Its text names the whole step, including any command. An address it gives is one
  the governing guidance or the product itself states, or one the agent opened and saw serve that
  step; never one assembled from the product's name.
- **Surface.** Where the step happens on a surface the agent can open — a viewer, a settings page,
  a sign-in page — the agent opens it at the exact place and verifies it shows before asking, so
  the reader's part is the action alone.
- **Result.** A confirmation is the reader's word, not the outcome: check the result at its source
  before building on it.
- A question-tool request for an action the reader owns is asked again as global **Asking the
  user** says; a later message mentions the action again only when it blocks the next step or the
  reader asks what they owe. Once they say they will do it later, it is settled and stays out of
  every later message and request.
- When the reader has said they will review later, a report omits its `Next:` review action instead
  of repeating it.
- Record the action and the reader's deferral of it with `session-ledger`, as an active-work entry
  owned by the reader with the deferral as an observation, so the settled state survives
  compaction and handoff.

## Before sending

Every unresolved decision, optional choices included, appears in the numbered list as an active
question-tool request or as evidence-pending work, according to its readiness; an unconfirmed
assumption appears as an assumption, never as a question. A chat question appears only where the harness has no question tool. A resolved or
superseded question does not reappear.
