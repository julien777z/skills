# Authorization

What `SKILL.md`'s **Task Authorization** and **Showing The Plan** apply: what an authorization covers, when a
step is a new approval boundary, and how a step or choice reaches the user.

## What An Authorization Covers

- **A direct invocation authorizes one full run at the requested scope.** An explicit request to
  continue a loop authorizes repeated runs only within that loop until its outcome or the user's
  explicit stop or handoff. Start the invoked skill and ask before narrowing its scope.
- **An authorized task, including a fix request or a plan in execution, covers its ordinary work for as
  long as it stays active**: implementation, verification, scoped external changes, retries,
  recovery and cleanup. A follow-up, interruption, failed attempt or context reset does not require
  the user to approve those sub-steps again. Never ask the user to restate the task with
  "continue", "proceed" or another intermediate approval question: state progress and take the next
  ordinary authorized action.
- **A new authorization is needed only where the action materially expands the target, recipient
  or outcome**, or a platform actually requires an action-time confirmation. Make that question
  specific to the new decision or action; never ask the user to reconfirm the task or say
  "continue" to resume it.
- **Work is never declined for a guessed budget.** For an invoked skill, do not decline, defer or
  drop a finding, fix or validation step because the work looks large, difficult, or likely to
  exceed a guessed time, context or token budget. Only the user declares a budget spent. Work until
  complete, short of the limit in [review rounds](review-rounds.md), which is the user's standing
  instruction; a concrete gate holds only its dependent operation. On an explicit user stop or
  handoff, report what finished and record precisely what resumption needs.
- **Merge, deployment, publication and release are separate outcomes outside the ordinary scoped
  external changes above**, and `merge-gate`'s **Authorization** says what authorizes each. An
  unauthorized merge leaves the pull request draft for the user; a deployment, publication or
  release the request does not name is no part of the task, and nothing waits on it.

## Approval Boundaries

- **Before treating an intermediate step as a new approval gate, read the applicable tool or
  workflow rule and test its exceptions against the actual action and existing authorization.**
  - A consent page, a credential being saved, or a security-related label alone does not establish
    expanded access. Routine sign-in retaining the authorized recipient, permissions and duration
    remains part of the task unless the governing rule explicitly requires confirmation for that
    case. Name the exact triggering change or platform requirement when confirmation is required.
  - An implementation constraint is not a new approval boundary. Exhaust authorized ways to
    complete a sub-step yourself.
  - When a platform imposes an action-time confirmation for a distinct sensitive action, complete
    all non-impactful preparation first and ask one exact question immediately before that action.
    Make clear that the task remains authorized. Wait up to 10 minutes without polling or
    interacting with the approval surface; treat it as failed only after that window or an explicit
    failure. A failure is not approval: wait for the user to resume before prompting again.
  - Do not mistake an action-time confirmation for a mandatory user hand-off: after the user
    confirms the specific pending action, perform it yourself. Hand off only when the platform
    requires the user's own interaction. Never request a secret through chat.
  - After a required confirmation, complete the remaining authorized work without another approval
    question. A refused or unanswered confirmation blocks only the action it governs, as **Work You
    Have Already Named** says of every wait.
- **A plan shown to the user, and a proposed change presented at a user-approval boundary, each
  carry `review-proposal`'s ready receipt.** First check for its valid ready receipt for the exact
  proposal and reviewed inputs; when present, show the plan, or present the supporting content and
  ask, without re-entering it. Otherwise prepare that receipt first. This applies to plans and to
  approval-requiring change proposals, not
  factual questions, routine authorized work or a platform's separate action-time confirmation.
  `acceptance-gate`'s technical verdict is not a user-approval request and never recursively
  enters this procedure.
- **A question the guidance already answers is not the user's to answer.** Before a question goes
  out, and again each time one carried from an earlier turn, a note or a summary would be put
  again, read the rules and the repository's project guidance governing its subject; where they
  decide it, act and report what was done. The class: whether to delete, reset or recreate a local
  resource, such as a cache volume filling the disk or a database stuck on a migration the branch
  has since regenerated, and whether to reset or reopen local records to reach a state, such as a
  test account back at its first sign-in, both of which `pre-production`'s **Local Stacks** gives the agent; what a
  data change owes records already stored, which project guidance says; which of two
  implementation details to use where a rule picks one; how to remove duplication the guidance
  treats as a defect — which repository or package owns shared behavior and which mechanism replaces
  parallel copies — which `pre-production` and `code-simplify` settle; and what configuration exists
  or how it is scoped, which is read where it lives. A permission denial leaves the decision where
  it was, as [working environment](environment.md)'s **Environment Refusals** says.
- **An encountered issue's remedy passes the product-choice test before it is chosen**, as
  `pre-production`'s **Product Choices** sets, including one proposed by a worker or reviewer. An
  ambiguous instruction has no approved interpretation: name both concrete outcomes and build on
  the user's answer, quoting their words in a delegated brief. This decision wait holds only the dependent remedy, never the
  remaining authorized work.

## Steps Only The User Can Take

A step only the user can take, which the work waits on, goes to the user as a reader-owned action,
asked as `user-facing-output` says. Before it does, settle that it is theirs:

- **Whether a step is only the user's is settled before asking.** A step the agent's tools can
  reach by any route — inside a machine or VM it controls, through a viewer or settings page it can
  open, or briefly through the user's own desktop input where the task's authorization and tool
  policy permit it — is the agent's to take, never put to the user as a request or as a choice
  between their doing it and the agent's. The agent prefers the route that leaves the user's
  desktop alone and states any interruption, such as a moving cursor, when it happens. Only what
  needs the user's own identity, device, password or physical presence goes to them.
- **Reach is settled by locating the target, never by one failed route.** Before a machine, service
  or setting is called out of reach, find where it runs — whether its address is one of this
  machine's own, whether it runs in containers or processes here, and which tailnet node,
  management API or other host the agent controls reaches it — and try each route; a refused
  connection to one address rules out that route alone.

## Choices Between Versions Of A Page

**A choice between substantially different versions of a page shows every option rendered.** When
the options differ in layout, structure or the controls the reader uses — a list or a grid, one
column or two, a section moved or removed — the question comes right after a capture of each option
as the product would draw it, built as an uncommitted preview where it does not exist yet, at the
widths where the options differ, shown as `share-media`'s **Previews for a choice** says.
Describing an option, or showing only the current state, leaves the reader guessing at the one they
cannot see, so the question waits until every capture is ready. A drawing made of text, such as a
sketch in a question tool's preview, is a description, not a capture. A choice between wordings or
between small adjustments of one detail is shown as text or a single capture.
