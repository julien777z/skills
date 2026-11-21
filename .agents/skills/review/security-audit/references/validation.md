# Validation and Verification

Contents: **Refuting findings**, **Independent verification**.

The skill that runs these says how many refuters and verifiers it launches; where it launches none,
the same prompts are applied in process against the same rubric.

### Refuting findings

Collect all findings from the hunters and **consolidate duplicates first**. Hunter scopes overlap
on purpose, so the same issue is frequently reported by more than one hunter — merge findings that
share a root cause before validating, or you'll validate and report the same bug multiple times.
For each remaining finding, try to disprove it. The hunters are biased toward finding things; the
refuters are biased toward killing false positives, so a refuter holds one finding, or the findings
of one subsystem when the launching skill's cap groups them, never a hunter's whole list.

Each refuter prompt should:
1. State the specific finding being validated (title, claimed attack, claimed impact)
2. Ask the agent to read the exact code paths and verify each step of the trace
3. Ask it to apply the five tests in the rubric's **What A Surviving Finding Has Been Put Through** —
   exploitation, impact, baseline, mitigation, and parser or runtime behavior, and the rubric's
   **Precedents**

Tell each refuter:

```
Your job is to DISPROVE this finding. Read the actual source code at every step. If you cannot disprove it, confirm it with the exact code that makes it exploitable. Return one of:
- "CONFIRMED: [explanation of why it's real, with code evidence]"
- "REJECTED: [explanation of what the finding got wrong, with code evidence]"
```

Kill false positives on the rubric's terms — its **What A Surviving Finding Has Been Put Through** closes on what that costs and what it must not cost.

For each finding that survives, hold in the session everything the result will need — the session
is the only carrier, so a field nobody writes down is a field the later steps cannot check. That
is: its id, severity, the attack, the impact, the conditions it rests on, the trace as file paths,
line numbers and the enclosing scope of each step, the root cause, and the smallest remediation
under the rubric's **Find The Smallest Fix Before Proposing One**. Hold each hardening note the hunt
produced the same way, under its own id; the result reports them. A finding whose trace cannot be
stated as real paths and line numbers verified against the source is not sufficiently verified —
verify it or reject it.

### Independent verification

The agent that found a vulnerability also wrote its trace, and it will not catch its own blind spots.
A run that verifies findings independently launches **one fresh read-only agent per confirmed
finding**, all in parallel, within the launching skill's cap. Each gets exactly one finding and
verifies it independently. Give each agent that finding and this prompt:

```
You are an independent verifier. You did not write this finding. Your job is to read the actual source code and verify that every factual claim is correct.

1. Read the file and line number cited in every trace step. Verify:
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
- "CORRECTED: [field]: [what was wrong] → [what it should be]" — factual error in one field, named from the finding as refutation recorded it
- "REJECTED: [reason]" — the finding is fundamentally wrong
```

Apply the agent's corrections:
- **VERIFIED** — nothing to change
- **CORRECTED** — correct the finding before it is reported, and say in the report that it was corrected
- **REJECTED** — drop the finding, or report it as investigated and rejected with the reason

This is the final quality gate, and the result waits for it.
