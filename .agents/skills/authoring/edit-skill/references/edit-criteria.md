# Edit Criteria

Criteria this skill's **Behavior** steps apply while diagnosing a failure, placing an edit, writing
it and checking it. `SKILL.md` names the section each step reads; the order and gates stay there.

Contents: **Causal Diagnosis**, **Scope Statement**, **Shared Targets**, **Changed Output
Examples**, **Moved Text**, **Tools And Dependency References**, **Source Check Routes**, **Already
Reviewed Batches**, **Relocations**, **Resuming A Batch**.

## Causal Diagnosis

- Trace the actual path from the request to the missed behavior: whether the instruction was
  absent, its skill loaded, its trigger or sequence kept it from the decision, a conflicting
  instruction overrode it, or the agent failed to apply guidance it had. Read exceptions and
  stopping clauses with its callers. When the substantive rule is already correct, inspect the
  step that produced the rejected recommendation, triage, brief or action: what instruction and
  review evidence it used, what next action those required, and how its chosen action differed.
  Repair that decision step at its owner rather than restating the substantive rule or ending
  with a noncompliance report. Remove conflicting permissions and test other routes in the same
  failure class, and none outside it, then replay the original decision under the repair before
  closing the issue.
  Record missing historical evidence without inventing a cause; it does not prevent repairing
  the observed decision path. When the owning skill was not invoked, harden its frontmatter
  description first; body text cannot control a run that never loads the skill.
- Test the proposed instruction against that original decision path before proposing or writing it. If a
  reader could follow it and still repeat the miss, explain the mismatch to the user, name the
  instruction that actually caused or allowed the decision, and correct that owning path and
  its conflicting callers. Escalate a genuine unresolved choice, not permission for an already
  authorized repair. Do not mechanically apply a requested wording change or add a general
  reminder beside a stop rule it cannot override. The original scenario must demonstrate that
  the causal correction changes the reader's next action.

## Scope Statement

The statement is written before the edit, in the shape `SKILL.md`'s
**Output** gives, and revised when the written text turns out to change more or less than it says.

- **Each line says one thing the user can check against what they meant.**
  - *You said* quotes the user's words, each example value named by its kind in brackets as
    `pre-production`'s **Examples And Paths** says, in the ledger entry and every reviewer brief,
    never in the statement shown to the user, who wrote them; for a
    gap the agent noticed itself the shown statement opens with `Noticed:` and states the gap.
  - *From now on* names the situation, what agents do there and what they did before.
  - *Also changes, same class* lists every other situation of that class the edit changes, by the
    skill or rule that governs it.
  - *Stays as it is* names the nearest case outside the class, the one a broader reading of the
    user's words would have changed, and what agents still do there.
  - *Inherited without an edit* lists each skill, rule and flow that reads the changed text and is
    not itself edited, with what changes for it or `no change`.
  - *Beyond what you said, waiting for you* lists each change the edit does not make until the
    user answers.
- **Narrow probe.** Test the draft against the original decision path as **Causal Diagnosis**
  says: could a reader follow the text and still repeat the miss? Then test one further case of
  the same class that the request never mentioned, a different kind of thing from its examples. A
  case the draft would still handle as before means the draft only renamed the examples; it is
  rewritten until that case changes, and the case is listed under *Also changes*.
- **Broad probe.** Name the nearest case outside the class and read the draft, and every reader
  the inheritance search finds, for that case. It must be handled as before: a draft that changes
  it is narrowed until it does not, and the case is the *Stays as it is* line. Then ask of every
  item under *Also changes*, and every behavior change under *Inherited*, whether the user,
  reading only their own words, would expect it. An item that fails leaves the draft, moves to
  *Beyond what you said* and takes the policy-change route, while the rest proceeds.
