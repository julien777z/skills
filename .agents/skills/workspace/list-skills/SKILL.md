---
name: list-skills
description: List every skill available to this session — the shared skills repository's skills and the current repository's own skills, in separate sections — each marked user- or model-invocable with a one- or two-line summary. Use when the user asks which skills exist, what a skill does, or what they can invoke.
short_description: 'List shared and repository skills with who can invoke each and what it does.'
---

# List Skills

## Sources

- **Skills repository**: every `SKILL.md` under the shared skills repository's `.agents/skills/`,
  read from the checkout the user-level skill root resolves to, or a fresh read of that repository's
  default branch when no checkout is present.
- **This repository**: every `SKILL.md` under the current repository's `.agents/skills/`. When the
  current repository is the skills repository, or has no skills, the section holds `- None`.

Read each skill's frontmatter from its canonical `SKILL.md`; never from a provider mirror, a skill
catalogue, or memory. Plugin and built-in harness skills are outside both sources.

## Each Entry

- **Invocation**: `user` when the frontmatter sets `disable-model-invocation: true`, otherwise
  `model`.
- **Summary**: the `short_description`, or, without one, the `description` cut to one or two lines
  that say what the skill does. Never invent a summary the frontmatter does not support.

## Categories

- Both sections use the skills repository's categories: its folders under `.agents/skills/`, each a
  sub-section titled by the folder name in title case, in name order.
- A skill with no folder, or with a folder the skills repository lacks, goes under the category
  whose skills do the same kind of work, judged from its summary; one that fits none goes under
  `Other`, listed last.
- Sort entries by name within each category, and leave out a category with no entries in that
  section.

## Output

Reply in chat with exactly this shape; the listing is the answer, so it is not sent as a file:

```markdown
## Skills repository

### <Category>
- `<skill-name>` — **<user | model>** — <summary>

## This repository (`<owner>/<repo>`)

### <Category>
- `<skill-name>` — **<user | model>** — <summary>
```

A section with no skills holds `- None` in place of its categories.
