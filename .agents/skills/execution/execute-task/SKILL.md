---
name: execute-task
description: "Always run this. Invoke once, before the first edit, at the start of every task that changes files — including one whose edits sub-agents make, and one that only begins changing files because work turned up a defect — and keep it active until verified completion or explicit user stop or handoff: it applies the repository's product constraints, fixes the bugs the work encounters rather than reporting them, commits each small step and pushes it promptly once its checks pass, keeps session-created source work to one pull request per repository, simplifies and gates the finished task's diff once, checks every outcome it reports, whether its own action or a sub-agent's claim, at the source of truth, and delivers each repository independently. Never invoke it from inside a skill it runs."
short_description: 'Apply repository guidance, fix issues found along the way, validate the diff, and deliver the change.'
---

# Execute Task

Run every change the same way, whether a plan preceded it or the user asked for it in one line.

## Dependencies

- `pre-production` — the target-contract policy for every repository and its data obligations.
- `code-simplify` — simplify the finished task's complete diff before delivery.
- `acceptance-gate` — judge the finished task's complete diff before the pull request leaves draft or merges, and each fix for a flag it raises.
- `generic-push` — keep each repository's publishing metadata independent during multi-repository changes.
- `merge-conflict` — bring in a conflicting or moved base, found when a push is read back, before other work.
- `subagent-selection` — the hand-up a worker without an agent tool uses for an independent step.
- `merge-pr` — mark the finished pull request ready and drive its checks to green at **Completion**.

## One Run Per Task

- Invoke this skill once, at the start of a task, before the first edit. A run stays active until
  the task's outcome is verified complete or the user explicitly stops or hands it off. **Work You
  Have Already Named** retains outstanding items and their next actions through reports, gates and
  interruptions. Nothing in the task re-enters the skill; the run simply has not ended.
- A skill that lists this one as a dependency — `plan-change` does — invokes it once, and the
  skills this one invokes never invoke it back: `pre-production`, `code-simplify`,
  `acceptance-gate`, `generic-push`, `merge-conflict`, `subagent-selection`, and `merge-pr` are
  leaves of this run. A second invocation while one is active does nothing more than continue the
  active run.
- This skill never invokes `plan-change`. Where a task needs a plan, `plan-change` runs first and
  invokes this skill once the plan is approved.
- A read-only task — a question answered from the code, a listing, a report with no edit — does
  not run this skill; a task whose edits sub-agents make is not read-only for the agent that
  delegated them. A read-only turn does not close an open run either: a run still holding named
  work stays active through such a turn, and that turn moves its items.

## Task Authorization

- Carry the user's authorization for the task through its ordinary implementation, verification,
  scoped external changes, retries, recovery, and cleanup. A follow-up, interruption, failed attempt,
  or context reset does not require the user to approve those sub-steps again.
- Treat merge, deployment, publication, and release as separate outcomes outside the ordinary
  scoped external changes above. "Implement this plan" is not an explicit instruction for any of
  those outcomes, even when the plan names the action and target. Before acting, identify the
  user's separate explicit instruction for that action and target or applicable guidance or an
  invoked skill that expressly authorizes it; otherwise complete the reviewable work and leave
  that outcome pending.
- Ask only for a decision that materially changes the authorized target, recipient, or outcome, or
  for an action-time confirmation a platform actually requires. Make that question specific to the
  new decision or action; never ask the user to reconfirm the task or say "continue" to resume it.
- **A question the guidance already answers is not the user's to answer.** Before a question goes
  out, and again each time one carried from an earlier turn, a note or a summary would be put
  again, read the rules and the repository's project guidance governing its subject; where they
  decide it, act and report what was done. The class: whether to delete, reset or recreate a local
  resource, such as a cache volume filling the disk or a database stuck on a migration the branch
  has since regenerated, and whether to reset or reopen local records to reach a state, such as a
  test account back at its first sign-in, both of which the global rules give the agent; what a
  data change owes records already stored, which project guidance says; which of two
  implementation details to use where a rule picks one; and what configuration exists or how it is
  scoped, which is read where it lives. A permission denial leaves the decision where it was, as
  **Environment Refusals** says.
