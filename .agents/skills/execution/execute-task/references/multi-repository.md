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

A dependency still in review, unreleased or unmerged holds no push, check or walkthrough, as the
GitHub rule's **Pre-Push Gate** says. What the rule leaves to this reference:

- Every build, test and walkthrough runs against the checked-in reference the manifest names,
  never a local copy the manifest does not name.
- Which branch is consumed, and a red check the dependency explains, are surfaced in user chat as
  **Delivery Artifacts** says rather than waited on; adopting the dependency's maintained delivery
  target is named work for when it merges.

## Each Repository Speaks Only Its Own Vocabulary

What goes inside a change keeps to its own repository's words in every repository the run
touches, as `pre-production`'s **Whose Standards Apply** and **Naming And Language** say.

Where this run touched more than one repository, sweep for borrowed words before delivering:
search each repository for the distinctive nouns of the others it was worked on beside, and read
what comes back. A borrowed name is invisible to the author precisely because it was familiar.
