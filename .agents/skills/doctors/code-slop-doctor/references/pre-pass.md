# Code Slop Doctor Pre-Pass

The mechanical commands run before any reviewer reads; read from **Pre-Pass** in `SKILL.md`. A bold section name below is a section of `SKILL.md` or of [the lens criteria](lenses.md).

These are the mechanical commands `doctor-protocol` runs once before any reviewer reads, each
listing candidates for the lens named beside it. A tool the repository does not configure is handled
as `doctor-protocol`'s **Measure Before Fan-Out** says. The commands below name the usual tool per
language.

- **Lint and type findings** — the repository's configured lint and type checks over the scope with
  no changed-lines filter.
- **Tangled flow, ceremony and long functions** (**Reads As Slop**) — the repository's linter with
  its complexity and simplification rules switched on for this one run: for Python the first or
  second command below, for TypeScript Biome's complexity group.
- **Copied blocks** (**Duplicate Implementation**) — the repository's cross-file duplication
  detector over each area's trees other than tests, at the tool's default similarity.
- **Dead code** (**Tolerated Past**) — Python: `vulture`, once with the test roots included and
  once without, so a symbol only tests consume stands out; TypeScript: `knip`.
- **Dependencies** (**Dependency Drift**) — unused, undeclared and transitive-only packages from
  `deptry` or `knip`; outdated ones from the package manager, with each runtime version file and
  each container file's `FROM` line set beside the newest stable release; advisories from the
  package manager's audit; and commit-hash pins from the search below, run over workflows,
  manifests and shared checkouts.
- **One-call wrappers** (**Pass-Through Layer**) — a syntax-tree script kept in the run's working
  files, on Python's `ast` or TypeScript's `ts-morph`: every function whose body, after its
  docstring, is one returned or bare call whose arguments are its own parameter names or constants,
  printed with its target and caller count.
- **Single-implementation abstractions** (**Speculative Abstraction**) — the same kind of script:
  every Protocol, abstract base, interface or abstract class with its implementers and subclasses
  counted across the whole tree, listing those with zero or one.
- **Module table, symbol index and import graph** (**Scattered Structure**, **Duplicate
  Implementation**, **Divergent Siblings**) — public names per module from the syntax tree, the
  catch-all search and line counts below, and the import graph from `import-linter` contracts or
  `pydeps` for Python and `madge` for TypeScript, with every edge into an executable marked.
- **Suppressions and escape hatches** (**Tolerated Past**) — the suppression search below, counted
  per file.
- **Warnings** (**Tolerated Past**) — every warning printed in the saved output of
  `doctor-protocol`'s baseline checks, which already run install, build and each suite once, kept
  as a list. The pre-pass runs nothing again with warnings as errors, which would cost as long as
  the suites again to find warnings that output already shows.
- **Environment reads** (**Configuration Drift**) — the environment search below outside the
  settings modules, and each deployment's configuration column, read by name once.
- **One-machine paths and banned terms** (**Repeated Literal**, **Reads As Slop**) — the path
  search below over committed files, and a whole-word, case-insensitive search for each term
  `banned-terminology`'s list and the repository's own table hold, over identifiers and file names.
- **Migration replay** (**Migration Chain**) — the chain replay and drift check the repository's
  migration tooling defines.
- **Use-case candidates** (**Fragmented Use Case**) — the use-case table's candidate rows, each
  loaded and timed as **Inventory** says.
- **Styling count** (**Hand-Written Styling**) — each app's hand-written styling count, as that
  lens defines it.

```sh
ruff check --select SIM,RET,C90,PLR,ARG --no-fix <source roots>
pylint --disable=all --enable=R1702,R0915,R0912,C0121,R1703,R1705,R1719,W0611 <source roots>
vulture <source roots> <test roots> --min-confidence 80
vulture <source roots> --min-confidence 80
npx knip --reporter json
deptry .
npx knip --dependencies
poetry show --outdated
npm outdated --json
pip-audit
npm audit --omit=dev
rg -n 'uses: .+@[0-9a-f]{40}' .github
rg -n '\b[0-9a-f]{40}\b' <manifests>
rg --files -g '{utils,helpers,common,misc}*'
git ls-files | xargs wc -l
pydeps --show-deps <package>
npx madge --circular --json <source root>
rg -c 'type: ignore|pyright: ignore|noqa|pylint: disable|@ts-ignore|@ts-expect-error|biome-ignore|eslint-disable|\bAny\b|cast\('
rg -n 'os\.environ|os\.getenv|process\.env|import\.meta\.env'
rg -n '/home/|/Users/|/tmp/|[A-Za-z]:\\'
```