- Apply the global rules' **Task execution and authorization** decision boundary before choosing
  an encountered issue's remedy, including one proposed by a worker or reviewer. An ambiguous
  instruction has no approved interpretation: name both concrete outcomes and build on the
  user's answer, quoting their words in a delegated brief. This decision wait holds only the
  dependent remedy, never the remaining authorized work.
- An implementation constraint is not a new approval boundary. Exhaust authorized ways to
  complete a sub-step yourself. Do not mistake an action-time confirmation for a mandatory user
  hand-off: after the user confirms the specific pending action, perform it yourself. Hand off only
  when the platform requires the user's own interaction. Never request a secret through chat.
- After a required confirmation, continue the remaining authorized work without another general
  approval request. A refused or unanswered confirmation blocks only the action it governs, as
  **Work You Have Already Named** says of every wait.

## Browser Access

- Use the user's `@Chrome` browser for browser work unless the user names another browser. When
  the user explicitly selects an existing tab or window, use only that authorized surface;
  otherwise create a new task-owned tab before any page read or action. Retain its handle or stable
  ID and keep actions bound to it under the global rules' tab-ownership procedure. Keep a new tab
  in the background when supported; tab isolation does not require another profile or account.
- When attaching a browser CLI to an existing browser, create and select the task tab first, or
  select the existing surface the user explicitly authorized, before commands that navigate or
  inspect the current page. A named CLI session alone does not establish tab ownership.
- For the default Chrome route, if connected tab control is unavailable, use regular Chrome with
  the same surface-selection requirement above. It may come to the foreground. Continue through an
  appropriate API or CLI when that is more direct. Report a browser-specific blocker only when the
  authorized browser's normal recovery paths cannot complete the required interaction.

## Environment Refusals

- **An environment refusal is a route to find, not a blocker to report.** A repository missing from
  the session is attached or cloned as a writable checkout; a host the environment refuses is reached
  through a path it does serve, and a tool that took the refused path is fixed to take the served
  one. Report a blocker only once every served path has been tried and has failed. A command a
  permission check refuses falls under the next bullet instead, even when it targets a host.
- **A permission check is not a route to find: what it refuses is not attempted again, and the
  decision never becomes the user's.** Use the owner's own routine tool from the start — a package
  manager's cache-clean rather than a raw delete of its cache directory — because that is the
  ordinary way to do the job, not a workaround. Once a permission boundary refuses an action,
  whether a rule the user set or an automated safety check, that outcome is not attempted again by
  any other command, tool or wording, and every other piece of work carries on. Report the refusal
  once, plainly, as a permission the user can grant: what was refused, and that it runs once
  allowed — "The permission check blocked `<command>`; it runs once you allow it, and everything
  else is done." Whether the action is wanted was settled by the guidance before the check ran, so
  the report never asks it or offers options: "Delete X? Yes or no" is the defect.

## Product Constraints

`pre-production` is active in every change task. Read it completely, explicitly invoke it, and
announce the invocation before the first edit. Listing it as a dependency is not an invocation.
Read the repository's product state from its project guidance before choosing how to change a
contract or stored value.

Before each edit, read the shared and repository rules governing every surface it reaches — its
language, framework and package, and the kind of thing it changes, such as a form, a query, a test
or interface copy — and nearby analogous files. Where those files disagree, the one departing from
the rest, or from the mechanism that owns the concern, is an encountered issue to fix, never the
pattern to copy. That holds at every point new instructions arrive, not only at the task's start:
a correction, a fix step or a resumed brief that sends the work to a surface whose rules the run has
not read has them read before it is acted on, and having worked in the same language or package
earlier in the run is not having read them. Match the analogous files' code grouping and spacing in
every new or substantially edited file; inspect the complete result beside those siblings before
delivery. A formatter passing is not a substitute for that comparison.

