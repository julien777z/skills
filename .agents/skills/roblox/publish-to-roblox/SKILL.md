---
name: publish-to-roblox
description: Explicit user-invoked publish of the game the session has been building to its Roblox experience, so the user can play the current build. Run only when the user asks to publish to Roblox.
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
- When the request names no experience and the project names more than one candidate, ask the
  user which one through the question tool before building anything for it. When the project names
  none, ask whether to create a new experience for the game; only the user's answer authorizes
  creating one.
- Confirm, through Roblox's public APIs, that every place ID belongs to the chosen universe before
  publishing. A place that belongs elsewhere stops the publish of that place.

## Workflow

1. **Freeze the build.** Take the latest pushed head of the session's branch, and record it.
   Build the publishable places from that head with the project's own build command and its
   integrity check, so they hold exactly that head's code, artwork, world and terrain archives,
   never a previously saved place copy.
2. **Publish from the isolated runner**, as `roblox-studio` sets up, holding its runner lock: open
   each built place in the runner's signed-in Studio and publish it over its existing place in
   the chosen universe, maps before the start place. A place with no existing counterpart is added
   through the delivery route in `roblox-studio`'s source, editor, and publication reference; for a
   new experience, publish the start place first through Publish to Roblox As as a new experience,
   then add the maps that way. Read the place and universe IDs in that editor before and after each
   publish. Grant asset permissions the publish dialog asks for when they cover the project's own
   assets; leave the audience setting as it is.
3. **Record what was created.** Write the ID of every experience or place this run created into the
   project configuration **Target** reads, commit it on the session's branch and push it, so the
   next publish finds them rather than creating them again.
4. **Verify** each place's new version or update time from Roblox, not from the dialog's success.
5. **Clean up, then release.** Close the editors the publish opened and confirm the runner is idle,
   then release its lock; a failed publish ends the same way.

## Output

```markdown
**Published to Roblox:** [<experience name>](<experience URL>) · build [<short head>](<commit URL>)

| Place | ID | Updated |
| --- | --- | --- |
| [<place>](<place URL>) | <id> | <time, or `new` for a place this run created> |

Play: [<start place>](<game URL>)
Not included: <each commit after the frozen head as a link to it, or none>
```
