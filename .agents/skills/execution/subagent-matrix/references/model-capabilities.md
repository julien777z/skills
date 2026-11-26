# Model Capabilities

These are model families, not pinned versions. Each capability label selects the latest available
member of its family on the current host. The calling skill chooses the capability level appropriate
to each assignment. Cheap through advanced form the ordinary capability ladder; specialist is a
separate tier.

| Capability | Codex family | Claude family | Selection | Fallback |
| ---------- | ------------ | ------------- | --------- | -------- |
| `cheap` | Terra | Sonnet | Lower-cost, bounded tasks and cheaper-model checks | Caller-authorized ordinary ladder |
| `standard` | Sol | Opus | Balanced reviews, analysis, and substantive tasks, and a narrow independent judgment: a small packet whose answer accepts no diff for merge | Caller-authorized ordinary ladder |
| `advanced` | Astra | Fable | Difficult and the most demanding tasks, and an independent judgment that accepts a diff for merge or a plan before it is built | Caller-authorized ordinary ladder |
| `specialist` | Astra | Mythos | Only a calling skill explicitly selecting specialist | Claude: `advanced` by default, or caller-selected tier; Codex Astra holds |

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
