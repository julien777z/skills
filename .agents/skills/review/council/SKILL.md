---
name: council
description: Get review or feedback from three models on different providers, and loop until they agree. Use when the user says "council".
short_description: 'Ask three models from different providers for review, and loop until they agree.'
---

# Council

Before the council reads anything, answer outstanding pull-request comments, fix known issues and
run the relevant checks, so it reviews the current work. When the user wants to drop the
implementation and explore new ideas, skip fixes to code that is being replaced.

## Dependencies
- `review-pass`

## Members

Use the members the user's instructions name. Otherwise pick the latest flagship of three different
providers at high effort, such as Claude Opus, GPT Sol and Gemini Pro.

- **T3 Code:** resolve the models with `orchestrator_capabilities`, then start one `delegate_task`
  per member in parallel, each a new task.
- **Elsewhere:** use the harness's subagents on those models.
- When fewer than three providers are reachable, fill the empty seats with the strongest other
  model of a reachable provider and say so in the result. A named member who is unavailable is
  reported, never replaced silently.

## Rounds

1. Give each member the request, the intent, the diff or material, and the check results. For a
   review, keep members read-only and ask each for findings rated blocker, should or nit, as the
   `review-pass` skill's reviewer brief defines them, and a score out of 10.
2. Collect the replies. Summarise the useful findings, where members disagree, and the next steps.
3. Make the changes you agree with, then start a fresh round. Each full review pass is one round.
4. Stop when every member is satisfied, or after three rounds; then show the open disagreements and
   let the user decide.

Fight scope creep: a finding outside the request follows `review-pass`'s **Review Loop** rule for problems outside
the change.

## Output

When the work ends in a pull request, put this section in its description, before the model and
harness line; edit the description rather than posting a comment. With no pull request, put it in
the final reply. Write `no score` for a member who gave none; never invent one.

```markdown
## Council review

Rounds: <n>

| Member | Round 1 | Round <n> |
| --- | --- | --- |
| <model> | <score>/10 | <score>/10 |
```
