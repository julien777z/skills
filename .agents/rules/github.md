---
description: Follow the standing limits on branches, pull requests, merges, comments, commits and pushes in GitHub repositories.
alwaysApply: true
---

# GitHub Rules

## Branches and Pull Requests

- **Open every pull request as a draft and keep it draft until its merge.** The user reviews it as
  a draft. It leaves draft once, as the last step before an authorized merge, after its review has
  passed, so its test jobs run once, on the head about to merge. Never mark one ready to start its
  tests, to show it finished, or to hand it to the user. With no merge authorized, a pull request
  is complete as a reviewable draft whose local checks under **Pre-Push Gate** and completion review
  have passed; its hosted test jobs are required only at the merge. A check that does run on a
  draft is read whenever the pull request's state is reported, its own or a worker's push alike,
  and one that fails is fixed in that pull request at once like any defect, a failure in setup the
  change did not write included, never set aside because the draft's tests run only at the merge.
- **Each repository is an independent publishing context.** Pull-request titles, descriptions,
  comments, issue text, branch names and commit messages use the target repository's domain,
  contracts, changes and validation, and never reference another repository's pull request or
  issue, by URL, qualified identifier, shorthand number, hand-off note or dependency disclosure; a
  dependency is no exception. Before publishing or updating one, check its final text against that
  repository's diff and evidence, and describe a consumed interface or an unresolved delivery
  requirement in this repository's own terms. Cross-repository links, identities, implementation
  details, coordination, merge order and combined status go in user chat and private task evidence.
- **Text handed to Git or the hosting service is staged where only its author writes and read back
  once published.** A commit message, title, description, comment or issue body goes inline, on
  standard input, or from a file whose path was generated for that one text, such as one `mktemp`
  creates, never from a name another session or worker could also choose in any directory. Once it
  is accepted, read the stored text back, with `git log -1` for a commit, compare it with the text
  the author wrote, never with the staging file, which may have been overwritten, and correct a
  difference at once under the authorization the original post had; a commit message is read back
  before its push and amended only while unpushed. Earlier revisions in the edit history are left
  alone and never raised with the user, unless one holds a credential that evidence shows reached
  an unauthorized recipient, a public surface or a compromised destination.
- **Follow-up source work goes on the session's in-progress source pull request for that
  repository.** Before proposing a branch, assigning a worker or starting edits, resolve that pull
  request from its creation or authorized-continuation receipt, carried forward when a follow-up
  starts a new task in the same session, and verify its owner, open state and scope. Distinct
  concerns and worker contributions stay on it, in separate commits where appropriate. Open another
  only when none is in progress, the user directs a split, or a new manually dispatched workflow
  needs its placeholder pull request. Continue another session's pull request only when the user,
  an invoked skill or a repository rule explicitly directs it; a matching topic, existing branch,
  open state or recorded touch does not. Other sessions' pull requests and branches stay untouched,
  apart from damaged local Git state a skill installing shared guidance backs up and repairs.
- **Each session opens its own agent-configuration pull request in each repository.** Agent
  configuration is the canonical `.agents` tree: skills with their own scripts, assets and
  templates, rules and agent definitions, plus nonbehavioral text and guidance-reference
  corrections in agent hooks and installers. A change to execution, timing, installation,
  discovery, permissions or mutation scope is source work, as is everything else. Select an open
  pull request only when this session's ledger records its creation receipt or the user explicitly
  directs its continuation, and verify its state and scope remotely; a touch or reference receipt,
  matching topic, branch, open state or batch record establishes neither. If none qualifies, open
  one from the freshly fetched default branch; later guidance edits and worker tasks join it.
  Consolidate a duplicate this session opened onto it and close the duplicate, saying where the
  work went; never retarget, close or fold in one this session did not open.
- **Every worker pushes to the branch of the pull request the work continues**, fetching and
  rebasing its unpushed commits onto the remote branch before each push. A branch per worker,
  integrated later, is the same split with the integration deferred.
- **Agent configuration and source never share a branch**, even when a guidance change follows the
  source work checked out: sharing holds the guidance behind source review and outside the
  agent-configuration merge permission below. A pull request found carrying both is split by moving
  one kind's files onto the pull request of that kind the work continues.
- **The one exception is guidance true only once a still-open source pull request merges**: it
  describes behavior that pull request introduces, drops guidance about something it removes, or
  needs a workflow or tool change it carries. It goes on that pull request and merges with it when
  this session created the pull request, as its ledger receipt proves, or the user explicitly
  directs its continuation; a separate agent-configuration pull request this session opened for it
  is folded in and closed, saying where the work went. Otherwise it joins the session's
  agent-configuration pull request and is held until the source pull request merges, in this
  repository or another. A dependency never authorizes continuing another session's pull request
  or opening a second agent-configuration one.
