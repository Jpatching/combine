# Current context — Fortnite + Skate

**Goal:** the complete selected interactive Fortnite island with actual Skate
movement, tricks and grinds, retaining building/editing/destruction. No playable
integration exists. [Requirements](../research/results/2026-10-06-fortnite-adapter-qualification.md).

**Previous investigation:** C-024 investigated the selected 12.41 CL12905909 executable's
integrity mismatch and whether matching original input is obtainable. The previous board cards are historical planning, not an active task queue.

**Last recorded evidence:** manifest mismatch and Authenticode HashMismatch; ZIP CRC
passed and disk hashes agree. Cause remains unresolved; 397 manifest files and
39 extras remain unchecked. [Acquisition evidence](../research/results/2026-10-06-fortnite-12-41-preparation.md).
Private diagnostics remain in ignored `.private/fortnite-12.41/`. No new download,
launch, login or protection changes are authorized by this workflow cleanup.

**Parked:** Synergy's physical trial remains unaccepted; hit radius is unimplemented.
Prior gameplay was owner-reported; recovery/repeatability remain incomplete.
[Historical trials](archive/HANDOFF-2026-10-07.md).

**Fresh start — 2026-10-07:** existing implementation retained. PRs #1 and #2
closed without merging. The previous workflow, task routing and backlog are
retired. The next work comes from the owner's request; no old task is selected.

**Baseline recovery — 2026-10-07:** the owner authorized one recovery PR from
preserved tip `03444e2`, retaining implementation and final documentation cleanup.
The [recovery PR #3](https://github.com/Jpatching/combine/pull/3) uses branch
`recovery/source-baseline-20261007`; local backup
`backup-recovery-source-20261007` preserves the pre-recovery source tree, and
`backup-clutter-state` retains the original history. Resume this recovery before
starting another source slice. Matt's original skills remain unchanged.

Fresh checks pass: repository gate (34 tests), standalone Skate patch replay
against runtime `f608f85e407ff1b7689d54a9aafdd16e95711ac4`, 15 standalone tests,
asset-free preparation example, exporter Release build and 13 synthetic CLI
checks. Independent Standards review found an exporter private-root guard gap;
the fix verifies Git ignores the root and has no tracked files beneath it.
Follow-up Standards review resolved the guard finding; Spec review found no
actionable source findings in either revision. Exporter dependency restore uses
the committed lock; upstream projects warn about Microsoft.Bcl.Memory 9.0.0,
while the runner's resolved dependency manifest selects its pinned 9.0.14.

**Accepted recovery debt:** `cargo +1.95.0 test --offline --locked --manifest-path
skate/crates/skate-host/Cargo.toml --all-targets` fails to compile because pinned
upstream `src/physics.rs:401` references missing `src/tests/map_startup.rs`.
The full host suite remains unverified. The owner explicitly selected merging
this recovery with that inherited debt recorded, superseding the earlier hold
until the full suite passes. This exception applies to recovery PR #3; it does
not turn the failed check into a pass or waive future slice validation.

**Next authorized setup:** merge recovery using a merge commit, synchronize clean
local `main`, then create `prototype/fortnite-skate-surface` in a separate persistent
worktree from that updated `main`. Keep one active source slice, with a fresh
branch and worktree per new slice; resume unfinished work on its existing branch.
The native experiment asks whether the existing Skate simulation can drive a
visible marker on one real Fortnite surface. Rough presentation is accepted for
the first proof; actual Skate movement, collision, input and repeatability are
still required. Matt's HTML/UI `prototype` skill does not establish native
integration; use `implement`, focused checks and `code-review` for this experiment.
Keep experimental checkpoints on their branch and promote useful implementation
through reviewed PRs. The immediate task is setup and a fresh-session handoff;
client acquisition and game launch are not included. No game assets were loaded,
game launched, real export performed or owner gameplay acceptance claimed here.
