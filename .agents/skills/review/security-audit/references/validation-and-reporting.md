# Validation, Reporting, and Verification

Every level runs every phase. Where a phase below launches agents, the effort table in `SKILL.md`
sets the number at every level, and where it gives none the phase runs in process against the same
rubric.

### Phase 3: Validate findings

Collect all findings from Phase 2 agents and **consolidate duplicates first**. Phase 2 deliberately overlaps agent scopes, so the same issue is frequently reported by more than one hunter — merge findings that share a root cause before validating, or you'll validate and report the same bug multiple times. For each remaining finding, launch a **separate `research` validation agent** that tries to disprove it. The hunting agents are biased toward finding things; the validation agents are biased toward killing false positives. This adversarial step is critical.

For findings from the same attack surface, batch them into one validation agent. Launch validation agents in parallel where they cover independent areas.

Each validation agent prompt should:
1. State the specific finding being validated (title, claimed attack, claimed impact)
2. Ask the agent to read the exact code paths and verify each step of the trace
3. Ask it to apply the five tests in the rubric's **What A Surviving Finding Has Been Put Through** —
   exploitation, impact, baseline, mitigation, and parser or runtime behaviour

Tell each validation agent:

```
Your job is to DISPROVE this finding. Read the actual source code at every step. If you cannot disprove it, confirm it with the exact code that makes it exploitable. Return one of:
- "CONFIRMED: [explanation of why it's real, with code evidence]"
- "REJECTED: [explanation of what the finding got wrong, with code evidence]"
```

Kill false positives on the rubric's terms — its **What A Surviving Finding Has Been Put Through** closes on what that costs and what it must not cost.

For each finding that survives, hold in the session everything the report and any later issue will
need — the session is the only carrier, so a field nobody writes down is a field the later phases
cannot check. That is: its id, severity, the attack, the impact, the conditions it rests on, the
trace as file paths, line numbers and the enclosing scope of each step, the root cause, and the
smallest remediation under the rubric's **Find The Smallest Fix Before Proposing One**. Hold each
hardening note the hunt produced the same way, under its own id; Phase 5 reports them and Phase 6
takes a decision on each. A finding whose trace cannot be stated as real paths and line numbers
verified against the source is not sufficiently verified — verify it or reject it.

### Phase 4: Independent verification

The agent that found a vulnerability also wrote its trace, and it will not catch its own blind spots.
A fresh agent verifies every claim.

Launch **one `research` agent per confirmed finding** via the Task tool, all in parallel. Each agent gets exactly one finding and verifies it independently. Give each agent that finding and this prompt:

```
You are an independent verifier. You did NOT write this finding. Your job is to read the actual source code and verify that every factual claim is correct.

1. Read the file and line number cited in EVERY trace step. Verify:
   - The file exists at that path
   - The line number matches the described code
   - The scope (function name) is correct
   - The description accurately reflects what the code does

2. Verify the root cause statement by reading the cited file and confirming the described defect exists.

3. Verify the execution payloads would actually work:
   - Does the endpoint exist at the claimed URL?
   - Does the HTTP method match?
   - Would the input pass validation as described?
   - Would auth/access checks pass as described?

4. Verify conditions are complete — are there prerequisites the finding missed?

5. Check the remediation — would the fix actually prevent the attack without breaking normal functionality?

Return one of:
- "VERIFIED" — all claims checked out against the source
- "CORRECTED: [field]: [what was wrong] → [what it should be]" — factual error in one field, named from the finding as Phase 3 recorded it
- "REJECTED: [reason]" — the finding is fundamentally wrong
```

Apply the agent's corrections:
- **VERIFIED** — nothing to change
- **CORRECTED** — correct the finding before it is reported, and say in the report that it was corrected
- **REJECTED** — drop the finding, or report it as investigated and rejected with the reason

This is the final quality gate. Do not skip it.

### Phase 5: Report

Present the findings in chat, in one message, ordered by severity. There is no report file: this is
the report.

For each finding give its id, severity, the attack in one or two sentences, the impact, the
conditions it rests on, the trace as file paths with line numbers, and the smallest remediation —
with the materially simpler alternative beside it where one exists, as the rubric requires.

Then, briefly: the baseline comparable the severities were calibrated against, the hardening notes
with their own ids, what the codebase does well, and the coverage statement recommending another run.

Keep it short. A report longer than the codebase deserves is padding.

### Phase 6: Remediation plan and approval

The audit's job does not end at a report. Get the user's explicit decision on every finding, then
implement only what they approve.

**Do not create a fix pull request until the user has approved at least one fix.** That pull request
is the vehicle for approved fixes, never for findings alone. This does not prevent `defer-scope` from
creating a record for a deferred finding. If the environment forces a fix pull request to exist
before approval, keep it draft and do not present it as a deliverable.

The order is: audit → report → present the plan and stop → record every decision → create or reuse
the durable issues → implement only approved fixes → open or ready the validated fix pull request →
update issue metadata and states.

1. **Present the plan.** Preferred path: call the platform's plan-approval mechanism with one
   independently decidable item per finding, ordered by severity, each with its proposed fix and
   blast radius, each accepting **Fix / Defer / Drop**. Then stop and wait. Do not edit application
   code or mark a pull request ready before every finding has a decision.

   **Fallback when no plan mechanism is available** (a headless run, or an agent without one): the
   Phase 5 report has already put every item in front of the user, so walk the findings **one at a
   time** — a **single question per finding** (through the platform's structured-question tool if it
   has one, otherwise a plain chat question) offering **Fix / Defer / Drop**, plus any per-finding
   options such as enforce-versus-remove. Wait for the answer, then ask the next. **Never batch
   several findings into one prompt** — the user should never have to answer five at once. Ask about
   higher-severity findings first. Hardening notes come after the confirmed findings at the same
   cadence; offering to skip the whole hardening batch in one question first is fine.

2. **Record the decisions where the work is picked up.** On the Linear route:
   - For each approved finding, require the security label the repository's project guidance names
     and invoke `linear` to search before creating. Search active, completed, canceled, and archived issues using the label,
     repository metadata, origin pull request, affected surface, and root cause. Reuse only a
     confident match.
   - Create one issue when no match exists. Include the finding id, severity, attack, impact,
     conditions, verified trace, smallest approved remediation, and the `linear` metadata block with
     `Source: security-audit`. Apply other existing labels only when `linear` finds a confident match.
   - Route each deferred finding through `defer-scope`. Retain the security label beside the
     deferral label because the deferred work remains a security concern. A dropped finding
     creates no issue.
   - If an approved issue is later rejected or declined, add the evidence and move it to a
     canceled-category state. Say in the report which it was, and why. Do not delete the issue or
     claim to archive it manually.

   Where the session exposes no Linear integration, an approved finding is carried by its fix and a
   deferred one by `defer-scope`; a dropped one is recorded nowhere, which is what dropping it means.

3. **Implement only approved items.** Apply the smallest correct fix and add or adjust tests. Commit
   and push only after the approved implementation is complete. The fix pull request contains the
   code, tests, contracts, migrations, and generated application output the fix needs, and nothing
   about the audit itself.

4. **Update tracking when the validated pull request is ready.** For every finding that remains
   confirmed and approved, replace pending resolution metadata on its Linear issue with the
   pull-request number, add the validated result, and move it to a completed-category state. The
   completion condition is a ready validated pull request, not its merge. Do not merge without the
   user's separate authorization.

If Linear fails after any issue was created or reused, keep its identifier and retry or report the
blocked update. Do not create a second record for that finding.
