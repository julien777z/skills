---
name: modernize-pr
description: 'Bring an old pull request up to date with its base, or decide it should not be. Use when asked to modernize, rebase or refresh an aging pull request, to bring a stale pull request back to life, or to judge whether one still belongs in the product. Judges the idea against the current base before touching the branch.'
license: MIT
metadata:
  source: https://github.com/t3dotgg/tstack/tree/main/skills/modernize
---

# Modernize PR

Modernize the idea, not just the branch. A clean rebase does not prove that the pull request still
belongs in the product, and Git reporting no conflicts does not make it current.

## Dependencies
- `session-ledger`
- `merge-conflict`
- `pre-production`

## Scope

The invocation names the pull requests: one, or a set that implements one change across
repositories, such as an API change and its client. A set is judged as one change, with one
disposition, since landing one half without the other leaves each repository wrong.

The invocation authorizes reading each pull request and, for a `MODERNIZE` disposition, bringing
its branch up to date and pushing it. That is the user's direction to continue those pull requests,
whoever opened them. Merging, closing, changing the base branch and widening the change stay with
the user, as the global rules and the GitHub rules say.

Record each pull request with `session-ledger` before reading it, as a `reference`, and as
`touched` once this run pushes to it.

## Establish The Intent

1. Read each pull request at the host: its state, base, head repository and branch, head commit,
   author, checks and review state, then its title, description, linked issues, commits, review
   threads and complete diff.
2. State the smallest coherent goal the change was trying to reach, before judging how it was
   built.
3. Fetch the latest remote base and pull-request head, using the pull request's actual base
   branch. Record the merge base, so the original change and what the base did since can be read
   apart.

## Check What Changed Around It

Read the commits and diffs the base gained since the merge base. Search merged and open pull
requests in the same repository when titles, code paths or behavior suggest a replacement or a
competing implementation, and for a set, in each repository it spans.

Look past overlapping lines:

- Has the same user-facing problem already been solved?
- Did the APIs, types, schemas, dependencies or boundaries it relies on change?
- Do both sides now claim the same behavior or invariant?
- Was the code it changes deleted, moved or deliberately simplified?
- Would landing it restore an old behavior or contract, or make two ways to do one thing?
  `pre-production` decides what a current change may keep of an obsolete owned contract.
- Is what it delivers still worth what it costs to maintain?

Age alone is not evidence, and the effort already spent is not a reason to keep it.

## Choose A Disposition

Choose one before pushing anything:

- **`MODERNIZE`**: the goal is still wanted and the implementation is still the right shape. Bring
  the branch up to date as **Bring It Up To Date** says.
- **`REWORK`**: the goal is still wanted, but bringing the branch up to date would keep the wrong
  implementation. Describe the smallest credible rewrite against the current base: what it keeps
  from the pull request, what it drops, and what the base already provides. Push nothing unless the
  invocation also asked for the rework.
- **`CLOSE`**: the change is superseded, obsolete, pointed the wrong way, or no longer worth its
  cost. Cite the concrete evidence: the merged pull request or base commit that replaced it, the
  code that no longer exists. Push nothing.

A pull request is closed only on the user's word. A `REWORK` or `CLOSE` that waits on the user goes
to them as a question, as the global rules' question-tool bullet says, with the evidence and the
disposition as its recommendation.

## Bring It Up To Date

For a `MODERNIZE` disposition:

1. Work in a disposable worktree at the recorded pull-request head, leaving every existing
   checkout as it is.
2. Bring in the freshly fetched base through `merge-conflict`, resolving each collision by the
   change's goal and the base's newer invariants. A collision that shows a product or architecture
   disagreement reopens the disposition rather than being guessed through.
3. Compare the series before and after with `git range-diff`, and read the final diff against the
   base: no intended behavior is gone, and nothing the base already has is brought back.
4. Run the checks the GitHub rules' **Pre-Push Gate** requires for the touched area. Tell a real
   failure from one the base already has or one the environment caused, with its evidence.
5. Push with `--force-with-lease` pinned to the remote head recorded before the update. When the
   lease fails, fetch and judge again rather than overwrite someone's new work.

## Output

Return this report, one block per pull request set, keeping every heading and writing `None`
under one with nothing to list:

```markdown
**<MODERNIZE | REWORK | CLOSE>**: <one sentence on why>

Pull requests

- <[repository#number](url)>: <state, head before, head after when pushed>

What the base changed

- <each change on the base that bears on this one, linked>

Conceptual conflicts

- <each, or `None found`>

Update

- <range-diff result and push, or `Not pushed: <disposition>`>

Checks

- <each check run and its result on the head named>

Rewrite plan

- <for `REWORK`: what it keeps, drops and builds on; otherwise `None`>

Not verified

- <what could not be checked, or `None`>
```

Keep observed facts and judgment apart: a fact names where it was read, and a judgment says it is
one.

## Guardrails

- Never merge, retarget or comment on a pull request this skill handles, or close one without the
  user's word; the GitHub rules' **Comments** section governs any post.
- Never force-push without the lease pinned to the recorded head.
- Never rebase an obsolete branch: a `CLOSE` stops before any update.
