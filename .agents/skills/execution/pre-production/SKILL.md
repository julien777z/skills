---
name: pre-production
description: "The product state before it ships, applied to implementation, review and operational data tasks, maintenance, cleanup, tooling and CI repairs included: build only the target contract, never adding a compatibility shim or keeping support for an obsolete owned contract or revision; update its owned consumers and migrate retained data. Also covers which contracts, environments and records a project's guidance marks as having users or as disposable, what retained data obliges, configuration as an owned contract, deliberate breaks of owned contracts across repositories, adapting to a third-party provider's contract, and what a requiredness change and a backfill owe retained data, including before building anything that needs a value some existing records lack, such as a field a provider newly requires."
short_description: 'Build the target contract for the product before it ships, with no compatibility for obsolete owned shapes.'
user-invocable: false
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
- Keep owned cutover sequencing in the release procedure. Move affected users to the target
  contract and convert retained data in versioned migrations. Do not add runtime behavior for
  mixed owned versions, half-applied transitions, or an in-flight state the work has established
  is absent. Ordinary recovery uses the current contract.

## Target Contract

- **Implement only the target contract.** Never add a compatibility shim or retain support for an
  obsolete owned contract or revision, even temporarily. This governs runtime code, configuration,
  tooling, CI, data handling, documentation, and instructions. Update affected owned consumers,
  convert retained data through versioned migrations, and remove obsolete paths. Put any cutover
  sequencing in the release procedure.
- Treat configuration inputs as owned contracts. Replace a stale deployed value at the existing
  setting and its deployment owner; do not add another file, environment key, or fallback path to
  override it.
- An owned workflow boundary has one canonical representation. Normalize a provider's layout,
  cardinality, or revision at the owned adapter where it enters the workflow; every downstream
  consumer reads that one representation. A branch, probe, fallback, or helper that accepts an
  earlier representation downstream is compatibility: replace it by updating the adapter and its
  consumers.
- **A fact about an actor or entity reaches a service on the operation for the resource it applies
  to.** A consent, an identity or a setting a provider needs is read from the one place the domain
  keeps it and sent where that resource is created or updated, never added as a field of an
  operation on a different or child resource that happens to need it first: a member's accepted
  newsletter terms go on the request that opens the member's mailing-list subscription, never on
  the request that adds a delivery address, so any later feature that needs the same acceptance
  reuses it. A value describing the operation's own resource, such as an address's lines on its
  create, stays on that operation.
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

## Retained Data

- For a requiredness change, establish the affected data's retention scope under **Product State**
  before deciding what its revision keeps or clears; required columns do not themselves create an
  obligation to preserve disposable or nonexistent rows.
- **A value a design needs that existing records lack is required and backfilled, never made
  optional for them**, where its absence is no supported domain state and the value can be derived
  or **Product State** establishes the affected records are disposable. A value read at request time
  from a related record some records lack, such as a time zone read from an optional preferences
  record, is one of these. It is made required where the domain places it: on the related record and
  the link to it only where the domain gives every record that related record, and otherwise on the
  record that needs it, its column, wire field and model all required to match; this placement is
  settled here and never put to the user, so a related record the domain does not give every record
  is never made required to carry the value. Either way the
  migration gives every existing record the value from its source or a placeholder the next bullet
  allows, and removes only a row the next bullet deletes. Neither what the agent builds nor any
  option, plan or recommendation it puts to the user keeps the column nullable for records without
  the value, proceeds without it, sends a provider less than the provider requires, fills it at
  request time with a value that is not the record's own, such as another actor's, or refuses, skips
  or deletes the records that lack it where a source or such a placeholder can supply it, an error
  raised for them included. Each keeps legacy support for those records, or drops them where the
  migration owes them a value. Released user data with no authoritative source is a retention
  question for the user, asked before the design is offered, as **Product State** says.
- For retained values, use the authoritative source where one exists. Where none exists, use a
  type-valid placeholder only when it expresses a legitimate domain state, or when the records are
  disposable pre-production data and the placeholder is a value describing the record, such as a
  placeholder consent date for library members created before consents were stored: test data, never
  an invented entity, identity, ownership or scope. A disposable row that needs one of those and has
  no source is deleted by the migration. Never overwrite a known retained value, fabricate a
  placeholder in runtime code, or keep a permanent schema default solely to make a migration
  convenient.
- **A backfill writes each row's value under the new contract, never one chosen so existing rows
  keep behaving as before.** A flag set on every pre-change row so it keeps the old outcome, such as
  staying exempt from a new check, closed to a new path, or treated as the old kind, is a legacy
  fallback written into data. So is a branch on a creation date or a stored version that does the
  same. Where the new field records a fact, such as who did something or when, backfill that fact
  from its authoritative source. A description or comment saying earlier rows keep the old
  behavior identifies a fallback the migration or runtime must remove.
