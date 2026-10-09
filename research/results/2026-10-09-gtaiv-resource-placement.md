# GTA IV resource-to-street placement investigation

Observed: 2026-10-09. Public-source investigation and separate local read-only
trace for #20, on
`implement/gtaiv-composite-collision`, starting at
`47e8a2c0d46981ffb3b9cfeec5afd98eb91bffbb`. No game assets or private
identities are included. Public source was read; upstream programs, viewers,
converters and game runtimes were not executed.

## Finding

The inspected implementations distinguish static WBN bounds from placed
drawable instances and model-bound dictionaries. They support investigating
the WBN's decoded spatial footprint against nearby WPL instances; they do not
establish a reliable WBN-name-to-WPL-instance association or prove where this
particular resource is active in GTA IV. Applying an arbitrary WPL instance
transform to a WBN is not supported by the inspected paths.

The best available candidate investigation is to retain the exact archive-entry
provenance privately, inspect its collision footprint in GTA coordinates, and
compare nearby map instances/recognisable landmarks independently. Archive
membership and overlapping positions are candidate evidence, not a completed
street identification.

## Actual GTA4Unity loading path

All links in this section pin GTA4Unity at
`c107e46cf8ab4e3d42f9c0bf685f80bb732a3609`.

1. [GTADatLoader](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/IVUnity/GTADatLoader.cs)
   mounts IMG archives and caches entries in `gameFiles` by lowercase name. It
   loads base WPLs selected by gta.dat and other base-game streaming WPLs
   separately. This is the path from archive entries into the reconstructed
   map, not a direct WBN-to-WPL join.
2. [ECSWorldBootstrap](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/IVUnity.ECS/ECSWorldBootstrap.cs)
   calls `CollisionBuilder.StartBuild` during startup.
3. [CollisionBuilder](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/IVUnity/CollisionBuilder.cs)
   selects all cached `.wbn` entries, parses their geometry, merges vertices
   per resource and creates each collider entity at zero translation with the
   identity transform. It does not consult WPL instance transforms or match
   collision entry stems to placed models. Its `parent` parameter is unused.
4. [WorldEntityBaker](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/IVUnity.ECS/WorldEntityBaker.cs)
   separately resolves drawable model hashes/names and creates instances using
   WPL positions and rotations.

This is concrete third-party treatment of static WBN geometry as spatially
placed data, independent of drawable placement. It is not GTA IV runtime
loader evidence. Its collider selection also uses all cached WBNs, while the
WPL loading path filters base-game WPLs, another reason to avoid treating this
reconstruction as authoritative evidence of current host collision.

### Important composite-reader limitation

[CollisionFile](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/Collision/CollisionFile.cs)
reads the bound pointer at root +8. Its comment calls this a dictionary, which
should not be treated as proof of a dictionary-based resource association.
[PhBoundComposite](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/Collision/PhBoundComposite.cs)
enumerates children but **does not apply their matrices**.
[PhBoundGeometry](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/Collision/PhBoundGeometry.cs)
unquantizes vertices and changes axes to Unity `(-x,z,-y)` only. Therefore this
pinned viewer cannot independently validate transformed composite placement.
Identity placement of its collider entities is evidence of its design, not
proof that its decoded composite vertices are correctly located.

## WPL fields usable for a bounded private correlation

[IPL](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/IVUnity/IPL/IPL.cs)
reads 17 little-endian 32-bit header words (68 bytes). Version is at byte 0,
INST count at byte 4, and BLOK count at byte 64. INST records follow the header.
[Ipl_INST](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/IVUnity/IPL/Items/Ipl_INST.cs)
reads each 48-byte record as follows:

| Record offset | Field |
| --- | --- |
| 0 | Three float32 position components, GTA x/y/z |
| 12 | Four float32 quaternion components, x/y/z/w |
| 28 | Unsigned 32-bit model hash |
| 32 | Signed 32-bit flags |
| 36 | Signed 32-bit LOD index |
| 40 | Signed 32-bit unknown field |
| 44 | Float32 unknown field |

These records can narrow the search to nearby placed models. Their positions
are model origins, not mesh extents, so proximity or absence of nearby origins
cannot establish or disprove geometric overlap. A defensible local inspection
must first check the version, counts, complete spans and finite position values;
this note does not qualify arbitrary WPL files or all trailing sections.

The pinned [Ipl_BLOK](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/IVUnity/IPL/Items/Ipl_BLOK.cs)
is explicitly unsupported and consumes no binary fields. It supplies **no
usable BLOK layout or bounds/reference association**. Inferring those fields
from this source would invent evidence.

## Independent converter corroboration

