# Recording During A Task

How a guidance correction is recorded, where its edit is written and when it is delivered; read from **Recording During A Task** in `SKILL.md`.

Honor the selected workflow's verification sequence and any delivery or installation hold when
recording or delivering a batch.

- A process correction is classified at once and written only when its verified run or merge is
  available, as **A process is encoded only once it has worked** says; any other correction is
  recorded once diagnosed.
- A direct request to change guidance, such as "use edit-skill to reflect that", is recorded the
  same way. While another task runs, the requested action is the behavior it describes, applied to
  the current work, and the guidance edit is its record. While a guidance batch is in flight, its
  delivery is that action and the user's words are its evidence.
- Record the correction as a `guidance_correction` entry with `session-ledger`: the user's words, if
  any, quoted as `pre-production`'s **Examples And Paths** says, the evidence of the gap, and for a
  process its verified run, a reproduction scenario, the Scope Statement **Identify the failure class** writes,
  whose From now on line is the entry's intended behavior, the canonical files it will change, and
  `pending` as its `status`. **Validate input** through **Resolve which repository owns the target** run at once, while the evidence
  is fresh, to fill the entry; the edit itself (**Write the edit**, **Split a multi-item request**
  and **Branch and commit**) is written as the bullet
  below on writing it says, and delivery from **Run `validate_sources.py check`** onward waits.
- **A recorded correction governs the rest of the session at once**, ahead of the installed text it
  amends. Before a decision a pending entry's subject covers, read the ledger's pending entries and
  follow their intended behavior. Putting a question or a recommendation to someone is such a
  decision, as much as acting is: the entry decides what it carries. Recording a correction and then
  repeating the miss it records is the failure this section exists to prevent. What an entry's
  Scope Statement lists as waiting for the user governs nothing until they answer. A pending entry may
  restate or tighten the installed text, never grant an authorization the global rules' **Authorization** or the GitHub rule reserves to
  the user's own words. A brief to any worker whose task a pending entry's subject covers carries that
  entry's intended behavior, with the user's words quoted and the installed text it amends named.
- Write the edit in the checkout **Resolve which repository owns the target** resolves, on the branch **Branch and commit** selects — the batch's own
  branch while a batch is in flight and its pull request has not merged — commit it, and push it to
  that branch's pull request once the checks the GitHub rule's **Pre-Push Gate** defines pass, opening a draft when the branch has
  none; this holds for a source pull request **Branch and commit** selects as for an agent-configuration one.
  When the checkout holds the active task's uncommitted or source-branch work, write and commit the
  edit from a separate worktree on the selected branch, leave the task's tree untouched, and stage
  only the guidance files. Record the branch, the `commits` list and the pull request in the entry's
  `data`, bring that pull request's description up to date at the milestone, then run `update-skills` at once for eligible edits under its **What Takes Effect**, so the installed
  copy every agent loads, subagents included, carries them. A running agent keeps the text it
  already read: tell each running worker this session started, as `subagent-matrix`'s **Dispatch** says. Nothing else of delivery runs while the task does: no
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
