---
name: reconcile-tailscale
description: Reconcile all affected consumers when changing Tailscale policy, tags, services, routes, OAuth clients, credentials, or their runtime and automation references. Run before mutation; the repository where a symptom appears never bounds the consumer inventory. Verify every affected execution surface before retiring shared authority. Every encountered Tailscale failure triggers causal guidance diagnosis through edit-skill while the operational repair continues.
short_description: Reconcile Tailscale authority and every affected execution consumer.
---

# Reconcile Tailscale

A shared security dependency is changed only with its affected consumers accounted for. Source
configuration, credential identity, deployed environment and automated runner are separate parts
of that proof; agreement in one never establishes agreement in another.

## Dependencies

- `coordinate-repositories` — discover and deduplicate the bounded repository collection, preserve
  unrelated work, and deliver each applicable repository.
- `edit-skill` — diagnose every encountered Tailscale failure while operational repair continues.
- `proton-pass` — retrieve only the credential fields a required operation needs without exposing them.

## Workflow

1. Establish the authorized outcome, environments and mutation boundaries. Apply the global
   Tailscale policy for naming, groups and tag ownership. Discover each repository's deployment
   procedure and configuration owner from its project guidance. This procedure reconciles a
   Tailscale change; a general configuration audit remains owned by `config-doctor`, which runs
   only when directly invoked. Reading a deployment procedure supplies its read-only inspection
   route and never authorizes a rollout.
2. Invoke `coordinate-repositories` for its bounded discovery and normalized-remote manifest.
   Inspect every unique repository's current remote configuration before deciding applicability;
   include consumers beyond the repository where the symptom occurred. Retain multiple execution
   surfaces under one repository row rather than treating duplicate worktrees as consumers.
   Augment that manifest with live deployments, nodes, services, and automated runners reached by
   the changed authority, including live consumers with no matching source declaration. Keep
   discovered consumers outside the authorized scope visible as unresolved boundaries; obtain
   the required authority before changing them, and do not retire a dependency they still use.
3. Read current tailnet policy and live resource and OAuth metadata. Trace both directions from
   each changed dependency: its producers and every consumer it authorizes, and each consumer's
   required operations back to the authority supplying them. Record groups, tag owners, grants or
   ACLs, service and route permissions, OAuth scopes and permitted tags, and the credential identity
   each operation actually uses. Check current provider documentation for the operations under
   change rather than assuming a tag or scope implies another permission. For routed traffic,
   distinguish access to the router device from permission to use its routes. Exit-node use
   requires the caller to reach `autogroup:internet`, with `via` restricting the permitted exit
   nodes where appropriate; a grant to the node itself does not provide that access. Evaluate
   tagged runner identities separately from people: user-group grants do not authorize them.
4. Map each OAuth client ID to every execution consumer and its credential reference. Inspect
   source settings, manifests, deployment specifications and effective runtime references, plus
   organization, repository and environment secrets and workflow bindings used by automation.
   Record environment and component or job names, setting names, secret-reference locations and
   client IDs, never secret values. A secret name proves a reference, not the identity it contains:
   use provider metadata or minimal private credential access through `proton-pass` to establish
   identity when needed. An unreadable consumer or unknown identity remains unverified, never
   absent. Do not dump complete environments, secret stores or credential-bearing payloads.
5. Choose the target authority from each consumer's required operations and environment boundary.
   One shared OAuth client and separate clients per environment are both valid when their scopes
   and permitted tags provide least privilege for the authority they hold. Use separate clients
   when sharing would grant a consumer authority belonging to another environment; retain sharing
   when the authorized consumers need the same authority. Do not prescribe either topology from
   the incident. Reconcile policy, service and route ownership with the chosen identities without
   broadening permissions merely to make a failed operation pass. Surface any unsettled security
   choice before applying it while continuing independent authorized work.
6. Prepare the replacement authority and a cutover sequence that keeps required consumers working.
   Update every affected consumer within the authorized scope through its existing configuration
   and credential owner: canonical source, live runtime bindings and automated runner references
   alike. Preserve unrelated configuration and work. Follow each target's deployment procedure
   and action-time approval requirements; a prepared source change or secret update is not a
   deployed cutover. Keep every affected consumer on the manifest until its resulting execution
   state is read back and verified.
7. Verify both ends using the identities and environments that will execute after the change.
   Exercise the producer operation that needs the changed authority, such as node provisioning,
   service publication or route approval, and the real consumer service or request path through
   that boundary. Verify automated jobs with their actual runner identity and secret scope; a
   local credential test cannot establish their cutover. Use authorized read-only checks or the
   repository's designated mutation target as appropriate. A green workflow, an active deployment,
   a policy check or a health endpoint bypassing the boundary is insufficient alone. Record each
   result with its client ID, target, operation and observed execution revision or run.
8. Re-read the complete manifest and live references after cutover. Reconcile stale references,
   missing consumers and changed runtime identities; repeat the affected verification when new
   evidence invalidates it. Revoke an old client or remove old authority only after every affected
   consumer has verified cutover and no live or automated reference still depends on it. An
   unresolved consumer blocks retirement and overall completion, even when the original symptom
   is fixed. Read back retirement and recheck the required producer and consumer operations.

## Encountered Failures

Every Tailscale failure encountered during the task starts `edit-skill` for its guidance diagnosis
alongside the operational repair. Record the failing execution, consumer identity, required
operation, effective authority and missing validation in the active private ledger. Repair an
evidenced guidance gap at its canonical owner; when existing guidance already forbids the miss,
record that noncompliance rather than duplicating the instruction. Generalize the failure class,
never the current environment or resource names. Follow `edit-skill`’s active-work batching: local
corrections apply immediately, and source repair continues while guidance verification and delivery
wait for the recorded coherent checkpoint.

## Output

Report the verified authority and consumer cutover, repository delivery links, producer and real
consumer checks, and retirement state. Name each unresolved consumer, unknown identity or pending
approval with the next action it requires; never report complete from source agreement alone.

## Guardrails

- Discovery supplies evidence and consumer obligations, not permission to mutate new environments,
  broaden access, merge, deploy or revoke credentials beyond the authorized outcome.
- Keep the consumer map and credential metadata in private task evidence. Never write secrets or
  incident-specific repository, environment or client identities into shared guidance.
