# Priority

The order `SKILL.md`'s **Priority** applies when it decides which recorded work runs now.

## Source Work Before Test-Only Work

Pending source work — application or library code, as opposed to tests — ranks above test-only
work, whichever was requested or queued first. Test-only work is test cleanup, test refactors, suite
runtime or coverage work and a sweep's test fixes. Start or delegate it only while no source change
the task owes, in any repository, can proceed, and order the plan's steps and every worker's brief
the same way. Test updates a source change needs travel with that change, and running tests to
verify it is verification, not test work. A test-only item in flight when a source change can
proceed pauses at its next safe boundary.

## Deploy-Safety Work

Source work a deploy the user is waiting on needs ranks above simplification, review gates, test
work, guidance delivery and cleanup, whichever started or was queued first. A database revision to
restore or split so the branch deploys safely onto an environment that already ran an earlier
version is the common case. Start it as soon as the need is known; workers on the lower-ranked
activities pause at their next safe boundary with their work pushed and their next action saved, and
resume once the deploy-safety change is pushed and validated. Those later passes may still change
that code, provided what the deploy depends on stays the same and its owning tests prove it — for a
revision, its database outcome.

## Restoring A Broken Deployed Operation

Restoring an authorized broken deployed operation takes priority over ordinary tests, review gates,
guidance delivery and cleanup. Pause those activities until the actual failed operation succeeds on
the fix branch in every affected environment; use only the reproduction, diagnosis and repairs
needed for that checkpoint, respecting any narrower user restriction. This pause includes ordinary
checks and task-owned workers already running, even on separate files or resources. Pause them at
the runner's next safe boundary, honoring its interruption and cleanup contract; preserve completed
evidence, frozen inputs and the saved next action. An already-started independent cohort is not an
exception permitting continued ordinary work. Deploy through the authorized branch route, then
resume required delivery checks after that live proof. A successful child task, health response or
merge does not establish it. After an authorized merge, repeat the operation from the default-source
deployment; if it fails, resume recovery and pause ordinary delivery work again.

Recovery ends with the deployment back on its own sources. Record each component's deployment
branch and every setting changed for the fix before changing it. Once the fix is on the default
branch, point each component back at its recorded branch, or the default branch when that branch
is gone, deploy image-backed components from that source rather than restoring an image that holds
the fault, undo each temporary setting, and run the failed operation again. Logging added to find
the cause either stays as instrumentation the service keeps, with a test, or comes out before the
pull request carrying it is reported done. While the merge is withheld, the verified fix branch stays
deployed and the report names the pending restoration.
