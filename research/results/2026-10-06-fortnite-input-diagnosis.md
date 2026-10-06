# Fortnite input diagnosis — 2026-10-06

**Result: input route blocked.** The identified 3.1 input mounts 0/10 game
containers, indexes zero files and finds no worlds. Independent version-4 footer
checks confirm all ten containers carry an encrypted-index flag. The pinned parser
deliberately skips these before reading the index without a supplied key/custom
handler. No supported compatibility correction was found; no key was obtained,
flag changed, payload decrypted, installation changed or asset uploaded.
No island, terrain/building export or collision witness exists.

## Identity and reviewed execution

Observed from 10:26 UTC. Private identity record names
`++Fortnite+Release-3.1-CL-3917250-Windows`: 3,323 manifest/archive files, no
recorded missing/extra files, matching shipping SHA-1
`b017f433b1238c0eed9f43fdb80df3ea1d90361e`. Reference manifest SHA-256:
`4dd1ab60ef742b6bc56f2565be29b60896b3ce57f5e31bf7a2ba07fffe2a6ff0`.
These identity/membership/shipping results are inherited metadata, not a fresh
archive-wide verification or acquisition-rights finding. This session freshly
rehashed all ten game containers with Python `hashlib.file_digest(..., 'sha1')`;
10/10 match the private recorded reference hashes. Raw filenames/hashes/logs stay
in ignored private diagnostics. Original archive and earlier attempts remain.

Reviewed inherited, still-untracked `Program.cs`, `check_runner.py`, project and
dependency lock before execution. Runner mounts/indexes only in inventory mode,
does not submit keys or initialize downloadable codecs, and rejects incomplete
inventory. Source parser is a clean Apache-2.0 checkout pinned at
`e4ea4ba8ec2b88d08b2066dfb8962863dccb36cc`; pinned source and package/build
configuration inspected. Lock records exact resolved transitive packages; root
Microsoft.Bcl.Memory is 9.0.14. The inherited executable dependency manifest also
resolves 9.0.14. Other-game encryption branches are not selected. This is a
bounded source/dependency review for inventory, not a comprehensive security or
distribution clearance for every exporter/codec path.

Reproduction used inherited `FortniteExport.dll` SHA-256
`c2770504727fd365128c12c10f651fd813e18aedba42bf8b5c6dab487cecb1e7`
and local .NET SDK 10.0.401. A fresh source build was attempted, but blocked:
first .NET's default first-use cache was read-only; retry with a writable
DOTNET_CLI_HOME exposed missing inherited NuGet cache/analyzer assemblies
(`CS0006`, MemoryPack.Generator.dll missing). Upstream project restore metadata
also reports NU1903 for transitive Microsoft.Bcl.Memory 9.0.0; root runner has
the 9.0.14 override. No fresh runner build or complete dependency audit is claimed.
The inherited executable passed its ten synthetic CLI checks. Runner source was
preserved unchanged and its binary is only a reproduction witness.

## Reproduction and cause boundary

Set private paths locally; never publish their values. Both output folders must
be new and separate from input:

```sh
"$COMBINE_DOTNET" "$COMBINE_RUNNER_DLL" inventory "$COMBINE_PAK_ROOT" "$COMBINE_NEW_REPORT_1" GAME_UE4_20
"$COMBINE_DOTNET" "$COMBINE_RUNNER_DLL" inventory "$COMBINE_PAK_ROOT" "$COMBINE_NEW_REPORT_2" GAME_UE4_19
python3 tools/fortnite-export/check_runner.py "$COMBINE_DOTNET" "$COMBINE_RUNNER_DLL"
python3 tools/fortnite-export/check_headers.py "$COMBINE_PAK_ROOT" "$COMBINE_NEW_HEADER_REPORT"
```

