# Vendor Guidance

Contents: the vendor pages to fetch, what each host loads and caps, and a dated summary of what
the pages said when last fetched. The doctor's measurement rewrites the summary and the fetch
dates on every run; a redirect becomes a new row with its target.

## Pages

| Vendor | Topic | URL | Last fetched | Redirect seen |
|---|---|---|---|---|
| Anthropic | Agent skills overview and frontmatter | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | 2026-09-05 | from docs.claude.com |
| Anthropic | Skill authoring best practices | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | 2026-09-05 | from docs.claude.com |
| Open spec | Agent skills specification | https://agentskills.io/specification | 2026-09-05 | none |
| Anthropic | Claude Code skills and frontmatter | https://code.claude.com/docs/en/skills | 2026-09-05 | none |
| Anthropic | Claude Code memory and rules files | https://code.claude.com/docs/en/memory | 2026-09-05 | none |
| Anthropic | Claude Code best practices | https://code.claude.com/docs/en/best-practices | 2026-09-05 | from anthropic.com/engineering |
| Anthropic | Effective context engineering | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | 2026-09-05 | none |
| Anthropic | Equipping agents with skills | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | 2026-09-05 | none |
| Open format | AGENTS.md | https://agents.md/ | 2026-09-05 | none |
| OpenAI | Codex skills | https://learn.chatgpt.com/docs/build-skills | 2026-09-05 | from developers.openai.com/codex |
| OpenAI | Codex AGENTS.md discovery and cap | https://learn.chatgpt.com/docs/agent-configuration/agents-md | 2026-09-05 | from developers.openai.com/codex |
| OpenAI | Skills authoring narrative | https://developers.openai.com/blog/skills-agents-sdk | 2026-09-05 | none |

## Hosts

| Host | Rules-file target | Skill body target | Listing budget | Description truncation | Rules cap |
|---|---|---|---|---|---|
| Claude Code | under 200 lines per always-loaded file | under 500 lines, about 5k tokens | 1% of context by default | 1,536 characters with the when-to-use field | none; a file over 4 MiB is skipped |
| Codex | none published | none published | 2% of context, or 8,000 characters | none published | `project_doc_max_bytes`, 32 KiB by default; content past it is dropped |
| Cursor | none published | none published | none published | none published | none published |

After compaction Claude Code re-attaches only the first 5k tokens of each invoked skill, within
25k tokens across all of them. A SessionStart hook's plain stdout enters context on startup,
resume, clear, compact, and fork.

## Summary, fetched 2026-09-05

- The context window is a public good, and the model is already very smart. Per paragraph: does it
  justify its token cost? Per rule line: would removing it cause a mistake? If not, cut it. Bloated
  rules files cause the model to ignore the instructions that matter.
- A rules file holds facts and every-session conventions: build commands, layout, conventions that
  differ from defaults, gotchas. Procedures and sometimes-relevant knowledge belong in skills.
  Advisory text that must be deterministic becomes a hook.
- A skill is a directory with `SKILL.md`; `name` and `description` are the only fields both vendors
  read. `name` equals the directory, lowercase with hyphens, at most 64 characters. `description`
  is 1–1024 characters, third person, and says what the skill does and when to use it; Codex adds
  when it should not trigger. Everything about when to use the skill goes in the description, not
  the body.
- Progressive disclosure: metadata always loaded, body on trigger, bundled files on demand. Keep
  references one level deep; a reference over 100 lines opens with a table of contents. Scripts run
  without their code entering context.
- Match the degrees of freedom to the task: a heuristic where several approaches are valid, an
  exact script where the operation is fragile. Over-specified brittle logic and vague generalities
  are the two failure modes; the target is specific enough to guide and flexible enough to leave
  judgement.
- Emphasis is scarce: capitalised imperatives on many lines mean none stands out. Explain the why.
- Offer one default and an escape hatch, never a menu. Avoid time-sensitive text. Keep terminology
  consistent. Never assume a package is installed.
- Contradictory rules are picked arbitrarily; review nested rules for conflicts.
- OpenAI: the rules file carries the mandatory skill-usage triggers; if routing is unreliable, fix
  the metadata before adding code; keep each skill to one job; prefer instructions over scripts
  unless behaviour must be deterministic.
- Evaluate before documenting: at least three scenarios and a no-skill baseline, tested on the
  lower-tier models as well as the strongest.
