# Acceptance Gate Rubric

What the gate judges by: why it exists, what the intent statement and a verdict must contain, how
worth is priced, and the tests behind each question. `SKILL.md` says how the gate is run. The gate
also borrows two rubrics it does not own: `code-simplify`'s, which defines slop and prices a
mechanism, and `security-audit`'s, which defines an exploitable finding and its remedy.

## Why The Gate Exists

An agent that has decided a fix is owed, a deferral is justified, an issue is worth building, or a
base merge is done is the worst judge of whether the result reintroduces what its own change removed
or costs more than it buys. The fix reads as correct because the rule it breaks is the one the change
is still establishing, a deferral reads as prudent because nobody has yet asked whether the work was
small, and a finding reads as urgent because nobody has asked whom it protects. Every question below
is one the author would answer in its own favour, so a different subagent answers it.

## What The Intent Statement Names

Ground intent in the user's accepted requirements, the change's history, and the current diff.
The statement names:

- the required behavior and ownership boundaries, with the accepted requirements that establish them;
- the shapes removed and their replacements, read from current deletions and the originating commits;
- the pull request's title and body, checked against those requirements and the implementation.

Read deletions before additions, but do not treat an empty deletion set as an empty intent. A file
added and removed within the branch disappears from its final diff without cancelling the ownership
decision that removed it. Preserve that decision until the user changes it. When inputs disagree,
resolve them against the accepted requirements and history instead of silently narrowing the scope.

## Product State

Worth is judged against product state declared by the target repository's project guidance, and the
gate takes those facts as given: who the users are, how many people hold the site-wide admin role,
whether a production environment exists. Never infer missing product state or import it from another
repository. A safeguard is worth what it withholds from somebody who can be on the wrong side of it;
where the product state puts nobody there, the safeguard protects nothing today, and the fact that
would change that — a second admin, external users, a production deployment — is the reconsideration
criterion its record carries. Product state bounds who can be on that wrong side; it never decides
whether an exploit counts, which **Exploitable Findings** settles.

Two things never count as product state. The deployment's dimensions — row counts, instance size,
traffic — are facts about today's environment, and repository guidance must bar them from every
design argument; a mechanism that cannot grow is a defect whatever the current table holds. And a defect is
never weighed at all, because a broken behaviour has no gain side to price.

## What A Verdict Names

It returns the verdict its question defines: **accept** or **flag** for every question but triage,
and one of triage's four dispositions there. Every verdict is specific. Acceptance names, for every
addition whose kind matches a removed shape, the addition, the shape it takes, and why that is
neither the removed shape nor a finding under the rubric; additions of other kinds are summarised.
"Looks reasonable" is not acceptance. A flag names the lines, the shape they take, the intent item or
rubric item they violate, and the remedy the change itself would take — narrow the model rather than
subtract from it, derive the set from the declaration that carries it, extend the mechanism the
change introduced. A disposition names the test that decided it and the fact it rests on.

A finding confirmed by a review that refutes everything it can is evidence that the problem is real;
the gate does not re-validate it.

## Exploitable Findings

Every question that reads a diff — diff, final acceptance, base incorporation — also reads it for
what an attacker can reach, whenever the diff changes code the repository executes: source, the
configuration that grants access, a dependency manifest, a workflow. Prose, documentation and agent
configuration are not that, and a diff confined to them skips this section entirely.

The criteria are `security-audit`'s `references/rubric.md`, and they cut in both directions.

- **Only what can be exploited.** A finding names the attacker, what they send, and what they get.
  "Theoretically" and "potentially" mark the place where the work stopped, not a finding.
- **A defense-in-depth gap is not one.** Where a layer the diff leaves in place already prevents the
  attack, the absence of a second layer is a hardening note under `Also read`, never a flag, and
  never inflated to carry one.
- **Severity is likelihood and impact together, and the flag bar is medium.** A targeted exploit with
  real consequence, a state change an attacker can force, a disclosure of secrets or credentials, a
  business-logic bypass whose blast radius is real: each is a flag. A finding that defeats an
  explicit security boundary — an action the system gates behind a role, performed without it — is a
  flag with the boundary named. Below that bar it is a hardening note. If the concrete damage cannot
  be described, the severity is lower than it looks.
