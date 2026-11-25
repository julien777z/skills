# Pictures

The `roblox-game-overview` skill's procedure for staging, checking, capturing and reusing the
pictures its dashboard shows.

Contents: **Manifest And Reuse**, **Staging A Scene**, **Framing Check**.

## Manifest And Reuse

The manifest is a JSON file beside the spec and the pictures, in the dashboard's folder that survives a restart. Each picture has one entry: the
commit it was captured at, the capture's path, a fingerprint of each kind of input that produced it,
the hash of each file among them, and a `rejected` flag.

| Input | What it covers |
| --- | --- |
| Staging | The scene's progress checkpoint, the side step it sets, everything the game's staging places on stage at that progress, and the target's own definition: its point, interaction or encounter |
| Looks | The character appearance data, the avatar's rig and outfits, and for a scene that shows a creature, the creatures' definitions, their kit and the client code that draws their nameplates |
| World | The area and room files the scene stands in, every art file a marker in them names, and its map's terrain file |
| Camera | The scene's own spec: its kind, target, approach side, distances and heights |

**The scene set is fixed before any capture: one scene for every part the pages show.** A scene the
game keeps in its own scene list is used as the game defines it, and the game's list is never
edited. A part the game's list leaves out gets a scene in the skill's own list beside the manifest,
written once and kept for later runs. Owed scenes are those in the set that are new, rejected or
changed; nothing else is captured.

Each run, after reading the game:

1. Compute every scene's inputs at the head read and compare them with the manifest.
2. Keep each picture whose fingerprints all match, and render and deliver the page with them before
   staging anything, as the skill's **Run Order** says.
3. Recapture each scene that is new, rejected, or whose inputs changed, naming the changed input and
   file as the reason in the run's report.
4. Retire the entry of a scene whose subject no longer exists, and drop its picture.
5. Record each recapture against the head it was captured at once it passes its framing check and
   the agent has read it.

A picture the reader or the agent rejects is marked `rejected` and recaptured on the next pass
whatever its fingerprints say.

## Staging A Scene

Hold one of the game's editors, as `roblox-studio`'s testing reference says for the game's editor
pool, and open a built copy of the place that holds every map in that editor's slot, in place of its
warm editor; start Play with a disposable profile, and never save. Reuse the repository's own capture helpers for each step below
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

**Batch the captures.** One script works through about ten minutes of owed scenes under one
editor's lock and stops there. Then close, release, render and deliver, as the skill's **Run Order**
step 3 says, before the next batch's lock is acquired. A later batch skips captured scenes and
retries a failed one once.

## Framing Check

Before capturing a scene that names an actor or props, measure that subject by name in the held
view. A round is captured from the round's own camera with no measure. Never measure by nearest
model: a scene with no named subject is captured unmeasured and read first.

- **Find the subject by walking the world's character models** and picking the actor the scene
  stages by its own name or encounter, or the small props around the target when the scene stages
  no character. Spatial queries skip parts that turn querying off, which characters and props often
  do, and an actor that walks its ground stands away from its encounter's named point, so the
  nearest model there can be another one; a check that measures either passes a frame that cuts the
  real subject off.
- **Project every visible part's corners** through the camera to get the subject's screen box.
- **Judge it**:
  - in frame: the whole box sits inside the frame, clear of each edge by a small margin, since a
    check on the box's middle alone passes a creature cut off at the frame's corner;
  - large enough: a character covers a meaningful share of the frame, more for a portrait or a
    creature in a fight than for a scene;
  - not behind the avatar: a ray from the camera to the subject's middle reaches it before the
    avatar, and the avatar's box covers at most half of it;
  - for a portrait or a creature, facing the camera: the head's look direction points toward it.
    A character's facing point does not say which side its face is on, so this is measured, never
    assumed.
- **Reframe in the same batch** when a check fails: move the camera to the avatar's other side when
  the avatar covers the subject, closer when the subject is small, further when it leaves the frame,
  and to the subject's other side when it faces away. Try three framings, capture the last one even
  when it still fails, and record the failure so the agent reads that picture first.

Read every capture whole before using it, as the check passes only what it can measure.
