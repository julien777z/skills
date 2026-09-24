# Framework and component practices

For a multi-screen stateful interface, choose one established declarative framework and keep a single owner for each UI tree. React Luau offers familiar components/hooks; Fusion offers a different reactive model. Consider team knowledge, maintenance status, ecosystem, and the existing UI before choosing. A formatter or framework alone does not repair architecture. Keep server gameplay independent from the UI framework.

Prefer maintained [Roblox React Lua](https://github.com/Roblox/react-lua) packages for new React projects; inspect the active package manifest before changing an existing dependency. Distinguish official packages from community forks and do not migrate frameworks during unrelated work. Install exact compatible React/renderer versions through Wally and commit the lockfile. Wally's generated alias modules do not automatically forward exported Luau types. [wally-package-types](https://github.com/JohnnyMorganz/wally-package-types) generates those forwarding declarations using the Rojo sourcemap; run a pinned version after package installation before analysis/build. Regenerate aliases instead of manually editing them.

Keep shared theme, buttons, modal shells, cards, and viewport adapters canonical. Component props and domain data stay typed. React's `Node` and `ReactElement` types are not interchangeable in all package versions: explicit component return types and typed child dictionaries can resolve inference/variance errors without casting to `any`. Inspect the installed package types when diagnosing this.

Use anchored containers, list/grid layouts, automatic sizing, constraints, scrolling, and safe insets. Preserve minimum readable text and touch control sizes. Do not scale an entire fixed desktop canvas down to a phone. Measure a tutorial target's actual `AbsolutePosition`/`AbsoluteSize` relative to its overlay instead of converting through an assumed 1280×720 coordinate system. Validate short landscape screens, narrow windows, safe areas, overflow, and modal input blocking.

Retain original artwork through narrowly scoped adapters. Mount a viewport scene once for its asset identity, preserve it across selection changes, and destroy its models, render subscriptions, and animations on unmount. A React wrapper around an unchanged imperative screen is not a screen migration.

## Interaction and presentation

- Use clear hierarchy, a restrained palette, consistent spacing, legible cards/buttons, and clear state feedback. Avoid excessive panels obscuring the environment.
- Related windows should share one modal shell and lifecycle: consistent dimensions, backdrop, focus/input handling, close behavior, and repeated-trigger behavior. Put each feature's content inside that shell; opening another window must replace the current one rather than stack overlays. At the repeated-click checkpoints in the parent skill, verify toggling and switching between every entry point.
- Keep stable widgets alive across frequent snapshots. Destroying and recreating ViewportFrames/cards on every click can cause blank flashes and asset reloads. Update text, health, selection, and enabled state in place; rebuild only when layout/content changes. Keep hover colors consistent with the current selected/disabled base color.
- Use short purposeful transitions; avoid motion that delays basic actions. Give distinct actions recognizable effects and impact timing. Offer reduced camera shake/motion where effects warrant it.
- Design for touch separately. Global scaling of a desktop canvas can make text unreadably small. Enlarge labels and action targets, scroll a wide hand/list where appropriate, and inspect overlap with Roblox's own thumbstick, jump button, top bar, and device safe areas.
- Hide/disable movement controls during interfaces or gameplay modes that prohibit movement, then restore them reliably. Clear modal instruction overlays before expecting the user or test driver to press underlying combat buttons.
- Contextual prompts should appear near relevant NPCs/items. Do not add a permanent "E Interact" button when the proximity prompt already explains the action. Touch must still have an actionable prompt.
- Display authoritative health/resources, legal targets, status effects, and confirmed actions. Use player-facing action names rather than internal content IDs. Make invalid selections understandable without allowing them on the server.

## Nested child dictionaries in React 17.2.1

A dictionary nested directly inside another children dictionary (`Content = props.children`) produced `createTextInstance is unimplemented`; the renderer attempted to render the dictionary key as raw text. Wrap the nested collection in `React.createElement(React.Fragment, nil, props.children)` or merge children into the owning dictionary. Host text belongs in a TextLabel/TextButton `Text` property. This was reproduced with outfit preview buttons after the title screen had rendered successfully, so startup success alone did not validate the next screen.

## Compact combat and touch controls

Budget panels against the measured usable height, including safe insets. Three stacked
44-pixel action rows can exceed a compact action panel's height; consider a two-column grid
when it keeps every control reachable. Put team targets in scrollable side columns on short
landscape screens and reserve a measured central region for the battle camera. Fit
camera framing to that region rather than assuming the desktop hand's height. Inspect
the wizard, monsters, floor boundary, and scenery occlusion after resizing and after
selection/resolution transitions; fitting controls alone is insufficient.

Blocking movement input does not hide Roblox's touch thumbstick and jump button.
Own their visibility while a modal or combat interface blocks exploration, handle
late-created touch UI, and restore its prior state on exit/cleanup. Check this with
real simulated-device input, including retreat and menu close. Preserve readable
card labels and artwork; do not shrink an entire desktop screen to fit.

For short modal layouts, budget the title and primary action together instead of reserving
a large header and a separate footer that leave only a sliver of content. Measure the
actual body: show complete readable cards, using a simple slot-then-spell flow when two
rows will not fit. Avoid nested scroll regions whose bars can draw beyond a clipped
ancestor; give each visible horizontal card row its own bounded space. Keep transient
overworld notices from covering modal actions. Verify scrolling to the final item and
resizing while the window is open, not only the initial screenshot.

## World-space text

Before changing a sign or other world-space message, inspect the adornee and all of
its text-bearing descendants, SurfaceGuis, BillboardGuis, decals, and textures. Find
the authored presentation and runtime writers; fix ownership so updates are
idempotent and do not leave competing text on the same face. Preserve intentional
artwork and give any simultaneous messages separate layout space.

Choose surface dimensions, canvas resolution or PixelsPerStud, font size, padding,
line spacing, and wrapping together for the intended reading distance. Shorten copy
or enlarge/restructure the presentation when it cannot fit legibly; automatic text
scaling alone can hide overflow by making words too small. Verify in Play at normal
player height on supported desktop and touch viewports, including the longest real
content, relevant lighting, oblique approaches, and overlapping world objects.
Inspect screenshots before and after state changes and after repeated application
or rejoin; check the rendered words, not just Text properties or label bounds.

## Composition and feature ownership

Follow the template's distinction between mounting, feature state, and leaf components. A canonical Core UI mount helper owns the ScreenGui and React root; its caller owns unmounting. Use one root per mounted interface, `ResetOnSpawn = false`, and an explicit safe-inset policy. Inject the PlayerGui from the client entry point so engine tests do not depend on `Players.LocalPlayer`.

Feature App components own subscriptions and UI state. Receive subscriptions as typed props, connect them in effects, and return cleanup. Leaf modules return component functions with exported typed Props; they receive data/actions without requiring networking or fetching the local player. Keep rules, formatting, and state transformations engine-free where useful. Preserve expensive preview/card identities during snapshot updates.

Run React tests in the project's Roblox engine tier; pure presentation policy can use its standalone tier. Automated checks complement the parent skill's real-input, repeated-click, responsive, and visual acceptance checks.
