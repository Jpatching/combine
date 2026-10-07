# GTA IV 1.2.0.59 diagnostic candidate

This is a read-only CLEO Redux diagnostic, not a skating adapter. It samples the
real game through a JS script and passes the values into an x86 native plugin.
The plugin correlates samples with CLEO's after-scripts callback. Direct C++ GTA
native invocation is not established by this approach.

The [candidate pins](../../research/gtaiv.lock.json) and
[source qualification](../../research/results/2026-10-07-gtaiv-source-qualification.md)
identify the reviewed documentation, SDK signatures and definitions. Release
checksums there come from GitHub metadata; loader archives have not been downloaded
or independently verified here. No universal-modder tools are installed or run.

## Build the diagnostic

Use a 32-bit Windows C++ compiler. For MinGW from Linux:

```sh
cmake -S tools/gtaiv-diagnostic -B .private/gtaiv-diagnostic-build \
  -DCMAKE_SYSTEM_NAME=Windows -DCMAKE_CXX_COMPILER=i686-w64-mingw32-g++ \
  -DCMAKE_BUILD_TYPE=Release
cmake --build .private/gtaiv-diagnostic-build
node tools/gtaiv-diagnostic/check_script.cjs
```

The result is `combine_iv_diagnostic.cleo`. The verified MinGW build imports only
Windows system libraries (KERNEL32, msvcrt, VERSION); CLEO SDK exports are resolved
from the already loaded `cleo_redux.asi`. Missing exports or SDK versions below 4
reject loading. A first-loop gate requires SDK host IV and executable file version
1.2.0.59 before any gameplay queries. This version-resource check does not prove
authenticity or reject a modified executable with the same version resource.

Fetch the exact `gta_iv/gta_iv.json` source named in the pins into a private
preparation folder, then produce a separate file:

```sh
python3 tools/gtaiv-diagnostic/prepare_definitions.py \
  .private/gtaiv-source/gta_iv.json .private/gtaiv-source/gta_iv.diagnostic.json
```

The preparer requires the pinned hash and refuses to overwrite its destination.
It adds two named command definitions with the SDK's exact argument order. This
has been checked structurally, but acceptance of those custom definitions by
GTA IV's CLEO runtime remains untested. No numeric native IDs are invented.

## Build the existing Skate host for x86

Export only source from mashup commit
`f608f85e407ff1b7689d54a9aafdd16e95711ac4` into a private build directory, preserving
the relative layout `upstream/skate/`. Copy `skate-harness/` alongside `upstream/`
as `harness/`, including its dependency lock. Do not build inside retained upstream
or game installs. With Rust 1.95.0 and an i686 MinGW C compiler available:

```sh
rustup target add i686-pc-windows-gnu
cargo build --offline --locked --manifest-path .private/gtaiv-build/harness/Cargo.toml \
  --target i686-pc-windows-gnu --target-dir .private/gtaiv-build/target
```

Offline mode needs the dependencies already cached. The harness links the original
`Session::new`, `tick`, `pose` and `period` calls, without local Skate patches.
Compilation and linking have passed. The executable imports XINPUT1_3.dll in
addition to Windows system APIs; runtime library availability remains untested.
Its debug executable's disk size is not a measurement of process memory.

On Windows, supply the existing private converted Skate asset directory as its
first argument and redirect stdout/stderr to a private log. It creates a synthetic
Y-up floor, advances 120 neutral-input ticks and checks finite root transforms and
an advancing tick count. This is a separate diagnostic: even a pass would not prove
GTA collision, controller integration, embedding, memory fit, animation or gameplay.
No harness execution or asset initialization has been verified in this session.
The full upstream host test suite still has the missing `src/tests/map_startup.rs`
debt; the build does not resolve it.

## Runtime sequence and acceptance

1. Qualify the supplied archive's executable and launcher/support files. Preserve
   its bytes and the game version. A replacement authentication library must not
   become a protection-bypass route. Do not silently substitute versions or DLLs.
2. Establish an isolated stock launch through the identified normal startup route,
   in solo play. Keep original installs intact and use separate user/profile state.
   Ordinary GTA saves can live outside the executable folder, so copying a game
   alone does not isolate saves. Record usable controls, normal exit and relaunch.
3. Review and byte-verify the exact x86 loader packages before staging them only
   into that qualified isolated copy. Do not run bundled example scripts or plugins.
   CLEO documents `dinput8.dll` as GTA IV's loader name. This source inspection is
   not a complete audit of either loader binary or its closed runtime internals.
4. In that isolated copy, place the plugin under `CLEO/CLEO_PLUGINS`, the JS script
   under `CLEO`, and the generated definitions as `CLEO/.config/gta_iv.json`.
   Preserve private baseline definitions. Inspect the active definition file after
   startup: CLEO can fetch missing/invalid definitions. Abort qualification on an
   unexpected definition change rather than claiming the pinned API was used.
5. Over three fresh launches, check the identity and first-callback log lines,
   then deliberately walk, drive, move the camera and hold each stick direction.
   Compare successive `COMBINE_IV sample` entries with those actions. `timer_ms`
   is documented in milliseconds; frame, callback step, rotation and stick values
   retain raw units/ranges until separately demonstrated. Thread IDs must establish
   that script commands and callbacks use the expected same game thread.
6. Close the game before disabling the diagnostic: move its JS and `.cleo` files
   out of their discovery directories into private storage, then relaunch. Verify
   absence of sample logs and normal walking, driving and camera controls. For
   comparison with completely stock behavior, use the preserved stock copy.
   Do not hot-unload a plugin with registered callbacks.
7. Keep logs, assets, profiles, executable hashes and archive inventory private.
   Record only source-safe passed/failed/blocked/not-tested classifications publicly.

Collision geometry, grind-edge detection and bone-animation access each require
their own real-game result. Height probes and bone-position query definitions do
not qualify a collision mesh or writable animation. Plugin loading alone cannot
resolve skating feasibility. Once the route has supporting runtime evidence, use
`/to-spec` for mount, move on one GTA surface, trick, grind one edge and dismount.
Same-process embedding stays preferred; this x86 build provides no reason to select
a separate helper. Solo gameplay first; Melty publication remains deferred.
