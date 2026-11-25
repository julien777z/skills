---
name: edit-skill
description: Add or edit anything under `.agents` — a skill, rule, agent definition, hook, setting, reference or project guidance — including when the user points out a mistake in how an agent followed or wrote guidance, or questions where guidance was placed, even with no request to edit a skill, and when carrying a guidance batch through delivery to its merge or hold, and verifying a guidance change in a live agent chat. Fix the underlying issue and the guidance path that allowed it, writing the change for the class of failure the user plainly meant, no narrower and no broader, classified before the change is first described, proposed or edited anywhere and shown to them as a Scope Statement first. A correction that encodes a new process waits until that process has worked on the work in hand, which a merged change that carried it has; every other correction is recorded and written at once.
short_description: 'Edit a skill, rule, or agent file and fix the guidance gap that prompted the change.'
---

# Edit Skill

Upsert `.agents` source-of-truth files for agents, skills, or rules based on user input, and carry
every edit through the route **Guidance Delivery** selects for it, whether the user invoked this
skill or the edit arose while doing other work. An edit that skipped this is unverified, and the
report says so.

**A process is encoded only once it has worked, and only a new process waits.** A request to put a
new process into guidance — a workflow, a procedure, a tool or route, a way of building or
delivering something — is first carried out on the work in hand and verified to work; the guidance
is then written from that run: the steps and commands it used, what had to differ from the source
that described it, and what failed along the way. A merged change that carried the process is that
run, so its guidance is written from the merged work, never held for a fresh run after the merge.
Documentation, a plan, a worker's proposal or the request's own description of the process is the
source to try, never the text to encode. Every other correction — a gap a guidance failure exposed,
a rule the user states — depends on nothing the current work does: record it and write its edit at
once under **Recording During A Task**, which sets when it is delivered, while the current work is
corrected beside it; a problem the current work meets never holds or drops such a correction.

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
checking whether guidance allowed the miss. Record the owning file's correction in the same turn,
beside correcting the work, so the next session does not repeat it.

A correct instruction does not close a reported failure to follow it: the causal diagnosis under
**Identify the failure class** traces, repairs and verifies the application step that admitted the rejected decision, and where no guidance governs
the subject, creates its new owner under **Guidance Changes Proceed Automatically**.

## Guidance Changes Proceed Automatically

A user request or an encountered guidance gap, once **Validate input** confirms its premise,
authorizes the canonical `.agents` correction its Scope Statement lists inside what the user said;
a policy change, which that statement lists as beyond it, waits for the user as **Identify the failure class**
says. The statement is shown, never asked: do not ask for a plan, or for approval of the statement,
of a guidance-output example, of a proposed flow or of the pull request. **Apart from a policy
change and a product choice, which reach the user as above, a guidance change reaches the user
only when the agent is unsure whether it does what they meant**, asked through the question tool;
otherwise its gates run and it merges. A hold the invoking workflow or a rule sets, such as the
GitHub rule's hold on a pull request that adds a doctor skill, still applies. A guidance edit that
intentionally changes the product still follows `pre-production`'s **Product Choices**. The gate
set of the edit's route validates the correction.
When a separate source task is active, or a guidance batch is in flight, preserve its execution and
follow **Recording During A Task** for the edit's timing.

## Dependencies
- `skill-pass`
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
- `share-media`

## Recording During A Task

A recorded correction governs the rest of the session at once, ahead of the installed text it
amends, and never holds the task's next step. Record it as a `guidance_correction` entry with
`session-ledger`, backed up and batched as that skill says; once its edit is committed, run
`update-skills` for eligible edits and tell each running worker as `subagent-matrix`'s
**Dispatch** says. Read the [recording reference](references/recording-during-a-task.md) before
recording one: it says what the entry holds, where the edit is written and when it is delivered.

## Guidance Delivery

This route delivers the frozen batch of `guidance_correction` entries its invocation names,
beside the source stream. It holds the source pull request only for the checks its ridden edits
need and the delivery of the batch carrying them; only an edit on that pull request, or one the GitHub rule's **Merge Authorization** holds for a source pull request, waits for that merge. **The primary agent coordinates it**, starting its
reviewer, gate and skill-test agents in the background so the user's review of the source pull
request overlaps it. Coordination needs no independent reader, so the route goes whole to a
delegated worker, at `subagent-matrix`'s standard capability level, only where the host lets a
worker start subagents of its own.

