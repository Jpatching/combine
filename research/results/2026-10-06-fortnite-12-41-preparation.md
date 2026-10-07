# Fortnite 12.41 isolated acquisition and verification

Observation date: 2026-10-06. Owner selected Windows **CL12905909** for
download and integrity verification. No game launch, login, protection changes,
runtime API changes or private asset upload are part of this slice. The working
mashup and existing Fortnite clients are preserved; writes are confined to a new
ignored `.private/fortnite-12.41/` directory and redacted project evidence.

## Inputs and provenance

- Authorized source: `https://cdn.cbn.lol/12.41`, redirecting to
  `https://r2.cbn.lol/++Fortnite+Release-12.41-CL-12905909-Windows.zip`.
- HTTP declared archive size: **42,516,907,454 bytes**. Server ETag:
  `aa41aa8da6ee8a3062649ed6ce81517c-5069`; Last-Modified:
  `Thu, 14 Aug 2025 18:44:03 GMT`. The multipart ETag is not an archive checksum.
- Exact-build comparison reference: [VastBlast/FortniteManifestArchive](https://github.com/VastBlast/FortniteManifestArchive),
  pinned repository revision `b228ac917383377dec99f29e88c7f1394b141d16`,
  [manifest jTfg_xZZ2H4T9L__PEmzI2Y90hr9Aw](https://github.com/VastBlast/FortniteManifestArchive/blob/b228ac917383377dec99f29e88c7f1394b141d16/Fortnite/Windows/jTfg_xZZ2H4T9L__PEmzI2Y90hr9Aw.manifest).
  Git blob `d693a965c035aacf3433003789a6a6d8f8b31118`;
  downloaded manifest **30,444,005 bytes**, SHA-256
  `16865435438ea2a6d2c638a7bf1237c2a9a1a91c7f6cd0fafe7cf304f7ae2120`.
- Manifest identifies `++Fortnite+Release-12.41-CL-12905909-Windows`:
  **398 files / 89,276,937,798 bytes**. Its file hashes use SHA-1;
  the one-off verifier decodes the decimal byte strings before comparison.

This is comparison with a community-archived manifest, not independently
authenticated publisher distribution provenance. A locally calculated archive
SHA-256 identifies the downloaded bytes; it is not a publisher-supplied checksum.

## Preparation and checks

Initial free Linux space: **657,337,872,384 bytes**. HTTPS HEAD and range reads
established the download size and ZIP64 directory before extraction. Python's
ZIP reader required absolute ZIP64 offsets; a sparse local metadata-only file
allowed inspection without allocating the 42.5 GB payload twice.

Directory preflight: **511 entries, 437 files, 89,698,972,585 extracted bytes**.
The archive wrapper is stripped when writing the isolated extraction directory.
Before extraction, reject traversal/absolute/device paths, backslashes, alternate
data streams, duplicate/case-colliding names, file/directory collisions, links,
special files, encrypted entries and unexpected compression. Check free space
again with a 10 GiB reserve. Never overwrite an existing extraction directory.

```text
HTTPS archive -> resumable .part -> size + SHA-256 + path/space checks
  -> fresh private extraction with ZIP CRC and manifest SHA-1 comparison
  -> extracted-file SHA-256 readback -> separate Windows version/signature check
  -> integrity result; no launch
Failure -> stop, retain isolated files and private diagnostics
```

The private verifier uses Python's standard ZIP reader to check CRC on every
stream. It records SHA-1/SHA-256 and compares manifest file sizes and SHA-1.
It checks the shipping executable first and stops if that manifest identity
differs. A second read hashes extracted files to verify disk output. The nested
extra archive is treated as an opaque file and is not unpacked.

Commands and private evidence are retained under `.private/fortnite-12.41/`:

```sh
curl --fail --location --proto '=https' --proto-redir '=https' \
  --continue-at - --retry 5 --retry-delay 5 --connect-timeout 30 \
  --speed-limit 1024 --speed-time 120 --silent --show-error \
  --dump-header .private/fortnite-12.41/download-headers.txt \
  --output .private/fortnite-12.41/archive.zip.part https://cdn.cbn.lol/12.41
python3 .private/fortnite-12.41/verify-local.py --preflight
python3 .private/fortnite-12.41/verify-local.py
python3 .private/fortnite-12.41/check-identity.py
```

These are one-off local helpers, not a new public installer. Verification refuses
an existing output directory; do not rerun extraction over an installation.
The Windows helper reads version resources and `Get-AuthenticodeSignature`;
it does not execute the shipping executable.

## Final results

**Downloaded, but rejected for this preparation slice.** Verification stopped
on the first extracted file: the shipping executable differs from the archived
exact-build manifest. No complete installation or playable trial was prepared.

The HTTPS download exited **0** and produced exactly **42,516,907,454 bytes**.
The complete archive was read once to calculate SHA-256:
`490125c6c81b0a85908a4542c31ad642ed9818d2a88ae99544664afd270281de`.
It is retained privately as `archive.rejected.zip`; it is not an incomplete
download despite originally using the resumable `.part` filename.

| Comparison | Result |
| --- | --- |
| Manifest filenames present | 398 / 398 |
| Missing filenames | 0 |
| Extra files | 39 |
| Manifest contents fully matching | 0 verified before stop |
| Modified manifest files | 1 verified: shipping executable |
| Remaining contents unchecked | 397 manifest files + 39 extras |
| ZIP CRC | Shipping executable passed; remaining 436 files unchecked |
| Extracted disk readback | Shipping executable SHA-1 reproduced the mismatch |

Shipping executable size is **159,640,832 bytes**, matching the declared
manifest size. Expected SHA-1:
`88e69fa47c475d76b6963a470b0b5bb21d1c3cb2`.
Observed SHA-1:
`3b390bf9d1e72b4b0ab7cfd1bc5c807d47a10c91`.
Observed SHA-256:
`78f00934fa00f0c184e6b0a7219048a17066f6bba6a13d4408735928f295cdfe`.
The 39 extras comprise seven settings/diagnostic files under Win64, one nested
archive under Paks, 26 cached CMS files and five downloaded EMS configuration
files. Their contents were not inspected or extracted. No pristine-package or
publisher-provenance claim is made.

The verifier exited **1** with `Shipping executable manifest identity mismatch;
stop`. Only the shipping executable was extracted, into `extracted-unaccepted/`.
Private `archive-summary.json`, `comparison.json`, `verification-failure.json`,
inventories and logs retain the diagnostics. The one-off verification helper's
executed SHA-256 is
`425706b4d19e8a0616c350dbba267e9e83fc3bb3e914cca45af1368490fd5206`.
Ten unsafe-path examples plus manifest byte decoding, case collision, symlink
and file/directory collision checks passed. The manifest's raw bytes also
reproduced its pinned Git blob hash.

Separate Windows `Get-AuthenticodeSignature` inspection returned
**`HashMismatch`**, with an embedded Epic Games Inc. signing certificate and
Symantec timestamp certificate. An embedded certificate does not make the
altered file's signature valid. Windows SHA-256 independently matched the Linux
result above. FileVersion, ProductVersion, ProductName and CompanyName were all
empty; executable version resources therefore cannot establish the build.
The identity helper exited **1** because it could not confirm the requested
identity. These checks establish an integrity failure, not why the file changed
or a malware diagnosis. No client code was executed.

The owner asked whether another full read is necessary: **no after this stop
condition**. A full CRC scan would be necessary to claim complete ZIP integrity,
but cannot repair or override the identified executable mismatch.

## Boundaries and next step

Integrity-checked files do not establish playability, ban safety, distribution
rights or an approved local-server startup route. No account, game executable,
loader, server, nested archive or included script is executed in this slice.
Original installations, pins and runtime interfaces remain untouched.

Next: resolve the executable mismatch or obtain a manifest-matching
**12.41 CL12905909** package before continuing preparation. The intended
local-server startup review remains subsequent to successful verification;
no startup trial is prepared from this rejected copy. Preserve the
no-DRM/anti-cheat-bypass boundary; missing adapters are subsequent build work
under the existing qualification contract.

## Source handoff

Evidence branch: `slice/fortnite-12-41-preparation`, base
`93f4b0c28d10bcc9ae3860090d8f1d3f02ac4e0f`. This slice changes only this report,
the decision record and handoff. Prior source history is stacked on unmerged
work; no merge is requested. Upstream HEAD was refreshed and remains
`f608f85e407ff1b7689d54a9aafdd16e95711ac4`; runtime pin unchanged.
Lead review checks the report against private JSON, the stop condition, asset
exclusions and absence of runtime changes. Repository gate result and source
publication are recorded in the current handoff and live board.

The older board helper rejected the owner's customized visible fields before
writing. A bounded private wrapper reused its snapshot/field-write/read-back
functions, preserving every view, field and other item. No board layout was reset.
