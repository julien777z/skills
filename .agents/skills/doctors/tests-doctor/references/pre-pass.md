# Tests Doctor Pre-Pass

The mechanical commands run before any reviewer reads; read from **Pre-Pass** in `SKILL.md`. A bold section name below is a section of `SKILL.md` or of [the lens criteria](lenses.md).

These are the mechanical commands `doctor-protocol` runs once before any reviewer reads, serialized
as the runner requires, each listing candidates for the lenses that read it. A tool the repository
does not configure is handled as `doctor-protocol`'s **Measure Before Fan-Out** says. The commands
below are pytest's, and a suite on another runner uses that runner's equivalent.

- **Collected tests** — every test the runner collects per target, and every test directory no
  target reaches.
- **Timing** — every runner target through the runner's own per-test and per-fixture duration
  reporting, with baseline pass and fail state and suite wall times. Rank cases and fixtures only
  where existing reporting attributes their costs; missing attribution is recorded as unmeasured,
  not filled by a new maintained diagnostic system. A suite that cannot run locally uses its
  existing CI timing when available.
- **Coverage by test** — line coverage per suite with the test that covers each line, where the
  runner's coverage plugin records it.
- **Fixtures** — every fixture the runner knows against the references to it, listing those no
  test requests, and every fixture definition by module.
- **Doubles** — a syntax-tree script kept in the run's working files that lists every patch target
  and mock construction with the module that owns the target.
- **Skips** — every skip mark, xfail mark, conditional skip and commented-out test.
- **Repeated blocks** — the repository's cross-file duplication detector over every test tree, at
  the tool's default similarity.
- **Symbols only tests consume** — every module-level symbol in an application package with its
  consumers classified by root, from the symbol table or a dead-code detector run with and without
  the test roots; and every import from a test root into an executable, from the import table.
- **Test-to-source map** — one row per test module with the source module or package it resolves
  to, as **Align Structure With Siblings And Source** lays the table out.

```sh
pytest --collect-only -q
pytest --durations=0 --durations-min=0
pytest --cov --cov-context=test
pytest --fixtures -q
rg -n 'pytest\.mark\.(skip|skipif|xfail)|pytest\.skip\(|pytest\.importorskip|^\s*#\s*(async )?def test_'
rg -n '@pytest\.fixture' -g 'test_*.py' -g 'conftest.py'
vulture <source roots> --min-confidence 80
```
