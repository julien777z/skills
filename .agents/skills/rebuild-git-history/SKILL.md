---
name: rebuild-git-history
description: "Rewrite a branch you own into one commit per material change, or drop one change from it, without losing content: the old head stays under a backup ref, the result is proven against it before anything moves, and the push is leased. Invoke as /rebuild-git-history or $rebuild-git-history, or from a skill that needs a branch's commits to correspond to its changes."
---

# Rebuild Git History

A branch whose commits each carry one material change can be read, linked, reviewed, and reverted
one change at a time. This skill produces that branch from one whose commits mix changes, or
removes one change from it, and it proves at every step that nothing else changed.

## Preconditions

Stop and say so when any of these fails; none is worked around.

- **The branch is yours**: you created it, or its author handed it over. A branch somebody else is
  working is never rewritten, and a commit already on the default branch is never touched.
- **The working tree is clean.** Commit or stash everything first; the rebuild reads only committed
  content, and anything uncommitted would be read as part of no change.
- **The remote default branch is freshly fetched**, and the branch's merge base with it is known:
  `git merge-base origin/<default> HEAD`. Every step below builds on that merge base and nothing
  newer, so the rebuild never incorporates the base by accident.

## Workflow

1. **Keep the old head.** `git update-ref refs/backups/<branch>/<utc timestamp> HEAD` and note
   the SHA as the old head. Everything below can be abandoned by checking that SHA out again.
2. **Choose the range to regroup.** Read `git log --oneline <merge base>..HEAD`. The range runs from
   the merge base to the last commit that mixes changes; call that commit the range end. Commits
   after it that each already carry one change are kept as they are and cherry-picked in step 6.
   `git diff --name-status <merge base> <range end>` is the complete list of paths to regroup;
   where the branch contains a merge from the default branch, the merge base already sits after
   it, so the list holds only the branch's work.
3. **Group the paths by material change.** One group per change a reviewer would name: a contract
   broken on purpose, a mechanism replaced, a behaviour added, a shared owner introduced. Tests go
   with the change they cover. Check that every path from step 2 lands in exactly one group before
   committing anything.
   - **A file that serves two changes is split by hunk, not assigned whole.** Read that file's diff
     and put each hunk with the change it belongs to; when the group is committed, take only its
     hunks out of the range end with `git checkout --patch <range end> -- <path>`, answering yes to
     those hunks and no to the rest. A whole-file assignment silently carries the other change's
     lines under the wrong commit, and nothing later detects it. Only where the hunks cannot be
     separated does the file go whole, with the group that owns most of it, and the report names
     that file as kept whole.
   - **Read each group's diff once it is assigned** and look for a hunk that names another
     group's subject — a stub, a fixture, a config setting for a change filed elsewhere. Move it
     before building.
4. **Drop a change, when that is the purpose.** A change the user no longer wants is a group that is
   built as nothing: its paths revert to the merge base, and any path it shares with a kept change
   keeps only the kept change's hunks. Name the dropped group in the report, and expect the tree
   check in step 7 to show exactly its hunks removed and nothing else.
5. **Build the new history on the merge base.** Start a scratch branch there with
   `git checkout -b <scratch> <merge base>`; never an orphan branch, and never a reset onto the
   default branch. Then, for each group in order: `git checkout <range end> -- <paths>` for the
   group's surviving whole paths, `git checkout --patch <range end> -- <path>` for each split
   file, `git rm` the paths the range end deletes, and commit with a message naming that one
   change. The tree is dirty between taking a group's content and committing it; that is the one
   dirty state the rebuild allows, and every group's commit leaves it clean again.
6. **Cherry-pick the kept commits.** `git cherry-pick <each commit after the range end, in order>`,
   unchanged. A kept commit that touches a path a dropped change removed conflicts as a
   modify/delete; resolve by removing the path and continuing, never by restoring it.
7. **Prove the tree.** For a regroup, `git diff <old head> <scratch branch>` reads empty. For a
   drop, read that same diff hunk by hunk: every hunk in it removes lines the dropped change added
   or restores lines it removed, and nothing else appears. A file the dropped change shared with a
   kept change therefore shows only the dropped hunks gone, with the kept hunks still in place; a
   shared file that reverts wholly to the merge base is the kept change lost, and a per-path
   listing (`--name-status`) cannot tell the two apart, so it is never the proof. In both cases
   `git diff --name-only origin/<default>...<scratch branch>` names no path the branch never
   touched. Any failure means a group was wrong: fix the grouping and rebuild from step 5; never
   push.
8. **Move the branch and push with lease.** `git branch -f <branch> <scratch branch>`, then
   `git push --force-with-lease=<branch>:<old head> origin <branch>`. The lease refuses the push if
   anything landed on the remote branch since the old head was read, which is the one case where a
   rewrite could lose work.
9. **Keep the backup until the branch merges.** Delete `refs/backups/<branch>/*` only after the
   pull request is merged or closed; until then it is the way back.

## Fixing up one commit afterwards

A hunk that belongs in an existing commit — an import the docs commit needed, a fixture the feature
commit forgot — is a rewrite of the same branch, and it takes the same guardrails as a rebuild.
Commit the hunk with `git commit --fixup=<that commit>`, then:

1. Keep the old head as step 1 does: a fresh `refs/backups/<branch>/<utc timestamp>` at the fixup
   commit, and its SHA as the old head.
2. `GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash <merge base>`. The rebase target is the
   merge base the branch sits on, never the default branch: onto the default branch, the same
   command also replays the branch onto every commit the base gained since, which is a base
   incorporation nobody reviewed. A conflict while replaying is resolved to the content the fixup
   commit carried, never by dropping either side.
3. Prove the tree as step 7 does: `git diff <old head> HEAD` reads empty, because an autosquash
   moves content between commits and changes nothing about the result;
   `git diff --name-only origin/<default>...HEAD` names no path the branch never touched; and
   `git merge-base origin/<default> HEAD` is unchanged. Any failure means the rebase went wrong:
   `git reset --hard <old head>` and start again; never push.
4. Push with the lease as step 8 does, against the head the remote held before the fixup.

## Report

One line per rebuild in the caller's report: `Rebuilt <branch>: <n> commits, tree identical to
<old head> | dropped <change> (<paths>), backup <ref>, pushed with lease[, <path> kept whole].`
A fixup reports the same line with `Fixed up <commit> on <branch>` in place of the first clause.

## Guardrails

- Never a soft reset onto a newer base followed by one commit: it records the old merge base's copy
  of every untouched file and silently reverts the base's work. The scratch branch starts at the
  merge base the branch already sits on.
- Never a rewrite of a branch that is not yours, of any commit already on the default branch, or of
  a range that contains a merge you did not perform.
- Never a push without the lease, a push after step 7 failed, or a backup deleted before the
  merge.
- Never begin a rebuild or a fixup on a dirty working tree, and never run one while a test run reads
  the tree. The only dirty state inside a rebuild is a group's content taken and not yet committed.
- Never a rewrite of the branch — rebuild or fixup — that skips the backup ref, the tree proof, or
  the lease. The three are one mechanism, and a route through the skill that drops one of them is a
  route that can lose content.
