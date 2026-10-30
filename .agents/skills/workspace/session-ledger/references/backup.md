# Ledger Backup Comments

The shapes of the backup comments the **Backup** section requires, and what they may say.

- **A comment is a fallback for resuming the task, written for a public reader, never a copy of an
  entry.** It holds only what resuming needs, stated generically. The user's words, personal data,
  exact values, the reproduction scenario, the incident that exposed a gap, and anything else about
  the task stay in the private ledger; the comment paraphrases them as the class they belong to. It
  follows the GitHub rule's independent publishing context: no other repository's name, pull
  request, product vocabulary or environment value, and no secret.
- The task token is an opaque value derived from the ledger's stable task identity, such as a short
  hash of it. It says nothing about the task, is the same on every comment the task posts, and can
  be derived again from task context when the ledger is lost, so recovery can tell this task's
  comments from another task's.

## Guidance correction

One comment per `guidance_correction` entry:

```markdown
## Ledger entry
`<entry id>`
Task: `<task token>`

- **Failure class:** <the class of miss, stated generically>
- **Invariant:** <what must hold>
- **Intended behavior:** <what the guidance now says>
- **Canonical files:** <files>
- **Commits:** <short SHAs>
- **Delivery:** <status> — <current stage and next action>
```

## Plans, decisions and questions

One comment per kind on a pull request, headed `## Ledger plans`, `## Ledger decisions` or
`## Ledger questions`, with one section per entry:

```markdown
## Ledger plans
Task: `<task token>`

### `<entry id>`
- **Goal:** <what the plan delivers in this repository>
- **Status:** <status> — <steps done, the active step, and what comes next>

### `<entry id>`
...
```

- A decision's section holds **Decision:** the choice, paraphrased, and **Applies to:** the work it
  governs.
- A question's section holds **Question:** the choice that was open, **Answer:** the option chosen,
  paraphrased, and **Applies to:** the work it unblocked.
