---
name: pre-production
description: Apply target-contract constraints to every implementation and review task, including tooling and CI repairs. Never add or retain support for an obsolete owned contract or revision by any mechanism without explicit user approval before implementation; update its owned consumers and migrate retained data instead. Apply to relevant CI failures after validation classification.
short_description: 'Apply target-contract constraints to implementation and review tasks.'
---

# Pre-Production

Build the clean target contract instead of preserving transitional behavior.

## Product State

- Apply this skill in every repository. Read its project guidance to determine which contracts have
  external users, which environments and records are disposable, and which surfaces are privileged;
  never infer those facts from an environment name.
- Migrate affected users and retained data onto the target contract before removing the old one.
  Release state changes the migration work; it does not by itself justify a legacy runtime path.

## Encountered Issues

Apply `execute-task`'s **Encountered Issues** validation classification before choosing work from a
failed check. Fix and validate every issue that remains in the task, even when it predates the task
or sits outside the initial file set. Follow the evidence through affected callers and owners.
That obligation is not a licence to audit areas the evidence never reaches; it is also not a reason
to stop at the first file, and the section below governs how far it does reach.
The repair must satisfy **Target Contract**; an encountered failure never authorizes compatibility
with an obsolete owned contract or revision.

- **A relevant red CI job is an encountered issue.** A package index serving no candidates,
  a registry or network timeout, a runner fault, a test that passes on a second try: each is the
  pipeline depending on something it does not control, and that dependency is a defect in the
  repository. Fix the input that exposes it — restore resolved dependencies from a cache keyed on the
  lockfile, replace a live service with a fake, make the test deterministic — and push that.
  Re-running the job is never the fix: a green re-run proves the outage ended, not that the pipeline
  survives the next one.

## Scope Follows The Defect, Not The Request

- **The scope of a change is the whole shape of the problem, not the files the request happened to
  name.** A reported symptom is where the defect surfaced, not its boundary. When the same defect
  appears beside it — a second implementation of the mechanism, a sibling path answering the same
  question from a different input, a parallel copy nobody reconciled — that is one piece of work, and
  splitting it leaves the half that stays behind as the version the next person extends.
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
  against the bounded local-refactoring test above. Do not turn a sequence of individually useful
  cleanups into an unrequested redesign, or invent an umbrella concern to make them one defect.
  An explicitly requested broad refactor still receives its stated scope. File counts are evidence
  of spread, not a cap on the repair itself: a necessary migration may be wide, while a small
  unrelated rewrite may already be disproportionate.
- **Incidental work goes one hop, never further.** What the work notices while making the requested
  change — in a file it opened, a check it ran, a capture it read — is fixed. A file opened or edited
  only to make such an incidental fix is never itself a source of more incidental work: what else it
  holds is listed, not chased.
- **Incidental work has a size budget.** The incidental part of a change — everything the request
  did not ask for, apart from a confirmed bug in the path of the requested behaviour, which is always
  fixed — stays about the size of the requested part, or within 150 changed lines across 10 files
  when the requested part is smaller. Inside the budget, everything noticed is fixed. Once the next
  incidental fix would pass it, the rest is listed under **Noticed, not changed** in the change's
  report, one line each, and is neither fixed, deferred, nor put to the user as a question. An
  explicitly requested broad refactor and a doctor run set their own scope and carry no budget.
- **A correction to how one screen looks or reads is the user's decision about that screen, not a
  defect to sweep.** A layout, a wording, a tone or a style the user changes on one page is applied
  to that page, and other pages with the same shape are listed for the user to decide on, never
  changed in the same pass: a choice of taste on one screen says nothing about the others. A rule
  written from the correction governs new work; the existing pages it would reach wait for the
  user's decision the same way. A shape a standing rule already named as a defect before the
  correction, and a broken mechanism, a wrong value, a missing guard or a parallel implementation,
  stay under the bullets above on every page.
- Inspect the complete mechanism before choosing its repair. Prefer the clean result that solves
  that defect throughout its affected paths; do not equate a broader cleanup with a better fix.
