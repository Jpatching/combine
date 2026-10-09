# Separate Skate worker evaluation

Historical evidence from 2026-10-08. For current task authority and verdict, read
[the current context](../../docs/HANDOFF.md) and its linked live issue. Recommendations
below record this investigation; they do not select new work.

Evaluated 2026-10-08 for [issue #20](https://github.com/Jpatching/combine/issues/20). The owner selected offline GTA IV with ordinary gameplay preserved and approved evaluating a separate Skate process. Mount while on foot; Skate controls riding; dismount restores GTA movement, camera and vehicle use. [Recorded host decision](../../docs/adr/0001-preserve-offline-gta-gameplay.md).

## Result

**A separate worker can run the existing Skate Session, exchange real input and movement, retain a warm Session between rides, and restart independently of GTA.** Private Linux and Windows trials passed on a synthetic floor with existing private converted assets. This supports a Windows bridge trial; it is not installed GTA integration or skating acceptance.

Keep GTA IV rather than decompiling and rewriting the whole game in Rust. This is an engineering recommendation: it retains the world, renderer, traffic, vehicles and missions while focusing work on collision, input and presentation. The existing MW2/Skate host provides a reusable Session, not a GTA importer or replacement GTA gameplay implementation. [Source comparison](2026-10-08-gtaiv-live-diagnostic-tooling.md).

## Exact source and experiment

The worker used an exact Git archive of upstream `f608f85e407ff1b7689d54a9aafdd16e95711ac4`, exporting only its Skate subtree. It directly uses the real public `skate_host::bridge::Session`: `new`, `activate`, `tick`, `pose` and `suspend_input`. No upstream source was changed. The added harness is separate from the installed adapter. [Pinned Session implementation](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-host/src/physics/bridge.rs).

The private worker accepts prepare, tick and stop records with ride identity and sequence; it returns ordered pose summaries. Three ride cycles reuse the same Session. Neutral, push and steering each advance 240 requested ticks, for 720 returned poses per full playback trial. The worker validates finite root, velocity and bone matrices internally; the transport sends movement and bone count, not the full skeleton or rendered picture.

Linux deadline injection suspends the owned child with `SIGSTOP`. Windows deadline injection sends a diagnostic-only request that sleeps for two seconds. Each parent detects the missing response at its 250 ms deadline and terminates only its owned evaluation child. No GTA process was stopped, restarted or terminated by these trials. No game files, controls or camera were changed.

## Checks and timings

All builds used the committed adapter dependency lock with only the root package name changed for the new harness, and `--locked --offline`. Debug and optimized Linux builds passed; the optimized Windows build passed for `i686-pc-windows-gnu`. A 64-bit Windows worker was not built or tested.

| Observed Windows optimized workload | Prepare/remount | Mean request round trip | Maximum request round trip |
| --- | --- | --- | --- |
| First preparation, neutral playback | 17.686 s | 3.446 ms | 6.606 ms |
| Warm remount, push playback | 0.013 s | 3.117 ms | 7.874 ms |
| Warm remount, steering playback | 0.012 s | 3.260 ms | 13.940 ms |

The Session reported a 16.667 ms simulation period. These are sequential synthetic requests, not frame-paced GTA measurements or a sustained gameplay guarantee. Optimized Linux means were 2.535–3.515 ms; warm remounts were 11.7–12.3 ms. The unoptimized Linux trial averaged 15.9–17.4 ms, illustrating why its timing cannot select a production budget.

Passed in Linux and Windows:

- Real Session preparation, 720 finite ordered movement responses, and distinct push/steering motion.
- Three ride/stop cycles retaining a warm Session and normal worker shutdown.
- Refusal of an incoming stale ride identity.
- A requested or injected stall detected at a 250 ms deadline.
- Owned-child termination detected; a fresh child subsequently prepares, ticks and stops.

The first Windows trial returned its 720 poses but failed its final two-second shutdown check. The corrected trial measured bounded shutdown with a ten-second deadline and passed; its maximum observed shutdown wait was 0.014 s. The initial failure's cause is unresolved. This is not evidence that shutdown always finishes within either observation. An earlier Windows idle-pipe timeout was replaced with actual requested-stall injection before the final passing run.

Reproduction commands for the retained temporary setup:

```sh
python3 /tmp/combine-skate-worker-evaluation/evaluate.py --release
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '\\wsl.localhost\Ubuntu\tmp\combine-skate-worker-evaluation\evaluate-windows.ps1'
```

The Windows command requires the existing private asset pointer and reviewed WSL/Windows access; neither command installs into GTA. Source, exact pin, build lock, binary hashes and raw results are retained privately. The Windows assets are read from their existing location, not copied into Git or uploaded.

## Remaining bridge work

The owner confirmed the next acceptance seam: real GTA → worker → GTA, mounting/push/steering on one real surface, dismount, and native control/camera restoration when the worker stalls or exits.

The current parent harnesses wait synchronously. A game-side adapter must use nonblocking bounded exchange; preparation must complete before player control transfers. It must discard stale outgoing poses after dismount/restart, not merely reject stale incoming requests. Duplicate/out-of-order sequence behavior and collision revisions need bridge checks. The harness's trusted line decoder is not a bounded production decoder.

GTA collision, scale, headings, scene/controller ownership, visible movement/camera, walking/vehicle recovery and live fault restoration remain unverified. This trial does not resolve the sampled surface's over-0.05-metre refusal. Retaining a warm Session must not reuse outdated collision when the surface changes. Full skeleton/board presentation remains additional work.

Repository check: `python3 scripts/verify.py` passed 43 tests and links in 47 tracked documents. Newly added notes and the ADR were checked separately because the gate excludes untracked Markdown. The full upstream host-test suite remains unverified: the pinned host references missing `src/tests/map_startup.rs`. Existing upstream warnings remain unchanged. #20 stays open; no source integration, deployment, release or owner gameplay acceptance is claimed.
