# Bounded GTA IV collision resource inspection

Run `python3 tools/gtaiv-collision/inspect_resource.py <local-file>` (Windows:
`py -3 tools/gtaiv-collision/inspect_resource.py <local-file>`). The file must already
be extracted and remain outside Git. The command reads one regular file and prints
only JSON `verdict` and `reason` fields. It never prints paths, names, identifiers,
bytes, counts or geometry. Exit codes: 0 structurally decoded, 2 unsupported,
1 invalid. Paths beginning with `-` must be expressed as an absolute path.
There is no archive extractor, network operation, game hook or asset output.

The public Python parser `decode_resource(bytes)` returns an `Inspection` of
vertices/faces in unchanged RAGE coordinates or raises `Refusal` with `verdict`
and `reason`. Use that interface only in private local tooling or with authored
synthetic data. Its return value must not be uploaded, logged publicly or committed.
The CLI deliberately publishes only the bounded verdict.

## Supported evidence and conservative limits

The read-only parser supports little-endian RSC5 bounds (`0x20`), checksummed
zlib (`0xda78`), and a tagged system-memory root at dictionary offset 8.
Geometry (`4`) and BVH (`10`) roots decode their polygon buffers. A single
composite (`12`) may contain geometry/BVH children with explicit rigid transforms.
Nested composites and other child shapes refuse the whole resource.

Signed 16-bit vertices reconstruct as quantized coordinates times axis scale,
plus geometry center. For composite children, the parser then applies the stored
basis vectors and translation, retaining GTA coordinates. Both composite count
fields must agree. The primary matrix is required; the secondary matrix must be
absent, alias it, or have identical meaningful components. The four padding words
are ignored, including NaN padding. All twelve meaningful components must be
finite. Basis dot products must match an orthonormal basis and determinant +1
within `1e-5`; scale, shear and reflection return unsupported.

Unflagged triangles use a zero fourth-index sentinel. Unflagged quads use a
nonzero fourth index and split into `(0,1,2)` and `(2,3,0)`, following corroborated
IV readers. Every index must be in range; triangle/quad corner indices must be
distinct and every output triangle nondegenerate. High-bit index flags remain
unsupported. Stored polygon normals must be finite and nonzero. Transformed
vertices and triangles are rechecked for finite values and precision collapse.

Limits: **16 MiB** input, **32 MiB** declared/inflated memory, **256** children,
**32,767 total output vertices**, and **100,000 total output triangles**, including
quad expansion across children. Counts and complete buffer spans are checked
before relevant array construction. There is no recursive traversal. Null child
pointers, invalid pointer tags, truncated arrays, overlapping consumed spans and
inconsistent counts refuse; a failed child never becomes a partial world.
Aliasing primary/secondary matrices is explicitly allowed; shared mesh buffers
are conservatively rejected. Child boxes must have finite, ordered bounds.

The complete zlib stream, starting at byte 12, must validate its checksum and
consume exactly the declared size. Missing/corrupt checksums, incomplete streams,
trailing data and concatenated streams are invalid. Unsupported versions, types,
codecs, shapes and transform semantics return unsupported. Neither refusal
supplies an empty or replacement world.

**What the verdict covers:** the consumed polygon buffers and transforms, not
all collision-resource structure or fidelity. BVH search trees are not traversed
or validated; materials, adjacency, margins and unused pointers are not decoded.
Child boxes are checked structurally, not for enclosure of the decoded mesh.
The tool is not a validator for installing an original WBN in GTA.

## Owned-file evidence and remaining gate

On 2026-10-09 the same private owned resource from the
[street experiment](https://github.com/Jpatching/combine/issues/20#issuecomment-6087765258)
changed from `unsupported / unsupported-root` to
`structurally-decoded / validated-geometry`. Its composite children are BVH meshes;
an intermediate triangle-only candidate refused quads, before the source-backed
quad extension. The final check applied the explicit child transforms and
completed the bounded geometry checks. Only the verdict was emitted; no owned
bytes, coordinates, geometry, paths or identities were published. Acquisition
remains separate from this inspector; no game was launched or runtime changed.

This is an owned-file decoding result, **not independently verified street
placement**. There is no existing physical checkpoint proving that this resource
supplies the selected street's active collision. Before Skate integration, qualify
an independent local host-contact or exporter reference, compare scale/orientation
and floor/curb/wall plus a clear-space control, and record a separate verdict.
The [source investigation](../../research/results/2026-10-09-gtaiv-composite-transforms.md)
separates source facts, algorithm tests and that remaining physical proof.

## Source provenance and licensing

New standalone Python implementation, 2026-10-09, for
[issue #34](https://github.com/Jpatching/combine/issues/34), licensed
**GPL-3.0-only** under the accompanying [full license](LICENSE).
Format/reference source is Infinity-Loops/GTA4Unity and its vendored RageLib,
immutable revision `c107e46cf8ab4e3d42f9c0bf685f80bb732a3609`:

- [CollisionFile.cs](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/Collision/CollisionFile.cs)
- [PhBoundGeometry.cs](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/Collision/PhBoundGeometry.cs)
- [PhPolygon.cs](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/Collision/PhPolygon.cs)
- [ResourceHeader.cs](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/Common/Resources/ResourceHeader.cs)
- [ResourceUtil.cs](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/Common/Resources/ResourceUtil.cs)
- [CompressionDeflateCodec.cs](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/Common/Compression/CompressionDeflateCodec.cs)
- [Upstream GPLv3 license](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/LICENSE)

Inherited RageLib attribution: **Copyright (C) 2008 Arushan/Aru**. Its resource
headers grant GPL version 3 or later and disclaim warranty. The newer collision
files have no individual notices; their repository root carries GPL version 3,
and no contrary terms were found in the inspected files or README. This isolated
tool uses GPL version 3, compatible with those inherited terms. No author identity
or broader license grant is inferred. This license applies to this tool, not other
Combine code, its runtime or GTA assets. There is no warranty; source licensing
does not establish publisher/asset rights.

Changes from the reference are a standalone Python parser with bounded input and
inflation, strict spans/tag/count/face validation, conservative unsupported results,
explicit rigid child transforms, no export and private diagnostics suppressed.
The permissive Unity loops and silent child skipping are not reproduced. Public source was read as text; no upstream project was executed.

Additional format corroboration and matrix provenance are pinned in the
[source investigation](../../research/results/2026-10-09-gtaiv-composite-transforms.md).
CitizenFX source was read for format facts only; no CitizenFX implementation was
copied or linked. The new Python traversal, transforms and tests were independently
authored. Existing GPLv3 terms and RageLib attribution remain applicable.

## Verification

`python3 tests/test_gtaiv_collision.py -v` exercises the agreed public parser and
command boundaries with authored data. The base triangle is `(1,2,3)`, `(3,2,3)`,
`(1,4,3)`. A +90-degree Z rotation followed by `(10,20,30)` translation must produce
`(8,21,33)`, `(8,23,33)`, `(6,21,33)`, specified independently of the decoder.
The transformed-child test failed before implementation and passed afterward.
The quad test likewise failed before its bounded extension. Refusal tests cover
malformed transforms, internal motion, child spans, total counts, shared buffers,
unsupported children/flags, invalid quads and transformed precision loss.
The command returns only a verdict even after an earlier child succeeds.

All 19 focused tests passed. `python3 scripts/verify.py` is the repository gate.
No Python typechecker is configured here. Synthetic tests and the owned-file
verdict do not establish placement, active GTA collision, physical units/winding,
Skate contact, streaming, traffic/doors, grind semantics or gameplay acceptance.