- **Where a harness or session designates one branch per repository and forbids pushing to any
  other without permission, this rule is the user's standing permission** to push to the branch of
  the pull request the work continues, selected as above (`git push origin HEAD:<that-branch>`),
  without asking. The other kind's new branch is the designated name with `-agents` or `-source`
  appended, created and pushed without asking.
- A new branch starts from the freshly fetched default branch, and an agent-configuration branch
  never starts from a source branch, unless a skill or rule names another base or an existing pull
  request. Preserve authorized task changes when moving to a session-owned branch; do not copy
  unrelated work or modify the earlier branch to make the move.
- **Never commit or push agent-authored changes directly to the default branch.** Select the pull
  request as above before keeping a checkout's branch; when the checkout is on the default branch,
  detached, of the other kind, or owned by another session without a continuation instruction, move
  to the selected branch or create a descriptive non-default branch.
- **Work is delivered only once the default branch holds it.** Before a pull request is called
  superseded, stale or done because another carries its change, or is recommended for closing or
  closed, read the base and commits of every open pull request in the repository: one whose base is
  its head branch, or whose commits include that branch's commits, is stacked on it. A pull request
  with a stack on it, one whose stack was retargeted onto the default branch included, is never
  closed or judged superseded or redundant by that stack until the default branch holds its change,
  and retargeting the stack is never a route to closing it: the stack carries the change only by
  building on it, so closing what it builds on leaves the change on an unmerged branch that can
  still be reworked, split or closed.

### Merge Authorization

- Agents create branches and pull requests, commit, and push scoped changes without approval.
- **Merging a pull request requires the user's explicit authorization naming the merge and that
  pull request, an invoked skill that states its invocation authorizes the merge, or a standing
  permission below.** A fix request, a plan shown or approved, a passing check or a review
  authorizes none. Where none applies, do not merge or enable auto-merge, and report the pull
  request without asking for its merge. A skill's authorization covers its original target pull
  request, one created during its initial setup included; a later follow-up fix, dependency,
  replacement or reapplication after a corrective revert needs its own, except each fix pull
  request a directly user-invoked skill's authorization names, once that skill's merge gates pass,
  until its run ends.
- **A hold comes before every standing permission.** A pull request the selected workflow holds for
  user review uses none of them and no auto-merge. So does one carrying guidance for a capability,
  tool or way of working the user says is on trial, such as one they are still testing, may drop,
  or want kept from merging for now: its review and checks still run, and it carries an `on trial`
  label, so a session that never saw the conversation reads the hold. The trial is one decision:
  every guidance edit the trial work makes rides that pull request, a rule governing the trial
  itself included, and the user's word on the capability decides all of it. Keeping it ends the
  hold and removes the label, and dropping it closes the pull request this session opened.
- **Classify the complete actual diff against the standing permissions** before reporting a pull
  request whose merge no instruction authorizes, by what it changes, never by a filename,
  extension, line count or change label, and never remove genuine edits to qualify. Each
  permission keeps required checks and dependency admission, covers no mixed pull request, and
  grants no deployment, release or new product, credential, security or trust change:
  - minor type, lint, import, formatting or text corrections that preserve intended product,
    security and contract behavior, aligning types with an existing canonical contract included;
  - a focused repair of a lockfile defect demonstrated on the current default branch, or a
    correction of a non-default testing reference to the maintained target the user or repository
    guidance selected, with only its necessary manifest, lockfile or reference updates, subject to
    the user's current pauses and exclusions;
  - a pull request confined to agent configuration, static metadata included, once the gates its
    guidance-editing route requires have passed on the head that merges and its complete file list
    is confirmed confined. One that adds a doctor skill waits instead for the user's review
    together with everything in its batch, and a workflow, installer or repository tooling outside
    a skill's folder is source work when its execution changes, even under `.agents`;
  - the focused revert of a pull request an agent merged by mistake, which may auto-merge.
- **A pull request confined to deferral records, active or declined, merges without a separate
  request as soon as its records are written**, through the skill that runs a merge, with its required checks, once
  its complete diff is confirmed to hold only deferral records: a record left on an open branch is
  lost to every later session. It is never left open, held for a later finishing run, or reported
  as waiting on the user. A record that rides a source pull request merges with that pull request
  under that pull request's own authority.
