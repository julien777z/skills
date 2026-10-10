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
   exploitation, impact, baseline, mitigation, and parser or runtime behaviour, and the rubric's
   **Precedents**

Tell each validation agent:

```
Your job is to DISPROVE this finding. Read the actual source code at every step. If you cannot disprove it, confirm it with the exact code that makes it exploitable. Return one of:
- "CONFIRMED: [explanation of why it's real, with code evidence]"
- "REJECTED: [explanation of what the finding got wrong, with code evidence]"
```

Kill false positives on the rubric's terms — its **What A Surviving Finding Has Been Put Through** closes on what that costs and what it must not cost.

For each finding that survives, hold in the session everything the report will need — the session
is the only carrier, so a field nobody writes down is a field the later phases cannot check. That
is: its id, severity, the attack, the impact, the conditions it rests on, the trace as file paths,
line numbers and the enclosing scope of each step, the root cause, and the smallest remediation
under the rubric's **Find The Smallest Fix Before Proposing One**. Hold each hardening note the hunt
produced the same way, under its own id; Phase 5 reports them. A finding whose trace cannot be
stated as real paths and line numbers verified against the source is not sufficiently verified —
verify it or reject it.

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

Write every finding, ordered by severity, to one file in the session's scratch directory. In chat,
give the top five by severity in one line each and the next action, and send that file with the
summary.

For each finding the file gives its id, severity, the attack in one or two sentences, the impact, the
conditions it rests on, the trace as file paths with line numbers, and the smallest remediation —
with the materially simpler alternative beside it where one exists, as the rubric requires.

The chat summary then gives, briefly, the baseline comparable the severities were calibrated against, the hardening notes
with their own ids, what the codebase does well, and the coverage statement recommending another run.

Keep it short. A report longer than the codebase deserves is padding.
