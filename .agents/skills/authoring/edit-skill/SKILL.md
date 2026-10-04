---
name: edit-skill
description: Add or edit a skill, rule, or agent file under `.agents`, including when the user points out a mistake in how an agent followed or wrote guidance or questions where guidance was placed. Write each change for the whole class of failure the request is one instance of, which is the same mistake in every kind of document, file, tool, or step it can occur in, not only the one the request names, the section it says to put the fix in, or the one path that let this instance through. Diagnose and fix the underlying issue and the guidance path that allowed it, even without an explicit request to edit a skill. Deliver every behavior-changing guidance edit through simplification, the acceptance gate, and `test-skill` before its pull request merges.
short_description: 'Edit a skill, rule, or agent file and fix the guidance gap that prompted the change.'
---

# Edit Skill

Upsert `.agents` source-of-truth files for agents, skills, or rules based on user input, and carry
every edit through the same delivery whether the user invoked this skill or the edit arose while
doing other work. An edit that skipped this is unverified, and the report says so.

An open `.agents` pull request is not a delivery result. Continue the same run through its source
check, required review steps, merge, Agent Sync result, and verification of generated
root instructions and provider output; stop only for a genuine gate.

**A gap you notice yourself starts this skill, exactly as a request does.** Guidance that let a miss
through, a skill whose trigger did not fire when it should have, one that says nothing about the case
in hand, a step you found yourself doing that no skill describes: each is this skill's input, and
noticing it is the whole trigger. Waiting to be told is what leaves the next session to rediscover
the same gap, and the session that hit it is the only one holding the evidence.

The tell is a sentence you are about to write to the user about your own process — that you skipped
a step, that a check did not apply, that you should have done something earlier. Write the guidance
change first, then the sentence; it is a finding about the guidance, not a confession.

**The user pointing out how you work is the same trigger, and it is never only the one fix.** "Why
did you do it that way", "you should have done X", "don't do Y again": each names a gap in the
guidance that let it through, and each carries two pieces of work — correct the thing in front of
you, and change the file that would have prevented it. Doing only the first leaves the next session
to make the same mistake and the user to point it out twice.

Both start in the same turn: they are one piece of work, and the guidance change is never offered,
proposed, or listed as a next step. It then runs the delivery below like any other edit, and the
only thing that carries it past this turn is a question this skill puts to the user.

Two outcomes are reported rather than written into a file. Where the search finds nothing that
governs the subject, that absence is the finding and step 2's rule on proposing a new file applies.
Where the governing file already says it correctly, the finding is that the guidance was not
followed — say so, and do not restate the rule beside itself. Either way the report names the
outcome, because silence reads as the guidance having been fixed.

## Dependencies

- `code-simplify` — the pass over the guidance itself before it merges.
- `acceptance-gate` — the diff question over the `.agents` change once it reads clean.
- `test-skill` — the proof that every behavior-changing guidance edit changes what a reader does before it merges.
- `subagent-selection` — the model tier for live verification chats.
- `merge-pr` — the verified squash merge of the pull request step 7 clears.
- `execute-task` — the environment-refusal policy an unreachable validator source falls under.

## Behavior

1. Validate input.
   - If input is missing or empty, ask: **"What should I add or update in `.agents`?"**

