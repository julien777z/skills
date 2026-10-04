# Merged targets

Verify the delegated repository, original pull-request URL, actual merge commit, and its first
parent. Bind `first-parent..merge-commit` as the immutable review target. Read the original pull
request's description and discussions as evidence; never refresh its description, reopen it,
amend its merge, or substitute the current branch for this range.

Initially there is no working pull request. Inspect and validate findings against the complete
delivered range and its repository context. Read existing source-check and deployment evidence;
do not create an empty branch or pull request just to rerun validation on unchanged delivered code.
Simplification, thread triage, and review may each discover the first confirmed finding.

Once a finding requires a correction, fetch the default branch and create the fix branch there.
Implement the correction, run its required source checks, push, and create the new draft fix pull
request through REST. Record its canonical URL in the session ledger. Bind that URL as the working
pull request while retaining the immutable range as the original review target. Consolidate the
same repository's confirmed findings into the appropriate working fix pull request.

Pass both the complete original range and complete fix diff to reviewers and validators, with each
remedy increment identified. Description refresh, tests for the changed behavior, final acceptance,
and exact-head merge gating operate on the fix pull request. The original merge remains unchanged.
A clean range with no correction has no working pull request and no merge step.
