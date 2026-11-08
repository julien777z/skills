# Reviewer Brief

The `review-pass` skill's brief for each **Review Loop** round. The reviewer gets no history, so the
brief carries everything; fill every `<…>` field.

```text
Review only. Do not edit, commit, push, comment on PRs, or start subagents.
Repo: <abs path> Base: <sha> Intent: <intent> Out of scope: <scope> Checks: <results>
See: git diff <base> [-- <paths>]; git status --short (read untracked files).
Read surrounding code. Find bugs, broken callers, mismatch with intent, and unsafe
handling of user input (paths, patterns, queries, markup).
Flag new code that re-implements a helper the repo already has (cite it), and
abstractions with a single implementation. Flag workarounds: a remedy that hides
the symptom (folds away, skips, retries, catches, special-cases) instead of fixing its cause.
Skip style unless it hides a bug. Flag code, tests or guards the intent does not need.
blocker = intended case wrong. should = a real bug callers will hit, an unsafe input,
a workaround, or a duplicate of an existing helper. nit = the rest.
List problems you see outside the change separately, with the files a fix would touch.
Reply:
VERDICT: APPROVE or CHANGES
S1 [blocker|should|nit] <file>:<line> <claim>. Fix: <suggestion>
O1 [outside] <files> <claim>
```

A later round sends this brief again with the ledger (`fixed:`, `disagree:`, `declined:`, each with
evidence), the same base diff and the change since the last round, and asks the reviewer to check
open ids and changed code only, marking each `resolved` or `still open: <reason>`.

Severity is the same scale every review in this repository uses:

| Severity | Meaning |
| --- | --- |
| `blocker` | The intended case is wrong. |
| `should` | A real bug callers will hit, an unsafe input, a workaround, or a duplicate of an existing helper. |
| `nit` | Everything else. |
