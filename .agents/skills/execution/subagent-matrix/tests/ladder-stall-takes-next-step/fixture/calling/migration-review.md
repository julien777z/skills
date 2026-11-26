# migration-review (calling skill)
Purpose: an independent read of `migrate.sql` before it runs against the production ledger
(2.1 million rows).
Reviewer: one independent reviewer at the advanced capability level, high effort. No provider or
exact model is required.
Fallback policy: if the advanced level is unsupported, step down through `subagent-matrix`'s
ordinary fallback ladder, no lower than standard.
Brief to send as it stands: "Review migrate.sql for anything that fails or locks the table on a
2.1 million row ledger_entries table. Findings with file and line, rated blocker/should/nit, and a
score out of 10."
