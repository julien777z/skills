---
name: edit-skill
description: Add or edit a skill, rule, or agent file under `.agents`, implement the concrete issue that prompted it, and deliver it through simplification, the acceptance gate, the smoke test, and the user's approval of an example response before the pull request merges. Applies whenever agent guidance is added or edited, invoked or not, and whenever a gap in existing guidance is identified — a skill that let a miss through, one whose trigger did not fire, one that says nothing about the case in hand — because noticing the gap is what starts this skill, not being asked to fix it.
---

# Edit Skill

Upsert `.agents` source-of-truth files for agents, skills, or rules based on user input, and carry
every edit through the same delivery whether the user invoked this skill or the edit arose while
doing other work. An edit that skipped this is unverified, and the report says so.

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
only thing that carries it past this turn is a question that delivery puts to the user.

Two outcomes are reported rather than written into a file. Where the search finds nothing that
governs the subject, that absence is the finding and step 2's rule on proposing a new file applies.
Where the governing file already says it correctly, the finding is that the guidance was not
followed — say so, and do not restate the rule beside itself. Either way the report names the
outcome, because silence reads as the guidance having been fixed.

## Dependencies

- `code-simplify` — the pass over the guidance itself before it merges.
- `acceptance-gate` — the diff question over the `.agents` change once it reads clean.
- `smoke-test` — the proof that a skill edit changes what a reader does.

## Behavior

1. Validate input.
   - If input is missing or empty, ask: **"What should I add or update in `.agents`?"**

2. Identify target type and name.
   - Supported types: `agent`, `skill`, `rule`.
   - If the user explicitly says the type, use it.
   - If type is not explicit, infer it only when confidence is high.
   - If not confident, ask: **"Should this be an agent, skill, or rule?"**
   - **When the request names no target, find the guidance that let the gap through and change it
     there.** A request usually arrives as a symptom with no file attached — "that is a bad
     implementation, do not use X" — and the file to edit is the one that governs the thing X
     belongs to: the language rule for a language construct, the testing rule for a fixture, the
     review skill for something a review let past, the skill that ran for something it did while
     running. Search the rules and skills by the subject of the request, not by the request's words,
     read what the candidate already says about that subject, and put the change where a reader
     doing that work will meet it, at the breadth step 5 asks for. Never ask which file; the search
     is this skill's job.
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
     repository-specific agents live in the repository they describe. An existing skill is shared
     when the entry the user-level root holds for it (`~/.claude/skills/<name>`,
     `~/.codex/skills/<name>`, `~/.cursor/skills/<name>`) is a symlink into a checkout of the skills
     repository — read the link — and repository-owned when the current repository holds it under
     `.agents/skills/`, at any depth. A new skill goes to the skills repository when it reads generically
     once written and to the current repository when its correctness depends on a local contract.
     An agent definition that a shared skill runs on goes with that skill; every other agent, and
     every rule, is repository-owned.
   - A shared target is edited in the skills repository's checkout — the one the user-level link
     resolves to, or a fresh clone when the session has none — on its own branch and pull request,
     never through the link's path from another repository's branch.
   - `agent` -> `.agents/agents/<name>.md`
   - `rule` -> `.agents/rules/<name>.md`
   - `skill` -> `.agents/skills/<name>/SKILL.md`, or `.agents/skills/<folder>/<name>/SKILL.md`
     where the repository sorts its skills into folders; the folders group the source and never
     change the name a skill installs under.
   - Never read or write `.cursor/*`, `.claude/*`, `.codex/*`, or any other non-`.agents` agent or provider folder.
   - Do not manually create, update, or sync mirrored command/skill/rule files in those folders; repository automation propagates changes from `.agents` to Cursor, Claude, Codex, and similar targets. The one exception is a mirror the same change would leave pointing at a path it renames or deletes — a per-skill symlink into a directory the change moves — which is renamed in the same change so the branch never carries a dangling link.
   - This path restriction applies to the agent-content update, not to source changes required to fix an underlying issue from step 3.

