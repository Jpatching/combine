# Combine workflow configuration

Open [Combine — Now](https://github.com/users/Jpatching/projects/5/views/4) for
current work. The private board owns active status; [BACKLOG](../BACKLOG.md)
preserves earlier history. [Tracker operations](agents/issue-tracker.md) define
updates and offline recovery.

The reusable guide, skill adaptations, hook and validation live outside this
repository under `~/.codex/workflows/solo-development/` and the global
`matt-workflow` skill. This document contains Combine-specific configuration only.

- Destination: proper Synergy menu plus trickshot hit radius, without Combine
  practice additions. Existing work stays preserved.
- Requirements: [menu guide](TRICKSHOT_MENU.md); decisions: [DECISIONS](DECISIONS.md).
- Current evidence: [source coverage](../research/results/2026-10-04-menu-coverage.md).
  C-017's approved choices are recorded in the menu guide and D-013; to-spec and
  to-tickets finalised the Intervention contract. Resume implementation from its
  board draft. Hide HUD is deferred and is not a prerequisite.
- Full gate: `python3 scripts/verify.py`. Native build/render and Windows trials
  use the menu guide and [baseline runbook](WINDOWS_BASELINE.md).
- Passing checks is not owner acceptance. Source publication still requires the
  owner's replacement-menu acceptance; no CI/CD or new gameplay was added here.

Update the same Project draft at each phase change with evidence, next actor and
blockers. The roadmap is another view of those items; no start/target-date fields
are configured, so it currently supplies no delivery schedule. Keep dates based
on an agreed schedule, not guesses.

```text
Implement -> checks pass -> isolated trial + exact launch instructions
                 | fail -> fix             | owner tries -> fix / accept
                                           v
                   accepted source -> authorized publication/review/merge
```

Each playable slice's card must link its build/hash, launch command or shortcut
and short owner checklist before requesting a trial. Use the menu guide's trial
procedure. Commits, PRs, merges and releases get actual links/evidence when they
exist; there is currently no configured source remote or automatic deployment.
Keep historical evidence and the catalogue as references; resume from Now and
the relevant contract, without copying whole archives into each new handoff.
