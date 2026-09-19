---
name: manage-mcps
description: Audit, restore, reauthenticate, and align managed remote MCP connectors across Claude Desktop and Codex when the user directly invokes $manage-mcps, while preserving unknown connectors and permission overrides.
disable-model-invocation: true
---

# Manage MCPs

Keep Claude Desktop and Codex aligned with the managed catalog declared by this skill's provider references.

## Authoritative References

- The repository's deployment skill, when the skill listing declares one — the environment catalog
  and authentication order for its hosting provider. Read it; it is user-invoked and cannot be
  invoked from here.

## Invocation Boundary

Run this skill only when the user directly invokes `$manage-mcps` in the current task. An agent must not invoke it implicitly, infer it from an MCP or connector request, or treat an earlier task's invocation as authorization for a new task.

## Provider Resolution

1. Identify the providers requested by the user or already present in the managed catalog.
2. Read each applicable provider reference in `references/` completely.
3. Read the applicable provider reference declared in **Authoritative References** completely on every invocation.
4. Resolve environments, accounts, teams, credentials, and their order only from that authoritative file. Never copy those mappings into this skill.
5. Expand each managed service definition over the environments that reference names. Generate display names and client identifiers from the service name and resolved environment.

Use `references/digitalocean.md` for DigitalOcean.

## Audit

1. Inspect both clients before changing either:
   - Inspect Claude Desktop connectors through Computer Use.
   - Inspect Codex through its MCP CLI and MCP configuration. Verify that the CLI used for connection tests is the version bundled with or selected by the active Codex client; do not assume the first `codex` on `PATH` is the same version.
2. Compare the dynamically expanded managed inventory with both clients and classify every expected connector as unchanged, missing, unauthenticated, or configuration drift.
3. Preserve connectors outside the managed catalog and never interpret “add all MCPs” as authorization to add optional services.
4. Inspect existing permission settings without changing them. Report every setting that differs from the defaults in **bold**.
5. Fetch any provider catalog required by its reference, subtract the managed services, and list the remaining services as optional additions.

## Approval Boundary

Before any mutation, present one exact combined preview that names:

- Every connector to add, reauthenticate, or update in each client.
- Every credential destination or storage change.
- Every permission change, if any.
- Every connector that will remain unchanged when that context helps define the batch.

One user approval covers the disclosed batch for the session, including identical work across its
environments and clients, retries, cleanup of failed attempts, and authentication-path changes needed
to finish it.

When Computer Use requires action-time confirmation, stage the complete disclosed client-side batch
and request one combined confirmation immediately before its first risky action. Do not split either
approval by client, environment, connector, credential transfer, permission group, retry, or cleanup.
Ask again only when the connector inventory, credential destination, permissions, or external resource
scope expands materially, or when the active client or Computer Use policy requires a separate handoff.
Preview and obtain approval for an expansion before continuing.
Re-audit immediately before mutation. “Add all MCPs” restores every missing managed-catalog entry in
both clients after this preview; optional provider services remain excluded.

## Reconciliation

1. Apply the approved batch in provider-defined environment order.
2. Reconcile Claude Desktop first. For new Claude connectors, inspect each permission group's current blanket value. Only when it differs, use the group control to set the complete read-only category to `Always allow` or the complete write/delete category to `Needs approval`. Do not rewrite a category that already has the required value, and do not set every tool individually unless preserving or applying an explicitly approved per-tool override.
3. Verify every changed Claude connector is connected and exposes its expected tools before changing Codex.
4. Reconcile Codex only after Claude verification succeeds. For new Codex connectors, inspect the current server-wide approval mode and use the broadest supported category policy equivalent to read-only automatic approval and write-sensitive approval. When supported, set `default_tools_approval_mode = "writes"` only when it differs; use per-tool policy only for explicitly approved exceptions.
5. Preserve existing category and per-tool permission overrides. Reauthentication and unrelated configuration updates never reset permissions.
6. Use each provider skill's secure authentication workflow and disclosure boundary.
7. Verify every changed Codex connector is connected and exposes its expected tools.
8. Re-inspect both clients and report whether their dynamically expanded managed inventories match. Leave unrelated connectors untouched.

## Catalog Maintenance

After an approved connector addition or durable configuration change, update the applicable provider service definition in the same branch or pull request. Do not update this skill for token rotation or for environment, team, or authentication-context changes already owned by the provider skill.

Add another provider by declaring its skill dependency in this file and adding a focused reference that defines its managed remote services. Keep provider-specific endpoints and mechanics out of this file.

## Guardrails

- Manage remote MCP connectors only unless the user explicitly requests a local server.
- Never reproduce or persist credential values outside the provider skill's authorized execution boundary.
- Never remove unknown connectors.
- Never add optional services implicitly.
- Never merge a catalog-change pull request unless the active user request authorizes it.