**The batch takes one of two routes, chosen from its diff and its Scope Statements, never from how
small it looks.** Each route below is the gate set its batch passes on the head that merges.

- **Short route.** Every entry changes one requirement in one file, its Scope Statement records
  `flow not affected` and lists nothing beyond what the user said, and the batch adds or removes no
  skill, rule, dependency or script. It runs the source check, `skill-pass`'s pass and
  `code-simplify` in process, one `acceptance-gate`, and `test-skill`'s single-scenario form, with
  no `review-pass`. Read the [delivery routes reference](references/delivery-routes.md) for how
  each runs and how a batch moves to the full route.
- **Full route.** Every other batch, through **Check the sources** to **Conclude the skill test**
  below. One whose head its invoking workflow already reviewed and accepted skips **Review the
  batch**'s `review-pass`, as the [edit criteria](references/edit-criteria.md)'s **Already Reviewed Batches** says.
- A batch that changes no instruction a reader follows, as `test-skill`'s **When It Runs**
  recognizes one, skips the skill test. It still passes the source check and one independent
  `acceptance-gate` read of its delta, briefed as **Brief `review-pass`'s final acceptance** says,
  and that gate's acceptance gives the head `merge-gate` receives.

1. **Resume the batch** as the [edit criteria](references/edit-criteria.md)'s **Resuming A
   Batch** says, including an entry rebuilt from its backup comment and an edit that rides a
   source pull request. The steps below
   cover the agent-configuration pull request.
2. **Check the sources** as **Run `validate_sources.py check`** says.
3. **Review the batch.** Run `review-pass` once over the batch, naming every head it carries. Give it each entry's Scope
   Statement, with the user's words and evidence, as the intent statement, the brief **Brief
   `review-pass`'s final acceptance** describes for its reviewer and acceptance gate, and **Check
   prose duplication**'s checks for its simplification pass. Once that simplification pass is
   done, start **Run one `test-skill` round** on the pushed head, beside review round 1 and never
   behind it: its scenario writing, environment and readers need the failure class and the diff,
   not the accepted head.
4. **Conclude the skill test** on every head `review-pass` accepted: `test-skill` carries each
   result whose inputs that head left unchanged and reruns the rest. It takes every entry's
   reproduction scenario as an input, entries that share a failure class grouped into one
   scenario; then **Hold each changed output to its concrete example** through **Read the merged text back before using it**. A guidance repair the skill-test round makes, here or on a source pull
   request under **Resume the batch**, goes back through `review-pass` over its delta, and the skill-test round reruns
   every scenario `test-skill` does not carry forward, on the head that review accepts. A batch
   in the set `review-pass`'s **Set and timing** defines merges at a head its **Combined Review**
   accepted.
5. **Record each stage.** After each completed or failed stage, record its exact head, stage result, and first
   nonterminal next stage in each entry. Resume from that stage without repeating completed work.
   After the skill-test round, record the pull request, its head, the skill-test results and the merge or
   hold. Keep its `status` `pending` while a hold remains, with its concrete dependency and saved next
   action. This route never sets an entry's terminal status.
- Before the surrounding task ends or hands off, every `pending` entry is processed, or carries its
  concrete blocking decision, failed gate or unavailable dependency, with its evidence and saved next
  action; a recorded correction is reported as recorded until its batch has merged.
- **Delivery is the agent's own work, never the user's errand.** It starts at its own trigger
  without the user asking, and its operational choices — another round, splitting a correction onto
  its own pull request, dropping one, accepting a residual miss — are the agent's, a contested one
  going to `council` in **Ask** mode. No question, report, pending-decision list or note puts such a
  choice to the user or describes a pending batch as waiting on them; one that does is corrected,
  never carried forward. A policy change **Identify the failure class** sends to the user, dropping it
  included, and a user-review hold stay theirs, the policy change asked through the question tool.
