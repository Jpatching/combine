# Skating trial prepared and launched — 2026-10-03

Status: **preparation passed; process launched; human skating/replay test pending.**
Player outcome: skate on Rust with the owner's DualSense, then return to the setup.
Tracking reference: C-003b. This is agent-assisted preparation, not an unaided-player
setup-time measurement or a passed gameplay recipe.

## What, where and why

- **What:** inspect the supplied archive, extract its Xbox filesystem, run the pinned
  converter and configure a separate skating trial. No new skating implementation.
- **Where:** private source/evidence in ignored `.private/c003b/`; Windows trial at
  `%LOCALAPPDATA%\CombinePilot\v0.4.0\mw2-skate`, with the runtime in nested
  `2010-Rust-Rewrite-Mashup`. Original `mw2-only` trial retained.
- **Why:** reuse implemented upstream integration, keep original installations intact,
  and separate preparation failures from controller/gameplay failures.

```text
Local 7z -> ISO -> extracted Xbox files -> bundled converter -> isolated trial
             |             |                    |                  |
          hash/size    XEX2 + files        output checks       launch + play
                                                               | not observed
                                                               +-> pending
```

Each arrow has evidence below. Successful files/process checks do not prove skating.

## Exact inputs and extraction

- Runtime: v0.4.0 / `f608f85e407ff1b7689d54a9aafdd16e95711ac4`; existing
  70,231,384-byte release archive reverified against its pinned SHA-256 before use.
- First supplied ZIP was PS3 (BLES00760 / PS3_GAME), no `default.xex`; inspected
  without extraction/execution and rejected as incompatible with this converter.
- Subsequent local `Skate_3.7z`: 4,011,025,808 bytes; SHA-256
  `a4084782cda47bba6f2eda68c26e8f41fe46c80bffb21732e013642fcbf4309d`, matching
  previously read hosting metadata. This establishes byte identity, not publisher
  authenticity, ownership or distribution permission; provenance remains unresolved.
- Archive has one regular, unencrypted ISO entry. Local libarchive unpacked it;
  ISO size 6,397,689,856 bytes; SHA-256
  `059f6412dc8e122f0646fc308be76cb8d7a68b973ccf9b8abda1ee6e0de61f0b`.
  Archive hashing plus unpacking took 407.15 seconds.
- [XboxDev extract-xiso](https://github.com/XboxDev/extract-xiso/tree/3f5b62cfe68f000b0e3c8a30104973f3a297948e)
  built locally from commit `3f5b62cfe68f000b0e3c8a30104973f3a297948e` using
  CMake 3.28.3 and GCC 13.3.0 (Ubuntu 13.3.0-6ubuntu2~24.04.1).
  Commands: `cmake -S .private/c003b/extract-xiso-src -B .private/c003b/extract-xiso-build`;
  `cmake --build .private/c003b/extract-xiso-build -j2`.
  Inherited compile warning: integer-to-pointer size cast in `write_tree:1730`, a
  creation path. Reviewed extraction copies file bytes; no image rewrite/patch mode used.
- Extractor `-l` confirmed all five converter input paths. `-x -s` extracted into
  `.private/c003b/skate3-extracted`, skipping the console system-update directory.
  All 101 extracted files matched listed sizes (6,396,955,444 bytes); `default.xex`
  has the XEX2 header. Extraction plus inventory hashing took 25.36 seconds;
  no extraction warnings. No console executable or updater was run.

## Preparation and preservation evidence

- Wrapper: ignored `.private/c003b/prepare-skating.ps1`; this is local orchestration,
  not a committed product API. It fails on an existing trial, missing inputs or wrong
  runtime hash; invokes only the bundled converter; validates four required outputs;
  writes the same two path settings used by the upstream wizard.
- Direct script invocation from the WSL share was blocked as unsigned. Effective
  policy was RemoteSigned. With environment approval, the locally generated script
  was copied to Windows local temp, checked byte-identical and run under the unchanged
  policy. No execution-policy change or security-software disablement occurred.
- Converter returned 0 in 41.53 seconds. Four required outputs present: skater model,
  game configuration, physics skeletons and skater collections. Empty stderr file.
- Preparation ran 18:32:39.9941974Z–18:34:15.0954617Z. The existing Minecraft 26.3
  cache was copied into the new trial after checking its completion marker/client
  hash; the original trial was not edited or linked as shared mutable storage.
- MW2 before this trial: all 178 files / 12,101,823,987 bytes matched the original
  pre-first-launch manifest: zero added, removed or changed (167.82 seconds).
- Extracted Skate inputs after conversion: all 101 files unchanged by hash, size
  and membership (15.66 seconds). Raw manifests remain private.
- Windows detected DualSense Wireless Controller over Bluetooth; owner confirms
  owning a DS5. Detection is not a successful input test. No controller driver installed.
- Started the new `iw4l.exe` from its own directory at
  2026-10-03T18:35:24.3887509Z, PID 56004. Runtime logs remain private.
- After launch, generated `skate-data/assets/board.json` (4,225,250 bytes) and
  `rig.json` (16,413 bytes) were present. These are preparation evidence, not play.

## Remaining test and next decision

Owner: Create Game → Rust → press J → use DualSense to move/turn and attempt a trick.
Record actual board visibility, collision, controller response and errors. Then test
10 on/off transitions, recovery, ten minutes of play and exit/relaunch. Compare MW2
files again after the completed session. A game window or generated model alone is
not a pass. The earlier possible Minecraft freeze is still undiagnosed.

Skating outcome, replay, post-session source preservation and owner acceptance remain
pending. No source build of the game, public multiplayer, update, purchase, publication,
asset upload or redistribution occurred. Redaction reviewed: yes.