CitizenFX is pinned at `0105063b0394b1b9d085c917a8dc9c9abf0a620f`.
Its [conversion dispatch](https://github.com/citizenfx/fivem/blob/0105063b0394b1b9d085c917a8dc9c9abf0a620f/code/components/tool-formats/src/ConvertFormats.cpp)
defines NY WBN roots as `datOwner<phBound>` and WBD roots as
`pgDictionary<phBound>`. Static WBN conversion reads the bound directly;
dictionary conversion emits individual hash-named bounds. A separate optional
drawable conversion path looks up a dictionary entry using the drawable's
basename and attaches that bound to the drawable. The similarly named
`g_wbnFile` option variable does not change its actual WBD dictionary cast.

The [NY-to-Five bound conversion](https://github.com/citizenfx/fivem/blob/0105063b0394b1b9d085c917a8dc9c9abf0a620f/code/components/rage-formats-x/include/convert/phBound_ny_five.h)
preserves composite child matrices and defaults explicit horizontal translation
offsets to zero. User-selected `bound_x`/`bound_y` offsets modify vertex offsets,
centroids, centres of gravity and AABBs. The static WBN path does not read a WPL
or apply a drawable instance transform. This corroborates preservation of
resource spatial coordinates but is an IV-to-V converter, not evidence of GTA
IV's active loader or contact semantics. No converted asset was produced.

[GTAIV-MapMover](https://github.com/renan-hath/GTAIV-MapMover/blob/78908805c96649bbb668e1bc74e88932cbf8cce9/GTAIV-MapMover/GTAIV_Map_Mover.py)
separately translates exported OPL instance coordinates and OBN centroid/vertex
offset fields. It has no binary WBN/WPL parser and no association or runtime
verification. It is corroboration of separate map-placement data paths only.

These are existing evidence pins; no pin was moved. GTA4Unity's GPLv3 and
CitizenFX's applicable source licences govern their code, not game asset rights.
No implementation was copied into project source.

## Unresolved links and stop condition

- A private exact archive-entry match can establish acquisition provenance; it
  does not by itself name the street.
- No inspected source establishes a universal WBN-stem-to-WPL-stem rule.
- No usable BLOK association was obtained from the inspected WPL parser.
- No authoritative GTA IV runtime loader path was verified in this investigation.
- Nonidentity child transforms prevent the pinned GTA4Unity viewer from being
  an independent transformed-composite placement oracle.
- Recognisable street landmarks and an independently supported coordinate
  placement remain necessary before checkpoint measurement tooling. Ground
  contact, walls and host gameplay acceptance remain separate later proofs.

The private investigation can use spatial correlation to propose a candidate,
but if that candidate cannot be tied to an independently identifiable street
and placement, the experiment remains inconclusive and stops at location.


## Local trace by the host agent

The background investigator inspected public source only. Separately, the host
agent reused the retained private acquisition definitions for bounded reads of
the one source archive; it did not rerun acquisition or modify the installed
archive. The temporary WPL field inspection followed the layout above and was
an investigative command, not a new supported parser or measurement tool.

Verified local observations:

- The retained WBN SHA-256 matches the acquisition record. The archive size and
  modification timestamp match the retained record, and the bytes at the recorded
  archive entry independently reproduce that WBN digest. The archive entry name
  and exact provenance were retained privately.
- The archive contains 11 WBN and 9 WPL entries. The selected WBN has no same-stem
  companion entry. A bounded scan of 271 loose map-data files found no reference
  to the selected resource name/stem; it found archive references, including one
  uncommented IMG directive naming that archive. This is a configuration record,
  not verification that the live game has activated that configuration/resource.
- Existing decoder `decode_resource` produced resource-coordinate bounds with
  child transforms applied. Every explicit child matrix in this owned resource
  is exactly identity. The matrices were read and compared, not substituted.
  That makes the viewer's matrix omission inert for this field on this input
  only; it does not qualify the rest of that viewer or prove world placement.
- The 9 archived WPL entries passed the bounded version-3, count/span and finite
  position/quaternion checks for 3,324 INST records. No trailing-section or BLOK
  validation is claimed. Under the hypothesis that decoded WBN coordinates are
  world coordinates, 564 instance origins fall inside its horizontal bounds,
  across four WPL entries. These are model origins, not independently decoded
  surfaces; the result does not identify a unique street or verify the hypothesis.

The local provenance, registration, bounds, matrix classification and instance
correlation records remain in the ignored private experiment directory. No game
bytes, identities, coordinates or raw records were sent to reviewers or committed.
No upstream viewer/converter, game launch, native measurement, staging or Skate
integration ran. No production source or tests changed; TDD was not reached
because the owner's location prerequisite remains unmet.

**Verdict: inconclusive at location.** Acquisition provenance is recovered and a
candidate map area can be investigated privately. The exact missing link is an
independently recognisable street/landmark match with qualified coordinate
placement for this resource. Use the retained candidate records for that check;
repeating acquisition or merely comparing more model origins will not supply it.
If a qualified local viewer/reference cannot establish that match, retain the
inconclusive result and stop before measurement tooling.

After location is established, select distinctive road, pavement and height-change
checkpoints. Freeze numeric comparison tolerance and repeatability rules before
sampling GTA at the same coordinates as the mesh predictions. Unavailable results
cannot pass. Report agreement, disagreement or inconclusive; any agreement covers
those ground checkpoints only. Walls remain the next proof.
