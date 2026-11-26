# Round 1 variants

How **Review Loop**'s round 1 changes for a delta that spans several areas or is risky.

Contents: **Split round 1 by area**, **Panel round 1 for risky deltas**.

## Split round 1 by area

When the delta spans several areas, such as packages, services or apps, and is too large for one
careful read: up to five reviewers, one per area group, each briefed with its group's paths and the
whole diff as context, so a finding that crosses groups is still seen. Merge their findings into one
ledger before answering. Later rounds go back to one reviewer over the changed code and the open
findings.

## Panel round 1 for risky deltas

When the delta touches security, permissions, auth, data loss or concurrency, round 1 goes to
`council` in **Ask** mode with the round's brief, in place of the single reviewer, and its findings
become the ledger. When round 1 is also split, the risky area group goes to `council` and the other
groups share the remaining two of the five reviewers. **Workflow**'s **Diff Review** is a separate
check that neither replaces the panel nor is replaced by it: it runs beside round 1, whoever reads
that round, on a line-pattern match.