- **A draft agent-configuration pull request is an intermediate delivery state, never this
  skill's result or a turn boundary.** At a checkpoint and before reporting its state, read the
  complete pull-request head and file list, not only the latest edit, and record the target
  repository's lifecycle, its current state, and its next transition. A draft confined to
  canonical agent configuration records `agent-configuration exception` and `merge-gate` as its
  next action, which is invoked once its route's gates and the file-list check pass, unless the
  GitHub rule's **Merge Authorization** holds it; it never records `await user authorization`
  otherwise. Delivery continues through the Agent Sync result and the verification of generated
  output, and the report names the merged state or a concrete documented gate with its evidence.
  A genuine gate holds only its dependent step while repair or resolution remains active.

## Behavior

1. **Validate input.**
   - If input is missing or empty, ask: **"What should I add or update in `.agents`?"**
   - **Confirm the request's premise before anything else.** A request often rests on the user's
     reading of what happened: what the agent did, proposed or meant, or what the code does. Check
     that reading against the conversation, the plan or the code. When it is wrong, say so plainly:
     what was actually meant or done, and which existing guidance already covers it. Then stop. Make
     no guidance edit, open no pull request and record no correction, because there is no miss to
     repair, such as a user who asks for a rule against a step the plan never proposed because they
     read its wording as naming something else. When only part of the premise holds, act on
     that part alone. This is different from a real miss that existing text already covers, which
     **Identify the failure class**'s causal diagnosis still repairs.

2. **Identify the failure class, then its target type and name.**
   - **Classify the moment the gap is noticed, before the change is first worded anywhere.** State
     the observable outcome the user rejected and the invariant a correction must preserve, without
     using the named component, format, file or tool as the boundary. Identify at least two ways the
     same outcome can arise, including a workaround that obeys the proposed wording but violates
     that invariant, and a different kind of decision, such as a sentence, quantity or choice, not
     only more examples of one format. Test the proposed scope against those routes before stating
     the change anywhere — a report or question to the user, a queued list, a worker brief, a remedy
     or a ledger line — or writing it: if any still allows the rejected outcome, widen the owning
     decision to that class, and no further, and remove conflicting permissions first. Every such
     statement scopes the rule to the class, naming the instance at most as one example, unless the
     instance is the root cause, which the rule then names and stays scoped to; waiting to write
     never waits to classify. Keep the incident and these cases in the verification record; shared
     guidance states the invariant, not their identities. Classify before choosing the owner, since
     a component's owner can hide a broader failure.
   - Supported types: every kind the description names. Use the type the user states; otherwise
     the owner search below decides it, never a question to the user.
   - A file or skill the request names is a candidate, not proof of ownership. Compare it with its
     callers and dependencies before choosing the target. A condition governing a specific action
     belongs to that action's skill, even when a broader caller sequences the surrounding task.
     When the owner necessarily runs before the action, remove equivalent conditions from callers;
     strengthen its trigger or invocation only if that owner would otherwise be missed. Explain the
     placement.
   - Before choosing an owner, test the candidate against `skill-pass`'s **Where Guidance Lives**:
     name the skill that runs when the requirement applies before choosing a rule or
     `.agents/global.md`, and check what the candidate's name and description bound.
   - **When the request names no target, find the guidance that let the gap through and change it
     there.** A request usually arrives as a symptom with no file attached — "that is a bad
     implementation, do not use X" — and the file to edit is the one that governs the thing X
     belongs to: the language rule for a language construct, the review skill for something a
     review let past, the skill that ran for something it did while running. Search the rules and skills by the subject of the request, not by the request's words,
     read what the candidate already says about that subject, and put the change where a reader
     doing that work will meet it, at the breadth `skill-pass`'s **Writing** asks for. Never ask which file; the search
     is this skill's job.
   - **A violated instruction, or any guidance failure the user points out, calls for causal
     diagnosis and an application repair**, before editing, as the
     [edit criteria](references/edit-criteria.md)'s **Causal Diagnosis** says.
   - **Write the Scope Statement before the edit, and show it.** A named addition is the starting
     point: inspect the owning guidance, related callers and dependencies for what the same class
     of failure needs. Then write the statement in the **Output** shape as the
     [edit criteria](references/edit-criteria.md)'s **Scope Statement** says, store it in the
     ledger entry, and show it in the message that acknowledges the correction. Its narrow probe
     asks whether a reader could follow the text and still repeat the miss; its broad probe, that
     the nearest case outside the class behaves as before. The edit covers the class the user
     plainly meant, no narrower and no broader. It costs no subagent and holds nothing.
     - What the statement lists inside that class is written at once, with no question; product
       choices still follow `pre-production`'s **Product Choices**.
     - **Beyond what the user said is a policy change**: a requirement neither the request nor its
       failure needs, such as a step, a routing rule or a hold the request never named; any
       exception to, or change of, standing guidance the user did not ask to change, however
       necessary the repair makes it look; and any other change they would not expect from their
       own words. It is asked through the question tool with the standing text it would change,
       and written only once the user's own words, or an invoked skill's explicit instruction for
       that change, approve it, while the rest of the edit proceeds.
     - **When the statement records `flow affected`**, the user is also shown the proposed-flow
       comparison of the edit's branch against the default branch once the edit is pushed. This holds for every
       guidance change: a correction, a gap the agent noticed, a rule or global-rules edit, a
       skill edit. It is shown, and the edit proceeds without waiting for an answer, unless the
       statement lists something beyond what the user said or the invoking workflow holds it.
   - **When no existing file of the inferred or selected type governs the subject, create the new
     owner under Guidance Changes Proceed Automatically.** Record its recommended name, scope, and
     behavior in the correction evidence; do not ask for approval. An existing file of that type
     that governs the subject is always edited instead, however thin its current text.

