---
name: code-simplify
description: Review a change for duplicated mechanisms, needless abstractions and maintainability, then fix what it admits. Use when the user asks to simplify or clean up a change, or when another skill's workflow runs it as one of its steps.
short_description: 'Review a change for duplication and needless abstraction, then fix what it finds.'
---

# Code Simplify

Find what the change should not have added — a second copy of something the repository already
owns, an abstraction nothing needs, a forwarding layer, a new suppression — and fix it. The
criteria and the severity scale are in the skill's rubric reference, `references/rubric.md`; read
it whole before the pass.

## Dependencies
- `list-prs`
- `pre-production`
- `subagent-matrix`
- `test-fixture`

## 1. Scope

1. Take the scope the caller names. Otherwise use `git diff $(git merge-base <base> HEAD)` plus the
   untracked files the branch adds, where `<base>` is the repository's remote default branch.
2. Write the change's intent in one or two sentences, from the user's request or the caller's
   brief. Nothing the intent asks for is a candidate for removal.
3. Read the full contents of every touched file and the sibling modules in their packages: the
   siblings show where the logic should have lived and what it duplicates.
4. Invoke `list-prs` for the ongoing task when the change shares a mechanism or contract with other
   repositories, and read those pull requests' heads for the affected-repository map. Reuse a
   caller's lookup while its heads are current.
5. When the scope includes tests, fixtures or test support, invoke `test-fixture` first and apply
   its criteria to those files.

## 2. Review

- **Small scopes in process.** When one reviewer can hold the diff, the touched files and their
  siblings at once, review in process and start no subagents.
- **Larger scopes by slice.** Partition by app, service or package into at most five slices,
  grouping neighboring areas when there are more, and launch one read-only `code-simplify` agent
  per slice through `subagent-matrix` at its advanced capability level, each with the rubric, its
  slice's diff and file contents, the intent and the affected-repository map. Add one cross-cutting
  reviewer, within those five, only when parallel implementations across slices will not fit in one
  slice's context. Apply `subagent-matrix`'s launch fallback when a worker cannot start.
- **Subagents review; the parent applies.** Each returns findings anchored to path and line with
  severity and remedy, and edits nothing. The parent drops duplicates and findings another subsumes,
  and checks each remaining finding against the code before acting on it.
- Run the rubric's five greps first, then its standards, then trace changed flows.

## 3. Fix

- Apply every `blocker` and `should` inside the change directly to the working tree, completely,
  including the consumers it must update; contract changes follow `pre-production`'s target-contract
  decision.
- Fix a `nit` only when it is a one-line change in a line the change already touches; otherwise
  list it as declined.
- Outside the change, fix every bug, whatever its size. Non-bug cleanup outside the change
  follows `pre-production`'s size budget; return what is past it to the caller to record as deferred
  work.
- Check each remedy against the language and layout rules for its file before applying it.
- After fixing, rescan only when the fixes added, moved, merged or deleted a module or changed an
  interface other code reads: a fresh reviewer gets the earlier findings, the fix diff and the files
  it touches. Fixes applied in place need no rescan.
- If the pass grew the diff past what the intent needs, cut first.

## Output

```markdown
**Code simplify:** <scope> — <n> finding(s), <clean | fixed | open findings remain>

- **Greps:** <hits per grep, or "no hits for any of the five greps">
- **Fixed:** <id [severity] file:line — one clause each, or none>
- **Declined:** <id [nit] — reason each, or none>
- **Outside the change:** <fixed id | returned id: what the caller records, or none>
- **Affected repositories:** <repo: disposition each, or "current repository only — <search>">
- **Diff:** <shortstat before> → <shortstat after>
```

Per-item detail past five items goes in a file sent with the report.
