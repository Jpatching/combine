# Build and try the replacement menu

This slice gives the existing local practice actions a Synergy-derived native
menu. [README](../README.md) is the player guide; this document owns developer
reproduction and acceptance steps. No console commands are needed to use the menu.

```text
Physical buttons -> menu state (page, history, cursor, repeat, release barrier)
                          | closed / unavailable -> no menu UI
                          | open
                          +-> native proportional-font panel
                          +-> typed action -> local-host checks -> existing queues
                                                  | unavailable -> menu feedback
After closing -> wait for physical release -> gameplay controls resume
```

Navigation and practice actions are separate. The native panel has seven row
slots (unused slots remain blank). Action results remain visible until the next
action; an accepted queue request is labelled requested, not completed.

## Pinned source and build

Use runtime `f608f85e407ff1b7689d54a9aafdd16e95711ac4` (v0.4.0) and
Synergy `33bcc80f5446e7543a2eb68b17c798e29d3f27c4`. The pins and observed source
hashes are in [upstream.lock.json](../research/upstream.lock.json).
The patch contains the prior local practice implementation and its replacement
UI. Apply it to a clean checkout of the selected runtime, not over the old patch:

```sh
git apply --check /path/to/combine/patches/trickshot-v0.4.0.patch
git apply /path/to/combine/patches/trickshot-v0.4.0.patch
cargo +1.95.0 xwin build --locked --profile play --target x86_64-pc-windows-msvc -p launcher
```

Established cross-build tools: Rust 1.95.0, cargo-xwin 0.23.1, Clang/LLVM 19.1.1
for native dependencies, and Rust's bundled rust-lld linker. The Windows SDK and
CRT are the existing cargo-xwin cache; retain Cargo.lock. Upstream's moving
`stable` is not the reproduction pin. No upstream updater is built or published.
See the [result record](../research/results/2026-10-03-synergy-menu.md) for exact
local build commands, hashes, verification results and inherited warnings.

## Focused verification

The two pure Rust modules can be tested without dependencies or game assets:

```sh
rustc +1.95.0 --edition 2024 --test crates/console/src/practice_menu.rs -o /tmp/menu-tests
/tmp/menu-tests
rustc +1.95.0 --edition 2024 --test crates/console/src/practice_core.rs -o /tmp/practice-tests
/tmp/practice-tests
```

Build the actual input/action integration tests, then run the resulting console
test executable on Windows with the `practice` filter:

```sh
cargo +1.95.0 xwin test --locked --profile play --target x86_64-pc-windows-msvc -p console --lib --no-run
cargo +1.95.0 xwin build --locked --profile play --target x86_64-pc-windows-msvc -p console --example practice_menu_preview
```

The preview executable takes `width height fresh-output-directory`. Run it once
at `1280 720` and once at `1920 1080`. It renders the production UI on a plain
background, captures root/Aim/error/closed states and exits. It loads no game
assets or profile and opens no network interface. Keep generated images local.
This verifies native rendering, not gameplay or owner acceptance.

## Fresh Windows trial

Build `target/x86_64-pc-windows-msvc/play/iw4l.exe`, calculate SHA-256, and use
[scripts/prepare-trickshot-trial.ps1](../scripts/prepare-trickshot-trial.ps1):

```powershell
.\scripts\prepare-trickshot-trial.ps1 -Source '<prepared baseline runtime>' `
  -Binary '<built iw4l.exe>' -Destination '<fresh development folder>' `
  -ExpectedSha256 '<64-character build hash>'
```

The script refuses an existing destination or a mismatched binary, copies the
prepared baseline, rewrites internal runtime references, verifies the deployed
hash and checks the source executable remained unchanged. Failed preparation
retains the incomplete folder for inspection. It does not compare every original
game file; the baseline runbook's post-session hash check remains outstanding.

Close the prior game, then run `iw4l.exe map mp_rust` in the new folder. Optional
`-Launch` prepares and starts in one operation, refusing if another game is open.
Preparation, a started process and successful play are distinct results.

## Owner sense-check

At both 1280×720 and 1920×1080:

1. Launch on Rust: no practice panel/banner. Open with L2+R3 and F6; confirm the
   right-side layout and readable proportional text, arrows and cyan selection.
2. Enter each submenu and go back. Hold D-pad and triggers; selection repeats
   without firing. Cross/Square select; Circle/R3 go back. Escape closes only this menu.
3. Hold fire/jump/melee/skate buttons while closing: gameplay waits for release.
   Close with aim lock enabled: no practice overlay remains.
4. Try Return before saving and Place before adding a bot: error inside menu,
   menu stays open. Save, move, return; repeat while skating and confirm exit first.
5. Add/place/freeze a bot. Apply and restore the controller preset. Enable aim
   lock deliberately, verify release stops it, then turn it off.
6. Change maps: save cleared and aim lock off. Confirm recovery/relaunch.

Record pass/fail/not tested, readability and controller feel in the result record.
The old panel's rejection is not acceptance. Publish reviewed source and notices
to **Jpatching/combine only after explicit acceptance of this replacement**.