## Encountered Issues

Apply `pre-production`'s encountered-issues policy while making the change. The rules below govern
how those issues are handled.

- **A bug the work turns up, or a finding a gate, review, or simplification pass returns, is fixed
  in the change in flight, in a shape the standing guidance allows as the next bullet says, and
  offering it to the user is not a disposition.** "Want this handled, or shall I leave it?" reads as
  diligence and is the failure this section exists to prevent: it spends a turn to obtain permission
  for something already required, and a no leaves a known defect in the tree with the agent's name
  on the decision. The question that is genuinely the user's is about a **product change** — what a
  feature does or presents, what a record keeps, who a surface serves, a contract a consumer outside the user's
  control speaks — never whether an encountered issue gets fixed.
- **An instruction one agent passes another — a brief, a correction, a review finding, a gate's fix
  step, a note or summary an earlier turn left for a later one — is checked against the standing
  guidance before it is sent and again before it is acted on**, because it never outranks that
  guidance, as the global rules' **Task execution and authorization** says. Each side reads every
  item against the rules and skills governing the surface it changes — the language, framework,
  copy and testing rules, and the skills the worker runs — opening them at that moment where it has
  not read them yet. The class is any item asking for what a rule rules out: a review finding
  asking for the catch-all exception handler the language rule bans, a brief telling a worker to
  skip a check a skill requires before a push, a correction asking for copy the copy rules forbid,
  one asking for a boat-rental waiver to arrive filled in from the renter's last booking when the
  forms rule says a form someone attests to starts empty.
  - **The agent writing it** rewrites an item a rule forbids into a shape the rule allows, or drops
    it where none exists. One the user asked for in their own words goes out with those words quoted
    and the rule they set aside named; a rule the agent thinks is wrong is put to the user, never
    overridden by an instruction.
  - **The agent receiving it** carries out every other item. For the forbidden one, it fixes the
    defect the item names in a shape the rule allows, where one exists, and leaves only the
    forbidden shape undone. It names that item and the rule it breaks to the sender, through the
    next hand-up or report, and neither implements nor drops it silently. Only the user's own
    words, quoted, with the rule they set aside named, override it.
- **Where a defect came from is never asked, and the fix never waits on it.** Being found rather
  than assigned, predating the change — older code in a file the work touches, a gap a gate labels
  pre-existing — or being the change's own doing changes nothing about whether it is fixed or where:
  the fix lands on the branch in flight. "Is this the change's doing or pre-existing?", "was it
  already there?", "is it a regression of earlier work?" — put to the user, a gate, a reviewer, or a
  worker — have no answer that changes that, so the question only holds the fix behind it, and a
  defect reported as under investigation is reported instead of fixed. The agent that sees it
  starts the fix in that turn, itself or through a worker's brief; where history would help write
  the fix — a lost commit to restore, the change that broke it — read it from version control while
  fixing. Origin decides one thing in this guidance: whether an authorized merge waits on a failing
  check, under the GitHub rule's **Merge Authorization**. That decides only when the merge happens;
  the failing check is still an encountered issue, fixed under `pre-production`'s red-CI rule. Say
  in the report what was fixed and why it was in the path of the work, so the reviewer sees a
  decision rather than a surprise.
- What puts a **new** issue in that path is an act the work performed: a file it opened, a command
  it ran, a check it read, a review it received, and anything it looked at — a screenshot or
  recording, its own or a worker's, a walk through the product, a log, a report. A defect seen there
  is found exactly as a failing test is. How far the fix then reaches is a different question, and
  `pre-production`'s **Scope Follows The Defect, Not The Request** answers it.
- Never reject a fix solely because it is described as high risk. Assess its expected net effect,
  concrete failure modes, and available validation instead of treating the label as a stop rule.
