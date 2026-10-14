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
Use Git and the relevant PR for revision/push state; [workflow #61](https://github.com/Jpatching/combine/issues/61)
owns the current GTA candidate and verdict. An older revision cannot reproduce
later source changes.
The gate checks research metadata, recipe inputs, tracked Markdown links and tests; it proves no
playable integration. The checker reports invalid inputs and returns nonzero.
The `repository-checks` CI job runs this same gate on pull requests and pushes to
`main`. It does not compile the native runtime or establish gameplay acceptance.

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
the reference trial below identifies the preserved input checkpoint.
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
The [current contract](FORTNITE_SKATE.md) requires Fortnite building/editing/destruction
with Skate movement/tricks/grinds. Follow the linked live experiment for candidate
selection and first-proof acceptance. Establish usable exact-client startup and
reviewed native execution before the Skate experiment; missing adapter code is
experiment work. Historical candidate ordering does not select today's task.

A future guide must record exact client/server/Skate revisions, lawful private
input requirements, reviewed dependencies, coordinate/collision conversion and
observed build/skate/jump/grind/edit/destroy/recovery/relaunch results. Full-island
checks add coverage and identified-hardware measurements. Owner verdict remains
separate. No game assets, binaries, settings or private logs belong in source.

## Preserved Synergy reference build

The input checkpoint is `c5910860c57b69c7e7c8dc2edae88f3cf99a31f7`,
built from the five-patch chain above. Its executable SHA-256 is
`e06c7f1fc217523485363fe156fe448ea94b2cba8b14c52cb66a3d4fff5e9268`.
The input patch SHA-256 is
`00af9a992b9ce7b04c1ce3a89a37734377a129093dbff3f6e04aa7453e091527`.
Compare the actual trial manifest and bytes before reuse. These are historical
build identities, not acceptance of physical input or all menu options.

Native preview reproduction uses the same Windows toolchain:

```sh
cargo +1.95.0 xwin build --offline --locked --profile play --target x86_64-pc-windows-msvc -p launcher --bin iw4l -p console --example practice_menu_preview
```

The preview is an asset-free renderer check of the earlier native menu, whose
presentation the owner rejected. The requested menu is actual Synergy GSC.
Keep LLVM 19 bin directories on PATH and its library directory on
LD_LIBRARY_PATH when building native dependencies. Preserve upstream lock
versions; regenerating Cargo.lock changes the reproduction inputs.

## Standalone Skate world preparation

Apply this independent patch to a clean runtime at the same pin, outside the
menu trial. It supplies native world input, not a Fortnite decoder or renderer.

```sh
git apply --check /absolute/path/to/combine/patches/skate-standalone-v0.4.0.patch
git apply /absolute/path/to/combine/patches/skate-standalone-v0.4.0.patch
cargo +1.95.0 test --offline --locked --manifest-path skate/crates/skate-host/Cargo.toml --test standalone_world
cargo +1.95.0 run --offline --locked --manifest-path skate/crates/skate-host/Cargo.toml --example standalone_prepare -- --validate-only
```

Offline commands need cached dependencies. The standalone crate has its own
lockfile; the runtime root lock stays unchanged. Native input uses Y-up host
coordinates. `--validate-only` reads no game assets and does not prepare gameplay;
`--assets <local-Skate-root>` prepares and drops a synthetic Session.
The pinned host's full unit suite references missing `src/tests/map_startup.rs`;
the full upstream suite remains unverified. The retained rail regression checks
the exact host arithmetic rather than assuming finite endpoints imply a safe rail.

GTA reproduction and runtime checks belong to the [candidate #69](https://github.com/Jpatching/combine/pull/69)
and its `tools/gtaiv-skate/README.md`; the cleanup branch does not contain that
unmerged adapter. Use the candidate's exact revision and instructions for native
builds and the qualified local ride. File hashes alone do not prove loaded source.
