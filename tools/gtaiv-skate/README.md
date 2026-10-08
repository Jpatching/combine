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
node tools/gtaiv-skate/tests/status-script.cjs
# Windows PowerShell:
# powershell -NoProfile -File tools/gtaiv-skate/tests/status.ps1
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
an existing output. It adds twelve commands and marks
`GET_GROUND_Z_FOR_3D_COORD` as conditional in the generated definitions. The
pinned input remains unchanged; no numeric native IDs, hooks or game offsets are
invented.

The ground correction was checked on the stated GTA/CLEO versions: the original
definition returned success bits `1` interpreted as a float (approximately
`1.4e-45`), which the near-zero guard rejected. An explicit output-buffer probe
returned a height agreeing with `GET_CHAR_HEIGHT_ABOVE_GROUND`; the conditional
definition then produced the same agreement through the ordinary `native` call
on two repeated live checks. Higher query origins and a collision request with a
wait did not fix the original definition. This establishes ground-query output
handling, not a complete surface survey or skating acceptance. The proprietary
CLEO return-handling path is not exercised by the portable mocked tests.

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
- `combine_game_status.js` → `CLEO/` (read-only state publisher).
- Prepared JSON → the owner-selected runtime's `CLEO/.config/gta_iv.json`, preserving the
  previous private file. This preparation uses the pinned base; it does not
  preserve unrelated custom definitions automatically.
- Beside `combine_skate.cleo`, create private `combine_skate.assets.txt` containing
  exactly one absolute directory of already-converted Skate assets, UTF-8 (BOM
  accepted). This is data, never a command. Do not commit/upload it or private logs.

No installer, launch, asset conversion or redistribution runs in the build.
The DLL imports XINPUT1_3 and Windows system libraries; confirm availability.

For private automated worker trials only, add `--evaluation` to `build.py --worker`
and `prepare_definitions.py`. Normal builds do not register evaluation commands.
This enables `COMBINE_SKATE_EVAL_INPUT(profile,duration)` for four fixed profiles:
neutral, X push, X push with left steering, and X push with right steering.
Each request expires after 50–1000 milliseconds. Playback requires a mounted ride,
foreground GTA and a connected, neutral physical controller; controller activity,
lost focus, stop, dismount, reset and rescue cancel it. Expiry returns to physical
input. The simulation, collision checks, transport and pose application are the
same paths as normal riding. No virtual controller driver is required.

`COMBINE_SKATE_EVAL_OWNER` exposes the current player/ped/camera handles to a private
observer. Stage `tests/live-evaluation.js` separately as an evaluation script using
the closed-game preparation rules above. F8 runs bounded input playback and reads
actual GTA movement, heading and active camera position. F9 observes ordinary
walking displacement for two seconds while the harness supplies walking input.
The script also checks native control and destruction of the owned camera after
a ride ends. Its log contains fixed verdicts only. It never teleports the player,
writes camera/player state, mounts or substitutes a pose. The input command is its
only riding write; expiry also protects against a stopped observer script.
Remove the observer and restore the normal plugin/definitions after evaluation.
These checks establish measured bridge behavior, not camera usability, physical
controller qualification, metre calibration or owner acceptance.
The observer uses wrapping game time plus an independent `GetTickCount` deadline;
a paused/interrupted scene refuses observation. An external harness must also
bound its wait because a paused script scheduler cannot run observer code.

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
InitOnce and an ownership lock. The default candidate keeps Session calls on one script thread; reset
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

## Compact live context

`combine_game_status.js` queries pause, cutscene, player-control and on-foot state.
The plugin adds readiness, owned mount state and XInput slot 0 availability. It
atomically replaces a small fixed-schema snapshot under the current Windows
user's `%LOCALAPPDATA%/Combine/gtaiv-status/state.json`, at most twice a second
while unchanged. It does not record coordinates, assets, settings or raw logs.

From the repository root in Windows PowerShell:

