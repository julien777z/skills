---
name: roblox-react
description: Apply whenever a React-rendered Roblox UI is opened, inspected, designed, created, modified, or playtested, including HUDs, menus, tutorials, cards, viewport previews, and React-owned world-space messages. Require readable, visually inspected desktop/touch interfaces, explicit cleanup, and repeated real-input Play tests.
---

# Roblox React interfaces

Make the UI clean, easy to use, beginner friendly, and visually pleasing. Treat these as acceptance criteria, not optional polish after code compiles. Preserve the game's established artwork and visual identity unless a redesign is requested. Reading an interface alone does not authorize an unrelated migration.

Apply [luau](../luau/SKILL.md) whenever reading or editing its Luau code. Apply [roblox-studio](../roblox-studio/SKILL.md) for engine setup and playtest orchestration. Read [Framework and component practices](references/components.md) before changing architecture, dependencies, lifecycle, or layout.

## Clarity and visual quality

Give each screen one clear purpose and a recognizable primary action. Use plain player-facing labels, readable type, consistent spacing, alignment, color, and shared controls. Keep related actions together; avoid crowded panels and redundant instructions. Make the next step understandable to someone seeing the game for the first time. Explain unfamiliar actions when needed without exposing internal IDs or implementation details.

Review the whole screen before individual controls. Identify the focal point and primary action; inspect the composition’s position, proportions, whitespace, and balance against the usable viewport. A centered title does not center an off-center group. For selection screens, bound and align the title, full previews, confirmation, and status as one composition; preserve intentional asymmetry when the design calls for it. Check safe areas and the surrounding world, HUD, notices, and overlays together on wide, narrow, and short screens. Record the visual defect and repair even when every control is clickable and inside its bounds.

Make selected, hovered, focused, disabled, pending, successful, and failed states distinct. Explain why an action is unavailable where useful. Do not rely on color alone. Keep text legible over the world, accommodate wrapping and long content, and avoid tiny targets or decorative motion that delays actions. Respect reduced motion and preserve keyboard/gamepad focus where supported.

Give card artwork, names, costs, slot numbers, and status labels dedicated layout space. Do not place status text over the illustration or squeeze an arbitrary label into a slot-number badge. Check the longest real label at the smallest supported card size, including selected, disabled, and provider-granted cards; inspect rendered text, not only its container bounds.

For React-owned world-space messages, apply [world-space text inspection](../roblox-studio/references/world-space-text.md)
alongside the component lifecycle and interaction checks below.

Share the theme, buttons, cards, modal shell, and preview adapters. Related windows use consistent close behavior, backdrop, focus/input handling, and dimensions appropriate to their content. A second window replaces the first; repeated triggers follow the game's documented toggle behavior. Exclusive start screens and modals must block underlying pointer, keyboard, hover, and movement input, then restore it on exit.

Use contextual prompts for nearby interactions and actionable touch equivalents. A tutorial teaches the actual current controls one step at a time, with feedback and pointers attached to measured controls. Use a recognizable arrowhead and tail for tutorial pointers, with a gentle bounce and a still reduced-motion state. Reserve a gutter beside the measured target; the entire animation envelope must stay outside instruction text, labels, and other controls. Positioning an arrow above a button does not establish that the space above it is empty. Dismiss blocking lessons before requiring the underlying action. Do not overwhelm beginners with controls or explanations that are not yet relevant.

## Responsive components

Persistent objective HUDs should prioritize the short next action over chapter headings and paragraphs. Keep a slim reminder visible, briefly reveal details on objective changes, and provide a clear click/tap disclosure control. Deliberately opened details should remain readable until dismissed; cancel automatic preview timers on objective replacement or unmount. Inspect both expanded and settled states, including long objectives on narrow screens.

Fit panels to their content. Short dialogue or a small set of actions should not leave a large empty box. Use automatic sizing or measured layout content, readable maximum widths, and viewport height limits; introduce scrolling only when content exceeds those limits. Check both short and long copy, and reset scroll position when replacing the content with a new page.

Use anchored containers, list/grid layouts, automatic sizing, constraints, scrolling, and safe insets. Preserve minimum readable text and usable touch targets. Do not shrink a fixed desktop canvas to fit a phone. Check narrow and short landscape viewports, text overflow, scrolling to the last item, and overlap with Roblox's top bar and movement controls.

Account for visible borders, focus/selection strokes, shadows, and rounded corners when placing controls inside clipping or scrolling containers. A control whose rectangle fits can still lose the outer half of its stroke. Reserve inner padding for the largest visual extent and the scrollbar; verify the first and last controls and both side edges.

