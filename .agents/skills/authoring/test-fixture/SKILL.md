---
name: test-fixture
description: Must be used before creating, moving, renaming, editing, reviewing, or generating any test, fixture, factory, test data, test support, or test configuration in any language, and before executing tests after such a change. Rejects hard-coded domain test data when a canonical fixture or factory owns it, and enforces existing-coverage reuse before new tests, one class per file with small cases folded into existing owning classes, concise parametrized cases, honest doubles, and regression-proof validation.
short_description: 'Check test data and fixtures before changing tests or running tests after a fixture change.'
---

# Test Fixture

Build tests from the repository's canonical test surfaces, keep them beside the source concern they
exercise, and prove that each test protects behavior or an independent contract.

## Dependencies

Read the repository's product-constraints skill when the skill listing declares one, found by its
description rather than assumed by name. It says how broad the fix for an issue encountered while
tracing a test surface is; without one, fix what the focused pass can finish.

## Workflow

1. Read the complete [rubric](references/rubric.md) before inspecting, reviewing, changing, or
   executing any covered test surface. Discover the repository's test roots, distribution and build
   roots, artifact boundaries, fixture packages, factory owner, shared test utilities, runner
   targets, and analogous sibling tests. For a test of shell, process, container, browser, network,
   or operating-system behavior, identify the runtime CI or the deployment declares before writing
   it. That target is the only contract for the durable regression test: construct, execute, and
   validate it there. A local host can diagnose a failure, but never defines the test's contract or
   validates a passing regression test.
2. Apply the rubric's value gate before adding or changing a test. Name its observable
   guarantee, credible regression, distinct coverage need, and any production seam it demands.
   Search and read existing coverage of the same classification first; do not add a test or file when it already catches the regression. Check an existing test's independent contract and collect the rubric's evidence before deleting it.
3. For an application change, finish and validate the source implementation across every affected
   component and repository before writing or strengthening tests or test support. If an applicable
   authorized manual path exists, verify the complete behavior there first; fix and retry failures
   before writing tests. A pull-request-head test deployment requires explicit user authorization.
   After a test-only change, run the relevant test target; do not repeat source, manual, or external
   validation unless the test exposes a source defect that changes the implementation. Existing tests
   may still be run to diagnose development failures.
4. Identify the source owner and its existing test module beneath the corresponding suite and classification. Extend that module before creating another; apply the rubric's class/file boundary test before splitting or relocating a suite.
   Before choosing a support destination, classify what each definition actually does: model generation,
   domain/scenario or I/O setup, pure utility work, or lifecycle registration. Search by that operation,
   including constructors and nested builders, and trace owners, dependencies and consumers. Apply the
   rubric’s placement to that responsibility; a decorator, re-export or return type does not establish
   a separate owner.
   Reuse the canonical fixture or factory for every domain value. When it lacks required data,
   extend that owner and update its consumers instead of spelling the value in the test.
5. Reuse an existing case when setup, execution, and assertions match. Parametrize cases that vary
   only by inputs or outcomes; keep shared fixture context outside the parameter table.
6. Keep builders and fixtures out of test modules. Put reusable construction in the established
   fixture, factory, or test-utility owner and keep each test focused on arranging, exercising, and
   asserting behavior.
7. Run real deterministic application code and real domain models. Double only boundaries the
   process cannot cross or faults the real path cannot produce, using the shallowest declared seam.
8. Before completion, inspect every literal added or changed in tests and test support.
   Replace domain data, sample identities, addresses, names, identifiers, payload fields, and fixture
   facts with values read from the canonical fixture or factory. A provider request or response body
   remains domain data even when it is an expected value, so build it from that owner rather than
   writing it inline. Keep a literal only when the rubric admits it. In a review, report the
   disposition of every changed literal family, including allowed protocol, parametrized-case, and
   ownerless local-control values. A review is incomplete until each family is listed with one of the
   rubric's dispositions, even when that disposition permits it.
9. Prove every distinct new behavioral guarantee through the mutation workflow below, restore the
   exact baseline, and run the affected repository targets once on the completed tree.

## Mutation Proof

After writing new or materially strengthened behavioral tests, prove each distinct guarantee:

1. Select the nearest editable canonical first-party implementation. Never mutate generated or
   vendored output, run generation for proof, or mutate the test itself. Mutate test support only
   when that support is genuinely the subject under test.
2. Apply the global rules' **Tools and environments** experimental-isolation boundary before
   selecting the mutation route. Record the canonical target's content hash, staged and unstaged
   state, and the candidate's baseline. In a private candidate, verify the actual loaded source and
   dependency paths, and preserve the native runner's partitions, environment and lifecycle. An
   isolated file that the process never imports is not a proof target. If isolation cannot retain
   that contract, record the demonstrated limitation and coordinate an exclusive window before
   touching shared state; never substitute a different execution contract to make isolation work.
3. Apply the smallest mutation that violates only the intended behavior. Run the narrowest
   repository-native selection containing the relevant cases. Require an
   assertion or observed-outcome failure that demonstrates the intended regression; a setup,
   collection, import, or syntax failure is not proof. For parametrized coverage, confirm the newly
   added case detects its corresponding mutation.
4. Reverse only the temporary mutation and rerun the affected tests successfully through the same
   route. Verify the canonical content hash and version-control state match the recorded baseline
   exactly, including when proof used a private candidate. Preserve unrelated work without reset
   or checkout, and release an exclusive window only after restoration and the passing control.

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
