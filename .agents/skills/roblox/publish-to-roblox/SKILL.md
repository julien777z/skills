---
name: publish-to-roblox
description: Publish the game the session has been building to its Roblox experience, so the user can play the current build. Use to publish to Roblox. Run only when the user asks for it.
short_description: 'Publish the session’s game build to its Roblox experience.'
---

# Publish to Roblox

Publish the build the session has produced to the project's own Roblox experience, verify what went
live, and report how to play it. The invocation authorizes this one publish to the experience and
places it resolves below; it authorizes no change to the experience's audience, settings or
monetization, and no publish to any other experience.

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
  building anything. A place that belongs elsewhere stops the whole publish, so no mixed build goes
  live, and the report names that place.

## Workflow

1. **Set up missing destinations first.** When **Target** leads to creating an experience, or a
   place the build produces has no published counterpart, create it through the delivery route in
   `roblox-studio`'s source, editor, and publication reference, a new experience starting from its
   start place. Write each new ID into the project configuration **Target** reads, then commit and
   push it, so the build carries every destination and the next publish finds them.
2. **Freeze the build.** Take the latest pushed head of the session's branch, and record it.
   Build the publishable places from that head with the project's own build command and its
   integrity check, so they hold exactly that head's code, artwork, world and terrain archives,
   never a previously saved place copy.
3. **Publish from the isolated runner**, as `roblox-studio` sets up, holding its runner lock: open
   each built place in the runner's signed-in Studio and publish it over its place in the chosen
   universe, maps before the start place. Read the place and universe IDs in that editor before
   and after each publish. Grant asset permissions the publish dialog asks for when they cover the
   project's own assets; leave the audience setting as it is.
4. **Verify** each place's new version or update time from Roblox, not from the dialog's success.
5. **Clean up, then release.** Close the editors the publish opened and confirm the runner is idle,
   then release its lock; a failed publish ends the same way.

## Output

```markdown
**Published to Roblox:** [<experience name>](<experience URL>) · build [<short head>](<commit URL>)

| Place | ID | Updated |
| --- | --- | --- |
| [<place>](<place URL>) | <id> | <time> |

Created: <each experience or place this run created, as a link, or none>
Play: [<start place>](<game URL>)
Not included: <each commit after the frozen head as a link to it, or none>
```
