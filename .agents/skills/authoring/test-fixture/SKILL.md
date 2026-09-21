---
name: test-fixture
description: Must be used before creating, moving, renaming, editing, reviewing, or generating any test, fixture, factory, test data, test support, or test configuration in any language, and before executing tests after such a change. Enforces source-mirrored placement, canonical fixtures, concise parametrized cases, honest doubles, and regression-proof validation.
---

# Test Fixture

Build tests from the repository's canonical test surfaces, keep them beside the source concern they
exercise, and prove that new coverage detects the regression it claims to prevent.

## Dependencies

Read the repository's product-constraints skill when the skill listing declares one, found by its
description rather than assumed by name. It says how broad the fix for an issue encountered while
tracing a test surface is; without one, fix what the focused pass can finish.

## Workflow

1. Read the complete [rubric](references/rubric.md) before inspecting, reviewing, changing, or
   executing any covered test surface. Discover the repository's test roots, fixture packages,
   factory owner, shared test utilities, runner targets, and analogous sibling tests.
2. Identify the source owner and place the test beneath its corresponding suite and classification.
   Reuse the canonical fixture or factory for every domain value. When it lacks required data,
   extend that owner and update its consumers instead of spelling the value in the test.
3. Reuse an existing case when setup, execution, and assertions match. Parametrize cases that vary
   only by inputs or outcomes; keep shared fixture context outside the parameter table.
4. Keep builders and fixtures out of test modules. Put reusable construction in the established
   fixture, factory, or test-utility owner and keep each test focused on arranging, exercising, and
   asserting behavior.
5. Run real deterministic application code and real domain models. Double only boundaries the
   process cannot cross or faults the real path cannot produce, using the shallowest declared seam.
6. Before completion, inspect every literal added or changed in tests and test support.
   Replace domain data, sample identities, addresses, names, identifiers, payload fields, and fixture
   facts with values read from the canonical fixture or factory. Keep a literal only when the rubric
   admits it. In a review, report the disposition of every changed literal family, including allowed
   protocol, parametrized-case, and ownerless local-control values. A review is incomplete until each
   family is listed with one of the rubric's dispositions, even when that disposition permits it.
7. Prove every distinct new behavioral guarantee through the mutation workflow below, restore the
   exact baseline, and run the affected repository targets once on the completed tree.

## Mutation Proof

Write every new or materially strengthened behavioral test in the implementation batch before
starting proof; a batch of one still qualifies. Then, for each distinct guarantee:

1. Select the nearest editable canonical first-party implementation. Never mutate generated or
   vendored output, run generation for proof, or mutate the test itself. Mutate test support only
   when that support is genuinely the subject under test.
2. Record the target's exact content plus staged and unstaged state. Apply the smallest unstaged
   mutation that violates only the intended behavior.
3. Run the narrowest repository-native selection containing the relevant cases. Require an
   assertion or observed-outcome failure that demonstrates the intended regression; a setup,
   collection, import, or syntax failure is not proof. For parametrized coverage, confirm the newly
   added case detects its corresponding mutation.
4. Reverse only the temporary mutation. Verify content and version-control state match the recorded
   baseline exactly without reset or checkout, preserve unrelated work, then rerun the affected
   tests successfully.

Never commit or push while a mutation is present. Pure placement, naming, or prose changes that
claim no new behavior do not need mutation proof. If no canonical owned source can be mutated
safely, report the exact blocker and do not claim the test was proven effective.

Report each mutation, the intended regression failure it demonstrated, and the restored passing run.

## Completion

Fix concrete violations encountered in the relevant tests, sibling tests, fixtures, factories, and
shared utilities at the breadth the product-constraints skill sets. Do not turn a focused change
into an unrelated repository-wide audit.

Run the locally available targets reached by the final diff. Run the full suite only when every test
is relevant or the user explicitly requests it.

Report source-to-test placement, sibling conventions checked, fixture and factory owners reused or
extended, parametrized cases reused, encountered corrections, literal-sweep corrections, mutation
proofs, and final affected targets.