- **The remedy is found in `security-audit`'s order, not written for the sink.** A guarantee the code
  already has and fails to read, then the surface whose deletion closes the finding outright, then a
  product decision that dissolves it, and only then new enforcement. A flag that names new machinery
  where a value already in hand would have closed the hole is at the wrong altitude, and naming the
  smaller option is part of the flag even when it is not the one recommended.

An exploitable finding also reaches triage and admission, which are not diff questions: the fix
test and the close test each carry the clause that keeps it, and **Product State** carries the bound.
Having no released users empties the attacker set only where the repository's guidance says the
deployment is unreachable; where that guidance puts it on a network others can reach, the product
having no users of its own does not mean it has no attackers.

**A clean read here is not an audit, and never reports as one.** The gate reads a diff with three
read-only tools and answers one question; it cannot fan out, follow a data flow across a codebase, or
try to disprove its own finding. A verdict that raises nothing says the diff's added lines carried no
exploitable finding the gate could see. Only the `security-audit` skill, run at a level that fans
out, says anything about the codebase.

So a shape the gate can see but cannot chase to an attacker is not dropped: name it under `Also read`
and recommend a `security-audit` run over the surface it sits on. That is the gate declining to guess,
not the gate finding nothing.

## The Tests Behind Each Question

**Triage — what should happen to this?** The item is an issue, a finding, or a proposed record, and
the answer is one of four dispositions, decided by the tests below in order. The first that holds
ends the question.

1. **fix** — the item is a confirmed defect. A defect is anything the system does that a reader would
   call broken. Wrong output, a lost write, a lost notification, a crash and an exhausted budget are
   its familiar shapes, not its boundary. Work the system cannot finish in useful time, a resource
   that grows with the data with nothing to bound it, a stored value nothing limits, work a restart
   throws away where a sibling phase keeps its place, and a job that only advances because a
   container happens to stay alive are defects of exactly the same standing. "The result is still
   correct", "it only costs time" and "how much to keep is a policy question" describe a defect; they
   never exempt one — a system that is right and too slow to use is broken. Measured evidence from a
   live run — a rate, a duration, a memory trail, a kill — is evidence of a defect the way a
   confirmed review finding is: the gate takes it as given and never re-derives the defect from the
   tree, because a tree read alone cannot see a rate. A defect is fixed in the change in flight, or
   on a branch off the default when nothing is in flight, whatever its size and whatever shape its
   fix takes. A migration is how a fix is written, never a reason to record it instead. A check that
   would rediscover the defect does not soften this: rediscovery excuses the record, never the fix.
   Product state never softens it either: broken is broken for one admin as for a thousand users.
   A missing safeguard is not a defect — the system does what it was built to do, and the question is
   whether it should do more — so it goes on to the tests below. The exception is a safeguard whose
   absence is an exploitable finding under **Exploitable Findings**: what the system does includes
   what an attacker can make it do, so that is a defect here and is fixed in the change in flight.
2. **close** — the item is real but not worth doing. Either the product state leaves it protecting or
   serving nobody — an access control between the one admin and the data only that admin can see, a
   hardening against users the product does not have, neither of which retires a finding an attacker
   the product does have can still reach — or something in the repository rediscovers
   it on demand, a doctor's lens, a lint or type rule, a structural test, so that running the check is
   the pickup and a record would be a second copy that goes stale. A close names the fact it rests on
   and the reconsideration criterion: the product-state change that would make the work real, or the
   check that owns it.
3. **defer** — the item is worth doing, and one of these holds: the gain today does not carry the
   mechanisms the fix would add, priced by the rubric; the work is of genuine size and its need is
   arguable — a redesign, a sweep across many files somebody could reasonably decline; an external
   blocker stands, which is something outside the repository the fix cannot be written without — a
   credential nobody has issued, a vendor change, an answer only a third party can give; a decision
   that is somebody else's is already put to that person and still open, or the user declined it in
   the current request; or an attempted fix, shown to the gate, could not be completed without the
   removed shape or a rubric finding. That the code under change is deployed or running somewhere, a
   backfill in flight on live data included, is the order the fix rolls out in, stated in the pull
   request; it is never a blocker. The gate never routes work to a decision on its own: where a fix
   has a product dimension, the change takes the cleanest fix and states the trade-off in the pull
   request, or the fork is put to the user now, never filed as theirs unasked. A defer also requires
   that the record's resolution criteria describe an end state and name the intent a fix has to
   preserve, never a mechanical condition a relocated shape could satisfy.
   Size is not that arguability and never stands in for it. The test is a question somebody could
   answer differently, so a conversion repeated across a hundred call sites is long rather than
   arguable and the number of files it touches decides nothing. Nor are the size and shape of the
   work inputs the gate may take on trust: "large", "not mechanical", "each site needs its own
   judgement" and "it spans suites the change does not touch" are the asker's characterisation of
   the asker's own record. Check the count against the tree and open enough of the actual call sites
   to see whether the edit repeats. This is the inverse of the fix test's treatment of a measured
   rate, which is taken as given precisely because reading the tree cannot produce one — size is
   exactly what reading the tree can.
