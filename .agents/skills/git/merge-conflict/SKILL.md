---
name: merge-conflict
description: Incorporate the base branch into a branch — a merge, a rebase, a pull, a branch update, or a conflict Git or the hosting service reports — by comparing what each side did and keeping the better answer, with the resolved result gated before it is pushed. Use whenever the base is brought into a branch, whether or not Git reports a conflict, and whenever a pull request is un-mergeable.
---

# Merge Conflict

Bringing the base into a branch is a change of its own, and it is reviewed as one. Git decides
nothing here: a hunk that merges cleanly and a hunk it marks conflicting are both places where two
answers to one question may now sit in one tree.

## Dependencies

- `acceptance-gate` — its **Base incorporation** procedure judges the resolved result before it is
  pushed.
- `pre-production` — the tie-breaker when two designs are equally good, in a repository that
  declares it; elsewhere the repository's project guidance stands in.

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

1. **Record the previous base** — the merge-base commit before incorporation — and the base commit
   being incorporated; both go to the gate at step 9.
2. **Fetch the exact current base and head** with explicit refspecs, and confirm the fetched objects
   are the hosting service's current head and base. Merge the base into the branch, or rebase onto it
   where the repository's convention and the branch's ownership allow; never rewrite history on a
   branch somebody else is working.
3. **Read the whole incorporation, not the conflict markers.** Diff the previous base to the
   incorporated base, and read that diff against the branch's own diff: every place both touched the
   same question is a collision, whether Git marked it or merged it silently.
4. **Compare each collision on what the two designs do in this tree.** For each one, name which
   side's answer is better and why before touching either: which leaves fewer mechanisms for one
   concern, which removes duplication the other invites, which failure modes each has already
   produced in code somebody wrote. A design already duplicated in its own tree is evidence about
   that design. Three outcomes are available, and the reason for the one taken is written down:
   - the branch's shape stands, and the incoming call sites move onto it;
   - the base's shape is better, so the branch's is dropped for it and the branch's call sites move;
   - each carries something the other lacks, so the result is refactored to take both parts
     deliberately — one mechanism carrying both behaviours, never both mechanisms side by side.
5. **A tie has not finished.** There is no coin-flip default and no presumption for either side:
   apply `pre-production`'s test and take whichever yields the cleaner result and leaves the fewest
   mechanisms behind. Where that still does not separate them, the two are one design under two
   names, and the answer is the spelling the rest of the repository already reads.
6. **Preserve behaviour on both sides.** The base's behaviour stays; the branch's authorized result
   stays; only their shapes are chosen between. A resolution that drops a behaviour either side
   introduced is a defect, not a resolution.
7. **Regenerate what is generated** — lockfiles, generated contracts, provider mirrors — from the
   resolved sources with the repository's own tooling, never by hand. Remove every conflict marker,
   run `git diff --check`, and run the repository's fast checks.
8. **Read the changed-file list against the base before anything else.** Every path in it is either
   one the branch touched or a regression: a path the branch never edited that now differs from the
   base is the base's own work being undone. Restore it from the base and look for its siblings.
9. **Gate it.** Run `acceptance-gate`'s **Base incorporation** procedure with the previous base, the
   incorporated base, the originating change with its intent, and the resolved result; that
   procedure states what a flag obliges and what its verdict does not grant.
10. **Push only after the verdict**, then re-query mergeability. Where the choice at step 4 is close
    and changes an interface others build on, put it to the user with a recommendation, as
    `pre-production`'s **Trade-Offs Are Surfaced, Never Enforced** directs, rather than settling it
    silently; block only when a safe resolution needs a product or contract decision nobody has
    authorized.

## Output

The report line the delivery owes:

```markdown
Base incorporated: <previous base>..<incorporated base> into <branch>; <n> collisions —
<n> branch shape kept, <n> base shape taken, <n> merged; gate: accepted | flagged and corrected.
```
