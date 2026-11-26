# Project Guidance

## Verification

- Do not add or maintain tests, test fixtures, test-support modules, test runners, or test CI in this repository, including for bootstrap and tooling code. Validate changes with source checks and temporary, untracked execution checks; do not commit those checks or introduce a replacement test suite. The one exception is the pinned regression scenarios `test-skill` runs: one folder per scenario in a skill's top-level `tests/` folder, a YAML file and its fixture's data files, never code; runners and code tests stay out. This narrows the Python rules that send behavior to a test, python-formatting's **Formatting and Documentation** comment rule and poetry's **Testing** section: here the code's names and structure carry behavior, and a comment is kept to the external quirk.