3. **Include the underlying issue.**
   - When the user raises a concrete issue or provides evidence such as screenshots while requesting agent guidance, update the guidance and implement the underlying product or code fix in the same task.
   - Treat the issue and evidence as requested scope, not merely as background for the `.agents` update.
   - Skip the underlying fix only when the user explicitly requests an instruction-only change.

4. **Resolve which repository owns the target, then its path inside that repository's `.agents`.**
   - Decide whether the target is shared or repository-owned, and its path for its type, as the
     placement bullets of `skill-pass`'s **Where Guidance Lives** say.
   - A shared target is edited in a writable checkout of the skills repository, on a branch and
     pull request in that repository, never through the link's path from another repository's
     branch. The [edit criteria](references/edit-criteria.md)'s **Shared Targets** says which
     checkout that is, and how the edit transfers to a separate skills-repository session and is
     replayed when no writable checkout can be obtained.
   - Write guidance only under `.agents`. Provider folders such as `.cursor/`, `.claude/` and `.codex/` are generated by Agent Sync after the merge, so a hand edit or a local sync run's output is overwritten and drifts, as `skill-pass`'s **Harnesses** says; read one only to verify what Agent Sync generated, as **Read the merged text back before using it** says, never as the source of guidance. A mirror left pointing at a path the change renames or deletes is reconciled by the workflow on the default branch, so a branch carrying a stale or broken one meanwhile is expected.
   - This path restriction applies to the agent-content update, not to source changes required to fix an underlying issue from **Include the underlying issue**.
   - When importing external guidance, inspect its actual entry points and file layout before registering it. If an owned sync tool cannot represent the source, extend that tool for the source's format and register the original content directly. Keep a standalone reference collection standalone: do not invent a substitute skill, relabel its files as skills, or bury it in another skill's references.

