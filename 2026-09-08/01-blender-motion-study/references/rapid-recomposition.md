# Lane B: rapid decomposition and recomposition

The companion lane to the weighted handoff. Alternate them where the script changes meaning, rather
than imposing one move on every beat. White subject, pure black background, 9:16, centred focal
position.

## Composition

One readable focal object becomes another through a short, coherent redistribution of parts. Let
the silhouette read before and after the transformation. Keep the busy intermediate brief.

## Camera

Front-facing, fixed. Allow a shallow 3D object where it helps the shape; the transition belongs to
the object. Whatever format the study ends up inside still controls the final framing.

## Identity

Preserve visual continuity through a shared centre, a shared material and a shared direction of
travel. Decompose into meaningful groups, then recompose quickly. Do not force each old stroke into
a particular new stroke. Same-topology deformation, group assembly and a concealed replacement are
three different implementations; write down which one the scene actually uses.

## Anti-patterns

Slow shredded intermediates, arbitrary particles, prolonged invisibility, constant wobble, uniform
bouncing, and decorative extra objects. Fast does not mean a hard cut: accelerate into the change,
reform clearly, and dissipate the remaining motion during a brief settle.

Initial tuning range, authored rather than measured: about 0.2 to 0.4 seconds for the main
transformation, with small timing offsets between functional groups. Holds carry the meaning.
Physical response should fit the implied material and mass. Use deterministic keyframes instead of a
simulation unless actual collision behaviour is needed.

## In the example script

`motion_study_example.py` compresses two triangles into a diamond, deforms that surface into a small
round core, then grows separate machine components around it with keyed curve draw-on. The core stays
visible until the replacement part fills its footprint, so attention never has to jump.

This is mesh deformation plus core-mediated replacement and curve assembly. It is not arbitrary
image-to-image morphing, particle reassembly, or preservation of every source stroke. The ball
follows a small 240 Hz planar gravity and restitution loop against circular bumpers, a capsule wall
and fixed flipper segments; everything else is authored kinematics. Rendering is CPU Cycles at eight
samples, 1080 x 1920, 60 fps, a white constant-colour material and no bloom.

## Three lessons from the first proofs

1. A closed curve at zero bevel factor can stay visible. Close paths with an explicit final point and
   keep the curves non-cyclic, so draw-on is predictable.
2. Overlap the incoming object's visible entrance with the outgoing object, so no frame is empty.
3. For connected growth, a child branch begins only after its parent tip reaches the junction.
   Overlapping the draw-on intervals produced detached tips; sequential 0.17 second generations fixed it.

## Measured once, on one laptop

The 300 frame, five second sequence rendered in about four minutes on the CPU with three threads at
low priority, peaking at about 0.5 GB resident memory and 2.9 core equivalents, with no thermal
warning recorded. Three short repair renders of 12 to 113 frames took between 15 and 80 seconds
each. One machine's observed cost, not a guarantee.
