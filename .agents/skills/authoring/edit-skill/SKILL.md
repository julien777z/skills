---
name: edit-skill
description: Add or edit anything under `.agents` — a skill, rule, agent definition, hook, setting, reference or project guidance — including when the user points out a mistake in how an agent followed or wrote guidance or questions where guidance was placed. Before proposing or editing guidance, derive the observable failure and test the proposed scope against alternative implementations of it. Write each change for the whole class of failure the request is one instance of, which is the same mistake in every kind of document, file, tool, or step it can occur in, not only the one the request names, the section it says to put the fix in, or the one path that let this instance through. Diagnose and fix the underlying issue and the guidance path that allowed it, even without an explicit request to edit a skill. A correction that encodes a new process waits until that process has worked on the work in hand; every other correction is recorded and written at once, whatever happens to the current work's repair. While another task is active, every correction, a direct request to edit guidance included, is pushed to a draft guidance pull request and recorded, with a generic backup comment there, and the rest of its delivery runs in bulk when that task completes; one arriving while a guidance batch is in flight joins that batch's pull request, which reruns only the checks the new edit invalidates. Use it too when carrying a guidance batch through delivery to its merge or hold. Deliver every behavior-changing guidance edit through `review-pass`, the acceptance gate, and `test-skill` before its pull request merges.
short_description: 'Edit a skill, rule, or agent file and fix the guidance gap that prompted the change.'
---

# Edit Skill

Upsert `.agents` source-of-truth files for agents, skills, or rules based on user input, and carry
every edit through the same delivery whether the user invoked this skill or the edit arose while
doing other work. An edit that skipped this is unverified, and the report says so.

**A process is encoded only once it has worked, and only a new process waits.** A request to put a
new process into guidance — a workflow, a procedure, a tool or route, a way of building or
delivering something — is first carried out on the work in hand and verified to work; the guidance
is then written from that run: the steps and commands it used, what had to differ from the source
that described the process, and what failed along the way. Documentation, a plan, a worker's
proposal or the request's own description of the process is the source to try, never the text to
encode. Every other correction — a gap a guidance failure exposed, a rule the user states — depends
on nothing the current work does: record it and write its edit at once under **Recording During A
Task**, which sets when it is delivered, while the current work is corrected beside it. A problem
the current work meets while it is being corrected is that work's own issue, never a reason to hold
or drop a correction that does not depend on it.

An open `.agents` pull request is not a delivery result. Processing continues through its source
check, required review steps, merge or hold, Agent Sync result, and verification of generated root
instructions and provider output. A genuine gate holds only its dependent step while repair or resolution
remains active.

**A gap you notice yourself starts this skill, exactly as a request does.** Guidance that let a miss
through, a skill whose trigger did not fire when it should have, one that says nothing about the case
in hand, a step you found yourself doing that no skill describes: each is this skill's input, and
noticing it is the whole trigger. Waiting to be told is what leaves the next session to rediscover
the same gap, and the session that hit it is the only one holding the evidence.

The tell is a sentence you are about to write to the user about your own process — that you skipped
a step, that a check did not apply, that you should have done something earlier. Diagnose the route
before the sentence; when it exposes a guidance gap, record and write the correction while the work
is corrected.

**The user pointing out how you work is the same trigger.** "Why did you do it that way", "you
should have done X", "don't do Y again": each calls for correcting the thing in front of you and
checking whether guidance allowed the miss. Record the owning file's correction at once, beside
correcting the work, so the next session does not repeat it.

Correct the current behavior and trace its guidance path in the same turn. Neither the issue nor its
verification disappears when the surrounding task resumes.

A correct instruction does not close a reported failure to follow it. Step 2 traces and repairs the
application step that admitted the rejected decision, then verifies that repair against the miss.
Keep an unknown historical cause unproven; do not replace that repair with a noncompliance report or
another copy of the substantive rule. Where no guidance governs the subject, step 2 creates its
new owner under **Guidance Changes Proceed Automatically**.

## Guidance Changes Proceed Automatically