2. Identify target type and name.
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
   - **A file's name and description bound what it owns.** Before choosing a skill or rule, state
     the condition its name and description set — a release stage, a technology, a mode, a kind of
     task — and ask whether the guidance would still be true where that condition does not hold. If
     it would, that file is too narrow, however close its neighbouring section: the guidance goes to
     the file whose scope matches its own, and a global rule takes what holds everywhere. Neither
     running on every task nor already holding a related rule, such as one on required fields when
     the guidance is about required settings, makes a narrower file the owner.
   - **When the request names no target, find the guidance that let the gap through and change it
     there.** A request usually arrives as a symptom with no file attached — "that is a bad
     implementation, do not use X" — and the file to edit is the one that governs the thing X
     belongs to: the language rule for a language construct, the testing rule for a fixture, the
     review skill for something a review let past, the skill that ran for something it did while
     running. Search the rules and skills by the subject of the request, not by the request's words,
     read what the candidate already says about that subject, and put the change where a reader
     doing that work will meet it, at the breadth step 5 asks for. Never ask which file; the search
     is this skill's job.
   - **A violated instruction is evidence of an unresolved guidance gap.** Never close the edit as
     already covered merely because existing guidance forbids the failure. Find why that guidance
     did not control the run — its trigger, dependency, sequence, enforcement, visibility, or
     wording — and strengthen the owning guidance or workflow so the same path cannot bypass it.
     Close every other path the failure's class takes, not only the one this instance used.
     When the owning skill was not invoked, harden its frontmatter description first; body text
     cannot control a run that never loads the skill.
   - When the user points out a guidance failure, trace the actual path from the request to the
     missed behavior before editing: which instruction applied, whether its skill loaded, and why
     the agent's decision diverged. Correct the current work and the owning guidance in this run.
   - **When no existing rule or skill governs the subject, propose a new one and ask before
     creating it.** State the recommended name and, in at most three sentences, what it would say
     and what it would change, with the question tool; create it only on a yes. An existing file
     that governs the subject is always edited instead, however thin its current text.

3. Include the underlying issue.
   - When the user raises a concrete issue or provides evidence such as screenshots while requesting agent guidance, update the guidance and implement the underlying product or code fix in the same task.
   - Treat the issue and evidence as requested scope, not merely as background for the `.agents` update.
   - Skip the underlying fix only when the user explicitly requests an instruction-only change.

4. Resolve which repository owns the target, then its path inside that repository's `.agents`.
   - **Shared or repository-owned.** Generic skills live in one shared skills repository and reach
     every session through a user-level skill root; repository-specific skills, every rule, and
     repository-specific agents live in the repository they describe. Inspect a skill's content and
     dependencies to decide ownership, including for an existing skill: a user-level symlink shows
     where it is installed, not where it belongs. A new or existing skill goes to the skills
     repository only when it reads generically without losing required behavior. If making it
     generic would remove or misstate guidance it needs to give, put it in the repository it
     describes under `.agents/skills/`, at any depth; move a misplaced existing skill there.
     **Guidance whose correctness depends on a current repository's product, resources, topology, contracts, configuration, or relationships is project guidance.** It belongs in that repository's `.agents/project.md` or a repository-specific skill, regardless of the subject that exposed the gap. A shared skill may teach the classification procedure, but never carry a current repository's facts or boundaries.
     An agent definition that a shared skill runs on goes with that skill; every other agent, and
     every rule, is repository-owned.
   - A shared target is edited in the skills repository's checkout — the one the user-level link
     resolves to or, when the session has no editing checkout, a writable checkout attached to
     or cloned into the session — on a branch and pull request in that repository, never
     through the link's path from another repository's branch. A cloud setup clone installed
     only to provide skills is not the editing checkout. Transfer the edit to a separate
     skills-repository session only when no writable checkout can be obtained, never by editing
     the installed clone.
     The originating session supplies the observed miss and its failure class, original task,
     relevant diff or small file set, repository commit, original skill text, and two to four
     observable pass criteria.
     Include a sanitized fixture when the skills session cannot read the originating repository.
     The skills session tests original and proposed wording against the same case and names the
     exact proposed pull-request head. For repository-dependent behavior, the originating session
     then reads that head's `SKILL.md` explicitly and replays the case in its own context before
     merge; fetch the head when accessible or receive the exact file as a scratch artifact. A new
     head invalidates that replay. Do not assume a pull request automatically installs its skill.
   - `agent` -> `.agents/agents/<name>.md`
   - `rule` -> `.agents/rules/<name>.md`
   - For a scoped rule, declare its file patterns once as `paths` in canonical frontmatter.
     Do not duplicate them as `globs`; Agent Sync writes each provider's required scope key.
     Use `alwaysApply: true` only when the rule belongs in every session.
   - `skill` -> `.agents/skills/<name>/SKILL.md`, or `.agents/skills/<folder>/<name>/SKILL.md`
     where the repository sorts its skills into folders; the folders group the source and never
     change the name a skill installs under.
   - repository facts only some skills need -> `.agents/references/<name>.md`, as the global
     rules' **Repository guidance** places them; Agent Sync neither mirrors nor validates them.
   - Never read or write `.cursor/*`, `.claude/*`, `.codex/*`, or any other non-`.agents` agent or provider folder.
   - Do not manually create, update, or sync mirrored command/skill/rule files in those folders; repository automation propagates changes from `.agents` to Cursor, Claude, Codex, and similar targets. This holds with no exception, including where the change leaves a mirror pointing at a path it renames or deletes: the workflow reconciles those on the default branch, and a branch carrying a stale or broken one meanwhile is expected.
   - This path restriction applies to the agent-content update, not to source changes required to fix an underlying issue from step 3.
   - When importing external guidance, inspect its actual entry points and file layout before registering it. If an owned sync tool cannot represent the source, extend that tool for the source's format and register the original content directly. Keep a standalone reference collection standalone: do not invent a substitute skill, relabel its files as skills, or bury it in another skill's references.

