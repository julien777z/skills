# Lint, analysis, and test tooling

Provide `just fmt`, `just lint`, `just analyze`, and `just test` recipes, and run the applicable checks for source changes. Inspect the repository's pinned tool manifest, package lockfile, task runner, and CI workflows to discover versions and command details before editing. Do not silently upgrade tools during a refactor.

- [StyLua](https://github.com/JohnnyMorganz/StyLua) formats source; run the configured formatting check.
- [Selene](https://kampfkarren.github.io/selene/roblox.html) supplies Roblox-aware lint checks.
- [luau-lsp analyze](https://github.com/JohnnyMorganz/luau-lsp) checks Roblox types using matching API definitions and a fresh Rojo sourcemap.
- [Lute lint](https://lute.luau.org/cli/lint/) is a separate lint pass, not interchangeable with Selene.
- Use configured architecture and Gitleaks checks alongside those tools; keep engine and manual checks distinct.

Exclude installed packages, generated networking, vendored code, and verification artifacts consistently. Anchor root exclusions so build-output patterns cannot accidentally exclude authored builders.

When configuring CI, keep lint, automated tests, and build/artifact integrity checks distinct. Read the actual workflows to determine which checks exist and whether cloud execution is provisioned.

## Readability and blank lines

Author logical blank-line groups before formatting: StyLua preserves single gaps between statements, Selene leaves whitespace to formatters, and neither Lute's lint rules nor Luau analysis can identify responsibilities, so no available option enforces grouping. Keep `collapse_simple_statement = "Never"` so statements stay expanded, inspect readability explicitly, and do not claim an enforcement option that does not exist.

## Test suites

Separate engine-independent behavior tests from Roblox engine tests, using shared typed fakes where appropriate. A Lute runner with Jest-compatible assertions is not actual Roblox Jest execution. Discover the project's installed runner, suite locations, and supported commands; keep manual interaction tooling separate and results ignored.

Commit the project's package lockfile when its package manager produces one. When using a dedicated test project, mount development packages and fixtures only there; delivery integrity must reject them. Cover authority, failure, cancellation, transitions, rewards, and shared spatial contracts. Static checks do not prove rendering, player controls, persistence across joins, or multiplayer behavior.

## Verified version-specific issues

Some Lute releases misclassify locals used only as assignment receivers or Roblox require arguments as unused. If the project carries a correction, inspect its exact scope and focused regressions for both false positives and real unused variables and parameters, and re-evaluate the patch on a Lute upgrade; another repository does not have it installed.

Some Blink releases do not parse a range suffix after a map declaration even where newer documentation shows it. Use the pinned compiler's supported syntax, bound client requests with string and array ranges and server validation, and never claim a map-size bound that is not enforced.

Verify renamed module trees with the fresh sourcemap.

If Wally directories contain leftover package copies, move the generated directories out of the build input and run the configured package installation again. Wally installation does not prove stale files were removed. Source/package equality must use the clean installed closure.
