# Merge And Read-Back

The last three delivery steps, read from **Deliver the batch** in `SKILL.md` when the batch reaches the file-list check.

### Check the diff file list against the default branch, then merge

The authorization covers
a pull request carrying only `.agents` files, and the file outside them that slips in is never
announced. Read the changed paths, never your memory of what you edited. A path outside
`.agents` leaves this branch — dropped when it was never meant, moved to the source pull
request the work continues under **Branch and commit** when it was — and the new head goes back through **Brief `review-pass`'s final acceptance**. Everything
in `.agents`, merge it, as the entry point's step says, with the head the gate accepted, which for a pull request in `review-pass`'s **Combined Review** set, and no other, is also the head that review accepted — but first
ask whether any line it adds or drops is true only once a still-open source pull request
merges. Select where dependent guidance goes under the GitHub rule's **Branches and Pull Requests**
and the [guidance pull requests reference](guidance-pull-requests.md),
and report any hold under its **Merge Authorization**. Otherwise a pull request carrying a
skill change merges once **Hold each changed output to its concrete example** found every changed output matching its concrete example, and
one carrying only rules has no example to match and merges once **Run `validate_sources.py check`** through **Run one `test-skill` round** pass, unless their **Merge
Authorization** holds it. Report a held pull request for the user's review.

### Nothing is copied by hand

The skills repository is the only copy of a shared skill;
sessions receive a merged edit through the refresh `merge-gate`'s **After Agent Sync** requires, never through a copy
placed in another repository or install. A skill that reads generically but was written into one repository's `.agents` is
moved to the skills repository in the same change rather than left as a second copy.

### Read the merged text back before using it

A merge changes the default branch, not the
checkout: a session working on another branch still carries the old skill in its tree, and a
skill invoked from there runs the text the change just replaced. After the merge, fetch the
default branch and read every skill or rule the change touched from it — `git show
origin/<default>:<the skill's SKILL.md path there>`, and the references beside it — and run
from that text for the rest of the session. A skill invoked while its change is still open
is read the same way from the branch that carries it, never from a checkout that predates
it.
`merge-gate` then waits for the default-branch Agent Sync run; its **After Agent Sync**
requires the installed copy to be refreshed before reporting completion.
Once the run finishes, inspect every generated artifact on the default branch that represents
the changed source, including `AGENTS.md` when the source feeds root instructions and
provider trees such as `.cursor/`, `.claude/`, and `.codex/` when they represent the changed
package. Diagnose stale or missing output through Agent Sync; never repair it by editing
generated files.
