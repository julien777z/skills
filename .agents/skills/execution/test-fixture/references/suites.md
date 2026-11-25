# Suites, Modules And Test Configuration

Apply these conventions wherever a test, suite, test configuration or test job is written or
changed. The rubric owns what a test is worth, where it sits against its source, its data, its
doubles and its name.

## Suites And Classifications

- Call a group of tests a suite, and unit, integration, smoke, or end-to-end its classification, in code, guidance, pull requests, and messages to the user.
- Keep smoke tests in a `smoke_tests/` classification folder beside `unit/` and `integration/`.
  Source-mirroring rules do not apply inside `smoke_tests/`: put a single smoke module directly in
  that folder, and add a subject folder only when it holds multiple smoke modules. Run that folder
  through a separate reusable workflow called by the main test workflow; selecting the suite
  selects its execution contract.
- Smoke tests always exercise the real configured service; never mock service calls or responses.
  A new smoke test against a third-party provider is written only when the user asks for one, as
  the rubric's **Third-Party Calls Use Documented Doubles** says; otherwise its coverage is an
  integration test using the documented double.
  Remove live-mode flags, opt-in markers,
  conditional skips and fixture branches that choose between real and simulated execution. Missing
  credentials or an unavailable required service fail the suite; neither turns it into a skipped or
  mocked success. Fixtures may own real client setup, scenario construction and cleanup.
- Apply `pre-production`'s **Built Artifacts And Live Deployments** mutation rules. Always-live
  execution grants no additional mutation authority.
- Every directory holding tests must be reachable from a runner target, and a test should assert that correspondence. A suite that no target selects is a suite nothing reports on.

## Module Conventions

For Python tests; a suite in another language follows its native runner and the conventions its
repository already uses.

- Use pytest async tests (`async def test_...`).
- Group tests in classes named `TestXxx`.
- Use fixtures for setup (defined in `conftest.py` or fixture modules).
- Register custom pytest markers in `pyproject.toml` under `[tool.pytest.ini_options].markers` instead of adding them dynamically in `pytest_configure(...)` inside `conftest.py`.
- Add a single-line docstring to every test class and test function.
- Test docstrings must start with `Test that ...` (example: `"""Test that when no credentials are provided an exception is raised"""`).
- Keep all imports at the top of test files. Never import inside test functions or methods.

## Test Configuration

For Python suites; another language keeps test configuration where its runner reads it.

- Define test configuration values (hostnames, database URLs, API keys, repository identities, workflow references, etc.) in `pyproject.toml` under `[tool.pytest.ini_options]` in the `env` section. Values tied to a repository, workflow, deployment target, or provider resource are configuration even when a test currently has only one expected value; renames and target changes must require one configuration update rather than edits across test modules.
- Keep non-secret test environment values in that pytest-env configuration, not in workflow YAML. Workflows provide only secrets, provider credentials, and service-container configuration that pytest-env cannot supply.
- Do not hardcode configuration values in `conftest.py` files.
- Access these values through the production typed settings object when one exists; otherwise use `os.environ` in test code.
- **Test runs treat warnings as errors**, through the runner's own setting, such as pytest's
  `filterwarnings = ["error"]`. Every warning is fixed as `pre-production`'s deprecated-usage bullet
  says. The one ignore allowed is for a defect inside a third-party package that no release fixes,
  no replacement avoids, and nothing the repository passes or configures resolves: it matches that
  package's module and message alone, with a comment naming the package and the upstream fix it
  waits for. A warning about how the repository calls or configures a package, such as an unset
  setting or a deprecated argument, never qualifies.

## Time Budgets

- **Every job that runs a test suite declares `timeout-minutes` of at most 15**, so a hung suite
  fails instead of holding a runner until the platform's six-hour default. A job that calls a
  reusable workflow cannot carry the key, so it goes on the job inside the reusable workflow that
  runs the suite. A local runner that wraps the suites bounds each suite's run at the same 15 minutes.
- **Every suite finishes within five minutes of wall time**, or within a tighter budget the
  repository configures. The 15-minute timeout only stops a hung run; a suite that needs longer than
  its budget is a defect, never a reason to raise the timeout or the budget.
  - Find what made it slow — a test that waits on a real clock, an immutable resource (a schema, a
    compiled artifact, a client) rebuilt per test where it could be built once per session, work
    repeated across parametrized cases — and fix that cause, or remove what cannot be made cheap,
    until the suite fits. The rubric's **Test Cost** names the test, family or module to act on.
  - Splitting the suite across jobs only to stay under the budget, or giving any suite a timeout
    above 15 minutes, hides the same defect.
  - A suite stopped by its time limit, or past its budget, is a defect even when the default branch
    overruns too, so the baseline exclusion in `pre-production`'s **Encountered Issues** never
    covers it. Where its fix goes follows who caused it, so the change stays reviewable as itself:
    - a suite the change made slower is fixed in the change, whatever the fix's size;
    - a suite the change did not slow is a defect the work noticed, placed as `pre-production`'s
      **Scope Follows The Defect, Not The Request** says.
  - Every instruction about a suite's runtime — a worker's brief, a fix step, a gate's remedy —
    states the budget as its target, never only the timeout, since a suite that merely stays under
    the timeout can still be three times over budget.
