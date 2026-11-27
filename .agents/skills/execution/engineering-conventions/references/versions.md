# Versions

What `SKILL.md` applies when a change chooses a runtime, base image, dependency release, hold or pin,
or a reference to external code.

- Reference external code and automation by a maintained version tag when available, or by a
  maintained branch while developing or when no release tag exists. Do not pin dependency manifests,
  shared checkouts, or workflow references to commit hashes. Lockfiles and release records may retain
  the exact resolved commit for reproducibility and provenance.

- **Every project the owner runs or consumes runs the newest stable language runtime, base image
  and dependency releases it works with.** Which release is newest is read from its publisher's
  release list at the time, such as the runtime's official release page or the package registry, never from
  memory or from a version the user names, which is checked the same way. A change made for that move — one the user asks for, or
  the upgrade pull request a warning leads to, as `scope-of-change`'s **Scope Follows The Defect, Not
  The Request** places it — moves what the project actually runs onto them: its version file,
  container images, CI and lockfile, with whatever code changes the new releases need, including in
  an owned package that only widened its range to let a consumer move. Neither of these is that
  move: a CI leg kept on the old release beside the new one, or a dependency held below its newest
  release. A change that touches a manifest or lockfile for another purpose, such as adding one
  dependency, takes that dependency's newest stable release and moves nothing else. Hold one back only
  where an install or test shows the newer release failing on the project's runtime, such as
  a dependency the owner does not control pinning it, and name that failure in a comment beside
  the constraint; a pin in a package the owner controls is widened in that package as part of the
  move, its release left to the owner; a
  migration the newer release needs is part of the move, not a reason to hold. Widening a
  supported range to admit a newer release is fine, since an owned project's range serves the
  owner's own projects. Raise its minimum once keeping the lower release no longer makes sense,
  such as when the formatter or the code would stay on the older release's syntax. A library
  published for consumers outside the owner's projects keeps the range its language rule sets.
