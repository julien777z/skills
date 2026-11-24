---
name: get-doctors
description: List every doctor skill the skill listing declares with a one-line summary of what it audits, and give the order to run several of them in a row. Use when asked which doctors exist, what each one covers, or which doctor to run first.
short_description: 'List every doctor skill with what it audits, and the order to run several in a row.'
---

# Get Doctors

Return the doctors the skill listing declares and what each one audits, or the order to run
several of them in a row, and nothing else.

## Dependencies
- `doctor-protocol`

## Workflow

1. Search, never read whole, the `SKILL.md` files of the skills the host's skill listing
   declares, shared and repository-owned alike, for the ones that declare `doctor-protocol` as a
   dependency: in a frontmatter dependency field or as an entry of the `## Dependencies` section.
2. A doctor is one of those matches whose body runs the protocol. Search the matches for the
   protocol's name and read only the matching lines: a doctor carries the instruction to run it.
   The protocol itself, a skill that declares the protocol to read it without running on it, and
   a skill that merely mentions a doctor are not doctors.
3. Read only each doctor's frontmatter. The summary is the first sentence of its `description`,
   verbatim, so the listing cannot drift from the skill.
4. Sort by name.

## Run Order

When the request is for the order to run several doctors in a row, or a doctor asks which runs
after it, build the listing above and order it instead of sorting by name. Each run changes what
the later ones read, so place each doctor by what its description says it audits and fixes:

1. the doctor whose fixes close vulnerabilities, since they add guards and tests;
2. the doctor that corrects contracts and schemas, so models settle;
3. the doctor that removes unneeded code, tests and configuration;
4. the doctor that audits what the product's pages show and say, so its fixes land on the
   components that remain;
5. the doctor that audits the tests that remain;
6. the doctor that audits documentation, which resolves references to everything removed;
7. the doctor that audits agent guidance, last.

A doctor none of these describes goes after every doctor whose fixes change what it reads and
before every doctor that reads what it changes; one that fits nowhere goes just before
documentation. When the request names only some doctors, return those in this order.

## Output

For the listing, return only this heading and Markdown list, with no status summary or extra prose:

```markdown
Doctors

- <doctor name> — <first sentence of its description, verbatim>
```

If no doctor exists, return `- None` under `Doctors`.

For the run order, return only this heading and numbered list:

```markdown
Doctor run order

1. <doctor name> — <first sentence of its description, verbatim>
```
