---
name: progress
description: Show the current task's progress as a dashboard built from the session ledger — its plans, which steps are done, running, next or blocked, percent complete, estimated time remaining, questions waiting on the user, the answers already given, the task's pull requests, a Wrap up page with what is left to get them merged and deployed — readiness, merge and deploy order, deploy needs and checks once live — and an Architecture page with a diagram of how they work, what each changes, the settings they add, change or remove, and what to keep in mind. Use whenever the user asks for progress, status, a dashboard, what is left or what is waiting on them, at any point in a task.
short_description: 'Show the task’s progress as a dashboard.'
---

# Progress

Build the task's dashboard from what the ledger records, never from what the chat still remembers,
and deliver the same dashboard again on every request so the user keeps one page.

## Dependencies
- `session-ledger`
- `list-prs`
- `use-dashboard`

## Workflow

1. **Read the ledger.** Resolve and read the task's ledger through `session-ledger`. A question the
   task has put to the user that the ledger lacks is reconstructed and recorded first, from verified
   task evidence, as that skill's recovery rules say, approved only where the user's own message
   approved it; so is a plan the task put to them in the question carrying the "Approved" option.
   The dashboard never shows a step the ledger does not hold. The figures cover the whole task since
   its first approved plan, so that check spans every plan it has had, finished ones included: a
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
4. **Build the spec** in the shape below, with `updated_at` set to now.
5. **Select the delivery route, then render.** Before invoking `use-dashboard`, choose the
   host's ongoing-work channel when authorized work remains, or the normal reply route for
   standalone reporting. Pass that route to the renderer for its delivery, as a dashboard of session
   work; whether it updates an earlier page is `use-dashboard`'s **Session work** rule. Record a
   new page in a `dashboard` entry with its path and any published link, so the next request finds
   it.
6. **Report and return to the caller.** Through the selected route, send the link or file and one
   line: percent complete, time remaining, and how many questions wait on the user, each the figure
   the dashboard shows. When reporting interrupts unfinished authorized work, carry out the active
   run's saved next action under the global rules' pending-work boundary. A report without
   that action does not complete this step; when an awaited result holds the action, retain that
   owner's wait and resume route.

## Spec

- **Header.** `title`: `Progress Dashboard`. `topic`: the task in a few words, such as "Bulk
  export". `subtitle`: the task's goal, such as "Let admins download a month of invoices as one
  file". It sets no `status`, so the navbar shows no badge.
- **Progress.** A step's work is its estimate, or for a step with parts the estimates of its parts
  not skipped; a skipped step has none. `value`: finished work over all work, across every plan
  that is not withdrawn, where finished work is each done step's work and each done part of a step
  neither done nor skipped. `detail`: "<done> of <total> steps done", counting steps with work,
  adding "across <n> plans" when there are several.
  `segments`: one per step with work, in plan order, labeled with the step's title, `details` its
  status, "~<n> min estimated", then "took <n> min" once done or "<done> of <n> parts done" for a
  step with parts, such as ["Done", "~18 min estimated", "took 21 min"],
  `weight` that work in minutes, toned `good` when done, `accent` when active, `critical` when
  blocked, and neutral otherwise. A step neither done nor skipped with done parts takes them as a
  first segment, toned `good`, then its remaining work as a second, toned by the step's status as
  above, when any remains, so the bar fills as the percentage does.
- **Metrics,** in this order: **Time remaining**, the work not yet finished, totaled as
  `session-ledger` totals a plan, prefixed `~` because it is an estimate, counting only the agent's
  work, with no `detail` for anything the user owes; **Waiting on you**, the count of open
  questions; **Pull requests**, the count of open and draft pull requests, with "<n> open · <n>
  draft" in `detail`; **Elapsed**, measured from the first plan's recorded approval time.
- **Counts.** `counted` is set on the `links` "Pull requests", the `table`s "Plans" and "Ready to
  merge", the `changes` "Config changes" and "Migration changes", and the `notes` "Decisions and
  notes", whose length changes as the task does; no other section is counted.
- **Order.** Every list and table on the page is sorted by a logical key — its group first, then
  merge order, plan order or status — never by when an entry was recorded. The `links` "Pull
  requests", for one, runs repository by repository, the repositories in the order their first pull
  request merges, or by `<owner>/<repo>` when no merge order is set, and each repository's pull
  requests in merge order, then by number.
- **Pull request names.** The page names each pull request "PR #<number> - <short title>": a few
  words saying what it does, not necessarily its title, such as `PR #1337 - Add bulk export`.
