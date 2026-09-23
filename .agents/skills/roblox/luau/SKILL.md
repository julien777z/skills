---
name: luau
description: Apply whenever Roblox Luau source is opened, read, reviewed, created, or modified, including scripts, modules, builders, tests, network contracts, and tooling configuration. Enforce readable typed code, server authority, lifecycle cleanup, shared spatial definitions, and the project's StyLua, Selene, luau-lsp analyze, and Lute lint checks.
---

# Roblox Luau

Use this skill even for reading existing Roblox Luau so proposed changes follow its ownership and contracts. Inspect the repository's current conventions and canonical implementation before editing. Reading source alone does not require changing it or running the whole validation suite. User instructions and the actual change determine scope.

Read [architecture and platform contracts](references/architecture.md) when changing ownership, composition, network contracts, environment detection, persistence, or security. These conventions adopt the approved template while preserving the explicit MVP policy below.

## Readable, focused implementation

Follow [Roblox's style guide](https://roblox.github.io/lua-style-guide/) and the corroborating [DevForum discussion](https://devforum.roblox.com/t/roblox-lua-style-guide-keep-code-clean-and-consistent/415376). Prefer descriptive names, expanded statements, small cohesive functions, explicit dependencies, and one canonical implementation. Split startup, network dispatch, gameplay services, presentation, camera, and UI when they have independent responsibilities. Do not hide compressed or brittle code behind a framework.

Use explicit Luau syntax and the checked-in formatting settings. Keep a repository-wide mechanical format separate from behavioral changes. Avoid unrelated rewrites during a small fix.

Separate logical groups with a single blank line: services/imports, module state, function definitions, guards, object construction, state changes, animation, and cleanup. Keep tightly related statements together, such as an instance and its property assignments; do not insert a blank line after every statement. Choose boundaries by responsibility, not a fixed line count. Passing a formatter or linter is not proof of readability: inspect the formatted result and retain intentional grouping.

Use `--!strict` for new and rewritten runtime modules. Define precise profiles, snapshots, spatial definitions, component props, and tagged network intent/event unions. Refine unknown values at boundaries. Do not use blanket `any`, disabled diagnostics, or broad lint suppression to make checks green. Inspect actual dependency type exports before adding casts; fix a missing contract at its owner.

## Authority and durable state

Keep authoritative state and rewards on the server. Client requests express intentions. Parse unknown input into bounded tagged values, reject non-finite numbers and invalid indices, and validate player eligibility, session/round identity, ownership, proximity, targets, costs, and rate limits. Static types do not validate client data.

Preserve session ownership, serialized saves, failed-load protection, shutdown saves, and once-only rewards. Never overwrite a failed load with defaults. Keep saves and gameplay contracts unchanged unless the task authorizes a change. Use isolated Studio profiles and validation keys when testing persistence. Development commands require server-side authorization.

Separate animation/camera completion from authoritative resolution. Missing assets, slow rendering, or cancelled effects must not stall gameplay. Keep content definitions, gameplay services, and client presentation distinct without imposing a large architecture on a small feature.

## Structured player persistence

Prefer loleris's **ProfileStore**, the successor to ProfileService, for new structured player-profile saving/loading. Read [ProfileStore integration guidance](references/player-data.md) when choosing, adding, or changing persistence. Keep one typed server-side owner, pin the dependency, respect session ownership and failed-load protection, and verify actual save/rejoin behavior. This preference does not require replacing an existing persistence layer during unrelated work.

## MVP data and compatibility policy

Prefer one clean current runtime contract. Do not add backwards-compatible game code, compatibility shims, legacy load branches, dual formats, deprecated aliases, or shipped migrations unless the user explicitly requests them. Remove superseded paths instead of maintaining them for hypothetical consumers.

For an unreleased/MVP game, development profiles may be reset or moved to a fresh namespace when fundamentally incompatible. A **short one-off migration for the team's explicitly identified testing profiles is also allowed** when it preserves useful testing progress cheaply. Execute it separately from game startup/loading, verify the resulting records against the current schema, then remove the executable migration script. Keep only concise outcome evidence under ignored verification output. Do not include migration code, reconciliation/backfill branches, or old-schema support in runtime modules, builds, or the shipped repository. Do not turn a quick developer-only conversion into a permanent migration framework.

Before that one-off conversion, identify the exact development store and allowlisted tester keys, read and retain a temporary before-state, and respect any active session ownership. Transform only the intended records, validate the result, verify it by loading the current contract, and remove the script. This exception does not authorize a bulk migration of unknown or real player data. If a quick conversion is not sensible, a clean development reset remains valid. Never silently migrate during ordinary player loads.

Keep incompatibility distinct from an unavailable or failed DataStore load: a read failure must never overwrite an unknown existing record with defaults. Keep test namespaces separate from real player data. If a released game or real player progress is involved, establish that requirement before choosing any data deletion; the MVP reset rule is not authority to wipe production users. A code-only refactor that preserves the current contract does not need a schema bump or reset.

## Spatial ownership

Use explicit map IDs; never infer map identity from arbitrary coordinate thresholds. Author geometry, destinations, navigation, doors, spawns, and protected areas relative to named map/model frames and share those definitions between builders and runtime consumers. Named bounds can locate a player in a combined test map, but authoritative place/map identity remains explicit.

Use named attachments or tagged instances for movable interaction anchors. Validate proximity against their current server position. Retain stable authored quest destinations when actors move or stream out. Numeric coordinates are valid authored content; duplicated positions and implicit identity are the problem. Check whole protected footprints, not only object centers. Focused spatial regressions should move a frame or anchor and verify its consumers together.

## Own lifecycle and cancellation

Give connections, render callbacks, tweens, spawned/delayed work, and camera ownership an explicit owner and cleanup path. Invalidate stale work on unmount, character replacement, streaming removal, encounter exit, and shutdown. Check generation/session identity after every relevant asynchronous wait. Restore prior state rather than guessed defaults; release held inputs even on failure.

For Roblox UI work, also apply [roblox-react](../roblox-react/SKILL.md). For Studio, assets, playtests, or source/place synchronization, apply [roblox-studio](../roblox-studio/SKILL.md). Read [Lint and test tooling](references/tooling.md) when running or changing checks.

## Keep guidance current

Record verified reusable Luau/tooling issues and solutions here or in its references. Put React-specific lessons in `roblox-react`, Studio operations in `roblox-studio`, and game-specific rules in the project skill. Replace superseded guidance, label unresolved limits, and leave evidence/logs in the workspace. Edit canonical `.agents` content only; generated provider mirrors belong to Agent Sync.
