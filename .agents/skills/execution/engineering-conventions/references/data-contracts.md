# Data Contracts

What `SKILL.md` applies when a change shapes a field, a column, a partial update or a read that can
find a value absent. What a requiredness change owes rows already stored is `pre-production`'s
**Retained Data**.

## Required Fields

- Make fields and columns required by default. Keep one nullable only when absence is a genuine
  supported domain state.
- An absent value on a read path is a schema question. First establish whether the domain requires
  it. Represent legitimate absence at the operation that can return it. When one shape represents
  both a present entity and no entity, give those states distinct representations so a present
  entity requires its identity. If the domain and the column both require a field, align the wire
  and model with the column. If the domain requires it and the column allows absence, align the
  column too. Apply `pre-production`'s **Target Contract** when a shared shape is the cause of an impossible branch.

## Partial Updates

- **A partial update expresses intent through its existing field presence or field mask.** Apply
  the fields that mechanism selects and leave every other field alone. Use the contract's own
  representation for an explicit clear. A separate control earns a place only when it expresses
  a distinct operation the update fields cannot represent.