- **Finding what inherits is a search the editing agent makes itself.** List the readers of each
  changed skill, rule and section as `skill-pass`'s **Source Check** says, then search the rules
  and skills by the subject of the changed decision for a reader that makes that decision without
  citing the text. For a rule that loads in every session or by file pattern, the inheriting
  skills are the ones whose steps make the changed decision. Read each hit's sentence in its
  context and state what changes for that reader.
- **Flow is affected** when any line names a changed step, launch, loop, invocation, borrow, read,
  count, scope or cap in how skills run, or a decision a neighboring skill or rule now makes
  differently: who decides, act or ask, keep or remove, stop or continue. The statement's heading
  records which, and a wording fix with no such effect records `flow not affected`.
- **What the statement feeds.** It is the intent statement the review and the acceptance gate
  receive, and its *Stays as it is* line reaches the skill test as the case a scenario must leave
  unchanged.

## Shared Targets

- A shared target is edited in the skills repository's checkout — the one the user-level link
  resolves to, or the main checkout behind it when the link resolves into `update-skills`'
  overlay worktree, or, when the session has no editing checkout, a writable checkout attached to
  or cloned into the session — on a branch and pull request in that repository, never through the
  link's path from another repository's branch. A cloud setup clone installed only to provide
  skills is not the editing checkout. Transfer the edit to a separate skills-repository session
  only when no writable checkout can be obtained, never by editing the installed clone. The
  originating session supplies the observed miss and its failure class, original task, relevant
  diff or small file set, repository commit, original skill text and the outcome the user
  requires, with a sanitized fixture when the skills session cannot read the originating
  repository. The skills session tests original and proposed wording against the same case and
  names the exact proposed pull-request head. For repository-dependent behavior, the originating
  session then replays the case against that head before merge as `test-skill` runs a scenario,
  its reader given that head's files, fetched or received as a scratch artifact, and carries the
  result across heads only as `test-skill` carries one. Do not assume a pull request
  automatically installs its skill.

## Changed Output Examples

- The changes that take a concrete example are any new or changed user-facing output shape — a
  table, a report layout, a sent file, a message template, a listing — in a skill whose response
  the user reads or acts on. It is changed when the user would notice it in the response itself: a
  new or moved column, a different grouping, a link where there was none. A new status value or a
  reworded label is not that, and a skill whose result is edits, a merge, a deployment, a verdict
  another skill consumes, or a report only an agent reads has no such response. Whether an output
  changed is the editor's call, from what the skill returns before and after. **Model the example
  on a small slice of the work in hand**, cut to a scope read in a minute, with every value the run
  would produce — numbers, hashes, findings — stated as made up. Write it as one markdown file
  whose first line is `**EXAMPLE — modeled on a small slice of the current work; no skill test
  was run.**`. Only where the work in hand gives the output nothing to show does the example use
  an invented scenario with invented names, first line `**EXAMPLE — fictional output; no skill
  test was run.**`. The example is task evidence: the skill text it leads to still keeps its own
  examples generic. Read it whole, write the
  skill to produce that shape, then validate it through the required skill-test run, review, and
  acceptance gate. A guidance-output format is routine guidance design, not a user approval gate; a change to the product
  a skill operates still follows `pre-production`'s **Product Choices**.

## Moved Text

Guidance moved between files — a skill relocated, bullets gathered into a new rule or out of one —
that lands beside a statement of the same requirement is merged with it into one in the same
change, keeping every distinct criterion and exception, and any other defect a standing rule names
that the move brings to light is fixed in it, as `pre-production`'s **Scope Follows The Defect, Not
The Request** says of a defect the work notices, with `acceptance-gate` judging the repair's scope
and size. Moving text unchanged proves it survived; it is never a reason to report a defect as
left for the user.

## Tools And Dependency References

- Treat a missing tool required to run, build, test, or review a repository as source work. First
  use a standard-library or already-provided equivalent when it fully serves the task; remove any
  existing repository dependency, bootstrap installation, and repository references it displaces,
  rather than leaving obsolete tooling behind. Do not add a dependency for an incidental harness.
  When the tool is essential, install it through the repository's bootstrap entry point, found from
  its README and tooling: extend it where it exists, create one only where none does, and verify a
  fresh bootstrap provides the tool. Keep that bootstrap repository-neutral — it serves every developer
  and agent, so its name, behavior, and messages must not be Claude- or Codex-branded.
