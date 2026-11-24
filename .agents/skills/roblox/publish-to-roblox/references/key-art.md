# Key Art

The `publish-to-roblox` skill's procedure for an experience's icon and thumbnails: what the pictures
of today's top games share, how to stage and composite pictures of that kind from the game's own
assets, and how to set and read them back.

## Study the Top Games First

- Read Roblox's discovery sorts through the public explore API,
  `GET https://apis.roblox.com/explore-api/v1/get-sorts?sessionId=<any UUID>`, and take the games
  of its trending, playing-now, revisited and play-with-friends sorts; read the sort IDs from the
  response rather than assuming them.
- Fetch those games' icons through
  `https://thumbnails.roblox.com/v1/games/icons?universeIds=<ids>&size=512x512&format=Png` and their
  thumbnails through
  `https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=<ids>&size=768x432&format=Png&countPerUniverse=<n>`,
  and lay each kind out as a contact sheet.
- Read the sheets whole before staging anything. They are the standard every picture is held to.

## What Those Pictures Share

| Picture | What it shows |
| --- | --- |
| Icon | One hero subject in close-up, such as a character's face and upper body or a creature, mid-action or with a strong expression, on a radial burst, bright sky or dark gradient. Saturated color, rim light and glow separate it from the backdrop. A bold, thick-outlined wordmark or one or two words sit at the bottom. It still reads at 150 px. |
| Thumbnail | A posed key-art moment showing the game's hook, such as a catch, a race or a fight, from a low or close camera. Cinematic light, bloom, depth of field and glowing effects. The logo sits in a corner, with at most a few words. |

A player-height gameplay screenshot is not a game picture, however good the scene.

## Stage From the Game's Own Assets

Copy the built place first, recording the source place file's checksum, and point every capture at
the copy, staging there with the game's own characters, creatures, outfits, props, effects and
places. Before the first upload, compare the source file with that checksum; when it differs,
rebuild it from the frozen head with the build command and integrity check of the skill's
**Freeze the build** step, and redo every capture from the copy.

- **Pose, then anchor.** Pose characters and creatures through their joint offsets, such as a
  `Motor6D`'s `C0`, or freeze an animation at a strong frame. Then anchor every part where it
  stands, so nothing moves between the tiles of one picture.
- **Frame from the camera first.** Place the camera, then turn each character three-quarters toward
  it while it still faces what it acts on, so every face reads. Use a narrower field of view than
  play does.
- **Light with color.** Put colored rim lights behind the subject and colored fill lights beside it,
  with bloom, depth of field and color correction. A white key light flattens the subject.
- **Hide what play shows.** Turn off every overhead name, health bar and HUD element, the core GUI
  and the top bar, so no test account's name appears. Freeze particles at a full frame and move
  wandering characters out of the shot.
- Raise the graphics quality for the capture, and restore the editor's own level afterward.

## Capture

- Make the editor's window as large as the display allows, and capture at that size, so nothing is
  upscaled more than it must be.
- Where the picture is larger than the viewport, capture it in overlapping tiles from one eye
  position, each aimed at its part of the picture, leaving out the band the client cannot hide,
  such as Roblox's menu button, and stitch the tiles by their projection into the picture.
- **Check every overlap for ghosting.** Warp each pair of overlapping tiles into the picture and
  compare them where both cover it; a difference means something moved between tiles. Anchor it and
  capture again rather than keep a ghosted picture.
- Capture an icon's subject on its own, close up, rather than cropping it from a wide shot. To cut
  it out, capture the same frame over a black and then a white backdrop behind the subject, and take
  its transparency from the difference between the two.

## Composite

- Grade the picture with saturation, contrast and a tint suited to the game's mood, and add a radial
  burst or glow behind the subject, a soft glow around it, bloom on its brightest parts and a
  vignette.
- Add a wordmark of the game's name in an openly licensed display font, such as one under the SIL
  Open Font License: a gradient fill, a thick dark outline, a drop shadow and a glow. A place's
  picture may add the place's name beneath it.
- Keep the subject centered with a margin, since Roblox rounds an icon's corners and crops
  thumbnails on small cards. An icon is 512×512 and a thumbnail 1920×1080.
- The steps every picture repeats — stitching the tiles, the overlap check, the cut-out and the
  composite — run from one helper in the repository's `.agents/tools/`, committed with the task's
  source work; each picture's own parameters stay with the task's working files.

## Check

- Read each picture whole on its own at its full size, naming every picture in the set as it is
  read, and look for clipping, a floating or hidden subject, stray text or names, gray
  placeholders, upscale blur, and a wordmark crowding the subject.
- Lay the whole set out as one sheet with every picture shrunk to 150 px, beside the trending
  sheets, read it whole, and ask whether each picture still says what the game is.
- Redo any picture that fails either check, keeping everything **Composite** adds, such as moving or
  resizing a crowding wordmark rather than leaving it out, and put each redone picture through both
  checks again, with a new 150 px sheet, so the last sheet read holds exactly the pictures that will
  be uploaded.
  State where the set still falls short of the trending pictures.

## Upload and Set

The Open Cloud calls need the `asset:read` and `asset:write` scopes for the experience's creator,
through whichever route the project provides for them.

1. **Upload each picture as an Image asset.** Send `POST /assets/v1/assets` as a multipart form with
   a `request` part, a JSON object holding `assetType: "Image"`, a display name and the creator
   under `creationContext`, and the file under `fileContent`. Poll
   `GET /assets/v1/operations/<operationId>` until it is `done`, and read `response.assetId`.
2. **Note each place's revision.** Read `GET /assets/v1/assets/<placeId>` and record its
   `revisionId`.
3. **Set each place's icon and thumbnails** with
   `PATCH /assets/v1/assets/<placeId>?updateMask=icon` and `?updateMask=previews`. The `request`
   part holds `{"assetId": "<placeId>", "icon": "assets/<imageId>"}`, or
   `{"assetId": "<placeId>", "previews": [{"asset": "assets/<imageId>"}]}` with the full list in
   display order. The route answers a JSON body with 404, so send a multipart form. Where a tool
   sends a form only with a file, add a small filler file under a field name the API does not read,
   never `fileContent`, which carries an asset's content. The experience's own icon and thumbnails
   are its start place's.
4. **Confirm nothing else changed.** Read each place's record again and check that its
   `revisionId` is the one step 2 recorded.

## Read Back

- Read the pictures through the public thumbnails API:
  `https://thumbnails.roblox.com/v1/places/gameicons?placeIds=<ids>&size=512x512&format=Png`,
  `https://thumbnails.roblox.com/v1/games/icons?universeIds=<id>&size=512x512&format=Png`, and the
  `multiget/thumbnails` call above for the universe.
- Download every set picture into one sheet and read it whole, confirming each is the new picture
  and not the placeholder.
- A state other than `Completed`, such as `Pending`, means moderation is still reviewing the image:
  read again until it completes or a bounded wait passes, and report the state as read.
