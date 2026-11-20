# Verification

When tests, builds, browser verification and reviews run during a task, which suites a run covers,
how a run and its failures are read, and the environment each runs in. What makes a test worth
writing, keeping or removing, and how suites are laid out, configured and budgeted, is
`test-fixture`'s.

## Verification Cadence

- During implementation, edit and inspect the code. Run a diagnostic check only when it answers
  a specific uncertainty and the entire planned batch is known to finish in less than one minute,
  including setup and every selected suite or tool. Use recent comparable runs to estimate it;
  an unknown duration or a total of one minute or more waits. Splitting a batch into individually
  quick commands does not qualify.
- Finish a feature, including its callers and necessary tests, before running its relevant tests,
  build, applicable browser verification and review once. Select browser verification under
  **Environments** before planning its prerequisites. Where it applies to a UI feature, inspect its
  rendered screen and comparable existing interactions at this checkpoint, and fix design or copy
  defects before moving to unrelated work or the final combined checks. Take browser captures only of
  a change that alters what a page shows; a change with no visible effect, a backend or test-only
  repair included, gets no walkthrough capture unless the user asks for one. A task with several features
  may verify each completed feature; an edit, file, commit, push, handoff or plan step is not a feature boundary.
- Classify validation failures under `pre-production`'s **Encountered Issues** before expanding
  repair work. Fix a completed-feature batch's relevant failures together, then repeat only the
  checks the fixes affect. While repairing a failure or a review or gate finding, run only the tests
  that cover the changed code; a repository's full suites run once per pull request, on the head
  delivery accepts, never once per repair.
  Reuse successful evidence for unchanged code and inputs. A new commit or reviewer is not itself
  a reason to repeat verification; a changed dependency, relevant input or unresolved concern is.
  Formatting, import ordering, comments, documentation, and an equivalent non-executable change
  preserve behavioral evidence once the diff establishes that they cannot affect the tested
  behavior. Run the formatter, linter, type checker, or other focused check that owns the edit;
  do not rerun a behavioral suite solely because its head changed.
- **A run whose result a known change will supersede is stopped, never awaited.** Once a result, a
  partial one included, shows a fix is needed, or another change to the same inputs is already
  planned, stop your own in-flight local run of those inputs, make and push the change, then run
  the batch once on the new head; hosted checks follow `merge-gate`. Stop it through its runner's own
  interruption route so fixture teardown and stack and lock release run, and confirm it has exited
  and released its resources before starting the next run. A superseded run holds no push.
- Before delivery, complete the required repository checks and review the combined pull-request
  diff. Reuse still-valid completed-feature results; run the full required checks where the final
  repository state or integration needs them. This cadence changes when verification runs, never
  its required coverage or the exact-head evidence a delivery gate requires.
- Apply the same cadence to the parent and delegated workers. Brief the feature boundary and its
  planned verification batch. Cleanup follows the same completed-scope batch and affected-check
  rerun rule; its presence does not add a test run per edit. Batch related guidance edits before
  their source validation, review and skill tests; verify the final wording rather than
  each intermediate revision.

## Suites And Failures

- Before selecting a test invocation, apply `pre-production`'s **Verification And Experiments**
  boundary to the repository's actual runner, target declarations and setup/cleanup lifecycle.
  Run through its test-runner skill at the required scope, preserving the runner's execution
  partitions rather than joining paths in one framework invocation. A single suite is for iterating
  on a failure you are actively fixing, never the run a change is verified against.
- **Choosing which suites to run is not the author's call.** Do not skip a suite because it looks
  unaffected, runs slowly, or needs services started — start them. If a suite genuinely cannot run,
  name it and say why alongside the result, because a result reported without that caveat claims
  coverage that was never achieved.
  - A suite cannot run only when this session found why itself: its own runner refused with a
    concrete cause after the recovery `pre-production`'s **Local Stacks** gives, or a credential or
    hosted service it requires is absent from where the repository configures it (its settings,
    secrets or environment).
  - When a reviewer, worker or plan says a suite needs credentials, a service or access, check that
    as above; the statement is never the reason itself.
- **A run that verifies a change is read for its cost as well as its counts.** Read each suite's
  wall time against the budget `test-fixture` sets for a suite. Where the native runner supplies
  call durations, compare their sum with wall time; a large gap identifies time outside test bodies.
  Use existing setup and fixture reporting to attribute that cost, recording unavailable attribution
  as unmeasured under existing runner reports. The usual setup causes are a fixture whose setup,
  summed over every test that uses it, dominates (an autouse one especially), an external account
  or identity created per test though nothing per-test lives on it, and a stack torn down and
  rebuilt each run though its inputs have not changed. What the read finds is handled as
  `test-fixture`'s **Test Cost** decides.
- For every pull request an agent creates, ensure all test-related CI jobs pass before considering
  delivery complete; investigate and fix any failures within the pull request's scope.
- When CI tests fail, read the job logs by whichever route reaches them, such as the hosting
  service's API, CLI or connector. Ask the user for the failure output only once the reach check in
  [authorization](authorization.md)'s **Steps Only The User Can Take** finds no route.

## Environments

- Before planning browser walkthroughs or rendered UI inspections, read `run-site`'s **Principles**
  and select its environment applicability. Required automated tests and builds still run.
- **Tests leave the user's desktop undisturbed.** Before selecting or launching a test that uses
  windows or apps, choose an isolated desktop, a headless runtime, or hidden test-owned windows.
  Suppress focus changes, app activation, taskbar or dock appearances, notifications, and sound;
  apply the same policy to child windows and anything the test launches. A hidden first window
  alone does not establish isolation. Verify the runtime's window and activation policy before
  launch, and observe that it stays hidden while it runs. Never minimize, hide, or rearrange the
  user's own windows to make room. General approval to implement or test a change does not approve
  interrupting the desktop. When the behavior cannot be tested silently, prepare the test first,
  explain the specific interruption and ask for explicit permission before that part runs. Continue
  independent checks through nondisruptive routes and report what still lacks verification.
- A cloud workspace snapshot restores files, not running processes. A failing `docker info` at session start means the daemon may need to be started; it does not by itself prove Docker is unavailable.
- Prefer the repository's service-startup helper or skill. Otherwise start the daemon explicitly and wait for `docker info` to succeed:

```bash
mkdir -p .agent_sources/logs
sudo systemctl start docker 2>/dev/null \
  || sudo service docker start 2>/dev/null \
  || (sudo dockerd > .agent_sources/logs/dockerd.log 2>&1 & disown)

for attempt in $(seq 1 15); do
  docker info > /dev/null 2>&1 && break
  sleep 1
done
```

- Report Docker as unavailable only when the CLI is missing or `docker info` still fails after the explicit start attempt, and include the daemon log in that report.
- Browser-automation daemons may start browsers with fresh temporary profiles. Save authenticated session state explicitly and restore it after a daemon restart instead of assuming cookies survive.
