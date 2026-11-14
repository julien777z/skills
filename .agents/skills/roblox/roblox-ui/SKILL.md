---
name: roblox-ui
description: Apply whenever a Roblox UI is opened, read, reviewed, inspected, designed, created, modified, or playtested, including HUDs, menus, tutorials, selection screens, viewport previews, and UI-owned world-space messages. Require readable, visually inspected desktop/touch interfaces, explicit cleanup, and repeated real-input Play tests.
short_description: 'Design and change Roblox interfaces, including HUDs and menus.'
---

# Roblox UI

## Dependencies

- `luau`
- `roblox-worldbuilding`
- `roblox-characters`

## Clarity and visual quality

Follow `luau`'s required UI framework. Make every interface clean, easy to use, beginner friendly, and visually pleasing. Treat these as acceptance criteria, not optional polish after code compiles. Preserve the game's established artwork and visual identity unless a redesign is requested.

Apply `luau` whenever reading or editing its Luau code. Return required engine setup and playtest work to the caller. Read [Framework and component practices](references/components.md) before changing architecture, dependencies, lifecycle, or layout.

Give each screen one clear purpose and a recognizable primary action. Use plain player-facing labels, readable type, consistent spacing, alignment, color, and shared controls. Keep related actions together; avoid crowded panels and redundant instructions. Make the next step understandable to someone seeing the game for the first time. Explain unfamiliar actions when needed without exposing internal IDs or implementation details. Tabs or categories that divide a list name the kinds of thing it holds, such as fish and insects in a collection log; an attribute some entries share, such as being rare, newly found or seasonal, is a filter over those kinds, never a category of its own, so no entry is split from its own kind.

Give every action control its name, or a one-line effect, beside its icon; an icon or a key letter alone leaves players guessing what an ability does. Show the input that triggers each action for the device in use (the key on keyboard, the button on gamepad, the on-screen control on touch), and update it when the player switches device.

Review the whole screen before individual controls. Identify the focal point and primary action; inspect the composition’s position, proportions, whitespace, and balance against the usable viewport. A centered title does not center an off-center group. A 3D preview, such as a character, vehicle or creature in a viewport, centers its subject on the subject's rendered bounds, recomputed whenever the shown item changes the silhouette, and frames it so the part the preview exists to show, such as a vehicle's new wheels or a pet's saddle, is visible, faces the viewer and fills enough of the frame to judge; a character preview has its rig and accessories fitted as `roblox-characters` says before the camera is fit. For selection screens, bound and align the title, full previews, confirmation, and status as one composition; preserve intentional asymmetry when the design calls for it. Repeated items shown side by side, such as cards in a row, list rows or grid tiles, share one layout: each shared element, such as a name, a bar, an icon or a price, sits at the same position in every item, so it lines up across the set. Content only some items carry, such as a status line or a badge, takes reserved space or goes after the shared elements, never centering that moves them, and the items share one size. Inspect the set with the optional content on some items and off others. Check safe areas and the surrounding world, HUD, notices, and overlays together on wide, narrow, and short screens. Record the visual defect and repair even when every control is clickable and inside its bounds.

Make selected, hovered, focused, disabled, pending, successful, and failed states distinct. Explain why an action is unavailable where useful. Do not rely on color alone. Keep text legible over the world: give it its own contrast with a heavy weight and dark stroke or an opaque panel behind it, and check it against the brightest and busiest backgrounds it can appear over, since thin, gray or small text on a translucent panel loses contrast over bright scenes. Accommodate wrapping and long content, keep transitions short and purposeful, and avoid tiny targets or decorative motion that delays actions. Respect reduced motion and preserve keyboard/gamepad focus where supported.

Text the player must notice goes where their eyes already are: an instruction they must read to continue, and the outcome of a deliberate action they chose and are waiting on, such as finishing a craft, claiming a reward or a refused attempt; frequent routine feedback, such as a small gain from each pickup, is not this card. Put it in a framed card near the center of the screen, or beside the thing it asks them to act on or the thing their action changed, in type larger than the surrounding HUD or panel text, never a line of small text tucked into a corner, a footer or a toolbar. An outcome is transient: it holds long enough to read, about two to three seconds, then fades without blocking the next action, while a refusal's next step stays until the player acts. Inspect every transient notice, this card included, together with the persistent HUD: a notice can cover a persistent objective or the primary action even when each component fits on its own, so reserve space or place it where it covers no active control, and verify short and wrapped messages on desktop and phone. Judge the card as a first-time player would meet it, from a full-screen capture at each supported size: someone who has not looked for it must notice it within a second.

Give artwork, names, costs, and status labels dedicated layout space. Do not place status text over artwork or squeeze long labels into tiny badges. Check the longest real label at the smallest supported component size and in every relevant state; inspect rendered text, not only its container bounds.

For UI-owned world-space messages, apply `roblox-worldbuilding`'s world-space text inspection
alongside the component lifecycle and interaction checks below.

Share the theme, controls, modal shell, and preview adapters where the game uses them. Related windows use consistent close behavior, backdrop, focus/input handling, and dimensions appropriate to their content. Every dismissible panel shows its close control in the same place across the game, by convention a high-contrast X at the top-right corner, never covered by other HUD elements, and it closes its panel even while other panels are open. A panel's title row holds only its title and close control at every screen size; its actions sit in their own row under the body, compacted on short screens rather than moved beside the title. Reserve a panel whose only exit is a confirm button for a real decision. A second window replaces the first; repeated triggers follow the game's documented toggle behavior. A window the player carries, such as a journal, map or inventory, leaves movement and the camera working while it is open and takes input only on its panel; a window that belongs to standing somewhere, such as a workbench, board or travel gate, and exclusive start screens and modals block underlying pointer, keyboard, hover, and movement input, then restore it on exit.

