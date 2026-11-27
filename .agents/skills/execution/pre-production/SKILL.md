---
name: pre-production
description: "The product state before it ships, applied to implementation, review and operational data tasks, maintenance, cleanup, tooling and CI repairs included: build only the target contract, never adding a compatibility shim or keeping support for an obsolete owned contract or revision; update its owned consumers and migrate retained data. Also covers which contracts, environments and records a project's guidance marks as having users or as disposable, what retained data obliges, partial updates, configuration as an owned contract, deliberate breaks of owned contracts across repositories, adapting to a third-party provider's contract, required fields and backfills, and why the current deployment's size never sets the design."
short_description: 'Build the target contract for the product before it ships, with no compatibility for obsolete owned shapes.'
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
  required by an established contract.
- Keep owned cutover sequencing in the release procedure. Move affected users to the target
  contract and convert retained data in versioned migrations. Do not add runtime behavior for
  mixed owned versions, half-applied transitions, or an in-flight state the work has established
  is absent. Ordinary recovery uses the current contract.

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

## Target Contract

- **Implement only the target contract.** Never add a compatibility shim or retain support for an
  obsolete owned contract or revision, even temporarily. This governs runtime code, configuration,
  tooling, CI, data handling, documentation, and instructions. Update affected owned consumers,
  convert retained data through versioned migrations, and remove obsolete paths. Put any cutover
  sequencing in the release procedure.
- **Repair the design that causes the defect.** Trace the operation from its entry point to the
  component that decides the outcome. Check which constraints are real product or external
  requirements and which are choices the repository already made. If an owned contract, model,
  or flow cannot express the intended behavior directly, change it and its callers. The number of
  callers is a cost to verify, not a reason to preserve the old design. Never invent an entity,
  identity, scope, or state to satisfy the old shape. A guard, fallback, or special case needs to
  represent a supported case at the boundary that owns it.
- **A partial update expresses intent through its existing field presence or field mask.** Apply
  the fields that mechanism selects and leave every other field alone. Use the contract's own
  representation for an explicit clear. A separate control earns a place only when it expresses
  a distinct operation the update fields cannot represent.
- Treat configuration inputs as owned contracts. Replace a stale deployed value at the existing
  setting and its deployment owner; do not add another file, environment key, or fallback path to
  override it.
- An owned workflow boundary has one canonical representation. Normalize a provider's layout,
  cardinality, or revision at the owned adapter where it enters the workflow; every downstream
  consumer reads that one representation. A branch, probe, fallback, or helper that accepts an
  earlier representation downstream is compatibility: replace it by updating the adapter and its
  consumers.
- Keep resilience within the current supported contract: error handling, browser support, empty
  states, and provider-failure behavior the released product needs. Supporting an obsolete owned
  contract or revision is a compatibility shim even when described as resilience or repair.
  Third-party contracts remain governed by **Owned And Third-Party Contracts**.
- Prefer a deliberate break to an owned API, wire, schema, payload, or stored shape when it
  materially simplifies the result. Update affected consumers and migrate retained data, then remove
  the old shape; update every consumer and generated contract in the same change. A break the
  requested work or a defect requires is made without a question.
- **An owned contract stays owned across repositories.** A consumer in a sibling repository the
  user owns makes the break multi-repository work, never somebody else's decision; only a consumer
  outside the user's control freezes a shape. The new shape reaches every site answering the same
  question, as a defect's repair does, never only the one the work started from.
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
- An absent value on a read path is a schema question. First establish whether the domain requires
  it. Represent legitimate absence at the operation that can return it. When one shape represents
  both a present entity and no entity, give those states distinct representations so a present
  entity requires its identity. If the domain and the column both require a field, align the wire
  and model with the column. If the domain requires it and the column allows absence, align the
  column too. Apply **Target Contract** when a shared shape is the cause of an impossible branch.
- For a requiredness change, establish the affected data's retention scope under **Product State**
  before deciding what its revision keeps or clears; required columns do not themselves create an
  obligation to preserve disposable or nonexistent rows.
- For retained values, use the authoritative source where one exists and a type-valid placeholder
  only where none exists and the placeholder expresses a legitimate domain state. The
  **Target Contract** prohibition on invented identities, ownership, and scopes also applies during
  migration. Never overwrite a known retained value, fabricate a placeholder in runtime code, or
  keep a permanent schema default solely to make a migration convenient.
- **A backfill writes each row's value under the new contract, never one chosen so existing rows
  keep behaving as before.** A flag set on every pre-change row so it keeps the old outcome, such as
  staying exempt from a new check, closed to a new path, or treated as the old kind, is a legacy
  fallback written into data. So is a branch on a creation date or a stored version that does the
  same. Where the new field records a fact, such as who did something or when, backfill that fact
  from its authoritative source. A description or comment saying earlier rows keep the old
  behavior identifies a fallback the migration or runtime must remove.
