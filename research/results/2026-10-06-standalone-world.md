# Standalone Skate world preparation — 2026-10-06

C-023 introduces a validated world-only input into the existing Rust Skate host.
Callers can reject malformed/excessive collision geometry before reading assets
or starting physics, then prepare a host without MW match startup. This is the
first implementation sub-slice toward the full-island spec, not a renderer or
Fortnite decoder. Real host preparation with game data, gameplay and owner
acceptance remain unverified.

[Specification](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=262165772),
[C-023](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=263192627),
[next rendering ticket](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=263192734).
Full-island destination and selected Fortnite version unchanged. No voice changes.

## Implementation and boundary

Source patch: `patches/skate-standalone-v0.4.0.patch`, directly against runtime
`f608f85e407ff1b7689d54a9aafdd16e95711ac4`. Separate ignored checkout; existing dirty
Synergy runtime untouched. Changes are limited to Skate-host public module export,
new `standalone` module, public integration tests, example and standalone Cargo.lock.
No new dependency, game asset, network reader or file-format schema is introduced.
The root runtime Cargo.lock stays unchanged; standalone dependencies were resolved
from its copied lock using the cached registry and captured in their own lock.

`World::validate` consumes native triangle/rail/spawn/heading vectors and explicit
caller limits. It rejects empty/non-finite/degenerate geometry, unstable triangle
area or rail segment math, coordinate range, invalid budgets and host rail-ID
overflow. Checked payload sizing and count limits precede geometry traversal and
host expansion. Validated fields are private so they cannot change before
`World::prepare` invokes the existing `Session::new`. Errors returned from
preparation omit private asset paths; upstream startup diagnostics remain local.
No global match/renderer is installed; success transfers the host to the caller.

Limits apply to already allocated native input payload, not total process/physics
memory. A future file decoder must bound allocations before making these vectors.
Collision-clear spawn, coordinate/scale fidelity, grind quality, material/index
validation, unsafe file references and full-island resource budgets belong at the
real decoder/render/world integration and remain unimplemented. This API checks
finite spawn/heading, not that a spawn is safe to skate. The native input is Y-up
host coordinates; no MW-to-Skate transform is applied twice.

```text
Native triangles/rails/spawn + explicit limits
  -> validate -> owned World -> private Skate asset root -> existing host
       | reject: typed error       | missing/incompatible: redacted error
       +-- no asset read/physics   +-- no global session installation
```

## Reproduction

Apply the patch to a clean pinned runtime checkout, not the menu trial:

```sh
git apply --check /absolute/path/to/combine/patches/skate-standalone-v0.4.0.patch
git apply /absolute/path/to/combine/patches/skate-standalone-v0.4.0.patch
cargo +1.95.0 test --offline --locked --manifest-path skate/crates/skate-host/Cargo.toml --test standalone_world
cargo +1.95.0 run --offline --locked --manifest-path skate/crates/skate-host/Cargo.toml --example standalone_prepare -- --validate-only
```

Offline commands require the cached dependencies; missing cache is a toolchain
prerequisite, not a reason to change pins. Implementation used target directory
`.private/fortnite-build` from the Combine root. Native host: Linux x86_64 WSL2,
Rust/Cargo 1.95.0. Windows native build/physical controller not checked this slice.

The example's `--assets <local-Skate-root>` prepares/drops the synthetic host;
it does not render or tick gameplay. With `--validate-only`, it prints explicitly
that no assets, host or gameplay were tested. Missing directory and invalid CLI
arguments exit 1; successful asset-free validation exits 0. Asset names/paths are
not returned in the new public preparation error.

## Checks and inherited debt

- Red: initial public test failed to compile because `standalone` did not exist.
  Green: first non-finite geometry test passed after adding the boundary.
- Red/green regressions: tiny triangle area and tiny rail segments initially
  passed validation; tests demonstrated underflow and drove stable-f32 checks.
- Focused native integration tests: 13 passed, 0 failed. Includes valid input,
  count/byte boundaries, malformed rails, rail-ID overflow, missing directory and
  incomplete local assets using a source-only directory.
- Standalone example: asset-free validation passes; missing asset root and invalid
  flag fail explicitly. No real Skate assets opened and no game launched.
- Broader `cargo test --all-targets`: FAILED before tests because upstream
  `physics.rs` references missing `src/tests/map_startup.rs`. Pinned Git source
  contains the reference and no tracked host tests directory. This inherited
  failure is not removed or waived; full Skate-host unit suite is unverified.
- Independent review found long/thin overflow and near-collinear normal underflow
  gaps. Both were reproduced red, then fixed by matching the host normal check
  and native triangle constructor; regression cases now pass.
- Final patch replays byte-for-byte across all 5 changed files in a clean pinned
  checkout. SHA-256:
  `0c9ee1c9d295c3508d95fe067ceb4b6bae13fba2ebeb208372d507e36df11c3c`.
- Three inherited Linux compile warnings: unused input capability cache and two
  private-interface warnings. No unrelated cleanup included.

Repository gate: PASS, 27 tests (4 inherited scaffolding tests), 2 recipes and
17-document links. Independent Standards and Spec re-review: no remaining
actionable findings. `git diff --check`: PASS. A local source checkpoint is not publication, merge, release or
owner acceptance. Next: render/input/camera ownership through the standalone
session (C-025), after local Skate prerequisites are verified; C-024 independently
needs the authentic selected-build export witness. That earlier remote observation is superseded: remote main a5593d6 and the
qualification branch b399c55 are published, with PR #1 open and unmerged. See the
[current handoff](../../docs/HANDOFF.md); C-024 input is current, C-025 follows its
asset prerequisite check. Review the complete PR diff before proposing merge.
