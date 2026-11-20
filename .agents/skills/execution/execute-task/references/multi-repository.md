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

The delivery rule above governs the artifacts around a change. This one governs what goes **inside**
it, and it binds in every repository the run touches whether or not that repository's own rules say
so — a repository with no independence rule of its own is the one most likely to be given another's
words.

**Never write another repository's nouns into this one.** Its product name, its services, its
skills, its tables and columns, its record types, its routes, its identifiers, the words its
business speaks: all of them stay where they are. That holds in source, tests, fixtures, sample
data, error messages, comments, and documentation alike, and it holds hardest in a library or a
tool, where every reader is a different consumer who has never heard of the repository the author
happened to come from.

**An example is where this fails, because an example needs a name and the author has one to hand.**
Documenting a folder layout, a config key, a path shape, or a call, the concrete thing the author
just saw is the nearest name and the worst one: it reads as this tool's own vocabulary to everyone
after them, and it goes stale the moment that other repository renames it. Invent the name instead.
An example naming a real artifact of another repository is the defect, however accurate it is.

Name things for the shape being demonstrated, never for whichever caller prompted the work. A
consumer's needs are a legitimate reason to build something and never a reason to name it after
them. Describe the target repository's own contract and behavior to reviewers; keep
consumer-specific coordination in user chat, as **Delivery Artifacts** above says.

Where this run touched more than one repository, sweep for it before delivering: search each
repository for the distinctive nouns of the others it was worked on beside, and read what comes
back. A borrowed name is invisible to the author precisely because it was familiar.
