# Open targets

For an unqualified direct CR, use every open URL returned by `list-prs`. That list already reconciles
the task's verified records across repositories. When it is empty, use `code-review`'s branch and
commit setup rules, create one pull request through REST with `draft=true`, and record the returned
canonical URL through the task ledger. An existing draft is reviewable.

Bind every URL as its own review target and working pull request. Record each merge-base and exact
head; every confirmed finding remains on that target's working branch through the shared workflow's
gates.
