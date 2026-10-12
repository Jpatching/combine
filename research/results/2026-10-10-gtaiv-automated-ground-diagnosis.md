# Automated GTA ground diagnosis — 2026-10-10

Source workspace: `implement/gtaiv-qualified-ground` at
`3fb683a9a4d7c88ffbba162ad3a8f9e99f26a443` for the paired-height follow-up;
earlier trials used `a9760d0a8ca99269376dfa086c144463410615a4`.
Ground implementation remains
in draft PR #57, stacked on retained draft #23. Runtime reference remains
`b403377481a33e407aeb81b78b8d38984aac4735`; no qualified triangle supplier
was activated and neither PR was merged.

## Verified behavior

User-local Windows FFmpeg installation passed checksum and capture checks.
The private runner recorded the actual F6 `over-0.05-metres` refusal,
retained native GTA control and decoded 171 video frames. This is failed-mount
evidence, not a ride. Private recordings and raw logs remain outside Git/uploads.

Local OCR and guarded Enter pulses automated the offline title and Start menus.
Input requires the captured process/start identity, expected executable,
foreground window and non-minimized state; the child releases its own key.
Timeout retains that child rather than killing it before key-up. No focus
stealing occurred. Independent source review corrected this timeout boundary
and a diagnostic record-count limit.

The owner approved bounded paired script/definition trials, normal restarts
and exact restoration. Ordinary CLEO JS starts at new-game/save loading;
the initial process-only trial had no markers and left the hypothesis untested.
The reader subsequently bound to the current run and handled quoted log output.

A loaded-world buffer probe reached zero initial character displacement and
`waiting-for-world-collision=false`, then caught an exception before observing
the ground return. Its owned buffer was freed. A subsequent attempt to scope
memory permission through the diagnostic filename failed with Windows
`MoveFileInfoItemUnauthorizedAccessError`; staging rollback verified the
retained pair. No global permission setting or ACL was changed.

A narrower probe omitted Memory reads/writes. Three batches queried the same
centre and corner coordinates: all six native calls returned actual JS boolean
`true`. Character displacement was 0/24/25 mm; query coordinates remained fixed.
The probe completed and freed its owned buffer. This verifies the four-input,
zero-output conditional-return contract on the retained GTA version.

Final recovery restored and hash-verified the retained script, definitions
and manifest, then verified fresh foreground unmounted GTA gameplay/control
after normal restart.

## Paired success and height follow-up

A private diagnostic plugin was built from exact retained adapter source
`b403377481a33e407aeb81b78b8d38984aac4735` and pinned upstream
`f608f85e407ff1b7689d54a9aafdd16e95711ac4`. Its worker library was rebuilt,
then the x86 C++ plugin compiled and linked with warnings treated as errors.
The temporary helper exposes only its own four-byte float buffer: finite seed,
value, adjacent guard check and clear. It accepts no arbitrary memory address.
An independent source review found no blocker. This is instrumentation of the
retained worker route, not installation of #53's triangle implementation.

The reviewed script, definitions and plugin were temporarily staged together
after normal shutdown, with exact backups, frozen candidate hashes and verified
rollback. Six synchronous ground calls paired actual JS boolean `true` with a
finite changed buffer value and intact adjacent guards. All six owned-buffer
clears and the completion marker were observed in current-run logs.

Three readings at each of two fixed horizontal coordinates had **0 mm height
spread**. The corner-minus-centre height was **-22 mm** in every batch. At the
centre, character Z minus character height above ground agreed with the ground
query within the reported **0 mm**, with horizontal position checked within
1 mm. Character three-dimensional displacement was 0/24/25 mm, so the character
was not claimed motionless. `IS_CHAR_WAITING_FOR_WORLD_COLLISION` was false in
all three batches. Millimetre values are rounded diagnostic output.

This proves the paired conditional return and owned-buffer height observation
on the retained GTA build. These two live query points were not established as
any of the four frozen checkpoint points. Exact coordinates, six measurement
objects, raw logs, build outputs and prototypes remain in the private debug area.

Normal shutdown restored the exact retained plugin, definitions, mount script
and runtime manifest; all retained hashes matched. The offline-menu runner then
passed fresh foreground unmounted GTA gameplay/control after normal restart.
A separate read-only check confirmed the retained executable was responding,
not minimized, with current-process status age zero and all runtime hashes
matching. Module enumeration did not identify the plugin modules;
that enumeration is not used as plugin-loading evidence.

## Cursor-free checkpoint capture follow-up

At source workspace `b859bb9f8fb3f3c73a6d27789354f2129fcdac43`, a reviewed
private launcher reused the public capture/marker/visibility sources at
`0e39f07bd1e9d1ddd4e77259b6731f2b8ebef9a7` and the retained isolated viewer.
The current signed editor's ProductVersion matched the exact
`6000.4.0f1_8cf496087c8f` pin. Early attempts refused before staging because of
a stale discovery filter, an unrecorded pre-cleanup marker version and an
already-closed project. The binary pin and complete marker source were checked
before correcting those preparation assumptions; unrelated changes were not
overwritten.

The actual fresh Play run passed the viewer bootstrap's selected-overlay coverage,
viewer streaming readiness and fresh four-marker checks, emitted its capture-complete
marker and returned `inspection-pending`. All 16 expected images were written:
four checkpoints, two viewpoints and map-only/restored pairs. They passed PNG
signature/dimension checks and Windows full-pixel decoding at 960 × 720. No C#
compiler errors were observed. Pixel content and precise anchor-base association
have not been interpreted or accepted; file integrity does not establish them.

