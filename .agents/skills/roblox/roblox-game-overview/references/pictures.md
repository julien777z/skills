# Pictures

The `roblox-game-overview` skill's procedure for staging, checking, capturing and reusing the
pictures its dashboard shows.

## Manifest And Reuse

The manifest is a JSON file beside the spec in private storage. Each picture has one entry: the
commit it was captured at, the capture's path, a fingerprint of each kind of input that produced it,
the hash of each file among them, and a `rejected` flag.

| Input | What it covers |
| --- | --- |
| Staging | The scene's progress checkpoint, the side step it sets, everything the game's staging places on stage at that progress, and the target's own definition: its point, interaction or encounter |
| Looks | The character appearance data, the avatar's rig and outfits, and for a scene that shows a creature, the creatures' definitions, their kit and the client code that draws their nameplates |
| World | The area and room files the scene stands in, and its map's terrain file |
| Camera | The scene's own spec: its kind, target, approach side, distances and heights |

Each run, after reading the game:

1. Compute every scene's inputs at the head read and compare them with the manifest.
2. Keep each picture whose fingerprints all match; it goes into the first render.
3. Recapture each scene that is new, rejected, or whose inputs changed, naming the changed input and
   file as the reason in the run's report.
4. Retire the entry of a scene whose subject no longer exists, and drop its picture.
5. Record each recapture against the head it was captured at once it passes its framing check and
   the agent has read it.

A picture the reader or the agent rejects is marked `rejected` and recaptured on the next pass
whatever its fingerprints say.

## Staging A Scene

Open a throwaway editor on a built copy of the place that holds every map, start Play with a
disposable profile, and never save. Reuse the repository's own capture helpers for each step below
where it has them.

1. **Move the profile to the scene's progress** through the game's own test or admin route, and set
   any side step, so the game's staging places that progress's characters and props. Group scenes
   that share a progress so the profile moves once per group, and close the one-time windows a
   checkpoint opens.
2. **Set the avatar down before the target**, searching for ground from just above the stand point;
   indoors, a search from high above lands the avatar on the roof.
3. **Hold a scripted camera** behind and beside the avatar, looking at the target, after releasing
   any camera an earlier scene still holds.
4. **Wait for streaming to settle** around the view and preload its assets.
5. **Check the framing**, below, and reframe until it passes.
6. **Hide every screen GUI** and capture once two captures in a row match.

Kinds of scene: a quest or step at its target; a portrait in front of a character, with the avatar
out of frame; a district from above; a room or dungeon entered through its door, or set down inside
one whose door is not yet open; a creature in a fight.

**A creature in a fight** is started through the game's own encounter route at a center the game
accepts, the one its own search for duel ground finds near the creature's roaming area; a center
picked by hand is refused silently when the circle's ground is missing, uneven or crosses a path.
Hold the camera beside the creature across the circle from the avatar, so it faces the camera, then
leave the fight through the game's own exit, which may confirm in a screen of its own.

**Batch by lease.** List every scene in one file, and let one script work through the list within a
lease, stopping while the lease still covers closing the editor. A later lease skips captured scenes
and retries a failed one once. Queue for the runner in turn; the page is already delivered, and each
batch's pictures are rendered into it as the batch lands.

## Framing Check

Before capturing, measure the subject in the held view:

- **Find the subject by walking the world's character models**, nearest the point where the actor
  actually stands, or the small props around the target when no character stands there. Spatial
  queries skip parts that turn querying off, which characters and props often do, so a query finds
  the wrong model or none: it passed an actor hidden behind the avatar and failed props standing in
  plain view. The point is where the actor stands, which can be well away from its encounter's
  named point.
- **Project every visible part's corners** through the camera to get the subject's screen box.
- **Judge it**:
  - in frame: the whole box sits inside the frame, clear of each edge by a small margin. A check on
    the box's middle alone passed a creature cut off by the frame's corner;
  - large enough: a character covers a meaningful share of the frame, more for a portrait or a
    creature in a fight than for a scene;
  - not behind the avatar: a ray from the camera to the subject's middle reaches it before the
    avatar, and the avatar's box covers at most half of it;
  - for a portrait or a creature, facing the camera: the head's look direction points toward it.
    A character's facing point does not say which side its face is on, so this is measured, never
    assumed.
- **Reframe in the same lease** when a check fails: move the camera to the avatar's other side when
  the avatar covers the subject, closer when the subject is small, further when it leaves the frame,
  and to the subject's other side when it faces away. Try three framings, capture the last one even
  when it still fails, and record the failure so the agent reads that picture first.

Read every capture whole before using it, as the check passes only what it can measure.
