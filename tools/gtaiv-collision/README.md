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

This experiment supports only little-endian RSC5 bounds (`0x20`), raw DEFLATE
(`0xda78`), a tagged system-memory root pointer at dictionary offset 8, and root
Geometry (`4`). Quantized signed 16-bit triples are scaled per axis and translated
by the geometry center. Polygon records are 32 bytes; only unflagged triangles
with a zero fourth index are accepted. No Unity coordinate conversion is applied.
The supported layout is source evidence, not exact-version owned-input evidence.

The file cap is **16 MiB**, declared/inflated total memory **32 MiB**, vertices
**32,767**, polygons **100,000**, and traversal exactly **one geometry root**.
Header sizes and counts are checked before decompression/array construction.
Decompression reads at most declared size plus one byte, requires complete raw
DEFLATE and rejects extra data. The pinned codec uses raw mode for both its
writer and reader (`Deflater(..., true)` / `Inflater(true)`), with codec
`0xda78` written separately by ResourceHeader; zlib wrappers and trailers
are outside this supported format. System pointers must have tag 5 and a nonzero
in-range offset; dictionary, geometry, vertex and polygon spans must be disjoint.
Decoded coordinates and polygon normals must be finite; normals and face
cross products must be nonzero, indices in range and triangle vertices distinct.
These are conservative investigation caps, not measured gameplay budgets.

Other versions, resource types, codecs, box/BVH/curved geometry, spheres, capsules,
unknown roots and **all composites** return unsupported. Composite child transforms
are never traversed or assumed identity. Quads and index flags also refuse because
the source's fourth-index convention is ambiguous at vertex zero and flag meanings
have not been qualified. Empty geometry, bad spans/counts/indices, degenerate faces,
truncation and decompression failures return invalid. Neither outcome supplies an
empty or replacement world. The command only validates the specified subset;
unused fields/adjacency/materials are not a fidelity claim.

No extracted owned resource is available for this session's structural test.
The coordinator's approved read-only installation check found no loose WBN/WBD
resources. Existing archives were not opened or extracted. Therefore no owned
resource decode or compatibility result is claimed; the next step is obtaining
one extracted resource through reviewed tooling. This experiment does not prove
placement, active GTA collision, units/winding, Skate contact, streaming,
traffic/doors, grind semantics or gameplay.

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
no geometry conversion/export and private diagnostics suppressed. The unsafe
Unity loops, permissive unknown-root behavior and composite traversal are not
reproduced. Public source was read as text; no upstream project was executed.

## Verification

`python3 -m unittest discover -s tests -p test_gtaiv_collision.py -v` tests the
agreed command/parser boundaries using authored fixtures only. The fixture's
independently specified triangle is `(1,2,3)`, `(3,2,3)`, `(1,4,3)`; expectations
are not generated by the decoder. Each behavioral slice was observed failing
before implementation, then passing. The repository gate is
`python3 scripts/verify.py`. Neither check supplies owned-resource or runtime proof.
