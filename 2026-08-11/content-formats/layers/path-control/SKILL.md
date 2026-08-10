---
name: path-control
description: Use when the operator says "path control", "draw the camera path", "annotated camera move", "draw the line on the plate", "fly the camera through this still", or wants a video shot to follow an exact route through a scene instead of whatever the text prompt happens to produce. A layer, not a format: it bolts onto any format that generates motion from a still.
canonical: true
layer: L-PATH
---

# Path control (L-PATH)

Direct the camera by drawing on the plate. A red line marks the route, numbered waypoints mark
the order, the annotated plate goes to Seedance 2.0 as an image reference, and the prompt tells
the model to erase the line. The model flies the route and the marker never appears in the
footage.

What this buys that text prompting cannot: **an exact route, in an exact order, reaching an exact
end point.** Prose gets you a genre of move. A drawn line gets you the move.

**References:** two reels, scraped 2026-08-10 with the house Apify token and decoded frame by frame.

| Ref | Account | Source artwork | Plays / likes | Clip |
|---|---|---|---|---|
| A | `@maiciej_`, `instagram.com/p/Dbz_OTCKbFd/` | Zbyszko Siemaszko press photograph, Pulawska St, Warsaw, 1968 | 10.1K likes | `reference-bank/reels/maiciej-pathcontrol-Dbz_OTCKbFd.mp4`, 26.6s, 1080x1920 |
| B | `@tudormorari.ai`, `instagram.com/p/DbftzezssqF/` | Matejko's Stanczyk, Bocklin's self-portrait, Van Gogh's Starry Night | 192.5K likes | `reference-bank/reels/tudormorari-pathcontrol-DbftzezssqF.mp4`, 20.0s, 750x1333 |

Decoded contact sheets are `reference-decode-a.png` and `reference-decode-b.png` in this folder.
Ref B states its stack in the caption: made inside Higgsfield, tagged `#seedance`.

**Both reels are presentations of the method, not the method.** Each is a stacked frame: the
render on top, the annotated source underneath. That layout is how the creator shows their
working. It is not a house format and nothing here asks you to copy it.

---

## The method, in order

1. **Take one still.** A photograph, a painting, a generated plate, a map, a floorplan. Anything
   the camera can be inside.
2. **Draw the route on it in red.** One continuous stroke from where the camera starts to where
   it ends, through the space rather than across the surface.
3. **Number the waypoints.** Ref A marks 3 points, ref B marks 2. The numerals are drawn in the
   same red, in the same hand, sitting beside the stroke rather than on it.
4. **Pass the annotated plate as an image reference**, never as a start image. See the wiring
   below, this is the one thing that breaks the shot.
5. **Instruct the erase in the prompt.** The red line is a direction to the model, so the prompt
   has to say it is not scenery.
6. **End outside the plate.** Both references finish somewhere the original never showed: a
   fireplace behind Stanczyk, the street behind the taxi. That reveal is where the effect lives,
   and a path that stays inside the original framing wastes the technique.

## The annotation spec (measured, not quoted)

Sampled off full-resolution frames of both reels. Ref B was measured on its Starry Night section
because its Stanczyk section is mostly red costume and poisons a red mask.

| Ref | Stroke colour | Stroke width | As % of frame width | Red coverage of the plate |
|---|---|---|---|---|
| A, at 14.0s | `#E91B28` | 10px on 720 | 1.39% | 1.31% |
| B, at 16, 17, 18s | `#E01925` | 8px on 720 | 1.11% | 1.57% |

**The spec this gives you.** Stroke colour is a saturated primary red in a narrow band,
`#E01925` to `#E91B28`, and neither creator used a soft or dark red. Stroke width is **1.1% to
1.4% of frame width**, which on a house 1080x1350 plate is **12px to 15px**. Total red coverage
lands near **1.3% to 1.6%** of the plate, so the line is assertive and still leaves the picture
readable underneath.

Two consequences worth stating:

- **Thin lines are the failure mode.** At under 1% of frame width the stroke reads as part of the
  picture rather than as an instruction, and the erase instruction has less to key on.
- **The red has to be a colour the plate does not contain.** Ref B's own Stanczyk section is the
  warning: a red line over a red costume is ambiguous. On a plate with red in it, the drawn route
  competes with the subject, so pick the plate or pick another route.

## Wiring it to the house stack

Verified live off the CLI on 2026-08-10, `higgsfield model get seedance_2_0`:

| Param | What matters here |
|---|---|
| `image_references` | array, **at most 9** including start and end image. This is where the annotated plate goes. |
| `start_image` | object or null. **Do not put the annotated plate here.** |
| `end_image` | object or null. Useful for F16 The Loop, where the move has to return to its opening frame. |
| `aspect_ratio` | `auto, 16:9, 9:16, 4:3, 3:4, 1:1, 21:9`. **No 4:5.** Generate 3:4 and let the rig crop to 1080x1350. |
| `duration` | integer. Seedance rejects under 4s, so generate the minimum and trim with `ffmpeg -t -an`. |
| `generate_audio` | defaults **true**. house clips are silent, so set it false and still verify with ffprobe. |
| `resolution` | up to `4k`, but `mode: fast` caps at 720p. Use `mode: std` for 1080p and above. |
| Total budget | at most 12 reference files across images, videos and audio. |

**The start image trap.** A start image is literally frame one of the render, so an annotated
plate passed there puts the red line on screen at the top of the clip. The plate has to ride as
an image reference for the erase instruction to have anything to do. This is untested on the house
account and it is the single assumption the whole layer rests on, so the first generation tests
exactly this and nothing else.

## What the prompt has to carry

The drawn line replaces the camera-move description, so the prompt stops describing the move and
starts describing three other things:

1. **The erase.** State that the red line is a camera path annotation and must not appear in the
   output.
2. **What stays still.** Path control moves the camera. Say explicitly that the subject and the
   scene hold their position, or the model will animate the people as well and the shot stops
   reading as a move through a frozen world.
3. **The pace across the route.** The line gives geometry and carries no timing. Where the camera
   slows and where it accelerates is prose, and in several formats the pace change is the whole
   argument: F21 Bottleneck crawls at the pinch, F14 Dead End stops dead at the last waypoint.

House rules still bind: detailed positive prose, camera distance led, no negatives wall and no
JSON.

## How it sits with the existing formats

- **It changes no format's look.** It replaces how a move is specified inside formats that
  already generate motion from a still, so F2 noir-painterly keeps its plates, its palette and
  its crushed blacks.
- **It makes the shipped still library filmable.** F7 statics, F5 news slides and F8 quadrant
  plates are all stills a line can be drawn on, so several formats built on this layer cost zero
  new paid generations.
- **It does not touch the carousels or the statics themselves.** Those ship as they are.

## Gate status, 2026-08-10

**Unproven on the house account.** The method is confirmed by three independent public sources and
by two decoded reels, and the parameters above are read off our own CLI. No house generation has
run. Nothing built on this layer ships until one test clears, and per the house floor that test
is a single paid generation, reviewed before a second is bought.

The twelve formats drafted on this layer, F13 to F24, are in
`projects/content-engine/ideas/frozen-world/dossier.html`. **F20 Map Flight is the first test**,
because a drawn route over a map is the exact case the public sources documented, so a failure
there is the method rather than our plate.
