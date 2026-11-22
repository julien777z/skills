# Environments

What holds when work touches a local stack, a verification run, an experiment, a built artifact or
a live deployment. `SKILL.md` names this file at the point a change reaches one.

## Local Stacks

- **Local stack resources are disposable, and repairing them is part of the work, never a question
  for the user.** Local databases and their migration state, Redis, Docker containers, volumes,
  networks, images and the daemon itself can be repaired, reset, dropped or recreated whenever the
  task needs them working. A database stuck on a revision a branch has since regenerated, a stale
  cache, a wedged container: fix it and carry on. The same holds for each of these:
  - **The records a local stack holds:** create, edit, reset, reopen or convert them whenever the
    work needs them in a given state — a test account to sign in with, a submission held in review
    to show a banner, a record a new rule no longer accepts — as the repository's data policy says,
    report what was done, and never put the choice to the user.
  - **The tooling that brings a local stack to a state:** a scenario command, the test accounts and
    records it creates, and what each scenario seeds are added, changed or redesigned as the work
    needs, never put to the user in a plan, a question or a gate's remedy, and never a product
    choice, since no user of the product meets them.
  - **What the session's own work leaves behind when disk, memory or a port runs short:** build
    caches and the leases and snapshots holding them, stopped containers, orphaned processes and
    build output.
  - **Development data in a non-production deployment**, when the project's guidance or its release
    stage marks it disposable: an unreleased product's staging saves, its test profiles and
    accounts, and the records a staging environment holds for its testers are reset, converted or
    recreated whenever the work needs them, such as a test save that no longer loads after an
    item's ID changed, then reported, never put to the user.
- **The limits on that rule:**
  - **A resource another run is actively using is never stopped**, such as a test runner holding
    the stack's lock. Wait for it or use a separate resource. A route that limit rules out, such as
    restarting a daemon a running test still uses, leaves narrower ones, such as removing only the
    leases, records or processes the session's own work created; recovery is exhausted, and
    reported as a gate, only once no route remains.
  - **Production data, and records real users or other people own, stay with the user.**
  - **Deployed and shared remote environments are otherwise not local**; **Built Artifacts And Live
    Deployments** below governs them.

## Verification And Experiments

- Before combining, reordering or parallelizing verification, read its owning runner and lifecycle
  declarations. Preserve their process, session, environment, dependency and resource isolation,
  including setup and cleanup order; related inputs or one verification checkpoint do not establish
  that checks can share an execution context. Keep the declared partitions unless their actual
  contract supports the proposed optimization. Classify a failure against that invocation first:
  correct an unsupported invocation and reproduce through the native route before blaming or
  changing application code. A failure that persists there is investigated at its actual owner.
- Isolate experimental faults from working state other writers, readers or checks can observe.
  Use a private candidate built from the canonical implementation under its native execution contract;
  establish which implementation and dependencies the experiment actually loads and that shared
  state remains unchanged. If that route cannot preserve the contract, establish the concrete
  limitation before arranging an exclusive window with the affected writers, readers and check
  owners. Hold that window through exact restoration and the successful control; a short mutation or later restore
  does not make concurrent exposure safe. Never claim isolation is impossible without checking it.

## Built Artifacts And Live Deployments

- Do not rebuild, republish, or redeploy an already validated artifact solely because its source
  head advanced. Compare the edits with the artifact's actual source: cleanup proven to preserve
  runtime behavior, dependencies, configuration, and required artifact metadata needs no new
  artifact. Keep required source checks, and report the deployed artifact's actual commit and
  digest rather than claiming the cleaned-up head is deployed. A behavior change, an unproven
  equivalence, or a requested release requiring a new artifact still needs the build and rollout.
- Treat create, update, and delete requests against a live deployment as data mutations, not health
  checks: run them only against a target the repository explicitly designates for mutation testing,
  leaving no persistent synthetic records in a stable or shared staging environment, and keep live
  smoke testing read-only everywhere else. Where the same artifact and materially equivalent
  configuration run in several environments, one successful write test on that target plus
  read-only health and routing checks on the others validates the shared path.
