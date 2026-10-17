---
name: progress
description: Show the current task's progress as a dashboard built from the session ledger — its plans, which steps are done, running, next or blocked, percent complete, estimated time remaining, questions waiting on the user, the answers already given, the task's pull requests, and an Architecture page with a diagram of how they work, what each changes, the settings they add, change or remove, and what to keep in mind. Use whenever the user asks for progress, status, a dashboard, what is left or what is waiting on them, at any point in a task.
short_description: 'Show the task’s progress as a dashboard.'
---

# Progress

Build the task's dashboard from what the ledger records, never from what the chat still remembers,
and deliver the same dashboard again on every request so the user keeps one page.

## Dependencies

- `session-ledger` — read the task's records and keep the dashboard's own.
- `list-prs` — find the task's pull requests.
- `use-dashboard` — render the spec this skill builds and deliver the page.
- `execute-task` — its already-active run owns the saved next action after reporting; standalone reporting does not start a run.

## Workflow

1. **Read the ledger.** Resolve and read the task's ledger through `session-ledger`. A plan or
   question the task has put to the user that the ledger lacks is reconstructed and recorded first,
   from verified task evidence, as that skill's recovery rules say; the dashboard never shows a step
   the ledger does not hold. An active or blocked step that `execute-task`'s **Progress Record**
   records with parts, held in the ledger without them, gets them recorded the same way, with the
   parts already finished marked done.
2. **Find the task's pull requests** with `list-prs`, requesting every state, then read each one's
   current state from its host: open, draft, merged or closed, the checks on its head, and review
   state.
3. **Write the Architecture page** once the task has a pull request the page covers. It covers the
   task's pull requests except those closed without merging, which the dashboard leaves out. The
   `dashboard` entry records the page's sections as last written and the head of
   each pull request they were written from: reuse them while the page covers the same pull requests
   and every head is unchanged; otherwise read the diffs of the pull requests it covers, write them
   again, and record them with the new heads.
4. **Build the spec** in the shape below, with `updated_at` set to now.
5. **Select the delivery route, then render.** Before invoking `use-dashboard`, choose the
   host's ongoing-work channel when authorized work remains, or the normal reply route for
   standalone reporting. Pass that route to the renderer for its delivery. When the ledger records
   an earlier delivery of this task's dashboard, update that same page; otherwise record a
   `dashboard` entry with the page path and any published link, so the next request finds it.
6. **Report and return to the caller.** Through the selected route, send the link or file and one
   line: percent complete, time remaining, and how many questions wait on the user, each the figure
   the dashboard shows. When reporting interrupts unfinished authorized work, carry out the active
   run's saved next action under `execute-task`'s **Work You Have Already Named**. A report without
   that action does not complete this step; when an awaited result holds the action, retain that
   owner's wait and resume route.

## Spec

- **Header.** `title`: a summary of the task in a few words, such as `Add bulk export`.
  `subtitle`: the task's goal in one line. `status`: `Waiting on you` (`warning`) while a question
  is open, which covers a step an open question blocks; `Blocked` (`critical`) while a step is
  blocked on anything else; `Done` (`good`) once every plan is complete; otherwise `On track`
  (`good`).
- **Progress.** A step's work is its estimate, or for a step with parts the estimates of its parts
  not skipped; a skipped step has none. `value`: finished work over all work, across every plan
  that is not withdrawn, where finished work is each done step's work and each done part of a step
  neither done nor skipped. `detail`: "<done> of <total> steps done", counting steps with work,
  adding "across <n> plans" when there are several.
  `segments`: one per step with work, in plan order, labelled "<plan title>: <step title>",
  `weight` that work in minutes, toned `good` when done, `accent` when active, `critical` when
  blocked, and neutral otherwise. A step neither done nor skipped with done parts takes them as a
  first segment, toned `good`, then its remaining work as a second, toned by the step's status as
  above, when any remains, so the bar fills as the percentage does.
- **Metrics,** in this order: **Time remaining**, the work not yet finished, totalled as
  `execute-task` totals a plan, prefixed `~` because it is an estimate, with any time the user owes
  in `detail` and outside the figure; **Waiting on you**, the count of open questions; **Pull
  requests**, the count of open and draft pull requests, with "<n> open · <n> draft" in `detail`;
  **Elapsed**, measured from the first plan's recorded approval time.
- **Pull request names.** The page names each pull request "PR #<number> - <short title>": a few
  words saying what it does, not necessarily its title, such as `PR #1337 - Migrate admin to
  Tailscale`.
