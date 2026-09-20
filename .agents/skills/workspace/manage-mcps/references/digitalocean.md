# DigitalOcean Remote MCPs

The owning workflow supplies the ordered project catalog and validated authentication context for each project. Do not retain a project, team, domain, or context mapping here.

## Managed Services

Expand every managed service over every project supplied by the owning workflow, in its declared order for all-project operations.

| Service | Remote endpoint | Claude display name | Codex identifier |
| --- | --- | --- | --- |
| Apps | `https://apps.mcp.digitalocean.com/mcp` | `DigitalOcean Apps — <environment>` | `digitalocean_apps_<environment_slug>` |
| Droplets | `https://droplets.mcp.digitalocean.com/mcp` | `DigitalOcean Droplets — <environment>` | `digitalocean_droplets_<environment_slug>` |
| Databases | `https://databases.mcp.digitalocean.com/mcp` | `DigitalOcean Databases — <environment>` | `digitalocean_databases_<environment_slug>` |
| Volumes | `https://volumes.mcp.digitalocean.com/mcp` | `DigitalOcean Volumes — <environment>` | `digitalocean_volumes_<environment_slug>` |
| Container Registry | `https://docr.mcp.digitalocean.com/mcp` | `DigitalOcean Container Registry — <environment>` | `digitalocean_container_registry_<environment_slug>` |
| Networking | `https://networking.mcp.digitalocean.com/mcp` | `DigitalOcean Networking — <environment>` | `digitalocean_networking_<environment_slug>` |
| Spaces | `https://spaces.mcp.digitalocean.com/mcp` | `DigitalOcean Spaces — <environment>` | `digitalocean_spaces_<environment_slug>` |

Derive `<environment_slug>` by lowercasing the dynamically resolved environment label, replacing each run of non-alphanumeric characters with one underscore, and trimming leading or trailing underscores.

## Authentication Resolution

Use the validated context supplied for each project. A matching context name is not proof of access.

Retrieve a token only when configuring or probing a connector. Keep it in the persistent Node session or the helper process that immediately consumes it. Follow the owning skill's agent/tool access, disclosure, and rotation boundaries without adding stricter handling here.

## Claude Desktop

1. Inspect Settings → Connectors through the persistent Computer Use session and classify the dynamically expected connectors.
2. For an addition or reauthentication, retrieve the token for the validated context directly into the persistent Node session.
3. Enter the token only as the secure `Authorization` header value `Bearer <token>`.
4. Start with the documented base endpoint. If Claude rejects an exact duplicate URL needed for another environment, append a stable query label derived from the environment, then make an authenticated MCP `tools/list` request to that exact URL before saving it. The query label distinguishes Claude entries; the bearer token determines access.
5. Inspect each permission group's blanket value. Use the group control only when the read-only category is not `Always allow` or the write/delete category is not `Needs approval`; never rewrite a category that already matches. Touch individual tools only for explicitly approved exceptions. Then verify the connector is connected and inspect both group-level state and any per-tool overrides.

Do not guess another URL form when either the authenticated probe or Claude connection fails. Report the blocker without exposing the response credential.

## Codex

Configure each HTTP MCP entry with the provider-managed authentication helper installed by the owning workflow:

- The service's documented base endpoint.
- `http_headers_helper` invoking the installed helper through Python with the dynamically resolved context as its sole argument.
- `default_tools_approval_mode = "writes"` for new entries, as Codex's category-level policy for automatic reads and approval-sensitive writes. Preserve the setting without rewriting it when it already matches.

Do not put a token in `config.toml` or an environment variable recorded by the configuration. Preserve unrelated MCP entries and settings. Codex refreshes helper-provided authentication according to its documented same-origin authorization behavior.

## Optional Services

During every audit, fetch DigitalOcean's current remote MCP endpoint catalog from `https://docs.digitalocean.com/reference/mcp/configure-mcp/`. Subtract every service in the managed-services table, and list the remaining service endpoints as optional additions without configuring them. Identify any tokenless global service separately from project-scoped authenticated services.

When the user approves a new managed DigitalOcean service, add its service row here and apply it across every project supplied by the owning workflow. Changes to projects, teams, ordering, or authentication contexts remain outside this reference.