When a transition combines UI with world effects, inspect the effect through the actual scene materials and from the approach camera. Glass can hide translucent geometry behind it; a verified remedy is to hide that surface locally during the effect and restore its previous transparency on cleanup. Own and restore any cinematic camera as well. A component preview proves appearance and cleanup, not successful cross-place travel.

Keep domain state authoritative and component props typed. Use stable keys and preserve expensive cards/ViewportFrames while changing selection, health, or enabled state. Own every subscription, tween, timer, model, and render callback; clean them up and cancel stale work on unmount. See the component reference for package typing and artwork adapters.

## Play test: click repeatedly and inspect the result

Use Studio's supported MCP input and viewport capture inside the [isolated runner](../roblox-studio/references/isolated-testing.md), as described in [background testing](../roblox-studio/references/mcp-testing.md). Test actual player-facing controls; direct state mutation is not proof a button works. Do not take over the user's host keyboard/mouse or open obstructive host test windows.

Run the repeated-click pass at the **start of a UI testing session**, when **creating or materially changing a UI**, and during **final verification / before an authorized publication**. A Play restart or routine retest within the same session is not a new session requiring the entire pass. Reuse recorded coverage; repeat an affected check only when a change, failure, or unresolved issue justifies it.

At those checkpoints, cover each affected flow:

1. Open the screen, read it as a beginner, and perform its primary and secondary actions. Check discoverability, readability, clear outcomes, and recovery from invalid actions.
2. Click each entry point multiple times, including rapid repeated clicks. Toggle the same menu open/closed, switch between every related menu, close/reopen it, and switch while state is updating. Check for stacked backdrops, duplicate submissions, stale selections, stuck focus, flicker, and orphan previews.
3. Exercise hover/press/leave, disabled controls, keyboard shortcuts, scroll boundaries, empty/loading/error states, and click outside the modal. Verify clicks cannot pass through to the world or hidden UI. Movement must resume after closing.
4. For selection/confirmation flows, change selection repeatedly, confirm, and attempt a duplicate confirmation. Verify the visible selected state and authoritative result agree; a timeout advancing the game is not proof a click registered.
5. Inspect screenshots at supported desktop, narrow, and landscape phone/tablet sizes when UI changes. Apply the whole-screen composition criteria above; read every instruction, inspect all four button edges and rounded corners, and observe a complete pointer bounce at each affected tutorial step. Check its full motion envelope for text overlap and clipping, including while scrolling. A bounding-box assertion, successful click, or clean lint result is not visual acceptance. Record what was visually inspected; do not infer coverage from a different step or screen. Operate touch controls and scrolling in the simulator, including safe areas. Do not claim physical-device coverage from simulation.
6. Repeat the flow after character replacement, encounter exit, or another relevant lifecycle boundary. Verify camera/input restore, previews remain stable, and connections or animation work do not accumulate.
7. For React-owned world-space text, apply the linked world-space inspection to initial and changed presentations; other UI screenshots and successful gameplay do not cover it.

Fix visible or interaction defects discovered in the affected flow even when lint and builds pass. Keep evidence of actual outcomes. Scale broader gameplay coverage to the change and distinguish Studio, device simulation, persistence, and published-client verification.

## Keep guidance current

Record verified reusable UI/React issues and solutions in this skill. Put Studio connection/input orchestration in `roblox-studio`, general Luau lint/type guidance in `luau`, and game-specific UI contracts in the project skill. Keep one canonical owner for each rule and leave generated agent mirrors to Agent Sync.

## Startup and transient feedback

For loading that can make the player wonder whether the game is stuck, show a visible
progress bar and a plain-language description of the current stage. Drive determinate
progress from measured work; use an indeterminate bar while the amount of remaining
work is unknown. Never invent percentages with a timer or show completion before the
player can continue. Asset loading alone does not establish that the profile, world,
character, or destination is ready. Keep feedback responsive through each required
stage, distinguish slow progress from failure, and provide a bounded timeout with
actionable recovery instead of an endless loading screen. Verify fast, delayed,
stalled, and failed loads on desktop and touch layouts, including reduced motion and
the transition from loading to usable gameplay.

Exercise a fast first interaction as well as the settled screen. A wardrobe preview can
finish before the live character is ready. If a valid request starts a busy UI state,
the server must acknowledge a temporary readiness rejection with recoverable feedback;
silently returning can leave the UI stuck forever. Verify that the same visible button
becomes usable again and succeeds once the character is ready. Keep authority checks.

Inspect transient notices together with the persistent HUD. A wide top-center toast
can cover the chapter panel even when each component fits the viewport independently.
Use a reserved area above the exploration toolbar and bound its width; verify short
and wrapped messages on desktop and phone. Combat notices need their own placement
so they do not cover cards or targeting controls.
