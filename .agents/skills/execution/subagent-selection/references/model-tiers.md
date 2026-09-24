# Model tiers

These are model families, not pinned versions. Each tier uses the latest available member of its
family on the current host. The calling skill chooses the tier appropriate to each assignment.
The tiers are ordered from cheap to frontier; frontier is the highest tier in this policy.

| Tier       | Codex | Claude | Intended use                                       |
| ---------- | ----- | ------ | -------------------------------------------------- |
| `cheap`    | Luna  | Haiku  | Lower-cost, bounded tasks and cheaper-model checks |
| `standard` | Luna  | Sonnet | Balanced reviews, analysis, and substantive tasks  |
| `advanced` | Sol   | Opus   | Difficult tasks requiring stronger reasoning       |
| `frontier` | Astra | Fable  | The most demanding tasks; highest available tier   |

The tiers describe selection policy, not identical capabilities across providers or guaranteed
host availability. An absent family remains unavailable rather than being mapped to another tier.
Reasoning effort is a separate dispatch setting; no tier implies a particular effort or permission
to change repository or global configuration.
