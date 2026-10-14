# Model Capabilities

These are model families, not pinned versions. Each capability label selects the latest available
member of its family on the current host. The calling skill chooses the capability level appropriate
to each assignment. The labels range from cheap to frontier, with frontier representing the
strongest available model family in this policy.

| Capability | Codex | Claude | Intended use                                       |
| ---------- | ----- | ------ | -------------------------------------------------- |
| `cheap`    | Luna  | Haiku  | Lower-cost, bounded tasks and cheaper-model checks |
| `standard` | Terra | Sonnet | Balanced reviews, analysis, and substantive tasks  |
| `advanced` | Sol   | Opus   | Difficult tasks requiring stronger reasoning       |
| `frontier` | Astra | Fable  | The most demanding tasks; strongest available model |

The labels describe selection policy, not identical capabilities across providers or guaranteed
host availability. An absent family remains unavailable rather than being mapped to another
capability level.
Reasoning effort is a separate dispatch setting; no capability level implies a particular effort or
permission to change repository or global configuration.
