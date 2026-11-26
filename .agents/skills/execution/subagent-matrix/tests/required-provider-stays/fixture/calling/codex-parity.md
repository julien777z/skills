# codex-parity (calling skill)
Purpose: judge whether the retry delays in `change.diff` interact badly with the Codex runtime's
30-second silent-task kill (see `intent.md`).
Required: dispatch this review through `council` on the Codex provider only. Three independent
reviewers at the advanced tier, all on Codex. A reviewer on another provider cannot assess Codex runtime
scheduling, so a result from one does not count.
Brief to send as it stands: "Assess whether the sleep(2) retry loop in change.diff can leave a Codex
task silent for more than 30 s, and whether the final failure still reaches the caller. Findings with
file and line, rated blocker/should/nit, and a score out of 10."
