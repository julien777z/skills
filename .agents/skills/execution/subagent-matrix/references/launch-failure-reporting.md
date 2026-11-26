# Launch Failure Reporting

How a required direct subagent dispatch that cannot start is recorded and reported; read from
**Launch Failure Reporting** in `SKILL.md`, whose **Workflow** and **Dispatch** the bold names
below cite.

When a required direct subagent dispatch cannot start, preserve its exact attempted dispatch.
Handle capacity refusals under Workflow step 3 and other launch failures under **Dispatch**.
Use the native launcher's availability to judge whether it could start the assignment.

- Attempt the selected native dispatch once whenever its direct tool is exposed. Never claim an
  attempted invocation when the tool was not exposed.
- State the native tool's exact name, the assignment role and gated work, selected model, reasoning
  effort, history mode, and every argument sent to the host. Preserve argument names and values;
  omit only typed credentials or other secret values, retaining their field names and shapes.
- State the complete host receipt exactly when one exists. When no invocation was possible, say
  which direct tool surface was inspected and that there is no host receipt.
- Classify the outcome as one of: native tool not exposed, no resolved dispatch identifier, explicit
  unsupported-model receipt, rejected dispatch, capacity refusal, or accepted dispatch whose worker
  later failed. Do not collapse these into a generic unavailable-agent claim.
- Name the fallback taken, with its loss of independence when it ran in process; do not substitute an unrelated agent or claim it performed the assignment.

Use this user-facing shape whenever a launch failure is material to the task:

```markdown
## Subagent launch fallback

- **Assignment:** <required independent step>
- **Native tool:** `<exact direct tool name>` — <attempted or not exposed>
- **Selected dispatch:** `<model>` / `<reasoning effort>` / `<history mode>`
- **Arguments:** `<complete argument names and safe values>`
- **Host receipt:** <verbatim receipt, or `none — <why no invocation was possible>`>
- **Classification:** <one permitted classification and its evidence>
- **Fallback:** <assignment held, handed up to the delegating agent, or top-level in-process work and its loss of independence>
```
