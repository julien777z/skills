---
name: security-audit
description: Must be used before writing or changing code that crosses a trust boundary — input handling, authentication, authorization, sessions, secrets, cryptography, deserialization, file paths, subprocesses, outbound requests, templates — and for any security review of a branch, pull request or pending changes. Its rubric owns what counts as an exploitable finding, the precedents that rule false positives out, whether a credential an agent has seen counts as exposed in any task, how code is built safely, and the smallest fix; the skill reports, and its caller owns what happens to each finding. Use when asked to check a change for security bugs or to security-review a change.
short_description: 'Security guidance for writing code and reviewing a change for exploitable vulnerabilities.'
---

# Security Audit

Find the **exploitable vulnerabilities with real impact** a change adds or makes reachable, and
build code that crosses a trust boundary so it adds none. The skill's rubric reference,
`references/rubric.md`, holds what counts as a finding, what it is worth, which precedents rule a
finding out, how such code is built, and what a remedy costs; read it whole before writing or
reviewing and apply it throughout. This file holds how that judgment is applied to one change.

## Dependencies
- `subagent-matrix`
- `change-scope`
- `writing-conventions`

## While Writing Code

Before writing or changing code that crosses a trust boundary — input handling, authentication,
authorization, sessions, secrets, cryptography, deserialization, file paths, subprocesses,
outbound requests, templates — read the rubric and apply **Building It Safely** to every line the
change writes. A finding in those lines is the change's own defect: it is fixed in the change,
never reported for a later decision.

## 1. Scope

A security review of a branch, a pull request or pending changes reviews the change, because the
change is what its caller can still alter before it merges. This skill's scope is always a change:
a request to audit a whole codebase, with no change in question, is not run here, and goes to the
codebase security audit the skill listing describes.

1. Take the change the caller names. Otherwise use the merge-base diff against the repository's
   remote default branch plus the untracked files the branch adds.
2. Read every changed line with the callers, sinks and trust boundaries it reaches, so a trace can
   run past the hunk: the entry points that reach it, the authentication and authorization on that
   path, and the sinks its data reaches.
3. Choose from the skill's [attack classes](references/attack-classes.md) the classes those paths
   can carry. Hunt what the change adds or makes reachable; a pre-existing finding met on that path
   is still a finding.

## 2. Review

- **Small scopes in process.** When one reader can hold the diff and everything it reaches at once,
  review in process and start no subagents. Apply the skill's [hunting](references/hunting.md)
  methodology and its validation rules, then try to disprove each finding yourself with the
  refuter's tests in the skill's [validation](references/validation.md) reference.
- **An invocation that cannot launch agents runs in process over any scope**, and its result says
  the review read in process, so its caller knows no independent refuter checked a finding.
- **Larger scopes by slice.** Partition the reach by trust boundary or subsystem into at most four
  slices, the riskiest first, and launch one read-only hunter per slice in parallel. Each gets the
  scope's map from **Scope**, its slice and attack classes, and the hunting reference's prompt. A
  hunter may start at most two research agents of its own, as that reference allows, so a review
  starts at most twelve hunting agents.
- **Every finding a hunter returns faces a refuter before it is reported.** Merge findings that
  share a root cause, then give each remaining finding one fresh read-only refuter with the
  validation reference's refute prompt, all in parallel: a hunter is biased toward keeping what it
  found. At most ten refuters run; past ten findings, each refuter takes the findings of one
  subsystem.
- **Launch each agent through `subagent-matrix`** at its specialist capability level with
  `advanced` as its fallback for authorized defensive work, including a research agent a hunter
  starts, whose brief carries that selection.
- **Subagents report; the parent decides.** The parent checks each confirmed finding's trace against
  the source — every file, line and scope it cites — before it reports it, and drops one whose
  trace does not hold.

A finding in lines the running task wrote is fixed in that task's change. Any other finding is
returned to the caller, who applies `change-scope`'s **Scope Follows The Defect, Not The
Request** to place the fix. No findings file is
committed, and the review changes no code.

Give each finding a stable id (`F1`, `F2`, …) and each hardening note its own (`H1`, `H2`, …) when
the result is first presented, and refer to it by that id everywhere afterwards — in chat, in a
plan, in a commit. A title or a position in a list changes; an id does not.

## Output

```markdown
**Security audit:** <scope> — <n> finding(s), <in process | <h> hunters, <r> refuters>

- **Findings:** <id [severity] file:line — attack in one sentence; impact; conditions; smallest
  remediation, with the materially simpler alternative beside it where one exists; or none>
- **Hardening notes:** <id — why it is not exploitable, or none>
- **Rejected by a precedent:** <count per precedent, or none>
- **Read:** <the changed lines and the paths traced from them; a clean result says no exploitable
  finding was seen in what was read, never that the code is safe>
```

Per-item detail past five items goes in a file in `.agent_sources/` at the root of the worktree the
review runs in, sent with the result.