- Fix and verify a non-defect improvement when the correction can be completed in one focused pass
  and produces an overall net gain: removing a code smell, simplifying the implementation, or
  applying the target-contract policy from `pre-production`. A defect, or a finding a gate, review,
  or simplification pass returns, is governed above and carries no such condition.
- Delete every piece of confirmed dead code encountered during implementation, even when it sits
  outside the files or packages already being changed. Confirm that no live application or
  library consumer, public export, or external contract still depends on it, judged where the
  change will land as `code-simplify`'s rubric says; remove tests that exist only to exercise the
  dead code; and validate the affected behavior. This requirement does
  not turn implementation into a proactive dead-code audit of the whole repository.
- Use the repository's relevant tests as the regression guardrail; do not preserve a defect solely
  because an existing test asserts the old behavior. When coverage is absent or insufficient, use
  the strongest available validation and account explicitly for the uncovered behavior.
- One focused pass means the correction needs no separate research or design phase and is not
  expected to require multiple implementation iterations.
- Apply an owned API, protobuf, schema, payload, or stored-shape change selected by
  `pre-production` without a second approval; update every consumer the user controls, in
  whichever repository it lives, plus every generated artifact and required migration for the
  target contract.
- Apply **Task Authorization** to encountered corrections. Ask only when the correction is a product
  change as the first bullet defines it, changes security or disclosure posture, reaches a
  repository, environment, or external recipient the task did not authorize, or a platform requires
  action-time confirmation. Another file, component, or package in the same repository is never a
  new target, and neither is a repository the user owns that consumes a contract the change breaks:
  it is delivered under **Multi-Repository Delivery**. The obligation to fix a bug or returned
  finding remains; apply **Task Authorization** to its remedy rather than treating the finding
  as permission for an unsettled product choice. Continue independent authorized work while that
  choice waits, and never ask whether the defect should be ignored.
- When asking, state the trigger, impact, expected work, recommendation, and concrete choices.

## CI Gates And Deliberate Breaks

Some required checks exist to detect deliberate changes: contract compatibility, schema
compatibility, generated-output drift.

- Such a gate going red is an accepted, reported outcome of an intentional break, never a reason
  to reshape the change.
- Never weaken the gate to recover green: no ignore lists, no exception entries, no reserved
  placeholders faking compatibility.
- Report it instead. State in the pull request that the break is deliberate and list exactly what
  the gate reported, so a reviewer can confirm nothing unintended is in the diff.
- Do not let a green run drive design. Choosing a wider or additive shape so that a gate stays
  green is the same defect as suppressing the gate.

## Ongoing Simplification

Read and invoke `code-simplify` once across the finished task's complete diff, under
**Completion**, never per push.

Own each coherent feature through integration: the primary agent settles dependencies, product
decisions and the combined result. Simplify a feature as it is built; the final `code-simplify` pass
still covers the complete diff. Assign a worker an independently owned scope with a concrete
boundary and return condition, not an arbitrary slice of the primary agent's feature. Keep cleanup
found in a feature with that feature; schedule independent cleanup beside other work when ownership
does not overlap. When cleanup crosses an interface or repository, bring its producer and consumers
to a coordinated checkpoint, verify compatibility at both ends, and keep the cleanup named until
that check passes. Neither a slower dependency nor unrelated work drops an encountered issue from
the task.

- Every pass covers three things, never the diff hunks alone: the **changes** themselves, the
  **similar code** they resemble, and the **sibling modules** around them.
  - **Changes**: the full contents of every file the task has touched so far, not only the lines
    edited in the current batch.
  - **Similar code**: every other place in the repository already expressing the same concept,
    shape, or operation as the changed code — a near-duplicate helper, a parallel implementation,
    a second representation of one value. Search by concept and by key operation, not by filename;
    a sibling-only read cannot find the canonical implementation another package owns. Where the
    change and the code it resembles should be one thing, make them one thing.
  - **Sibling modules**: the other modules in each changed file's package, which is where a
    misplaced piece of logic and its rightful home become visible together.
