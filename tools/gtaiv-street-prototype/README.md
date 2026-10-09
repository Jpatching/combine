# GTA IV street collision experiment

Throwaway experiment for [#20](https://github.com/Jpatching/combine/issues/20),
2026-10-09. **Verdict: blocked at collision layout, before world placement or
runtime integration.** No GTA ride, rendered board, animation or wall contact
was demonstrated. No PR exists for this experiment.

The owner selected real offline GTA IV with the existing Skate simulation.
The first gameplay target is one real street: visible board and recognisable
skating animation, push/steer, ollie onto pavement, stop against a wall,
dismount, then enter and drive a GTA car. Traffic and pedestrians remain active;
physical Skate interaction with moving objects is deferred. This target extends
the older issue's placeholder presentation; it does not claim that work is done.
The immediate experiment asks whether actual GTA street collision can reach the
pinned Skate Session correctly. A supporting tool alone cannot pass that test.

## Observations

- Read-only header classification of 119 local map archives found no plain IMG
  v3 headers. That initial result alone did not establish encryption or corruption.
- Reviewed the pinned RageLib header, table, entry and local archive-decoding
  implementation. A private bounded adaptation successfully read the first
  archive and copied one WBN into ignored local storage. The exact-version local
  reader prerequisite validated. No executable or installed archive was modified;
  keys, paths, archive entries, resource identities and game bytes remain private.
- The unmodified inspector at `fcb4acc0c643d7244a8cae1db83c9e08b1a07887`
  returned `invalid / decompression-error` for that owned resource.
- Bounded local inspection found a complete stream of the declared size and a
  four-byte trailer matching its Adler-32 checksum. The inspector starts after
  the zlib header, inflates raw DEFLATE, then rejects that valid trailer.
- An authored fixture reproduced the same failure. A temporary correction uses
  the complete zlib stream, including header and checksum. The fixture then
  reaches `unsupported / unsupported-root`; bad checksum, truncation, missing
  checksum and appended data remain rejected.
- The same temporary correction on the owned resource reaches
  `unsupported / unsupported-root`. A bounded root-type check identifies a
  composite. Geometry has **not** been decoded. The pinned composite reader
  enumerates children but does not apply their matrices, so it cannot establish
  their placement. No children were flattened or silently skipped.
- A read-only Windows check found GTA closed. OpenIV was absent from three
  conventional installation paths; this is not an exhaustive software inventory.
  No game launch, input, staging or runtime capture occurred in this experiment.

## Reproduce the framing finding

Requires Python 3, Git, and the inspector Git object above in this repository.
No downloads or third-party Python packages are needed for this reproduction.

```sh
python3 tools/gtaiv-street-prototype/reproduce_framing.py
# Optional: the single private resource acquired during this experiment.
python3 tools/gtaiv-street-prototype/reproduce_framing.py /private/resource.wbn
```

The script loads the exact inspector source into a temporary directory and
changes only the zlib framing there. It does not modify the inspector branch or
install a fix. Exit zero means the authored framing checks passed; read the
separate optional resource verdicts. It does not mean geometry or gameplay passed.
The authored fixture deliberately has an unsupported composite marker and no
geometry. Keep actual resources outside Git and AI uploads.

Private acquisition code and evidence are retained in the ignored
`.private/gtaiv-street-collision/` directory. Publicly preserved code is the
source-safe framing reproduction, not an archive extractor or playable adapter.

Verification: the reproduction passed with authored data and with the optional
owned-file inspection (whose corrected verdict remains unsupported).
`python3 scripts/verify.py` passed 54 tests and link/context checks across 59
documents on this main-based experiment branch. These differ from the inspector
branch's earlier 61 tests because its seven tests are not merged into main.

## Next decision

The acquisition obstacle has moved: a local resource is now available, but its
composite layout and child transforms are unsupported. Correct the framing
defect in the existing inspector candidate through its review flow. Before
feeding any triangles to Skate, establish bounded composite/transform decoding
and validate a selected street's placement against actual GTA physical contact.
If those transforms cannot be established, reconsider the acquisition route.
Do not infer identity transforms, relax the flatness guard, or substitute a
synthetic floor. The full street milestone still requires runtime proof.

Preserve draft [#37](https://github.com/Jpatching/combine/pull/37), the earlier
runtime candidate and draft [#23](https://github.com/Jpatching/combine/pull/23).
This experiment neither merges nor accepts either candidate.

## Provenance

The reproduction is GPL-3.0-only, matching the inspector it temporarily loads.
The inspector carries its own licence and attribution in its pinned tree.
Format references below are from GTA4Unity/RageLib at
`c107e46cf8ab4e3d42f9c0bf685f80bb732a3609`; RageLib's archive/resource headers
credit Copyright (C) 2008 Arushan/Aru and GPL-3.0-or-later.
Source licences do not establish rights to game assets.

- [IMG header](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/FileSystem/IMG/Header.cs),
  [table](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/FileSystem/IMG/TOC.cs),
  [entry](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/FileSystem/IMG/TOCEntry.cs),
  [archive reader](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/FileSystem/IMG/File.cs).
- [Resource reader](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/Common/Resources/ResourceFile.cs),
  [bound types](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/Collision/BoundType.cs),
  [composite reader](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/Collision/PhBoundComposite.cs).