```powershell
powershell -NoProfile -File tools/gtaiv-skate/game-status.ps1
powershell -NoProfile -File tools/gtaiv-skate/game-status.ps1 -Watch -TimeoutSeconds 30
powershell -NoProfile -File tools/gtaiv-skate/game-status.ps1 -WaitPlayable -TimeoutSeconds 30
```

The first prints the five-line report. Watch prints only state changes. Wait
returns exit 0 for fresh on-foot gameplay with a controller and ready adapter;
exit 2 means the deadline elapsed. `-Json` returns the same fixed labels and
`CanTest` decision. Neither mode sends input. Check exit status before proceeding,
then check again immediately before input; the mount adapter also refuses
cutscenes, pause menus and disabled GTA control independently.

Reports older than two seconds, another process/start time, invalid schema or
failed queries become `unknown` and block input. Before game scripts run, menu
and loading state cannot be distinguished by this native publisher. A fresh
`gameplay` label with disabled player control still blocks unmounted tests.
Mounted Skate intentionally disables GTA controls, which is reported separately.
The report establishes test prerequisites, not surface validity, visible movement,
correct scale, usable camera or gameplay acceptance. Local OCR can supplement
menu/message confirmation; screenshots and raw evidence remain private.

## Optional separate-worker candidate

Build with `build.py --worker` to produce the optional asynchronous plugin and
`combine_skate_worker.exe`; the ordinary build preserves the in-process candidate.
Stage the executable beside the plugin and private asset pointer only after normal
closure and backed-up staging. The worker reads that same private asset-pointer
file. There is no installation or launch in the build.

The GTA script submits preparation, then polls `COMBINE_SKATE_POLL` without taking
control until a fresh finite pose is available. Mount returns 0 for refusal, 1 for
immediate in-process readiness, or 2 for pending worker preparation. Poll returns
0 for refusal, 1 for readiness, or 2 while pending. F6, movement away from the
sampled position, pause/cutscene, input loss or a 60-second preparation deadline
cancels preparation while GTA retains control. Mounted pause/cutscene now restores
GTA immediately in either candidate.

A dedicated supervisor owns process and pipe operations; GTA commands only submit
to a capacity-one queue or read the latest validated snapshot. One bounded deferred
prepare request remains pending while prior cleanup occupies that queue; polling
submits it without blocking, and cancellation clears it. Fixed binary
messages carry ride generation, request sequence and collision revision. Output
with mismatching identity, nonfinite pose or invalid period is refused. Riding
ends after a response gap above 250 ms. Temporary snapshot publication contention
uses only the last accepted pose with its original timestamp, matching ride/revision
and runtime identity, and independently validated ground. Repeated reads never
extend that deadline; poisoned shared state refuses riding. A Windows kill-on-close job contains owned
workers; cancellation/failure terminates only that child. No game-thread shutdown
wait is performed. An idle Session can remain warm; each new ride installs collision
from the newly sampled grid before activation. Cancellation during an outstanding
request may discard the warm child. The unchanged 5 cm surface guard still applies.

Additional source checks:

```sh
rustc --edition=2024 --test tools/gtaiv-skate/tests/wire.rs -o /tmp/combine-worker-wire-tests
/tmp/combine-worker-wire-tests
rustc --edition=2024 --test tools/gtaiv-skate/tests/freshness.rs -o /tmp/combine-worker-freshness-tests
/tmp/combine-worker-freshness-tests
```

`tests/native-worker.cpp` is a standalone Windows smoke harness linked against the
worker-feature static library. Run it beside the built worker and private asset
pointer. It checks bounded parent calls during real Session preparation and pose
exchange, warm remount, push/steer response, discarded dismounted poses, suspension
and exit of its own child, and fresh recovery. It never attaches to GTA. Its refusal
outcome plus mocked JS cleanup checks do not prove actual GTA control/camera
restoration; the mounted gameplay/fault trial remains required for #20 acceptance.
