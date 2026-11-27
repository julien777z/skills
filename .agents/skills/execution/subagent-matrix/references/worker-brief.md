# Worker Brief

The brief for a worker that implements a scope or fixes findings, launched under `SKILL.md`'s
**Dispatch**. The worker gets no history, so the brief carries everything; fill every `<…>` field.
A fix brief adds the `Findings` block and keeps the rest.

```text
Task: <implement | fix> <one line naming the outcome>
Intent: <the user's words for this work, each decision recorded on it, and what is out of scope>
Scope: <the plan step, or the coupled steps in order, with the invariant the work keeps>
Files: <exact paths to change; they bound the scope, not the design>
Repo: <abs path> Worktree: <abs path> Branch: <the pull request's branch> Head: <sha> (one line per pull request of a bulk set)
Rules: <rule files whose patterns match those paths; the repository's `.agents/tools/` folder>
Reuse: <one receipt per addition the plan names: what it does · searched · found · reuse | extend | new: why>
Push checks: <each fast check command with its scope; never a test suite>
Suites: <each test suite command with its scope, run once at the end | none: a later assignment ends the task>
Result: <abs path the complete report is written to>
Findings (fix only): <each finding verbatim with its id, severity and the reviewer's remedy · remedies
already tried and why each failed · round <n> of 3>

A finding's remedy is the reviewer's proposal, never the fix itself. Before applying one, check it
against every intent the brief names: a repair that also removes a check, a behavior or a test case
the base branch carries, one the finding does not name as its defect, keeps that one beside the new
one, unless the intent says it goes; when the remedy as written would drop it, apply the remedy
beside it and say so in the report.

Before writing anything the Reuse lines do not cover (a function, component, hook, type, constant
set, fixture, configuration entry or block of logic), search the repository and its shared
packages by what it does and by its key operation, and write its receipt. Reuse an existing owner,
or extend it with the one parameter or condition it lacks; write new code only with the search
that found no owner, and add no parameter, option or branch for a condition nothing uses.
Fix every defect you meet where `pre-production`'s **Scope Follows The Defect, Not The Request**
places it. Hand up work outside your assignment so the coordinator can apply that placement rule. Leave alone
only cleanup past the repository's incidental size budget and a choice that is the user's, and
report each.
Push: commit each coherent step and push it once its Push checks pass, at least every five minutes
of work. Run the Suites once, when your assignment's changes are complete, then rerun only the
suites covering each fix. Fetch and rebase unpushed commits onto the remote branch before each
push; never amend or rebase a pushed commit. End with nothing uncommitted and nothing unpushed.
A review, gate or further worker your step needs and you cannot launch is handed up to the agent
that briefed you, never done in process.

Report, written to Result and returned:
BRANCH: <branch> HEAD: <sha>
CHANGED: <file: what changed, one line each>
REUSE: <one receipt per addition made, planned or not: what it does · searched · found · decision>
CHECKS: <command: result, one line each; a suite not run: owed at the end>
FINDINGS (fix only): <id: fixed at file:line | disagree: evidence>
LEFT ALONE: <item: why, or none>
OPEN: <question or hand-up, or none>
```

The delegating agent reads the head and each `CHECKS` result at its source before building on
them. A report with no `REUSE` receipt for something the diff adds is sent back to the worker
before any dependent work starts.
