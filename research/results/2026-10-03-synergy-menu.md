# Synergy-derived native menu — 2026-10-03

The rejected console-text practice panel is replaced by a native right-side menu.
Source/build/synthetic input checks and native asset-free rendering checks passed.
A fresh Windows development trial was prepared and launched. Owner controller
and gameplay acceptance is pending; no source publication or release has occurred.

## Source and scope

- Combine branch/base at start: `main`, `714660171c6726241075913308e3009516c3ebb6`.
  Pre-existing dirty documentation/evidence and the original untracked practice
  patch were preserved and extended. No implementation commit has been made.
- Runtime: [v0.4.0 source](https://github.com/chasmlol/2010-rust-rewrite-mashup/tree/f608f85e407ff1b7689d54a9aafdd16e95711ac4).
- Menu: [Synergy MW2 source](https://github.com/SyndiShanX/Synergy-GSC-Menu/blob/33bcc80f5446e7543a2eb68b17c798e29d3f27c4/MW2/Synergy/maps/mp/Synergy.gsc).
  Source inspected: initial_variables/create_menu/input_manager, visibility,
  submenu history, cursor scrolling and option rendering. Exact hashes and source
  scope are in [the lock](../upstream.lock.json).
- Both remote HEADs and the selected runtime tag/Synergy main were refreshed on
  this date and still matched these pins. No baseline was advanced.
- Reviewed artifact: [trickshot-v0.4.0.patch](../../patches/trickshot-v0.4.0.patch),
  SHA-256 `44f037ae7a459209bcc081cc8ce7e26e7de886936ff414bb5ba1aa08f9e01812`.
  It includes complete new Rust sources, integration edits, preview, tests,
  COMBINE-NOTICE.md and the upstream GPLv3 text. No binary/assets are included.

The native port keeps a seven-slot viewport, history/cursor restoration and typed
actions, with cyan styling and the existing proportional Oxanium game font.
Closing removes all UI entities. Physical keyboard state survives the gameplay
input reset so the release barrier also covers held keys after close. Pad menu
navigation and gameplay/skating publication observe the same capture state.
Action feedback stays inside the menu; request acceptance is not claimed as
completed movement/spawn. Existing local authority queues remain the action path.

## Build and verification

Toolchain: Rust `1.95.0 (59807616e 2026-04-14)`, cargo-xwin `0.23.1`, Ubuntu
Clang/LLVM `19.1.1 (1ubuntu1~24.04.2)` for native dependencies. Rust's bundled
rust-lld uses LLVM 22.1.2. Existing cargo-xwin SDK/CRT cache was reused. The
upstream Cargo.lock dependency versions were retained; the only lock additions
are console dependencies on hud_iw4/playerstate_iw4 and test-only gamemode_iw4.
A temporary lock regeneration changed versions; those changes were discarded
before the successful final builds. No dependency update is part of the patch.

Commands from the patched runtime checkout, with the local cargo-xwin and LLVM
19 bin directories on PATH and its LLVM library directory on LD_LIBRARY_PATH:

```sh
cargo +1.95.0 xwin test --offline --locked --profile play --target x86_64-pc-windows-msvc -p console --lib --no-run
cargo +1.95.0 xwin build --offline --locked --profile play --target x86_64-pc-windows-msvc -p console --example practice_menu_preview -p launcher
cargo +1.95.0 xwin build --offline --locked --profile play --target x86_64-pc-windows-msvc -p launcher --bin iw4l
```

All exited 0. The final runtime build completed in 10.89 seconds using the warmed
cache. Runtime SHA-256:
`298c5b4097e7fd8b18632d7dacd1b62c0c39977905eb3a9e5642c92c721dcdf0`.
Patched Cargo.lock SHA-256:
`dc1689f140c5fac899126f60dfa82dee97df76d65eccd78e604952061a783a5d`.

The Windows console test executable was run with `practice --nocapture`:
**18 passed, 0 failed, 0 ignored, 0 filtered out; 0.08 seconds.** It exercises:

- Closed defaults, submenu backtracking and remembered selection; seven-slot
  scroll/wrap boundaries, delayed repeat and non-repeating actions.
- Opening-chord consumption; Escape closes without reaching pause; keyboard and
  pad holds cannot shoot/jump/melee/toggle skating until release.
- Missing save/bot/preset feedback, save/return through existing action queues,
  leaving skating first, timeout/missing queue errors, map invalidation.
- Dummy bot request, freeze toggle, smooth preset/restore snapshot.
- Default-off aim lock; aim release, skating, menu capture, human presence,
  non-alive target, teammate and synthetic wall exclusions; angular boundaries.
- Closed native renderer has zero UI nodes, including with aim lock enabled.

`git apply --check` and apply succeeded against clean selected-base copies of all
modified upstream files. The two pure suites compiled from that applied patch:
**6 menu tests + 4 policy/math tests passed.** This checks the reviewable artifact,
not only the ignored development checkout. Final workspace/patch equality was
checked for every included source and licence file.

Native Windows preview executable ran at **1280×720 and 1920×1080**, each exiting
0. Root, Aim, missing-bot feedback and closed states were captured locally. Visual
inspection confirmed proportional font, cyan selection, submenu arrows, right-side
placement, unclipped labels and wrapped error feedback. Both closed images are
blank backgrounds. The preview uses the production renderer with no game assets,
profile, game UI layers or network. In-game contrast, pause interactions and
controller feel still need the owner's observations. Local previews remain under
ignored `.private/trickshot/preview-720` and `preview-1080`.

Inherited build warnings: render_frame has a must_use attribute on a static;
skate-host has two private-interface warnings. The preview also reports seven
unused-navigation warnings because it includes the production state module for
its shared labels/types; these are not runtime errors. Early build errors in
new test wiring were fixed before the passing build. No warning was suppressed.

## Trial and owner checkpoint

[Preparation script](../../scripts/prepare-trickshot-trial.ps1) copied the prepared
baseline into `%LOCALAPPDATA%\CombinePilot\v0.4.0\synergy-menu-dev`. The destination
was fresh. Deployed SHA-256 matched the above binary; source runtime executable
hash was unchanged. The existing `trickshot-dev` and `mw2-skate` trials remain.
The script's first invocation was blocked as unsigned by Windows; the approved
retry used an execution-policy override for that process only, without changing
machine policy. A separate **Combine Synergy Menu** desktop shortcut was created.

The prior game closed, confirmed by the owner. The new executable was launched
with `map mp_rust` (process 70180). Process/window checks establish launch only.
No game screenshot, game files or raw private gameplay logs were uploaded. No
OBS recording was made. The full post-session original-game hash comparison
remains outstanding from the baseline work.

Next: owner follows the [sense-check](../../docs/TRICKSHOT_MENU.md#owner-sense-check)
and reports replacement acceptance or concrete changes. Only then publish the
reviewed source/notices to Jpatching/combine. An unauthenticated read-only
`git ls-remote` of that destination requested credentials; existence/access was
not established. The connected GitHub search and local `gh repo view` also could not resolve
that repository (absent or inaccessible). No remote is configured locally. Do not infer GitHub access or
claim publication. The stunt launcher (old plan removed)
remains a separate proposal with no implementation.

## Final repository gate

`python3 scripts/verify.py` exited 0: lock structure, two recipes, local links in
13 documents and **16 Python tests passed** (0.087 seconds). `git diff --check`
exited 0. All 13 patch files matched the patched build checkout byte-for-byte;
the licence also matched the pinned Synergy licence verbatim. The result was
appended after the gate without changing source, pins or link targets.

The new trial's process was checked after launch: running, responding, title
`iw4l - mp_rust`. The owner has been asked for an explicit replacement verdict;
no affirmative acceptance has been received. The owner reported that the options
were unchanged, asked where EB was, and requested ideas for a bigger crossover.
Clarified that this slice ported presentation/navigation and retained eight practice
actions; no EB or other Synergy gameplay feature was implemented. The owner confirmed EB means explosive bullets;
preferred library games remain pending. This is not acceptance.

GitHub follow-up: the locally authenticated account was verified to match
Jpatching (boolean comparison only; no credentials exposed). The requested
repository still could not be resolved. Creation/publication remains conditional
on replacement acceptance; no repository or remote was created.
