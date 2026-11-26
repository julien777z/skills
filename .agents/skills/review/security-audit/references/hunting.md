# Vulnerability Hunting

Contents: **How the surface is split**, **Hunting methodology** (the prompt every hunter gets, with
its angles and validation rules).

A hunter is the agent, or the in-process pass, that reads a scope as an attacker would. The skill
that launches hunters says how many; this reference says how they divide the surface and what each
is told.

### How the surface is split

Split by attack class **and** by subsystem, because a focused hunter beats a broad one that runs
out of context: where the map of the target reveals an auth system, a plugin system, a media
pipeline and a comment engine, each is its own partition before any class is doubled up. Where
there are fewer hunters than partitions, cover the riskiest partitions first and say in the result
which were not reached.

Every hunter prompt includes:
1. The map of the target — its architecture, trust model and input surfaces — copied in verbatim
2. The specific attack class and scope to investigate
3. Relevant file paths from the map as starting points
4. The hunting methodology (below)
5. The validation rules (below), with the rubric's **Exploitability**, **Precedents** and **What A
   Surviving Finding Has Been Put Through** pasted in whole

### Hunting methodology — include in every hunter prompt

Tell each agent to think like an attacker, not a code reviewer:

```
## How to hunt

Don't just check if defenses exist. Try to break them.

Read the code at depth; do not stop at the first function. Follow the data through
every layer — from the entry point through validation, transformation, storage, retrieval,
and output. Bugs live in the gaps between layers.

Think about these angles:

1. The happy path is defended. Attack the sad path.
   Error handlers, fallback branches, catch blocks, default cases, timeout paths,
   retry logic, cleanup routines. What happens when things fail? Are errors handled
   with the same rigor as success? Does a failed validation leave state half-modified?

2. What happens at boundaries?
   Empty input. Maximum-length input. Null vs undefined vs missing. Zero. Negative numbers.
   Unicode edge cases. The first item and the last item. One more than the maximum. Exactly
   at the rate limit. The moment a token expires.

3. What do components assume about each other?
   Does the database layer assume the API layer validated input? Does the renderer assume
   content was sanitized on write? Does the auth middleware assume routes register themselves
   correctly? Find where trust is implicit and test whether it's justified.

4. What if operations happen in the wrong order?
   Call step 3 before step 1. Call delete during create. Send the callback before the request.
   Hit the confirmation endpoint without starting the flow. Replay a completed flow.

5. What if two things happen at once?
   Two requests to the same resource. Modify while reading. Delete while iterating.
   Publish while someone else is editing. Two users claiming the same unique resource.

6. Where do two parsers or validators disagree?
   Input accepted by the schema but rejected by the database. URL parsed differently by
   the router vs the application code. Content-type header says one thing, body is another.
   Filename extension vs MIME type vs magic bytes.

7. What survives a round trip?
   Data stored then retrieved — is it the same? Does encoding change? Does escaping
   double-up? Is a relative path resolved differently on read vs write? Does serialization
   lose type information?

8. What does the configuration control?
   What happens when config is missing or default? Can an environment variable override a
   security control? Does a feature flag disable validation? What's the security posture
   during setup/first-run before config is complete?

9. Follow the money (or the privilege).
   For every operation that changes state, ask: who authorized this? Trace back to the
   permission check. Is it checking the right permission? Is it checking against the right
   resource? Is there a parallel path to the same state change that checks differently
   or not at all?

10. Look for leaked context.
    Error messages that reveal internal paths. Stack traces in production. Timing differences
    that reveal whether a record exists. Response size differences. HTTP headers that
    disclose versions. Debug endpoints that survived into production.

11. What parameters override security-relevant defaults?
    Where a default is safe but a user-supplied parameter can change it. Look for
    every input that overrides a security-relevant default and check if the override
    is gated by appropriate permissions.

12. Where do unverified claims drive trust decisions?
    Anywhere self-declared identity, capability, or metadata influences an access
    or trust decision without independent verification.

Where you can launch agents, you may launch a research agent when evaluating a potential finding
needs a subsystem understood in depth, so its reading stays out of your own context. Launch at
most two over your whole hunt, each with one subsystem and one question; read a single file
yourself instead.

Your scope is your primary focus, not a boundary.
If while investigating your assigned area you notice something wrong in a different
category — a permission issue while tracing injection, a race condition while reviewing
auth — report it. Don't ignore a bug because it's "not your area." Attackers don't
respect category boundaries.

## Validation rules — apply before reporting a finding
Apply the three sections of the rubric pasted below: **Exploitability**, **Precedents**, and the
five tests in **What A Surviving Finding Has Been Put Through**. Return only findings that survive
all five, each with its concrete attack, or "No exploitable vulnerabilities found" if that is
honest.
```