- When simplification or dead-code deletion changes another file, add that file's full contents,
  its similar code, and its sibling modules to the scope recursively before continuing.
- Resolve the final pass the same way, from the complete diff.
- Apply every simplification that produces an overall net improvement, using `pre-production` for
  contract decisions; ask only about one that meets **Encountered Issues**' condition for asking.

## Pre-Push Gate

Every push goes out once the pre-push checks below pass, on a draft and on a pull request ready for
review alike; nothing holds committed work on one machine. `code-simplify` and `acceptance-gate`'s
diff question do not run per push: they run once over the finished task's complete diff, under
**Completion**. A fix pushed for a flag a gate or review raised gets one fresh `acceptance-gate`
run over that fix's increment, read with the whole branch diff as its originating diff, as
`acceptance-gate`'s **Bounds** require; that fresh verdict is what other skills mean by an
increment's **Pre-Push Gate** verdict.

Read the shared testing rule before planning test runs or briefing an implementation worker.
Its **Verification Cadence** governs tests, builds, browser walkthroughs and reviews, including
pre-push checks. Deferred feature verification does not hold an intermediate push and remains
required afterward. Run the relevant batch after the feature is complete, then the required final
checks before delivery; retain evidence that the change has not invalidated.

**A check's report starts a repair decision, not a design specification.** Before choosing or
accepting a remedy, name the underlying defect, its existing owner, and the guidance governing that
owner. Compare the proposed remedy with fixing that owner directly: what cause disappears, what
behavior remains verified, and what structure the remedy adds. Reject a remedy whose only benefit
is changing what the check sees while leaving the cause in place; choose the compliant root-cause
repair instead. Apply this comparison to a worker's fix, a configuration or validation change, and
a proposed completion claim as well as code. A passing check does not close the issue until the
repair satisfies that comparison; keep it open under **Encountered Issues** when it does not.

- **Required checks use CI’s commands and scope, at the verification checkpoints above.** Read
  the workflow files that trigger on a pull request and run every checking job that can run
  locally — lint, format, type checks, build, tests, generated-output drift, docs or coverage
  checks — with the job's own command and scope, plus any check a skill in use requires. Do not
  restart the batch for each push; retain results whose code and inputs remain unchanged. Project
  guidance that lists those commands is a shortcut to the workflows, never a
  substitute; where the two disagree, the workflow is right. A job that needs a hosted service or a
  running stack, or is too slow to run before every push, joins the slow verification below and is
  named in the report.
- **A local variant of a CI check is not that check**, and each of these passes locally and fails
  in CI: lint or type checks scoped to the changed files, where CI's whole-tree run finds an import
  another change left unused in a file the branch never touched; a formatter or linter in write
  mode, which rewrites what CI's check mode reports; a tool at a version or with a config other than
  the one CI resolves; a job left out because the diff looks unrelated to it, such as a
  generated-output drift check or a whole-tree check that every shared component has a docs page.

Before each push, list the exact adjacent line pairs where setup, a guard, transformation, side effect,
or return meets the next phase without the blank line required by the global code-layout rule.
Fix every listed boundary in the complete changed files; an unrelated bug or a passing formatter
does not satisfy this spacing check.

- **Commit each small coherent step and push it as soon as its checks pass**, and at least every
  five minutes of work — a function and its callers updated, a test brought to pass, one finding
  fixed — never at the end of a unit or task. A push is what lets the user review and test the work, and the only copy that
  outlives the machine: a recycled container or an ended session takes every commit and edit no
  remote holds.
- **Nothing outside the change holds a push or becomes a question about pushing.** A dependency
  still in review in another repository, an unreleased package version, a sibling pull request not
  yet merged, CI expected to stay red until one of those lands: the branch consumes the
  dependency's pull-request branch, or its default branch once merged — in the manifest, the
  lockfile and any workflow checkout, as the global rules' version-reference bullet allows while
  developing — or builds on a same-repository sibling's branch as the GitHub rule's branch bullets
  set out, and pushes. Which branch it consumes, and a red check that dependency explains, are
  reported in user chat rather than waited on, never in the pull-request description; switching
  back to the released version is named work for when the dependency merges.
