---
name: progress
description: "Show the current task's progress as a dashboard built from the session ledger: its plans and step status, percent complete, time remaining, questions waiting on the user and answers given, the task's pull requests, a Wrap up page for what remains to merge and deploy, and an Architecture page for what the pull requests change. Use whenever the user asks for progress, status, a dashboard, what is left or what is waiting on them, at any point in a task."
short_description: 'Show the task’s progress as a dashboard.'
---

# Progress

Build the task's dashboard from what the ledger records, never from what the chat still remembers,
and deliver the same dashboard again on every request so the user keeps one page.

## Dependencies
- `session-ledger`
- `list-prs`
- `use-dashboard`
- `pre-production`
- `execute-task`
- `merge-gate`

## Workflow

1. **Read the ledger.** Resolve and read the task's ledger through `session-ledger`. A question the
   task has put to the user that the ledger lacks is reconstructed and recorded first, from verified
   task evidence, as that skill's recovery rules say, approved only where the user's own message
   approved it; so is a plan the task showed them, recorded as shown unless their own message
   approved it.
   The dashboard never shows a step the ledger does not hold. The figures cover the whole task since
   its first plan was shown or approved, so that check spans every plan it has had, finished ones included: a
   plan another entry names, such as one a later plan continues or supersedes, and finished work the
   task's record shows that no recorded step holds, such as completed items on the harness task
   list, are each a plan the ledger lacks. A plan that continues or supersedes another replaces only
   the steps it names; the earlier plan's finished steps stay in the count. An active or blocked
   step that verified task evidence shows with parts, held in the ledger without them, gets them
   recorded the same way, with the parts already finished marked done.
2. **Find the task's pull requests** with `list-prs`, requesting every state, then read each one's
   current state from its host: open, draft, merged or closed, the checks on its head, and review
   state.
3. **Write the Architecture page** once the task has a pull request the page covers. It covers the
   task's pull requests except those closed without merging, which the dashboard leaves out. The
   `dashboard` entry records the page's sections as last written and the head of
   each pull request they were written from: reuse them while the page covers the same pull requests
   and every head is unchanged; otherwise read the diffs of the pull requests it covers, write them
   again, and record them with the new heads.
4. **Build the spec** in the shape the [dashboard spec](references/dashboard-spec.md) holds, with
   `updated_at` set to now.
5. **Select the delivery route, then render.** Before invoking `use-dashboard`, choose the
   host's ongoing-work channel when authorized work remains, or the normal reply route for
   standalone reporting. Pass that route to the renderer for its delivery, as a dashboard of session
   work; whether it updates an earlier page is `use-dashboard`'s **Session work** rule. Record a
   new page in a `dashboard` entry with its path and any published link, so the next request finds
   it.
6. **Report and return to the caller.** Through the selected route, send the link or file and one
   line: percent complete, time remaining, and how many questions wait on the user, each the figure
   the dashboard shows. When reporting interrupts unfinished authorized work, carry out the active
   run's saved next action under `execute-task`'s **Waits And Awaited Results**. A report without
   that action does not complete this step; when an awaited result holds the action, retain that
   owner's wait and resume route.

## Spec

Read the [dashboard spec](references/dashboard-spec.md) before building it: it holds the header,
progress figure, metrics, counts, ordering, pull request names and every page's sections.

## Guardrails

- Show only what the ledger and the hosts verify. A time is measured only when the ledger holds
  both ends of it; anything else is an estimate and reads as one.