- The bar is what the cleanest result requires, not what the smallest diff permits. Existing users
  and data may require migration work; effort alone is never a reason to keep parallel mechanisms.
- **A derivative class, a flag, a parallel helper, or a second declaration added to avoid touching
  something is not a smaller change; it is the same change plus a new thing to delete later.** When the
  narrow option requires inventing structure the clean option would remove, the narrow option is the
  more expensive one.

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
- This is not a licence for speculative distribution. The bar is unchanged: the cleanest result for
  the contract the released product needs. It removes exactly one argument from the discussion — that
  the current deployment is small — and settles nothing else about how much scale the work warrants.

## Trade-Offs Are Surfaced, Never Enforced

- **A behaviour change is not a blocker.** Where the cleanest result shifts behaviour — a value
  reaching a store it never reached before, a permission finally applying where it always should have,
  a value newly shown to or withheld from someone — that is the user's decision, and the way to put
  it to them is to state it plainly and carry on with the work that does not depend on the answer.
  A shape change to an owned contract is not one of those: it is made, with every consumer, and
  stated in the pull request.
- **Never quietly narrow the work to avoid the conversation.** Choosing the option that changes nothing
  is choosing the sloppier result on the user's behalf while hiding that a choice existed. Silence
  reads as "there was no decision to make".
- When a genuine fork appears, present it as options, state each consequence concretely, and **say
  which one removes the most duplication and leaves the fewest mechanisms behind**. Recommend that one.
  The user may take the trade-off or refuse it; they cannot weigh what they were not told.
- Reserve a blocking question for a decision that is genuinely theirs — a security posture, a product
  behaviour, a disclosure boundary — under the global rules' **Task execution and authorization**.
  A change to the product experience is not exempt because its consequence seems small or its
  remedy obvious. Routine internal changes within the settled experience proceed and are stated
  in the pull request.
- Say what changed for whom. "This is a change, not a refactor" belongs at the top of the description,
  not buried among the mechanics.
- **A measured failure is never a trade-off.** A rate, a duration, a kill or a resource trail observed
  on a live run is a defect; only the shape of its fix is put to the user. Whether it is fixed, or
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
  materially simplifies the result. Migrate affected consumers and data, then remove the old shape;
  update every consumer and generated contract in the same change.
- **An owned contract stays owned across repositories.** A consumer in a sibling repository the
  user owns makes the break multi-repository work, never somebody else's decision; only a consumer
  outside the user's control freezes a shape. **Scope Follows The Defect** holds for a break as for
  a bug: the new shape reaches every site answering the same question, never only the one the work
  started from.
- Do not weaken a compatibility gate to hide an intentional break. Report the exact failure and the
  contract change it detected so a reviewer can distinguish intended from accidental breakage.
- For disposable development records, follow the repository's stated policy. A one-time conversion
  of explicitly identified tester data may run outside shipped code when it is more useful than a
  reset; verify its result and remove the conversion script. Never assume released user data is
  disposable or carry a tester conversion as a runtime compatibility path.

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
  and the wire and the model follow that column, never the other way round. The shape to recognise:
  a validation error at a read site answered by widening the reader instead of asking what the store
  allows.
- **What a requiredness change owes the rows already stored is the repository's call, not this
  skill's.** Read its project guidance before writing anything that touches them. Two answers are
  both coherent and they are opposites: a repository whose environments are disposable resets the
  data as an operational action and writes no data migration at all, while one that keeps its
  environments preserves every known value, takes it from its authoritative source where one exists,
  and writes a type-valid placeholder only where no source has it. Assuming either answer in the
  wrong repository destroys data or ships a migration nobody wanted.
- Whichever answer the repository gives, never overwrite a known value, never fabricate a placeholder
  in runtime code, and never keep a permanent schema default solely to make a migration convenient.
- Before selecting an implementation for a schema or stored-representation change, invoke the
  database-migration skill for that role, including when the repository has no migration runner or
  uses startup reconciliation. Resolve its local commands and layout through project guidance;
  missing infrastructure is work to establish, not permission to bypass that owner. It governs the
  mechanics, what the change owes existing rows, and validation.
