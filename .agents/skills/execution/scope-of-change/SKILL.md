---
name: scope-of-change
description: "What a change takes on: the problems it fixes, how far it reaches, the pull request it rides, and the decisions it makes rather than asks. Read before planning, fixing, reviewing or gating a change, when a check fails or work turns up a problem, and before putting a decision to the user. Covers classifying a failing check against the default branch, which checks must pass, a lint or formatting check red on unwritten code, a hosted attempt a runner interrupted, what a defect is and how far its fix reaches, repairing the design behind a defect, a limit with no evidenced requirement, why today's deployment size never sets the design, side work and its pull request, a package consumed through a branch reference, the cleanup size budget, deferral grounds and widening it when the user says \"widen scope\" or \"clean up what you find\", a better shape than the repository's, a correction to one screen against a rule, product choices against routine details, restoring intended behavior, and surfacing trade-offs."
short_description: 'Decide what a change fixes, carries and leaves, and which of its choices go to the user.'
user-invocable: false
---

# Scope Of Change

A change takes on the whole shape of the problem it repairs, fixes every defect it meets, carries
its side work where one careful review can read it, and puts to the user only the choices that are
theirs.

## Dependencies
- `pre-production`
- `session-ledger`

## Encountered Issues

- **Classify validation failures first, before the failure is diagnosed, handed to a worker, or
  mentioned to the user.** Read the default branch's latest run of the
  same check, hosted or local, and reproduce there only when no such run exists. When that evidence
  establishes the same failure under comparable inputs, and the change neither introduces nor
  worsens it, record the check and that evidence as a baseline failure in the task's record, which
  every later gate receives. A test already
  failing on the default branch is recorded this way and left. Continue the requested work
  and its relevant validation; do not repair, rerun, investigate further, ask a product question, or
  record a deferral for that failure merely because validation encountered it. **Nothing the user
  reads names a baseline failure or says one was left out**: no report, summary, status list, open
  item or question, apart from a merge that branch protection rejects for it, whose rejection is
  reported with its provider evidence. No report claims the excluded check passed either; it
  covers the checks the change answers for. This exclusion does not cover a defect the user assigned, a suite past its
  runtime budget, deprecated usage or a printed warning, as the
  deprecated-usage bullet below says, a failure of the behavior the task must establish,
  a non-essential check's finding the next bullet has the change fix,
  or a confirmed finding independently established by a review or source inspection apart from
  diagnosis of the excluded check. Do not reopen an exclusion by relabeling that same failure as a
  review or source finding. Assigned defects and independent findings remain fix responsibilities
  even when older code caused them.
  Missing comparison evidence is not a baseline exclusion; inspect the failure at its native owner
  before choosing its disposition. Pass established exclusions and their evidence to every later
  validation or merge gate.
  A brief that hands a validation failure to a worker carries the classification's result, and
  never asks the worker to fix a baseline failure. A baseline failure's cause, even one only the
  user could remove such as a provider setting or credential, is never put to the user as a gate or
  a request, apart from that rejection.
- **Only essential checks have to pass: the test suites, and only for what the change answers for.**
  A non-essential check, such as lint, formatting or other static analysis, that fails on findings
  in code the change did not write may stay red. That holds whether the findings predate the change
  or the change brought them to light, such as a new lint rule meeting existing code or a
  changed-file lint run meeting older code in a file the change edits. Fix the findings in lines the
  change writes, and the other findings in a file the requested work itself edits, the callers and
  consumers it must update included, while they fit the size budget in force below, measured as it
  measures cleanup. Leave the rest for later work on that code: it is not deferred work, so it is
  neither recorded nor reported. Never fix past that to turn the check green, and never loosen, disable,
  rescope or ignore the check. A status report covers only the checks the change answers for, so it
  neither names this red check nor asks about it, apart from a merge branch protection rejects for
  it, reported as the bullet above says. A finding that
  shows a defect, such as deprecated usage or a vulnerability, stays one, fixed as the bullets below
  say. A finding the change's own code or contract change causes is the change's wherever it points:
  a changed signature whose untouched callers no longer type-check is fixed in those callers, as
  `pre-production`'s **Target Contract** requires. An essential check that already fails on the
  default branch is a baseline failure, handled as the bullet above says.

