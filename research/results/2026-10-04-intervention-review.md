# Preserved Intervention build and review helpers — 2026-10-04

The native Intervention implementation passed its technical checks, but the
owner rejected its presentation as the requested replacement and confirmed
**Synergy itself**. This is preserved development evidence, not an accepted
menu, gameplay result or release. D-015 supersedes the native-menu mechanism.
No owner review folder was prepared for this build.

## Source and build identity

- Inherited checkpoint: `b7aed59a27ca59f507338db76c98cccac5f8c023`.
- Source branch: `slice/intervention-review`.
- Adapter/implementation: `f1c960a8a62004fcfcbaf7746e1c60207527558f`.
- Tested native source: `730b11354934b43c2ca703aec615ea31d3e77f2e`.
- Runtime pin: `f608f85e407ff1b7689d54a9aafdd16e95711ac4`.
- Synergy reference pin: `33bcc80f5446e7543a2eb68b17c798e29d3f27c4`.
- Windows executable SHA-256:
  `3a9992ce4ab9f489d6895d3774cb8b96b9609c4a7ce2c99dd601f04d292b92b7`.

Apply these patches in order:

| Patch | SHA-256 |
| --- | --- |
| `trickshot-v0.4.0.patch` | `44f037ae7a459209bcc081cc8ce7e26e7de886936ff414bb5ba1aa08f9e01812` |
| `skate-audio-v0.4.0.patch` | `0f42b291c87ee2a57ee19a29603298ebd359abb9ead97743b475571101aa4456` |
| `intervention-v0.4.0.patch` | `3815a63856d332f8a7e8ea8bdf9453d3925b45fbd181b4162457d78c8ce4f624` |

Deferred Hide HUD was excluded and preserved unchanged, SHA-256
`31568ed152da16aecd4a93194c602e9a8fe05af29744a52e45936e7dbf3e780a`.
Both upstream refs were refreshed October 4 and matched their existing pins.
The patch was applied to a clean runtime plus menu/audio baseline; its eight
changed files matched the tested source byte for byte.

## Behavior and checks

The preserved native build has six root sections and only the Intervention path
enabled. It submits a typed weapon request and correlates client, request, weapon
and match generation. "Equipped" requires both the acknowledgement and an alive
player actually holding the weapon in inventory. Missing/dead worlds, unavailable
catalogues, duplicate pending requests and a ten-second confirmation timeout
produce feedback. Standard ammunition is used. This does not reproduce Synergy's
full menu or its delayed 999-round behavior.

Tools: Rust 1.95.0, cargo-xwin 0.23.1, Clang/LLVM 19.1.1, existing Windows SDK/CRT.
Commands from the patched upstream root:

```sh
cargo +1.95.0 xwin build --offline --locked --profile play --target x86_64-pc-windows-msvc -p launcher --bin iw4l -p console --example practice_menu_preview
cargo +1.95.0 xwin test --offline --locked --profile play --target x86_64-pc-windows-msvc -p console --lib --no-run
```

- Final Windows build passed. Existing render/skate visibility warnings remain.
- Console test executable run on Windows with `practice --nocapture`: **17 passed,
  zero failed/ignored/filtered** (six navigation and eleven integration checks).
- Synthetic production-UI previews at 1280×720 and 1920×1080: root, Intervention,
  error and closed states captured and inspected. Labels were readable and closed
  state empty. **Owner rejected this native presentation as the replacement.**
- Raw build/test/render logs, images and the preserved executable remain local
  under the ignored `.private/intervention/` evidence directory. Initial fixture
  setup, prompt binding and preview-launch failures were corrected before these
  final results; they are not gameplay results.

## Shared handoff helpers

Reusable helpers are installed in the global solo-development workflow directory.
Combine's committed adapter is `scripts/prepare-trickshot-trial.ps1`; its draft
checklist is `templates/intervention-checklist.txt`.

- Shared board/hook tests: **15 passed**. Required views are validated while extra
  views survive; updates preserve unrelated items, read back bodies/fields, stamp
  actual starts once, and report API/read-back failures as sync pending.
- Windows review-bundle fixtures: **14 passed**. Actual shortcuts opened the
  synthetic executable/files/checklist. Missing or changed binaries, existing
  destinations, duplicate launches, an independently running process, copy failure,
  shortcut failure and failed required checks were exercised. No game assets were
  used in those fixtures. Synthetic launch success is not gameplay evidence.
- Start date and Target date fields exist on the existing private Project.
  C-016's actual start is October 4; target remains blank. The extra roadmap view
  and unrelated drafts were preserved. Roadmap date-field mapping needs a UI check;
  the exposed API did not report it.

The public source repository `https://github.com/Jpatching/combine` was created
and ADMIN/PUBLIC access verified, then connected as `origin`. No source push,
PR, merge or release occurred. Current project instructions still require owner
replacement acceptance before source publication. No assets, private logs,
recordings or settings were added to source history.

## Current continuation

Use the actual pinned Synergy GSC with the existing runtime script engine.
The source's MW2 README requires IW4x; compatibility must be demonstrated.
Do not present the native build above as the requested menu. Actual integration
results and the next action are in the [handoff](../../docs/HANDOFF.md) and the
existing [C-016 draft](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=261972158).