5. Upsert behavior.
   - Read the [guidance quality criteria](references/guidance-quality.md), then inventory and read the
     target entry point and its referenced files, scripts, templates, and examples. Follow supporting
     links within the package; reviewing only `SKILL.md` or the edited hunk is incomplete. Apply the
     same genericity, ownership, clarity, and evidence standards to every file.
   - **A change to what a skill returns the user is approved as a fictional example before the
     skill is written to produce it.** The class is any new or changed user-facing output shape — a
     table, a report layout, a sent file, a message template, a listing — in a skill whose response
     the user reads or acts on. It is changed when the user would notice it in the response itself: a
     new or moved column, a different grouping, a link where there was none. A new status value or a
     reworded label is not that, and a skill whose result is edits, a merge, a deployment, a verdict
     another skill consumes, or a report only an agent reads has no such response. Whether an output
     changed is the editor's call, from what the skill returns before and after. Write the example
     for a realistic invented scenario with invented names, as one markdown file whose first line is
     `**EXAMPLE — fictional output for approval; no smoke test was run.**`, check it as the global
     rules' **User-Facing Output** requires, and send it as the final message of a turn that asks in
     plain text whether to approve or reject it, one skill at a time. On a rejection, ask what must
     change, revise the example, and ask again. Only then write the skill to produce exactly the
     approved shape; the required smoke run follows in delivery and is never how a format is
     proposed.
   - Trace each miss to the instruction that produced or allowed it, including instructions for
     adding or recording guidance. Name that governing instruction and its replacement in the
     change. Removing a bad example while retaining a directive that regenerates it is incomplete.
     Put incident evidence in the project/verification record and state that destination explicitly.
     Fix the producing instruction and its output together.
   - When generalizing or shortening guidance, account for each useful instruction removed: retain
     it as a reusable procedure, link its owning guidance, or establish why it no longer applies.
     Check that the next reader can still perform the action and recognize success; removing the
     incident details must not remove the lesson. Apply the preservation criteria in the quality reference.
   - Check skill shape and output against those criteria. Move inline criteria to a named reference
     when required, and add the appropriate output template or delivery report line when absent.
   - Update existing files in place and report any structural changes. Before delivery, follow the
     entry point's links again and confirm that each route loads its required guidance. References
     must not hide an essential rule or introduce an unexplained mode or dependency. Check genericity
     with a materially different instance of the same failure class; state that case and its expected
     outcome in validation. Renaming the original example or replaying only it does not establish breadth.
   - After a dependency receives a separately authorized release, replace consumer references to
     its branch with a maintained version tag. Use a minor release for a new capability or a patch
     release for a bug fix; verify any moving major tag points to that release and validate the
     consumer against it. Do not switch to an unpublished tag or the default branch.
   - If target file does not exist, create it with a concise structure matching existing style.
   - Group frontmatter fields by subject. Put a field that summarizes, qualifies, or overrides
     another immediately after the field it relates to, unless the format requires another order.
     Place new body guidance under the broadest existing subject section that fits.
   - A heading names the subject a reader looks under — Comments, Commits, Workflows — never the
     requirement it holds. Add a section only when no existing one covers the subject, and name it
     for the whole subject: a heading that states one rule invites the next rule on that subject
     into a heading of its own. A restriction on one subject goes under that subject's heading;
     `## Guardrails`, kept at the bottom, holds only constraints that span the file's subjects.
   - Express each independent requirement once, as one concise statement or bullet, without padding. Merge overlapping or synonymous guidance without losing distinct criteria or exceptions.
   - Normalize the touched file's nearby structure when needed: combine narrow sections, remove redundant wording, and order foundational guidance before specialized concerns.
   - **Prefer the broad statement, and let the request's shape be its example.** A request
     arrives as one symptom, and the rule it needs names the class that symptom belongs to; the
     symptom's shape stays as one illustration of it. In shared guidance that illustration never
     carries the incident's own vocabulary — the labels, headings, records, screens or values of
     the product that prompted it, however ordinary they read: a label lifted from the screen
     under review is that screen's copy. Retell it with invented nouns from an unrelated domain, as
     the global rules' **Repository guidance** requires, and replace any such noun already in the
     section the edit touches. Asked for `Final` on string constants, write `Final` for
     every module-level constant; asked for a walkthrough rule because a page reloaded in a
     loop once a back-end change was absent, write that the run is judged against intended
     behaviour because an API error surfaces as any unintended behaviour, and name the loop
     only as one instance. A rule written for the symptom is silent on the next one, and the
     next one is what it will be read for. A named field, file, section, document kind, tool,
     or step, including the place a request says to put the fix, is an example of its class and
     a candidate home under step 2, never the limit of the rule, unless the contract requires
     its exact identity. Broaden to the class the user plainly meant, never to a neighbouring
     subject. Wording handed over — rule text in the request or in a delegating agent's brief —
     is input to this, never the spec: name the decision the examples force, list at least two
     instances of a different kind from those examples and from each other, and write the rule
     to cover them, widening narrower wording as it arrives. A wider label for the same examples
     is not that decision. After the draft, apply it to one further case the request never
     mentioned and that is a different kind of thing again; a case the draft would still handle
     as before means the draft only renamed the examples, and it is rewritten until that case
     changes too. Apply that decision to every instruction in the file that does the same work.
     One section rewritten while a neighbour still does the narrow thing is the draft only half
     done, and it is rewritten until the neighbour changes too. An agent delegating an edit
     passes the class and the evidence, not finished rule text for one case.
   - Describe reusable roles, boundaries, and decision criteria generically even in
     repository-focused guidance when the pattern is not repository-specific. Keep concrete
     repository names only when correctness depends on that local contract.
   - Before adding a requirement to a shared rule, test it against a repository without the feature that prompted it. If it prescribes the current repository's documentation sections, inventory, or generation workflow, put it in `.agents/project.md`; keep the shared rule limited to guidance that still makes sense elsewhere.
   - When the user asks to add guidance from another repository, treat that repository as source material: encode transferable requirements in the owning skills and refer to those skills by name. Before delivery, audit the edited package for the source repository's name, links, paths, commands, versions, and configuration; never hard-code or cite that repository in a skill.
   - Separate temporary task, session, and pull-request directions from lasting guidance before
     writing. Apply the former to the current work only; never encode them as canonical rules or
     skills.
   - A skill may restate an ambient rule when it helps the reader act at the point of use; this does
     not license a second copy of a decision boundary owned by a skill that necessarily runs.
   - Keep reusable skill names, instructions, scripts, and interfaces model-agnostic. Name a client or model only in a scoped compatibility section where its behavior genuinely differs.
   - Do not add committed tests for skills or their helper scripts, inside or outside the skill directory. Keep any needed execution checks temporary and untracked.
   - **Refer to a skill, and to anything inside it, by the skill's name, never by path.** `the `code-simplify` skill's rubric reference` is right; a relative path into another skill's directory is wrong, because the directories move between repositories and user-level roots and the name is the only stable handle.
   - Declare every invoked skill by canonical skill name in a near-top `## Dependencies` section of the owning `SKILL.md`. That section lists skills only, never tools, plugins, scripts, references, assets, executables, or filesystem paths.
   - **A skill restricted to user invocation is never an automatic dependency.** A directly
     user-invoked workflow may delegate such an action only when its contract explicitly authorizes
     that action and bounds its targets, and the restricted action's own entry point recognizes
     that delegation. Declare it in the workflow's dependencies. This authority lasts only for that
     invocation; discovery, an ordinary task, a prior run, or an automatic caller supplies none.
     Otherwise move any shared steps into a model-invokable skill both may depend on rather than
     bypassing the restriction. Naming a user-only skill or suggesting the user invoke it is not
     delegation or authorization.
   - Invoke dependent skills only from the owning `SKILL.md`. References and other supporting files are passive and must not invoke skills or identify dependencies through relative paths to another `SKILL.md`.
   - Before delivery, audit each edited skill's complete package and its affected callers: list every instruction to apply or invoke another skill, compare those names with the owning entry point's `## Dependencies`, and resolve missing, stale, or path-based entries and any user-only dependency lacking the explicit bounded delegation above. Check references separately for hidden invocations and cross-skill filesystem links; move the invocation to `SKILL.md` and refer to the other package by skill name. A passing source mirror does not replace this audit.
   - Do not embed product-specific file paths or copy current application code into reusable skills; those go stale when files move or refactors land. Prefer generic placeholders (for example `services/<name>/...`), short pattern descriptions, or minimal invented examples that are not tied to live paths or current line-level code.
   - **A skill that reads generically belongs to every repository, so write it that way and put it in the skills repository.** Repository paths, product names, and domain nouns turn a reusable workflow into one repository's copy of it; keep them out unless the skill's correctness depends on that local contract, and where a skill genuinely needs one local fact, take it from the repository's project guidance or a setting rather than baking it in. Where a shared skill needs a repository-specific collaborator — a migrations skill, a finalization skill, a deployment skill, a deferral label — it names the role and finds the skill by its description in the skill listing, and the repository's `project.md` **Repository Skills** table says which local skill fills the role.
   - **Generic ownership is determined by what the skill must do, not its name.** A generically named skill can depend on one repository's contract; keep that skill in the repository and its facts in project guidance. Language, platform, framework, and workflow skills that truly apply across products remain shared and read repository commands, identities, hosts, packages, and fixtures from project guidance rather than embedding them.