A user request or an encountered guidance gap, once **Behavior** step 1 confirms its premise,
authorizes the canonical `.agents` correction, except a policy change, which **Behavior** step 2
sends to the user. Do not ask for a plan or for approval of a guidance-output example; an approval
hold the invoking workflow sets is that workflow's and still applies. An example renders the settled
instruction and is task evidence, not a new product experience because a user reads it. A guidance
edit that intentionally changes the product still follows `pre-production`'s **Product Choices**. The
required skill test, review, and acceptance gate validate the correction. When a separate source
task is active, or a guidance batch is in flight, preserve its execution and follow **Recording
During A Task** for the edit's timing.

## Dependencies
- `code-simplify`
- `acceptance-gate`
- `pre-production`
- `test-skill`
- `subagent-matrix`
- `review-pass`
- `merge-gate`
- `session-ledger`
- `update-skills`
- `council`
- `i-have-adhd`
- `share-media`

## Recording During A Task

Honor the selected workflow's verification sequence and any delivery or installation hold when
recording or delivering a batch.
Validate skill dependencies and their actual call and policy-read paths under the [authoring reference](references/authoring.md)'s **Dependencies** and **Validation** sections.

- A correction that encodes a new process waits for that process's verified run, as **A process is
  encoded only once it has worked** says; a method or lesson the work has not yet tried is not a
  correction until then. Every other correction is recorded as soon as its gap is diagnosed.
- A direct request to change guidance, such as "use edit-skill to reflect that", is recorded the
  same way. While another task runs, the requested action is the behavior it describes, applied to
  the current work, and the guidance edit is its record. While a guidance batch is in flight, its
  delivery is that action and the user's words are its evidence.
- Record the correction as a `guidance_correction` entry with `session-ledger`: the user's words,
  where the user gave any, quoted as `pre-production`'s **Examples And Paths** says, the evidence of
  the gap, and for a process its verified run, a reproduction scenario, the intended behavior, the
  canonical files it will change, and `pending` as its `status`. Steps 1–4 of **Behavior** run now,
  while the evidence is fresh, and their result goes into the entry; the edit itself (steps 5 and 6 and
  **Branch and commit**) is written as the bullet on writing the edit below says, and delivery from
  **Run `validate_sources.py check`** onward waits.
- **A recorded correction governs the rest of the session at once**, ahead of the installed text it
  amends. Before a decision a pending entry's subject covers, read the ledger's pending entries and
  follow their intended behavior. Putting a question or a recommendation to someone is such a
  decision, as much as acting is: the entry decides what it carries. Recording a correction and then
  repeating the miss it records is the failure this section exists to prevent. A pending entry may
  restate or tighten the installed text, never grant an authorization the global rules' **Authorization** or the GitHub rule reserves to
  the user's own words: a merge, a deployment, a publication, a comment, or a push to another
  session's branch. A brief to any worker whose task a pending entry's subject covers carries that
  entry's intended behavior, with the user's words quoted and the installed text it amends named.
- Write the edit in the checkout step 4 resolves, on the branch **Branch and commit** selects — the batch's own
  branch while a batch is in flight and its pull request has not merged — commit it, and push it to
  that branch's pull request once the checks the GitHub rule's **Pre-Push Gate** defines pass, opening a draft when the branch has
  none; this holds for a source pull request **Branch and commit** selects as for an agent-configuration one.
  When the checkout holds the active task's uncommitted or source-branch work, write and commit the
  edit from a separate worktree on the selected branch, leave the task's tree untouched, and stage
  only the guidance files. Record the branch, the `commits` list and the pull request in the entry's
  `data`, bring that pull request's description up to date at the milestone, then run `update-skills` at once for eligible edits under its **What Takes Effect**, so the installed
  copy every agent loads, subagents included, carries them. A running agent keeps the text it
  already read: tell each running worker this session started which skill, rule or agent definition changed, each section that changed, and what it now says. Nothing else of delivery runs while the task does: no
  review, gate, skill-test round, merge or worker, except the checks a batch in flight reruns for an edit
  that joined it, as `session-ledger`'s **Guidance Batches** says. A standing instruction about how guidance
  pull requests are reviewed or merged governs that delivery when it runs, never when. A gate result
  that arrives for a guidance pull request already open is recorded as its entry's stage result, and
  its repair waits with the rest.
- **Every `guidance_correction` entry is backed up** as `session-ledger`'s **Backup** section says.
- A related correction recorded before its batch is frozen joins the same entry or sits beside it
  in that batch; the batch is one pull request, apart from edits the GitHub rule puts on a source
  pull request. One recorded while a batch is in flight joins that
  batch, and one recorded after the batch's pull request merged starts the next, as
  `session-ledger`'s **Guidance Batches** says; tell the user which.