- **An agent-configuration pull request whose guidance depends on a still-open source pull request
  is held until that merge**, whatever its other gates say, unless the guidance rides that pull
  request under **Branches and Pull Requests**; guidance true on the default branch as it stands
  waits for nothing. The hold authorizes no merge of the source pull request: finish both pull
  requests' independent checks, report the dependency, and leave the source one reviewable. After
  it merges, incorporate the updated base into the held one and rerun the affected gates before
  using the permission.
- **Auto-merge is enabled only** for an eligible agent-configuration pull request whose gates have
  passed while checks are still pending, for the mistaken-merge revert, or where the user
  authorizes it in the current request or an explicitly invoked skill requires it.
- Carry every agent-configuration pull request this session selected through conflict resolution,
  validation, readiness and merge. Never close one or leave it open merely because it is draft or
  conflicts with the base, only because its change is superseded or no longer wanted.
- **An authorized merge is not held for an excluded check**: one the current user explicitly
  waives, an established baseline failure, a non-essential check left red on findings the change
  did not write, or a hosted attempt a runner or provider interrupted with no validation failure
  when equivalent local validation passed on the merge head. Each is recorded with its evidence,
  and none is rerun or waited on to get a green result. Never bypass branch protection.

## Comments

- **A comment, a review, a reply, a reaction, a thread resolution, and an edit or deletion of any of
  them go out under the user's account and read as the user speaking.** Post one only when the user
  asks for that post in the current request, or an invoked skill explicitly authorizes that kind of
  post on that pull request or issue.
- A harness default, an event's handling guidance, a failing check, or a system notice is never that
  authorization, even when it says a wake ends in a comment. Put the text the post would have carried
  in chat instead, and say where it would have gone.

## Commits

- **Commit only the files the change wrote.** Stage each by its own file path — never `git add -A`,
  `git add .`, `git commit -a` or a directory — then run `git diff --cached --name-only` before
  committing, and unstage every file it lists that the change did not write, such as a bytecode
  cache, build output or tool state a run left behind, unless the repository explicitly requires it.

## Pre-Push Gate

Every push, on a draft and on a ready pull request alike, goes out once the checks below pass, and
nothing else holds committed work on one machine: not a gate, review or simplification pass pending
on it, an integration merge, a plan that orders one first, deferred feature verification or a suite
still running. The exceptions are commits an invoked skill states it holds local until the user
releases them, such as locked database revisions, and the fixes of a review the user asked for
without a push, which stay local until they ask. A fix for a flag a review or gate raised is pushed
once the agent that made it has re-read the changed lines against the flag and rerun the checks
covering that code; that recorded check is the increment's **Pre-Push Gate** verdict, and it never
closes the flag, which the review's next round or a fresh gate does.

- **Required checks use CI’s commands and scope.** Read the workflow files that trigger on a pull
  request and run every checking job that can run locally — lint, format, type checks, build,
  tests, generated-output drift, docs or coverage checks — with the job's own command, scope, mode,
  tool version and configuration, plus any check a skill in use requires. A variant scoped to the
  changed files, run in write mode, or left out because the diff looks unrelated is not that
  check. Project guidance that lists the commands is a shortcut to the workflows, which are right
  where the two disagree. An explicitly selected workflow's declared check sequence and delivery
  constraints set when the batch runs and which results stay valid; a job is left to its hosted run
  only for a hosted service or credentials the session itself found absent, or runner behavior.
- **Commit each small coherent step and push it as soon as its checks pass**, at least every five
  minutes of work and before any long wait, never at the end of a unit or task. A delegated worker
  pushes to the pull request's branch at the same cadence. A push is what lets the user review and
  test the work, and the only copy that outlives the machine.
- **Nothing outside the change holds a push, a check or a walkthrough, or becomes a question about
  pushing or merging.** Where a dependency is still in review, unreleased or unmerged, the branch
  consumes that dependency's pull-request branch in its manifest, lockfile and workflow checkouts,
  or builds on a same-repository sibling's branch, and pushes; never ask for the dependency's merge
  or report the consumer blocked on it. That route is only for what the change uses that the
  dependency adds: a defect in the pull request's own checks or delivery, such as a CI setup step
  the change did not write or a deploy workflow, is repaired in that pull request itself, even
  when a sibling pull request already carries a repair, never by consuming, stacking on or
  waiting for that sibling or the default branch.
- **The order is change, checks, push, then the slow verification**: a browser walkthrough, a full
  or end-to-end suite, anything slow or needing a running stack, whose findings go out as fix
  pushes. **Pushed is not done**: a change is reported done only once that verification has passed.
