---
name: publish-to-roblox
description: Explicit user-invoked publish of the game the session has been building to its Roblox experience, so the user can play the current build. Run only when the user asks to publish to Roblox; one invocation publishes once, and later changes in the session are never republished without a new request.
short_description: 'Explicit user-invoked publish of the session’s game build to its Roblox experience.'
disable-model-invocation: true
---

# Publish to Roblox

Publish the build the session has produced to the project's own Roblox experience, verify what went
live, and report how to play it. The invocation authorizes this one publish to the experience and
places it resolves below; it authorizes no later publish, no change to the experience's audience,
settings or monetization, and no publish to any other experience.

## Dependencies

- `roblox-studio`
- `agent-lock`

## Target

- Read the experience and its places from the project's guidance and configuration, such as an
  environment module that names a staging or work-in-progress universe and the place IDs its maps
  record. Publish to the development or staging experience by default; publish to a production
  experience only when the request names it.
- When the request names no experience and the project names more than one candidate, or names
  none, ask the user which one through the question tool before building anything for it.
- Confirm, through Roblox's public APIs, that every place ID belongs to the chosen universe before
  publishing. A place that belongs elsewhere stops the publish of that place.

## Workflow

1. **Freeze the build.** Take the latest pushed head of the session's branch, and record it.
   Bring the project's saved delivery places up to that head through the project's own
   synchronization and integrity checks, so the published places hold exactly that head's code,
   artwork, world and terrain; commit and push that update when it changes the repository's files.
2. **Publish from the isolated runner**, as `roblox-studio` sets up, holding its runner lock: open
   each delivery place in the runner's signed-in Studio and publish it over its existing place in
   the chosen universe, maps before the start place. Read the place and universe IDs in that
   editor before and after each publish. Grant asset permissions the publish dialog asks for when
   they cover the project's own assets; leave the audience setting as it is.
3. **Verify** each place's new version or update time from Roblox, not from the dialog's success.
4. **Release** the runner lock and close the editors the publish opened.

## Output

```markdown
**Published to Roblox:** <experience name> · build <short head>

| Place | ID | Updated |
| --- | --- | --- |
| <place> | <id> | <time> |

Play: <game URL of the start place>
Not included: <changes after the frozen head, or none>
```
