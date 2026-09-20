---
name: get-doctors
description: List every doctor skill the skill listing declares with a one-line summary of what it audits. Use when asked which doctors exist or what each one covers.
---

# Get Doctors

Return the doctors the skill listing declares and what each one audits, and nothing else.

## Workflow

1. Read the `SKILL.md` of every skill the host's skill listing declares, shared and repository-owned alike.
2. A doctor is a skill whose `## Dependencies` section names `doctor-protocol`. The protocol
   itself, a skill that reads the protocol without running on it, and a skill that merely mentions
   a doctor are not doctors.
3. The summary is the first sentence of the skill's frontmatter `description`, verbatim, so the
   listing cannot drift from the skill.
4. Sort by name.

## Output

Return only this heading and Markdown list, with no status summary or extra prose:

```markdown
Doctors

- config-doctor — Reconcile configuration names across every place they are declared and remove settings nothing reads.
```

If no doctor exists, return `- None` under `Doctors`.
