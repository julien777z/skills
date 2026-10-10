# Open targets

For an unqualified direct CR, resolve every current-repository ledger pull request that CR's **Pull
Request Ownership** retains. When the retained set is empty, use `code-review`'s branch and commit
setup rules, create one pull request through REST with `draft=true`, and record the returned
canonical URL in the session ledger. An existing draft is reviewable.

Bind every URL as its own review target and working pull request. Record each merge-base and exact
head; every confirmed finding remains on that target's working branch through the shared workflow's
gates.