- The task's next step is never held by a correction: record it and carry on.

## Guidance Delivery

This route delivers the frozen batch of `guidance_correction` entries its invocation names,
beside the source stream. It holds the source pull request only for the checks its ridden edits
need and the delivery of the batch carrying them; only an edit on that pull request, or one the GitHub rule's **Merge Authorization** holds for a source pull request, waits for that merge. Run it as a delegated worker, at `subagent-matrix`'s standard capability level, when the session can, so the
user's review of the source pull request overlaps it.

1. Read every entry in the frozen batch and resume at its recorded first
   nonterminal stage, rebuilding a lost or truncated entry from its backup
   comment as `session-ledger` accepts it; the comment's existence records that the correction was admitted under **Recording During A Task**, its Intended behavior stands as the recovered intent for step 3 beside the user's words, taken from the conversation where they survive and otherwise named as missing in that intent, never replaced by that paraphrase, and **Run one `test-skill` round**
   rebuilds the reproduction scenario from its failure class and invariant, with anything else
   unrecoverable handled as `session-ledger` incomplete retrieval. An entry with no recorded commit
   applies its edits under **Behavior** steps 5 and 6, on the branch **Branch and commit** selects; one with a
   pushed commit resumes from that head, taking the pull request's current state, tip and diff
   against the base from the host, which override the entry's and the comment's recorded commits
   and delivery stage; a merged or closed pull request resumes at verifying the merged text, never
   at review. An edit **Branch and commit** puts on a source pull request this session drives is pushed there and
   passes **Run `validate_sources.py check`**'s source check on the head carrying it before that pull request's source stream
   proceeds, and **Run one `test-skill` round**'s skill-test round on the head that pull request's review pass accepted, before the source review and delivery. It carries **Check prose duplication**'s checks into that
   pull request's simplification pass and **Brief `review-pass`'s final acceptance**'s incident vocabulary into its final acceptance. An edit **Branch and commit** selects on
   another session's source pull request runs **Run `validate_sources.py check`** through **Run one `test-skill` round** here on the head it pushed, and the
   delivery report says the push moved that pull request's head past its owner's acceptance. An
   edit on either source pull request is recorded as held for that pull request's merge once its
   source check and skill-test round pass, so its batch can be done. The steps below cover the
   agent-configuration pull request.
2. Run **Run `validate_sources.py check`**'s source check.
3. Run `review-pass` once over the batch, naming every head it carries. Give it each entry's recorded
   user's words and evidence as the intent statement, the incident vocabulary for its acceptance
   gate as **Brief `review-pass`'s final acceptance** describes, and **Check prose duplication**'s checks for its simplification pass.
4. Run **Run one `test-skill` round**'s skill-test round once over the batch, naming every head `review-pass`
   accepted, with every entry's
   reproduction scenario as an input and entries that share a failure class grouped into one
   scenario, then **Hold each changed output to its concrete example** through **Read the merged text back before using it**. A guidance repair the skill-test round makes, here or on a source pull
   request under step 1, goes back through `review-pass` over its delta, and the skill-test round reruns
   every scenario `test-skill` does not carry forward, on the head that review accepts.
5. After each completed or failed stage, record its exact head, stage result, and first
   nonterminal next stage in each entry. Resume from that stage without repeating completed work.
   After the skill-test round, record the pull request, its head, the skill-test results and the merge or
   hold. Keep its `status` `pending` while a hold remains, with its concrete dependency and saved next
   action. This route never sets an entry's terminal status.
- Before the surrounding task ends or hands off, every `pending` entry is processed, or carries its
  concrete blocking decision, failed gate or unavailable dependency, with its evidence and saved next
  action. Never lose a correction, treat a recorded one as
  delivered, or hold the source pull request for it beyond the checks its ridden edits need and the
  delivery of the batch carrying them.
- **Delivery is the agent's own work, never the user's errand.** It starts at its own trigger
  without the user asking, and its operational choices — another round, splitting a correction onto
  its own pull request, dropping one, accepting a residual miss — are the agent's, a contested one
  going to `council` in **Ask** mode. No question, report, pending-decision list or note puts such a
  choice to the user or describes a pending batch as waiting on them; one that does is corrected,
  never carried forward. A policy change **Behavior** step 2 sends to the user, dropping it
  included, and a user-review hold stay theirs, the policy change asked through the question tool.
