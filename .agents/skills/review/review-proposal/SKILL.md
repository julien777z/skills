---
name: review-proposal
description: "Prepare a proposed change for an existing user-approval boundary or a directly requested proposal review. Challenge the whole proposal with three fresh standard reviewers per round, count nit-only rounds as clean, and obtain independent Proposal acceptance after two substantive clean rounds or four-round dispute adjudication. Technical readiness never grants user approval."
short_description: 'Challenge a proposal and obtain independent acceptance before presenting it for approval.'
---

# Review Proposal

The calling agent runs this workflow directly. It prepares the decision; the caller presents it
and obtains the user's approval under the global question procedure.

## Dependencies

- `pre-production` — apply the full target-contract guidance to the proposal and every alternative.
- `subagent-matrix` — select and dispatch fresh reviewers and the separate acceptance role; retain
  their original results and recover incomplete producers under its Dispatch procedure.
- `acceptance-gate` — the independent Proposal verdict and its binding repair procedure.
- `session-ledger` — retain the proposal, inputs, review evidence, dispositions and pending decision.

## Scope

Use where approval of a proposed change is already required: implementation plans and explicit
product, security, disclosure or scope alternatives. This creates no new approval requirement.
Factual questions, status reports, routine authorized actions and a platform's separate action-time
confirmation do not enter this workflow. Optional factual discovery is not an attack slot.

## Workflow

1. **Prepare the evidence.** Build the acceptance-gate intent statement from the user's requirements,
   accepted decisions and verified repository facts. Distinguish facts, proposed changes and choices
   the user must make. Freeze the proposal, intent, full pre-production text, relevant project guidance
   and referenced contract or retained-data facts, with their exact content identities. Every attacker
   receives the same material and the [attack criteria](references/attack-criteria.md). Record a verified
   absence or a non-repository scope explicitly; missing required evidence returns `needs-evidence`
   with its source and next action. Do not load unrelated rules or invent facts. Explicit alternatives
   can be reviewed without choosing for the user; incomplete evidence cannot be treated as a choice.
2. **Attack the whole proposal.** Dispatch three fresh read-only standard reviewers per round using
   subagent-matrix. Give them different emphases: requirements/authority, ownership/design and
   verification/cost/recovery. Each still applies every criterion to the whole proposal and receives
   the complete pre-production guidance. Keep peer reports out of the round. Run ready slots in
   parallel when capacity permits; queue unstarted slots otherwise. Follow the selector's original
   result and producer-recovery contract, replacing only stopped or unproven slots, never live workers
   or valid siblings. Count only verified compliant launches, identical inputs and complete originals.
3. **Resolve findings and count rounds.** Read every original and consolidate duplicates. Before
   updating the streak, classify each reported item as material, nit or refuted against the criteria
   and record its evidence-backed disposition. An attacker's `CHANGES_REQUIRED` label alone never
   makes a round unclean; retain that label separately for the gate. Investigate concrete material
   objections and apply justified remedies. A clean round has
   three complete reports and no unresolved material finding under the criteria; nit-only rounds
   count clean. Normally obtain two consecutive substantively clean rounds with fresh cohorts.
   Material changes to approach, scope, ownership, verification, intent or supporting facts invalidate
   affected evidence and restart the streak. Avoid applying optional polish during attacks. For a
   byte-changing clarification without those effects, retain both identities and the comparison
   supporting carry-forward; never claim the old report reviewed new bytes.
4. **Obtain independent acceptance.** After two clean rounds, send the current proposal to
   acceptance-gate. After four attack rounds without the streak, send it for the same independent
   Proposal adjudication instead of dispatching another cohort. This alternate route never claims
   two clean rounds occurred. Supply its five native inputs and exactly `Proposal — should this be
   written?`. The proposal item includes the actual round history, every substantive finding or
   material alternative verbatim with evidence, benefit, tradeoff and disposition, coverage receipts,
   and locators/content identities for the directly available originals. An index is navigation,
   never a substitute for originals. Retain each original and its digest/readback receipt through
   session-ledger; verify its bytes again before dispatch and deliver frozen content through the
   native content-or-file route. An ordinary path or digest alone does not freeze a file. Use direct
   content where the file boundary cannot be preserved, or hold for the actual delivery limitation.
   Do not add a snapshot platform or truncate evidence. Verify the separate fresh gate's compliant
   dispatch, exact packet and complete original verdict before counting it.
5. **Repair and return.** Apply acceptance-gate Bounds to flags, preserving original objections and
   remedies. A flag never becomes readiness because a counter elapsed. Send repairs to a fresh gate;
   restart attacker review only if a repair changes approach, scope, ownership or verification. A new
   material design cycle retains its preceding history and the same four-round adjudication
   checkpoint; renaming or caller re-entry cannot erase objections or reset a cycle. Missing or lost
   gate output follows subagent-matrix recovery without redoing valid attacker evidence. Return the
   result to the caller. Do not request approval here or recursively review the gate itself.

Reuse a ready receipt only for its exact proposal, reviewed inputs and affected-owner map. A changed
item invalidates that acceptance receipt even when earlier attack evidence can be carried forward.
The caller consumes the ready receipt once through the global question procedure; encountering it
again is not a reason to rerun the workflow. Keep unresolved user choices separate from technical
readiness and continue independent authorized work while they wait.

## Output

Return this record through session-ledger, with detailed evidence at private locators:

```yaml
status: ready-for-user-approval | held | needs-evidence
proposal: <locator and exact content identity>
inputs: <reviewed input identities and affected-owner map>
rounds: <actual history, clean streak and normal/adjudication route>
evidence: <original report identities, coverage and alternative dispositions>
gate: <exact packet, dispatch and original verdict, or missing evidence>
next_action: <caller presentation or concrete repair/recovery>
```

`ready-for-user-approval` requires independent acceptance. It never authorizes implementation,
merging, deployment, publication or a separate user-triggered action.