- Follow the user's explicit consumer-reference choice, and otherwise `pre-production`'s
  **Versions**; use the default branch when the user chose it or applicable reference guidance
  permits it.

## Source Check Routes

When the sync tool cannot reach an imported skill's source repository, that is an environment
refusal, not a blocker: attach or clone the repository, and when the tool
fetches through a path the environment refuses, fix the tool to use one it serves.

When the guidance needs a change in an unreleased tool owned by another repository, point
the draft consuming workflow at that tool's active branch and validate against it, without
waiting for the tool's review loop. That workflow change is source work under **Branch and commit**'s source
route; its delivery follows `merge-gate`'s dependency gate rather than merging a testing reference.
The guidance rides that workflow's source pull request, as the GitHub rule's **Branches and
Pull Requests** says, and merges with it; that pull request waits for the tool through the
same gate. After the tool merges, the consumer adopts and validates its maintained target under **Tools And
Dependency References**. No merge here authorizes a release.

## Already Reviewed Batches

A workflow that fixes guidance under its own review, such as a doctor run, hands the route a head
it has already reviewed and accepted. The route takes that review and acceptance as its own when
the invocation supplies all of these for the batch's complete `.agents` diff at its current head:

- an independent review whose confirmed findings are resolved;
- an independent final acceptance by `acceptance-gate`, read after that review;
- the brief both readers were handed, which is `skill-pass`'s **Reviewer Brief**, with the
  workflow's intent statement where no Scope Statement exists.

The route then runs **Run `validate_sources.py check`** and
**Run one `test-skill` round** for the guidance the diff changed, started on that head, and no
`review-pass`. A repair the skill-test round makes goes through `review-pass` over its delta, as
**Guidance Delivery**'s **Conclude the skill test** says, and a head that moved since the acceptance for any other reason
is a batch like any other. The pull request then merges or holds as the handing workflow's
delivery rule and the GitHub rule's **Merge Authorization** say.

Every other batch takes the short or the full route, whatever started it.

## Relocations

Moving a skill between repositories, or generalizing local copies into one every repository can adopt, produces a new
file and no new guidance, and a skill-test run against a miss nobody had proves nothing. What makes
it a relocation is that the guidance survives, so establish that rather than asserting it:
diff the new file against every original line by line, and account for each line the diff
removes as either the same instruction in repository-neutral words or guidance relocated to a
named home — the owning repository's project guidance for what only that repository can state.
A line carrying an instruction no original carried is an edit riding along, and
**Run one `test-skill` round**'s skill-test round decides it on its own terms.

Where the originals disagreed, the disagreement is the thing to get right, and neither answer
may be picked for both. Carry the shared guidance and hand the contested question back to each
repository, checking that each one already states its answer where the skill now sends its
reader; a repository that does not is the flag, because the merge silently gave it the other
one's answer.

## Resuming A Batch

Read every entry in the frozen batch and resume at its recorded first
nonterminal stage, rebuilding a lost or truncated entry from its backup
comment as `session-ledger` accepts it; the comment's existence records that the correction was admitted under **Recording During A Task**, its Intended behavior stands as the recovered intent for **Guidance Delivery**'s **Review the batch** beside the user's words, taken from the conversation where they survive and otherwise named as missing in that intent, never replaced by that paraphrase, and **Run one `test-skill` round**
rebuilds the reproduction scenario from its failure class and invariant, with anything else
unrecoverable handled as `session-ledger` incomplete retrieval. An entry with no recorded commit
applies its edits under **Write the edit** and **Split a multi-item request**, on the branch **Branch and commit** selects; one with a
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
source check and skill-test round pass, so its batch can be done.
