---
name: pre-production
description: Apply target-contract and product-state constraints to implementation, review, and operational data tasks, including maintenance, cleanup, tooling, and CI repairs. Never add or retain support for an obsolete owned contract or revision by any mechanism without explicit user approval before implementation; update its owned consumers and migrate retained data instead. Apply to relevant CI failures after validation classification.
short_description: 'Apply target-contract constraints to implementation and review tasks.'
---

# Pre-Production

Build the clean target contract instead of preserving transitional behavior.

## Product State

- Apply this skill in every repository. Read its project guidance to determine which contracts have
  external users, which environments and records are disposable, and which surfaces are privileged;
  never infer those facts from an environment name.
- **Establish retention obligations before proposing preservation work.** Use the user's explicit
  instructions and repository facts to identify the affected users and records that must survive.
  A schema, an audit field, or generated test rows prove a supported shape, not that real users or
  valuable stored evidence exist. Apply an explicit statement that affected data is nonexistent or
  disposable; ask only about a concrete conflicting fact or a genuinely unresolved retention choice.
  Do not invent a production environment or require queries against one to confirm that statement.
- **Operational safeguards enforce evidenced requirements.** Before adding an execution limit,
  preservation step, or restriction to authorized work, identify the user or repository requirement,
  service contract, or observed resource risk it enforces. A remote environment, a large dataset, or
  a hypothetical production concern alone supplies none. Do not invent a cutoff or reduce the
  requested outcome on that basis; carry out the authorized work and verify it. Preserve limits
  required by an established contract, and handle measured failures under **Encountered Issues**.
- Migrate affected users and retained data onto the target contract before removing the old one.
  Release state changes the migration work; it does not by itself justify a legacy runtime path.

## Encountered Issues

- **Classify validation failures first, before the failure is diagnosed, handed to a worker, or
  mentioned to the user.** Read the default branch's latest run of the
  same check, hosted or local, and reproduce there only when no such run exists. When that evidence
  establishes the same failure under comparable inputs, and the change neither introduces nor
  worsens it, record the check and that evidence as a baseline failure in the task's record, which
  every later gate receives. Continue the requested work
  and its relevant validation; do not repair, rerun, investigate further, ask a product question, or
  record a deferral for that failure merely because validation encountered it. **Nothing the user
  reads names a baseline failure or says one was left out**: no report, summary, status list, open
  item or question, apart
  from a merge that branch protection rejects for it, whose rejection is reported with its
  provider evidence. No report claims the excluded check passed either; it covers the checks the
  change answers for. This exclusion does not cover a defect the user assigned, a suite past its
  runtime budget, as the testing rule's **Every suite finishes within five minutes of wall time**
  bullet says, deprecated usage or a printed warning, as the
  deprecated-usage bullet below says, a failure of the behavior the task must establish,
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

Fix and validate every defect that remains in the task, even when it predates the task or sits
outside the initial file set; cleanup that fixes no defect follows the size budget below.
Follow the evidence through affected callers and owners. That obligation is not a license to audit
areas the evidence never reaches, and the section below governs how far it reaches.
The repair must satisfy **Target Contract**; an encountered failure never authorizes compatibility
with an obsolete owned contract or revision.

- **A relevant red CI job is an encountered issue.** A package index serving no candidates,
  a registry or network timeout, a runner fault, a test that passes on a second try: each is the
  pipeline depending on something it does not control, and that dependency is a defect in the
  repository. Fix the input that exposes it — restore resolved dependencies from a cache keyed on the
  lockfile, replace a live service with a fake, make the test deterministic — and push that.
  Re-running the job is never the fix: a green re-run proves the outage ended, not that the pipeline
  survives the next one.

- **A test that costs far more than it covers is removed.** When one test, parametrized family or
  module is disproportionate under the testing rule's **Test Cost** criteria and cannot be made cheap as those
  criteria allow, apply that rule's **Test Deletion Evidence** requirements before deleting it.
  Keep or extend a cheaper test of the same classification where the contract needs one. Never keep it
  in any of the ways the testing rules list for absorbing a slow test.

## Scope Follows The Defect, Not The Request

