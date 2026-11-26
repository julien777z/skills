# Vendor Rubric

Contents: how a passage is judged; the checks, grouped as prohibitions and firm rules, what to
leave out, structure and size, and model behavior; where the sources disagree and what this
repository chose; the evidence a cut needs.

This reference holds what the model vendors' skill and prompting guidance asks of agent guidance,
restated as checks for this repository. The pass in `SKILL.md` applies it to every instruction it
covers, and the source check's `wording` command lists where to look first. Each check gives the
principle, what a violation looks like, the better form, and how firmly the sources state it:

- **stated** — several vendor pages say it outright;
- **one source** — a single page says it, or it is written for one model family;
- **implied** — it follows from what the pages say and none says it directly.

The pages behind a check are named by kind: the skill best-practices page, the coding agent's
skills and memory pages, the general and per-model prompting pages, the vendor's own skill-writing
skill, its engineering posts on skills and context, and the prompt audit that ships with the
coding agent.

## How A Passage Is Judged

Read the file whole, then judge each prohibition and each firm rule in it as one of four:

- **Keep.** The passage carries something the model cannot know or still gets wrong. Say which:
  - a fact about this repository: the owner's standing permissions and limits, a contract, a
    convention that differs from common practice, a reason behind a constraint, stated once in the
    file that applies it;
  - a failure the repository's correction record shows agents still making with the passage's
    subject, where the passage names that failure;
  - a named default the model falls back on, as **Named Defaults** covers.
- **Reword.** The substance stays and the form changes: the goal and its reason in place of a
  prohibition, an absolute given its scope, or the action to take in place of the action to avoid.
- **Merge.** Several passages share one reason; that reason is stated once at its owner and the
  rest go.
- **Cut.** The passage restates what a current model does unprompted, repeats another owner, or
  is a generic caution with no repository fact in it. A cut that rests on what the model already
  does meets **Cutting A Passage** first.

**A passage's subject protects nothing.** Wording about authorization, merging, deployment,
release, security or data loss is judged like any other. The line that records who may merge and
what the owner has pre-authorized is a repository fact and is kept, once, at its owner. A line
telling the reader to be careful with a release, or repeating that permission in a third file, is
a generic caution or a restatement and is reworded, merged or cut on the same evidence as a line
about formatting.

## Prohibitions And Firm Rules

### Goal And Reason Over A Prohibition

- Principle: describe the result wanted and why. A list of what to avoid is weaker than a
  description of success, and a prohibition against a mistake the model was not going to make can
  pull it toward that mistake. A reason lets the reader judge the case the rule did not foresee; a
  bare rule gets applied where it does not fit.
- Violation: three or more prohibitions in a row; a "never" tail on sentence after sentence; a
  requirement with no reason and no named consequence near it.
- Better form: one sentence stating the result and its reason, with the unwanted case kept as a
  single illustration only where it is a real, repeated miss. "Export the stock list as CSV, never
  as a spreadsheet, never with merged cells and never without a header" becomes "Export the stock
  list as CSV with one header row, because the importer reads the first row as column names."
- Firmness: stated, for the positive form and for the reason. The reason is a clause attached to
  the requirement, never an account of how the rule came about.

### Absolutes

- Principle: the newest models apply "never", "always" and "only" exactly as written, including
  to a step the person in charge has approved. A firm rule therefore carries its scope, its
  exception and its reason in the same bullet, or is written as the action to take.
- Violation: "Never restart the queue worker" where the same file, another file or plain sense
  allows a restart in some case; an "always" whose reason covers fewer cases than its words.
- Better form: "Restart the queue worker only when no job is running, because a restart drops the
  job in flight", or the action form, "Check that no job is running before restarting the queue
  worker." The action form keeps the reader responsible for the step where the prohibition form
  makes it refuse.
- Firmness: stated, with a vendor measurement, for the newest model family. The authoring
  reference's **Writing** holds the repository's rule on an absolute.

