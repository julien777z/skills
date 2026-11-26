---
name: roblox-ui
description: Apply whenever a Roblox UI is opened, read, reviewed, inspected, designed, created, modified, or playtested, including HUDs, menus, tutorials, selection screens, viewport previews, loading screens, and UI-owned world-space messages.
short_description: 'Design and change Roblox interfaces, including HUDs and menus.'
---

# Roblox UI

## Dependencies

- `luau`
- `roblox-worldbuilding`
- `roblox-characters`

## Clarity and visual quality

Follow `luau`'s required UI framework. Make every interface clean, easy to use, beginner friendly, and visually pleasing. Treat these as acceptance criteria, not optional polish after code compiles. Change artwork and visual identity where they stand out as incorrect or would be better another way, as the global rules' game-design bullet says.

Apply `luau` whenever reading or editing its Luau code. Return required engine setup and playtest work to the caller. Read [Framework and component practices](references/components.md) before changing architecture, dependencies, lifecycle, or layout.

Give each screen one clear purpose and a recognizable primary action, and review the whole screen before individual controls. Read [screens, lists and windows](references/screens-and-lists.md) before designing or changing a screen's layout, a list with a detail side, control states, a notice or a window.

For UI-owned world-space messages, apply `roblox-worldbuilding`'s world-space text inspection
alongside the component lifecycle and interaction checks below.

Use contextual prompts for nearby interactions and actionable touch equivalents. A tutorial teaches the actual current controls one step at a time, with feedback and pointers attached to measured controls. The pointer already shows where to act, so each step's text is one short line saying what the action does for the player, such as "Tap Boost to pull ahead!" or "Place a plank to cross the gap.", never the click route the pointer shows, such as "Open your bag, choose the plank, then tap the gap to place it.", and never the tutorial's own bookkeeping, such as "Select Place to complete this step." A lesson shows no lesson title, step number or count of steps left, since none of them changes what the player does next. A lesson that explains before it asks for an action gives each page one idea, and its button reads "Next" on every page before the last and "Begin" on the last or only page, never "I understand", "OK" or "Got it", which ask the player to vouch for having read it. Every step whose target is away from the player draws the guide line from the player to it as well as its pointer, a step that is travel, such as riding a lift to the next floor, or a wait, such as an oven timer, as much as any other. While a step is active, hide a prompt that would send the player somewhere else, such as a conversation prompt left on a character whose part is done, or have the step's guide line point to the real target, since a player who sees that prompt may think they must use it again. If using animated pointers, give them a clear shape and a still reduced-motion state. Reserve a gutter beside the measured target; the entire animation envelope must stay outside instruction text, labels, and other controls. Positioning an arrow above a button does not establish that the space above it is empty. Dismiss blocking lessons before requiring the underlying action. Do not overwhelm beginners with controls or explanations that are not yet relevant.

## Responsive components

When a game has a persistent objective HUD, prioritize the next useful action over long headings and paragraphs. Keep a slim reminder visible: the goal with a live count toward its target, such as "Repair lanterns 2/3", plus its reward when it has one; during a guided sequence it holds the current step's goal, never the step's position in the sequence. Top center, clear of Roblox's top bar and the touch movement controls, is the conventional place for it. Briefly reveal details on objective changes, and provide a clear click/tap disclosure control. Deliberately opened details should remain readable until dismissed; cancel automatic preview timers on objective replacement or unmount. Inspect both expanded and collapsed states, including long objectives on narrow screens.

**A main window keeps one fixed size.** A window the player opens and works in, such as a shop, an inventory, a quest log, a map or a settings window, is the same size whatever it holds: switching tabs, changing the selection, filtering a list or a list with few entries never resizes or moves it, and content past its space scrolls inside it. Choose each size for the largest content the window shows at each supported screen size, within the viewport's height and clear of Roblox's top bar and touch controls, and give windows of one kind the same size. Only a small transient panel, such as a line of dialogue, a confirmation or a notice, sizes to its content, so a short message never leaves a large empty box. Check both short and long content, and reset scroll position when replacing the content with a new page.

Use anchored containers, list/grid layouts, automatic sizing, constraints, scrolling, and safe insets. Preserve minimum readable text and usable touch targets. Do not shrink a fixed desktop canvas to fit a phone. Check narrow and short landscape viewports, text overflow, scrolling to the last item, and overlap with Roblox's top bar and movement controls, such as the thumbstick and jump button.

Account for visible borders, focus/selection strokes, shadows, and rounded corners when placing controls inside clipping or scrolling containers. A control whose rectangle fits can still lose the outer half of its stroke. Reserve inner padding for the largest visual extent and the scrollbar; verify the first and last controls and both side edges.

When a transition combines UI with world effects, inspect the effect through the actual scene materials and from the approach camera. Glass can hide translucent geometry behind it; a verified remedy is to hide that surface locally during the effect and restore its previous transparency on cleanup. Own and restore any cinematic camera as well. A component preview proves appearance and cleanup, not successful cross-place travel.

Keep domain state authoritative, and domain data and component props typed. Use stable keys, and keep widgets and expensive previews/ViewportFrames alive across frequent snapshots: update text, selection, health, and enabled state in place and rebuild only when layout or content changes, since recreating a preview on every click causes blank flashes and asset reloads. Own every subscription, tween, animation, timer, model, and render callback; clean them up and cancel stale work on unmount. See the component reference for package typing and artwork adapters.

## Play test: click repeatedly and inspect the result

Require Studio's supported input and viewport capture in a qualified runner; return runner setup and playtest orchestration to the caller. Test actual player-facing controls; direct state mutation is not proof a button works. Do not take over the user's host keyboard/mouse or open obstructive host test windows.

Run the repeated-click pass at the **start of a UI testing session**, when **creating or materially changing a UI**, and during **final verification / before a publication**. A Play restart or routine retest within the same session is not a new session requiring the entire pass. Reuse recorded coverage; repeat an affected check only when a change, failure, or unresolved issue justifies it.

At those checkpoints, cover each affected flow:

1. Open the screen, read it as a beginner, and perform its primary and secondary actions. Check discoverability, readability, clear outcomes, and recovery from invalid actions.
2. Click each entry point multiple times, including rapid repeated clicks. Toggle the same menu open/closed, switch between every related menu, close/reopen it, and switch while state is updating. Check for stacked backdrops, duplicate submissions, stale selections, stuck focus, flicker, and orphan previews.
3. Exercise hover/press/leave, disabled controls, keyboard shortcuts, scroll boundaries, empty/loading/error states, and click outside the modal. Verify clicks cannot pass through to the world or hidden UI, and that nothing under an open overlay shows hover or fires. Movement must resume after closing.
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
