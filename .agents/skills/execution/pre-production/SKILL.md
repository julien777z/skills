---
name: pre-production
description: Apply a pre-release repository's product constraints when planning, implementing, simplifying, or reviewing contracts, schemas, migrations, and stored data. Use it to decide how broad a change should be, whether a nearby duplicate belongs in scope, and how to surface a behaviour trade-off rather than narrowing the work around it.
---

# Pre-Production

Build the clean release target instead of preserving transitional behavior.

## Product State

- This skill applies to a repository that has not released: work in progress, pre-MVP, deployed
  only to environments its own team uses, with no external users depending on any contract it
  serves.
- The repository's project guidance states the rest — which environments exist, how disposable
  their data is, and which surfaces are privileged. Read it before deciding anything this skill
  leaves to the repository, and never assume one repository's answer holds in another.
- Where the repository's guidance says it has released users, this skill does not apply. Say so
  rather than applying it anyway.

## Encountered Issues

Fix and validate every concrete issue naturally encountered during authorized work, even when it
predates the task or sits outside the initial file set. Follow the evidence through the affected
callers and owners. That obligation is not a licence to audit areas the evidence never reaches; it is
also not a reason to stop at the first file, and the section below governs how far it does reach.

## Scope Follows The Defect, Not The Request

- **The scope of a change is the whole shape of the problem, not the files the request happened to
  name.** A reported symptom is where the defect surfaced, not its boundary. When the same defect
  appears beside it — a second implementation of the mechanism, a sibling path answering the same
  question from a different input, a parallel copy nobody reconciled — that is one piece of work, and
  splitting it leaves the half that stays behind as the version the next person extends.
- **"Out of scope" is the sentence that preserves the mess.** A site left outside the fix is exactly
  where it regrows, because the guidance a later reader finds there still describes the old shape.
  Bring the similar items in, or establish concretely that they are a different concern.
- Judge similarity by the question the code answers, not the directory it sits in or the layer it
  belongs to. Two modules deciding the same thing from different inputs are one concern wearing two
  implementations, however far apart they live.
- **Propose the broad version first.** A narrow patch offered as the whole answer costs the reviewer
  the chance to ask for the clean one, because they cannot ask for what they were never shown.
  Surveying the surrounding code for the same defect is part of answering the request, not a favour
  added to it.
- The bar is what the cleanest result requires, not what the smallest diff permits. Without released
  users there is no deprecation window to honour and no stored data to migrate around, so the only
  remaining argument for the narrow version is the effort of the wider one — which is the agent's
  effort to spend, never a cost to charge the user.
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
  a field appearing or disappearing for some caller — that is the user's decision, and the way to put
  it to them is to state it plainly and carry on with the work that does not depend on the answer.
- **Never quietly narrow the work to avoid the conversation.** Choosing the option that changes nothing
  is choosing the sloppier result on the user's behalf while hiding that a choice existed. Silence
  reads as "there was no decision to make".
- When a genuine fork appears, present it as options, state each consequence concretely, and **say
  which one removes the most duplication and leaves the fewest mechanisms behind**. Recommend that one.
  The user may take the trade-off or refuse it; they cannot weigh what they were not told.
- Reserve a blocking question for a decision that is genuinely theirs — a security posture, a product
  behaviour, a disclosure boundary. Where the consequence is small and the cleaner answer is obvious,
  take it and state it in the pull request rather than stopping.
- Say what changed for whom. "This is a change, not a refactor" belongs at the top of the description,
  not buried among the mechanics.
- **A measured failure is never a trade-off.** A rate, a duration, a kill or a resource trail observed
  on a live run is a defect; only the shape of its fix is put to the user. Whether it is fixed, or
  whether it may be recorded and left, is not a fork to present.

## Target Contract

- Implement the contract the released product should have. Do not add compatibility shims,
  transitional runtime branches, dual reads or writes, temporary feature paths, or speculative
  handling for obsolete shapes.
- Legitimate production resilience is not transitional fallback code. Keep the error handling,
  browser support, empty states, and provider-failure behavior the released product needs.
- Prefer a deliberate API, wire, schema, payload, or stored-shape break when it materially
  simplifies the result. Remove the old shape and update every in-repository consumer and generated
  contract in the same change.
- Do not weaken a compatibility gate to hide an intentional break. Report the exact failure and the
  contract change it detected so a reviewer can distinguish intended from accidental breakage.
- For disposable development records, follow the repository's stated policy. A one-time conversion
  of explicitly identified tester data may run outside shipped code when it is more useful than a
  reset; verify its result and remove the conversion script. Never assume released user data is
  disposable or carry a tester conversion as a runtime compatibility path.

## Owned And Third-Party Contracts

- Everything above is about contracts this repository owns, and they are free to break. **A
  third-party provider's contract is not one of them and cannot change at all.**
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
- Where the repository names a migrations skill for that role, invoke it for the mechanics,
  what it owes the rows it breaks, and validation.
