# Progress Record

What the task's ledger records about its plan and steps; read from `SKILL.md`'s **Progress Record**
before a plan is recorded or a step is added. Bold section names below are sections of `SKILL.md`.

- **The ledger holds the plan's current state, so nothing about progress depends on what the chat
  still remembers.** When a ready plan goes to the user, record it with `session-ledger` as a
  `plan` entry holding the fields `session-ledger` names for one, its status `shown` with that time,
  filled from the planning work even where the plan shown to the user leaves them out. Work the user
  adds to an active task, with or without a plan of its own, becomes a step on that plan or a plan
  entry of its own, with the user's words and the time they added it, before the first
  edit or dispatch it authorizes; a harness task list, the chat or a summary is never where it first
  lives. A step the agent adds, or widens past what the user asked, is recorded as agent-originated,
  proceeds under the task's authorization like the work **When A Plan Is Needed** says a plan in
  execution covers, and is never shown as user-approved; one that is a product choice goes to the user
  before it is built, as `pre-production`'s **Product Choices** says. Update it when the state
  changes, not when a report is due: the plan being shown, a step starting, finishing, blocking or being
  skipped, a follow-up's plan.
- **A step that waits on other work records what it waits for**: the gate, merge or result whose
  outcome lets it start. Every relayed result is checked against those records, and a result that
  clears one starts the waiting step in that same turn, whichever stream produced it. A report that
  lists only what is still running has not read the plan.
- **A step estimated over 30 minutes is recorded with its parts**: bounded pieces of that step's
  work, each with its own estimate in whole minutes, at least 1, together adding up to the step's.
  Mark each part done as it finishes, so recorded progress moves while a long step runs. The plan
  the user reads keeps its numbered steps; the parts live in the record.
