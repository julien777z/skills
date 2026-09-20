# Security Audit Rubric

What counts as a finding, what it is worth, and what its remedy costs. This file is the judgement;
the workflow that applies it lives in `SKILL.md` and the other references. Another skill may borrow
this file on its own — `acceptance-gate` reads it to judge a diff — so it states criteria and never
procedure.

## Only Report What You Can Exploit

Every finding names a concrete attack: who the attacker is, what they send, and what they get. "An
attacker could theoretically" is not a finding. "Send this request, get this result" is.

"Potentially" and "theoretically" mark the place where the work stopped. Either you can exploit it or
you cannot; if you need the word, you have not researched it far enough.

## Defense-In-Depth Gaps Are Not Vulnerabilities

Where one layer already prevents the attack, the absence of a second is a hardening note, not a
finding, and never inflated to carry a severity. "Missing validation where the query builder already
quotes identifiers" is a note.

## Severity Requires Impact

Severity is **likelihood** and **impact** together — how easy it is to reach, and what damage it
achieves.

- **CRITICAL** — unauthenticated remote code execution, full database dump, admin takeover without
  credentials.
- **HIGH** — authenticated remote code execution, injection with data exfiltration, stored
  cross-site scripting that fires for every user, authentication bypass. Also any finding where the
  permission model is *completely* defeated for an action with real consequences: a user performs
  something the system explicitly gates behind a higher role.
- **MEDIUM** — a targeted exploit needing specific conditions, a forged state change, disclosure of
  secrets or credentials. Also a business-logic bypass with real but limited consequences: it needs
  authentication, or is confined to the attacker's own data, or requires uncommon conditions.
- **LOW** — disclosure of non-secret data, denial of service requiring sustained effort, hardening
  gaps.

The line between HIGH and MEDIUM for a logic finding is whether it **defeats an explicit security
boundary**. A defeated boundary is HIGH. A data inconsistency, a finding needing privileged access,
or one with a small blast radius is MEDIUM.

If the concrete damage cannot be described, the severity is lower than it looks.

## Determine The Baseline Dynamically

Identify what the application is and what comparable applications exist, and calibrate against those
— not to dismiss findings, but to aim effort. A comparable with the same pattern that has been
exploited makes the finding **stronger**. A comparable with the same pattern nobody has exploited in
twenty years is one to understand before reporting.

Never hardcode a comparable. A content system is compared to other content systems, a gateway to
other gateways; a genuinely novel application may have none.

## What A Surviving Finding Has Been Put Through

A finding is worth reporting once it has survived every one of these, applied by someone trying to
kill it rather than to keep it:

1. **Exploitation** — the code at each step of the trace does what the trace claims, and the exact
   triggering input can be constructed.
2. **Impact** — what the attacker actually gets. "They learn field names" or "they cause an error"
   is LOW at best.
3. **Baseline** — whether the comparable has the same pattern, and if it has never been exploited
   there, why.
4. **Mitigation** — whether another layer prevents it: middleware, a database constraint, a
   framework default.
5. **Parser and runtime behaviour** — where the exploit depends on how a parser or runtime handles
   an input, verified against the spec or a real run, never reasoned from intuition. The most
   convincing false positives are built on "the parser will interpret this as".

Kill false positives aggressively without killing real findings. Three real findings are worth more
than thirty theoretical ones, and an honest "nothing found" is a valid result — after pushing hard.

## Find The Smallest Fix Before Proposing One

Establishing that a vulnerability is real is not the same as knowing what should change, and the two
get conflated: the trace ends at a sink and the remediation is written for the sink. That reliably
produces a fix at the wrong altitude — new machinery guarding a hole a value already in hand would
have closed.

Ask in this order:

1. **Is a guarantee already available that the code fails to read?** A provider's response carries a
   verification flag, a signature, an expiry, a scope; a platform enforces a constraint the schema
   never declares; a library offers the check hand-rolled here. Asserting an existing guarantee is
   nearly always smaller than building one, and it turns a promise the code merely assumes into
   something it states. Look here **first** — it is the case most often missed, because a trace
   ending at our own sink never points at the dependency's own answer.
2. **Does the exposure exist because the surface exists?** A route, a fallback, an optional field, a
   mode nobody uses: deleting it closes the finding outright and leaves nothing to maintain or
   bypass.
3. **Does a product decision dissolve it?** Requiring an invitation, dropping an unused affordance,
   narrowing who a feature serves. That decision is not the auditor's, so the finding carries it as
   an option for whoever decides, priced honestly against the code fix — never silently taken and
   never silently dropped.
4. **Only then, new enforcement.** A guard, a policy object, a claim check, a schema change.

**Report the alternative whenever it is materially simpler, even when it is not the one recommended.**
Materially simpler means fewer moving parts a reader has to hold: fewer new symbols, no new
abstraction, no migration, no new failure mode. State each option's real cost — the product
constraint it imposes, the flow it forbids — so the user is choosing rather than ratifying. A
remediation offering one option when a smaller one exists has made a design decision on the user's
behalf and hidden it inside a security finding, where it is least likely to be questioned.

State the condition the exploit rests on in the finding itself, and keep it attached in every
retelling. A finding whose conditions include "the provider must permit X" is describing a guarantee
the code does not assert — usually both the honest severity **and** the smallest fix, and both are
lost the moment the condition is dropped.

## Anti-Patterns

These are what make a security audit useless:

1. **Listing every deviation from a checklist as a finding.** A checklist is not a bug list, and
   every real application makes tradeoffs.
2. **Rating defense-in-depth gaps as HIGH or CRITICAL.**
3. **Ignoring the deployment model.** Rate limiting at the edge is a valid architecture; not every
   application needs it in the application layer.
4. **Treating designed behaviour as a bug.** Understand the trust model first. Where the design says
   admins are fully trusted, an admin doing admin things is not a finding.
5. **Padding with LOW findings to look thorough.** Ten LOWs do not make a useful report; three
   MEDIUMs do.
6. **"Potential" findings without proof.**
7. **Ignoring what the codebase does well.** Where the authentication is solid, say so — it builds
   trust in the findings that are reported and helps prioritize.
8. **Constructing exploits from incorrect parser or runtime assumptions.**
9. **Skipping business logic and creative attacks.** The standard classes are what every scanner
   checks; the value of a manual audit is what scanners cannot find — logic errors, state-machine
   violations, chained attacks, implicit trust assumptions.
10. **Giving up too easily.** "It uses parameterized queries so there is no injection" is a lazy
    conclusion. Check every raw query, every dynamic identifier, every search path, and every code
    path that bypasses the builder. Push.
