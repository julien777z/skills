---
name: use-diagram
description: "Create or revise a diagram from supplied content. Require an explicit direction from the request or caller; ask when absent. Preserve graph identity and meaning when changing direction alone."
short_description: 'Draw a Mermaid diagram with an explicit direction.'
---

# Use Diagram

## Inputs

- Content: the relationships, decisions or process to show, including any existing graph.
- Direction: explicit `LR`, `RL`, `TD`/`TB`, or `BT`, supplied by the user or calling workflow.

## Workflow

1. Resolve both inputs before drawing. Ask through the available question tool when direction is
   absent; never infer it from the subject. `TD` and `TB` both mean top to bottom.
2. Use Mermaid, with short concrete labels and groups only where they clarify ownership or phase.
   Distinguish execution order, conditions, parallel work and dependency relationships in a legend.
   Preserve uncertainty rather than inventing missing edges.
3. For a direction-only revision, retain node and directed-edge identities, labels, conditions,
   groups and meaning. Change direction declarations only; geometric routing can differ. Compare
   those attributes with the supplied graph before returning it. Label any separately requested
   semantic change explicitly rather than attributing it to orientation.
4. Inspect the whole graph for missing nodes, reversed arrows, disconnected required paths and
   inconsistent conditions. Use a bounded direct comparison; add no parser or installation merely
   to draw a diagram. Diagramming never executes depicted operations or spawns agents by default.

## Output

Return the diagram in a `mermaid` code block followed by the short legend needed to read it.
Include a source snapshot or uncertainty note when supplied. Longer detail follows the current
file-delivery rules. A diagram is not evidence that its depicted work ran.