- **Pages.** The dashboard's `icon` is `progress`, and its pages run in this order. `Overview`,
  `icon` `overview` and `layout` `rows`, holds the pull requests and the `table` "Plans", in that
  order. `Plan`, `icon` `checklist` and `layout` `rows`, follows with the `tree` "Plan tree", then
  one plan write-up per approved plan, in approval order, and is `locked`, with `sections` `[]`,
  until a plan is approved.
  `Progress`, `icon` `board`, holds the board, the answered questions, the notes and any other
  table. Once step 3 gives the page a pull request to cover, `Architecture`
  follows, with `icon` `diagram` and `layout` `rows`: the diagram, then the `tree` "What each pull
  request changes", then the `tabs` "Change details", then an `outline` "Keep in mind". While the task has an open or draft
  pull request, `Wrap up` comes last, with `icon` `release` and `layout` `rows`: the `table` "Ready
  to merge", the `diagram` "Merge and deploy order", then the `outline` sections "Between merges",
  "Deploy" and "Once live", each only when it has something in it. Its `status` is "<n> need you"
  (`warning`) while anything on it waits on the user — a pull request held on their review or
  answer, or an action under Between merges, Deploy or Once live that only they can take — and is
  left out once nothing does.
- **`table` "Plans"**: one row per plan that is not withdrawn, with the columns Plan, Steps done
  ("<done> of <n>"), Running, Waiting on you and Time left, the summary of what the board shows step
  by step, and `details` holding each row's plan write-up, so a row opens the plan.
- **`tree` "Plan tree"**, with `open_depth` 2: one entry per plan that is not withdrawn, in
  approval order, `label` the plan's title, `figure` "<done> of <n> steps" and `meta` "~<n> min left", or "Proposed" for a plan
  not yet approved; under it one entry per step, in plan order, `label` "<n>. <step title>", `tone`
  as its progress segment is toned, `meta` its status, then "~<n> min" while it is not done or its
  measured duration once it is, and `figure` "<done> of <n> parts" for a step with parts, counting
  parts not skipped; and under such a step one entry per part, `label` its title, `tone` `good`
  when done, `accent` when active, `critical` when blocked and neutral otherwise, and `meta` its
  status.
- **Plan write-up**: the plan as a reader who missed the conversation needs it, from the ledger's
  `plan` entry: an `outline` with `expanded` and `stacked` set, `title` the plan's title and `description` its
  goal, then "Approved · ~<total> min", or "Proposed · ~<total> min" for a plan not yet approved. Its groups, each only when it has something in it:
  "Context", why the plan exists and what it starts from, one item per point; "Steps", one item per
  step titled "<n>. <step title>", `detail` what the step changes and how, `meta` "~<n> min" and
  `tag` its status (Done, Running, Blocked, Next or Skipped) toned as the progress segments are,
  adding "· added by agent" for a step whose origin is `agent`;
  "Decisions", each choice the plan settled with the option taken and why; "Verification", how
  the result will be checked; and "After the plan", what it leaves to the user, such as reviewing
  and merging, never with a time, since the agent cannot know how long the user takes.
- **`notice`**, only while something waits on the user: `tone` `warning`, `title` "<n> question(s)
  waiting on you" when a question is open, and `body` the first open question in a sentence and
  the step it blocks; otherwise, while a step is blocked, `tone` `critical`, `title` "<step title> is
  blocked" and `body` what it waits for.
- **`board` "Work"**, four columns, with Up next and Done setting `page_size` 5 so each shows five cards at a time:

| Column | `tone` | Cards |
| --- | --- | --- |
| Waiting on you | `warning` | Each open question: `title` the question, `detail` "Recommended: <recommendation>", `tag` "Question". |
| In progress | `accent` | Active and blocked steps: `detail` what the step changes, from its ledger entry, `tag` the plan's title when the task has several plans, followed by " · blocked" when blocked, or "Blocked" alone when it has one, `meta` its estimate, adding "· <done> of <n> parts" for a step with parts, counting parts not skipped. Each question whose evidence is still owed: `title` the question, `detail` the evidence being gathered, `tag` "Question". |
| Up next | — | Steps not started, in plan order, with `meta` as above and `tag` the plan's title when the task has several plans. |
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
- **`table` "Ready to merge"**: one row per open or draft pull request, in merge order, with the
  columns Pull request, Checks, Conflicts, Open threads, Waits on and Ready. Checks is "Passing",
  "Failing: <check>" or "Running"; Conflicts "None" or "With <base>"; Open threads the count of
  unresolved review threads; Waits on the pull requests or actions it needs first, or "Nothing".
  Ready is "Yes" only when its checks pass, it has no conflict or open thread, and nothing it waits
  on is left; otherwise it names the first thing missing.
- **`diagram` "Merge and deploy order"**: each open or draft pull request as a node, `label` its
  name, which `references` makes a link, and `detail` its repository, with no `prs` frames; a merged
  pull request another still depends on joins with `change` `removed`, labeled as merged; and each
  environment a merge deploys to, such as a staging or production deployment, as a node with
  `detail` "deploys on merge" or "deployed by hand". `edges` run from a pull request to the one that
  merges after it, `label` what the later one needs from it, such as "its migration" or "its
  published package", and from a pull request to each environment its merge deploys. `steps` say in
  order, one sentence each, what to merge or deploy and what that sets off, each number on the
  arrows it releases; pull requests with no order between them share a step.
