---
name: incident
description: "Restore a broken deployed service using a browser and the repository's deployment skill as needed, deploy and test a fix branch, and merge scoped fix pull requests after one Bugs and Simplification review round. Invoke as /incident when something is down, degraded, stuck, or has to be working now."
disable-model-invocation: true
---

# Incident

## Dependencies

- `chrome:control-chrome` — reproduce and verify browser-visible failures in connected Chrome.
- `code-review` — supply the Bugs lens and finding validation.
- `code-simplify` — supply the Simplification lens rubric.
- `acceptance-gate` — filter findings and judge fixes against the recovery's intent.

A deployed service is broken and the only thing that matters is getting it working. Ordinary
delivery habits — asking before looking, waiting for a suite, waiting for a merge — each add a
round trip, and a service stays down for the sum of them.

## Opening The Run

The invocation carries no argument. Read what the incident is out of the session itself and state it
first, in four lines:

- **What is broken**, in one sentence a reader who was not here would understand.
- **Which environments**, named. One, both, or all of them; a staging-wide fault affects every
  environment on it.
- **Since when**, and how that is known.
- **What restored means**, concretely enough to be checked: every affected environment back in its
  intended state with nothing the incident involved still in flight. A finished migration and an
  active release, a rollout landed, a provider or DNS record or bucket or certificate working again
  and the services above it serving. A health endpoint answering is evidence, never the definition.

That statement is the scope of everything below. An authorization here reaches the environments and
apps it names and nothing else.

Never open a run without the invocation. Where the session shows a service is down and no `/incident`
was typed, say so in one line and offer it; the user declares an incident, the agent never does.

## Persistence

One invocation covers the whole recovery, not one action. It holds across turns and across
unrelated interruptions until the restored condition in the opening statement has been checked and
the agent reports recovery complete, or the user says "incident over" or "normal mode". A completed
code change, a green suite, an open or merged pull request, and a fixed narrow symptom do not close
the run.

Reporting recovery complete closes the invocation and ends its deployment, publication, monitoring,
and merge authorization. That statement is valid only after every opening restoration condition has
been verified from live state. Before using incident authority, check the most recent recovery status
in the conversation.

A later user message that identifies an unchecked or unresolved opening condition resumes the same
incident, even after an erroneous completion statement. Restate the environment, the outstanding
condition, and the next recovery step, then continue under the original authorization. A fresh
invocation is needed only after a valid closure.

An active incident has no final-response or handoff checkpoint. Do not end the task, emit a final
response, or leave a continuation prompt while any restoration condition is incomplete. Keep
executing the recovery in the same turn and use commentary only for progress. Only a valid closure
under this section permits a final response.

Follow-up bugs, product changes, review findings, and requests to update this skill are ordinary
work after a valid closure. They do not reopen the incident, even in the same thread or environment.
Apply ordinary authorization to follow-up pull requests and deployments, and leave pull requests
open unless current user instructions or another explicitly invoked skill authorize their merge.

Restate at the top of every turn: the environments, since when, and the step in hand. A reader
arriving mid-recovery needs no scrollback.

When it ends, say so in one line and return to the ordinary posture for the tidy-up.

## Act, Do Not Ask

Do these without asking, and report what they showed:

- Read any log, app spec, deployment status, workflow run, check run, database status or metric.
- Update an app spec on an app the opening statement names, when the change is a value already known
  or derivable from the repository, another app, or the failure itself.
- Deploy from the branch carrying the fix, and point runner or worker apps at the image it builds.
- Resize an instance temporarily to isolate a cause or finish work faster.
- Add debug logging to the service to isolate a root cause.
- Re-run, cancel or dispatch a workflow.
- Fix, commit and push a change the plan or the diagnosis already covers.
- Create or reuse the pull request carrying the fix.
- Use connected Chrome in agent-owned tabs to reproduce and test the affected flow.
- Merge scoped fix pull requests after **One Review Round** completes and live verification succeeds.

Stop and ask only for: a secret the user holds, a destructive action (deleting or truncating data, a
bucket, an app, a database, a cluster), a product decision, a spend that is not temporary, and a
pull-request merge outside the authorization below. An explicit user restriction, including an
instruction not to merge, always wins.

"Do you want me to check the logs" is the failure this skill exists to prevent. Yes.

## Cadence And Check-Ins

This section is the whole of the polling permission, and it lives here rather than in a rule. It
reaches only an active run of this skill and only the environments the opening statement names;
the repository's **Background Timers And Self Check-Ins** rule governs everything else, including
this session before the run opens and after it ends.

- **A step expected within about thirty minutes**: arm one check-in at a time, five to ten minutes
  out and never under two, saying what it watches and what it will do when it fires. When it fires,
  read the state, act, and arm the next one only if the step is still in flight.
- **Work expected to take hours** — a large migration, a long backfill, a slow rebuild: arm nothing.
  It is checkpointed or it is not, and either way a check every few minutes costs the user's budget
  and tells nobody anything. Read the durable state when the user asks or an event arrives.
- **Never a tight loop.** No `sleep` under two minutes, no repeated status call in one turn.

Estimate the duration from what the thing actually does — the rate a previous pass ran at, the size
of the work left — not from impatience. Say the estimate out loud when arming, so a wrong one is
visible.

## Tests And Checks

The repository's testing rule and `run-tests` order the suite for ordinary delivery: one run at the
end, after the push, over a tree that has stopped changing. An active run suspends that ordering,
because the tree changes with every diagnosis and the service is down the whole time.

