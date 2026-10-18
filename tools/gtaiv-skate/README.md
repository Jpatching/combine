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

## Authored triangle-ground candidate (#53)

The focused [source slice](https://github.com/Jpatching/combine/issues/53) adds
an explicit triangle route. Both
backends supply these triangles to the existing Session; neither replaces Skate
physics. `combine_skate.js` uses the triangle route when isolated preparation
supplies qualified private `SURFACES` data; an empty array uses the sampled
coverage window (#76) on the same triangle route.
Each entry declares its selected layer, evidence reference, checkpoint centre,
bounded radius and decoded triangles. Unique mesh/host agreement selects the
floor. Preparation, current queries and presented poses retain that selection;
leaving qualified coverage restores GTA control. Data is supplied only after
independent floor qualification, never inferred from a finite query alone.
The owner selected a bounded H2 proof before wider checkpoint qualification under
[the local trial](https://github.com/Jpatching/combine/issues/54).

The public C ABI and matching `COMBINE_SKATE_*` commands provide this sequence:

1. Stop the previous ride, then `SURFACE_BEGIN(layer, triangleCount)` with a
   nonzero selected layer and 1–4096 triangles.
2. Send exactly three GTA-space vertices per triangle using `SURFACE_VERTEX`.
   Invalid or incomplete preparation is refused.
3. `MOUNT_SURFACE(x, y, ground, heading, scale, layer, available)` requires a
   successful, loaded, intended-layer observation at the mount coordinates.
   Only `available=1` is accepted. This is a caller contract, not evidence that
   a query succeeded; finite height alone must never supply this flag.
4. Poll asynchronous preparation before taking control. On each update use
   `TICK_SURFACE(timer, queryX, queryY, ground, layer, available)` with the
   position at which ground was observed. The C ABI additionally takes the
   existing controller packet. Stop and restore ownership on refusal.
5. To move collision coverage during a geometry ride, upload a complete new
   triangle set with `SURFACE_BEGIN` and `SURFACE_VERTEX`, then call
   `SURFACE_REPLACE(queryX, queryY, ground, layer, available)` at the current
   displayed pose. The old and new meshes must both support that pose and agree
   with the same qualified ground observation. The layer, mount origin and scale
   stay fixed. The in-process backend returns 1 after installation. The worker
   returns 2 while installation is pending; poll until 1 before ticking again.
   Worker return 3 means an earlier tick is still pending: poll and retry the
   replacement with a fresh observation. Return 0 requires stopping the ride.

Every floor reaches a Session through one entry point, `Surface::install` in
`src/connection.rs`: install these triangles for this rider pose, or refuse with a
reason. Mount and replacement in both backends call it; each installed floor gets
the next revision (mount 1). Its thresholds are defined there once: **floor
agreement** (host ground at the query within 0.3 m of the mesh, ADR 0004), 0.001 m
query/pose agreement and same-floor support, 3 m pose height, 4096 triangles, area
and coordinate bounds. Floor agreement applies only while Skate reports ground
contact (any physical state but the air states, exposed as `VALUE(4)`: 1 grounded,
0 airborne); leaving the ground is not refused by it. Pose containment uses mesh
support at the returned pose position. Ambiguous overlapping support, missing
coverage and unavailable observations are refused. The Skate frame stays at the
mount origin for the whole ride, because Session cannot move the skater without
resetting its bodies; one upload reaches at most 1000 m from the rider and the frame
at most 8192 m from the origin, where f32 still resolves a millimetre.
Layer numbers are supplied by a qualified caller, not discovered GTA layers.
The geometry constructor bounds input; it cannot prove decoded GTA placement,
loading or contact. Ground agreement does not prove curb/wall response.

Worker frames now carry version 4. Geometry appears in bounded preparation and
replacement payloads; ordinary ticks carry a position-bearing observation and
responses report Skate ground contact.
Mixed old/new worker and parent binaries are rejected. Build/stage matching
candidates together, only after normal shutdown and with retained rollback.

The existing standalone Windows harness accepts `--surface-only` to run actual
Session ramp movement, unavailable-observation refusal, cancellation of a large
preparation against its suspended worker and remount recovery
without GTA. It requires a matching worker/library and the existing private asset
pointer. The authored ground function is a test oracle, never GTA query evidence.
Use `--surface-cancel-only` for the focused cancellation/recovery regression.
Relink the harness after rebuilding the worker-feature library; matching source
files alone do not establish that an existing executable contains the change.
Source/object compilation alone does not establish a passing native trial.

The in-process backend retains an idle Session after normal stop. A remount
reconfigures, installs the newly uploaded collision and activates at the new
origin with cleared input and clock. Dismounted poses remain unavailable.
Configuration/root changes, invalid configuration, any rejected operation and
`combine_reset` discard the retained Session. This avoids rebuilding the skater
on normal remount; the first mount still loads assets. Asset roots are immutable
for a process lifetime: restart after editing files within the same root, because
upstream also caches immutable animation data. This source change does not alter
the separate worker backend or establish live F6 timing in GTA.

Run `native-surface.exe --in-process --mount-reuse-only` against the exact rebuilt
default-feature library to measure cold initialization, normal remount and reset.
It requires a warm remount below 500 ms and below one third of the cold time,
checks the new origin and actual motion over a different authored slope, refuses
idle ticks and verifies that reset reloads the Session. Reset advances a shared
generation, so another callback thread invalidates pose/readiness immediately
and the owning thread retires its old Session at the next native boundary.
Use `--cross-thread-reset-only` for the focused public ABI reset check. These
standalone checks do not qualify GTA callback threading or gameplay behavior.

`tests/native-surface.cpp` isolates the authored ramp proof for either native
backend, without worker suspension/cancellation. Link it against the exact built
static library, keep the private asset pointer beside the executable, and run
`native-surface.exe --in-process` for the optimized default-feature build or
`native-surface.exe --worker` beside the matching worker-feature build. It requires
initial preparation return 1 or 2 respectively, so selecting the wrong backend
fails. Every remount reconfigures after stop. It checks missing/incomplete geometry
refusal without pose exposure or partial-preparation reuse, actual Session push
over changing ramp heights, height following, unavailable/wrong-layer refusal,
ground disagreement beyond floor agreement (0.3 m), query-position mismatch, stale-time refusal,
pose clearing and remount recovery. The moving-coverage case changes the ramp
slope mid-ride and requires Session to follow the new heights. These are authored
checks, not GTA
qualification; their native execution verdict belongs to the exact tested
source and binaries.

```sh
python3 tools/gtaiv-skate/build.py /path/to/source-repository \
  /private/new-build-directory --release
i686-w64-mingw32-g++ -std=c++17 -static -static-libgcc -static-libstdc++ \
  -Wall -Wextra -Werror \
  tools/gtaiv-skate/tests/native-surface.cpp \
  /private/new-build-directory/adapter/target/i686-pc-windows-gnu/release/libcombine_gtaiv_skate.a \
  -o /private/new-build-directory/native-surface.exe \
  -lversion -lxinput -lws2_32 -lbcrypt -luserenv -lntdll
```

The optimized default-feature library passed the complete authored trial with
both the default 2 MiB standalone stack reserve and a diagnostic 16 MiB reserve.
The debug library overflowed the default stack (`0xC00000FD`); with 16 MiB it
reached the ramp but refused a tick after a measured 406 ms tick-start gap exceeded
the adapter's 250 ms continuity limit. Optimization addressed these standalone
test conditions; this does not establish the available stack, latency or safety
of an existing GTA thread, or GTA riding acceptance.

Link against the worker-feature library for `--worker`, and relink after
every library rebuild. The worker's 50 ms bound is asserted for measured mount/poll/tick calls;
in-process mount/poll/tick calls are timed without claiming that asynchronous
bound. Configuration, geometry upload and stop are outside that timing metric.

## Source checks and build

Run from the repository root:

```sh
python3 scripts/verify.py
python3 tools/gtaiv-skate/check.py
# Windows PowerShell:
# powershell -NoProfile -File tools/gtaiv-skate/tests/status.ps1
```

The adapter command is the same authored check suite used by CI: JavaScript mount,
status and live observer checks; Rust connection, wire and freshness checks; and
C++ evaluation-input checks. It requires Node.js, Rust with edition 2024 support
and a C++17 `g++` on PATH. Missing tools or any failed check return a nonzero exit
status with a named failure. Compiled tests use a temporary directory that is
removed afterward. It needs no assets, credentials, downloads or game launch.
The repository gate stays separate so environments without Rust can still run it.
Pinned native definition checks and Windows status-report checks remain separate;
authored checks do not establish real Session or GTA gameplay acceptance.

With Rust's `i686-pc-windows-gnu` target and a 32-bit MinGW compiler on PATH:

```sh
python3 tools/gtaiv-skate/build.py /path/to/source-repository /private/new-build-directory
python3 tools/gtaiv-skate/prepare_definitions.py /private/pinned-gta_iv.json /private/new-gta_iv.json
```

The build exports the exact upstream Git object, never its working tree. It
requires a new destination, uses the committed dependency lock offline, and
produces `combine_skate.cleo`. The preparer requires the pinned JSON SHA256
`ba78c1ae32ea2eb800311f4513617e75c6283ac94805db016d157745356eb21b` and refuses
an existing output. It adds thirteen commands and marks
`GET_GROUND_Z_FOR_3D_COORD` as conditional in the generated definitions. The
pinned input remains unchanged. It also passes `DESTROY_CAM`'s camera handle by
value: the pinned pointer annotation left the owned camera alive after dismount
on GTA IV 1.2.0.59 / CLEO Redux 1.5.1. A private inactive-camera trial verified
immediate destruction with the generated correction. CI checks these generated
argument/return contracts against the hash-verified public definition pin;
that check does not establish gameplay or replace a live native smoke trial.
No numeric native IDs, hooks or game offsets are
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
installs, profiles and baseline copies. Close normally before staging. The separately
authorized JavaScript-only qualification below is the sole trial exception; native
plugins, worker binaries and definitions still require closed-game staging.
Keep the loader/diagnostic pins and
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
foreground GTA and neutral selected input. Controller mode requires a connected
physical controller; keyboard/mouse mode does not. Selected input activity,
lost focus, stop, dismount, reset and rescue cancel it. Expiry returns to physical
input. The simulation, collision checks, transport and pose application are the
same paths as normal riding. No virtual controller driver is required.

`COMBINE_SKATE_EVAL_OWNER` exposes the current player/ped/camera handles to a private
observer. Stage `tests/live-evaluation.js` separately as an evaluation script using
the closed-game preparation rules above. The opt-in `COMBINE_SKATE_EVAL_KEY`
reads only F8/F9 and the checkpoint's F7 through Windows while GTA is foreground; other action values
return false. This avoids relying on GTA's debug keyboard native for the trial.
F8 runs bounded input playback and reads
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

## JavaScript-only reload qualification (pending)

CLEO documents that editing an active JavaScript file restarts that script through
its file watcher ([lifecycle](https://re.cleo.li/docs/en/script-lifecycle.html)).
This does not establish adapter cleanup or native hot swapping. The authorized
qualification changes only a temporary startup log marker in the installed
riding script while dismounted; preserve its prepared floor data and retain the
watchdog, plugin, worker, definitions and other scripts.

Before the trial, verify released input, the same responding windowed foreground
GTA process, installed identities, fresh dismounted readiness and restored GTA
controls/camera. Back up the installed script outside the watched directory.
Atomically replace it, then require a new marker from CLEO and unchanged process
identity. Exercise mount, existing movement and dismount; verify normal controls
and camera. Restore the original bytes atomically through the same reload path,
verify the original hash and fresh readiness, and retain the local evidence
separately from earlier candidate trials. A file/hash change alone is not proof
that the script ran. Stop at the first failed boundary and diagnose it.

On 2026-10-13, released-key and installed-inventory checks passed, but the guarded
launch returned `window-not-ready` and the monitor timed out waiting for a process.
No script was replaced or gameplay input sent. Reload, remount and restoration
are therefore untested; no repeatable reload procedure or convenience command is
qualified. Resolve startup before this experiment. Floor coverage remains a
separate acceptance requirement.

## Behavior and runtime acceptance

The current source defaults to keyboard/mouse riding: **W** pushes, **A/D** steer,
the mouse orbits the chase camera and **F6** mounts/dismounts. Opposing steering
keys produce neutral steering. **F5**, while dismounted and not preparing, selects
keyboard/mouse or the preserved controller mode. Controller mode retains A/X
push and left-stick steering. Input selection is refused during a ride or pending
preparation; focus loss cancels riding without accepting background keys.

Mouse orbit uses GTA's `GET_MOUSE_INPUT`, with 0.15 degrees per pixel and pitch
bounded from −20° to 60°. Invalid mouse observations restore ordinary GTA control
and camera. Native status schema 2 reports `input_mode` and `input_ready` separately
from controller connection; schema 1 remains readable as legacy controller mode.
Authored checks and compilation do not establish live mouse/native behavior.

F6 toggles on-foot mount/dismount when the game is foreground. A connected Xbox
controller at XInput index 0 is required; A/X push and left stick steer through
stock Skate controls. Readiness/mount/failure messages appear in GTA's text area.
The stock ped is a rough visual placeholder for the simulation position and
heading. A chase camera follows it. Full Skate animation is not included.

At mount, the **coverage window** (`coverageWindow` in `combine_skate.js`, ADR 0004)
queries the ground native on a 5×5 grid at 2 m spacing (±4 m), from rider z + 2, and
uploads 32 triangles (two per cell) as layer 1 through `COMBINE_SKATE_MOUNT_SURFACE`.
Mount is refused with a stated **coverage gap** for a non-finite sample, a near-zero
sample (ambiguous or unloaded; the native has no success flag, so genuine zero-height
ground is unsupported) or a neighbouring step above `WALL_THRESHOLD` (0.3 m, equal to
`FLOOR.agreement`).
The window follows the rider in fixed 2 m world cells centred on the sample lattice:
crossing out of the centre cell resamples it and installs it through
`SURFACE_REPLACE` as a new revision, with no remount. Neighbouring windows share
lattice samples, so a swap leaves the floor under the rider unchanged. Reaching a
coverage gap on the way (wall-height step, unloaded or missing ground) dismounts
with "coverage gap (…)"; a window containing a gap is refused whole, so the ride
ends up to a window's half-width (4 m) before the wall. Riding requires **floor
agreement** while Skate reports ground contact: GTA ground at the rider within
`FLOOR.agreement` of the triangles, otherwise it dismounts with "floor agreement
lost". Rolling ground and curbs between samples keep it (`tests/coverage-window.cjs`
reports their interpolation error); curbs ride as ramps, so the ped can sit up to
the step height off GTA ground near them. Coordinates rotate GTA Z-up to Skate Y-up and translate around the
mount position. **One GTA unit = one metre is an assumption requiring runtime
measurement.** GTA heading 0 maps +Y to Skate −Z; headings/pose axes also need
runtime observation. This sampled patch is not a complete GTA collision mesh:
obstacles, walls, traffic, overhangs and holes between samples are not represented.
Select and privately survey one clear real GTA surface before acceptance.

Timing uses GET_GAME_TIMER milliseconds and the actual Session period. More than
250 ms between frames or over 32 pending ticks abandons riding. Invalid player,
vehicle/death transition, missing camera, disconnected controller, invalid pose,
changed ground height or leaving coverage restores GTA. Initialization retains
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
submits it without blocking, and cancellation clears it. A dedicated writer with
a bounded queue keeps large geometry pipe writes off the supervisor, allowing
it to observe cancellation and terminate its owned child while writes are blocked.
Versioned binary
messages carry ride generation, request sequence and collision revision. Output
with mismatching identity, nonfinite pose or invalid period is refused. Riding
ends after a response gap above 250 ms. Temporary snapshot publication contention
uses only the last accepted pose with its original timestamp, matching ride/revision
and runtime identity, and independently validated ground. Repeated reads never
extend that deadline; poisoned shared state refuses riding. A Windows kill-on-close job contains owned
workers; cancellation/failure terminates only that child. No game-thread shutdown
wait is performed. An idle Session can remain warm; each new ride installs collision
from the newly uploaded floor before activation. Cancellation during an outstanding
request may discard the warm child.

Worker wire and freshness checks are included in `check.py` above.

`tests/native-worker.cpp` is a standalone Windows smoke harness linked against the
worker-feature static library. Run it beside the built worker and private asset
pointer. It checks bounded parent calls during real Session preparation and pose
exchange, warm remount, push/steer response, discarded dismounted poses, suspension
and exit of its own child, and fresh recovery. It never attaches to GTA. Its refusal
outcome plus mocked JS cleanup checks do not prove actual GTA control/camera
restoration; the mounted gameplay/fault trial remains required for #20 acceptance.
