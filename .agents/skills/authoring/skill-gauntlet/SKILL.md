---
name: skill-gauntlet
description: Audit installed agent skills across every visible scope, then benchmark user-selected skills and propose upgrades or retirement through isolated blind evaluations and a resumable shared dashboard. Use to inventory skill quality, compare a skill with model-only behavior, improve skills experimentally, or run a skill-upgrade gauntlet.
short_description: 'Audit installed agent skills and evaluate upgrades or retirement.'
disable-model-invocation: true
---

# Skill Gauntlet

Build evidence that a skill adds durable value to the current model. Preserve originals, keep
evaluation roles independent, and prefer honest retirement over a manufactured improvement.

## Dependencies

- `use-dashboard` — validate, render, and publish the run dashboard.
- `execute-task` — record actual Gauntlet run or maintenance provenance on the already active
  execution run and follow its **Review-Only Delivery** route; do not start another execution run.

## Resources

- Read [references/protocol.md](references/protocol.md) completely before starting a run.
- Use `scripts/gauntlet.py` to initialize resumable run state, snapshot skills, verify snapshot
  integrity, and export public dashboard state.
- Invoke `use-dashboard` to validate, render, publish, and update the dashboard using the exported
  spec. Record its published link in run state and reuse that page for every update.

## Workflow

1. Discover every installed skill across all project, user, system, plugin, and provider scopes
   visible to the current harness. Resolve symlinks and precedence, but retain each installation
   record even when identical content is deduplicated.
2. Initialize a run under `~/.agents/skill-gauntlet/runs/<run-id>/`. Snapshot every complete skill
   directory before analysis, verify its digest, and mark whether its installed source is editable.
3. Record each skill's purpose, origin, dependencies, overlaps, precedence, and editability in the
   public state. Export and publish the dashboard with `use-dashboard`, give the user its URL in
   chat, present the inventory in chat, and wait for the user's selection. Never
   put selection controls in the dashboard or treat dashboard activity as approval.
4. After selection, run the complete protocol independently for each selected skill. Do not ask
   the user to choose experiments, interpret results, approve revisions, or direct iterations.
5. Pause only for a genuine external blocker, an action that can affect live systems or data,
   unavailable isolation needed to protect evaluation integrity, or unverifiable model identity.
6. After each completed phase, export public state and use `use-dashboard` to re-render and
   republish the same recorded dashboard. Persist sealed tasks and evaluation packets only in the
   run's private `sealed/` directory and never disclose them to
   builders or contestants before final evaluation.
7. Keep the lead agent as the only state writer. Serialize every utility mutation after receiving
   independent-agent results; never let parallel agents call `snapshot` or `update` concurrently.
8. Provisionally install a candidate in a task-owned isolated evaluation environment only after it satisfies
   the frozen iteration acceptance gate. Preserve the original and verify the candidate resolves
   under the intended precedence. Report an isolation or precedence blocker.
9. Run the final held-out acceptance gate after installation. If it fails, restore the isolated
   original snapshot, record the rollback, archive and replace the contaminated held-out set, and
   resume iteration.
10. Finish only when every selected skill is honestly green as an evaluated upgrade or
    `Green — retire`, with its proposed change ready for user review.

## Independence Rules

- Use fresh isolated agent runs for contract extraction, contract verification, benchmark design,
  benchmark audit, every contestant sample, every judgment, and candidate building.
- Give each role only the inputs defined by the protocol. Do not share conversations, reasoning,
  verdicts, contestant identities, skill implementations, or sealed artifacts across roles.
- Anonymize and randomize contestant outputs before judging. Judges evaluate actual deliverables,
  behavior, tool use, and artifacts rather than lead-agent summaries.
- Verify and record the exact model used for every run. Never guess a model's capability, silently
  substitute a model, or claim an unavailable model was tested.

## Delivery

- Preserve original snapshots and the evidence supporting every evaluated upgrade or retirement.
- After the protocol succeeds, deliver upgrade or retirement changes as scoped draft pull requests
  for user review under `execute-task`'s **Review-Only Delivery**. A green evaluation does not mean
  the active skill was installed or deactivated; leave active skills intact pending explicit user
  review and merge instructions.
- Do not edit managed or provider-owned skill sources in place.
- Report the dashboard URL, selected-skill evaluation outcomes, isolated installation destinations, restored originals,
  exact models, final held-out results, and any unresolved external blocker.
