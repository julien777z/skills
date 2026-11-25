# Reader Dispatch

How a skill-test reader is isolated and dispatched; read from **Workflow** step 2 and **Reviewer selection** in `SKILL.md`.

## Reader isolation

**A reader sees only the variant it tests, and the variant reaches it only as that run's input.**
Launch the reader as a local headless harness process the running session starts and waits on,
every user-level skill and rule root it is given set to an empty scratch root, and pass the
frozen variant through an option that adds a source for that one run, such as a plugin
directory, an appended system prompt or an input file the run reads. An option that sets where
the harness reads user-level skills or rules is a user-level root whatever folder it names, so
the variant never goes in one, in a folder one points at, or in any folder searched by default.
A subagent of the running session stands in only when its loaded guidance lists no copy of a
skill or rule under test, with the variant in its brief. Record the route, the command, the
scratch root's file list with digests, and the harness's record of the guidance it loaded. With
neither route, the round is a concrete gate, surfaced with its evidence and saved next action;
it never passes with a reader that saw another variant.

## Reviewer selection

Only after a host receipt explicitly
rejects the standard capability level's exact identifier as unsupported, select the next permitted lower mapped capability,
resolve its exact identifier, and launch the actual reader assignment. Advance again only after that candidate
receives its own explicit unsupported receipt; never move upward or inherit the orchestrator's model. This
fallback applies to this skill's default, never against the user's explicit model or capability constraint. A
`dispatch required` result with an exact identifier launches the actual required reader set. When a
required reader, scenario writer or grader cannot launch, apply `subagent-matrix`'s launch
fallback for its assignment.

Classify a rejected reader dispatch from the host receipt. Only a receipt establishing that the
requested capability or model is unsupported makes it unavailable for that attempt and permits the
fallback to a lower capability level. Retry a transient, concurrency, timeout, or unknown rejection once with the
same resolved selection; do not lower the comparison's capability level. When no required reader launched, retry
the required reader set. When one required reader launched, wait for its terminal report and retry
only the rejected or unattempted required counterpart, never a duplicate of the accepted reader.
When that retry cannot complete the required set, record its receipts and apply `subagent-matrix`'s
launch fallback for the missing assignment. Record every failed attempt separately from reader-run evidence,
including every required reader's receipt; grade and retain each run that completed, and withhold
the comparison and the passing verdict until the required set completes. When an unsupported request has a permitted fallback, wait for any accepted counterpart's
terminal report, record the incomplete attempt, then launch a fresh required set. When no permitted model fallback remains, record the rejection and apply `subagent-matrix`'s launch
fallback for the missing assignment.

Run each scenario's edited reader, and its original control only where **When It Runs** requires
one, with the same resolved model and reasoning effort where both run. Record
the catalog state, requested capability and family, exact dispatch identifier, resolved reasoning
effort, selector resolution, and accepted actual-assignment dispatch receipt with those explicit
parameters in each run's evidence entry. Record catalog state separately
from assignment state: a catalog-hidden family is `dispatch required` until its exact identifier is resolved
and the assigned worker accepts it, then it is `accepted`; a missing identifier triggers the launch
fallback and is not an unsupported-model receipt. Selector resolution retains an explicit unsupported request,
the exact fallback capability and dispatch identifier when one is permitted, why that fallback was selected,
and any explicit user override. Record the runtime-identity and runtime-label evidence as
`subagent-matrix`'s **Workflow** defines. Follow the selector's dispatch instructions.
