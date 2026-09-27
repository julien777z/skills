---
name: luau
description: Apply whenever Roblox Luau source is opened, read, reviewed, created, or modified, including scripts, modules, builders, tests, network contracts, and tooling configuration. Enforce readable typed code, server authority, lifecycle cleanup, shared spatial definitions, and the checks configured by the consuming project.
---

# Roblox Luau

## Dependencies

- `roblox-react` — apply for React-rendered Roblox interfaces.
- `roblox-studio` — apply for Studio operations, playtests, and place synchronization.

Use this skill even for reading existing Roblox Luau so proposed changes follow its ownership and contracts. Inspect the repository's current conventions and canonical implementation before editing. Reading source alone does not require changing it or running the whole validation suite. User instructions and the actual change determine scope.

Use the required Core/Features architecture and typed server platform ports. Use Rokit, Wally, Rojo, Blink, and `just` as the required toolchain. Use React Luau with ReactRoblox for Roblox UI. Read [architecture and platform contracts](references/architecture.md) when changing ownership, composition, network contracts, environment detection, persistence, or security, and [lint and test tooling](references/tooling.md) for commands and checks.

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

Use ProfileStore through one typed server-side owner for structured player data. Preserve session ownership, failed-load protection, cancellation during load, save/rejoin behavior, and released progress. Read [ProfileStore integration guidance](references/player-data.md) before changes.

## Data compatibility

Use versioned, append-only saved-data migrations and ProfileStore reconciliation when saved data changes. Append and test a migration for renamed, removed, split, or reinterpreted fields. A disposable development profile may be reset only when the project authorizes that operation and identifies the affected keys. Never turn a failed or unavailable DataStore read into a default profile save.

## Spatial ownership

Use explicit map IDs; never infer map identity from arbitrary coordinate thresholds. Author geometry, destinations, navigation, doors, spawns, and protected areas relative to named map/model frames and share those definitions between builders and runtime consumers. Named bounds can locate a player in a combined test map, but authoritative place/map identity remains explicit.

Use named attachments or tagged instances for movable interaction anchors. Validate proximity against their current server position. Retain stable authored quest destinations when actors move or stream out. Numeric coordinates are valid authored content; duplicated positions and implicit identity are the problem. Check whole protected footprints, not only object centers. Focused spatial regressions should move a frame or anchor and verify its consumers together.

## Own lifecycle and cancellation

Give connections, render callbacks, tweens, spawned/delayed work, and camera ownership an explicit owner and cleanup path. Invalidate stale work on unmount, character replacement, streaming removal, encounter exit, and shutdown. Check generation/session identity after every relevant asynchronous wait. Restore prior state rather than guessed defaults; release held inputs even on failure.

For React-rendered Roblox UI work, also apply `roblox-react`. For Studio, assets, playtests, or source/place synchronization, apply `roblox-studio`.

## Keep guidance current

Record verified reusable Luau/tooling issues and solutions here or in its references. Put React-specific lessons in `roblox-react`, Studio operations in `roblox-studio`, and game-specific rules in the project skill. Replace superseded guidance, label unresolved limits, and leave evidence/logs in the workspace. Edit canonical `.agents` content only; generated provider mirrors belong to Agent Sync.