- **No edit sits uncommitted through a long wait outside the checks.** Before the slow verification
  below, a background worker, CI on the pushed head, or a question to the user, bring the work to a
  coherent step, commit it, and push it; the checks' own runs are part of the push, not such a wait.
- **Delegated edits run at this cadence.** A brief handing a worker edits states it, names the
  branch the worker pushes to — the branch of the pull request the work continues, under **Pull
  Requests** — and names the exact files to change, under `subagent-selection`'s **Dispatch**. The
  worker pushes each step once its checks pass and reports the branch and head. The delegating
  agent, which holds the intent statement, reads that head under **Reported Outcomes** and, once
  the worker's task is finished, runs one `code-simplify` pass and one `acceptance-gate` diff
  question over that task's diff, returning what they flag as fix steps for the next worker. The worker ends with nothing uncommitted and
  nothing unpushed, never amends or rebases a pushed commit, and its report names the branch and
  head.
- **Pull requests stay draft while the work runs**, so these pushes start no test jobs, as the
  GitHub rule's **Workflows** section sets up; the tests run once, when **Completion** takes the
  pull request out of draft. A ready pull request the task resumes changing goes back to draft
  first, as the GitHub rule's **Branches and Pull Requests** says.
- **The order is change, checks, push, then the slow verification**: a browser walkthrough, a full
  or end-to-end suite, a run against a service without the change, root-causing a failure seen
  along the way — anything slow or needing a running stack. What it finds goes out as fix pushes, each once its checks pass.
- **Pushed is not done**: the change is reported done only once that verification has passed.

## Reported Outcomes

An outcome is what its source of truth shows, never what an action or a worker said about it.

- **After any action that changes shared state, read the resulting state before reporting it or
  starting the next item.** A push, merge, deployment, migration, or refresh reports that it ran,
  not the state it left, so read that state where it lives. After a push, that is the pull request
  on the pushed head, or, before one exists, the remote branch head: its mergeable state and the
  checks that run for its state starting — a draft starts no test jobs — since the base can move
  while the push runs.
- **Whatever that read shows wrong is the next thing done**, ahead of every queued item, and is
  never carried to "the next push" or bundled behind other work. A conflict or a moved base is
  brought in through `merge-conflict`, delivered under the **Pre-Push Gate**, and read back.
- **A delegated worker's report of an outcome is a claim, never evidence.** Before relaying it or
  building on it, check it at its source: "tests pass" against the run or the CI result on that
  commit, "pushed" or "exists" against the branch, "merged" or "refreshed" against the default
  branch or the installed copy, "deployed" or "healthy" against the host, "fixed" by reproducing it
  or reading the evidence, "the screenshot shows it" by looking at the image, "no references
  remain" by searching. A claim the check contradicts is the next thing done, ahead of queued
  work: sent back to the worker with what the read showed, or fixed here.
- **A deferral inside a report — "I'll do X next" — is named work of this run** under **Work You
  Have Already Named**, tracked until done; the report does not close it.
- **A status sent to the user states what was just read and where**, never what was reported or
  expected: conflicted, failing, running, or passing, on the head or target named. "Done" or
  "ready" is written only when that read says so, and a file sent with it is checked first as the
  global rules' **User-Facing Output** requires.

## Pull Requests

The GitHub rule's **Branches and Pull Requests** decides where each piece of work lands: new work
joins the open pull request of its kind that the work continues, whichever session opened it, never
one per task, worker or brief, stacked or not, and a pull request the session did not open keeps its
base and stays open. A guidance change never rides the source branch in flight, however closely it
follows that work. List a repository's open pull requests, not only this session's, before creating
any branch there, and say in chat what was consolidated when a stray one is folded in.

## Multi-Repository Delivery