5. Upsert behavior.
   - If target file exists, read it completely, then check it against **Skill shape** and **Output** below before making the requested change: a skill whose criteria sit inline gets a `references/` file, and a skill that returns a response with no `## Output` section gets one with its template, in this same edit and whether or not the request mentioned them, and list what they add among the files and sections the change makes. Then update it in place with the requested changes.
   - If target file does not exist, create it with a concise structure matching existing style.
   - Place new guidance under the broadest existing subject section that fits. Use durable topic headings rather than creating a heading for one requirement.
   - Express each independent requirement once, usually as one concise bullet. Merge overlapping or synonymous guidance without losing distinct criteria or exceptions.
   - Normalize the touched file's nearby structure when needed: combine narrow sections, remove redundant wording, and order foundational guidance before specialized concerns.
   - When adding a **new** restriction or rule, keep the wording **concise**—one clear statement or bullet per idea; do not pad with redundant sentences or multiple bullets that restate the same requirement.
   - **Stable guidance:** Write at the broadest scope that remains truthful. Describe reusable roles, boundaries, and decision criteria generically even in repository-focused guidance when the pattern is not repository-specific. Keep concrete repository names only when correctness depends on that local contract, and never turn one local example into an untrue universal rule.
   - **Prefer the broad statement, and let the request be its example.** A request arrives as one symptom, and the rule it needs names the class that symptom belongs to; the symptom stays as one illustration of it. Asked for `Final` on string constants, write `Final` for every module-level constant; asked for a walkthrough rule because a page reloaded in a loop once a back-end change was absent, write that the run is judged against intended behaviour because an API error surfaces as any unintended behaviour, and name the loop only as one instance. A rule written for the symptom is silent on the next one, and the next one is what it will be read for. Broaden to the class the user plainly meant, never to a neighbouring subject.
   - Keep reusable skill names, instructions, scripts, and interfaces model-agnostic. Name a client or model only in a scoped compatibility section where its behavior genuinely differs.
   - **A model the user names is written as a tier, with that model as one host's example.** "Use Sonnet agents" becomes "the host's mid tier — Sonnet on a Claude host, the equivalent tier elsewhere"; a request for the largest or smallest model is written the same way. The tier a skill's subagent runs on is stated in that skill's text, at the point it launches the subagent, never in a per-agent model override file.
   - **Refer to a skill, and to anything inside it, by the skill's name, never by path.** `the `code-simplify` skill's rubric reference` is right; a relative path into another skill's directory is wrong, because the directories move between repositories and user-level roots and the name is the only stable handle.
   - Declare every invoked skill by canonical skill name in a near-top `## Dependencies` section of the owning `SKILL.md`. That section lists skills only, never tools, plugins, scripts, references, assets, executables, or filesystem paths.
   - Invoke dependent skills only from the owning `SKILL.md`. References and other supporting files are passive and must not invoke skills or identify dependencies through relative paths to another `SKILL.md`.
   - Do not embed concrete repository file paths or copy code examples from the current codebase into `.agents` files; those go stale when files move or refactors land. Prefer generic placeholders (for example `services/<name>/...`), short pattern descriptions, or minimal invented examples that are not tied to live paths or current line-level code.
   - **A skill that reads generically belongs to every repository, so write it that way and put it in the skills repository.** Repository paths, product names, and domain nouns turn a reusable workflow into one repository's copy of it; keep them out unless the skill's correctness depends on that local contract, and where a skill genuinely needs one local fact, take it from the repository's `project.md` or a setting rather than baking it in. Where a shared skill needs a repository-specific collaborator — a migrations skill, a finalization skill, a deployment skill, a deferral label — it names the role and finds the skill by its description in the skill listing, and the repository's `project.md` **Repository Skills** table says which local skill fills the role.
   - Retain examples only when they clarify a non-obvious distinction; remove examples that merely repeat the prose.
   - Keep topic-specific restrictions with their topic. Keep an existing `## Guardrails` section at the bottom, and create one only for cross-cutting safety or preservation constraints.

   **Skill shape.** `SKILL.md` holds how the skill runs: its trigger, its dependencies, its
   workflow, its output, its guardrails. What a reader *applies* rather than *follows* lives in
   `references/<topic>.md` beside it, named for what it holds — a rubric, a checklist, a catalogue,
   a protocol — and `SKILL.md` names the file at the point the workflow reads it. A skill with two
   routes through it (two modes, two kinds of target, two hosts) keeps the shared workflow in
   `SKILL.md` and gives each route its own reference, so the file a reader loads first stays short
   enough to be read whole. A reference is passive: it states criteria and never a step, a
   dependency, or an invocation. Scripts the skill runs go under `scripts/`, assets it serves under
   `assets/`, and nothing else enters the directory: no provider metadata such as `agents/openai.yaml`,
   which stays outside repositories and is never propagated.

   **Description.** The front-matter `description` is read on every turn, for every skill, to decide
   whether this one fires. Its whole job is to state **when** — the situations that should reach it,
   in the words a task actually arrives in. What it does belongs there only so far as a reader needs
   it to recognise those situations; the body says the rest.

   So the slash command earns no space. It is the skill's own name, the listing already shows it, and
   a reader deciding whether to invoke has it in hand — `Invoke as /refactor to refactor a
   repository` spends its opening clause telling the reader something they used to get here. Keep the
   trigger and drop the command: `Use to refactor a repository, change request, branch, path, symbol,
   or concern.` The same goes for a phrase naming the skill, `Use this skill to`, and a restatement of
   the skill's title.

   Where an invocation carries an argument the trigger depends on, the argument is the thing worth
   naming — a target, a scope, a mode — not the command that precedes it.

   The opening sentence still says what the skill does, because a generated listing renders it as the
   skill's summary; the trigger follows it rather than replacing it.

   Judge a description by substitution: read it without knowing which skill it belongs to. If it still says which situations
   fire the skill, it works. If the remainder names no situation, it was never a trigger.

   **Output.** A skill whose result is a response the user reads — a listing, a report, a summary, a
   verdict, a draft — carries an `## Output` section as its last section before any `## Guardrails`,
   holding a hard-coded Markdown template the response is filled into: fixed headings, fixed list
   shapes, and a stated fallback for the empty case, so two runs on the same input read the same.
   A skill whose result is edits, a merge, a deployment, or a running system has no template to
   hold, and carries instead the report line its delivery step owes. The test is whether two
   correct runs should read the same shape; write the template when they should, and leave it out
   rather than forcing a shape onto a result that varies. That call is the editor's own, made from
   what the skill returns, never a question put to the user.