6. Multi-target behavior.
   - Apply multi-target updates for `agents`, `skills`, and `rules`.
   - When the inferred/selected type is singular (for example `skill`), distribute requested items across multiple files of that type as needed.
   - Update existing files when they already fit part of the request (for example update skill A and skill B).
   - Create a new file of that type when no existing file governs a requested item's subject (for example create skill C), after the question step 2 requires.
   - If one request contains multiple distinct items, map each item to the best existing file or a new file within the same inferred/selected type.
   - If scope is ambiguous, ask a short follow-up before editing.

7. Deliver it, in this order. The pull request carries only `.agents` files, so every call inside
   this delivery is the editor's own — a flagged gate, a smoke round that would not close — made
   and stated in the report, because a pull request confined to agent configuration has merge
   authorization under the GitHub rule after its stated gates; that authorization does not extend
   to a release workflow. A question asking for it only holds every later session on the guidance
   the change replaces. The approval of a changed output's fictional example, under **Upsert
   behavior**, is the one question put to the user, and it comes before delivery.
   1. **Branch and commit.** The edit goes onto the open agent-configuration pull request the work
      continues in the repository being edited, whichever session opened it, or, when it continues
      none, onto a branch from the freshly fetched default branch with a new pull request, under the GitHub rule's **Branches and Pull Requests** — never onto a
      source branch, the one checked out included. Commit the `.agents` files, never a provider
      mirror, and push each step once `execute-task`'s **Pre-Push Gate** checks pass to a draft pull
      request; steps 3–4 are the complete-diff pass its **Completion** runs, and step 7's `merge-pr` takes
      the pull request out of draft. None of that waits to be asked: the decision was made when the edit was requested, and
      a pull request left open keeps every later session working from the guidance this change
      replaced. A source fix required by step 3 is source work: it goes onto the source pull request
      the work continues in its repository under the same rule and merges as that work does.
   2. **Run `validate_sources.py`**, which sits under `scripts/` beside this skill, before the pull request opens, and again before it
      merges when the branch changed since. Nothing on a pull request runs the sync: the workflow
      runs on the default branch after the merge, so a file it refuses is refused once every session
      is already reading it. The script installs the sync tool at the revision the workflow pins and
      mirrors the canonical tree into a scratch copy, so what it refuses is exactly what the workflow
      would. Run it from the root of the repository being edited, with that repository's own
      interpreter or any interpreter meeting the sync tool's version, and fix every
      report it prints before pushing; a description holding a colon followed by a space is the usual
      one, and quoting the value is the fix.
      When the sync tool cannot reach an imported skill's source repository, that is an environment
      refusal under `execute-task`, not a blocker: attach or clone the repository, and when the tool
      fetches through a path the environment refuses, fix the tool to use one it serves.
      Check the entire canonical skills tree against repository packaging rules, including
      imported skills, rather than only the files being edited. Remove forbidden provider UI
      metadata such as `agents/openai.yaml` from canonical skill packages; leave generated
      mirrors to Agent Sync. A clean changed file does not make a failing tree validation pass.
      When the guidance needs a change in an unreleased tool owned by another repository, point
      the consuming workflow at that tool's active branch and validate against it, without waiting
      for the tool's review loop. That workflow change is source work, delivered and merged under
      step 1's source route, and this pull request's merge waits for it. After the tool merges and
      receives an authorized release, a later source change from the latest default branch replaces
      the branch reference with its maintained version tag, validated against the tagged tool and
      merged on the user's authorization. No merge here authorizes the release.
   3. **Run `code-simplify`** across the branch and act on what it reports: guidance duplicated
      between peer rules or skills, including a caller and a skill it always invokes; a section grown
      around a second subject; a heading named for a category with one member; a rubric left inline
      that the skill-shape rule sends to a
      reference. Prose duplicates as readily as code, and nothing else catches it. Every `.agents`
      change gets that pass over its entry point and supporting files, a one-line rule edit as much as a
      new skill: a single bullet added to
      the file that does not own it is exactly the duplication this catches, and it is the change
      least likely to be looked at twice. Run it in process over the branch's own files, never
      fanned out to subagents: a guidance diff is a scope one reviewer holds whole, and the reviewer
      who has to compare a new bullet against the section it duplicates is the one already holding
      both.
   4. **Run `acceptance-gate`** with its diff question over the `.agents` diff, the request as the
      intent statement. It judges whether the guidance answers the request at the breadth **Upsert
      behavior** asks for and whether every mechanism it adds earns its place. Treat a named tool,
      surface, or workaround in generic guidance as a finding unless the skill's contract depends on
      it; the incident's route must not narrow the durable decision boundary. Give the gate the
      incident's vocabulary — the product, its record and screen nouns, the labels the request
      quoted — so an example carrying any of it is a finding. A flag gets the one
      rewrite that skill allows, pushed as its own increment and put to a fresh gate. A second flag ends the rewriting: fix it
      when the flag names a defect in the guidance, merge as it stands when it names a preference
      the rewrite already answered, or drop the item when neither holds, and state which and why in
      the report, as that skill's **Bounds** leave it to the caller for a change whose merge needs
      no authorization.
   5. **Run `test-skill` for every behavior-changing skill, rule, or agent edit.** A rule's
      source type never exempts it: any changed instruction that can alter what a reader does gets
      an edited and original control run. Run it here rather than before step 3, because a round
      run against wording the simplification pass then rewrites has tested text nobody will follow.
      That pass settles how the guidance reads; this one settles whether it changes what a reader
      does, against the miss that prompted it and with the original text as the control. Give both
      readers the complete relevant package, including the references needed for the scenario; an
      entry-point-only test cannot prove a reference fix. A run that misses is diagnosed, changed
      and rerun as that skill says, never merged with a failing run.
      A **mechanical seam edit** changes no behaviour and needs no smoke run: a dependency
      replaced by the role phrase that finds it, a path generalized, a rename, a frontmatter key, a
      reference path corrected, wording that says the same thing shorter. The report says
      `not run: mechanical seam edit` for it, and the acceptance gate is its check.

      **A draft pull request is an intermediate delivery state, never this skill's result.** After
      the smoke, acceptance, and file-list checks pass, invoke `merge-pr` for the skill pull
      request; do not leave it draft under an ordinary source-work default or report it as
      delivered before its merged text and generated outputs are verified.

      **A skill that arrives by relocation is not a skill the change adds.** Moving one between
      repositories, or generalizing local copies into one every repository can adopt, produces a new
      file and no new guidance, and a smoke run against a miss nobody had proves nothing. What makes
      it a relocation is that the guidance survives, so establish that rather than asserting it:
      diff the new file against every original line by line, and account for each line the diff
      removes as either the same instruction in repository-neutral words or guidance relocated to a
      named home — the owning repository's project guidance for what only that repository can state.
      A line carrying an instruction no original carried is an edit riding along, and the paragraph
      above decides it on its own terms. The report says `not run: relocation, guidance preserved` and names where each
      original's specifics went.

      Where the originals disagreed, the disagreement is the thing to get right, and neither answer
      may be picked for both. Carry the shared guidance and hand the contested question back to each
      repository, checking that each one already states its answer where the skill now sends its
      reader; a repository that does not is the flag, because the merge silently gave it the other
      one's answer.
   6. **Hold each changed output to its approved example.** For every skill whose changed output
      the user approved as a fictional example, compare one run of your own on the branch in flight
      and every required smoke run against the approved example: headings, columns, order, file
      shape. A divergence is the skill's wording, fixed and rerun; a shape the user has not approved goes back to the user as a new fictional
      example, never into the merge.
   7. **Check the diff file list against the default branch, then merge.** The authorization covers
      a pull request carrying only `.agents` files, and the file outside them that slips in is never
      announced. Read the changed paths rather than trusting your memory of what you edited; a stray
      formatter run or a file picked up by `git add -A` looks identical to intent. A path outside
      `.agents` leaves this branch — dropped when it was never meant, moved to the source pull
      request the work continues under step 1 when it was — and the new head goes back through step 4. Everything
      in `.agents`, merge it through `merge-pr` with the head `acceptance-gate` accepted — but first
      ask whether any line it adds or drops is true only once a still-open source pull request
      merges, and if so hold it until that pull request has merged, as the GitHub rule's **Merge
      Authorization** says, and report it as that rule directs. Otherwise a pull request carrying a
      skill change merges once step 6 found every changed output matching its approved example, and
      one carrying only rules merges on sight as the GitHub rules say. A pull request a doctor run
      or `new-doctor` opens is left for the user instead; the steps above still run, the merge does
      not.
   8. **Nothing is copied by hand.** The skills repository is the only copy of a shared skill;
      sessions receive a merged edit through the refresh step 9 ends with, never through a copy
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
      `merge-pr` then waits for the default-branch Agent Sync run and refreshes the main local
      checkout and, for the skills repository, the installed copy this session loads.
      After that refresh, inspect every generated artifact that represents the changed source,
      including `AGENTS.md` when the source feeds root instructions and provider trees such as
      `.cursor/`, `.claude/`, and `.codex/` when they represent the changed package. Diagnose stale
      or missing output through Agent Sync; never repair it by editing generated files.