When one change spans multiple repositories, treat each repository as an independent delivery
context, with **Pull Requests** applying inside each of them.

- Invoke `generic-push` separately for each repository before committing or publishing.
- Write every branch name, commit message, pull-request title, pull-request description, review
  comment, code comment, and repository-local report solely from that repository's perspective.
- Do not name, link, describe, or explain another involved repository, its branch, pull request,
  implementation, or coordination context in those artifacts.
- Keep cross-repository coordination and combined status reporting in user chat.

## Each Repository Speaks Only Its Own Vocabulary

The delivery rule above governs the artifacts around a change. This one governs what goes **inside**
it, and it binds in every repository the run touches whether or not that repository's own rules say
so — a repository with no independence rule of its own is the one most likely to be given another's
words.

**Never write another repository's nouns into this one.** Its product name, its services, its
skills, its tables and columns, its record types, its routes, its identifiers, the words its
business speaks: all of them stay where they are. That holds in source, tests, fixtures, sample
data, error messages, comments, and documentation alike, and it holds hardest in a library or a
tool, where every reader is a different consumer who has never heard of the repository the author
happened to come from.

**An example is where this fails, because an example needs a name and the author has one to hand.**
Documenting a folder layout, a config key, a path shape, or a call, the concrete thing the author
just saw is the nearest name and the worst one: it reads as this tool's own vocabulary to everyone
after them, and it goes stale the moment that other repository renames it. Invent the name instead.
An example naming a real artifact of another repository is the defect, however accurate it is.

Name things for the shape being demonstrated, never for whichever caller prompted the work. A
consumer's needs are a legitimate reason to build something and never a reason to name it after
them. Describe the target repository's own contract and behavior to reviewers; keep
consumer-specific coordination in user chat, following the Multi-Repository Delivery rule above.

Where this run touched more than one repository, sweep for it before delivering: search each
repository for the distinctive nouns of the others it was worked on beside, and read what comes
back. A borrowed name is invisible to the author precisely because it was familiar.

## Work You Have Already Named

**Naming work as next is a commitment, and it stays this run's obligation across every later turn**
— including a turn whose own request changes no files, which would otherwise not run this skill at
all. The run that named the work owns it until it is done, and naming it is what keeps the run open
under **One Run Per Task**.

**A new request, an interruption, or a context summary cancels none of it**, and the work each one
displaces is named work whether or not a report named it: an approved plan short of its last entry,
commits a remote lacks, a checkout left mid-edit. The turn that serves the new request also moves
it — the user asking about something else is not the user withdrawing what they asked for before.

- **Write it down before anything else starts.** The displaced work goes into the session's task
  list, with its next step, before the first step of whatever displaced it.
- **An interruption pauses the step in flight; it never ends the run.** After a follow-up
  finishes, restore the displaced task as the in-progress item in the session's task list and
  execute its saved next step without waiting for "continue". A promise to resume is not that
  step. Completing
  its own delivery — including a guidance merge and refresh, a diagnostic answer, or a local
  environment repair — does not complete the surrounding task. Report that intermediate result
  while continuing. A held item keeps its saved next action; repair, resolution and waiting follow
  the global rules' **Tools and environments** boundary. End only when the task is verified
  complete or the user explicitly stops or hands it off.
  "Continue", or anything meaning it, resumes exactly the paused step and is never answered with
  nothing.
- **A context summary's pending list is this run's named work**, not background. The first turn
  after it moves the oldest item as well as whatever the summary's next step names. A constraint it
  carries, such as "ask before X", is an earlier turn's instruction, checked under **Encountered
  Issues** before it is obeyed.
- **Commits a remote lacks are undelivered work**; their next step is the pre-push checks and the
  push. A hook or status line counting unpushed commits whose checks pass reports a push owed now,
  not something to explain.

**The failure is a report, not a refusal.** It reads as diligence: the item appears under "still to
do", the turn ends, the next message arrives, and the item appears again, unchanged, in the next
report. Nothing was declined and nothing was done, and each repetition makes the next one easier,
because the item now looks like a standing note rather than work somebody is waiting for.