- At a checkpoint and before reporting its state, record the complete pull-request head and file
  list, the target repository's lifecycle, its current state, and its next transition. A draft
  confined to canonical agent configuration records `agent-configuration exception`
  and `merge-gate` as its next action unless the GitHub rule's **Merge Authorization** holds it; it
  never records `await user authorization` otherwise.

## Behavior

1. Validate input.
   - If input is missing or empty, ask: **"What should I add or update in `.agents`?"**
   - **Confirm the request's premise before anything else.** A request often rests on the user's
     reading of what happened: what the agent did, proposed or meant, or what the code does. Check
     that reading against the conversation, the plan or the code. When it is wrong, say so plainly:
     what was actually meant or done, and which existing guidance already covers it. Then stop. Make
     no guidance edit, open no pull request and record no correction, because there is no miss to
     repair, such as a user who asks for a rule against a step the plan never proposed because they
     read its wording as naming something else. When only part of the premise holds, act on
     that part alone. This is different from a real miss that existing text already covers, which
     step 2's causal diagnosis still repairs.

2. Identify the failure class, then its target type and name.
   - **Classify before proposing a remedy or editing guidance.** State the observable outcome the
     user rejected and the invariant a correction must preserve, without using the named component,
     format, file or tool as the boundary. Identify at least two different ways the same outcome can
     arise, including a workaround that obeys the proposed wording but violates that invariant.
     Include a different kind of decision, such as a sentence, quantity or choice, rather than only
     more examples of the same format. Test the proposed scope against those routes before presenting
     it to the user or writing it: if any still allows the rejected outcome, broaden the owning
     decision and remove conflicting permissions first. Keep the incident and these cases in the
     verification record; shared guidance states the invariant, not their identities. This check
     precedes choosing the owner, because a component-specific owner can conceal a broader failure.
   - Supported types: `agent`, `skill`, `rule`.
   - If the user explicitly says the type, use it.
   - If type is not explicit, infer it only when confidence is high.
   - If not confident, ask: **"Should this be an agent, skill, or rule?"**
   - A file or skill the request names is a candidate, not proof of ownership. Compare it with its
     callers and dependencies before choosing the target. A condition governing a specific action
     belongs to that action's skill, even when a broader caller sequences the surrounding task.
     When the owner necessarily runs before the action, remove equivalent conditions from callers;
     strengthen its trigger or invocation only if that owner would otherwise be missed. Explain the
     placement.
   - Read the [authoring reference](references/authoring.md) before choosing an owner, and test the
     candidate against its **Where Guidance Lives**: name the skill that runs when the requirement
     applies before choosing a rule or `.agents/global.md`, and check what the candidate's name and description bound.
   - **When the request names no target, find the guidance that let the gap through and change it
     there.** A request usually arrives as a symptom with no file attached — "that is a bad
     implementation, do not use X" — and the file to edit is the one that governs the thing X
     belongs to: the language rule for a language construct, the review skill for something a
     review let past, the skill that ran for something it did while running. Search the rules and skills by the subject of the request, not by the request's words,
     read what the candidate already says about that subject, and put the change where a reader
     doing that work will meet it, at the breadth the authoring reference's **Writing** asks for. Never ask which file; the search
     is this skill's job.
   - **A violated instruction, or any guidance failure the user points out, calls for causal
     diagnosis and an application repair.** Before editing, trace the actual path from the request
     to the missed behavior, and test the proposed instruction against that path before proposing or
     writing it, as the [edit criteria](references/edit-criteria.md)'s **Causal Diagnosis** says.
     Repair the decision step at its owner rather than restating the substantive rule or ending
     with a noncompliance report, and replay the original decision under the repair before closing
     the issue.
   - Treat a named addition as the starting point, not the limit. Inspect the owning guidance,
     related callers and dependencies for other gaps needed to solve the same issue. Before
     applying those additional corrections, tell the user which gaps you found, what you will add
     and why. Apply relevant guidance fixes without waiting to be invited to think more broadly;
     product choices still follow `pre-production`'s **Product Choices**. **An edit writes only what
     the request and the failure it repairs need.** Two kinds of edit are policy changes, proposed
     to the user with the standing text they would change and written only once the user's own words,
     or an invoked skill's explicit instruction for that change, approve them: a requirement neither the request nor its failure needs, such as a step, a routing
     rule or a hold the request never named; and any exception to, or change of, standing guidance
     the user did not ask to change, however necessary the repair makes it look.
   - **When no existing file of the inferred or selected type governs the subject, create the new
     owner under Guidance Changes Proceed Automatically.** Record its recommended name, scope, and
     behavior in the correction evidence; do not ask for approval. An existing file of that type
     that governs the subject is always edited instead, however thin its current text.