5. **Write the edit.**
   - Inventory and read the target entry point and
     its referenced files, scripts, templates, and examples. Follow supporting links within the
     package; reviewing only `SKILL.md` or the edited hunk is incomplete. Apply the same genericity,
     ownership, clarity, and evidence standards to every file.
   - **A change to what a skill returns the user is specified with a concrete example before the
     skill is written to produce it.** The [edit criteria](references/edit-criteria.md)'s **Changed
     Output Examples** says which changes count, how the example is modeled and written, and how
     it is validated; send the example as `share-media`'s **What reaches the user, and when**
     says. It is task evidence, not a user approval gate.
   - Trace each miss to the instruction that produced or allowed it, including instructions for
     adding or recording guidance. Name that governing instruction and its replacement in the
     change. Removing a bad example while retaining a directive that regenerates it is incomplete.
     Put incident evidence in the project/verification record and state that destination explicitly.
     Fix the producing instruction and its output together.
   - **Run `skill-pass`'s pass over the delta before delivery**: every added or changed
     instruction and example, the edited skill's complete package and affected callers, and every
     file a folded or incorporated pull request brings in. Its source check runs at **Run
     `validate_sources.py check`**; every other step runs here, and again for a later wording
     change before acceptance and skill tests. Move inline criteria to a named reference when its
     **Package And References** standards require it, and add the appropriate hard-coded output
     format or delivery report line when absent.
   - Update existing files in place and report any structural changes. Before delivery, follow the
     entry point's links again and confirm that each route loads its required guidance. References
     must not hide an essential rule or introduce an unexplained mode or dependency. Run the Scope
     Statement's two probes again on the written text and state each probe's case and outcome in
     validation: the narrow probe's case changes, and the broad probe's case does not.
   - A missing tool the repository needs to run, build, test or review, and a consumer's reference
     to a dependency, follow the [edit criteria](references/edit-criteria.md)'s **Tools And
     Dependency References**.
   - **Moved text is added text**, merged and repaired as the
     [edit criteria](references/edit-criteria.md)'s **Moved Text** says.

6. **Split a multi-item request.**
   - Apply multi-target updates for `agents`, `skills`, and `rules`. When the inferred or selected
     type is singular, map each distinct item of the request to the existing file of that type
     that fits it, and create a new file only when none governs the item's subject, under
     **Guidance Changes Proceed Automatically**.
   - Ambiguous scope is settled by **Identify the failure class**'s Scope Statement, shown and never asked.

