# Reviewer Brief

The `review-pass` skill's brief for each **Review Loop** round, and its **Combined review** form for
a **Combined Review** round. The reviewer gets no history, so the
brief carries everything; fill every `<…>` field.

```text
Review only. Do not edit, commit, push, comment on PRs, or start subagents.
Repo: <abs path> Base: <sha> Intent: <intent> Out of scope: <scope> Checks: <results>
Rules: <repository rule files whose patterns match the changed paths, or none>
Whole: <each skill or rule the diff touches, the 500-line budget of a SKILL.md or rule, and the real case, or none>
Guidance intent: <base guidance, user's explicit requirements and corrections in their words, and acceptance-gate rubric's Guidance Intent section, or none>
Reuse and removal: <owning criteria, planning evidence, and the candidate and callee sources the evidence cites, or not applicable>
See: git diff <base> [-- <paths>]; git status --short (read untracked files).
Read surrounding code. Find bugs, broken callers, mismatch with intent, and unsafe
handling of user input (paths, patterns, queries, markup).
Independently reconstruct the supplied reuse and removal record from the candidate and callee
sources. Include every field in the verdict when it applies.
Flag a setting, env var, secret, config key or workflow input left optional or given an unsafe default, or
code that skips or weakens its work when one is unset, unless its owner documents that absence
("tests lack it" does not). A default production gets the full behavior from is fine.
Flag breaks of the listed rules; skip other style unless it hides a bug. Flag code, tests or guards the intent does not need.
Read each Whole skill or rule in full: flag a requirement it states twice, growth past that budget,
and a step of the real case a reader of the result would take wrongly.
Apply Guidance Intent to the resulting package and to every suggested remedy. An explicit
requirement contradicted on any path is a blocker. Missing evidence holds approval.
blocker = intended case wrong. should = a real bug callers will hit, an unsafe input,
an optional setting above, a workaround, a duplicate of an existing helper, or a break of a listed rule. nit = the rest.
List problems you see outside the change separately, with the files a fix would touch.
Reply:
VERDICT: APPROVE or CHANGES
Guidance intent evidence: <controlling requirement and decisive path and evidence, if applicable>
Reuse and removal: <completed Source, Smallest change, and Proof fields, or not applicable>
S1 [blocker|should|nit] <file>:<line> <claim>. Fix: <suggestion>
O1 [outside] <files> <claim>
```

A later round sends this brief again with the ledger (`fixed:`, `disagree:`, `declined:`, each with
evidence), the same base diff and the change since the last round, and asks the reviewer to check
open ids and changed code, marking each `resolved` or `still open: <reason>`; a `Whole:` skill or
rule is still read in full at the new head every round.

## Combined review

```text
Review only. Do not edit, commit, push, comment on PRs, or start subagents.
Set: for each pull request: <repo abs path> Base: <sha> Head: <accepted sha> Intent: <intent>
Description: <title and body> See: git diff <base>...<head>
Changed since the last combined round: <per head, git diff <read head>..<head>, or first round>
Each pull request passed its own review. Read every diff together and report only flaws of the
combination, each naming the pull requests it needs:
- an interface, contract, schema, configuration name or generated type one provides and another
  consumes that does not match;
- a merge or deploy order under which an intermediate state breaks: name the safe order or the
  missing guard;
- one concern solved twice, or two mechanisms for one thing, across the set;
- behavior correct in each and wrong with both applied;
- a trust boundary, permission or data exposure that opens only across the set, held to the
  security-audit rubric's bar for an exploitable finding: <rubric path>;
- guidance that describes behavior another pull request in the set changes;
- a claim in one description that another contradicts.
blocker, should and nit as in the round brief above.
Reply:
VERDICT per head: <pull request> <head> ACCEPT or CHANGES
C1 [blocker|should|nit] owner: <pull request, or both> <file>:<line> <claim>. Fix: <suggestion>
Order: <safe merge and deploy order, or any>
```
