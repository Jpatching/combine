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

Next resolve the four checkpoint anchor bases and gather ordinary GTA physical
support at each independently identified surface, alongside fixed paired query
readings. Physical support is a proposed empirical witness, not evidence already
collected here. Whether it satisfies the separate loading criterion must be
explicitly resolved on the owning issue; do not silently set loading/layer flags
from query success, ped waiting state or numeric agreement. If an engine loading
oracle is required, the exact-version interface gap remains. Finish #39 before
#54 activation. Preserve the flat guard and existing geometry.
Board #55 and rider #56 remain downstream. #20/#52 stay open and both source
drafts await acceptance. Temporary prototypes remain in the private debug area.
