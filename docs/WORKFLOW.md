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
  C-017's approved behavior is recorded in the menu guide and D-013. D-015
  corrects the implementation: execute Synergy itself through the existing GSC
  engine. Resume C-016 from its board draft; the native menu was rejected. Hide HUD is deferred and is not a prerequisite.
- Full gate: `python3 scripts/verify.py`. Native build/render and Windows trials
  use the menu guide and [baseline runbook](WINDOWS_BASELINE.md).
- Passing checks is not owner acceptance. Source publication still requires the
  owner's replacement-menu acceptance; no CI/CD or new gameplay was added here.

Update the same Project draft at each phase change with evidence, next actor and
blockers. The roadmap is another view of those items. Start date and Target date fields
exist; starting implementation records the actual start once and targets stay
blank until scheduled. The existing view is preserved; its visual date-field
mapping still needs a UI check because the exposed API does not report it.

```text
Implement -> checks pass -> isolated trial + exact launch instructions
                 | fail -> fix             | owner tries -> fix / accept
                                           v
                   accepted source -> authorized publication/review/merge
```

Each playable slice's card must link its build/hash, launch command or shortcut
and short owner checklist before requesting a trial. Use the menu guide's trial
procedure. Commits, PRs, merges and releases get actual links/evidence when they
exist; the public `origin` is https://github.com/Jpatching/combine. Repository creation
and ADMIN/PUBLIC access are verified. Source push, PR, merge, release and automatic
deployment have not occurred. The refreshed project instructions retain the
replacement-acceptance prerequisite for source publication.
Keep historical evidence and the catalogue as references; resume from Now and
the relevant contract, without copying whole archives into each new handoff.

Combine's review adapter is `scripts/prepare-trickshot-trial.ps1`, using shared
`review-bundle.ps1` and `review-launch.ps1` from the global workflow directory.
The project checklist is `templates/intervention-checklist.txt`; exact commands
are in the menu guide. Supply issue, full source commit, upstream pins, ordered
patch hashes and passing checks to the local evidence manifest. Keep raw paths,
launch history and the owner verdict with that versioned review folder; share
only redacted evidence on the private Project. Local checkpoint commits are
authorized by the selected plan and precede the final build/test handoff.
