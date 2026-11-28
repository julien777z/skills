# Simplification scope

What `SKILL.md`'s **Ongoing Simplification** covers while the work is built.

## Ownership

Own each coherent feature through integration: the primary agent settles dependencies, product
decisions and the combined result. Simplify a feature as it is built. Assign a worker an
independently owned scope with a concrete boundary and return condition, not an arbitrary slice of
the primary agent's feature. Keep admitted cleanup with its feature; an independently selected
cleanup follows its own stated scope and ownership. When cleanup crosses an interface or repository,
bring its producer and consumers to a coordinated checkpoint, verify compatibility at both ends, and
keep the cleanup named until that check passes. Neither a slower dependency nor unrelated work drops
an encountered issue from the task.

## What The Pass Covers

- Simplifying as the work is built covers three things, never the diff hunks alone: the
  **changes** themselves, the **similar code** they resemble, and the **sibling modules** around them.
  - **Changes**: the full contents of every file the task has touched so far, not only the lines
    edited in the current batch.
  - **Similar code**: every other place in the repository already expressing the same concept,
    shape, or operation as the changed code — a near-duplicate helper, a parallel implementation,
    a second representation of one value. `code-simplify`'s **Before Choosing A Design** search
    found these before the edit; this pass rereads its receipts against the code as built. A copy of
    the change's own mechanism is the change's scope under `scope-of-change`'s **Scope Follows The
    Defect, Not The Request**: give the mechanism one owner, move every consumer onto it and delete the copies.
    Other code the change resembles and should be one thing with is made one thing within
    `scope-of-change`'s size budget. Follow that rule's placement for widened cleanup and use
    `defer-scope` for work it defers.
  - **Sibling modules**: the other modules in each changed file's package, which is where a
    misplaced piece of logic and its rightful home become visible together.
- When a repair changes another file, inspect its complete contents and relevant owners to verify
  that repair and its necessary consumer updates. This expands validation, not permission for a
  new cleanup frontier; use `scope-of-change`'s scope decision before adding another correction.
- Check the combined scope against the requested outcome, including all incidental changes;
  individually useful edits can add up to a disproportionate change. Ask only about a genuine
  decision **Encountered Issues** reserves for the user.
