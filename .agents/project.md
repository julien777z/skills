# Skills Repository

## Canonical Agent Guidance

- `.agents/` is the canonical template for provider guidance. Declare scoped patterns once under
  `paths`, without a duplicate `globs` field; Agent Sync links Claude to the canonical rule and
  generates Cursor's `globs`.
