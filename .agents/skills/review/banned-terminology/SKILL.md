---
name: banned-terminology
description: Owns the banned-terms list in resources/banned_words.json and enforces it. Use when naming anything, when reviewing a name, when the user says a term is bad, confusing, or should not be used, when they reject a replacement an entry recommends, when they lift a ban, or whenever the decision is about a word rather than one symbol.
---

# Banned Terminology

`resources/banned_words.json` is the list, and this skill is what makes it bind. Each entry carries
the term, what to use instead, why the term fails, and any replacement already rejected.

Never use vague, cute, or placeholder terminology in identifiers, docstrings, comments, or test
names. Name things for the behavior they actually have. This holds for **new and pre-existing
code**: touching a file that still uses a banned term means renaming it.

If you reach for a placeholder-ish term a future reader could not decode from the name alone, pick a
more intuitive name rather than adding it to the list.

## Enforcing the list

Read `resources/banned_words.json`, and the **Banned Terms** table in the repository's project
guidance where one exists, before naming anything new and before accepting a name in review. The
file holds the terms every repository bans; the table holds the terms one repository bans for its
own domain, in the same shape.
An entry's `use_instead` is the replacement; where one word hides several behaviors it names each,
and picking one for the whole inventory is what produces `assert_user` for a function that creates a
user.

`rejected_replacements` records substitutes already turned down. Reaching for one repeats a round
trip the list exists to prevent.

A term reaching a proto message, an RPC, a route, or a stored value makes the rename a deliberate
contract break, reported per the repository's rules rather than worked around.

## When the list itself changes

The decision is about a **word** rather than one symbol — the objection would apply anywhere the
word appeared:

- **Adding** — "X is a bad name", "I don't like X terminology", "don't use X", "rename X everywhere".
  Judging a term unintuitive **is** the decision to ban it; do not wait to be asked for the entry
  separately.
- **Updating** — the user rejects the replacement an entry recommends, or a better one is agreed.
  The entry changes, the old replacement moves to `rejected_replacements`, and every call site that
  took the old advice changes with it.
- **Removing** — a ban is lifted, or an entry describes a distinction the codebase no longer makes.

Renaming a single function, class, or variable is an ordinary edit and does not run this skill.

### Adding or updating

1. Write or amend the entry first, so the decision survives whatever happens to the sweep.

2. **Take the inventory before renaming anything**, so the size is known up front rather than
   discovered halfway:

   ```bash
   grep -rn "\b<term>_[a-z_]*\|\b<Term>[A-Z][a-zA-Z]*" --include="*.<ext>" . \
     | grep -v "/\.venv/\|__pycache__\|node_modules\|/generated/" \
     | grep -o "<term>_[a-z_]*\|<Term>[A-Za-z]*" | sort | uniq -c | sort -rn
   ```

3. **Sort the inventory by what each identifier does**, then rename per behavior.

4. **Leave third-party names alone.** A standard-library or SDK identifier carrying the term
   (`asyncio.ensure_future`, a `json` keyword argument, a generated `*Stub`) is not ours to rename.
   Rename only what this repository declares, and say in the pull request which external names still
   carry the word.

5. **Rename every usage the term reaches** — identifiers, docstrings, comments, test names, fixture
   names, the wire contracts that carry them, and the examples inside rule files.

### Removing

Delete the entry and nothing else. Names already changed are not evidence of the old rule and do not
get reverted; a ban lifting means the word is available again, not that the codebase owes it a
return. Rename back only where the user asks.

## Bar

- The list carries the decision, not only the diff.
- After an add or an update, the inventory command returns nothing this repository owns.
- Suffixes and compounds went too — banning a word does not leave `<term>ed` or `<term>_status`
  standing.
