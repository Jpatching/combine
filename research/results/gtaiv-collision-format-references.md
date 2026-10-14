# GTA IV collision format references

These pinned external sources explain constraints that cannot be inferred from
our decoder alone. They establish format evidence, not live CE 1.2.0.59 contact.
Use the [collision tool](../../tools/gtaiv-collision/README.md) for supported inputs
and commands; [#39](https://github.com/Jpatching/combine/issues/39) owns host-ground
qualification and [#61](https://github.com/Jpatching/combine/issues/61) owns current evidence.

## Composite matrices

[CitizenFX's NY phBound definitions](https://github.com/citizenfx/fivem/blob/0105063b0394b1b9d085c917a8dc9c9abf0a620f/code/components/rage-formats-x/include/phBound.h)
describe GTA IV geometry/BVH/composite types and padded child matrices.
The [NY-to-Five converter](https://github.com/citizenfx/fivem/blob/0105063b0394b1b9d085c917a8dc9c9abf0a620f/code/components/rage-formats-x/include/convert/phBound_ny_five.h)
copies child matrices without transposition. Independently, [Plugin-SDK's IV Matrix44](https://github.com/DK22Pac/plugin-sdk/blob/15f15b60bbf74c106e1b496ff92c98764abf4605/plugin_IV/game_IV/rage/Matrix44.h)
places basis/translation triples at 16-byte intervals and computes
`right*x + forward*y + up*z + translation`. Fourth floats are padding;
[CitizenFX Vector3](https://github.com/citizenfx/fivem/blob/0105063b0394b1b9d085c917a8dc9c9abf0a620f/code/components/rage-formats-x/include/rageVectors.h)
can initialize them to NaN. Do not confuse the padded 64-byte matrix with a
48-byte Matrix34 or apply a second host-coordinate conversion.

The two composite count fields have conflicting names in the inspected readers;
count/capacity equality is a conservative supported subset, not settled semantics.
Secondary child matrices are associated with internal motion; disagreement with
primary matrices needs further interpretation rather than an identity fallback.

CitizenFX's [licence](https://github.com/citizenfx/fivem/blob/0105063b0394b1b9d085c917a8dc9c9abf0a620f/LICENSE)
places this directory under the Creator Platform License, outside its listed LGPL
exceptions. These are format references for independently authored code, not
permission to copy implementations. [Plugin-SDK's licence](https://github.com/DK22Pac/plugin-sdk/blob/15f15b60bbf74c106e1b496ff92c98764abf4605/LICENSE)
and game-content rights remain separate.

## Resource placement

At GTA4Unity `c107e46cf8ab4e3d42f9c0bf685f80bb732a3609`,
[CollisionBuilder](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/IVUnity/CollisionBuilder.cs)
places decoded WBN colliders at identity, separately from WPL drawable instances.
Its [composite reader](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/Collision/PhBoundComposite.cs)
omits child matrices, so its viewer cannot independently validate transformed
composite placement. Static WBN bounds and WBD model-bound dictionaries require
distinct placement evidence; there is no established universal WBN-name-to-WPL
instance join. Nearby model origins and archive membership do not prove contact.

Preserve exact private resource provenance and independently compare placement,
scale, height layer and loaded host contact. A structurally decoded resource does
not establish active collision, curb/wall support or moving-object behavior.
The [physical collision feasibility reference](gtaiv-120059-physical-collision-feasibility.md)
retains the broader source comparison; its proposed proofs are historical decision
inputs, while the owning issues select current work.