So the test is the item's own line. Before a report goes out, compare each outstanding item against
the line the last report carried for it. **A line that has not changed means the item is finished in
this turn, before the report is sent** — not moved a little, and not dropped from the list, which
is the same failure with the evidence removed.

Each item's line records its current disposition:

- it is done;
- a named gate holds its dependent action — including an unanswered question or missing
  authorization — with its evidence, saved next action and live repair, resolution or wait route;
- it is no longer work, because the user withdrew it or a later request superseded it, said with
  that reason.

A held item remains outstanding; naming its gate or reporting it does not end the run. Withdrawal
or supersession removes only the work the user's instruction actually cancels.

**A wait blocks only the work that depends on what is awaited.** While one item waits on something
outside the run's hands — a background agent, CI, a review, a build, the user's answer to one
question or confirmation — start the authorized, already-named work that neither needs the awaited
result nor touches the files or resources the awaited work is changing. Each item held for the wait
names what it uses that only the awaited result will supply, and one with nothing to name starts
now: coming later in the plan, belonging to the same feature, or consuming a shape already agreed
with the awaited work, such as a planned contract, is not such a thing, so build against that shape.
When the awaited work is a building worker, another edit starts only in an independently owned
scope with separate files and resources, under `subagent-selection`'s **Dispatch**; otherwise do
read-only verification, review or question preparation while it runs.
A status report is not a stopping point. When every remaining item depends on an awaited result,
apply the global rules' **Tools and environments** pending-result boundary: keep the available
wait or event route active and resume the saved next action when it resolves. An unresolved user
choice holds its dependent remedy; it does not close the run or cancel independent work. A guidance
correction is an intermediate checkpoint under the same boundary, never a reason to end the
surrounding task. Report a blocker only on that boundary's concrete evidence.

## Completion

Before the final delivery steps below, verify the requested behavior on the change's branch within
the authorized scope, including reachable dependency branches. When a requested flow failed, repair
and push the fix, exercise that branch, and repeat the complete failed flow until its requested
outcome is verified. A narrower health check or passing component test cannot replace that flow.
Missing merge approval holds merging, never this branch verification; check the available branch
route before declaring a gate. Merge is delivery after verification, never its prerequisite.

Then take each pull request the task changed out of draft — once, with its work finished — and close
the run:

When the task uses several independent final reviewers outside `code-review`, assign distinct
concerns across the complete result rather than asking each the same question. After a repair,
rescan the affected ownership area and consumers, retain valid evidence for unchanged areas, and
return only invalidated review scopes to their reviewers. `code-review` owns this assignment and
rescan within its own invocation.

1. Run the final `code-simplify` pass across the complete pull-request diff and push its
   simplifications through the **Pre-Push Gate**.
2. Put the complete pull-request diff to `acceptance-gate`'s final-acceptance question with the
   intent statement. Push the fix for each flag as its own increment and put it to the fresh gate
   that skill's **Bounds** require; a second flag is decided under those **Bounds**.
3. Invoke `merge-pr` with the accepted head, merge withheld unless **Task Authorization** finds
   that merge authorized, and the **Pre-Push Gate** each fix is pushed through as its fix rule. It
   marks the draft ready, which starts its test jobs once, reads them back on the exact head, and
   fixes each failure until they pass.
4. Verify every requested outcome and every automatic incidental fix.
5. Confirm tests and relevant validation cover every incidental fix and simplification, and that
   intentional contract changes are reflected in the expected behavior.
6. Confirm multi-repository delivery artifacts describe only their owning repository.
7. Report the implementation, encountered fixes, simplification passes, validation, the pull
   request's ready state and check results, and any unresolved decision awaiting the user.

A workflow that already runs final acceptance runs steps 1–2 as its own; one that already invokes
`merge-pr` runs step 3 as its own.