Fix and validate every defect that remains in the task, even when it predates the task or sits
outside the initial file set; cleanup that fixes no defect follows the size budget below.
Follow the evidence through affected callers and owners. That obligation is not a license to audit
areas the evidence never reaches, and the section below governs how far it reaches.
The repair must satisfy `pre-production`'s **Target Contract**; an encountered failure never
authorizes compatibility with an obsolete owned contract or revision.

- **A hosted check a runner or provider interrupted is an excluded attempt, never a pipeline
  defect to fix.** A package index serving no candidates, a registry or network timeout, a runner
  fault: where the logs establish the interruption without a validation failure, the attempt
  supplies no validation result and is excluded as the GitHub rule's validation-exclusion bullet
  says, with the run, the interruption evidence and the matching local commands and results
  recorded. The pipeline is not changed to survive it, and the job is not rerun or waited on merely
  to get a green hosted result. A recorded validation failure stays a failure, such as a test that
  passes only on a second try: it is classified as the first bullet above says, and re-running the
  job is never its fix.

## Scope Follows The Defect, Not The Request

- **The scope of a change is the whole shape of the problem, not the files the request happened to
  name.** A reported symptom is where the defect surfaced, not its boundary. When the same defect
  appears beside it — a second implementation of the mechanism, a sibling path answering the same
  question from a different input, a parallel copy nobody reconciled — that is one piece of work, the
  change's own scope rather than incidental work under the size budget or an item left for later,
  and splitting it leaves the half that stays behind as the version the next person extends. The
  repair itself, the defect no longer showing anywhere, is always in scope. A repair whose visible
  effect beyond that reaches surfaces the user did not name, such as a shared component's new
  layout reaching every page that uses it, is a proposal for those surfaces, put to the user as
  **Product Choices** says, unless a standing rule names that shape a defect.
- **A parallel copy is reconciled by giving the mechanism one owner, never by keeping the copies in
  step.** Making copies identical, a test that they match, or a note to update both leaves the
  second mechanism in place. Pick the owner by the fewest-mechanisms test, across repositories as
  within one, move every consumer onto it and delete the copies.
- Establish the defect's boundary from the failed behavior, violated invariant, and mechanism that
  produces it. Repair every affected implementation and consumer of that mechanism, including
  necessary generated contracts and retained-data migrations. Sharing a directory, a naming
  convention, or a general quality rule does not make separate mechanisms the same defect.
- Useful local refactoring belongs with the repair when it simplifies the affected owner and its
  necessary consumers. Before applying it, trace the complete change it requires and judge the
  cumulative scope against its gain. An import update, a moved declaration, or a file opened for
  comparison does not start another cleanup of that consumer or its siblings. Choose the smallest
  coherent repair, not the fewest lines at the expense of a complete contract.
- Distinguish required repairs from optional structural improvements before widening the work.
  Fix confirmed broken behavior and defects introduced by the change; assess independent cleanup
  against the size budget below. Do not turn a sequence of individually useful
  cleanups into an unrequested redesign, or invent an umbrella concern to make them one defect.
  An explicitly requested broad refactor still receives its stated scope. File counts are evidence
  of spread, not a cap on the repair itself: a necessary migration may be wide, while a small
  unrelated rewrite may already be disproportionate.
- **Incidental work goes one hop, never further.** What the work notices while making the requested
  change — in a file it opened, a check it ran, a capture it read — is a defect, fixed as below, a
  non-essential check's finding, decided by the essential-checks bullet above, or cleanup, handled
  under the size budget below. Under the default budget, a file opened or edited only to make such
  an incidental fix is never itself a source of more incidental work: what else it holds is not
  chased, neither fixed nor recorded, and its non-essential checks' findings are left as the
  essential-checks bullet says.
