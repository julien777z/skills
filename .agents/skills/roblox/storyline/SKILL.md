---
name: storyline
description: Create, audit, or extend a game's substantial, coherent storyline with independent narrative proposals, motivated characters, playable story beats, a connected story web, and a satisfying ending. Apply when asked to develop or improve a game story; support world and map expansion when the narrative needs it.
---

# Storyline

Create a story players want to act in, not a synopsis pasted over chores. Work across genres and engines; obtain game-specific facts from the current project. Distinguish proposed canon from implemented and playtested content.

## Workflow

1. Establish mode: **create** for a new story, **audit** for an existing story, **extend** for a completed arc receiving new scope. Read the actual quests, dialogue, world layout, progression, and endings, not only a design summary. Record the audience, tone, player role, gameplay loop, scope, constraints, existing canon, and known implementation gaps. State reasonable assumptions; ask only for decisions that materially block the work.
2. Read the [story criteria](references/story-criteria.md) and [mode criteria](references/modes.md). Define what success means for this game before comparing proposals. In audit mode, identify concrete weak beats and contradictions with source pointers, then preserve what already works.
3. Spawn **three independent narrative subagents** with the same brief and source reading list. Each returns the structured proposal below, a distinct central conflict and character interpretation, and its strongest objections to its own idea. Do not give them other proposals or prescribe the winning twist. Queue work if concurrency is limited. Their scope is story proposals, not concurrent edits to game code. If subagents are unavailable, disclose the limitation and produce separately reasoned candidates locally.
4. Wait for all proposals. Compare their causal coherence, character agency, playable variety, emotional payoff, onboarding clarity, and production cost using the rubric. Select a coherent strongest proposal or a justified synthesis; do not combine incompatible premises merely to retain every idea. If none clears the quality bar, identify the missing quality and request a focused second round (normally at most two additional proposals). Report remaining weaknesses honestly.
5. Polish a complete story web and implementation map. Expand regions, routes, worlds, or maps when they earn their production cost through distinct playable beats. Identify required environment, art, systems, dialogue, and progression changes, separate essential scope from optional scope, and preserve explicit user limits. A scope proposal is not proof that a map exists. Separate major worlds into the project's established place/level boundaries.
6. In create/audit/extend design-only requests, return the proposed canon and implementation plan. When implementation is authorized, apply the selected improvements through the game's existing content owners and applicable implementation skills. Keep rewards, quest gates, UI instructions, destinations, environmental states, and recap text consistent. Verify the actual playable sequence and ending; distinguish a text audit from a playtest.

## Output

Each subagent and the orchestrator returns valid YAML using the [output schema](references/output-schema.yaml). Populate every section; use empty lists and explicit `unknown` values rather than inventing evidence. IDs are stable within the artifact, and character relationships, beat prerequisites, story-web edges, and setup/payoff links reference existing story IDs. A proposal may leave `selection` empty; the final artifact includes selection rationale, rejected alternatives, concrete changes, unresolved risks, and verification status. Return a concise player-facing premise with a link to the full YAML when the artifact is long. Keep spoilers in the artifact rather than accidentally revealing them in player-facing copy.

## Guardrails

- Every arc resolves its central dramatic question and earns its emotional ending. Future hooks do not excuse an unfinished current story.
- Extend consequences of previous victories; do not erase them, resurrect a defeated threat without groundwork, or retroactively make the player's actions pointless. Mark any proposed retcon and explain its necessity.
- Story length comes from meaningful developments, relationships, discoveries, and varied play—not repeated errands, long exposition, arbitrary travel, or word count.
- Audit candidly. Preserve names and mechanics when they work; recommend substantial changes when evidence supports them, with implementation cost and continuity consequences.
