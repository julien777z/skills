# Model Capabilities

These are model families, not pinned versions. Each capability label selects the latest available
member of its family on the current host. The calling skill chooses the capability level appropriate
to each assignment. Cheap through frontier form the ordinary capability ladder; specialist is a
separate tier.

| Capability | Codex family | Claude family | Selection | Fallback |
| ---------- | ------------ | ------------- | --------- | -------- |
| `cheap` | Luna | Haiku | Lower-cost, bounded tasks and cheaper-model checks | Caller-authorized ordinary ladder |
| `standard` | Terra | Sonnet | Balanced reviews, analysis, and substantive tasks | Caller-authorized ordinary ladder |
| `advanced` | Sol | Opus | Difficult tasks requiring stronger reasoning | Caller-authorized ordinary ladder |
| `frontier` | Astra | Fable | The most demanding ordinary assignments | Caller-authorized ordinary ladder |
| `specialist` | Astra | Mythos | Only a calling skill explicitly selecting specialist | Claude Mythos to Opus 5.5 only; Codex Astra holds |

The labels describe selection policy, not identical capabilities across providers or guaranteed
host availability. A catalog omission is not availability evidence; the workflow resolves an
exact host dispatch identifier and classifies its actual assignment. Reasoning effort is a separate dispatch
setting; no capability level implies a particular effort or permission to change repository or
global configuration.

A capture worker, mechanically capturing the pages and states a brief lists, takes the `cheap`
family on every host. It captures without judging; the delegating agent reads every image whole
before relying on it or sending it.

## Review panel

A review panel's three seats take these families, each at its latest host version. A caller that
asks for the panel names these families as its selection. A seat is a model family, not a provider,
so two seats may share a provider.

| Seat | Family |
| --- | --- |
| 1 | Sol |
| 2 | Opus |
| 3 | Fable |

## Dispatch candidates

Prefer the host's latest identifier matching the selected family. When a Codex catalog omits the
family, use the documented candidate below to launch the actual assignment. These are candidates
to test, not supported-model claims or replacements for a newer matching catalog entry.

| Codex family | Catalog-hidden candidate |
| ------------ | -------------------------- |
| Luna | `gpt-6-luna` |
| Terra | `gpt-5.6-terra` |
| Sol | `gpt-6-sol` |
| Astra | `gpt-6-astra` |

For a Claude host, `claude-mythos-5-2` and `claude-opus-5-5` are candidates for
Mythos and the specialist fallback respectively, not claims that the host supports them. Resolve
the latest matching Mythos identifier from the host first; use the exact Opus 5.5 identifier for
the specialist fallback.

Retain the exact request and host receipt. An unsupported rejection invokes only the calling
workflow's permitted fallback; it never authorizes changing capability policy or repository
settings. For any other family or host, resolve an identifier from its selection surface or an exact user
override; a family with no documented or host-resolved candidate triggers the launch fallback.
