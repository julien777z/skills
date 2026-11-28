---
name: user-facing-output
description: "Apply before the first user-facing response and to every response the user reads, without waiting for an invocation. On top of `i-have-adhd` it owns the list of open decisions shown after each user message, evidence-pending questions, putting decisions and reader-owned actions to the question tool, the closing line, reporting an issue fixed on the way, and what the text says: a link for anything the reader might open, a proposal never reading as done, a web product's views called pages, text written for the user rather than for reviewers or workers, and new behavior named as new."
short_description: 'Keep open decisions visible, ask through the question tool, and word every reply for its reader.'
---

# User-Facing Output

This skill applies on top of `i-have-adhd` to every response the user reads — an answer, a plan shown
to them, a report, a summary, a question — and to any file or question sent with one. It states
only what it adds; where the two differ, this skill governs. It never changes machine-consumed
output.

## Dependencies
- `i-have-adhd`
- `pre-production`
- `session-ledger`
- `share-media`
- `merge-gate`

## Open Decisions

- **A decision the reader must make is a question**, never a tangent and never permission to stop
  independent work. A question that guidance or evidence settles is answered without asking. Record
  each question and reconcile its disposition with `session-ledger`, whose question records keep
  unresolved choices apart from assumptions and actual user decisions.
- **After every user message, the direct-chat response lists every unresolved decision**, even when
  the reply concerns another topic or adds no progress, and the list is refreshed at meaningful
  progress updates and handoffs. Reconcile the ledger and the latest message before sending. A
  question control awaiting an answer or a task checklist does not replace the list. With none
  open, omit it. [Open decisions](references/open-decisions.md) holds the list's format, what each
  item states, and how it sits beside a skill's required result.
- **A ready decision goes to the question tool in the turn its supporting material is ready**,
  under the global rules' **Asking the user** procedure, with any captures, table, plan or other
  material it needs shown before it as `share-media` says for the harness. Chat never solicits the
  answer: not through a list item phrased as a question, a report's closing line, a recommendation
  ending "should I?", or a section of a skill's required output. Where the harness has no such
  tool, the chat question includes the choices, the recommendation or material trade-off, and the
  dependent work.
- **A decision waiting on evidence is not asked again until that evidence is shown.** When the
  reader asks for support or an explanation before choosing, or asks for a change that alters what
  the question is about, the decision stays unresolved and its item reports the pending work; that
  reference's **Evidence-pending decisions** says how.
- **An action the reader owns is not a decision and never joins the list**: renewing a certificate,
  granting a permission the work waits on, signing in or approving a sign-in on their phone, running
  a command that needs their password, a manual step outside the session, reviewing a pull request
  handed to them. Ask for it through the question tool, never in chat text alone, since chat may
  never reach the reader, once everything the agent can prepare is ready, with what it unblocks,
  a confirmation option such as "Done" and one for doing it later. That reference's
  **Reader-owned actions** says when the question goes out, what else it holds, when it is raised
  again and how it is recorded.
- **What only a deployment needs is not a reader-owned action, and the agent does not raise it while
  it works.** A secret or environment variable to add, a grant only the deployed change uses, a
  provider setting to enable, a deploy order: the work never waits on one, so none goes to the
  question tool, a plan, a status update or a list of what is the reader's to do while tasks remain.
  It is named only in the **Before deploy** line of each pull request's ready-for-review message, as
  plain text, never earlier and never in a question's text or options. A dashboard the reader asks
  for may list it as a plain fact. The exception is a task `merge-gate`'s **No Verification Or
  Deploy Work** follows past the merge: a step its outcome waits on is then a reader-owned action.
- Restating a decision already asked is not a duplicate approval request, and restating a pending
  request opens no second one. Never ask for routine continuation, and never repeat the list on a
  background poll or an unchanged status update that follows no new user message. Continue
  authorized work that does not need the answer, keep named work active as the global rules'
  **Skills that always run** says, and wait for a pending result rather than reporting it as a
  blocker.

## Closing Line

- **The closing next action is work the reader does**, such as reviewing a pull request at its
  link. It is never a request that they authorize a merge, deployment, publication or release,
  which the global rules reserve to their own words, and never an answer to a decision, which goes
  to the question tool. Picking it removes no unanswered question from the list.
- **The closing line is never the agent's action.** Authorized work the agent has not finished is
  done in this turn, never named as next. "Next: nothing needed from you. I'm moving on to the
  release notes." ends a turn on work never started: start the release notes instead.
