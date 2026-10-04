# Open targets

Resolve the requested open pull request under CR's **Pull Request Ownership**. When no pull request
exists, use `code-review`'s branch and commit setup rules, create it through REST with `draft=true`,
and record the returned canonical URL in the session ledger. An existing draft is reviewable.

Bind its URL as the review target and the working pull request. Record its merge-base and exact head;
every confirmed finding remains on that working branch through the shared workflow's gates.