### Emphasis

- Principle: importance is carried by a plain sentence and its reason. Capitals, words such as
  "critical" and stacked intensifiers make a current model over-apply the rule they mark, and
  when many lines carry them none stands out.
- Violation: a capitalized imperative, "do not skip", a repeated warning, emphasis with no reason
  beside it. A bold lead that is itself a prohibition counts when most bullets of a file open that
  way.
- Better form: the sentence at normal weight with its reason. A rule that holds every time with
  no exception becomes a hook, as **Scripts And Hooks** says.
- Firmness: stated for capitals and intensifiers; implied for bold leads. A bold lead that names
  a bullet's subject so it can be cited is a label and passes.

### One Principle Over Incident Patches

- Principle: many narrow conditions, each added after one incident, read as a maze, and the
  reader fails in the gaps between them. The principle they share is stated once.
- Violation: a paragraph in which each sentence is a separate "such as …, never …" case; a rule
  that grew a clause per correction; one session's stumble written down as a permanent rule; a
  single rule stated for the one instance that prompted it while its own reason covers a class.
- Better form: the shared reason, with one or two illustrations of different kinds. A fact about
  the environment that defies a reasonable assumption is different: such facts are kept and may
  accumulate, since no principle predicts them.
- Firmness: stated. The authoring reference's **Writing** bullet on a correction that restructures
  its bullet applies it to each edit.

### Approval Rules Name The Actions

- Principle: a broad rule to ask first holds back routine work, and telling the reader to act
  more freely is too vague to undo it. Name the actions that need the user's word and the routine
  steps that need none.
- Violation: "Ask before any outside action"; several scattered cautions about asking.
- Better form: "Sending a message to a customer and changing a price need the owner's word.
  Reading the catalog, drafting a reply and running the test suite do not."
- Firmness: one source, the newest model family's prompting page, which also says to keep a
  confirmation step for an irreversible action.

### Named Defaults

- Principle: where the model has a known default it falls back on, a list of the specific
  defaults to avoid works and a vague instruction to avoid the generic only swaps one default for
  another. This is the one place a list of things to avoid is the right form.
- Violation: rewriting a list of observed defaults into a general positive line; a list of
  defaults nobody observed the model produce.
- Better form: the short list, each entry something the model produced, placed after the positive
  sentence it belongs to.
- Firmness: one source, for visual and interface design on one model family. It limits **Goal And
  Reason Over A Prohibition** for design guidance and nowhere else.

## What To Leave Out

### What The Model Does Unprompted

- Principle: guidance holds what only its author knows. General engineering practice, default
  behavior and encouragement cost attention on every read and return nothing.
- Violation: general virtues such as "readable" or "well structured"; common practice restated;
  lines telling the reader to be thorough, to keep going or not to be lazy.
- Better form: the passage is cut, or replaced by the repository fact it stood near. The test is
  whether the reader would get the work wrong without the line, and an unsure answer is tested as
  **Cutting A Passage** says. Length alone justifies no cut.
- Firmness: stated.

### Thinking, Tools And Parallel Calls

- Principle: how hard the model thinks is set by the host's effort setting, never by prose. A
  current model calls independent tools in parallel unprompted, and a request to write out its
  reasoning in the answer can be refused.
- Violation: "think carefully", "plan before acting", "show your reasoning", a required reasoning
  field in an output, "use tools only when necessary", "run these calls in parallel".
- Better form: the line is removed; where a skill needs deeper thinking it sets the effort its
  host's frontmatter supports, inside a scoped compatibility section.
- Firmness: stated.

### Text Written For Older Models

- Principle: guidance is written for the model that reads it, and each model generation needs a
  fresh read. A compensation for an older model's weakness causes the opposite fault in a current
  one, and a new generation can need text added as well as removed.
