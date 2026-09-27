---
description: Essential guidance for every session and a route to more detailed topic rules.
alwaysApply: true
---

# Global Rules

- Read relevant shared rules before acting on their topics. A repository's generated `AGENTS.md`
  indexes its scoped rules; for user-level guidance, list and open applicable files under
  `~/.codex/rules/`, `~/.claude/rules/`, or `~/.cursor/rules/` when the harness does not load them.
- Implementing a plan or fixing an issue does not by itself authorize a merge, deployment,
  publication, or release. Read the installed `task-authority.md` and `github.md` rules before
  those actions.
- Never commit or push agent changes directly to the default branch. Read the installed
  `github.md` rule before other GitHub operations.
- Invoke a user-triggered action skill only on the user's direct request. Guidance maintenance
  and recording a deferral are exceptions described in `task-authority.md`.
- Never stage generated provider files by hand; Agent Sync owns their generation and commits.

## User-Facing Output

- Invoke `i-have-adhd` before the first response a user reads in the session, whether or not the
  user invoked it or the running skill names it. It shapes every response a user reads — an answer,
  a plan put for approval, a report, a summary, a question — until the reader's stop phrase. Per-item
  detail past five items — findings, rows — and any gated plan a skill requires go in a linked file.
