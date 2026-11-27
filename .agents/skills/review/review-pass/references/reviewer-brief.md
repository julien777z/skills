# Reviewer Brief

The `review-pass` skill's brief for each **Review Loop** round, and its **Combined review** form for
a **Combined Review** round. The reviewer gets no history, so the
brief carries everything; fill every `<…>` field.

```text
Review only. Do not edit, commit, push, comment on PRs, or start subagents.
Repo: <abs path> Base: <sha> Intent: <intent> Out of scope: <scope> Checks: <results>
Rules: <repository rule files whose patterns match the changed paths, or none>
Whole: <each skill or rule the diff touches, with the skill-pass skill and its authoring reference to read, or none>
Guidance intent: <base guidance, user's explicit requirements and corrections in their words, the editor's statement of scope, and acceptance-gate rubric's Guidance Intent section, or none>
Reuse receipts: <the author's receipt line per addition, and for a shared design its Source, Smallest change and Proof fields with the sources they cite, or none written>
Review: <the unreviewed delta: git range-diff <base>..<reviewed head> <base>..HEAD, or git diff <base> [-- <paths>] when the delta is the complete merge-base diff>
Context: git diff <base> [-- <paths>]; git status --short (read untracked files). Judge the delta; read the rest only to understand it.
Read surrounding code. Find bugs, broken callers, mismatch with intent, and unsafe
handling of user input (paths, patterns, queries, markup).
For every function, component, hook, type, constant set, fixture, configuration entry or block of
logic the diff adds, search the repository and its shared packages yourself, by what it does and by
its key operation, whether or not a receipt is supplied. A receipt is checked against your search,
never its starting point. Flag (a) a duplicate of an existing owner; (b) new code where an existing
owner needed one more condition or parameter; (c) a parameter, option, prop, flag or branch added
for a condition no caller produces, or that every caller sets the same way.
Read the code-simplify rubric for additions. For each added file, read its closest candidate
owners and check placement under **Reuse And Removal**, including a broader rename. Report the paths read and the
responsibility or boundary that decides placement. Apply code-simplify's **No forwarding layers**
to callables the diff adds or changes, including fixed values in an owned interface. Missing placement
evidence holds approval. Apply the simplification rubric's severity to a violated requirement.
Flag a setting, env var, secret, config key or workflow input left optional or given an unsafe default, or
code that skips or weakens its work when one is unset, unless its owner documents that absence
("tests lack it" does not). A default production gets the full behavior from is fine.
Flag breaks of the listed rules; skip other style unless it hides a bug. Flag code, tests or guards the intent does not need.
Read each Whole skill or rule in full and make the checks skill-pass's Reviewer Brief assigns a
review-loop reviewer, against the statement of scope and standing guidance; leave the checks it
assigns another reader to that reader.
Apply Guidance Intent to the resulting package and to every suggested remedy. An explicit
requirement contradicted on any path is a blocker. Missing evidence holds approval.
blocker = intended case wrong. should = a real bug callers will hit, an unsafe input,
an optional setting above, a workaround, a reuse finding (a), (b) or (c), or a break of a listed rule. nit = the rest.
The change is the pull request's whole diff against its merge base, whatever this round checks; code it wrote, moved or
recreated is inside it. List problems you see outside it separately, with the files a fix would touch.
Reply:
VERDICT: APPROVE or CHANGES
Guidance intent evidence: <controlling requirement and decisive path and evidence, if applicable>
Reuse search: <per addition: terms searched · candidate paths read · reuse, extend or new stands | finding id. For added files, give the chosen owner or reason to separate.>
S1 [blocker|should|nit] <file>:<line> <claim>. Fix: <suggestion>
O1 [outside] <files> <claim>
```

A later round goes to the same reviewer where the host can continue an agent: it gets the ledger
(`fixed:`, `disagree:`, `declined:`, each with evidence) and the change since the last round, and
checks open ids and changed code, marking each `resolved` or `still open: <reason>`. Where the host
cannot continue it, a new reviewer gets this brief again with the ledger, the same base diff and the
change since the last round. A `Whole:` skill or rule is read in full at the new head every round.

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
  bar for an exploitable finding in the `security-audit` skill's rubric reference;
- guidance that describes behavior another pull request in the set changes;
- a claim in one description that another contradicts.
blocker, should and nit as in the round brief above.
Reply:
VERDICT per head: <pull request> <head> ACCEPT or CHANGES
C1 [blocker|should|nit] owner: <pull request, or both> <file>:<line> <claim>. Fix: <suggestion>
Order: <safe merge and deploy order, or any>
```
