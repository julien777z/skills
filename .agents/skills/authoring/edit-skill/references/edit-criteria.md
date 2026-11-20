# Edit Criteria

Criteria this skill's **Behavior** steps apply while diagnosing a failure, placing an edit, writing
it and checking it. `SKILL.md` names the section each step reads; the order and gates stay there.

## Causal Diagnosis

Read at **Behavior** step 2.

- Before editing, trace the actual path from the request
  to the missed behavior: whether the instruction was absent, its skill loaded, its trigger or
  sequence kept it from the decision, a conflicting instruction overrode it, or the agent failed
  to apply guidance it had. Read exceptions and
  stopping clauses with its callers. When the substantive rule is already correct, inspect the
  step that produced the rejected recommendation, triage, brief or action: what instruction and
  review evidence it used, what next action those required, and how its chosen action differed.
  Repair that decision step at its owner rather than restating the substantive rule or ending
  with a noncompliance report. Remove conflicting permissions and test other routes in the same
  failure class, then replay the original decision under the repair before closing the issue.
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

## Shared Targets

Read at **Behavior** step 4.

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

Read at **Behavior** step 5.

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
  examples generic. Read it whole and send it as `share-media`'s **What reaches the user, and when** says, write the
  skill to produce that shape, then validate it through the required skill-test run, review, and
  acceptance gate. A guidance-output format is routine guidance design, not a user approval gate; a change to the product
  a skill operates still follows `pre-production`'s **Product Choices**.

## Tools And Dependency References

Read at **Behavior** step 5.

- Treat a missing tool required to run, build, test, or review a repository as source work. First
  use a standard-library or already-provided equivalent when it fully serves the task; remove any
  existing repository dependency, bootstrap installation, and repository references it displaces,
  rather than leaving obsolete tooling behind. Do not add a dependency for an incidental harness.
  When the tool is essential, install it through the repository's shared `bootstrap/install.sh`:
  create that entry point when it is absent, or extend it when it exists, and verify a fresh
  bootstrap provides the tool. Keep that bootstrap repository-neutral — it serves every developer
  and agent, so its name, behavior, and messages must not be Claude- or Codex-branded.
- Follow the user's explicit consumer-reference choice; otherwise, after a dependency receives a
  separately authorized release, replace its branch reference with a maintained version tag. Use
  a minor release for a new capability or a patch release for a bug fix; verify any moving major
  tag points to that release and validate the consumer against it. Never use an unpublished tag;
  use the default branch when the user chose it or applicable reference guidance permits it.

## Source Check Routes

Read at **Behavior**'s **Run `validate_sources.py check`**.

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

## Relocations

Read at **Behavior**'s **Run one `test-skill` round**.

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
