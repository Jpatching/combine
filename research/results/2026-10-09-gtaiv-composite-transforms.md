# GTA IV composite collision: bounded source contract

Observed: 2026-10-09. Scope: public source inspection for the next collision
inspector slice on #20. No upstream program, game resource, exporter, game or
Skate runtime was executed by this investigation. This is the delegated research
step from Matt's `research` skill, not evidence of owned-file compatibility.

## Finding

A bounded implementation can decode a composite containing geometry/BVH
polygon meshes, apply each child's explicit rigid transform, and reject the
whole result if any child or transform is unsupported. Independent GTA IV
matrix helpers corroborate the position formula. Real street placement remains
a separate proof: correctly applying a WBN child matrix does not establish the
resource's relationship to the live host world.

## Pinned sources and licensing

- GTA4Unity, `c107e46cf8ab4e3d42f9c0bf685f80bb732a3609`: existing reference;
  [GPLv3 license](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/LICENSE).
- CitizenFX/FiveM, `0105063b0394b1b9d085c917a8dc9c9abf0a620f`: inspected
  actual `RAGE_FORMATS_GAME_NY` definitions and IV-to-V conversion, rather than
  assuming V's layout. Its [root license](https://github.com/citizenfx/fivem/blob/0105063b0394b1b9d085c917a8dc9c9abf0a620f/LICENSE)
  assigns the Creator Platform License to this directory; `rage-formats-x`
  is outside the listed LGPL directory exceptions. Use independently authored
  decoding based on format facts; this note does not authorize copying its code.