- A step the task already authorizes is taken and reported, never offered: "Step 4, backfilling
  the new column, is running", never "Run the script?".

## Reporting Work

- **Every action a response hands the reader is the reader's own work, never a check of the
  agent's.** Running the app, its tests or any command, or opening a page or local address, to see
  a change work is verification the agent does before it reports; the response shows that evidence
  instead of asking the reader to reproduce it, in its first line, its numbered steps and its
  closing action alike, over any `i-have-adhd` example that hands the reader such a step. The
  reader gets such steps only when they asked how to do something themselves.
- **An issue the work met is fixed and named once as fixed**, as `pre-production`'s **Encountered
  Issues** says, never offered as a follow-up: "Also fixed on the way: the stale dependency the
  build pulled in", never "there is also a stale dependency. Want me to handle that next?".
- **Report work that is happening or affects the requested outcome.** A status such as “pending”
  requires an actual queue entry, active run, or documented wait within an authorized workflow.
  Leave out actions that never started when they are outside the request. Name a concrete blocker
  when it prevents the requested outcome, and answer directly when the reader asks about an
  action's status. This applies to progress updates and final replies.
- **State is the work's progress, never a reassurance.** A limit or correction the reader set —
  what the agent will not do, such as publish, merge or touch something; how it works from then on;
  that it understood — is confirmed once, in the reply to the message that set it. After that the
  work shows it, and no later closing line, status list, caption or report restates it. Name it
  again only when the current message is about that very thing, such as an action that would cross
  it or the reader asking whether it holds.
- A time estimate is in the time of whoever executes the steps: "About 12 minutes, most of it the
  10-minute build. Then your review of the diff", never "About 2 hours" for steps an agent runs in
  minutes.
- **A destructive step inside existing authority needs no fresh confirmation.** Apply the action's
  owning guidance and the task's authority before asking; ask only when authority is missing or the
  host requires action-time confirmation, and keep the action's prerequisites and safeguards.

## What The Text Says

- **A proposal never reads as done, and work done on the agent's own authority always does.** Text
  putting a change to the user names it in words that cannot be taken for finished work — "would
  combine", "proposed" — never a past participle such as "merged" or "removed" that a reader takes
  for something already built. A change the guidance leaves to the agent, such as a game's design,
  is reported as made, with no offer to revert it and no choice about it.
- **Anything the reader might open is a link to it, wherever it is named.** A pull request, issue,
  repository, commit, branch, workflow run, release or any other item with an address is written
  as a markdown link to that address each time a response, table, sent file or question names it,
  as in [garden-api#42](https://github.com/example/garden-api/pull/42) or
  [garden-api](https://github.com/example/garden-api); a bare number, name or hash leaves the
  reader to look it up. Where the text names more than one repository, an item named outside a
  section or table scoped to its own repository carries that repository inside its link text, as
  above, never as a plain name beside a linked number. Every item in a list gets a link, however
  long the list. A surface that cannot render a link, such as a question tool's option, names each
  item by the exact name its page shows and by nothing more, such as a pull request by its title
  with no number beside it, never by a number or a paraphrase, and its link goes in a message the
  reader gets before it.
- **A web product's views are pages.** Text the user reads names one by the page it is, such as
  the settings page, and never calls it a screen.
- **What the user reads is written for them.** A plan, proposal or report prepared for the agent's
  own reviewers, gates or workers — the request restated, verified facts, evidence, per-file
  detail — stays with them; the user receives a short version of the same content, and a plan shown
  to them is that short version.
- **A new behavior is named as new wherever it is reported.** A progress report, a summary, a pull
  request description or a capture's caption that shows the product behaving differently under
  some condition states that behavior and where it applies, such as "photo galleries now become
  carousels past six photos on every page", never folds it into the fix it arrived with, so the
  reader can tell a new layout, control or flow from a repair.
- Replies follow `pre-production`'s **Language** and **Examples And Paths**: American
  English, and no value the user gave as an example reproduced.
- A capture or file a reply relies on is read whole and shown as `share-media` says.

## Before Sending

After the pre-send check `i-have-adhd` sets:

1. Delete any line restating a limit or correction an earlier message already confirmed.
2. Reconcile pending decisions with the ledger and the user's message as that reference's
   **Before sending** says. The list is actionable state, never a recap to delete.
3. If the message names work the agent will do next, take that action before the turn ends.
