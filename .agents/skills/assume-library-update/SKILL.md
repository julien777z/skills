---
name: assume-library-update
description: Write consuming code against a library change that is authored but not yet reachable, when the library is the user's own and this session cannot push to it. Invoke as /assume-library-update when work in a consuming repository is blocked waiting on a dependency update that is written, opened, merged, or published but not yet reachable.
disable-model-invocation: true
---

# Assume Library Update

A dependency the user owns needs a change before the consuming repository can be finished, and this
session cannot deliver it — the push was refused for lack of access, or the repository could not be
attached at all. Waiting is the wrong answer: the consuming work is the part this session can do, and
leaving it undone strands the design in a chat log.

Write the consuming code **as though the library change already exists**.

## When this applies

All three hold, or it does not apply:

- The change belongs to a library **the user owns**, so it will land because they say so. Establish
  that from the repository itself — who it belongs to, whether the session reports push access — never
  from a name written into this file.
- This session is **blocked from delivering it**: a refused push, an authorization boundary, a
  repository that cannot be attached.
- The consuming change is **fully specified**. You know the signatures, because you wrote them or read
  them. Assuming an interface nobody has designed is guessing, not unblocking.

Where the library is a third party's, none of this applies. Pin or work around it instead.

## Writing the consuming change

- Call the new interface directly, with no shim, no `getattr` probe, no try/except around the import,
  and no branch that works both before and after. A compatibility layer for a version that will never
  ship in the wild is exactly the legacy handling the replacement-contract rules ban.
- Say in the pull request body which library, which change, and where that change currently lives, so
  a reader who hits the failure knows it is expected rather than broken.
- Leave the dependency constraint alone **only while the change is unreachable** — editing it before
  then points the build at something that does not exist yet. The moment the change exists anywhere
  fetchable, including an open pull request, this stops applying and **When the user says the library
  change exists** below governs instead. Staying in this mode past that point is the failure it is
  easiest to miss: the code is written, the dependency still names the published version, and every
  check quietly exercises the library the change was meant to replace.

## Tests and checks will fail, and that is the expected state

- **Do not run the suite to confirm it fails.** The failure is the known consequence of an unreleased
  dependency, and reproducing it locally spends minutes on an answer already in hand.
- **Do not treat the resulting red CI as a failure to drive to green.** No push, re-run, or fix reaches
  it, so there is nothing to do about it but say what it is.
- **Say that in the pull request body, and to the user.** The body is the change's own description,
  so a reviewer meeting the red check finds the reason where they are already reading. Why it does
  not go on the pull request as a comment is the comment rules' answer, not this skill's.
- Never weaken a test, a check, or a version constraint to manufacture green. The red run is a truthful
  record that the dependency is not there yet.
- This suspends the completion bar for **this** change only, and only for failures the missing update
  causes. A failure the consuming change itself introduces is still yours, and still gets fixed.
- **What is suspended is running the suite, never writing the change or its tests.** Those are two
  different things, and treating the first as licence for the second is how a mode meant to unblock
  work becomes a reason to leave it undone.
- **"I cannot verify it" is therefore never grounds to skip, narrow, or defer any part of the
  consuming change**, however delicate the part is. The reason will read exactly as well to the pass
  that could have run it, and by then nobody remembers the piece was left out. Difficulty is a reason
  to read the surrounding code harder and write the test more carefully; it is never a reason to hand
  the work on.
- Write the tests that would prove each piece, in the same change. They fail alongside everything else
  until the dependency lands, and then they are what verifies the work rather than an assertion about
  it — which is precisely what a delicate change needs and a claim in a pull request body is not.
- **Never report the consuming change as verified.** It is written and unverified until the dependency
  is reachable and the suite has run — say so in those words, since a red run nobody explains reads as
  a change that failed rather than one still waiting.

## When the user says the library change exists

They will say it is written, opened, merged, or published. Do not take the word for the state — read
the library repository and act on what is actually there, in this order:

1. **An open pull request carrying the change.** Point the dependency at that pull request's ref so the
   consuming repository can build and test against it now. Keep the package named in the project
   dependency table and give the source in the tool-specific table beside it — a package that appears
   only in the source table is not installed at all.
2. **No pull request, but the default branch already carries it.** The change merged. Point at the
   released version if one exists, and at the default branch if the release has not been cut.
3. **A pull request that has since been published.** Replace the ref with the released version
   constraint.

**Update every consumer, not the first one found**, and find them by **import** rather than by
declaration. A project that imports the package without declaring it is a consumer too — it has been
relying on the dependency arriving transitively, which a direct import should never do. Declare it
there as well, because a source override reaches only the projects that name the package themselves.

**A source given in the tool-specific table does not travel through a path dependency.** A monorepo
resolves each project against its own manifest, so pointing the one package that declares the
dependency at a ref leaves every other project resolving the published version, and the consuming
code then runs against the library it was written to replace. Each project carries its own source
entry beside its own declaration.

**Regenerate the lock beside every manifest, and commit both.** A changed manifest whose lock still
describes the old resolution fails installation outright — every job that installs that project
dies before it runs a line of the change, which reads as a broken branch rather than a missing
relock. Check every lock in the repository afterwards, not only the ones just edited: making one
project's dependencies explicit can turn a name it always had into a requirement its consumers must
now resolve.

Commit the manifests and locks **with the consuming change**. They are what lets any check reach the
library, so a branch carrying the code without them proves nothing that a green run would have
proven.

Then run the suite. This is the point where the completion bar returns, and it is carrying everything
the earlier pass skipped, so expect it to find work.

Replacing the ref with the released constraint is part of the same work, not a later tidy-up. Until
that happens the repository builds from a branch that can move or disappear, so do it the moment the
release exists.
