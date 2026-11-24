---
description: Apply when writing or editing a README or other reference documentation.
alwaysApply: false
paths:
- '**/README.md'
- '**/docs/**/*.md'
---

# README Rules

## Content

- A README's reader is a person using or developing the project, so a README holds what the
  project is, how to run or use it, where a developer finds its parts, and a Local Development
  section with the commands to install, run, and validate it locally. Anything only an agent acts on
  goes in the repository's rules and skills instead, with what one repository's agents must do in
  `.agents/project.md`: an environment variable or credential an agent
  session reads, even one a person adds to a cloud environment for the agent; a tool installed for
  agents; a procedure only agents follow.
- After drafting or editing READMEs and other reference documentation, compare each statement with
  the current capabilities and required steps. When their positive description already communicates
  the operation, delete corresponding claims about absent behavior or unneeded operations,
  including positive paraphrases. Retain a limitation only when it contributes a supported input,
  option, constraint or required step not otherwise stated. Remove historical comparisons. Describe
  available capabilities without assuming how consumers will use the project or framing guidance as
  prohibitions such as "never do X."
- Remove repeated explanations and prefer short sections, bullets, tables, and focused examples
  over long prose.
- **Order sections for a reader arriving cold, never by what landed most recently.** A section goes
  where its vocabulary is already established: one whose examples are all of some construct follows
  the section that introduces that construct, however central the behavior it describes is.
- A section grown into a wall of prose carries rules a table states better: move those rules into a
  table and leave the prose only what a table cannot say, such as caveats, reasons and exceptions.
- Write in plain language, as if explaining the repository to a colleague. Avoid repeating internal
  terms such as `canonical`; name the file or say `source` when that is clearer.

## Headings

- Write the top-level heading in every `README.md` in title case.
- Convert slug-style project names into readable words, such as `example-service` becoming
  `Example Service`.

## GitHub Actions And Libraries

- Lead with the consumer-facing purpose; do not state that an action or library is reusable when
  that is already evident from the project.
- Place a concise, list-based Features section immediately after the introduction.
- Include little to no implementation or internal technical detail; describe public capabilities
  and outcomes instead.
- Follow Features with an Example or Examples section.
- Introduce each example with a one- or two-line description of its purpose, followed by a small
  code example.
- In cron-based examples, use a conventional schedule such as every Monday and add an inline
  comment translating the cron expression into that plain-language schedule.
- For reusable GitHub Actions, include an Inputs table with the input name, default value, and
  purpose.
