# Lane A: the weighted object handoff

Preserve the focal location while replacing the whole object through visible motion. Alternate with
rapid decomposition and recomposition (`rapid-recomposition.md`) according to the script. Neither
lane requires every stroke of one drawing to interpolate into the next.

## Composition

White objects on pure black in 9:16. A readable object holds at centre, exits left, and the next
arrives from the right. The whole outline and its contents travel together. Keep the held state
clear; transient edge clipping during an actual entrance or exit is intentional.

## Camera

Static, front-facing. Motion belongs to the subject, never to a camera pan.

## Identity

Each new object can be its own drawing. No forced point correspondence, shredded geometry, crossing
stroke interpolation or drawn-out halfway shape. The sequence follows the script's meaning rather
than keeping the same physical object at all costs.

## Anti-patterns

Uniform spring presets on every object, indefinite wobble, large rubbery scale changes,
constant-speed slides with abrupt stops, slow icon morphs and idle decorative movement. Keep
transitions short, generally 0.25 to 0.4 seconds, then hold the destination. A morph is still valid
when it is short and legible; use it selectively, never as a blanket law.

## Authored physical response

Treat each object as having a mass, an arrival velocity, a braking interval and a pivot.

- A wide, heavy object brakes firmly with a restrained inertial lean and strong damping.
- A light object may arrive faster, overshoot slightly and rebalance with a small decaying rock.
- A third object can stop cleanly with no rebound at all.

Rotation, vertical movement and translation must all describe the same arrival event, and energy
decays after the stop. Do not bounce every item.

This is physically motivated authored animation, not a rigid-body or friction simulation. The
worked example uses cubic Hermite travel into a damped translation and rotation response, exported
at 60 fps so the short moves have enough temporal samples. Keep the response parameters in a JSON
file beside the scene, and inspect three frames: the entrance, the maximum lean, and the settled
hold.

## In the example script

`motion_study_example.py` implements this lane at the four second mark: the whole machine
accelerates out to the left on an eased curve while the tree brakes into the same centre through a
damped oscillation (`exp(-10v) * sin(17v)` on position, a matching decaying rotation), then the
tree's branches draw on in sequence. Read the block that begins "Whole mechanism accelerates out".

## Measured once, on one laptop

360 frames at 1080 x 1920 rendered in about three minutes on the CPU with three threads at low
priority, peaking at about 0.5 GB resident memory and 2.6 core equivalents, with no thermal warning
recorded. That is one machine's observed cost, not a guarantee.