The launcher's independent review caught restoration ownership checks that were
too early; per-file checks were added immediately before each write/delete.
Exact original source and metadata bytes, and previous file absences, were
restored after normally closing only the capture's bound editor. Project-version,
package-manifest, ECSMain scene and bootstrap preservation hashes passed; the lab
remains closed.
The private images and failed preparation records are retained. All 16 images
were requested in the local evidence viewer; owner viewing and surface/layer
acceptance remain unverified. No shared
pointer or synthetic keyboard input was used for this capture.
A final read-only GTA snapshot matched all retained runtime hashes and found the
retained game responding but minimized, with stale native status. Further GTA
trials require fresh foreground readiness; the earlier post-ground-trial recovery
pass is not a current readiness claim after the viewer work.

## Standalone in-process authored-surface follow-up

At source workspace `96d1c058f3216e3d50d3e1bf38d7731661bd704d`, a focused
standalone harness exercised the in-process adapter's public preparation,
tick and pose ABI against the actual pinned Session. It uses independently
authored literal ramp geometry, not the retained GTA resource. The selected
backend must return synchronous preparation `1` or asynchronous preparation `2`
as appropriate; every remount reconfigures after stop. Production adapter logic
and installed GTA runtime were not changed.

The first default debug executable overflowed its original 2 MiB stack
(`0xC00000FD`) before reaching authored assertions. With source and library
unchanged, a 16 MiB stack allowed mounting but riding refused. Targeted harness
timing then recorded a 382.812 ms tick and 406 ms tick-start gap before refusal,
exceeding the adapter's 250 ms limit on time continuity. This supports debug-performance
as the cause of that refusal; it is not a diagnosed GTA floor failure.

With the same 16 MiB stack and optimized default-feature library, the final
harness passed actual Session ramp mounting, 90 push ticks across distinct
heights, height following, unavailable/wrong-layer refusal, stale pose clearing
and remount recovery. Exit was zero, elapsed time 97.354 seconds and maximum
measured mount/poll/tick call 20,863.339 ms. Configuration, geometry upload and
stop are excluded; synchronous mounting dominates that metric. This does not
establish that these calls are suitable for GTA's live thread. Relinking that
same optimized library with the original 2 MiB stack also passed the complete
authored trial: exit zero, 93.294 seconds and maximum measured call 17,569.624 ms.
The optimized standalone proof therefore does not require the larger stack.

Executed final harness source SHA256:
`5a92c0eeeb7661ec71407f03d5c566f7c04c24e566662a9857e00e8b3293bb85`.
The builder offers a separate `--release` choice for optimized in-process output;
the actual tested library was built with manual Cargo release commands. This
does not change the default profile or install either candidate. A passing
authored Session check does not establish GTA ground, gameplay or source acceptance.
The same final harness also passed `--worker`: explicit native exit zero,
23.448 seconds and maximum measured mount/poll/tick call 1.024 ms, with the
expected initial preparation return `2`. A freshly linked standalone executable
reused the matching retained worker-feature library and worker; adapter Rust
files/manifests and all 2,905 exported upstream files matched current source and
the pinned export. The worker's existing suspension/cancellation proofs remain
separate. An initial runner failed to obtain the native exit code despite all
pass markers; a corrected runner repeated the trial and verified exit zero.

## Physical-state probe preparation

A fresh private candidate reuses the exact reviewed plugin/definitions and adds
read-only ordinary character-state observations around three fixed actual-ped-XY
height queries. Strict boolean state and finite velocity/speed observations remain
separate from physical contact, collision loading and intended floor identity;
those fields remain unknown. This is not a four-checkpoint collector.

Independent source review caught process-binding and late-observation gaps.
Shutdown now binds the preflight-validated PID/start identity; launch identity is
retained for collection, and the collector refuses already-executed queries on
attachment. It samples foreground readiness and requires exact public/private
row correspondence. JavaScript and Windows PowerShell syntax checks pass.
The two-second delay assists scheduling, not synchronization. Interrupted staging
requires manual recovery from the preserved transaction/backups; automatic
interruption recovery is not claimed. No staging, native calls, launch or
physical-support runtime trial occurred for this candidate.

## Limits and next step

The earlier boolean-only result left heights unobserved; the follow-up resolves
that narrower gap. Neither result independently proves loaded collision at each
query or the intended floor/layer. Neither is checkpoint qualification or
complete riding/restart acceptance.

Pinned [memory documentation](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/using-memory.md)
requires `mem` permission for reads/writes. The ordinary diagnostic filename
requested none; [default Lax behavior](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/permissions.md)
rejects such operations. Actual settings and the caught exception's exact call
were not observed, so this remains a likely prerequisite mismatch.

Bounded review of the pinned
[GTA IV native catalogue](https://github.com/sannybuilder/library/blob/34bedee0be2f57047ed8f0705c81f137ede3d3ce/gta_iv/gta_iv.json)
found no already-qualified independent arbitrary-point loading and floor-identity
oracle. A ped waiting condition describes the ped; model collision readiness
does not identify a static world instance, and a collision request is not a
readiness result. This is a bounded negative finding, not proof that the engine
has no internal interface. Old-version SDK offsets remain unqualified for CE.

Inspect the fresh four-point view sets locally to resolve checkpoint anchor bases,
then gather ordinary GTA physical
support at each independently identified surface, alongside fixed paired query
readings. Physical support is a proposed empirical witness, not evidence already
collected here. Whether it satisfies the separate loading criterion must be
explicitly resolved on the owning issue; do not silently set loading/layer flags
from query success, ped waiting state or numeric agreement. If an engine loading
oracle is required, the exact-version interface gap remains. Finish #39 before
#54 activation. Preserve the flat guard and existing geometry.
Board #55 and rider #56 remain downstream. #20/#52 stay open and both source
drafts await acceptance. Temporary prototypes remain in the private debug area.