- **A defect is anything the system does or shows that a reader would call broken**, and the system
  includes the repository's tooling: its tests, fixtures, build, setup and CI. An image that never
  loads, a wrong value, a state shown in the wrong place, a control that does nothing, a lost write
  or notification, a crash, an exhausted budget, a test suite the change leaves failing in a fresh checkout, a
  fixture that builds data the code would never hold, and a setup step or documented command that
  errors are its familiar shapes, not its boundary. A test already failing on the default branch is
  a baseline failure, recorded and left as **Encountered Issues** says, never a defect to
  investigate or repair.
- **Slow, unbounded or fragile work is a defect too.** Work the system cannot finish in useful time,
  a resource that grows with the data with nothing to bound it, a stored value nothing limits, work
  a restart throws away where a sibling phase keeps its place, and a job that only advances because
  a container happens to stay alive are defects of the same standing. "The result is still correct",
  "it only costs time" and "how much to keep is a policy question" describe a defect and never
  exempt one; a system that is right and too slow to use is broken. A missing safeguard is not a
  defect, since the system does what it was built to do, unless its absence is an exploitable
  security finding, because what the system does includes what an attacker can make it do.
- **Deprecated usage and printed warnings are defects.** An API, setting, default, input or
  dependency its owner has deprecated, and any warning a test run, build, install or CI log prints,
  is fixed where the next bullet places a noticed defect's fix: move to the supported replacement, or turn on the default the
  owner says is coming; a dependency that itself calls deprecated code is upgraded or replaced,
  apart from a narrow ignore for a defect inside a third-party package that nothing the
  repository controls resolves. A check a library warns it will start
  enforcing is deprecated usage when left off, never a missing safeguard. The replacement changing
  behavior, such as a stricter check, a refused token or a different sign-in, is part of the fix,
  never a reason to keep the deprecated form, call it pre-existing, or put the move to the user;
  released users move as `pre-production`'s **Product State** migration bullet says. Only a step
  the move needs that the user alone can take, such as supplying an identifier the session cannot
  read, goes to them, as that step.
- **A defect the work notices is always fixed.** The hop limit above does not bound it, and neither
  does its home: a shared component, an owned library or another owned repository. Use the GitHub
  rule's **Branches and Pull Requests** to place the fix in each affected repository. A defect the
  change introduced or the requested behavior cannot work without stays part of the change at any
  size. **Every other noticed defect is placed as the side-work bullet below says.** Use the GitHub
  rule's **Pre-Push Gate** for a dependency it needs. A defect is never deferred, left as a note or
  offered to the user as a question. **A suspected defect whose confirmation is in the agent's
  reach** — a run, a walk through the product, a measurement with its own tools — is investigated
  now and, if it confirms, fixed and placed as above; that it is unconfirmed, needs a walk or lies
  beyond this change is never a reason to defer it.
- **A security vulnerability the work finds is such a defect, whoever finds it and whenever it
  arrived.** One a gate, reviewer or audit reports in code the change never touched, one that
  predates the change, and one another layer is said to stop before that layer is traced on every
  path the attack takes are all fixed now as the bullet above requires, with a test that reproduces the attack first where one can exist. A shape that may be exploitable is traced to an attacker or
  ruled out in the same run. It is always closed with the fix that enforces the access
  the product already intends; only a change that widens access or changes who the feature serves
  goes to the user, as **Product Choices** says. Every mitigation
  within reach is carried in that fix, and a remaining step only another party can take, such as
  rotating a credential they hold, is reported as a gate with its owner and saved next action. It is never put to the user as something to
  consider or an option, recorded as deferred, left as a hardening note, or answered with a
  recommendation to run an audit of any kind later.