3. Include the underlying issue.
   - When the user raises a concrete issue or provides evidence such as screenshots while requesting agent guidance, update the guidance and implement the underlying product or code fix in the same task.
   - Treat the issue and evidence as requested scope, not merely as background for the `.agents` update.
   - Skip the underlying fix only when the user explicitly requests an instruction-only change.

4. Resolve which repository owns the target, then its path inside that repository's `.agents`.
   - Decide whether the target is shared or repository-owned, and its path for its type, as the
     [authoring reference](references/authoring.md)'s **Where Guidance Lives** says.
   - A shared target is edited in a writable checkout of the skills repository, on a branch and
     pull request in that repository, never through the link's path from another repository's
     branch. The [edit criteria](references/edit-criteria.md)'s **Shared Targets** says which
     checkout that is, and how the edit transfers to a separate skills-repository session and is
     replayed when no writable checkout can be obtained.
   - Never write `.cursor/*`, `.claude/*`, `.codex/*`, or any other non-`.agents` agent or provider folder, and never read one as the source of guidance; **Read the merged text back before using it** reads them only to verify what Agent Sync generated.
   - Do not manually create, update, or sync mirrored command/skill/rule files in those folders; repository automation propagates changes from `.agents` to Cursor, Claude, Codex, and similar targets. This holds with no exception, including where the change leaves a mirror pointing at a path it renames or deletes: the workflow reconciles those on the default branch, and a branch carrying a stale or broken one meanwhile is expected.
   - This path restriction applies to the agent-content update, not to source changes required to fix an underlying issue from step 3.
   - When importing external guidance, inspect its actual entry points and file layout before registering it. If an owned sync tool cannot represent the source, extend that tool for the source's format and register the original content directly. Keep a standalone reference collection standalone: do not invent a substitute skill, relabel its files as skills, or bury it in another skill's references.

5. Upsert behavior.
   - Inventory and read the target entry point and
     its referenced files, scripts, templates, and examples. Follow supporting links within the
     package; reviewing only `SKILL.md` or the edited hunk is incomplete. Apply the same genericity,
     ownership, clarity, and evidence standards to every file.
   - **A change to what a skill returns the user is specified with a concrete example before the
     skill is written to produce it.** The [edit criteria](references/edit-criteria.md)'s **Changed
     Output Examples** says which changes count and how the example is modeled and written. Write
     the skill to produce that shape, then validate it through the required skill-test run, review,
     and acceptance gate; the example is task evidence, not a user approval gate.
   - Trace each miss to the instruction that produced or allowed it, including instructions for
     adding or recording guidance. Name that governing instruction and its replacement in the
     change. Removing a bad example while retaining a directive that regenerates it is incomplete.
     Put incident evidence in the project/verification record and state that destination explicitly.
     Fix the producing instruction and its output together.
   - Move inline criteria to a named reference when the [authoring reference](references/authoring.md)'s **Skills**
     standards require it, and add the appropriate hard-coded output format or delivery report line
     when absent.
   - Validate every added or changed instruction and example for conflicts before delivery. Search the canonical
     rules and skills by its subject, required action and opposite disposition. Read the complete
     changed skill or rule and its supporting files, every file that loads alongside it, plus relevant sections in other skills, rules,
     callers and dependencies. Apply the [conflict criteria](references/conflicting-instructions.md), which name the authoring reference's bullets each change is also held to. Resolve competing instructions
     at their owners rather than adding a reminder beside them; where the new instruction conflicts
     with standing guidance the request did not ask to change, fit the new instruction to the
     standing one, as step 2 says. Record the searches, sources read
     and each resolution, or the evidence for a clean result. Repeat this check for later wording
     changes before acceptance and skill tests; an earlier clean result does not cover a new edit.
   - Update existing files in place and report any structural changes. Before delivery, follow the
     entry point's links again and confirm that each route loads its required guidance. References
     must not hide an essential rule or introduce an unexplained mode or dependency. Check genericity
     with one further case the request never mentioned, a different kind of thing from its examples.
     State that case and its expected outcome in validation. A case the draft would still handle as
     before means the draft only renamed the examples, and it is rewritten until that case changes too.
   - A missing tool the repository needs to run, build, test or review, and a consumer's reference
     to a dependency, follow the [edit criteria](references/edit-criteria.md)'s **Tools And
     Dependency References**.
   - Write every added or changed instruction as the [authoring reference](references/authoring.md) says, under
     each of its sections the edited file's kind and content fall under, **Harnesses** included for anything a harness runs or reads.
   - **Moved text is added text.** Guidance moved between files — a skill relocated, bullets
     gathered into a new rule or out of one — that lands beside a statement of the same requirement
     is merged with it into one in the same change, keeping every distinct criterion and exception,
     and any other defect a standing rule names that the move brings to light is fixed in it, as
     `pre-production`'s **Scope Follows The Defect, Not The Request** says of a defect the work notices, with
     `acceptance-gate` judging the repair's scope and size. Moving text unchanged proves it
     survived; it is never a reason to report a defect as left for the user.
   - Before delivery, audit each edited skill's complete package and its affected callers, every file a folded or incorporated pull request brings in included: list every skill each one refers to, by name or by a description that identifies it, compare them with the owning entry point's `## Dependencies`, and resolve every reverse, peer, missing, stale or path-based reference and any user-only dependency lacking explicit bounded delegation as the [authoring reference](references/authoring.md)'s **Dependencies** says. Check references separately for hidden invocations and cross-skill filesystem links. **Run `validate_sources.py check`**'s source check matches name forms only, so a passing check does not replace this audit.