- **Pages.** `Progress` holds the board, the pull requests, the answered questions, the notes and
  any table, in that order. Once step 3 gives the page a pull request to cover, `Architecture`
  follows it, with `layout` `rows`: the diagram, then `changes` "Config changes", then `changes`
  "Migration changes", then an `outline` "What changed in <pull request name>" for each pull request
  it covers, then an `outline` "Keep in mind".
- **`board` "Work"**, four columns, with Up next and Done setting `page_size` 5 so each shows five
  cards at a time:

| Column | `tone` | Cards |
| --- | --- | --- |
| Waiting on you | `warning` | Each open question: `title` the question, `detail` "Recommended: <recommendation>", `tag` "Question". |
| In progress | `accent` | Active and blocked steps: `detail` the step's note, `tag` "<plan title>" plus " · blocked" when blocked, `meta` its estimate, adding "· <done> of <n> parts" for a step with parts, counting parts not skipped. Each question whose evidence is still owed: `title` the question, `detail` the evidence being gathered, `tag` "Question". |
| Up next | — | Steps not started, in plan order, with `tag` and `meta` as above. |
| Done | `good` | Finished steps, `meta` their measured duration. |

- **`diagram` "Architecture diagram"**: one diagram covering every pull request the page covers, so
  an arrow can run from one pull request's code to another's. `prs`: each pull request, `ref` its
  name and `url`. `nodes`: the modules, services, skills or files the pull requests add, change or
  remove, each with `pr` naming the pull request that changes it and `change`, plus the unchanged
  parts they connect to, without either; `label` the name a reader finds in the code and `detail`
  its role in a few words. `edges`: the calls, reads, writes and data that pass between them,
  `label` what passes and `change` when a pull request adds or removes the connection. `steps`: how
  the change works, in order, one sentence each, with each step's number on the arrows it describes.
  Keep to the boxes the explanation needs, a dozen at most.
- **`links` "Pull requests"**: each open and draft pull request, leaving out merged and closed
  ones, which need nothing more from the reader. `label` its name, `url`, `detail` "<owner>/<repo>"
  and the checks and review state just read, `state` its `open` or `draft`, and `status` and
  `tone`: Open `good`, Draft neutral, and Failing checks `critical` in place of either when the
  head's checks fail.
- **`questions` "Answered"**: each answered question with the user's `answer` in their words and
  `meta` the time it was given.
- **`notes` "Decisions and notes"**: each recorded decision and each assumption made without the
  user, labelled as an assumption.
- **`table`**, only when the ledger holds tabular facts worth a grid, such as checks per pull
  request head.
- **`outline` "What changed in <pull request name>"**: the pull request's changes grouped by the area
  they touch, such as `Admin sign-in` or `Admin site`, with moves and renames last under
  `No behaviour change`. Each item's `title` says in a few words what now happens, and its `detail`
  how and why it matters in one or two sentences a reader follows without the diff.
- **`changes` "Config changes"**: each value the application reads while it runs that a pull request
  adds, changes or removes, such as an environment variable, a settings field or its default, a
  feature flag, a secret it reads, or a key in its configuration file. A setting only CI, a workflow
  or a deployment pipeline reads stays out — a GitHub Actions input, a workflow variable, a job's
  timeout. `name` the name a reader sets, `change`, and `detail` "<pull request name> · <its default
  or new value> · <what the user has to do, or Nothing>". A secret is named, never its value.
- **`changes` "Migration changes"**: each database migration a pull request adds, changes or
  removes. `name` the migration's file or revision, `change`, and `detail` "<pull request name> ·
  <what it does to the schema or stored data> · <what the user has to do, or Nothing>".
- **`outline` "Keep in mind"**: what a reviewer or the user needs before relying on the change —
  risks, limits, the order the pull requests merge in, anything a merge or deploy needs from the
  user — grouped by when it applies, such as `Before merge`, `Before deploy` and `After deploy`.
  `tone` is `critical` for what breaks something if missed and `warning` for what needs an action.
- **`references`**: each pull request in every form the page writes it — its name,
  "<owner>/<repo>#<number>", and "#<number>" when no other pull request of the task shares the
  number — with its `url`, so every mention of it is a link.

Leave out withdrawn plans and questions, and a section with nothing in it, except the board,
which keeps its four columns.

## Guardrails

- Show only what the ledger and the hosts verify. A time is measured only when the ledger holds
  both ends of it; anything else is an estimate and reads as one.
