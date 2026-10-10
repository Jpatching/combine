# Automated GTA ground diagnosis — 2026-10-10

Source workspace: `implement/gtaiv-qualified-ground` at
`a9760d0a8ca99269376dfa086c144463410615a4`. Ground implementation remains
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

## Limits and next step

Boolean success does not prove the buffer height, loaded collision at each
query or the intended floor/layer. This was not a stationary character-height
survey, checkpoint qualification or complete riding/restart acceptance.

Pinned [memory documentation](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/using-memory.md)
requires `mem` permission for reads/writes. The ordinary diagnostic filename
requested none; [default Lax behavior](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/permissions.md)
rejects such operations. Actual settings and the caught exception's exact call
were not observed, so this remains a likely prerequisite mismatch.

Reuse the earlier plugin-owned output-buffer proof to obtain paired successful
heights, or use a permitted scoped diagnostic. Then finish #39's independent
floor/layer qualification before #54 activation. Preserve the flat guard and
existing geometry; do not infer qualification from a finite height or boolean.
Board #55 and rider #56 remain downstream. #20/#52 stay open and both source
drafts await acceptance. Temporary prototypes remain in the private debug area.