- **Side work rides the change's pull request while the two read in one careful review, and goes
  on its own pull request past that.** Side work is a defect the work notices that the change
  neither introduced nor needs, incidental cleanup outside the files the requested work edits, a
  skill folder it edits counting as one file, and maintenance a standing rule asks for that the
  change does not need, such as a runtime or dependency upgrade.
  - While the change and its side work together are not too large for one careful read, as with a
    small change and a cleanup as large as it, the side work rides the change's pull request in
    separate commits per concern.
  - Past that, as with a change across hundreds of files, it goes on one side pull request per
    repository for the task, in separate commits per concern. That pull request starts from the
    freshly fetched default branch when it does not need the change, or from the change's branch,
    stacked on it, when it does; a worker builds it while the change goes on, and it is reviewed
    and gated on its own.
  - **No more than one pull request per repository holds a task's change and its side work where a
    consumer must test them together, whatever their size**, such as a package other repositories
    test through a branch reference while the change is unmerged: a consumer's manifest points at
    one branch of the package.
  - Side work in agent configuration rides the session's one agent-configuration pull request in
    its own commits, as the GitHub rule's **Branches and Pull Requests** keeps one per repository.
- **Incidental cleanup has a size budget, measured against the scope the user set and the size of
  the change in flight**, never against a fixed file count or only the files the change happened to
  edit. Incidental cleanup is everything the request did not
  ask for that fixes no defect, outside the change's own design, the defect's shape above and the
  non-essential checks' findings the essential-checks bullet decides. A change to a skill edits
  that skill's whole folder, its `SKILL.md`, references, scripts and templates alike, and cleanup
  inside that folder is held to neither budget's size limits: an
  agent reads a skill as one unit, so a rule restated between two of its files is tidied in the
  change that edits either one, keeping every criterion either copy carries. Cleanup in another
  skill keeps the budget in force; a placement move the guidance criteria require is part of the
  change, not cleanup.
  - **The default budget:** cleanup that fixes no defect — duplication, dead code, a misplaced
    helper, an abstraction with one implementation, layout — is done wherever the work met it,
    placed as the side-work bullet above says, unless a record ground below holds: a few files of
    cleanup met by a change of dozens and a sweep as large as a small change are both done.
  - **The widened budget** holds instead under a broad scope, where the user named the whole
    product, the whole codebase or everything, and while a decision the user scoped to the whole
    session widens it, until they withdraw it: every cleanup the work meets is in scope and done,
    whatever its file count, bar the record grounds below, and the one-hop limit above does not
    bound it. Each such fix gets its own commit, named for what it repairs.
    - **The user widens the session in their own words, and only then**, such as "widen scope" or
      "clean up what you find"; nothing else turns it on. Record that decision, and a later stop,
      with `session-ledger` as one scoped to the whole session, so it reaches every later task,
      context summary, handoff and worker brief.
    - While it holds, collect the items you are unsure about instead of deciding each one, and
      once the task's own change is done return them as one list for a single triage, whose
      answer is final for each item. The task's report adds one line: `Widened scope: <n> fixed
      (<one clause each>) · <n> deferred (<record links>)`.
  - **A deferral record for incidental cleanup is reserved for three grounds:** cleanup comparable
    in size to the change in flight or larger, the two together too large for one careful read, such
    as a sweep as large again as a change of hundreds of files; work an external blocker holds,
    something outside every repository the user owns that the fix cannot be written without; and a
    decision that is the user's, such as a design choice or a change to what the product does: one
    nobody has asked about is put to them now as **Product Choices** says, and one already put and
    still unanswered, when the run ends included, or one they decline is recorded. Work recorded on
    a ground is returned to the caller to record, listed in the change's report one line each with
    its record and its ground, and never fixed in the change. Everything else the work meets is
    done, since a record costs more than a small fix: a later run must find, read, triage and
    execute it, and it can be lost or misstated on the way. A defect, a security vulnerability
    included, and a suspected defect whose confirmation is in reach are never past the budget, as
    the bullets above say. An explicitly requested broad refactor sets its own scope and carries no
    budget.
- **A correction to how one screen looks or reads reaches every page when the user makes it a
  rule, and that screen alone when they do not.** A correction the user asks to have codified, or
  gives a reason for that holds wherever the shape appears, such as "labels sit above their fields
  so the eye moves straight down the form", names a defect. Every existing page with that shape is
  fixed in the same pass, as the change's scope rather than incidental work under the size budget,
  and the rule written from it governs existing pages as much as new ones. A layout, a wording, a
  tone or a style changed on one page with no such reason is the user's choice about that page. It
  is applied there, and other pages with the same shape are listed for the user to decide on,
  never changed in the same pass. A shape a standing rule already named as a defect is fixed on
  every page in the same pass too, as the change's scope; a broken mechanism, a wrong value, a
  missing guard or a parallel implementation stays under the bullets above. A page that builds its own copy of a shared component moves onto the shared
  one in the same pass even though its look changes with it: it takes the look the rest of the
  product already has, which is no new choice about that page, unless the task's record or the
  conversation shows the user decided that page's look, in which case the move goes to the user.
- **Repair the design that causes the defect.** Trace the operation from its entry point to the
  component that decides the outcome. Check which constraints are real product or external
  requirements and which are choices the repository already made. If an owned contract, model,
  or flow cannot express the intended behavior directly, change it and its callers. The number of
  callers is a cost to verify, not a reason to preserve the old design. Never invent an entity,
  identity, scope, or state to satisfy the old shape. A guard, fallback, or special case needs to
  represent a supported case at the boundary that owns it.
- **Operational safeguards enforce evidenced requirements.** Before adding an execution limit,
  preservation step, or restriction to authorized work, identify the user or repository requirement,
  service contract, or observed resource risk it enforces. A remote environment, a large dataset, or
  a hypothetical production concern alone supplies none. Do not invent a cutoff or reduce the
  requested outcome on that basis; carry out the authorized work and verify it. Preserve limits
  required by an established contract.
- Inspect the complete mechanism before choosing its repair. Prefer the clean result that solves
  that defect throughout its affected paths; do not equate a broader cleanup with a better fix.
- The bar is what the cleanest result requires, not what the smallest diff permits. Existing users
  and data may require migration work; effort alone is never a reason to keep parallel mechanisms.
- **A better shape is proposed, never swept in.** Where a different shape than the one the
  repository already follows would serve better — more standard, simpler, less code — the change
  keeps the existing shape and the conversion goes to the user as a proposal: the shape, why it is
  better, every instance it would convert and the size of that change, with a recommendation. This
  holds for an owned contract the work does not otherwise alter, the proposal naming every consumer
  it would change. It is
  built only once the user approves it and at the scope they approve, as its own work rather than
  under the size budget above, and never left half done; a sweep built unasked costs its whole size
  again when the user rejects it.
- **A derivative class, a flag, a parallel helper, or a second declaration added to avoid touching
  something is not a smaller change; it is the same change plus a new thing to delete later.** When the
  narrow option requires inventing structure the clean option would remove, the narrow option is the
  more expensive one.
- **A configuration directive is that narrow option too.** When a tool reports a problem in code the
  user owns — a bundler warning, a type error, a lint finding, a size limit — the fix is in the
  structure it points at: split the module, remove the unused export, move the import. A manifest
  key, a bundler or compiler option, an alias or an exclusion that stops the tool from seeing the
  problem leaves the structure as it was and hides it from the next reader.

## The Deployment's Size Is Not The Design

- **The deployment's current dimensions are facts about today, never constraints on the design.** How
  few rows its database holds, how small its instance is, how little traffic it serves: those
  describe what is deployed, not what the code has to be able to do. A mechanism that cannot grow past
  one process, one core, or one container is a property of the mechanism, and it is still that on the
  day the same code meets a hundred times the data.
- **"It is small enough today" is the sentence that ships the ceiling.** It is true whenever it is
  said and it is never true for long, and it sounds like an argument about the code while being an
  argument about the environment. The same goes for every relative of it: the table is short, the
  instance copes, the job finishes overnight, nobody has complained.
- **Judge the mechanism, not the environment it currently runs in.** Ask whether the work grows with
  the data and whether anything bounds it — not whether this month's instance survives it. Resizing is
  a number somebody revisits under pressure; a design that scales with the work is not.
- Where the environment genuinely limits what can be *demonstrated* — a single-node database that
  cannot show contention, a dataset too small to produce a rate — say so plainly and build for the
  target anyway. A design that cannot yet be proven here is still the right design; one that cannot
  scale is not, and a measurement taken on a small deployment is evidence about that deployment only.
- This is not a license for speculative distribution. The bar is unchanged: the cleanest result for
  the contract the released product needs. It removes exactly one argument from the discussion — that
  the current deployment is small — and settles nothing else about how much scale the work warrants.

## Product Choices

**Fixing an issue does not authorize choosing a new product experience.** Before making a product
choice, identify the user's instruction or standing guidance that settles it. If neither does,
explain the concrete issue, show the concrete alternatives with a recommendation, and ask before
building one; a required outcome does not approve an unnamed layout, control, scope or timing chosen
to achieve it. Do not silently reclassify a condition, reinterpret a rule, or conceal a conflict to
make the implementation fit. Keep the valid issue open while its decision waits, with independent
authorized work continuing as **Trade-Offs Are Surfaced, Never Enforced** says; never ask whether
the issue should be ignored.

- **Preserve established behavior outside a focused request.** Check the neighboring steps for
  visible effects the user did not request, including what loads on open, what an explicit action
  does, and how much information is available. Use the existing behavior and the user's examples
  to resolve what should carry forward. If the request would require an unresolved product choice
  about those steps, explain the visible effect and apply the decision rule above.
- **What a product choice is.** It changes what the product does or offers: what a feature does or
  what information it shows, who a surface serves, the steps of a workflow or a quantity the reader
  meets, a new layout, control or surface, scope, a workaround for a constraint the user set, and
  anything touching security, disclosure or authorization.
- **Fixes that are not one.** Closing a security vulnerability, so the product enforces the access
  it already intends, is a fix and never waits on this question, and so is moving off a deprecated
  API or setting onto its supported replacement, even when the replacement tightens access, as the
  deprecated-usage bullet in **Scope Follows The Defect, Not The Request** says. A game's design is
  never a product choice, as the global rules' game-design bullet says.
- **A fix's remedy meets the same test, judged by its visible reach.** A remedy whose visible
  effect is large — one that changes the layout, controls or flow a reader meets on many pages or
  across several products, or that a returning user would notice, such as every photo gallery
  turning into a carousel once it holds more than a few photos, or a form splitting into steps
  everywhere past some number of fields — is a product choice, and so is new visible behavior a
  remedy carries past the surface the user named to others like it; the defect no longer showing
  there is not. Each is proposed before it is built, whether it arrives as a fix, a later fix round
  adjusts it, or a gate accepted it: the proposal lists every page it would change and carries
  before-and-after captures of a few representative pages where the change shows, never every page,
  so the user decides where it applies. The user's word on how something looks under one condition,
  such as at one width, decides nothing about when it appears under another.
- **Check the visible behavior in loading, failure, recovery, and success before choosing a repair.**
  Adding a second control for an existing action or replacing the intended content, duration, or
  behavior in any of those states is a product choice even when the change is called a preload,
  fallback, or review fix. Ask before building an option the user has not approved. Approval to
  repair a defect or merge the work does not settle a product choice the user was never shown.
- **A routine presentation or interaction detail is not a product choice, and is not put to the
  user.** An alignment, a spacing, a size or tone on the product's existing scale, the placement of
  a message or control among the product's established positions, the wording of a message the
  change adds, a small layout adjustment confined to the surface in hand that leaves every value as
  easy to read: decide it by what serves the reader and stays consistent with the product, and
  state the choice and its reason in the report. Ask only where the user has said such a detail is
  theirs. A detail the user has already decided on that surface is not the agent's: before deciding
  one, look for their earlier word on it in the task's record and the conversation, and follow it;
  changing it goes to the user.
- **Making content fit its space is the agent's work; only what to remove or hide goes to the
  user.**
  - A remedy that keeps every value readable — a strip that scrolls with its scrollbar shown, a
    long value broken at its natural boundaries, items stacked, a control moved to one of the
    product's established positions — is a routine detail as above, decided and fixed at whatever
    width the defect shows, and so is a defect a capture shows that predates the change.
  - Squeezing columns until cells wrap onto several lines, truncating values, shrinking type, or
    narrowing cards, form fields or toolbar controls until their labels break word by word keeps
    everything visible by making rows and items tall and hard to scan, and is never the remedy.
  - Removing a column, field or item, or hiding it below a width, changes what information the
    product shows, so ask which content can go or be hidden at that size, with captures of the
    options, before changing the layout; until the user answers, the content keeps the room its
    values need.
- **Text already in the product keeps its words unless it is wrong or the user named it.**
  - Text that is plainly wrong or inconsistent, such as a label stating something untrue, one thing
    called by two names, or a message that does not match what happens, is corrected or left by
    judgment, and the report says which.
  - Text a standing rule names as a defect counts as wrong, and is fixed on every page it appears
    on, as the bullets in **Scope Follows The Defect, Not The Request** say.
  - A request to reword one text rewords that text alone; any other existing title, label,
    description or message that is correct but could read better keeps its words, beside it or
    elsewhere, even when the new wording suggests changing it, and the suggested rewording goes to
    the user for approval.

## Trade-Offs Are Surfaced, Never Enforced

- **A bug fix restores the intended behavior where it fails.** Identify that behavior from the
  request, owning contract, or working cases. Keep the rest of the experience and contract while
  diagnosing, planning, and testing the repair. A failed implementation, a working alternate
  path, or a cheaper substitute establishes nothing about whether the intended behavior can be
  restored. Investigate viable repairs within the authorized scope and take the next one when an
  approach fails. Offer a different outcome only when a verified constraint rules out restoring
  the intended behavior within that scope, or the user explicitly requests alternatives. If a
  constraint can be removed only by expanding scope or authority, explain the constraint and ask
  about that expansion as the global rules' **Asking the user** says.
- **Keep independent work moving while a product choice waits.** If a remedy changes the intended
  behavior and **Product Choices** reserves that decision for the user, state the choice plainly and
  carry on with work that does not depend on the answer.
  A shape change to an owned contract that `pre-production`'s **Target Contract** admits without a
  proposal is not one of those: it is made, with every consumer, and stated in the pull request.
- **Never quietly narrow the work to avoid the conversation.** Choosing the option that changes nothing
  is choosing the sloppier result on the user's behalf while hiding that a choice existed. Silence
  reads as "there was no decision to make".
- When a genuine fork appears, present it as options, state each consequence concretely, and **say
  which one removes the most duplication and leaves the fewest mechanisms behind**. Recommend that one.
  The user may take the trade-off or refuse it; they cannot weigh what they were not told.
  - A fork only in how the code is built — where shared behavior lives, which mechanism replaces
    parallel copies — is decided by that same test and stated in the pull request, never put to the
    user.
  - Converting existing instances that are not defective to a different shape is not such a fork:
    it is proposed to the user, as **A better shape is proposed, never swept in** says.
  - A fork between designs of what the reader sees is ranked by what serves the reader and the flow
    instead. **A rule about how the product looks or reads is a default that records earlier design
    judgment, never the argument for a design.** Where the better option departs from such a rule,
    recommend it on those merits, name the rule it departs from, and propose the rule change to the
    user, changing the rule once they agree; never present the rule as the reason to prefer the
    weaker option, and never depart from it silently.
- Reserve a blocking question for a decision that is genuinely theirs — a security posture, a product
  behavior, a disclosure boundary — as **Product Choices** reserves it, asked as the global rules'
  **Asking the user** says.
  A change to the product experience is not exempt because its consequence seems small or its
  remedy obvious, but a routine presentation or interaction detail is not such a change: it is
  decided and reported as **Product Choices** says. Routine internal changes within the settled
  experience proceed and are stated in the pull request.
- **A measured failure is never a trade-off.** A rate, a duration, a kill or a resource trail observed
  on a live run is a defect. Fix it under the same rule as any other bug. Whether it is fixed, or
  whether it may be recorded and left, is not a fork to present.