Both inventories: exit 1, InvalidDataException, 0 mounted, 10 unmounted,
10 parser-reported encrypted, 0 files/worlds; completeIsland/collisionQualified
false. Changing UE4 version does not change the footer/skip outcome. No full
version sweep is warranted because mounting never reaches package decoding.
New output folders retain inventory/failure/parser reports privately.

Three explanations tested: footer-version handling, altered bytes, protected
input. Fresh hashes exclude changes relative to recorded references. Independent
45-byte v4 footer parsing finds standard magic, version 4, flag 1, valid index
ranges ending precisely at the footer in 10/10. An initial diagnostic incorrectly
excluded 61 bytes (including the GUID added in v7), yielding false out-of-bounds
results; the corrected check and synthetic 45-byte boundary test replace that
intermediate result. No game bytes were altered.

Pinned source trace:
- `UE4/Pak/Objects/FPakInfo.cs`: v4 adds index encryption; GUID is v7; standard
  parser reads flag preceding magic and clears it only for versions below 4.
- `UE4/Pak/PakFileReader.cs`: IsEncrypted is Info.EncryptedIndex; v4 is within
  supported versions for both tested UE4 settings.
- `FileProvider/Vfs/AbstractVfsFileProvider.cs`, TryMountReader: encrypted reader
  without CustomEncryption returns before MountTo/index decoding.

All stored-index SHA-1 checks differed from the footer hashes. This is not a
decryption test or standalone corruption proof; no assertion about cryptographic
payload encryption follows. Independently established fact is the header flag
and parser policy, not the payload's encryption algorithm/state. Clearing the
flag, fetching/extracting keys or bypassing protection is excluded.

```text
Recorded 3.1 identity + fresh container hashes
  -> valid v4 footer, encrypted-index flag
  -> pinned parser skips mount -> no world -> no export/collision evidence
  -> stop this input route -> assess accessible replacement
       -> none qualified -> next: isolated existing Skate host asset load
```

## Replacement assessment

Owner already permits a suitable accessible build (D-023). Bounded local checks
found only Launcher/redist folders in the default Windows Epic installation root;
the mounted secondary drive root had no entries. This is not an exhaustive
machine search. Existing private input is 3.1; no replacement identity selected.

[Epic's installation guide](https://www.epicgames.com/help/c-34254770/c-37371353/a20224238?lang=en-US)
provides an accessible current PC install lead. It does not supply an inspected
island export or establish parser compatibility. [UEFN import documentation](https://dev.epicgames.com/documentation/fortnite/import-content-and-islands-in-unreal-editor-for-fortnite)
describes bringing content into UEFN, not an evidenced full Battle Royale island
export for this runtime. Neither qualifies a replacement for substitution.
No large download/install, account action or third-party game archive acquisition
was performed. No arbitrary older build or generic Unreal landscape was silently
substituted. A replacement remains gated on identity, ordinary mountability,
world/dependency/terrain/building/collision evidence and applicable access rights.

## Change, checks and handoff

Added only a read-only version-4 header diagnostic and synthetic tests. It reads
45-byte footers, validates flag/version/index bounds, reports anonymous container
ordinals to a new ignored private file and prints aggregate metadata. It rejects
symlinks, non-private roots, malformed/truncated/unsupported footers and overwrites;
never decodes payloads or claims completeness/collision. Existing exporter remains
untracked and unchanged. No Rust/runtime/gameplay changes.

Focused header tests: 7 passed, including the exact v4 boundary, invalid ranges,
flags/versions/truncation, preserved inputs/results and symlink refusal. Inherited
runner CLI checks: 10 passed, synthetic only. Full repository gate and final
board/source checkpoint are recorded in docs/HANDOFF.md. Required runner rebuild
remains blocked by missing cache; it is not hidden by the Python gate.

Next actor: **Codex**, C-025. Initialize the pinned existing Skate host against
the located prepared private assets in isolation, reporting loaded/rejected
assets before renderer work. That fallback proves only standalone readiness;
the Fortnite input/export requirements stay open. Source is local only; no owner
trial, acceptance, push, merge or release.
