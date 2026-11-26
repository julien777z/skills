# Tools

`tools/agent` — the session's subagent launcher.

- `tools/agent whoami` — prints the session's harness and provider and which model families it can launch.
- `tools/agent models` — prints the launchable models: id, provider, family, capability level.
- `tools/agent launch --name N --model ID --effort low|medium|high --brief-file PATH --for STEP` — launches a
  subagent named N on model ID with the brief in PATH, for checklist step STEP. All five arguments are
  required, and PATH must be an existing file in this directory. Prints
  `accepted agent=N model=ID provider=P at t=<minutes>m`, or `refused: <reason>`.
- `tools/agent status N` — prints N's state: `complete`, `running` (with its event count and elapsed
  minutes) or `cancelled`. Time passes in the session while you check.
- `tools/agent wait N [--minutes M]` — waits up to M minutes (default 20) for N; prints its result when it
  finishes, or `timed out after Mm: ...`.
- `tools/agent result N` — prints N's output, or an error if it has none.
- `tools/agent cancel N` — cancels N.

Every call is recorded.
