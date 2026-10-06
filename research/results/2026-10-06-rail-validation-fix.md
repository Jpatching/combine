# Reject overflowing Skate rail chords before asset initialization

The owner requested the narrow fix for PR #1's reproduced rail-validation defect.
Ordinary skating was not observed failing. The defect affects extreme but finite
rail coordinates accepted with caller-selected large limits: validation used a
64-bit direct endpoint distance, while the pinned host constructs and evaluates
32-bit spline coefficients. Rounding can overflow the host's chord despite a
finite validator result.

## Change and boundary

The standalone World validator now uses the pinned host's actual coefficient and
endpoint arithmetic, then requires a normal finite squared chord length. It
returns `InvalidRail` before asset initialization when that arithmetic is
unstable. Existing error behavior, input limits, triangles, assets and normal
skating simulation are unchanged. Two public-boundary tests cover the review
witness and accepted normal/large/translated stable rails.

Source base: PR #1 head `b399c55b3abff6fc864fd3158f7df36b17906eac`.
Runtime pin: `f608f85e407ff1b7689d54a9aafdd16e95711ac4`.
The [pinned spline implementation](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-host/src/grind_world/spline.rs#L62)
constructs coefficients; its decoder reconstructs the endpoint and sums squared
32-bit chord components. The fix mirrors those operations rather than changing
host physics. The reconstructed endpoint includes the start coordinate, so
translated rails use the same arithmetic too.

Updated patch: `patches/skate-standalone-v0.4.0.patch`, SHA-256
`75a3e6293756b832db9ef49e041c9bffebc8186dbe7215deead6a2fe23508fe1`.
No game assets, original installations or private runtime checkouts were changed.
The source patch remains a preparation/input-validation feature, not a Fortnite
renderer, loader or playable bridge.

## Reproduction and results

Observed 2026-10-06, Rust/Cargo 1.95.0, Linux source-only scratch checkouts.
Apply the patch to a clean checkout of the exact runtime pin, then run:

```sh
cargo +1.95.0 test --offline --locked --manifest-path skate/crates/skate-host/Cargo.toml --test standalone_world
cargo +1.95.0 run --offline --locked --manifest-path skate/crates/skate-host/Cargo.toml --example standalone_prepare -- --validate-only
```

Actual commands used absolute scratch manifest paths and a shared temporary
`--target-dir` to reuse compiled dependencies; game assets were not inputs.

- Before correction, the prior `review_rail_regression` test reproduced failure:
  0 passed, 1 failed, exit 101; validation incorrectly returned `Ok(World)`.
- After correction, `standalone_world`: **15 passed, 0 failed**. This includes
  all 13 existing tests and the two added cases.
- Fresh pinned-source replay: `git apply --check` and `git apply` passed;
  resulting validator and test bytes matched the tested files exactly.
- `standalone_prepare --validate-only`: PASS, synthetic world validated; no assets
  loaded or host started.
- Repository `python3 scripts/verify.py`: PASS, 27 tests, two recipes, links in
  17 documents at this isolated PR branch.

Three inherited compiler warnings remain. The broader host test suite still has
inherited missing `src/tests/map_startup.rs` debt; this focused repair neither
reruns nor waives that unrelated failure. No Windows build or physical gameplay
claim is made. Review and source publication are separate from owner acceptance,
PR merge and release. The Fortnite same-process host-qualification task continues
independently after this correction.
