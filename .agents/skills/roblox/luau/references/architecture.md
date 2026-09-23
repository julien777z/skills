# Core, features, contracts, and engine ports

Adapted from [roblox-game-template](https://github.com/Uglypoe/roblox-game-template/tree/main). Its architecture, platform, environment, networking, player-data, and security conventions apply; the parent skill's explicit MVP save policy overrides the template's migration framework.

## Dependency direction

Organize by side (`src/server`, `src/client`, `src/shared`), then `Core` and `Features/<Feature>`. Core is reusable infrastructure; authored content and game rules belong to features. Entry modules compose dependencies and start features. Keep one server and one client startup root per place. Preserve functional engine override scripts separately from startup roots; inspect their purpose before removing them.

Core must not require feature implementation. Narrow composition files may combine feature contracts, such as the profile template and root Blink schema. Contracts contain types, frozen constants, defaults, or schema definitions and require only other contracts. Requiring a Luau module for types still executes it, so avoid cycles and engine work at module load. Resolve services and start subscriptions inside explicit constructors/start functions.

Expose a feature's public module or contracts to other features; keep private modules private. Wire optional cross-feature events in the entry module through injected callbacks or GoodSignal. If two features depend on one another, move the shared contract, connect a signal, or reconsider their ownership. Do not make Core understand quests, map names, or enemy IDs to satisfy the folder structure.

Use string-path requires: `@game/...` for public mounted modules, `./Name` or `../Name` within an owning module tree, and `@self/Child` for children of a folder's `init.luau`. Use the actual Rojo sourcemap, including package trees. Avoid service-chain requires except at a runner boundary that explicitly needs an Instance.

Use frozen constants with literal-preserving casts for state/tag unions rather than repeating strings throughout producers and consumers. Keep the constants beside their feature contract and reuse generated network types where applicable. Content identifiers are authored data; registries should check unique IDs and required fields. Separate mechanics from content definitions rather than branching on named spells inside generic rules.

## Server platform adapters

Put server engine access in `src/server/Core/Platform`. A typed port is a narrow table of functions in domain terms. Construct adapters in `Platform.create()` and inject only the ports each service uses. Engine types in annotations are fine; engine values (`game`, `workspace`, `Instance`, `Enum`) remain in adapters, documented environment/network boundaries, or roots. Use the configured architecture check to enforce these boundaries; do not broaden its allowlist to conceal coupling.

Keep time, logging, players, persistence, networking, character operations, world queries, and teleportation explicit. Return domain values and translate engine enums in adapters. Disconnectable shapes let tests supply simple fakes. Do not copy unused template platform services, Clicker, analytics, or purchases into a game merely because the template has them.

Log through a typed `log` port. Use `LogService:Info` / `Warn` with a stable message and separate structured context. Add user, encounter, or feature context without logging credentials or full profiles. A warning records a recoverable failure; use an actual error when the caller must unwind. Do not substitute `print(message, context)` for structured logging.

## Environment and persistence boundaries

Resolve environment centrally and lazily. Distinguish production, staging, development, and a dedicated test place. Production must be explicitly configured; an unknown universe must not silently use production data. Treat leaked test-place markers in a listed game universe as invalid test isolation. Studio uses mock persistence by default; explicit persistence verification uses an isolated namespace and real cloud-backed editor. Never label mock saves as durable persistence evidence.

ProfileStore belongs behind the server platform's store adapter and one typed session owner. Compose each feature's save contract into the current profile shape. Preserve cancellation during load, presence checks after yields, failed-load protection, active ownership, serialized durable save confirmation, session loss, shutdown, and save-before-travel. See [player data](player-data.md) for the overriding no-shipped-migrations policy.

## Feature networking

Declare messages in feature-owned `.blink` files, imported by the project's root network schema. Generate with the configured Blink recipe; never edit generated modules or create competing handwritten remotes. Only the network owner loads generated Blink runtime modules, and only during startup. Feature services take typed event/transport dependencies so tests can deliver requests without real traffic.

Bound strings, arrays, and numeric payloads using syntax supported by the pinned compiler. Generated types are not authorization: validate player/session/round ownership, proximity, eligible targets, resources, request rates, and once-only outcomes on the server. Derive positions, stats, and rewards from server state. Keep acknowledgments for pending UI operations. Reject stale and duplicate requests without granting duplicate rewards.

Blink Sync handlers must not yield. Use Async handlers for loads, travel, or other yielding work and recheck ownership after relevant waits. Single listeners replace earlier listeners; Many listeners need explicit disconnect ownership. Do not require generated Blink repeatedly in Jest's per-spec module registries; test handler policy through fakes and verify actual transport separately in a client/server Play test.

## Secrets and future purchases

Keep credentials out of source, logs, fixtures, PRs, and generated artifacts. Use scoped Open Cloud credentials in CI secrets and Roblox's secret facilities for authorized runtime integrations. Separate test/staging/production resources. Scan staged files and full history with Gitleaks; a clean history scan does not inspect untracked working files. Use ordinary trusted workflows and never expose credentials to privileged execution of fork code.

If monetization is later authorized, apply [purchase integrity](purchases.md). Guidance alone does not authorize adding monetization.
