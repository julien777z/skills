# Core, features, contracts, and engine ports

Use this architecture for Roblox game code. Inspect the current ownership and data contracts before editing so changes preserve released progress and remain within the requested scope.

## Dependency direction

Organize source by server, client, and shared ownership, with `Core` for game-independent infrastructure and `Features/<Feature>` for game behavior. Core is reusable infrastructure; authored content and game rules belong to features. Entry modules compose dependencies and start features. Keep one server and one client startup root per place. Preserve functional engine override scripts separately from startup roots; inspect their purpose before removing them.

Core must not require feature implementation. Narrow composition files may combine feature contracts, such as profile defaults and the root Blink schema. Contracts contain types, frozen constants, defaults, or schema definitions and require only other contracts. Requiring a Luau module for types still executes it, so avoid cycles and engine work at module load. Resolve services and start subscriptions inside explicit constructors/start functions.

Expose a feature's public module or contracts to other features; keep private modules private. Wire optional cross-feature events in the entry module through injected callbacks or GoodSignal. If two features depend on one another, move the shared contract, connect a signal, or reconsider their ownership. Do not make Core understand quests, map names, or enemy IDs to satisfy the folder structure.

Use Rojo string-path requires: `@game/...` for public mounted modules, `./Name` or `../Name` within an owning module tree, and `@self/Child` for children of a folder's `init.luau`. Use the actual Rojo sourcemap, including package trees. Avoid service-chain requires except at a runner boundary that explicitly needs an Instance.

Use frozen constants with literal-preserving casts for state/tag unions rather than repeating strings throughout producers and consumers. Keep the constants beside their feature contract and reuse generated network types where applicable. Content identifiers are authored data; registries should check unique IDs and required fields. Separate mechanics from content definitions rather than branching on named spells inside generic rules.

## Server platform adapters

Put server engine access behind a server-side platform layer. A typed port is a narrow table of functions in domain terms. Construct adapters at the application composition boundary and inject only the ports each service uses. Engine types in annotations are fine; engine values (`game`, `workspace`, `Instance`, `Enum`) remain in adapters, documented environment/network boundaries, or roots. Enforce this boundary with an architecture check. Do not broaden its allowlist to conceal coupling.

Keep time, logging, players, persistence, networking, character operations, world queries, and teleportation explicit. Return domain values and translate engine enums in adapters. Disconnectable shapes let tests supply simple fakes. Add only the ports and features the game actually uses.

Log through a typed `log` port. Use `LogService:Info` / `Warn` with a stable message and separate structured context. Add user, encounter, or feature context without logging credentials or full profiles. A warning records a recoverable failure; use an actual error when the caller must unwind. Do not substitute `print(message, context)` for structured logging.

## Environment and persistence boundaries

Resolve environment centrally and lazily. Distinguish production, staging, development, and a dedicated test place. Production must be explicitly configured; an unknown universe must not silently use production data. Treat leaked test-place markers in a listed game universe as invalid test isolation. Studio uses mock persistence by default; explicit persistence verification uses an isolated namespace and real cloud-backed editor. Never label mock saves as durable persistence evidence.

Keep ProfileStore behind the server persistence boundary and one typed session owner. Compose each feature's save contract into the current profile shape. Preserve cancellation during load, presence checks after yields, failed-load protection, active ownership, serialized durable save confirmation, session loss, shutdown, and save-before-travel. Follow the project's release and data-retention policy for migrations.

## Feature networking

Declare server-client messages in feature-owned `.blink` files and import them through the root Blink schema. Generate with the configured recipe; never edit generated modules or create competing handwritten remotes. Only the network owner should load generated Blink runtime modules, and only during startup. Feature services take typed event/transport dependencies so tests can deliver requests without real traffic.

Bound strings, arrays, and numeric payloads using syntax supported by the pinned compiler. Generated types are not authorization: validate player/session/round ownership, proximity, eligible targets, resources, request rates, and once-only outcomes on the server. Derive positions, stats, and rewards from server state. Keep acknowledgments for pending UI operations. Reject stale and duplicate requests without granting duplicate rewards.

Blink Sync handlers must not yield. Use Async handlers for loads, travel, or other yielding work and recheck ownership after relevant waits. Single listeners replace earlier listeners; Many listeners need explicit disconnect ownership. When testing Blink with Jest, do not require generated Blink repeatedly in per-spec module registries; test handler policy through fakes and verify actual transport separately in a client/server Play test.

## Secrets and future purchases

Keep credentials out of source, logs, fixtures, PRs, and generated artifacts. Reuse existing Open Cloud credentials in CI secrets and Roblox's secret facilities for authorized runtime integrations. For a reusable key, select broad account-wide resource and operation permissions, even when the current workflow uses fewer; edit the existing key instead of creating another. Create a new key only if the existing one cannot be reused or edited. Separate test/staging/production resources. Scan staged files and full history with Gitleaks; a clean history scan does not inspect untracked working files. Use ordinary trusted workflows and never expose credentials to privileged execution of fork code.

If monetization is later authorized, apply [purchase integrity](purchases.md). Guidance alone does not authorize adding monetization.