- Violation: a retired model's name; fixed word caps and "summarize every N steps" rules; a ban
  on formatting or narration written to stop an old habit; a hard style rule such as one
  instruction per sentence, which a current model follows closely enough to make its prose choppy.
- Better form: the current rule alone, with length described in words. Text that makes the agent
  finish authorized work and report it plainly stays, because the newest models can stop early.
- Firmness: stated. The authoring reference's **Writing** covers text that says what changed.

### Volatile Facts And Terms

- Principle: one word names one thing throughout, and guidance holds no fact that dates.
- Violation: two names for one thing; a version, port, path or command copied into guidance.
- Better form: as the authoring reference's **Where Guidance Lives** says of tooling.
- Firmness: stated.

## Structure And Size

### Steps Matched To Fragility

- Principle: exact steps where one sequence is safe and a slip is costly; a goal, its limits and
  the check that proves it where the work needs judgment.
- Violation: numbered choreography for a review, a design or a diagnosis; loose prose for a
  history rewrite, a migration or an authorization flow.
- Better form: for judgment, the outcome, the constraints and how to verify; for a fragile
  operation, the exact commands in order.
- Firmness: stated.

### Description As The Trigger

- Principle: the description decides whether the skill loads. It says what the skill does and
  the kinds of situation that reach it, in the third person, main use first.
- Violation: a description past the open specification's 1,024 characters; a growing list of
  near-synonymous trigger phrases; procedure the body should hold; urgency in the body.
- Better form: what it does, then the categories of situation. The authoring reference's
  **Descriptions** holds the repository's criteria.
- Firmness: stated for the limit and the third person; the sources disagree on urgency, as the
  table below records.

### Progressive Disclosure And Size

- Principle: the entry point is short, a reference loads when the task needs it, and what loads
  in every session is smallest of all, since each of its lines takes attention on every task and
  a long file lowers adherence to all of it.
- Violation: a file past the budget the authoring reference's **Writing** sets for how it loads;
  a reference past 100 lines with no contents list; a reference that sends the reader to another
  reference; "see the references" with no word on when; a procedure, an example or a narrow case
  in an always-loaded file.
- Better form: the entry point split by route, each reference named with the condition that calls
  for it, and the most important instructions near the top, since a host that compacts a session
  keeps only the start of each invoked skill.
- Firmness: stated. A line count undercounts a file written one paragraph per line, so the token
  figure is read beside it.

### Examples

- Principle: the reader copies an example's length, tone and structure, and a single example
  becomes the rule.
- Violation: one "such as" per rule, each the incident that prompted it; a quoted string a reader
  may reuse word for word; an example of a judgment the model already makes.
- Better form: two illustrations of different kinds, marked as illustrations, or none where the
  rule is clear without one.
- Firmness: stated for the risk. The same pages still recommend examples, so the direction is
  fewer and varied, never none.

### One Owner

- Principle: a requirement stated in two files drifts, and a reader given two wordings spends
  effort reconciling them or picks one arbitrarily.
- Violation and better form: as **Prose Duplication** and **Conflict Check** in `SKILL.md` say.
- Firmness: stated. A copy that agrees with its owner and helps at the point of use is working
  redundancy, as the authoring reference's **Writing** allows; consolidate where copies disagree.

### Scripts And Hooks

- Principle: a step that must come out the same every time is code, and a rule with no exception
  is a hook or a deny rule, since prose is a guideline a reader may decide does not apply.
- Violation: arithmetic, parsing or validation described in words; a firm prose rule a hook could
  enforce, such as one against editing a generated file.
- Better form: the script or hook, and one line of guidance saying what it guards.
- Firmness: stated. A hook suits only a rule with no exception.

## Model Behavior

### Subagents

- Principle: a standing instruction to delegate is a habit from older models. A current model
  delegates as its prompts invite, and subagents are a large share of what a session costs.
- Violation: "delegate nontrivial work to subagents" with no condition; a fan-out with no count
  or cap; a second agent handed the same task in the hope of a better answer.