- Before restoration: run only the tests the fix's diff reaches, and only when they finish in minutes.
- A green check run is not a gate on deploying. Deploy the branch and let the checks catch up.
- Do not run, investigate, or fix lint, formatter, Pyright, or other static-analysis findings during
  recovery. They neither establish nor block restoration, and belong to ordinary delivery work after
  the incident ends.
- A red test the diff does not touch is noted in one line and left alone.
- After restoration, declare the incident complete from the live restoration checks. Resume ordinary
  delivery validation afterward; it does not delay recovery or its report.

## Deploy From The Branch

Create or reuse the fix's pull request before deploying repository changes. Record each affected
component's original repository, branch or image source, and any temporary setting before changing
it. Keep credentials out of that record.

Build and publish release images through the repository's GitHub Actions workflow, never locally.
Use the exact fix branch and only the authorized environments. Add scoped preview publication to
the workflow when needed, keeping publication separate from deployment submission for testing.
Verify the workflow's terminal result and image revision before deploying.

Point Git-backed components at the testing branch and image-backed components at the GHA images built
from it. Change only the components the fix affects, preserving unrelated app configuration.
Follow deployment through activation, inspect component health and relevant logs, and test the
original failure directly. For browser-visible behavior, use connected Chrome and the actual user
flow; a healthy deployment or passing suite does not substitute for it.

## One Review Round

Every incident recovery gets exactly one Bugs and one Simplification lens, whatever the failure or
the remedy: application code, configuration, deployment, or infrastructure. Review each scoped fix
pull request's complete diff; when recovery changes only live settings, review the redacted before
and after configuration and the operations performed. Do not invent a code change or pull request
for an operation with no repository change.

Use `code-review`'s finding validation and the full `code-simplify` rubric. Apply `acceptance-gate`'s
filtering and fix dispositions without duplicating its rubric here. Both lenses must finish; resolve
accepted findings, verify the corrections, and run affected checks. Apply final acceptance when
the gate's intent rules call for it, respecting its bounded rewrite and escalation rules.

This is a single round, not the ordinary code-review workflow: do not launch the other lenses,
restart the cohort after fixes, require consecutive clean rounds, or enter its fix-triggered
re-review or Rules-lens loops. Targeted verification of corrections and recovery changes remains
part of finishing the round. Report what the lenses reviewed and what was verified after them;
never claim that changed material was covered by an earlier receipt.

An invocation authorizes merging the scoped fix pull requests once this round is complete and live
verification succeeds, without another approval. A round with failed or incomplete coverage,
unresolved accepted findings, a blocking gate verdict, or failed affected validation is unfinished
and authorizes no merge. Stop for a real blocker rather than starting another round or bypassing it.

The authorization reaches only the pull requests carrying the declared recovery, not unrelated
work, a parent pull request carrying other features, or replacements and reapplications after a
corrective revert. An explicit no-merge instruction keeps those pull requests open.

## Restore Deployment Sources

Before closing recovery, restore the recorded deployment branches and temporary settings. If the
previous branch cannot be established or no longer exists, use the repository's live default
branch. For image-backed components, publish and deploy the fix from the restored source rather
than restoring an image that contains the fault.

Confirm that the restored source includes the verified fix before switching, then verify activation,
component health, relevant logs, and the original flow again. Do not report recovery complete while
restoration is still in flight or would reintroduce the fault.

If the user withholds merging, keep the verified testing deployment active and report the open
pull request and pending restoration. Do not merge, discard the fix, or restore the broken source
to satisfy the closing checklist. If the user explicitly ends the incident, report any temporary
state still active and the reason it remains.

## Deployment Operations

An invocation authorizes the browser and deployment operations needed within the opening scope;
neither needs a separate invocation or repeated permission. An active run carries the operations of
the repository's deployment skill directly, when the skill listing declares one, and otherwise the
hosting provider's own API. That skill's guardrail asking for confirmation before every mutation, and
its sentence putting deployment monitoring in a separate request, are both suspended for the apps the
opening statement names. Watching a rollout to restoration is the work.

- **Read a log** by fetching the live log URL the logs API returns, rather than shelling out to it.
- **Read deployment status** for phase, component health and the failing step's message. Treat
  `BUILDING` and `DEPLOYING` as distinct, and an automated rollback as a failure with a message to
  read rather than a state to wait out.
- **Update a spec** with the full spec the API demands. Resubmit every existing `EV[...]` value
  verbatim for that same app. Never copy an encrypted value between apps, and never echo one.
- **Show the redacted diff as progress**, not as a question.
- **Record a temporary resize** in the plan file with the value to restore, and restore it once the
  environment is back.

## Instrumentation

Adding logging to isolate a cause is ordinary work here, not a detour: a fault nothing reports is a
fault nobody can fix, and the disclosure is usually the fix's first half.

Before the pull request carrying it is called done, each addition either becomes instrumentation the
service keeps, with a test, or comes out.

## Never, Incident Or Not

- Push or commit to the default branch.
- Merge outside this invocation's bounded authorization or against an explicit user restriction.
- Delete or truncate data, or drop a column an approved plan does not already drop.
- Write a secret to a log, a commit, a pull request, or chat.
- Skip, disable or quarantine a test to get a check green.
- Report something as working that has not been read from live state.

## Closing The Run

Closing is a check, not a feeling. Against the opening statement, read from live state:

- Every affected environment in its intended state, and nothing the incident involved still in
  flight.
- The deployment active and every component healthy.
- Whatever the statement named as the fault working again, tested directly.
- The service log read for the first minutes after activation, not just at activation.

The report names each check, the single review round's findings and dispositions, and the restored
deployment sources. A check that could not be made is named as such, never implied. Once restoration
and its verification are complete, say the run is over and finish the ordinary delivery work the
recovery deferred.
