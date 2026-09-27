# Skills Repository

## Canonical Agent Guidance

- `.agents/` is the canonical template for provider guidance. Declare scoped patterns once under
  `paths`, without a duplicate `globs` field; Agent Sync links Claude to the canonical rule and
  generates a Cursor rule with only `globs`.
- Root `AGENTS.md` holds brief always-on guidance and a topic index. Give each indexed rule a
  description that says when to read it; keep the full instructions in `.agents/rules/`.
- Rules for actions that cannot be matched to files omit `paths`. Their Codex index entries are
  read on demand. Their provider mirrors have no file gate; Claude may load them unconditionally.