- Better form: what a subagent adds to the cost, when it pays (independent parallel work, a fresh
  reviewer, noisy output kept out of context), when to work directly, and how to brief one.
- Firmness: stated for the newest model family. The authoring reference's **Subagents** and
  **Flows** hold the repository's criteria.

## Where The Sources Disagree

| Topic | One reading | The other | This repository's choice, and why |
|---|---|---|---|
| Giving the reason | The prompting pages and the skill-writing skill: explain why | The coding agent's skills page: state what to do without narrating how or why | A reason clause on the requirement and no history, since a reason generalizes and a narrative only dates |
| Urgent descriptions | The skill-writing skill: make descriptions a little pushy, because skills under-trigger | The general prompting page: text written to fix under-triggering now over-triggers | Urgency only in a description and only where a trigger test shows the skill under-fires; none in a body |
| Strong words | The skill best-practices page shows capitalized "must" and "always" | The coding agent's pages, the skill-writing skill and the prompt audit: emphasis over-applies | Plain weight, since the best-practices page predates the newest models on this point |
| Lists of things to avoid | The prompting pages and the prompt audit: say what to do | The per-model page for design work: named defaults to avoid work | Positive by default; a list of named defaults stays in design guidance |
| Lists of gotchas | The open skill-writing guide: add each correction to a gotchas list | The prompt audit and the newest per-model page: cautions pile up | Environment facts accumulate; behavioral cautions are generalized into their principle |
| Checklists and steps | The skill pages: checklists for multistep work | The prompt audit: choreography degrades judgment work | Steps where order is the point, as **Steps Matched To Fragility** says |
| Delegation | The general prompting page: the model delegates well unprompted | The newest per-model page: remove lines that push delegation | The newer page, with a stated count and cap wherever a skill starts agents |
| Finishing | The coding agent's page: "keep going" lines cause over-work | The newest per-model page: the model can stop early, so add finishing text | Keep text that finishes authorized work and forbids ending on a promise; cut general encouragement |
| Contents list threshold | The skill best-practices page: past 100 lines | The skill-writing skill: past 300 | 100, the published platform figure |
| Size of a rules file | The coding agent's memory page: under 200 lines per always-loaded file | The skill pages: under 500 lines for a skill body | Both, by how the file loads, as the authoring reference's **Writing** sets out |
| What a description carries | The prompt audit: a description routes and does not instruct | This repository's **Descriptions**: it also carries a rule that binds before the body is read | The repository's, because a reader often acts on the description alone; such a rule is kept to one clause |

## Cutting A Passage

A cut that rests on what the model already does is a hypothesis until a run supports it, and one
good run supports nothing. The pass starts no run; it records the passage as a cut candidate with
its reason, and the workflow applying the pass runs the trial where it has the means.

- **The trial.** A bounded task the passage governs is run with the passage removed from the
  guidance the run loads, and judged against the outcome the passage itself states.
- **Repeated.** The task runs twice without the passage and a third time when the two disagree. A
  cut is recommended only when the runs agree that the outcome holds without the passage.
- **At the standard capability level**, never cheap: the question is whether a current model of the
  strength that reads the guidance still needs the passage, and a cheaper model does worse than
  that reader, so it keeps text the reader no longer needs.
- **Bounded.** Outside a doctor run, which tries every candidate, at most five passages are tried in
  one audit or delivery, those in files loaded in every session first, and the rest are reported as
  untried candidates and stay as written or are reworded.
- **What needs no trial.** A restatement of another owner is settled by reading both passages,
  and a merge or a rewording keeps the substance. Only removing substance on the ground that the
  model already has it needs the trial.
- **What the trial cannot settle alone.** A firm rule the owner stated records the owner's own
  judgment, so the runs alone never cut it: it is cut on the owner's word, or by a workflow the
  owner has authorized to decide such cuts, which records the runs beside the cut.