6. Multi-target behavior.
   - Apply multi-target updates for `agents`, `skills`, and `rules`.
   - When the inferred/selected type is singular (for example `skill`), distribute requested items across multiple files of that type as needed.
   - Update existing files when they already fit part of the request (for example update skill A and skill B).
   - Create a new file of that type when no existing file governs a requested item's subject (for example create skill C), under **Guidance Changes Proceed Automatically**.
   - If one request contains multiple distinct items, map each item to the best existing file or a new file within the same inferred/selected type.
   - If scope is ambiguous, ask a short follow-up before editing.

7. **Guidance Delivery** delivers the batch in this order, with `review-pass` carrying **Check prose duplication** and **Brief `review-pass`'s final acceptance**. Ordinary
   repairs and verification remain authorized throughout this delivery; resolve flagged gates under `acceptance-gate`'s **Bounds** and failing skill-test runs under
   `test-skill`. A pull request confined to agent configuration has merge authorization under the
   GitHub rule after its stated gates, a skill's changed scripts' own checks included, unless its
   **Merge Authorization** holds it; ask neither to repeat that authorization nor to continue an
   ordinary repair, and never record, report or ask for a permission hold by citing the ordinary
   merge default. That merge authority settles no genuine unresolved product, scope, or
   authorization choice: put that concrete choice to the user under **Bounds** while independent
   work continues. It does not authorize a release workflow. A changed output's concrete example, under **Upsert behavior**, is task evidence before writing that output; it does not wait for approval.
   1. **Branch and commit.** Select the edit's pull request under the GitHub rule's **Branches and Pull Requests** — never put it onto a
      source branch, the one checked out included, except guidance that rule puts on the source pull
      request it depends on, which merges with it. Commit the `.agents` files, never a provider
      mirror, and push each step once the checks the GitHub rule's **Pre-Push Gate** defines pass. Open the pull
      request as a draft; it stays draft until `merge-gate` marks it ready as the last step before its merge. **Check prose duplication** and **Brief `review-pass`'s final acceptance** review what no earlier pass covered, and
      **Check the diff file list against the default branch, then merge** merges it. Carry out each authorized transition as it becomes eligible. An
      open pull request leaves the current guidance in use. A source fix required by step 3 is source work: it goes onto the source pull request
      the work continues in its repository under the same rule and merges as that work does.
   2. **Run `validate_sources.py check`**, which sits under `scripts/` beside this skill, before the pull
      request merges, and again whenever the branch changes after that run. Nothing on a pull request runs the sync: the workflow
      runs on the default branch after the merge, so a file it refuses is refused once every session
      is already reading it. The script installs the sync tool at the revision the workflow pins and
      mirrors the canonical tree into a scratch copy, so what its mirror refuses is exactly what the
      workflow would; it also refuses the undeclared skill names and dependency cycles the
      [authoring reference](references/authoring.md)'s **Dependencies** describes. Run it from the root of the repository being edited, with that repository's own
      interpreter or any interpreter meeting the sync tool's version, and fix every
      report it prints before pushing; a description holding a colon followed by a space is the usual
      one, and quoting the value is the fix.
      When the sync tool cannot reach an imported skill's source repository, or the guidance needs a
      change in an unreleased tool another repository owns, follow the
      [edit criteria](references/edit-criteria.md)'s **Source Check Routes**: neither is a blocker,
      the tool's consuming workflow change is source work whose delivery follows `merge-gate`'s
      dependency gate, and no merge here authorizes a release.
      Check the entire canonical skills tree against the authoring reference's **Package And
      References**, imported skills included, rather than only the files being edited; leave generated
      mirrors to Agent Sync. A clean changed file does not make a failing tree validation pass.
      The script checks skill names only. For each file the batch changes, also check by reading
      and searching what the [authoring reference](references/authoring.md)'s **Writing** and **Rules** sections
      require: every cited section, path, script, command and flag resolves; no ruling or example
      disagrees with a file that loads beside it; and the file's line count is within its budget.
   3. **Check prose duplication** through the `code-simplify` pass `review-pass` runs over the delta,
      reading every touched `.agents` file whole, and act on what it reports: guidance duplicated
      between peer rules or skills, including a caller and a skill it always invokes, or between two
      files of one skill; a section grown around a second subject; a heading named for a category
      with one member; a rubric left inline that the authoring reference's skill shape
      sends to a reference. Prose duplicates as readily as code, and nothing else catches it. Every `.agents`
      change gets that pass over its entry point and supporting files, a one-line rule edit as much as a
      new skill: a single bullet added to
      the file that does not own it is exactly the duplication this catches, and it is the change
      least likely to be looked at twice.
   4. **Brief `review-pass`'s final acceptance**, which judges the batch's complete `.agents` diff
      with the intent statement **Guidance Delivery** step 3 gives it; this step starts no gate of
      its own. The brief asks whether the guidance answers the request at the breadth the
      [authoring reference](references/authoring.md)'s **Writing** asks for and whether every mechanism it adds earns its place, and hands the reviewer that reference to read whole, since nothing loads it for a reader of `.agents` files. A named
      tool, surface, or workaround in generic guidance is a finding unless the skill's contract
      depends on it; the incident's route must not narrow the durable decision boundary. The brief
      carries the incident's vocabulary — the product, its record and screen nouns, the labels the
      request quoted — so an example carrying any of it is a finding; it also carries the real case
      behind the request. Resolve each flag through `acceptance-gate`'s **Bounds**: repair the
      owning instruction, push the changed increment, and put it to the fresh gate those **Bounds**
      require. Repeated flags do not permit dropping owed work or merging flagged guidance, apart
      from the `council` decision that replaces another repair once 3 review rounds have failed the
      change; acceptance,
      or that recorded round-limit decision, must cover the final wording before delivery.

   5. **Run one `test-skill` round** over the batch on the head `review-pass` accepted. Give it every
      entry's reproduction scenario, grouping entries that share a failure class. `test-skill` owns
      the scenario writing, coverage, package, control, grading, and rerun procedure.
      Record an entry whose run `test-skill` does not require as `not run: <test-skill reason>`;
      the acceptance gate is its check.

      **A draft agent-configuration pull request is an intermediate delivery state, never this
      skill's result or a turn boundary.** Before a report names its state, read the target
      repository's agent-configuration pull-request lifecycle and take the next transition it
      requires. Read the complete pull-request file list, not only the latest edit or its informal
      label. After the skill test, acceptance, and file-list checks pass, invoke `merge-gate`; do not leave
      it draft under an ordinary source-work default or report it as delivered before its merged
      text and generated outputs are verified. The report names either the merged state or a
      concrete documented gate with its evidence; draft alone is neither.

      **A skill that arrives by relocation is not a skill the change adds.** Establish that the
      guidance survives, and settle where the originals disagreed, as the
      [edit criteria](references/edit-criteria.md)'s **Relocations** says. The report then says
      `not run: relocation, guidance preserved` and names where each original's specifics went.
   6. **Hold each changed output to its concrete example.** For every skill whose output changed,
      compare one run of your own on the branch in flight and every required skill-test run against that
      example: headings, columns, order, file shape. A divergence is the skill's wording, fixed and
      rerun; review and the acceptance gate validate the replacement shape before merge.
   7. **Check the diff file list against the default branch, then merge.** The authorization covers
      a pull request carrying only `.agents` files, and the file outside them that slips in is never
      announced. Read the changed paths rather than trusting your memory of what you edited; a stray
      formatter run or a file picked up by `git add -A` looks identical to intent. A path outside
      `.agents` leaves this branch — dropped when it was never meant, moved to the source pull
      request the work continues under **Branch and commit** when it was — and the new head goes back through **Brief `review-pass`'s final acceptance**. Everything
      in `.agents`, merge it through `merge-gate` with the head `acceptance-gate` accepted — but first
      ask whether any line it adds or drops is true only once a still-open source pull request
      merges. Select where dependent guidance goes under the GitHub rule's **Branches and Pull Requests**,
      and report any hold under its **Merge Authorization**. Otherwise a pull request carrying a
      skill change merges once **Hold each changed output to its concrete example** found every changed output matching its concrete example, and
      one carrying only rules has no example to match and merges once **Run `validate_sources.py check`** through **Run one `test-skill` round** pass, unless their **Merge
      Authorization** holds it. Report a held pull request for the user's review.
   8. **Nothing is copied by hand.** The skills repository is the only copy of a shared skill;
      sessions receive a merged edit through the refresh the GitHub rule's **After Agent Sync** requires, never through a copy
      placed in another repository or install. A skill that reads generically but was written into one repository's `.agents` is
      moved to the skills repository in the same change rather than left as a second copy.
   9. **Read the merged text back before using it.** A merge changes the default branch, not the
      checkout: a session working on another branch still carries the old skill in its tree, and a
      skill invoked from there runs the text the change just replaced. After the merge, fetch the
      default branch and read every skill or rule the change touched from it — `git show
      origin/<default>:.agents/skills/<name>/SKILL.md`, and the references beside it — and run
      from that text for the rest of the session. A skill invoked while its change is still open
      is read the same way from the branch that carries it, never from a checkout that predates
      it.
      `merge-gate` then waits for the default-branch Agent Sync run; the GitHub rules' **After Agent
      Sync** section requires the installed copy to be refreshed before reporting completion.
      Once the run finishes, inspect every generated artifact on the default branch that represents
      the changed source, including `AGENTS.md` when the source feeds root instructions and
      provider trees such as `.cursor/`, `.claude/`, and `.codex/` when they represent the changed
      package. Diagnose stale or missing output through Agent Sync; never repair it by editing
      generated files.

