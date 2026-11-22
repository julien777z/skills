# Multi-repository delivery

What `SKILL.md`'s **Multi-Repository Delivery** applies when one change spans repositories, and
how a branch consumes a dependency that is still in review.

## Delivery Artifacts

- Write every branch name, commit message, pull-request title, pull-request description, review
  comment, code comment, and repository-local report solely from that repository's perspective.
- Apply the GitHub rule's independent publishing context to those artifacts, including dependency
  and hand-off notes; foreign references and coordination belong in user chat.
- Keep cross-repository coordination and combined status reporting in user chat.

## Dependencies In Review

A dependency still in review in another repository, an unreleased package version, a sibling pull
request not yet merged, or CI expected to stay red until one of those lands holds no push, check or
walkthrough and becomes no question about pushing or merging, as the GitHub rule's **Pre-Push
Gate** says.

- The branch consumes the dependency's pull-request branch, or its default branch once merged, in
  the manifest, the lockfile and any workflow checkout, a maintained branch being a reference
  `pre-production`'s **Versions** permits while developing, or builds on a same-repository
  sibling's branch, and pushes.
- Every build, test and walkthrough runs against that checked-in reference, never a local copy the
  manifest does not name.
- A consumer that cannot build until its dependency merges is a manifest still naming the default
  branch: point it at the pull-request branch, never ask for the dependency's merge or report the
  consumer blocked on it.
- Which branch it consumes, and a red check that dependency explains, are surfaced in user chat as
  **Delivery Artifacts** says rather than waited on; adopting the dependency's maintained delivery
  target is named work for when it merges.

## Each Repository Speaks Only Its Own Vocabulary

What goes inside a change keeps to its own repository's words in every repository the run
touches, as `pre-production`'s **Whose Standards Apply** and **Naming And Language** say.

Where this run touched more than one repository, sweep for borrowed words before delivering:
search each repository for the distinctive nouns of the others it was worked on beside, and read
what comes back. A borrowed name is invisible to the author precisely because it was familiar.