- **The scope of a change is the whole shape of the problem, not the files the request happened to
  name.** A reported symptom is where the defect surfaced, not its boundary. When the same defect
  appears beside it — a second implementation of the mechanism, a sibling path answering the same
  question from a different input, a parallel copy nobody reconciled — that is one piece of work, the
  change's own scope rather than incidental work under the size budget or an item left for later,
  and splitting it leaves the half that stays behind as the version the next person extends. The
  repair itself, the defect no longer showing anywhere, is always in scope. A repair whose visible
  effect beyond that reaches surfaces the user did not name, such as a shared component's new
  layout reaching every page that uses it, is a proposal for those surfaces, put to the user as the
  global rules' product-choice bullet says, unless a standing rule names that shape a defect.
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
  change — in a file it opened, a check it ran, a capture it read — is a defect, fixed as below, or
  cleanup, handled under the size budget below. A file opened or edited only to make such an
  incidental fix is never itself a source of more incidental cleanup: what else it holds is deferred,
  not chased.
- **A defect is anything the system does or shows that a reader would call broken**, and the system
  includes the repository's tooling: its tests, fixtures, build, setup and CI. An image that never
  loads, a wrong value, a state shown in the wrong place, a control that does nothing, a lost write
  or notification, a crash, an exhausted budget, a test suite that fails in a fresh checkout, a
  fixture that builds data the code would never hold, and a setup step or documented command that
  errors are its familiar shapes, not its boundary.
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
  is fixed in the change in flight: move to the supported replacement, or turn on the default the
  owner says is coming; a dependency that itself calls deprecated code is upgraded or replaced,
  apart from the testing rule's narrow third-party ignore. A check a library warns it will start
  enforcing is deprecated usage when left off, never a missing safeguard. The replacement changing
  behavior, such as a stricter check, a refused token or a different sign-in, is part of the fix,
  never a reason to keep the deprecated form, call it pre-existing, or put the move to the user;
  released users move as **Product State**'s migration bullet says. Only a step the move needs that
  the user alone can take, such as supplying an identifier the session cannot read, goes to them,
  as that step.
- **A defect the work notices is always fixed, wherever it lives.** It is fixed in the change in
  flight, outside both the hop limit and the size budget below, however many files its fix takes.
  Sitting in a shared
  component, an owned library or another owned repository the pull request does not otherwise touch
  is no reason to leave it: the fix goes to that repository's pull request for this work. It is
  never deferred or offered to the user as a question.
- **A security vulnerability the work finds is such a defect, whoever finds it and whenever it
  arrived.** One a gate, reviewer or audit reports in code the change never touched, one that
  predates the change, and one another layer is said to stop before that layer is traced on every
  path the attack takes are all fixed in the change in flight, with a test that reproduces the
  attack first where one can exist. A shape that may be exploitable is traced to an attacker or
  ruled out in the same run. It is always closed in the change with the fix that enforces the access
  the product already intends; only a change that widens access or changes who the feature serves
  goes to the user, as the global rules' **Task execution and authorization** says. Every mitigation
  within reach is carried in the change, and a remaining step only another party can take, such as
  rotating a credential they hold, is reported as a gate with its owner and saved next action, as
  the global rules' **Tools and environments** says. It is never put to the user as something to
  consider or an option, recorded as deferred, left as a hardening note, or answered with a
  recommendation to run an audit of any kind later.
- **Incidental cleanup has a size budget.** Incidental cleanup is everything the request did not
  ask for that fixes no defect, outside the change's own design and the defect's shape above. A
  change to a skill edits that skill's whole folder, its `SKILL.md`, references, scripts and
  templates alike, and cleanup inside that folder is held to neither budget's size limits: an
  agent reads a skill as one unit, so a rule restated between two of its files is tidied in the
  change that edits either one, keeping every criterion either copy carries. Cleanup in another
  skill keeps the budget in force.
  - **The default budget:** cleanup that fixes no defect — duplication, dead code, a misplaced
    helper, an abstraction with one implementation, layout — fits only inside the files the change
    already edits and while it stays small beside the requested part.
  - **The widened budget**, which holds instead while a decision the user scoped to the whole
    session widens it, until they withdraw it: such cleanup fits when its fix touches about five
    files or fewer, needs no design decision from the user, does not change what the product does
    and needs no plan of its own. Each such fix gets its own commit, named for what it repairs.
  - Cleanup past the budget in force is deferred work: returned to the caller to record, listed in
    the change's report one line each with its record, and never fixed in the change or put to the
    user as a question. A defect, a security vulnerability included, is never past it. An explicitly
    requested broad refactor sets its own scope and carries no budget.
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
- Inspect the complete mechanism before choosing its repair. Prefer the clean result that solves
  that defect throughout its affected paths; do not equate a broader cleanup with a better fix.
