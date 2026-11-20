# Review rounds

**A change gets at most 3 review rounds in total: the first review and 2 re-reviews after
repairs.** Any change — source, tests, tooling, configuration, guidance or interface — that has
failed 3 rounds of review, gate, skill test, smoke test or CI, whatever each round raised, is not
repaired again: findings that keep coming on one change say the approach is wrong, not that the
next patch will land. The stop exists to end wasted rounds, never to add questions, and the task
stays active.

## Counting

- A change is one plan step, worker task or finding fix, and its rounds are counted together across
  every kind of check.
- Not counted: a round a broken runner, fixture or provider cut short before judging the change, a
  style flag, and a gap in a gate's evidence, as `acceptance-gate`'s **Bounds** defines them.
- The per-flag bounds of the skill running the loop still apply within those 3 rounds, and
  `review-proposal`'s attack rounds on a proposal keep their own count.

## Disposition At The Limit

- Put the disposition to `council` in **Ask** mode, with the change, each round's findings and
  remedies, and the three choices: use a simpler approach, revert the change, or accept it with the
  remaining findings recorded. Record its majority ruling and follow it. No council is convened
  over style alone.
- A confirmed defect, an exploitable vulnerability or a failing required check is never accepted
  this way.
- If the authorized outcome still needs work, update the active plan and start the replacement, a
  new change with its own rounds, at its first step **Priority** permits, under the existing
  authorization and without another plan approval. A different implementation idea is not a new
  approval boundary.
- Ask only when the replacement needs an unresolved product, scope, security, disclosure or
  authorization decision, and join that question to the questions already open rather than sending
  it separately.
- Report the decision in plain words, with current captures where the change is visible.