## Manual verification

When skill behavior needs a live agent chat, use `subagent-selection` to resolve the host's tiers
and choose its lowest available tier for that chat. Select the resolved model in the chat UI;
record it with the tested branch, exact commit, session type, and observed result. A resumed
container proves its maintenance path, not a fresh setup run.

### Claude Desktop

1. In Claude Desktop's Code view, choose Remote, open the environment picker, and use the settings
   control beside the selected environment to edit its setup script. Check out the pull-request
   branch and invoke the installer from that checkout. Preserve unrelated setup commands and
   settings; save the script and verify the editor reports the update.
2. Start a new cloud session with the pull-request branch attached. Verify from session evidence
   that setup ran the script at the intended commit, then check the skill and rule used by the
   session resolve into the intended checkout in both Claude's cloud home and the runtime's home.
   If the session reused an older setup image, record that result and obtain a fresh setup run
   before claiming setup passed.
3. After the source pull request merges and the verification task is finalized and closed, update
   the remote setup script to check out the repository's default branch. Save the script. Remove
   only stale test sessions created for this verification:
   right-click each session in Claude Desktop and delete it through the UI, one at a time; never
   use a script or API to delete sessions.

### Codex cloud

1. In Codex cloud Settings → Environments, create or edit an environment attached to the repository.
   Set its setup script to obtain the Skills checkout on the pull-request branch and invoke its
   installer. Set its maintenance script to invoke the same installer on a resumed container. Keep
   the network access needed by the test.
