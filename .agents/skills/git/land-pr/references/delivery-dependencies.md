# Delivery dependencies

Read the complete consumer head, not only changed lines. Inventory references that determine code
or artifacts it consumes: checkouts, actions and reusable workflows, dependency manifests and
lockfiles, build inputs, image tags or digests, package sources and generated artifacts. Follow
indirection through variables, scripts and provider configuration to the actual resolved input.
Include a prerequisite change whose behavior the consumer assumes even without a direct source
reference. A test-only fixture that cannot enter the consumer's delivery is not a delivery input;
a testing revision used to build, validate or package that delivery is.

For each input, retain its consuming location, provider, configured reference, resolved immutable
revision and evidence for its delivery state. Resolve the provider's actual default branch and
current release metadata from the provider, rather than assuming a branch name or trusting a PR
description. A maintained default branch or published release is eligible only when it includes
the behavior the consumer needs and contains no outstanding prerequisite change.

A pull-request ref, testing branch or artifact built from an unmerged revision remains a draft
dependency. Replacing its branch name with a commit, image digest or package version does not
change that state. Establish ancestry against the freshly fetched provider default branch for
resolved commits (`git merge-base --is-ancestor <revision> <provider-default>`), or equivalent
provider evidence. A squash merge may not preserve the tested commit's ancestry: read the actual
merge result and move the consumer onto the maintained reference containing it. For images and
packages, read build or release provenance linking the artifact to its source revision; a published
label alone cannot establish that a testing artifact is deliverable. Missing access or provenance
is an unresolved dependency, never a clean inventory.

While the consumer is draft, its body names each unresolved provider change with a direct PR link
when one exists, the consumed reference and resolved revision, its effect on delivery, and the
required transition. Retain the resolved revision and validation evidence when that transition
finishes, and remove obsolete blocker wording. This is dependency disclosure within the consumer's
own contract; unrelated cross-repository coordination stays in chat.

The maintained target follows the user's explicit reference choice, then applicable repository
guidance: a default branch, published release tag, or another permitted maintained reference.
Recorded commits establish provenance; they do not override the standing version-reference policy.
An explicitly permitted immutable reference still needs merged or released provenance. A dependency
merge does not authorize a release or make the consumer's old testing reference suitable for
delivery. Verify all consuming locations have moved and validate what they now resolve before
readiness; recheck mutable targets before merging.
