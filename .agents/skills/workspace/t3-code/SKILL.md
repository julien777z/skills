---
name: t3-code
description: Inspect and configure T3 Code environments, providers, and settings. Use for provider environment variables, including bulk imports, merges, individual changes, and removals, or other T3 Code configuration work.
short_description: 'Manage T3 Code configuration and provider environment variables.'
---

# T3 Code

Configure the selected T3 execution environment through its native interfaces. Discover actual
provider instance IDs; a display name, model name, or local checkout does not identify the target.

## Environment variables

Use `scripts/env.mjs` from this skill's resolved directory with Node.js 22 or newer. The helper
accepts supplied data; it does not depend on an application, clipboard, or credential source.

- `list` shows provider IDs, names, drivers, and variable names without values.
- `merge` accepts `.env` text or a JSON object of string values through stdin or `--file`.
  `--format auto` selects JSON when the input begins with `{`; otherwise it uses Node's dotenv
  parser. Explicit `--format dotenv` and `--format json` select the parser directly.
- `set NAME` reads one literal value through stdin or `--file`, including an empty or multiline
  value. Values never belong in command arguments.
- `unset NAME ...` removes only the named variables.
- Repeat `--provider ID` for several instances. Changes are previews until `--apply` is supplied.
  An authorized request covers applying its disclosed batch; do not ask the user to approve it again.

Merges replace matching variable names and preserve every unrelated variable and provider field.
An empty value is a value, never a removal. Imported values are sensitive by default, matching
T3's Add variable behavior. Preserve existing redaction markers and let T3 store secrets.

For example, with the resolved helper path in `T3_ENV_SCRIPT`:

```sh
node "$T3_ENV_SCRIPT" list --ssh user@node.example
cat ./provider.env | node "$T3_ENV_SCRIPT" merge --ssh user@node.example --provider claudeAgent
cat ./provider.env | node "$T3_ENV_SCRIPT" merge --ssh user@node.example --provider claudeAgent --apply
```

`--ssh` uses the existing SSH configuration and authentication. `--identity` and `--known-hosts`
select existing SSH files when needed. Omit `--ssh` to manage the local T3 environment. `--base-dir`
selects a non-default T3 data directory, and `--t3` selects its installed CLI executable.

## Dependencies

- `tailscale-config` — reconcile hostname and route consumers when provisioning or replacing nodes.
- `security-audit` — apply its secret, input, authentication, and authorization guidance to configuration changes.
- `proton-pass` — retrieve a needed existing credential only when it was not supplied and is not already available through authorized authentication.

## Configuration workflow

1. Identify the requested environment, provider instances, and project scope. Read installed T3
   version and native CLI help; use source matching that release when the UI or CLI does not expose
   the needed operation. The authoritative source is [T3 Code](https://github.com/pingdotgg/t3code).
   Reuse the intended account and environment; ask only about unresolved target ambiguity.
2. Inspect current configuration. For variables, run the helper's `list` command and resolve the
   requested provider names to its actual IDs. The helper manages environment-wide provider values,
   which apply across projects on that environment. Do not silently substitute another scope.
3. Obtain input from the user-authorized source: a file, pipe, provided values, or the selected
   application's environment editor through Computer Use. Copy that block as data. Keep values
   out of chat, command arguments, Git, diagnostics and screenshots. If a temporary input file is
   needed, create it privately with mode `0600`, use it only for the transfer, and remove it afterward.
4. Preview variable names and destination providers. Apply the authorized batch through the helper.
   It uses T3's native scoped session and settings mutation rather than editing settings files or
   provider account credentials. Existing Claude profiles and other provider runtime settings stay
   attached to their own instances.
5. Read the resulting configuration through T3 and verify the changed names, sensitivity and
   preserved settings. Confirm the selected environment's Providers screen when the task involves
   that UI. Existing running provider sessions may retain their original process environment;
   use a newly started session for the new values rather than restarting unrelated work.
6. For other configuration, use the same target, inspection, authorized mutation and readback
   procedure through the current native CLI/API. Inspect the current schema before using an
   operation not implemented by the variable helper; never invent a command or directly rewrite
   T3's persisted settings to bypass its secret handling.

## Node provisioning

When replacing an existing node, retain the intended node name and identify the old node by its
stable provider, Tailscale and T3 IDs before creating the replacement. Validate the new node's T3
connection, setup and requested configuration before removing the old node through the authorized
provider and T3 lifecycle.

After the old node is removed, reconcile the replacement's name. Tailscale may have assigned a
collision suffix such as `-1` while both machines existed. Remove that automatically added suffix
so the replacement uses the intended hostname; preserve numbers that belong to the intended name.
Keep its system hostname, Tailscale hostname, T3 environment label and provider display name
consistent, using their native interfaces. Preserve the replacement's IDs, credentials, projects
and chats.

Apply `tailscale-config` before this cutover. Read Tailscale's assigned DNS name after renaming;
never assume the requested hostname determines the final address. Update affected Serve routes,
setup links and other discovered hostname consumers, then verify HTTPS and the T3 connection at
the assigned address. Provisioning is incomplete until this post-removal name cleanup and
readback succeed.

## Output

Report the environment, provider IDs, affected variable names, preserved configuration, and verified
result. State any work still needed for a new provider session. Never include variable values or
session tokens.

## Guardrails

- Never infer exposure or rotate credentials merely because authorized agent work read them.
- Use only the user's selected destinations and providers; importing to one profile does not authorize others.
- Keep authentication profiles, provider enablement, model preferences, projects and chats intact during a variable change.
- Do not reveal stored values to produce a preview. Preserve T3's native secret storage and close only temporary sessions created by the helper.
