# Combined review

The mechanics of **Combined Review** in this skill's `SKILL.md`, which keeps the set and timing.

Contents: **Reviewer**, **What it looks for**, **Findings**, **A later round**, **Verdict**.

Pull requests reviewed one at a time can each be right and still be wrong together. One reviewer
reads the whole set for flaws only the combination has; it does not repeat each pull request's own
review.

## Reviewer

One per round, however many pull requests the set holds, resolved and launched as this skill's
**Review Loop** **Reviewer** bullet says, read-only and starting no subagents. Send the **Combined
review** form of [the reviewer brief](reviewer-brief.md) with each pull request's checkout, base,
accepted head, intent statement and description. The reviewer reads every complete merge-base diff
together; a stacked pull request's diff is its own patch against the branch it builds on.

## What it looks for

The flaws of the combination the **Combined review** form of the reviewer brief lists.

## Findings

Check each against the code as this skill's **Answer each finding** says. A confirmed finding goes
to the pull request that owns the fix, or to both when both must change. It is repaired there and
reviewed as that pull request's new delta under this skill's **Workflow**, and it counts within that
change's review-round limit `acceptance-gate`'s **Bounds** sets. A finding that spans repositories
is reported in user chat; each fix's commits, description and threads speak only of their own
repository, under the GitHub rule's independent publishing context.

## A later round

Runs only when a later change moves a head the round read: the reviewer reads what changed, with the
other heads as context and a pull request merged since at its merged commit. A rewrite whose tree is
identical keeps the verdict.

## Verdict

One per head. With `session-ledger`, add to each head's `review` entry the heads it was read with and
`accepted` or the findings still open. A head this round has not accepted is returned as held and is
not a head to merge.