- **`outline` "Between merges"**: each action a merge needs done before the next one can go, grouped
  by the step it follows, such as `After PR #119 merges`: repointing a dependency to the branch it
  merged into, regenerating the lock, publishing a build.
- **`outline` "Deploy"**: per environment, what reaching it needs that the pull requests do not
  carry — a secret or setting to set, a grant, a build to publish, a migration to run by hand — and
  what deploying sets off, such as a migration running.
- **`outline` "Once live"**: per environment, what the user can check after it deploys to know the
  change works there, such as a page to open, a job to watch or a log line to look for, each with a
  link where one exists; the agent checks none of it, as the global rules' **A merge leaves no
  deploy work** bullet says. In these three outlines, `tone` is `critical` when skipping the item
  breaks the next step and `warning` otherwise.
- **`links` "Pull requests"**: each open and draft pull request, leaving out merged and closed
  ones, which need nothing more from the reader, with `group_label` "Repository". `label` its name,
  `url`, `group` "<owner>/<repo>", `detail` the checks and review state just read, `state` its
  `open` or `draft`, and `status` and `tone`: Open `good`, Draft neutral, and Failing checks
  `critical` in place of either when the head's checks fail.
- **`questions` "Answered"**: each answered question with the user's `answer` in their words and
  `at` the time it was given, with `page_size` 5.
- **`notes` "Decisions and notes"**: each recorded decision and each assumption made without the
  user, labeled as an assumption.
- **`table`**, only when the ledger holds tabular facts worth a grid, such as checks per pull
  request head.
- **`tree` "What each pull request changes"**, with `open_depth` 2: one entry per pull request
  the page covers, `label` its name and `figure` "<n> changes"; under it one entry per area its "What changed
  in" outline groups by, in that order, `label` the group's title and `figure` the count of its
  items, followed by "Config" and "Migrations" entries when its config or migration changes hold
  anything; and under each area one entry per change, `label` the item's title, or for config and
  migrations the `name` with `meta` its `change` (Added, Changed or Removed). The tree is the map;
  the details are in "Change details".
- **`tabs` "Change details"**:
  the tabs "Code", holding an `outline` "What changed in <pull request name>" per pull request the
  page covers, in the tree's order; "Config", holding the `changes` "Config changes"; and
  "Migrations", holding the `changes` "Migration changes". A tab with nothing in it keeps its entry
  with `sections` `[]`, which the renderer leaves off, so when only one kind of change is left, its
  sections show without a tab bar.
- **`outline` "What changed in <pull request name>"**: the pull request's changes grouped by the area
  they touch, such as `Report export` or `Search page`, never the task itself, with moves and renames last under
  `No behavior change`. Each item's `title` says in a few words what now happens, and its `detail`
  how and why it matters in one or two sentences a reader follows without the diff. Its `links`,
  of kind `diff`, open the diff of each file that makes the change, in the pull request's Files
  changed view.
- **`changes` "Config changes"**: each value the application reads while it runs that a pull request
  adds, changes or removes, such as an environment variable, a settings field or its default, a
  feature flag, a secret it reads, or a key in its configuration file. A setting only CI, a workflow
  or a deployment pipeline reads stays out — a GitHub Actions input, a workflow variable, a job's
  timeout. `name` the name a reader sets, `change`, `group` the pull request's name, and `detail`
  "Default <value>, or New value <value> · <what the user has to do, or No action needed>", with a
  `diff` link to the line in the pull request's diff that sets it. A secret is named, never its value.
- **`changes` "Migration changes"**: each database migration a pull request adds, changes or
  removes. `name` the migration's file or revision, `change`, `group` the pull request's name, and
  `detail` "<what it does to the schema or stored data> · <what the user has to do, or No action
  needed>", with a `diff` link to the migration file in the pull request's diff.
- **Both `changes` sections** set `group_label` "Pull request".
- **`outline` "Keep in mind"**: what a reviewer or the user needs to know about the changes
  themselves before relying on them — a risk, a limit, a behavior that surprises — grouped by area as above.
  What merging and deploying needs or sets off belongs to the Wrap up page, and nothing here
  restates how the work is delivered, such as that a pull request waits for the user's approval,
  stays a draft or runs its checks. `tone` is `critical` for what breaks something if missed and
  `warning` for what needs an action.
- **`references`**: each pull request in every form the page writes it — its name,
  "<owner>/<repo>#<number>", and "#<number>" when no other pull request of the task shares the
  number — with its `url`, so every mention of it is a link.

Leave out withdrawn plans and questions, and a section with nothing in it, except the board,
which keeps its four columns, and the tabs of "Change details", which stay with `sections` `[]`.

## Guardrails

- Show only what the ledger and the hosts verify. A time is measured only when the ledger holds
  both ends of it; anything else is an estimate and reads as one.
