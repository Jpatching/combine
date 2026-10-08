# GTA IV → Skate mount adapter (issue #20)

Source candidate for GTA IV Complete Edition **1.2.0.59**, x86, CLEO Redux
1.5.1 SDK commit `bbf6773fe8cc1bfa95c73509a25928f97b0d8d13` and GTA native
definitions `sannybuilder/library` commit
`34bedee0be2f57047ed8f0705c81f137ede3d3ce` (`gta_iv/gta_iv.json`, API 0.108).
The in-process Rust library uses the untouched Skate `Session` from mashup
commit `f608f85e407ff1b7689d54a9aafdd16e95711ac4`. Assets are not included.

This is a runtime candidate, not observed skating acceptance. #20 remains open;
#21 and #22 must wait for its observed behavior and owner acceptance. Qualification
context is [#10](https://github.com/Jpatching/combine/issues/10).

## Source checks and build

Run from the repository root:

```sh
python3 scripts/verify.py
rustc --test tools/gtaiv-skate/tests/connection.rs -o /tmp/combine-connection-tests
/tmp/combine-connection-tests
node tools/gtaiv-skate/tests/script.cjs
```

With Rust's `i686-pc-windows-gnu` target and a 32-bit MinGW compiler on PATH:

```sh
python3 tools/gtaiv-skate/build.py /path/to/source-repository /private/new-build-directory
python3 tools/gtaiv-skate/prepare_definitions.py /private/pinned-gta_iv.json /private/new-gta_iv.json
```

The build exports the exact upstream Git object, never its working tree. It
requires a new destination, uses the committed dependency lock offline, and
produces `combine_skate.cleo`. The preparer requires the pinned JSON SHA256
`ba78c1ae32ea2eb800311f4513617e75c6283ac94805db016d157745356eb21b` and refuses
an existing output. It adds ten commands. Native signatures stay in the pinned
base; no numeric native IDs, hooks or game offsets are invented.

The portable checks exercise axis/scale, selected-surface bounds, timer
interruptions, cardinal headings and external GTA native control/camera
restoration. Mock native results establish adapter behavior only. The linked
library exercises real upstream Session APIs at build time. The **full upstream
host-test suite remains unverified**: pinned host references missing
`src/tests/map_startup.rs`. Two upstream private-interface warnings remain.

## Private preparation (requires runtime task authority)

Use the accepted stock baseline and its ordinary startup route. Preserve original
installs, profiles and baseline copies. Close normally before staging; never
hot-load or replace files in a running game. Keep the loader/diagnostic pins and
checksums from qualification #10. Stage into the owner-selected runtime with private backups:

- `combine_skate.cleo` → `CLEO/CLEO_PLUGINS/`.
- `combine_skate.js` and `combine_skate_watchdog.js` → `CLEO/`.
- Prepared JSON → the owner-selected runtime's `CLEO/.config/gta_iv.json`, preserving the
  previous private file. This preparation uses the pinned base; it does not
  preserve unrelated custom definitions automatically.
- Beside `combine_skate.cleo`, create private `combine_skate.assets.txt` containing
  exactly one absolute directory of already-converted Skate assets, UTF-8 (BOM
  accepted). This is data, never a command. Do not commit/upload it or private logs.

No installer, launch, asset conversion or redistribution runs in the build.
The DLL imports XINPUT1_3 and Windows system libraries; confirm availability.

## Behavior and runtime acceptance

F6 toggles on-foot mount/dismount when the game is foreground. A connected Xbox
controller at XInput index 0 is required; A/X push and left stick steer through
stock Skate controls. Readiness/mount/failure messages appear in GTA's text area.
The stock ped is a rough visual placeholder for the simulation position and
heading. A chase camera follows it. Full Skate animation is not included.

At mount, the native ground query samples a 5×5 grid, 8 metres wide. Ambiguous zero-height ground
results are rejected because the native has no success flag; genuine zero-height
surfaces are unsupported by this narrow candidate. The selected patch must be
clear and flat within 5 cm; riding is confined to its central
7 metres. Coordinates rotate GTA Z-up to Skate Y-up and translate around the
mount position. **One GTA unit = one metre is an assumption requiring runtime
measurement.** GTA heading 0 maps +Y to Skate −Z; headings/pose axes also need
runtime observation. This sampled patch is not a complete GTA collision mesh:
obstacles, walls, traffic, overhangs and unsampled holes are not represented.
Select and privately survey one clear real GTA surface before acceptance.

Timing uses GET_GAME_TIMER milliseconds and the actual Session period. More than
250 ms between frames or over 32 pending ticks abandons riding. Invalid player,
vehicle/death transition, missing camera, disconnected controller, invalid pose,
changed ground height or leaving the patch restores GTA. Initialization retains
GTA ownership until Session and camera are ready. Restoration unfreezes the ped,
returns player control and removes the owned camera. Each restoration operation
is attempted independently if a GTA native throws.

A separate watchdog script restores saved ownership after two seconds without a
frame or on CLEO runtime reset. Both scripts must be installed. Callback/script
threads are distinct in live qualification; shared state uses atomics, Windows
InitOnce and an ownership lock. Session calls stay on one script thread; reset
allows a new script thread to capture the next surface. Dynamic DLL unload or
simultaneous removal of both scripts cannot perform native restoration; close
normally, and do not hot-unload this adapter.

For #20, privately record: real surface selection/survey; native loading and
changing controller input; timer/pose/camera output; mount → push/steer →
dismount repeated; controller unplug; leaving surface; failed initialization;
script failure/watchdog; and normal GTA control/camera after each. Source/build
results, observed runtime behavior and owner acceptance are separate evidence.
Do not repeat waived stock qualification trials from #10. No game launch or
release is authorized merely by this source artifact.
