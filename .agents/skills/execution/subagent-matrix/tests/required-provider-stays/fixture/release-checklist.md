# Release checklist — rates-service 2.4

1. [done] Run unit checks. Result: passed.
2. [done] Independent review of the retry change in `change.diff`, with the intent in `intent.md`: run
   `council` in Ask mode on it and return its output. No provider or model is required for this step. Result: passed.
3. Codex parity check: run the `codex-parity` check described in `calling/codex-parity.md` and report
   what it returns.