6. Multi-target behavior.
   - Apply multi-target updates for `agents`, `skills`, and `rules`.
   - When the inferred/selected type is singular (for example `skill`), distribute requested items across multiple files of that type as needed.
   - Update existing files when they already fit part of the request (for example update skill A and skill B).
   - Create a new file of that type when no existing file governs a requested item's subject (for example create skill C), after the question step 2 requires.
   - If one request contains multiple distinct items, map each item to the best existing file or a new file within the same inferred/selected type.
   - If scope is ambiguous, ask a short follow-up before editing.

7. Deliver it, in this order. Every call inside this delivery is the editor's own — a flagged
   gate, a smoke round that would not close — made and stated in the report, because a pull
   request confined to agent configuration is already authorized to merge, and a question asking
   for that authorization only holds every later session on the guidance the change replaces.
   Step 6's review of an altered example response is the one question this delivery puts to the
   user.
   1. **Branch and commit.** Put it on the agent-configuration branch already in flight when one is
      open; otherwise branch from the freshly fetched default branch. Commit only the `.agents`
      files (and a mirror the rename exception in step 4 covers) and open a pull request carrying
      nothing else. None of that waits to be asked: the decision was made when the edit was
      requested, and a pull request left open keeps every later session working from the guidance
      this change replaced. A source fix required by step 3 is a separate change on its own branch;
      the two never share a pull request, because one is authorized to merge and the other is not.
   2. **Run `validate_sources.py`**, which sits under `scripts/` beside this skill, before the pull
      request opens, and again before it merges when the branch changed since. Nothing on a pull request runs the sync: the workflow
      runs on the default branch after the merge, so a file it refuses is refused once every session
      is already reading it. The script installs the sync tool at the revision the workflow pins and
      mirrors the canonical tree into a scratch copy, so what it refuses is exactly what the workflow
      would. Run it from the root of the repository being edited, with that repository's own
      interpreter or any interpreter meeting the sync tool's version, and fix every
      report it prints before pushing; a description holding a colon followed by a space is the usual
      one, and quoting the value is the fix.
   3. **Run `code-simplify`** across the branch and act on what it reports: guidance duplicated
      between peer rules or peer skills, a section grown around a second subject, a heading named for
      a category with one member, a rubric left inline that the skill-shape rule sends to a
      reference. Prose duplicates as readily as code, and nothing else catches it. Every `.agents`
      change gets that pass, a one-line rule edit as much as a new skill: a single bullet added to
      the file that does not own it is exactly the duplication this catches, and it is the change
      least likely to be looked at twice.
   4. **Run `acceptance-gate`** with its diff question over the `.agents` diff, the request as the
      intent statement. It judges whether the guidance answers the request at the breadth step 5
      asks for and whether every mechanism it adds earns its place; a flag gets the one rewrite that
      skill allows, and the rewrite goes to a fresh gate. A second flag ends the rewriting: fix it
      when the flag names a defect in the guidance, merge as it stands when it names a preference
      the rewrite already answered, or drop the item when neither holds, and state which and why in
      the report, as that skill's **Bounds** leave it to the caller for a change whose merge needs
      no authorization.
   5. **Run `smoke-test`** for every skill the change adds, and for every edit that changes what a
      reader does — a step added, removed, or reordered, a decision moved, a criterion changed — to
      a passing table. The simplification pass settles how the guidance reads; the smoke test
      settles whether it changes what a reader does, against the miss that prompted it and with the
      original text as the control. An edit whose smoke run fails is revised and rerun within the
      rounds that skill bounds, never merged on the strength of reading well; a spent bound is
      decided as that skill says. A **mechanical seam edit** changes no behaviour and needs no smoke
      run: a dependency replaced by the role phrase that finds it, a path generalized, a rename, a
      frontmatter key, a reference path corrected, wording that says the same thing shorter. The
      report says `not run: mechanical seam edit` for it, and the acceptance gate is its check.

      **A skill that arrives by relocation is not a skill the change adds.** Moving one between
      repositories, or generalizing local copies into one every repository can adopt, produces a new
      file and no new guidance, and a smoke run against a miss nobody had proves nothing. What makes
      it a relocation is that the guidance survives, so establish that rather than asserting it:
      diff the new file against every original line by line, and account for each line the diff
      removes as either the same instruction in repository-neutral words or guidance relocated to a
      named home — the owning repository's `project.md` for what only that repository can state.
      A line carrying an instruction no original carried is an edit riding along, and the paragraph
      above decides it on its own terms. The report says `not run: relocation, guidance preserved` and names where each
      original's specifics went.

      Where the originals disagreed, the disagreement is the thing to get right, and neither answer
      may be picked for both. Carry the shared guidance and hand the contested question back to each
      repository, checking that each one already states its answer where the skill now sends its
      reader; a repository that does not is the flag, because the merge silently gave it the other
      one's answer.
   6. **Put an example response to the user, one skill at a time, for the skills whose response
      the user uses and whose response this change alters.** A summary they read, a listing they
      act on, a report they take a decision from: for each such skill the change adds, or edits in
      a way that changes what it returns, run the edited skill yourself on real current input — the branch in flight for a skill that summarises or reviews, the request in
      hand for one that edits, the smoke scenario only where no real input exists — and show what it
      returned, verbatim, then ask with the question tool whether to approve or reject it. The run
      is this session's own: a subagent's smoke report and a hand-written illustration both stand in
      for the behaviour and neither is it. Show the next skill only after the previous one is
      approved, never several in one question. On a rejection, ask what must change, revise the
      skill, rerun the smoke round for the models that missed when the wording changed, run it again
      yourself, and show the new response; loop until every such skill's example is approved. A skill
      whose result is edits, a merge, a deployment, a verdict another skill consumes, or a report only
      an agent reads has nothing the user would use and skips this step; so does a rule-only change,
      and so does an edit that changes how a skill works but not what it returns — a reordered step,
      a procedure moved to a reference, a check added on the way — since an unchanged response has
      nothing new to review. A relocation under step 5 skips it for that same reason: the skill
      returns what it returned before the move, so there is no altered response to put to anyone.
      Altered means the user would notice it in the response itself: a new
      column, a changed shape, a different grouping, a link where there was none. A new value in a
      status line or a reworded label is not that, and asking over it spends the user's attention on
      nothing. The decision is the editor's, from what the skill returns before and after the edit.
   7. **Check the diff file list against the default branch, then merge.** The authorization covers a
      pull request carrying only `.agents` files, so one file outside them withdraws it — and the
      one that slips in is never announced. Read the changed paths rather than trusting your memory
      of what you edited; a stray formatter run or a file picked up by `git add -A` looks identical
      to intent. Everything in `.agents`, merge it: a pull request carrying a skill change merges
      once step 6 approved every example, and one carrying only rules merges on sight as the GitHub
      rules say. Anything outside, move that file to its own branch first. A pull request a doctor
      run or `new-doctor` opens is left for the user instead; the steps above still run, the merge
      does not.
   8. **Nothing propagates.** The skills repository is the only copy of a shared skill, and every
      session reads it through its user-level link, so a merged edit reaches the next session on
      its own. A skill that reads generically but was written into one repository's `.agents` is
      moved to the skills repository in the same change rather than left as a second copy.
   9. **Read the merged text back before using it.** A merge changes the default branch, not the
      checkout: a session working on another branch still carries the old skill in its tree, and a
      skill invoked from there runs the text the change just replaced. After the merge, fetch the
      default branch and read every skill or rule the change touched from it — `git show
      origin/<default>:.agents/skills/<name>/SKILL.md`, and the references beside it — and run
      from that text for the rest of the session. A skill invoked while its change is still open
      is read the same way from the branch that carries it, never from a checkout that predates
      it.

## Output

Return this report, filled in; keep every heading and write `None` under one with nothing to list:

```markdown
Files

- `<repository>/.agents/<path>` — created | updated | deleted | renamed from `<old path>`

Changes

- <one sentence per change to the guidance>

Underlying issue

- <what was fixed and how it was verified, or `None`>

Checks

- Source check: passed on <head> | failed: <report>
- Simplification: <clean | findings applied>
- Acceptance gate: <accepted | rewritten and accepted | flagged twice: <fixed | merged as it stands | dropped> — <reason>>
- Smoke test: <passing table reported above | bound spent: <stands with the miss | edited again | dropped> — <reason> | not run: <reason>>
- Example approved: <one line per skill: name — approved after <n> round(s) | skipped, no response the user uses | skipped, response unchanged | rule-only change>
- Merged text read back: <default branch head the touched skills and rules were re-read from | not merged>

Pull request

- <link, with `skills repository` or `<repository>` after it>

Skipped

- <item and why, or `None`>
```
