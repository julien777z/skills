# Lint, analysis, and test tooling

Inspect the repository's pinned tool manifest, package lockfile, task runner, and CI workflows. Prefer the applicable [template conventions](https://github.com/Uglypoe/roblox-game-template/tree/main): Rokit for tools, Wally for packages, and just for commands. Discover actual recipes and pinned versions before running them; do not silently upgrade tools during a refactor.

- [StyLua](https://github.com/JohnnyMorganz/StyLua) formats source; run the configured formatting check.
- [Selene](https://kampfkarren.github.io/selene/roblox.html) supplies Roblox-aware lint checks.
- [luau-lsp analyze](https://github.com/JohnnyMorganz/luau-lsp) checks Roblox types using matching API definitions and a fresh Rojo sourcemap.
- [Lute lint](https://lute.luau.org/cli/lint/) is a separate lint pass, not interchangeable with Selene.
- Use configured architecture and Gitleaks checks alongside those tools; keep engine and manual checks distinct.

Exclude installed packages, generated networking, vendored code, and verification artifacts consistently. Anchor root exclusions so build-output patterns cannot accidentally exclude authored builders. Do not suppress first-party diagnostics to get a green check. Generated agent mirrors are owned by Agent Sync, not a competing formatter.

Prefer separate lint jobs per tool in **Run Lint**, automated suites in **Run Tests**, and build/artifact integrity checks in **Build Places**. Read the actual workflows to determine which checks exist and whether cloud execution is provisioned.

## Readability and blank lines

Author logical blank-line groups before formatting. [StyLua's configuration](https://github.com/JohnnyMorganz/StyLua#configuration) preserves single gaps between statements but does not infer logical groups or require separation between functions. Its `block_newline_gaps` setting only controls existing gaps immediately inside the start/end of blocks: `Never` removes those edge gaps, while `Preserve` retains them. Neither setting inserts missing logical separation. Keep `collapse_simple_statement = "Never"` for expanded statements; do not mistake that option for blank-line enforcement.

[Selene deliberately leaves whitespace formatting to formatters](https://kampfkarren.github.io/selene/luacheck.html). [Lute's built-in lint rules](https://lute.luau.org/cli/lint/) and Luau type analysis do not enforce semantic grouping either. Lute supports custom rules, but a mechanical line-count heuristic cannot identify responsibilities. Inspect readability explicitly; adjust supported formatting options when they improve the actual output, without claiming an unavailable enforcement option.

## Test tiers

Separate engine-independent behavior tests from Roblox engine tests, using shared typed fakes where appropriate. A Lute runner with Jest-compatible assertions is not actual Roblox Jest execution. Discover the project's installed runner, suite locations, and supported commands; keep manual interaction tooling separate and results ignored.

Use one committed package lockfile with shared, server, and development dependencies. Mount development packages and fixtures only in a dedicated test project; delivery integrity must reject them. Cover authority, failure, cancellation, transitions, rewards, and shared spatial contracts. Static checks do not prove rendering, player controls, persistence across joins, or multiplayer behavior.

## Verified version-specific issues

Lute 1.0.0's unused-variable rule misclassifies locals used only as assignment receivers or Roblox require arguments. If the project carries a correction, inspect its exact scope and focused regressions for both false positives and real unused variables/parameters. Re-evaluate any patch on a Lute upgrade; do not assume another repository has it installed.

Blink 0.18.8's `Parser.Map` does not parse a range suffix after a map declaration, despite that syntax appearing in newer documentation. Use the pinned compiler's supported syntax. Bound client requests with string/array ranges and server validation; do not claim a map-size bound that is not enforced.

Rojo maps `init.luau` to the containing ModuleScript. A child require from that module uses `@self/Child`, not `./Child` (which resolves to a sibling of the ModuleScript). Verify renamed module trees with the fresh sourcemap.

If Wally directories contain leftover package copies, move the generated directories out of the build input and run the configured package installation again. Wally installation does not prove stale files were removed. Source/package equality must use the clean installed closure.