- The bar is what the cleanest result requires, not what the smallest diff permits. Existing users
  and data may require migration work; effort alone is never a reason to keep parallel mechanisms.
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

## Trade-Offs Are Surfaced, Never Enforced

- **A bug fix restores the intended behavior where it fails.** Identify that behavior from the
  request, owning contract, or working cases. Keep the rest of the experience and contract while
  diagnosing, planning, and testing the repair. A failed implementation, a working alternate
  path, or a cheaper substitute establishes nothing about whether the intended behavior can be
  restored. Investigate viable repairs within the authorized scope and take the next one when an
  approach fails. Offer a different outcome only when a verified constraint rules out restoring
  the intended behavior within that scope, or the user explicitly requests alternatives. If a
  constraint can be removed only by expanding scope or authority, explain the constraint and ask
  about that expansion under the global rules.
- **Keep independent work moving while a product choice waits.** If a remedy changes the intended
  behavior and the global rules reserve that decision for the user, state the choice plainly and
  carry on with work that does not depend on the answer.
  A shape change to an owned contract that **Target Contract** admits without a proposal is not one
  of those: it is made, with every consumer, and stated in the pull request.
- **Never quietly narrow the work to avoid the conversation.** Choosing the option that changes nothing
  is choosing the sloppier result on the user's behalf while hiding that a choice existed. Silence
  reads as "there was no decision to make".
- When a genuine fork appears, present it as options, state each consequence concretely, and **say
  which one removes the most duplication and leaves the fewest mechanisms behind**. Recommend that one.
  A fork only in how the code is built — where shared behavior lives, which mechanism replaces
  parallel copies — is decided by that same test and stated in the pull request, never put to the
  user. Converting existing instances that are not defective to a different shape is not such a
  fork: it is proposed to the user, as the global rules' **A better shape is proposed, never swept
  in** says.
  A fork between designs of what the reader sees is ranked by what serves the reader and the flow
  instead, as the global rules' standing-guidance bullet says of design rules.
  The user may take the trade-off or refuse it; they cannot weigh what they were not told.
- Reserve a blocking question for a decision that is genuinely theirs — a security posture, a product
  behavior, a disclosure boundary — under the global rules' **Task execution and authorization**.
  A change to the product experience is not exempt because its consequence seems small or its
  remedy obvious, but a routine presentation or interaction detail is not such a change: it is
  decided and reported as that section says. Routine internal changes within the settled
  experience proceed and are stated in the pull request.
- Say what changed for whom. "This is a change, not a refactor" belongs at the top of the description,
  not buried among the mechanics.
- **A measured failure is never a trade-off.** A rate, a duration, a kill or a resource trail observed
  on a live run is a defect. Fix it under the same rule as any other bug. Whether it is fixed, or
  whether it may be recorded and left, is not a fork to present.

## Target Contract

- Implement the contract the released product should have. Never add or retain support for an
  obsolete owned contract or revision by any mechanism without explicit user approval for that
  retention before implementation. This governs code, configuration, tooling, CI, data handling,
  documentation, and instructions as well as runtime paths. An old owned consumer failing against
  the current contract is a reason to update it, not an exception; update affected owned consumers
  and migrate retained data onto the target contract instead.
- Treat configuration inputs as owned contracts. Replace a stale deployed value at the existing
  setting and its deployment owner; do not add another file, environment key, or fallback path to
  override it.
- An owned workflow boundary has one canonical representation. Normalize a provider's layout,
  cardinality, or revision at the owned adapter where it enters the workflow; every downstream
  consumer reads that one representation. A branch, probe, fallback, or helper that accepts an
  earlier representation downstream is compatibility: replace it by updating the adapter and its
  consumers.