2. Start a fresh task on the pull-request branch. Verify the installed skill and shared rule links,
   and Codex's global `AGENTS.md`, resolve into the installed checkout at the intended commit.
   Run the installer again and verify it succeeds without changing unrelated content.
3. Resume a cached container and verify the maintenance script ran and the same links still resolve.
   Distinguish this result from a fresh setup result.
4. After the source pull request merges and the verification task is finalized and closed, update
   the environment setup script to obtain the Skills checkout on the repository's default branch.
   Save the script. Archive test tasks created for this verification.

## Output

Return this report, filled in; keep every heading, write `None` under one with nothing to list, and
send a file holding the items past five under any heading as the User-Facing Output rule requires:

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
- Acceptance gate: <accepted | rewritten and accepted | flagged twice: <fixed | merged as it stands | dropped> — <reason>>
- Smoke test: <passing tables reported above | dropped — <reason> | not run: <reason>>
- Example approved: <one line per skill: name — approved after <n> round(s), output matches it | skipped, no response the user uses | skipped, response unchanged | rule-only change>
- Merged text read back: <default branch head the touched skills and rules were re-read from | not merged>
- Refresh: <main checkout and installed copy at <sha>, installer rerun | skipped: <dirty paths> | not merged>

Pull request

- <link, with `skills repository` or `<repository>` after it, and `held until <source pull request> merges` when step 7 waits on one>

Skipped

- <item and why, or `None`>
```