- IV-SDK, `dddbd3f54b146bdb3a9852809e48e5cb169af3cd`: existing reference,
  [GPLv3 license](https://github.com/Zolika1351/iv-sdk/blob/dddbd3f54b146bdb3a9852809e48e5cb169af3cd/LICENSE).
- Plugin-SDK, `15f15b60bbf74c106e1b496ff92c98764abf4605`: IV-specific matrix
  helpers; [zlib-style license](https://github.com/DK22Pac/plugin-sdk/blob/15f15b60bbf74c106e1b496ff92c98764abf4605/LICENSE).

New pins are evidence references only; `research/upstream.lock.json` was not
changed. Source licenses do not establish rights to game assets.

## Composite layout

Offsets are relative to the bound object, not the resource wrapper.

| Offset | Serialized field |
| --- | --- |
| `0x80` | child bound pointer array, 4-byte entries |
| `0x84` | primary child matrix array |
| `0x88` | secondary/internal child matrix array |
| `0x8c` | child AABB array pointer |
| `0x90` | first unsigned 16-bit child count field |
| `0x92` | second unsigned 16-bit child count field |

The base is `0x80` bytes and the composite `0xa0`, corroborated by
[IV-SDK size assertions](https://github.com/Zolika1351/iv-sdk/blob/dddbd3f54b146bdb3a9852809e48e5cb169af3cd/include/phBound.h).
[GTA4Unity](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/Collision/PhBoundComposite.cs)
names `0x90` maximum and `0x92` active count. CitizenFX's
[pgArray](https://github.com/citizenfx/fivem/blob/0105063b0394b1b9d085c917a8dc9c9abf0a620f/code/components/rage-formats-x/include/pgContainers.h)
names these count and capacity. Require equality for this slice; neither
fallback count choice nor silently skipping null children is justified.

CitizenFX's [NY phBound definitions](https://github.com/citizenfx/fivem/blob/0105063b0394b1b9d085c917a8dc9c9abf0a620f/code/components/rage-formats-x/include/phBound.h)
identify geometry `4`, BVH `10`, composite `12`; sphere/capsule/box are distinct.
`Matrix3x4` contains four padded `Vector3` records. The secondary array is
described as an internal copy for `allowinternalmotion`, not definitively a
previous-frame array. Primary absence cannot imply identity. Different secondary
matrices require further semantics; a conservative static subset rejects them.
BVH inherits geometry, adding an acceleration pointer at `0xe0`. Flattening the
complete polygon array does not need acceleration-tree traversal.

## Matrix convention and independent oracle

Each matrix occupies 64 bytes: triples at `0x00`, `0x10`, `0x20`, `0x30`.
Fourth floats are padding: [CitizenFX Vector3](https://github.com/citizenfx/fivem/blob/0105063b0394b1b9d085c917a8dc9c9abf0a620f/code/components/rage-formats-x/include/rageVectors.h)
even initializes them to NaN. Finite checks should apply to the twelve meaningful
components, not impose a homogeneous `0,0,0,1` padding pattern.

The [IV-to-V conversion](https://github.com/citizenfx/fivem/blob/0105063b0394b1b9d085c917a8dc9c9abf0a620f/code/components/rage-formats-x/include/convert/phBound_ny_five.h)
copies child matrices without transposition. Independently, Plugin-SDK's
[IV Matrix44](https://github.com/DK22Pac/plugin-sdk/blob/15f15b60bbf74c106e1b496ff92c98764abf4605/plugin_IV/game_IV/rage/Matrix44.h)
validates four vectors at the same offsets and computes:

```text
p' = right * p.x + forward * p.y + up * p.z + translation
```

This agrees with its IV matrix multiplication and Euler construction. The
unpadded `Matrix34` helper is 48 bytes and should not be mistaken for this
serialized structure. Keep vertices in GTA coordinates while applying matrices;
a later host/Skate coordinate conversion is a separate operation.

An independently calculated regression case: serialize basis triples
`(0,1,0), (-1,0,0), (0,0,1)` and translation `(10,20,30)`. Local triangle
`(1,2,3), (3,2,3), (1,4,3)` must become
`(8,21,33), (8,23,33), (6,21,33)`. Hard-code those expected points rather than
calling the decoder's transform function to manufacture expectations. This
tests rotation and translation together, including the transposition failure.

## Mesh contract and limits

[GTA4Unity geometry](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/Collision/PhBoundGeometry.cs)
places polygon pointer at `0x8c`, quantization scale at `0x90`, vertex offset at
`0xa0`, vertex pointer at `0xb0`, and counts at `0xc8`/`0xcc`. Its signed
16-bit vertex triples reconstruct as `quantized * scale + offset`.
The [CitizenFX NY example](https://github.com/citizenfx/fivem/blob/0105063b0394b1b9d085c917a8dc9c9abf0a620f/code/components/rage-formats-x/tests/NYBounds.cpp)
asserts geometry size `0xe0` and reads polygon buffers from composite BVH children.

The conversion source independently reads 32-byte NY polygons and splits quads
into `(0,1,2)` and `(2,3,0)` when the fourth index is nonzero. It does not settle
every packed-index flag; retaining an explicitly checked triangle subset is
a conservative starting point. For unflagged indices, the two readers agree on
the nonzero fourth-index sentinel and the two-triangle split above. The completed
slice supports that quad subset and retains refusal for all high-bit flags; a
quad cannot encode vertex zero as its fourth corner under this contract. Nested composites require
bounded traversal, cycle detection, and child-to-parent composition; deferring
them with an explicit unsupported result is reasonable for the first slice.

Validate pointer tags and complete spans before reads; bound aggregate output,
not just each child's allocation. Reject unsupported shapes and malformed child
records as a whole, preserving the existing invalid/unsupported distinction.
Restrict to finite rigid transforms if scale/shear/reflection semantics have not
been qualified. Unequal secondary matrix contents, sparse counts, shape coverage,
Complete Edition compatibility and world placement remain explicit unknowns.
An owned-resource success still needs an independent local exporter or host
collision comparison before feeding geometry into Skate; synthetic expectations
prove the algorithm's selected contract only.

## Independent placement investigation

A second read-only investigator corroborated matrix application through the
IV-to-V matrix copy above and the pinned
[CodeWalker child transform](https://github.com/dexyfex/CodeWalker/blob/485d56bec00262ed7fa472261cce7bbc6202b96e/CodeWalker.Core/GameFiles/Resources/Bounds.cs),
[stored matrix conversion](https://github.com/dexyfex/CodeWalker/blob/485d56bec00262ed7fa472261cce7bbc6202b96e/CodeWalker.Core/GameFiles/Resources/ResourceBaseTypes.cs)
and [SharpDX point transform](https://github.com/sharpdx/SharpDX/blob/ab36f12303e24aa60fe804866617716b6ded95db/Source/SharpDX.Mathematics/Vector3.cs).
This is independent corroboration of the formula, not a second IV file decode.
CodeWalker consumes V resources; the IV-specific Plugin-SDK formula above is
the more direct matrix reference.

[GTAIV-MapMover](https://github.com/renan-hath/GTAIV-MapMover/blob/78908805c96649bbb668e1bc74e88932cbf8cce9/GTAIV-MapMover/GTAIV_Map_Mover.py)
moves collision through exported centroid/vertex-offset fields separately from
WPL instance placement. This does not justify either blindly applying WPL
placements to WBN geometry or assuming every WBN is already world-space.
No source from these additional references was copied or executed.

## Host implementation and owned-file observation

Separate from the researchers' source-only work, the host implemented the public
command/parser slice and ran it read-only on the one existing private owned WBN.
The baseline verdict was `unsupported / unsupported-root`; the final verdict was
`structurally-decoded / validated-geometry`. An intermediate triangle-only version
returned `unsupported-quad`; the corroborated unflagged-quad split resolved that
refusal. The final decode checked all traversed children and meaningful matrices.
No coordinates, assets, private identities or raw diagnostics were emitted.

The slice accepts one composite level and geometry/BVH polygon leaves; nested
composites refuse. It decodes polygon buffers, not the BVH search tree, margins,
materials or contact semantics. Child boxes have finite/order checks only, not
an independently validated enclosure relation. This is not whole-resource
validation and not proof of active host collision. The algorithm's authored
rotation/translation and quad tests were observed red before their implementation
and green afterward; expected points were not generated by the decoder.

There is no preserved independent physical checkpoint for the selected street.
No game launch, staging, runtime query or Skate integration occurred. The next
proof must first qualify a separate local host-contact or exporter reference,
then identify the resource-to-street relationship and compare scale/orientation,
floor, curb/wall and a clear-space control. Agree the measurements and tolerances
before a runtime trial; the older physical-collision report's provisional 0.02 m
gate is not a measured result or permission to relax existing guards. An exporter
comparison can corroborate file coordinates but still cannot prove currently
active host collision. Until that evidence exists, placement remains blocked.
