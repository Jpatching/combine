# Reproduce Combine source checks and the Synergy build

This guide separates public source validation, runtime compilation and private
player trials. Cloning Combine does not supply game data or a ready-to-play game.
Rust owns gameplay; original GSC owns Synergy's menu. Python/PowerShell are helpers.

## Check this source repository

With Git and Python 3.10+ (no Python packages required):

```sh
git clone https://github.com/Jpatching/combine.git
cd combine
python3 scripts/verify.py
python3 scripts/check_recipe.py recipes/mw2-skate.json
```

On Windows substitute `py -3` for `python3`. Select the desired source branch and
record `git rev-parse HEAD` and `git status --short` before comparing evidence.
Use the revision/push state in [the handoff](HANDOFF.md); cloning an older remote
revision will not reproduce later local documentation checkpoints.
The gate checks research metadata, recipe inputs, links and tests; it proves no
playable integration. The checker reports invalid inputs and returns nonzero.

## Compile actual Synergy in the pinned Rust runtime

Use a separate source checkout, never an original game installation. Example
from the Combine root, using its ignored private workspace:

```sh
git clone https://github.com/chasmlol/2010-rust-rewrite-mashup.git .private/reproduce-runtime
git -C .private/reproduce-runtime checkout --detach f608f85e407ff1b7689d54a9aafdd16e95711ac4
```

From that new runtime checkout, apply these Combine patches in this order,
replacing `/absolute/path/to/combine` with this source repository's path:

```sh
git apply --check /absolute/path/to/combine/patches/trickshot-v0.4.0.patch
git apply /absolute/path/to/combine/patches/trickshot-v0.4.0.patch
git apply --check /absolute/path/to/combine/patches/skate-audio-v0.4.0.patch
git apply /absolute/path/to/combine/patches/skate-audio-v0.4.0.patch
git apply --check /absolute/path/to/combine/patches/intervention-v0.4.0.patch
git apply /absolute/path/to/combine/patches/intervention-v0.4.0.patch
git apply --check /absolute/path/to/combine/patches/synergy-gsc-v0.4.0.patch
git apply /absolute/path/to/combine/patches/synergy-gsc-v0.4.0.patch
git apply --check /absolute/path/to/combine/patches/synergy-input-v0.4.0.patch
git apply /absolute/path/to/combine/patches/synergy-input-v0.4.0.patch
```

Stop on a failed check; do not force a partial application or change the pin.
The early patches are dependencies, not the selected native-menu experience.
The final patches execute actual Synergy. Deferred Hide HUD stays excluded.

Established Linux-to-Windows tools: Rust 1.95.0, cargo-xwin 0.23.1, Clang/LLVM
19.1.1, Rust's rust-lld and a separately provisioned Windows SDK/CRT cargo-xwin
cache. Preserve Cargo.lock. Dependencies and cache preparation require access;
this guide does not claim a clean-machine toolchain installation was tested.

```sh
cargo +1.95.0 xwin build --locked --profile play --target x86_64-pc-windows-msvc -p launcher --bin iw4l
cargo +1.95.0 xwin test --locked --profile play --target x86_64-pc-windows-msvc -p sim -p console --lib --no-run
```

Run the resulting sim tests with `synergy` and console tests with `practice` on
Windows. Record results, executable SHA-256, patch hashes and source revision.
[Menu guide](TRICKSHOT_MENU.md) owns diagnostic and trial preparation commands;
[exact-build evidence](HANDOFF.md) identifies the preserved reference trial.
These commands are drawn from recorded build evidence; they were not rebuilt
in this documentation session and platform-specific tools remain prerequisites.

## Prepare a private player trial

Use lawfully available local data and the [Windows baseline](WINDOWS_BASELINE.md).
Prepare a new versioned isolated trial and review folder through the
[trial adapter](../scripts/prepare-trickshot-trial.ps1), with actual Synergy enabled,
all required evidence and the [Synergy checklist](../templates/synergy-checklist.txt).
Verify without launching; preserve previous trials and original installations.
An incomplete folder or started process is not playable acceptance.

```text
Public source -> offline checks -> pinned Rust + patches -> exact Windows binary
Private lawful data + binary -> isolated trial -> owner play -> explicit verdict
Missing tools/data/check failure -> stop that stage, record exact prerequisite
```

## Fortnite with Skate: qualification comes before reproduction

There is no playable interactive Fortnite + Skate integration to reproduce yet.
[D-026 and the current specification](../research/results/2026-10-06-fortnite-adapter-qualification.md)
require Fortnite building/editing/destruction with Skate movement/tricks/grinds.
Qualify Project Reboot first; identify a compatible accessible client and reviewed
isolated launch route, then live collision/lifecycle, controls/pose and rendering
seams. A particular version, Combine and Blender are not mandatory. Earlier
static exports and preparation scaffolding do not satisfy this contract.

A future guide must record exact client/server/Skate revisions, lawful private
input requirements, reviewed dependencies, coordinate/collision conversion and
observed build/skate/jump/grind/edit/destroy/recovery/relaunch results. Full-island
checks add coverage and identified-hardware measurements. Owner verdict remains
separate. No game assets, binaries, settings or private logs belong in source.