- **A value that differs by environment has one name, and whatever already scopes values per
  environment supplies it** — an environment's secrets, a per-environment config file, a deployment
  registry. Never a second name per environment, nor an expression or branch choosing between
  names, such as `FEED_URL_STAGING` beside `FEED_URL_PRODUCTION` picked by `env == "production"`.
  Before adding a value, read how its siblings are scoped and supplied; a sibling selecting between
  per-environment names is a defect, moved onto the one name.
- Keep resilience within the current supported contract: error handling, browser support, empty
  states, and provider-failure behavior the released product needs. Supporting an obsolete owned
  contract or revision is compatibility, even when described as resilience or repair; it requires
  the approval above. Third-party contracts remain governed by **Owned And Third-Party Contracts**.
- Prefer a deliberate break to an owned API, wire, schema, payload, or stored shape when it
  materially simplifies the result. Update affected consumers and migrate retained data, then remove
  the old shape; update every consumer and generated contract in the same change. A break the
  requested work or a defect requires is made without a question. One chosen only because another
  shape would serve better, on a contract the work does not otherwise alter, is proposed to the user
  first, as the global rules' **A better shape is proposed, never swept in** says.
- **An owned contract stays owned across repositories.** A consumer in a sibling repository the
  user owns makes the break multi-repository work, never somebody else's decision; only a consumer
  outside the user's control freezes a shape. **Scope Follows The Defect** holds for a break as for
  a bug: the new shape reaches every site answering the same question, never only the one the work
  started from.
- Do not weaken a compatibility gate to hide an intentional break. Report the exact failure and the
  contract change it detected so a reviewer can distinguish intended from accidental breakage.
- For disposable development records, follow the repository's stated policy: it decides which
  values a change may discard, never how the change reaches a deployed database. Never assume
  released user data is disposable or carry a tester conversion as a runtime compatibility path.

## Owned And Third-Party Contracts

- Everything above is about contracts the user owns and can change by migrating every consumer
  of them. **A third-party provider's contract is not ours and cannot change at all.**
- So where the two must meet, only one side can move, and it is always ours. "The provider encodes it
  differently" is a statement about our model, not about theirs: our model is the one that accepts
  what the provider sends, in the shape the provider sends it.
- That makes a provider difference the weakest reason there is to keep a second model mirroring the
  one it converts into. A second model is what you build when neither side can move; on this boundary
  one side always can, so the pair is duplication rather than a boundary.
- **Adapting is not imitating.** The provider's encoding comes across — its string tokens, its date
  formats, its nesting, its keys — carried by validators and aliases on our own fields. Its
  vocabulary does not: field names, casing, and domain terms stay ours.
- Requiring a field the provider may legitimately omit is still wrong, and moving toward the
  provider's shape never licenses it. Accept what it can send; require only what an owned validation
  or selection boundary proves is present.

## Required Data

- Make fields and columns required by default. Keep one nullable only when absence is a genuine
  supported domain state.
- An absent value on a read path is a schema question, never a branch. When the column is already
  required, a warn-and-skip, an `or` between two sources for the same value, and a refusal keyed on
  the absence are all dead code and go, and the wire message and the model follow the column and
  require the field. When the column is not required, the fix is the schema change that requires it,
  and the wire and the model follow that column, never the other way round. The shape to recognize:
  a validation error at a read site answered by widening the reader instead of asking what the store
  allows.
- For a requiredness change, establish the affected data's retention scope under **Product State**
  before deciding what its revision keeps or clears; required columns do not themselves create an
  obligation to preserve disposable or nonexistent rows.
- For retained values, use the authoritative source where one exists and a type-valid placeholder
  only where none exists. Never overwrite a known retained value, fabricate a placeholder in runtime
  code, or keep a permanent schema default solely to make a migration convenient.
- **A backfill writes each row's value under the new contract, never one chosen so existing rows
  keep behaving as before.** A flag set on every pre-change row so it keeps the old outcome, such as
  staying exempt from a new check, closed to a new path, or treated as the old kind, is a legacy
  fallback written into data. So is a branch on a creation date or a stored version that does the
  same. Where the new field records a fact, such as who did something or when, backfill that fact
  from its authoritative source. The tell is a description or comment saying that rows from before
  the change keep the old behavior; keeping it needs the user's approval, as any legacy support
  does.