Use contextual prompts for nearby interactions and actionable touch equivalents. A tutorial teaches the actual current controls one step at a time, with feedback and pointers attached to measured controls. If using animated pointers, give them a clear shape and a still reduced-motion state. Reserve a gutter beside the measured target; the entire animation envelope must stay outside instruction text, labels, and other controls. Positioning an arrow above a button does not establish that the space above it is empty. Dismiss blocking lessons before requiring the underlying action. Do not overwhelm beginners with controls or explanations that are not yet relevant.

## Responsive components

When a game has a persistent objective HUD, prioritize the next useful action over long headings and paragraphs. Keep a slim reminder visible: the goal with a live count toward its target, such as "Repair lanterns 2/3", plus its reward when it has one, and in a fixed guided sequence the step's position, such as "Step 2 of 4". Top center, clear of Roblox's top bar and the touch movement controls, is the conventional place for it. Briefly reveal details on objective changes, and provide a clear click/tap disclosure control. Deliberately opened details should remain readable until dismissed; cancel automatic preview timers on objective replacement or unmount. Inspect both expanded and settled states, including long objectives on narrow screens.

Fit panels to their content. Short dialogue or a small set of actions should not leave a large empty box. Use automatic sizing or measured layout content, readable maximum widths, and viewport height limits; introduce scrolling only when content exceeds those limits. Check both short and long copy, and reset scroll position when replacing the content with a new page.

Use anchored containers, list/grid layouts, automatic sizing, constraints, scrolling, and safe insets. Preserve minimum readable text and usable touch targets. Do not shrink a fixed desktop canvas to fit a phone. Check narrow and short landscape viewports, text overflow, scrolling to the last item, and overlap with Roblox's top bar and movement controls, such as the thumbstick and jump button.

Account for visible borders, focus/selection strokes, shadows, and rounded corners when placing controls inside clipping or scrolling containers. A control whose rectangle fits can still lose the outer half of its stroke. Reserve inner padding for the largest visual extent and the scrollbar; verify the first and last controls and both side edges.

When a transition combines UI with world effects, inspect the effect through the actual scene materials and from the approach camera. Glass can hide translucent geometry behind it; a verified remedy is to hide that surface locally during the effect and restore its previous transparency on cleanup. Own and restore any cinematic camera as well. A component preview proves appearance and cleanup, not successful cross-place travel.

Keep domain state authoritative, and domain data and component props typed. Use stable keys and preserve expensive previews/ViewportFrames while changing selection, health, or enabled state. Own every subscription, tween, animation, timer, model, and render callback; clean them up and cancel stale work on unmount. See the component reference for package typing and artwork adapters.

## Play test: click repeatedly and inspect the result

Require Studio's supported input and viewport capture in a qualified runner; return runner setup and playtest orchestration to the caller. Test actual player-facing controls; direct state mutation is not proof a button works. Do not take over the user's host keyboard/mouse or open obstructive host test windows.

Run the repeated-click pass at the **start of a UI testing session**, when **creating or materially changing a UI**, and during **final verification / before an authorized publication**. A Play restart or routine retest within the same session is not a new session requiring the entire pass. Reuse recorded coverage; repeat an affected check only when a change, failure, or unresolved issue justifies it.

At those checkpoints, cover each affected flow:

1. Open the screen, read it as a beginner, and perform its primary and secondary actions. Check discoverability, readability, clear outcomes, and recovery from invalid actions.
2. Click each entry point multiple times, including rapid repeated clicks. Toggle the same menu open/closed, switch between every related menu, close/reopen it, and switch while state is updating. Check for stacked backdrops, duplicate submissions, stale selections, stuck focus, flicker, and orphan previews.
3. Exercise hover/press/leave, disabled controls, keyboard shortcuts, scroll boundaries, empty/loading/error states, and click outside the modal. Verify clicks cannot pass through to the world or hidden UI. Movement must resume after closing.
4. For selection/confirmation flows, change selection repeatedly, confirm, and attempt a duplicate confirmation. Verify the visible selected state and authoritative result agree; a timeout advancing the game is not proof a click registered.
5. Inspect screenshots at supported desktop, narrow, and landscape phone/tablet sizes when UI changes. Apply the whole-screen composition criteria above; read every instruction, inspect all four button edges and rounded corners, and observe a complete pointer bounce at each affected tutorial step. Check its full motion envelope for text overlap and clipping, including while scrolling. A bounding-box assertion, successful click, or clean lint result is not visual acceptance. Record what was visually inspected; do not infer coverage from a different step or screen. Operate touch controls and scrolling in the simulator, including safe areas. Do not claim physical-device coverage from simulation.
6. Repeat the flow after character replacement, encounter exit, or another relevant lifecycle boundary. Verify camera/input restore, previews remain stable, and connections or animation work do not accumulate.
7. For UI-owned world-space text, apply `roblox-worldbuilding`'s world-space inspection to initial and changed presentations; other UI screenshots and successful gameplay do not cover it.

Fix visible or interaction defects discovered in the affected flow even when lint and builds pass. Keep evidence of actual outcomes. Scale broader gameplay coverage to the change and distinguish Studio, device simulation, persistence, and published-client verification.

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

Exercise a fast first interaction as well as the settled screen. If a request starts a busy UI state before its required data or character is ready, the server must acknowledge a temporary rejection with recoverable feedback; silently returning can leave the UI stuck. Verify that the same visible control becomes usable again and succeeds once its prerequisites are ready. Keep authority checks.

## Keep guidance current

Record verified reusable UI/React issues and solutions in this skill. Put general Luau lint/type guidance in `luau`, a lesson whose subject another skill owns there, and game-specific UI contracts in the project skill. Keep one canonical owner for each rule and leave generated agent mirrors to Agent Sync.
