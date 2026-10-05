# Handoff — actual Synergy trial ready for owner test

The actual pinned Synergy GSC menu runs with its own presentation/options.
Intervention equip and input isolation passed bounded runtime and synthetic
checks. A versioned local trial is prepared; owner gameplay testing and exact-build
acceptance remain separate. Other option effects and trickshot hit radius are
unverified. The owner reports Intervention worked in the preceding most recent
trial, with other options missing; its exact build was not identified.

Phase 6 owner trial for the input checkpoint; one coverage batch follows, basic
loadout controls. The supplied six-batch order and release definitions are in
[WORKFLOW.md](WORKFLOW.md), D-018 and the live private board. Hide HUD stays deferred.
Fortnite qualification remains after the menu dependencies.

```text
Physical input -> actual Synergy GSC -> original menu action
       | captured / closing / held controls -> block gameplay
       | neutral release -> fresh input -> ordinary gameplay
       v
Exact trial -> owner test/report -> further option batches -> explicit acceptance
```

## Exact trial and source

Desktop folder: **Combine Synergy - 2026-10-05 - c591086**. Shortcuts:
**Test Synergy**, **Open trial files**, **Read checklist**. Source checkpoint
`c5910860c57b69c7e7c8dc2edae88f3cf99a31f7`, branch
`slice/synergy-input-isolation`, base
`b52c28f6fe1a21c81f610a7d96a7e48d7f953650`.
The subsequent documentation commit records delivery without changing build source.
Resolve branch HEAD with Git; never infer a merge or release.

Executable SHA-256:
`e06c7f1fc217523485363fe156fe448ea94b2cba8b14c52cb66a3d4fff5e9268`.
Review manifest read-back matches source checkpoint, executable, prepared/unaccepted
state and three shortcuts. `launch.ps1 -VerifyOnly` passes without launching.
Source runtime executable and settings are preserved; older trials remain.
The manifest includes all five patch hashes and unchanged runtime/menu pins.
Input delta is committed as `patches/synergy-input-v0.4.0.patch`; the ignored runtime
checkout is still intentionally dirty. Private logs/assets/settings remain excluded.

## Checks and limits

[October 5 evidence](../research/results/2026-10-05-synergy-input.md) records commands,
failed runs and inherited debt. Current successful checks:

- Windows build: pinned Rust 1.95.0 / cargo-xwin / play profile, launcher `iw4l`;
  hash unchanged after rebuild. Existing compiler attribute/private-interface
  warnings remain, no new warning repair included.
- Windows sim `synergy`: 4 passed; console `practice`: 20 passed.
- Repository gate `python3 scripts/verify.py`: 23 tests, 2 recipes, links in 14 docs.
- PowerShell log redaction/order fixtures and Synergy review adapter fixtures pass;
  shared review bundle suite: 14 checks pass.
- Input patch replays byte-for-byte across 16 runtime files.
- Corrected diagnostic 13 versus same-build disabled diagnostic 12 passes the
  strict checker: actual hierarchy/Intervention held/close/fresh shot, no observed
  open-menu shot, normal exit 0. Statistics/schema fault reproduced disabled.
- Corrected four PNGs are 1920x1080; preserved 720 captures are 1280x720.
  Root/Intervention visual inspection finds the original readable Synergy menu.

The 1080 PNG named closed still shows the menu; it does not prove closed
presentation. The stream records extra reopen/close transitions after the successful
close/fresh shot. Physical reliable close/reopen is an explicit owner checklist
item. Automated timed inputs and synthetic focus/reconnect checks do not establish
physical gameplay. Diagnostics 10 and 11 failed and are preserved privately;
old report 09 no longer passes the stricter provenance contract.

Independent bounded Standards/Spec review identified four diagnostic-evidence
issues; all corrected and re-reviewed without remaining actionable source findings.
Diagnostic faults from imported modules are retained with private arguments removed;
statistics exemption requires successful disabled same-build provenance.

Source publication read-back verified delivery revision
`c538565f49fe06b159a946888c74d560cb6256d7`; the existing card was moved to
Phase 6 and read back, preserving live views and unrelated items. Subsequent
handoff-only commits do not change trial source or executable; resolve current
branch HEAD and remote before continuing. No owner acceptance, local release, merge or public release.
Baseline recovery/freeze, audio listening and original-file comparisons remain
inherited gaps; no Fortnite adapter/assets are added.

## Next actor and check

Owner can test the game using Test Synergy: open with Aim+Melee, equip Intervention,
check keyboard/controller capture, close while holding Fire, release then fire,
focus/reconnect and quit/relaunch. Report this exact folder/build, any failing
control and which option effects worked. Other sections are available for inspection
but not verified as working. Codex then continues the basic loadout batch, checking
effects/reversal/failure/interaction, retaining unsupported entries as requirements.
