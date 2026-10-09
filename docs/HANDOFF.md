# Current context

## Current task

Reviewed: 2026-10-09

Task: [#20 — Mount → move → dismount](https://github.com/Jpatching/combine/issues/20).
Fetch its body and comments before resuming. The owner's current request selects work.

Source branch: `integration/gtaiv-skate-loop`

Source revision: `b403377481a33e407aeb81b78b8d38984aac4735`

Disposition: pushed; [PR #23](https://github.com/Jpatching/combine/pull/23) is draft and unmerged; complete gameplay acceptance is pending.

**A complete repeatable GTA IV + Skate ride has not passed.** Offline GTA IV supplies
normal city gameplay; Skate supplies riding. The owner approved evaluating a separate
worker alongside the preserved in-process candidate. See the
[host decision](adr/0001-preserve-offline-gta-gameplay.md) and [glossary](../GLOSSARY.md).
The issue owns acceptance and approved scope; this file is the starting pointer.

## Evidence

Latest runtime evidence: [2026-10-09 diagnosis](https://github.com/Jpatching/combine/issues/20#issuecomment-6078907484).

- At the source revision above, two unchanged-location mount attempts refused with
  `over-0.05-metres`, retaining GTA control. Playback never began. This reproduces
  a rejecting condition; the surface root cause remains unknown.
- Earlier trials passed actual worker mount/dismount and worker-failure control
  restoration. A later camera-definition fix passed camera destruction during
  mounted dismount. These are separate observations, not one accepted full ride.
  [Earlier progress](https://github.com/Jpatching/combine/issues/20#issuecomment-6067861907),
  [camera correction](https://github.com/Jpatching/combine/issues/20#issuecomment-6068900739).
- Push, both steering directions, usable camera, walking/vehicle recovery,
  scale/alignment and corrected mounted fault-camera recovery have not passed
  together. Owner gameplay acceptance remains pending; #21/#22 remain blocked.
- The latest diagnosis records 43 repository tests and links in 47 tracked
  documents passing. PR #23 has three successful CI jobs at the recorded revision.
  These are source checks, not playable acceptance. Full upstream host tests remain
  unverified because pinned `src/tests/map_startup.rs` is missing.

## Next step

Resume #20 only from its current live verdict. The recorded mount refusal is the
first blocker to riding. Use a bounded reproduction tied to the exact source and
installed runtime, then test a specific hypothesis; repeat setup only when integrity,
location or runtime state has changed. Game execution needs current task authority.

Collision feasibility research remains separate from live riding diagnosis. Read the
issue's latest research prerequisite before starting it; this context cleanup does
not select a new architecture, relax the surface guard or authorize a launch.

Preserved research is dated evidence, not the next task:
[worker evaluation](../research/results/2026-10-08-separate-skate-worker.md),
[native diagnostics](../research/results/2026-10-08-gtaiv-live-diagnostic-tooling.md),
[helper alternatives](../research/results/2026-10-08-gtaiv-runtime-helper-alternatives.md),
[MW2/GTA comparison](../research/results/2026-10-08-skate-mw2-gtaiv-integration.md).
GTA source and runtime instructions remain on the
[recorded candidate](https://github.com/Jpatching/combine/blob/b403377481a33e407aeb81b78b8d38984aac4735/tools/gtaiv-skate/README.md).

## Session close

Follow the [context maintenance procedure](agents/current-context.md) at a task
boundary: preserve findings, record the exact verdict and next step, and state whether
work is merged, pushed but blocked, or a preserved experiment. A temporary handoff
links these artifacts. Source integration, runtime observation and owner acceptance
remain separate. Recheck Git and the live tracker before relying on this snapshot.

## Historical reference

Fortnite/#4 is historical context for the current GTA work:
[previous snapshot](archive/HANDOFF-2026-10-09-fortnite-context.md),
[Fortnite contract](FORTNITE_SKATE.md).
Recovery, parked Synergy and earlier MW2/Minecraft observations remain in the
[October 7 archive](archive/HANDOFF-2026-10-07.md). Preserve retained branches and
original runtime backups; consult `git worktree list` before resuming an experiment.