## Manual verification

When skill behavior needs a live agent chat, follow the
[manual verification reference](references/manual-verification.md): how the dispatch is chosen
through `subagent-matrix` and recorded, and the Claude Desktop and Codex cloud procedures.


## Output

Return this report, filled in; keep every heading, write `None` under one with nothing to list, and
send a file holding the items past five under any heading:

```markdown
Files

- `<repository>/.agents/<path>` — created | updated | deleted | renamed from `<old path>`

Changes

- <one sentence per change to the guidance: the failure class it covers first, the triggering case as one example>

Underlying issue

- <what was fixed and how it was verified, or `None`>

Checks

- Source check: passed on <head> | failed: <report>
- Simplification: <clean | findings applied>
- Acceptance gate: <accepted on <head> | repaired and accepted on <head> | blocked — <concrete unresolved decision or unavailable compliant remedy>>
- Skill test: <passing tables reported above | dropped — <reason> | not run: <reason>>
- Example validation: <one line per skill: name — output matches concrete example after <n> round(s) | skipped, no response the user uses | skipped, response unchanged | rule-only change>
- Merged text read back: <default branch head the touched skills and rules were re-read from | not merged>
- Refresh: <installed source and commit | blocked: exact reason | not merged>

Pull request

- <link, with `skills repository` or `<repository>` after it, and `held until <source pull request> merges` when step 7 waits on one>

Skipped

- <item and why, or `None`>
```
