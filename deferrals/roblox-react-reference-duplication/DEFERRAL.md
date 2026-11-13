# roblox-react restates its requirements in two files

## Problem

The `roblox-react` skill's entry point (`.agents/skills/roblox/roblox-react/SKILL.md`) and its framework and component reference (`.agents/skills/roblox/roblox-react/references/components.md`) state the same requirements. The reference also repeats some of them internally. The copies agree today. But a change to any of these rules has to be found and made in up to three places, and a copy that gets missed becomes a contradiction.

| Requirement | `SKILL.md` | `references/components.md` |
| --- | --- | --- |
| Shared modal shell; related windows share close behavior and dimensions; a second window replaces the first | "Share the theme, controls, modal shell…" paragraph | "Keep shared theme, controls, modal shells…" paragraph; "Related windows should share one modal shell and lifecycle…" bullet |
| Responsive layout: anchored containers, list/grid layouts, automatic sizing, safe insets; no shrinking a fixed desktop canvas; short and narrow screens | "Use anchored containers…" paragraph under Responsive components | "Use anchored containers…" paragraph (near word for word); "Design for touch separately…" bullet; "Compact screens and touch controls" section |
| Keep expensive previews alive across updates; own and clean up subscriptions, timers, models and render callbacks | "Keep domain state authoritative…" paragraph | "Retain original artwork…" paragraph; "Keep stable widgets alive…" bullet; "Composition and feature ownership" section |
| Typed props and authoritative domain state | "Keep domain state authoritative and component props typed" | "Component props and domain data stay typed"; "Display authoritative state…" bullet |
| Blocking modal and movement input, then restoring it | "A window the player carries…" sentences | "Hide/disable movement controls…" bullet |
| Contextual prompts with touch equivalents | "Use contextual prompts…" paragraph | "Contextual prompts should appear near relevant NPCs/items…" bullet |
| Dismiss blocking lessons before the underlying action | "Dismiss blocking lessons before requiring the underlying action" | "Clear modal instruction overlays before expecting…" |
| Decorative motion and reduced motion | "avoid tiny targets or decorative motion… Respect reduced motion" | "Use short purposeful transitions…" bullet |
| Touch overlap with Roblox's own controls; reaching the last scroll item | "Check narrow and short landscape viewports… overlap with Roblox's top bar and movement controls" | "Design for touch separately…" bullet; "Keep the final scroll item and primary action reachable…" |

Within `references/components.md`, the desktop-canvas and safe-area statement appears in both the opening layout paragraph and the touch bullet. Preview identity across updates appears in the artwork paragraph, the stable-widgets bullet and the feature-ownership section.

## Why it remains open

A review of the change carrying the Roblox guidance batch found this outside that change. The duplication predates the change and fixes no defect. Fixing it means editing `references/components.md`, a file that change does not touch, and deciding which file owns each requirement. That puts it past the incidental cleanup budget.

Admission verdict (acceptance gate, Admission question): **accept**, by the defer test. It is incidental cleanup past the default size budget: the clean result needs edits to `references/components.md`, and it cannot be reached inside `SKILL.md` alone. `SKILL.md` loads the reference only before architecture, dependency, lifecycle or layout changes, so deleting the entry-point copies would cut those requirements off from the review and play-test routes. Which file owns each requirement is the agent's call under the agent-guidance rule's skill shape, not a user decision.

## Pickup scope

`.agents/skills/roblox/roblox-react/SKILL.md` and `.agents/skills/roblox/roblox-react/references/components.md`. Deliver it as an agent-configuration change.

## Resolution criteria

- Each requirement in roblox-react is stated once, in the file the agent-guidance rule's skill shape assigns it: how the skill runs and the critical decisions in `SKILL.md`, and criteria a reader applies in the reference. Where a reader needs the other file, a pointer names it.
- No instruction is lost.
- A reader following `SKILL.md` still reaches every requirement before acting, on every route: design, review, play test and layout.
