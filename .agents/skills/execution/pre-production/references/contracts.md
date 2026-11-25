# Contracts

Contracts the change touches beyond the owned target contract: a third-party provider's, a field's
requiredness and backfill, and a design's dependence on today's deployment size. `SKILL.md`'s
**Writing A Change** names this file at the point each is read.

Contents: **The Deployment's Size Is Not The Design**, **Owned And Third-Party Contracts**,
**Required Data**.

## The Deployment's Size Is Not The Design

- **Judge the mechanism, never the size of the environment it runs in.** How few rows the database
  holds, how small the instance is and how little traffic it serves describe what is deployed
  today, not what the code has to be able to do. "It is small enough today", "the table is short",
  "the instance copes", "the job finishes overnight" and "nobody has complained" are true whenever
  they are said and never for long. Ask whether the work grows with the data and whether anything
  bounds it: a mechanism that cannot grow past one process, one core or one container is still that
  on the day the same code meets a hundred times the data, and resizing is a number somebody
  revisits under pressure, where a design that scales with the work is not.
- Where the environment genuinely limits what can be *demonstrated* — a single-node database that
  cannot show contention, a dataset too small to produce a rate — say so plainly and build for the
  target anyway. A design that cannot yet be proven here is still the right design; one that cannot
  scale is not, and a measurement taken on a small deployment is evidence about that deployment only.
- This is not a license for speculative distribution. The bar is unchanged: the cleanest result for
  the contract the released product needs. It removes exactly one argument from the discussion — that
  the current deployment is small — and settles nothing else about how much scale the work warrants.

## Owned And Third-Party Contracts

- `SKILL.md`'s **Target Contract** is about contracts the user owns and can change by migrating every consumer
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
  column too. Apply `SKILL.md`'s **Target Contract** when a shared shape is the cause of an impossible branch.
- For a requiredness change, establish the affected data's retention scope under `SKILL.md`'s **Product State**
  before deciding what its revision keeps or clears; required columns do not themselves create an
  obligation to preserve disposable or nonexistent rows.
- For retained values, use the authoritative source where one exists and a type-valid placeholder
  only where none exists and the placeholder expresses a legitimate domain state. `SKILL.md`'s
  **Target Contract** prohibition on invented identities, ownership, and scopes also applies during
  migration. Never overwrite a known retained value, fabricate a placeholder in runtime code, or
  keep a permanent schema default solely to make a migration convenient.
- **A backfill writes each row's value under the new contract, never one chosen so existing rows
  keep behaving as before.** A flag set on every pre-change row so it keeps the old outcome, such as
  staying exempt from a new check, closed to a new path, or treated as the old kind, is a legacy
  fallback written into data. So is a branch on a creation date or a stored version that does the
  same. Where the new field records a fact, such as who did something or when, backfill that fact
  from its authoritative source. The tell is a description or comment saying that rows from before
  the change keep the old behavior; keeping it needs the user's approval, as any legacy support
  does.