4. **do** — none of the above: the item is worth doing and its cleanest fix is within reach, so it is
   done in the change in flight, or on a branch off the default when nothing is in flight.

**Admission — may this work be deferred?** The triage question asked of a proposed record. The
answer is accept when triage's disposition is defer, and otherwise a refusal naming the disposition
that applies: fix and do send the work into the change in flight, and close records the decision as a
cancelled record with its reason and reconsideration criterion. An explicit user instruction to
defer settles the defer test's justification; the gate still answers the fix test, confirms the problem
is real from the current tree or measured evidence, and checks that the criteria describe an end
state. A record whose attempted fix carries two gate flags is admitted on that evidence with no
further question.

**Proposal — should this be written?** Does the plan solve the problem without reintroducing what
the change removed, without a shape the repository's rules or the rubric ban, and at a cost its gain
carries? A plan that builds a mechanism beside one the repository or a dependency already has, or
whose size the problem does not need, is flagged with the smaller shape named as the remedy, however
cleanly it is written. The plan states what is added, moved, and deleted, and which existing shape
each choice reaches for.

**Diff — should this stand?** Does the finished diff do what the accepted proposal said, and nothing
in the removed shape?

Four shapes the diff question reads for on every change, because a fix written after review takes
them most easily: a reader that reaches through a lookup table keyed by a model for a fact the model
could declare on itself — `TABLE[model].label` in an added line is the finding even when the table
predates the diff — a repository-wide fact kept as loose strings inside one consumer instead of a
typed owner in the shared package, a container declared for one member — a router carrying one
handler, whose handler belongs on the router that owns its resource — and a data-holding class
declared outside a model-owned module. Only a Pydantic `BaseSettings` class belongs in
configuration; registries, manifests, policies, provider payloads, and response schemas remain
models. All four are the greps code-simplify opens with; the gate runs them over the diff's added
lines and lists their hits before anything else.

**Base incorporation — what did the base bring in that the change must refactor?**

- **Disposition.** The verdict names each incoming implementation matching the intent and its demonstrated
   disposition: consolidated, replaced, adopted, or retained behind an actual responsibility or
   dependency boundary. **Adopted** is the incoming implementation judged the better of the two, with
   the change's own shape dropped for it; the change is not privileged because it is the caller's. A
   retained name, filename, or origin in the base proves no boundary. Distinguish older ownership gaps
   found in surrounding code from incoming-base findings; both keep their real origin.
- **Comparison.** Where the base answered a question the change also answered, the verdict names which
   implementation was judged better and the evidence: which leaves fewer mechanisms for one concern,
   which removes duplication the other invites, which failure modes each has already produced in this
   tree. **Flag a resolution that states no comparison, and one whose only stated reason is that the
   incoming shape is one the change removes** — that reason is available in every collision and always
   points the same way, so it records no judgement. Arrival order is not evidence in either direction.

**Final acceptance — may this merge?** The item is the complete pull-request diff against the intent
statement and the rubric, read once after review is clean and before any check gate.

## The Gate Is Never Advisory

The gate is never advisory. A proposal it flags is not written; a diff it flags does not stand,
except that a second flag on a change confined to agent configuration leaves the disposition with
the caller, as **Bounds** says; a disposition is carried out by the caller — a fix or do goes into
the change, a defer is recorded, a close is recorded cancelled. What a disposition names as the
user's — an open fork the gate found unasked — is put to the user, and nothing else about it is.
