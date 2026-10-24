# Model Capabilities

These are model families, not pinned versions. Each capability label selects the latest available
member of its family on the current host. The calling skill chooses the capability level appropriate
to each assignment. The labels range from cheap to frontier, with frontier representing the
strongest available model family in this policy.

| Capability | Codex family | Claude family | Intended use                                       |
| ---------- | ------------ | ------------- | -------------------------------------------------- |
| `cheap`    | Luna  | Haiku  | Lower-cost, bounded tasks and cheaper-model checks |
| `standard` | Terra | Sonnet | Balanced reviews, analysis, and substantive tasks  |
| `advanced` | Sol   | Opus   | Difficult tasks requiring stronger reasoning       |
| `frontier` | Astra | Fable  | The most demanding tasks; strongest available model |

The labels describe selection policy, not identical capabilities across providers or guaranteed
host availability. A catalogue omission is not availability evidence; the workflow resolves an
exact host dispatch identifier and classifies its actual assignment. Reasoning effort is a separate dispatch
setting; no capability level implies a particular effort or permission to change repository or
global configuration.

## Codex role selections

Resolve the assignment's role before applying the general family table. These exact Codex
selections take precedence over a caller's capability label and over the coordinator's model;
a direct user override for that assignment still takes precedence.

| Role | Codex dispatch identifier |
| --- | --- |
| Review or simplification, including their coordinators, lenses, validators and refuters | `gpt-5.6-terra` |
| Acceptance gate | `gpt-6.1-sol` |

Classify what the assignment does, not its worker name. Ordinary implementation workers checking
their own changes are not independent review assignments. An acceptance gate remains its own role
when a review workflow invokes it. Other Codex assignments and Claude assignments retain the
capability-family selection above. An unavailable role selection is a concrete hold, never
permission to inherit the coordinator's model or substitute another family.

## Dispatch candidates

Prefer the host's latest identifier matching the selected family. When a Codex catalogue omits the
family, use the documented candidate below to launch the actual assignment. These are candidates
to test, not supported-model claims or replacements for a newer matching catalogue entry.

| Codex family | Catalogue-hidden candidate |
| ------------ | -------------------------- |
| Luna | `gpt-6-luna` |
| Terra | `gpt-5.6-terra` |
| Sol | `gpt-6-sol` |
| Astra | `gpt-6-astra` |

Retain the exact request and host receipt. An unsupported rejection invokes only the calling
workflow's permitted fallback; it never authorizes changing capability policy or repository
settings. For another host, resolve an identifier from its selection surface or an exact user
override; a family with no documented or host-resolved candidate remains an identifier hold.
