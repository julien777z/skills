---
name: linear
description: Create, find, and update Linear issues through the available Linear integration with dynamic team, workflow, project, and label discovery. Use when another repository workflow records or resolves work in Linear, or when the user asks to manage Linear issues.
---

# Linear

Manage Linear issues without assuming a workspace, team, project, workflow name, or label taxonomy.

## Preflight

Before choosing Linear as a durable store, use read operations to confirm that the integration is
present, authenticated, and authorized. List the accessible teams, workflow states, projects, and
labels needed for the operation.

Resolve the team in this order:

1. an explicit team supplied by the caller;
2. the team of a confidently matched existing issue for the same repository and concern;
3. the only accessible team.

When multiple candidates remain, ask the user. Never guess from a repository name. Resolve workflow
states from an explicit caller choice or by category, such as started, completed, or canceled,
rather than hard-coding a state name. Use a sole category match; ask before writing when several
states share the requested category. When an explicit state or required category has no accessible
match, ask for a correction and do not write.

Resolve a project only when the caller requires one or a confidently matched issue establishes it:

1. use an explicit project supplied by the caller;
2. otherwise retain the project of a confidently matched issue;
3. otherwise use the sole project whose name and description clearly own the work.

Ask when a project is required and zero or multiple candidates remain, and do not write until it is
resolved. Leave the issue unassigned when a project is optional and no confident owner exists; never
guess merely to populate the field.

If the integration is absent, unauthenticated, unreachable, or lacks access before any write, return
an unavailable result so the invoking skill can use its declared fallback. A missing or ambiguous
required team or label is a configuration decision, not unavailability: ask instead of creating a
label, choosing a near match, or silently falling back.

After one Linear write succeeds, Linear owns that record. Retry or report a later failed update;
never create a second repository record for the same work. Treat a create whose outcome is unknown
as a possible successful write: reconcile it with bounded searches by repository and stable key
before retrying. If ownership remains uncertain, report the blocked create and do not create again
or use the repository fallback.

## Find Before Creating

Search before every create. Include active, completed, canceled, and archived issues whenever the
integration supports those filters. Treat repository plus stable record key as strong identity. Use
an exact origin or resolution pull-request reference only to locate candidates because one pull
request may track several records; require the same stable key or corroborating source, affected
surface, and root cause before matching one. Report multiple PR-linked candidates as ambiguous.
Required labels and title are additional evidence, but title similarity alone is not a duplicate.

Reuse a confident match and update missing current context. Do not reactivate a completed or canceled
issue without an explicit disposition that justifies it. Report ambiguous candidates instead of
creating another issue.

## Labels

Read the available labels and their descriptions, then apply the existing labels that best describe
the issue. Do not embed label names in this skill, create labels without approval, or substitute a
nearby label for an exact label required by the invoking workflow. Respect label-group exclusivity
and omit an optional label when no confident match exists.

## Issue Contract

Write an actionable title and a concise description containing the problem, evidence, affected
surface, resolution criteria, and known blocker or proposed correction. End every managed issue with
this searchable metadata block, preserving the field names exactly:

```markdown
## Agent tracking

- Source: <invoking-skill>
- Repository: <owner>/<repository> | none
- Record key: <stable-key>
- Origin PR: <#number | none>
- Resolution PR: <#number | pending | none>
```

Resolve repository identity from authoritative change-request metadata or an unambiguous hosted
remote, never a local directory name. Ask when forks, multiple remotes, or transferred repositories
leave ownership ambiguous. Direct repository-independent work uses `Repository: none`; a
repository workflow must resolve its repository before writing. The caller supplies a stable record
key; for a direct request without one, agree on a concise key before creation rather than inventing
identity from the title. Use `Source: direct-linear` for a direct request.

A source pull request is the change during which the work was found; a resolution pull request is
the change that completes it. Use `pending` only when one is expected but not open, replace it
immediately after that pull request opens, and use `none` when resolution does not involve a pull
request. When no origin pull request exists, keep `none` truthful and use the resolution pull request
for later lookup when one exists.

Add factual progress or disposition context to the issue before changing its workflow state. Use a
completed-category state only when the invoking workflow says its completion condition is met.

## Cancel Or Delete

**Cancellation and deletion answer different questions.** Cancelling says the work was real and the
team is not doing it; deleting says the record should never have existed. Reaching for cancellation
in both cases fills the ledger with entries a reader has to re-litigate before dismissing, which is
the cost the wrong disposition imposes on everyone who reads it later.

- **Cancel** work that is genuinely a thing to do and is being declined, deprioritized, or left for
  another time. A canceled issue keeps its reason and its reconsideration criterion, because someone
  may well pick it up.
- **Delete** a record that describes nothing: one opened by mistake, a duplicate, a finding that
  turned out to be wrong, or work already done or made irrelevant by a change that has since
  landed. There is no reason to preserve it and nothing to reconsider.

Judge by whether the issue still describes real work, never by how it feels to remove one. An
accidental record left canceled is not tidier than a deleted one — it is a claim that somebody
weighed this and declined it, which is untrue.

Deletion is the one disposition the integration may not expose. When no delete operation is
available, say plainly that the record should be deleted and why, and ask the person to remove it
in Linear. Do not cancel it as a substitute and do not describe the result as deleted: report what
the record's state actually is. Never claim to archive an issue manually.

## Report

Return every issue read, created, reused, or updated; its identifier and URL; the labels and workflow
state applied; and any ambiguity, unavailable operation, or pending metadata update.
