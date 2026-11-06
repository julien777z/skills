---
name: merge-conflict
description: Incorporate the base branch into a branch — a merge, a rebase, a pull, a branch update, or a conflict Git or the hosting service reports — by comparing what each side did and keeping the better answer, with the resolved result put to `acceptance-gate`'s base-incorporation question. Use whenever the base is brought into a branch, whether or not Git reports a conflict, whenever a pull request is un-mergeable, when a finished change's base has moved before its final acceptance, or when an already applied local overlay input needs conflict resolution.
short_description: 'Bring the base branch into a work branch, resolve conflicts, and validate the result.'
---

# Merge Conflict

Bringing the base into a source branch is a change of its own, and it is reviewed as one. A local
overlay comparison resolves an already applied input without changing its source. Git decides
nothing here: a hunk that merges cleanly and a hunk it marks conflicting are both places where two
answers to one question may now sit in one tree.

## Dependencies
- `acceptance-gate`
- `pre-production`

## Neither Side Is Authoritative

- **The branch is not privileged because it is yours, and the base is not privileged because it
  landed first.** Arrival order is evidence about nothing, in either direction. "Incoming code takes
  a shape my change removes" and "the base already merged this" are available in every collision and
  each always points the same way, so on their own they decide nothing.
- **Never resolve by side.** `ours`, `theirs`, a checkout of one side's file, or accepting every
  hunk from one branch resolves nothing; each is a decision made without reading what the other side
  did. Every conflicting file is read on both sides before any of it is written.
- **A rule that favours your own side is not the judgement.** Once the comparison below has named a
  winner, code that takes the losing shape is refactored onto the winner in the same change, and
  which branch it came from is never a reason to leave it there.

## Procedure

Select the target from the actual work: a source branch incorporates its current base; a local
overlay has an input already selected, fetched and applied by its caller. For a local overlay,
the caller supplies the overlay as built so far, the input and its comparison base. Preserve the
source checkout, remote branches and unrelated edits throughout.

1. For a source branch, record the previous merge-base and the base being incorporated; fetch the
   exact current base and head with explicit refspecs and confirm them against the hosting service.
   Merge the base into the branch, or rebase onto it where repository convention and branch
   ownership allow; never rewrite history on a branch somebody else is working. For a local overlay,
   use the supplied applied input and comparison base without fetching, merging or rebasing its source.
2. **Read the whole incorporation, not the conflict markers.** Diff the previous base to the
   incorporated base, and read that diff against the branch's own diff. For an overlay, compare the
   input's diff from its supplied base against the overlay as built so far. Every place both touched
   the same question is a collision, whether Git marked it or merged it silently.
3. **Compare each collision on what the two designs do in this tree.** Apply `pre-production`'s
   target-contract policy to each candidate; a legacy path does not survive because it preserves
   previous behavior. Before touching either, name which answer is better and why: which leaves fewer
   mechanisms for one concern, which removes duplication the other invites, and which failure modes
   each has produced. A design already duplicated in its own tree is evidence. Record the reason for
   the outcome: keep the target's shape and move incoming call sites onto it; take the incoming shape
   and move the target's call sites; or deliberately combine what each lacks in one mechanism.
4. **A tie has not finished.** There is no coin-flip default and no presumption for either side:
   apply `pre-production`'s test and take whichever yields the cleaner result and leaves the fewest
   mechanisms behind. Where that still does not separate them, the two are one design under two
   names, and the answer is the spelling the rest of the repository already reads.
5. **Preserve behaviour required by the target contract.** Migrate affected consumers and retained
   data before removing an obsolete shape. A resolution that drops required behaviour is a defect;
   preserving a legacy runtime path is not a way to avoid the migration. Where a close choice changes
   an interface others build on, put it to the user with a recommendation, as `pre-production`'s
   **Trade-Offs Are Surfaced, Never Enforced** directs; block only when a safe resolution needs an
   unauthorized product decision or a change to a contract a consumer outside the user's control speaks.
6. Remove every conflict marker and run `git diff --check`. Read the changed-file list against the
   target before proceeding. For a local overlay, preserve paths unrelated to the input and inspect
   their siblings. For a source branch, compare against the base and restore paths the branch never
   edited that now undo the base's work; inspect their siblings.
7. For a local overlay, return the resolved tree and decisions to the caller for its own commit and
   verification. Do not generate mirrors, publish, or run source pull-request gates for this local
   comparison.
8. For a source branch, regenerate lockfiles, generated contracts and provider mirrors from the
   resolved sources with the repository's tooling, never by hand. Run `git diff --check` and the
   GitHub rule's **Pre-Push Gate** checks, push the resolved result, then re-query mergeability.
   Run `acceptance-gate`'s **Base incorporation** procedure with the previous base, incorporated
   base, originating change and intent, and resolved result.

## Output

For a local overlay, return the resolved tree and collision decisions to the caller. For a source
branch, the delivery owes this report line:

```markdown
Base incorporated: <previous base>..<incorporated base> into <branch>; <n> collisions —
<n> branch shape kept, <n> base shape taken, <n> merged; gate: accepted | flagged and corrected.
```