7. **Deliver the batch.** **Guidance Delivery** delivers the batch in this order, on the full route with `review-pass`
   carrying **Check prose duplication** and **Brief `review-pass`'s final acceptance**. Ordinary
   repairs and verification remain authorized throughout: resolve flagged gates under
   `acceptance-gate`'s **Bounds** and failing skill-test runs under `test-skill`. A pull request
   confined to agent configuration has merge authorization under the GitHub rule once its route's
   gate set has passed, a skill's changed scripts' own checks included, unless its **Merge
   Authorization** holds it; never ask to repeat that authorization or to continue an ordinary
   repair. It settles no genuine unresolved product, scope, or authorization choice, which goes to
   the user under **Bounds** while independent work continues, and it authorizes no release
   workflow.
   1. **Branch and commit.** Select the edit's pull request under the GitHub rule's **Branches and Pull Requests** and the [guidance pull requests reference](references/guidance-pull-requests.md) — never put it onto a
      source branch, the one checked out included, except guidance that rule puts on the source pull
      request it depends on, which merges with it. Commit the `.agents` files, never a provider
      mirror, and push each step once the checks the GitHub rule's **Pre-Push Gate** defines pass. Open the pull
      request as a draft; it stays draft until `merge-gate` marks it ready as the last step before its merge. An
      open pull request leaves the current guidance in use. A source fix **Include the underlying issue** requires is source work: it goes onto the source pull request
      the work continues in its repository under the same rule and merges as that work does.
   2. **Run `validate_sources.py check`**, the source check `skill-pass`'s **Source Check**
      describes, before the pull request merges, and again whenever the branch changes after that
      run. Nothing on a pull request runs the sync: the workflow runs on the default branch after
      the merge, so a file it refuses is refused once every session is already reading it. Fix
      every report it prints before pushing, and for each file the batch changes check by reading
      what that section leaves to reading.
      A sync tool that cannot reach an imported skill's source repository, and guidance that needs
      an unreleased tool another repository owns, follow the
      [edit criteria](references/edit-criteria.md)'s **Source Check Routes**; neither is a blocker.
   3. **Check prose duplication** through the `code-simplify` pass over the delta, which
      `review-pass` runs on the full route and the editing agent on the short one, reading every
      touched `.agents` file whole for the shapes `skill-pass`'s **Prose Duplication** lists, and
      act on what it reports. Every change to an instruction gets that pass over its entry point
      and supporting files. With `skill-pass`'s budget step it is the one check of a requirement
      stated twice and of the size budget, as its **Reviewer Brief** assigns each check.
   4. **Brief `review-pass`'s final acceptance**, which judges the batch's complete `.agents` diff
      with each entry's Scope Statement as its intent statement; this step starts no gate of its
      own, and on the short route the same brief goes to that route's one gate. The brief is
      `skill-pass`'s **Reviewer Brief**, carrying the incident's vocabulary and the real case
      behind the request, which the gate walks through the resulting package. Resolve each flag through `acceptance-gate`'s **Bounds**: repair the
      owning instruction, push the changed increment, and put it to the fresh gate those **Bounds**
      require. Repeated flags do not permit dropping owed work or merging flagged guidance, apart
      from the `council` decision that replaces another repair once the review rounds `acceptance-gate`'s **Bounds**
      allows have failed the change; acceptance, or that recorded round-limit decision, must cover the final wording before delivery.
   5. **Run one `test-skill` round** over the batch, started and concluded as **Guidance Delivery**
      says for its route. Give it every entry's reproduction scenario, observed miss, and
      Scope Statement's Stays as it is case, grouping entries that share a failure class.
      A correction for a class of recurring failures also exercises a different task that
      reaches the same decision, as the [edit criteria](references/edit-criteria.md)'s
      **Scope Statement** describes. `test-skill` owns scenario writing, coverage, packaging,
      controls, grading, and reruns.
      Record an entry whose run `test-skill` does not require as `not run: <test-skill reason>`;
      the gate of its batch's route is its check.

      **A skill that arrives by relocation is not a skill the change adds**: establish that as the
      [edit criteria](references/edit-criteria.md)'s **Relocations** says, then report `not run:
      relocation, guidance preserved` and name where each original's specifics went.
   6. **Hold each changed output to its concrete example.** For every skill whose output changed,
      compare one run of your own on the branch in flight and every required skill-test run against that
      example: headings, columns, order, file shape. A divergence is the skill's wording, fixed and
      rerun; review and the acceptance gate validate the replacement shape before merge.
   7. **Check the diff file list against the default branch, merge through `merge-gate`, copy
      nothing by hand, and read the merged text back before using it.** Read the [merge and read-back
      reference](references/merge-and-readback.md) when the batch reaches the file-list check; it
      holds these last steps, in order.

## Manual verification

When skill behavior needs a live agent chat, choose the dispatch through `subagent-matrix` and
record it as the [manual verification reference](references/manual-verification.md) says, then
follow that reference's Claude Desktop and Codex cloud procedures.

## Output

The Scope Statement, shown in the message that acknowledges a correction, one per entry:

```markdown
Guidance change — flow affected | flow not affected

- Noticed: <the gap> — only for a gap the agent noticed itself; a statement answering the user's request opens with From now on
- From now on: when <situation>, agents <do this> instead of <that>.
- Also changes, same class: <skill or rule> — <situation>: <new behavior> | None
- Stays as it is: <the nearest case outside the class, and what agents still do there>
- Inherited without an edit: <skill, rule or flow that reads the changed text> — <what changes for it | no change> | None
- Beyond what you said, waiting for you: <change, the standing text it would alter, why it seems needed> | None
```

The delivery report, filled in; keep every heading, write `None` under one with nothing to list,
and send a file holding the items past five under any heading:

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
- Route: <short | full | source check only> — <why it qualifies>
- Acceptance gate: <accepted on <head> | repaired and accepted on <head> | blocked — <concrete unresolved decision or unavailable compliant remedy>>
- Skill test: <passing tables reported above | dropped — <reason> | not run: <reason>>
- Example validation: <one line per skill: name — output matches concrete example after <n> round(s) | skipped, no response the user uses | skipped, response unchanged | rule-only change>
- Merged text read back: <default branch head the touched skills and rules were re-read from | not merged>
- Refresh: <installed source and commit | blocked: exact reason | not merged>

Pull request

- <link, with `skills repository` or `<repository>` after it, and `held until <source pull request> merges` when **Check the diff file list against the default branch, then merge** waits on one>

Skipped

- <item and why, or `None`>
```
