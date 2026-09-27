---
description: Read when creating or editing a README, including feature summaries, examples, and input tables for reusable GitHub Actions or libraries.
alwaysApply: false
paths:
- 'README.md'
- '**/README.md'
---

# Readme Rules

## README

- Describe available capabilities without assuming how consumers will use the project or framing guidance as prohibitions such as "never do X."
- Remove repeated explanations and prefer short sections, bullets, tables, and focused examples over long prose.

### GitHub Actions And Libraries

- Lead with the consumer-facing purpose; do not state that an action or library is reusable when that is already evident from the project.
- Place a concise, list-based Features section immediately after the introduction.
- Include little to no implementation or internal technical detail; describe public capabilities and outcomes instead.
- Follow Features with an Example or Examples section.
- Introduce each example with a one- or two-line description of its purpose, followed by a small code example.
- In cron-based examples, use a conventional schedule such as every Monday and add an inline comment translating the cron expression into that plain-language schedule.
- For reusable GitHub Actions, include an Inputs table with the input name, default value, and purpose.
- Include a Local Development section with the commands needed to install, run, and validate the project locally.

### Titles

- Write the top-level heading in every `README.md` in title case.
- Convert slug-style project names into readable words, such as `example-service` becoming `Example Service`.
