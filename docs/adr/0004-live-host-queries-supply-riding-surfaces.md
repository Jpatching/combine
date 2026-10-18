---
status: proposed
---

# Live host queries supply riding surfaces

Riding surfaces are built from **sampled surfaces**: ground heights queried from the
running GTA IV around the rider, through the ground-height native already used to
mount. They are sent to the Skate Session through the existing triangle-surface
route. Decoded static collision resources remain a dormant fallback. This replaces
the flat patch, which refused any ground more than 0.05 m off level, and avoids
the unresolved placement of decoded collision.

Accept this once one windowed ride on a sampled slope (mount, push, steer both
ways, dismount, walk) succeeds from a build of `main`.

## Considered Options

- **Decoded static collision** (the earlier route): complete geometry, including
  walls, but world placement of the decoded resources was never qualified.
- **Live host queries** (chosen): reuses an already-working native and the existing
  triangle route. It only sees floors. Walls become coverage gaps, and stacked
  floors need a later stepped probe.

## Consequences

- The vertical query starts just above the rider, so the floor under the rider is
  sampled. Rooftops and the road beneath a bridge work without stacked-floor support,
  but crossing between stacked floors does not.
- Every metre threshold depends on the unverified `SCALE = 1` assumption in
  `tools/gtaiv-skate/combine_skate.js`.

## Floor agreement

Triangles between 2 m samples miss curved ground by more than the original 0.05 m
ride check (about 0.08 m at an 8 m radius), so that check would end rides on
ordinary streets. **Floor agreement** asks which floor the rider is on, not how
planted the skater looks. Host ground at the rider must be within the wall
threshold (0.3 m) of the window, the same jump the window itself calls a wall.
One tolerance applies to every surface, authored or sampled. It applies only while
Skate reports ground contact, since an airborne rider over a planter or curb has not
changed floor. Losing it dismounts with "floor agreement lost".

Denser sampling was rejected: it shrinks curvature error but not the error near
a step, and it costs four times the probes per halving. The mount-preparation
check stays at 0.05 m, because it compares host ground with itself.

Known limitation: steps under the wall threshold, such as curbs, ride as ramps,
and the skater can be drawn up to the step height off host ground near them.
